import asyncio
import json
from datetime import datetime, timedelta, timezone

import pytest

import trade_full as ml


UTC = timezone.utc


def _write_jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, default=str) + "\n")


def _sample_feature(
    *,
    direction: str,
    ts: datetime,
    idx: int = 0,
    seconds_remaining: int = 50,
    phase_bucket: str = "LATE_EXEC",
    elapsed_fraction: float | None = None,
) -> ml.SignalFeatures:
    beat_price = 100.0
    gap_signed_pct = 0.18 if direction == "UP" else -0.18
    btc_price = beat_price * (1.0 + gap_signed_pct / 100.0)
    window_start = ts - timedelta(seconds=250)
    window_end = window_start + timedelta(seconds=300)
    up_odds = 0.58 if direction == "UP" else 0.42
    down_odds = 1.0 - up_odds
    fair_up = 0.82 if direction == "UP" else 0.18
    fair_down = 1.0 - fair_up
    signal_alignment = 5
    signed_alignment = 5.0 if direction == "UP" else -5.0
    odds_vel = 0.004 if direction == "UP" else -0.004
    if elapsed_fraction is None:
        elapsed_fraction = max(0.0, min(1.0, (300 - seconds_remaining) / 300.0))

    return ml.SignalFeatures(
        row_id=f"row-{idx}",
        ts=ml._iso_z(ts),
        condition_id=f"cond-{idx}",
        window_start_at=ml._iso_z(window_start),
        window_end_at=ml._iso_z(window_end),
        beat_price=beat_price,
        btc_price=btc_price,
        up_odds=up_odds,
        down_odds=down_odds,
        gap_pct=abs(gap_signed_pct),
        gap_signed_pct=gap_signed_pct,
        seconds_remaining=seconds_remaining,
        signal_alignment=signal_alignment,
        signed_alignment=signed_alignment,
        odds_vel=odds_vel,
        odds_vel_accel=0.001 if direction == "UP" else -0.001,
        cvd_divergence=1 if direction == "UP" else -1,
        macd_histogram=12.0 if direction == "UP" else -12.0,
        bb_pct_b=0.78 if direction == "UP" else 0.22,
        rsi=61.0 if direction == "UP" else 39.0,
        momentum_pct=0.22 if direction == "UP" else -0.22,
        is_late_window=1,
        is_bandar_zone=0,
        is_proximity_risk=0,
        price_roc_15s=0.12 if direction == "UP" else -0.12,
        price_roc_30s=0.24 if direction == "UP" else -0.24,
        cvd_change_last_30s=1.4 if direction == "UP" else -1.4,
        odds_edge_strength=up_odds - down_odds,
        elapsed_fraction=elapsed_fraction,
        fair_up=fair_up,
        fair_down=fair_down,
        edge_up=ml.compute_edge(fair_up, up_odds),
        edge_down=ml.compute_edge(fair_down, down_odds),
        direction_bias=direction,
        dip_label="SUSTAINED_ABOVE" if direction == "UP" else "SUSTAINED_MOVE",
        feature_source="test",
        phase_bucket=phase_bucket,
    )


def test_runtime_signal_engine_falls_back_without_model(tmp_path):
    registry = ml.ModelRegistry(tmp_path / "models")
    engine = ml.RuntimeSignalEngine(registry)

    prediction = engine.predict(_sample_feature(direction="UP", ts=datetime.now(UTC)))

    assert prediction.source == "fallback"
    assert prediction.signal == ml.LABEL_BUY_UP
    assert prediction.prob_up > prediction.prob_down


def test_backfill_ml_labels_from_feature_rows(tmp_path):
    log_dir = tmp_path / "logs"
    ts = datetime(2026, 4, 10, 0, 0, tzinfo=UTC)
    feature = _sample_feature(direction="UP", ts=ts, idx=1)
    _write_jsonl(log_dir / "ml_features_2026-04-10.jsonl", [feature.to_record()])
    _write_jsonl(
        log_dir / "prices_2026-04-10.jsonl",
        [
            {
                "ts": ml._iso_z(parse_ts),
                "btc": btc,
                "buy_vol": 0.1,
                "sell_vol": 0.0,
                "cvd": 0.1,
                "up_odds": 0.6,
                "dn_odds": 0.4,
            }
            for parse_ts, btc in [
                (ts - timedelta(seconds=30), 100.10),
                (ml.ml_parse_utc_ts(feature.window_end_at), 100.30),
            ]
        ],
    )

    appended = ml.backfill_ml_labels(log_dir)
    label_files = list(log_dir.glob("ml_labels_*.jsonl"))

    assert appended == 1
    assert len(label_files) == 1
    contents = label_files[0].read_text(encoding="utf-8")
    assert ml.LABEL_BUY_UP in contents


def test_train_outcome_model_and_use_active_model(tmp_path):
    log_dir = tmp_path / "logs"
    model_dir = tmp_path / "models"
    start = datetime(2026, 4, 1, 0, 0, tzinfo=UTC)

    features = []
    labels = []
    for idx in range(180):
        direction = "UP" if idx % 2 == 0 else "DOWN"
        ts = start + timedelta(minutes=5 * idx)
        feature = _sample_feature(direction=direction, ts=ts, idx=idx)
        features.append(feature.to_record())
        labels.append(
            ml.ResolvedLabelRecord(
                row_id=feature.row_id,
                condition_id=feature.condition_id,
                resolution_ts=feature.window_end_at,
                resolved_label=ml.LABEL_BUY_UP if direction == "UP" else ml.LABEL_BUY_DOWN,
                resolved_btc_price=100.25 if direction == "UP" else 99.75,
            ).to_record()
        )

    _write_jsonl(log_dir / "ml_features_2026-04-10.jsonl", features)
    _write_jsonl(log_dir / "ml_labels_2026-04-10.jsonl", labels)

    result = ml.train_outcome_model(
        log_dir=log_dir,
        models_dir=model_dir,
        promotion_state="active",
        min_rows=100,
    )
    registry = ml.ModelRegistry(model_dir)
    engine = ml.RuntimeSignalEngine(registry)

    prediction = engine.predict(_sample_feature(direction="UP", ts=start + timedelta(days=3), idx=999))

    assert result["metrics"]["rows_total"] == 180
    assert result["manifest"]["promotion_state"] == "active"
    assert prediction.source == "ml"
    assert prediction.signal == ml.LABEL_BUY_UP


def test_backfill_prefers_chainlink_settlement_over_binance(tmp_path):
    log_dir = tmp_path / "logs"
    ts = datetime(2026, 4, 10, 0, 0, tzinfo=UTC)
    feature = _sample_feature(direction="UP", ts=ts, idx=44)
    _write_jsonl(log_dir / "ml_features_2026-04-10.jsonl", [feature.to_record()])
    _write_jsonl(
        log_dir / "prices_2026-04-10.jsonl",
        [
            {
                "ts": feature.window_end_at,
                "btc": 99.80,
                "buy_vol": 0.1,
                "sell_vol": 0.0,
                "cvd": 0.1,
                "up_odds": 0.6,
                "dn_odds": 0.4,
            }
        ],
    )
    _write_jsonl(
        log_dir / "settlements_2026-04-10.jsonl",
        [
            ml.SettlementRecord(
                condition_id=feature.condition_id,
                resolved_at=feature.window_end_at,
                settlement_price=100.40,
                settlement_source="chainlink_market_resolved",
                settlement_source_priority=ml._label_source_priority("chainlink_market_resolved"),
                chainlink_settlement_price=100.40,
            ).to_record()
        ],
    )

    appended = ml.backfill_ml_labels(log_dir)
    label_file = next(log_dir.glob("ml_labels_*.jsonl"))
    record = json.loads(label_file.read_text(encoding="utf-8").strip())

    assert appended == 1
    assert record["resolved_label"] == ml.LABEL_BUY_UP
    assert record["label_source"] == "chainlink_market_resolved"
    assert record["chainlink_settlement_price"] == 100.40


def test_resolve_label_treats_equal_final_price_as_up():
    ts = datetime(2026, 4, 10, 0, 0, tzinfo=UTC)
    feature = _sample_feature(direction="UP", ts=ts, idx=45).to_record()

    label = ml.resolve_label_for_row(
        feature,
        ml.pd.DataFrame(),
        override_price=float(feature["beat_price"]),
        label_source="chainlink_market_resolved",
        override_resolution_ts=feature["window_end_at"],
        settlement_source_priority=ml._label_source_priority("chainlink_market_resolved"),
    )

    assert label is not None
    assert label.resolved_label == ml.LABEL_BUY_UP


def test_grouped_window_splits_do_not_overlap_conditions(tmp_path):
    rows = []
    start = datetime(2026, 4, 1, 0, 0, tzinfo=UTC)
    for idx in range(8):
        for sample in range(3):
            ts = start + timedelta(minutes=5 * idx, seconds=5 * sample)
            feature = _sample_feature(direction="UP" if idx % 2 == 0 else "DOWN", ts=ts, idx=idx * 10 + sample)
            feature.condition_id = f"cond-{idx}"
            rows.append(feature.to_record() | {"resolved_label": ml.LABEL_BUY_UP if idx % 2 == 0 else ml.LABEL_BUY_DOWN})
    frame = ml._prepare_training_frame(ml.pd.DataFrame(rows))

    splits = ml._window_split_indices(frame, n_splits=3, purge_windows=1)

    assert splits
    for train_idx, valid_idx in splits:
        train_conditions = set(frame.iloc[train_idx]["condition_id"])
        valid_conditions = set(frame.iloc[valid_idx]["condition_id"])
        assert not (train_conditions & valid_conditions)


def test_shadow_training_does_not_replace_existing_active_manifest(tmp_path):
    log_dir = tmp_path / "logs"
    model_dir = tmp_path / "models"
    start = datetime(2026, 4, 1, 0, 0, tzinfo=UTC)

    features = []
    labels = []
    for idx in range(180):
        direction = "UP" if idx % 2 == 0 else "DOWN"
        ts = start + timedelta(minutes=5 * idx)
        feature = _sample_feature(direction=direction, ts=ts, idx=idx)
        features.append(feature.to_record())
        labels.append(
            ml.ResolvedLabelRecord(
                row_id=feature.row_id,
                condition_id=feature.condition_id,
                resolution_ts=feature.window_end_at,
                resolved_label=ml.LABEL_BUY_UP if direction == "UP" else ml.LABEL_BUY_DOWN,
                resolved_btc_price=100.25 if direction == "UP" else 99.75,
            ).to_record()
        )

    _write_jsonl(log_dir / "ml_features_2026-04-10.jsonl", features)
    _write_jsonl(log_dir / "ml_labels_2026-04-10.jsonl", labels)

    registry = ml.ModelRegistry(model_dir)
    active_result = ml.train_outcome_model(
        log_dir=log_dir,
        models_dir=model_dir,
        promotion_state="active",
        min_rows=100,
        min_distinct_windows=50,
    )
    active_version = active_result["manifest"]["model_version"]

    shadow_result = ml.train_outcome_model(
        log_dir=log_dir,
        models_dir=model_dir,
        promotion_state="shadow",
        min_rows=100,
        min_distinct_windows=50,
    )
    applied = ml.auto_apply_trained_model(
        shadow_result,
        registry,
        auto_promote=False,
        fallback_state="shadow",
        activation_reason="test_shadow",
    )

    active_manifest = registry.load_manifest()

    assert applied["manifest"]["promotion_state"] == "shadow"
    assert active_manifest is not None
    assert active_manifest.model_version == active_version


def test_runtime_signal_engine_hot_reloads_auto_promoted_model(tmp_path):
    log_dir = tmp_path / "logs"
    model_dir = tmp_path / "models"
    start = datetime(2026, 4, 1, 0, 0, tzinfo=UTC)

    features = []
    labels = []
    for idx in range(180):
        direction = "UP" if idx % 2 == 0 else "DOWN"
        ts = start + timedelta(minutes=5 * idx)
        feature = _sample_feature(direction=direction, ts=ts, idx=idx)
        features.append(feature.to_record())
        labels.append(
            ml.ResolvedLabelRecord(
                row_id=feature.row_id,
                condition_id=feature.condition_id,
                resolution_ts=feature.window_end_at,
                resolved_label=ml.LABEL_BUY_UP if direction == "UP" else ml.LABEL_BUY_DOWN,
                resolved_btc_price=100.25 if direction == "UP" else 99.75,
            ).to_record()
        )

    _write_jsonl(log_dir / "ml_features_2026-04-10.jsonl", features)
    _write_jsonl(log_dir / "ml_labels_2026-04-10.jsonl", labels)

    registry = ml.ModelRegistry(model_dir)
    engine = ml.RuntimeSignalEngine(registry)
    result = ml.train_outcome_model(
        log_dir=log_dir,
        models_dir=model_dir,
        promotion_state="shadow",
        min_rows=100,
    )
    result["metrics"]["ready_for_active"] = True
    result = ml.auto_apply_trained_model(
        result,
        registry,
        auto_promote=True,
        fallback_state="shadow",
        activation_reason="test_auto_promote",
    )

    prediction = engine.predict(_sample_feature(direction="UP", ts=start + timedelta(days=3), idx=1001))

    assert result["manifest"]["promotion_state"] == "active"
    assert prediction.source == "ml"
    assert prediction.signal == ml.LABEL_BUY_UP


def test_runtime_policy_uses_bucketed_thresholds_and_skip_codes():
    previous = ml.BET_FREQUENCY_EXPANSION_PHASE
    ml.BET_FREQUENCY_EXPANSION_PHASE = "C"
    try:
        policy = ml.RuntimePolicy()
        reserve_feature = _sample_feature(
            direction="UP",
            ts=datetime.now(UTC),
            idx=900,
            seconds_remaining=110,
            phase_bucket="RESERVE",
        )

        reserve_skip = policy.decide(
            reserve_feature,
            0.73,
            0.27,
            reason_prefix="ml",
            source="ml",
            model_version="test",
            promotion_state="active",
        )
        reserve_buy = policy.decide(
            reserve_feature,
            0.75,
            0.25,
            reason_prefix="ml",
            source="ml",
            model_version="test",
            promotion_state="active",
        )

        assert reserve_skip.signal == ml.LABEL_SKIP
        assert reserve_skip.runtime_skip_reason_code == "RUNTIME_CANDIDATE_FLOOR"
        assert reserve_skip.candidate_confidence_floor == pytest.approx(0.74)
        assert reserve_buy.signal == ml.LABEL_BUY_UP
    finally:
        ml.BET_FREQUENCY_EXPANSION_PHASE = previous


def test_runtime_policy_keeps_late_exec_safety_floor():
    previous = ml.BET_FREQUENCY_EXPANSION_PHASE
    ml.BET_FREQUENCY_EXPANSION_PHASE = "C"
    try:
        policy = ml.RuntimePolicy()
        late_feature = _sample_feature(
            direction="UP",
            ts=datetime.now(UTC),
            idx=901,
            seconds_remaining=35,
            phase_bucket="LATE_EXEC",
        )

        prediction = policy.decide(
            late_feature,
            0.75,
            0.25,
            reason_prefix="ml",
            source="ml",
            model_version="test",
            promotion_state="active",
        )

        assert prediction.signal == ml.LABEL_SKIP
        assert prediction.runtime_skip_reason_code == "RUNTIME_CANDIDATE_FLOOR"
    finally:
        ml.BET_FREQUENCY_EXPANSION_PHASE = previous


def test_phase_c_is_default_when_env_not_set():
    assert ml.BET_FREQUENCY_EXPANSION_PHASE == "C"


def test_threshold_tuner_prefers_highest_coverage_profile_above_guardrail(tmp_path):
    log_dir = tmp_path / "logs"
    ts = datetime(2026, 4, 11, 0, 0, tzinfo=UTC)
    records = []
    for idx in range(20):
        records.append(
            {
                "ts": ml._iso_z(ts + timedelta(minutes=5 * idx)),
                "event": "prediction_resolved",
                "row_id": f"row-low-{idx}",
                "condition_id": f"cond-low-{idx}",
                "signal": "BUY_UP",
                "candidate_phase": "RESERVE",
                "phase_bucket": "RESERVE",
                "confidence": 0.72,
                "prediction_correct": False,
                "resolved_at": ml._iso_z(ts + timedelta(minutes=5 * idx, seconds=1)),
            }
        )
    for idx in range(15):
        records.append(
            {
                "ts": ml._iso_z(ts + timedelta(minutes=5 * (idx + 20))),
                "event": "prediction_resolved",
                "row_id": f"row-mid-{idx}",
                "condition_id": f"cond-mid-{idx}",
                "signal": "BUY_UP",
                "candidate_phase": "RESERVE",
                "phase_bucket": "RESERVE",
                "confidence": 0.74,
                "prediction_correct": True,
                "resolved_at": ml._iso_z(ts + timedelta(minutes=5 * (idx + 20), seconds=1)),
            }
        )
    for idx in range(15):
        records.append(
            {
                "ts": ml._iso_z(ts + timedelta(minutes=5 * (idx + 35))),
                "event": "prediction_resolved",
                "row_id": f"row-high-{idx}",
                "condition_id": f"cond-high-{idx}",
                "signal": "BUY_UP",
                "candidate_phase": "EARLY_EXEC",
                "phase_bucket": "EARLY_EXEC",
                "confidence": 0.76,
                "prediction_correct": True,
                "resolved_at": ml._iso_z(ts + timedelta(minutes=5 * (idx + 35), seconds=1)),
            }
        )
    _write_jsonl(log_dir / "prediction_analytics_2026-04-11.jsonl", records)

    tuned = ml.tune_runtime_thresholds_from_shadow_data(log_dir, min_windows=40)

    assert tuned["threshold_source"] == "auto_tuned"
    assert tuned["runtime_thresholds"]["reserve"] == pytest.approx(0.74)
    assert tuned["runtime_thresholds"]["early_exec"] == pytest.approx(0.76)


def test_threshold_tuner_prefers_realized_ev_when_execution_economics_exist(tmp_path):
    log_dir = tmp_path / "logs"
    ts = datetime(2026, 4, 11, 12, 0, tzinfo=UTC)
    records = []
    for idx in range(20):
        records.append(
            {
                "ts": ml._iso_z(ts + timedelta(minutes=5 * idx)),
                "event": "prediction_resolved",
                "row_id": f"row-cheap-winrate-{idx}",
                "condition_id": f"cond-cheap-winrate-{idx}",
                "signal": "BUY_UP",
                "candidate_phase": "RESERVE",
                "phase_bucket": "RESERVE",
                "confidence": 0.72,
                "prediction_correct": idx < 17,
                "payout_per_dollar": 1.10,
                "net_edge": -0.208,
                "resolved_at": ml._iso_z(ts + timedelta(minutes=5 * idx, seconds=1)),
            }
        )
    for idx in range(20):
        records.append(
            {
                "ts": ml._iso_z(ts + timedelta(minutes=5 * (idx + 20))),
                "event": "prediction_resolved",
                "row_id": f"row-clean-edge-{idx}",
                "condition_id": f"cond-clean-edge-{idx}",
                "signal": "BUY_UP",
                "candidate_phase": "RESERVE",
                "phase_bucket": "RESERVE",
                "confidence": 0.80,
                "prediction_correct": idx < 16,
                "payout_per_dollar": 2.00,
                "net_edge": 0.60,
                "resolved_at": ml._iso_z(ts + timedelta(minutes=5 * (idx + 20), seconds=1)),
            }
        )
    _write_jsonl(log_dir / "prediction_analytics_2026-04-11.jsonl", records)

    tuned = ml.tune_runtime_thresholds_from_shadow_data(log_dir, min_windows=40, min_win_rate=0.80)

    assert tuned["threshold_source"] == "auto_tuned"
    assert tuned["runtime_thresholds"]["reserve"] == pytest.approx(0.80)
    assert tuned["threshold_tuning_summary"]["selected_metrics"]["avg_realized_ev_per_trade"] > 0.50


def test_threshold_tuner_degrades_when_recent_validation_misses_guardrail(tmp_path):
    log_dir = tmp_path / "logs"
    ts = datetime(2026, 4, 12, 0, 0, tzinfo=UTC)
    records = []
    for idx in range(30):
        records.append(
            {
                "ts": ml._iso_z(ts + timedelta(minutes=5 * idx)),
                "event": "prediction_resolved",
                "row_id": f"row-{idx}",
                "condition_id": f"cond-{idx}",
                "signal": "BUY_UP",
                "candidate_phase": "EARLY_EXEC",
                "phase_bucket": "EARLY_EXEC",
                "confidence": 0.80,
                "prediction_correct": idx < 20,
                "resolved_at": ml._iso_z(ts + timedelta(minutes=5 * idx, seconds=1)),
            }
        )
    _write_jsonl(log_dir / "prediction_analytics_2026-04-12.jsonl", records)

    tuned = ml.tune_runtime_thresholds_from_shadow_data(
        log_dir,
        min_windows=10,
        min_win_rate=0.60,
    )

    assert tuned["threshold_source"] == "degraded_auto_guard"
    assert tuned["threshold_tuning_summary"]["selected"] == "degraded_auto_guard"
    assert tuned["runtime_thresholds"]["early_exec"] > 0.80
    assert tuned["runtime_thresholds"]["source"] == "degraded_auto_guard"


def test_strategy_audit_returns_no_data_for_missing_logs(tmp_path):
    report = ml.audit_strategy_decisions(tmp_path / "logs")

    assert report["rows"] == 0
    assert report["message"] == "no data"


def test_market_client_refresh_session_rotates_bundle_and_requests_ws_reconnect(monkeypatch):
    class FakeCreds:
        def __init__(self, suffix: str):
            self.api_key = f"key-{suffix}"
            self.api_secret = f"secret-{suffix}"
            self.api_passphrase = f"pass-{suffix}"

    class FakeClient:
        def __init__(self, suffix: str):
            self.creds = FakeCreds(suffix)

        def get_balance_allowance(self, *_args, **_kwargs):
            return {"balance": "1000000", "allowance": "0"}

    class FakeHttp:
        def __init__(self, suffix: str):
            self.suffix = suffix
            self.closed = False

        async def aclose(self):
            self.closed = True

    build_count = {"client": 0, "http": 0}
    created_http: list[FakeHttp] = []

    def fake_build_client(self):
        build_count["client"] += 1
        return FakeClient(str(build_count["client"]))

    def fake_build_http_client(self):
        build_count["http"] += 1
        http = FakeHttp(str(build_count["http"]))
        created_http.append(http)
        return http

    monkeypatch.setattr(ml, "POLY_ETH_PRIVATE_KEY", "0xabc")
    monkeypatch.setattr(ml, "POLY_HTTP_CLOSE_GRACE_S", 0)
    monkeypatch.setattr(ml.MarketClient, "_build_client", fake_build_client)
    monkeypatch.setattr(ml.MarketClient, "_build_http_client", fake_build_http_client)

    async def _run():
        market = ml.MarketClient()
        original_http = market._http
        ok, detail = await market.refresh_session()
        await asyncio.sleep(0)
        snapshot = market.session_snapshot()
        reconnect_requested = market.consume_market_ws_reconnect_request()
        await market.close()
        return ok, detail, snapshot, reconnect_requested, original_http

    ok, detail, snapshot, reconnect_requested, original_http = asyncio.run(_run())

    assert ok is True
    assert detail == ""
    assert snapshot["generation"] == 1
    assert snapshot["last_auth_success_at"]
    assert reconnect_requested is True
    assert build_count["client"] == 2
    assert build_count["http"] == 2
    assert original_http.closed is True


def test_market_client_heartbeat_failure_marks_session_degraded(monkeypatch):
    class FakeCreds:
        api_key = "key"
        api_secret = "secret"
        api_passphrase = "pass"

    class FakeClient:
        def __init__(self):
            self.creds = FakeCreds()
            self.heartbeat_ids = []

        def post_heartbeat(self, heartbeat_id=None):
            self.heartbeat_ids.append(heartbeat_id)
            raise RuntimeError("401 invalid signature")

    class FakeHttp:
        async def aclose(self):
            return None

    monkeypatch.setattr(ml.MarketClient, "_build_client", lambda self: FakeClient())
    monkeypatch.setattr(ml.MarketClient, "_build_http_client", lambda self: FakeHttp())

    async def _run():
        market = ml.MarketClient()
        ok = await market.send_heartbeat()
        snapshot = market.session_snapshot()
        heartbeat_ids = market._client.heartbeat_ids
        await market.close()
        return ok, snapshot, heartbeat_ids

    ok, snapshot, heartbeat_ids = asyncio.run(_run())

    assert ok is False
    assert heartbeat_ids == [None]
    assert snapshot["consecutive_auth_failures"] == 1
    assert "invalid signature" in snapshot["last_auth_error"].lower()


def test_market_client_heartbeat_supports_legacy_noarg_clients(monkeypatch):
    class FakeCreds:
        api_key = "key"
        api_secret = "secret"
        api_passphrase = "pass"

    class FakeClient:
        def __init__(self):
            self.creds = FakeCreds()
            self.calls = 0

        def post_heartbeat(self):
            self.calls += 1
            return {"ok": True}

    class FakeHttp:
        async def aclose(self):
            return None

    monkeypatch.setattr(ml.MarketClient, "_build_client", lambda self: FakeClient())
    monkeypatch.setattr(ml.MarketClient, "_build_http_client", lambda self: FakeHttp())

    async def _run():
        market = ml.MarketClient()
        ok = await market.send_heartbeat()
        snapshot = market.session_snapshot()
        calls = market._client.calls
        await market.close()
        return ok, snapshot, calls

    ok, snapshot, calls = asyncio.run(_run())

    assert ok is True
    assert calls == 1
    assert snapshot["last_heartbeat_ok_at"]


def test_market_client_place_bet_skips_when_below_live_min_order_size(monkeypatch):
    class FakeClient:
        def __init__(self):
            self.order_args = None
            self.order_type = None

        def create_market_order(self, order_args):
            self.order_args = order_args
            return {"signed": True, "price": 0.5}

        def post_order(self, signed, order_type):
            self.order_type = order_type
            return {"success": True, "orderID": "live-123"}

        def get_order_book(self, token_id):
            return {
                "bids": [{"price": "0.49", "size": "10"}],
                "asks": [{"price": "0.50", "size": "10"}],
            }

    class FakeHttp:
        async def aclose(self):
            return None

    async def fake_min_order_size(self, token_id):
        return 5.0

    monkeypatch.setattr(ml, "LIVE_TRADING", True)
    monkeypatch.setattr(ml, "POLY_ETH_PRIVATE_KEY", "0xabc")
    monkeypatch.setattr(ml.MarketClient, "_build_client", lambda self: FakeClient())
    monkeypatch.setattr(ml.MarketClient, "_build_http_client", lambda self: FakeHttp())
    monkeypatch.setattr(ml.MarketClient, "get_min_order_size", fake_min_order_size)

    async def _run():
        market = ml.MarketClient()
        result = await market.place_bet("UP", "token-up", 2.0, 0.50)
        placed_order = market._client.order_args
        order_type = market._client.order_type
        await market.close()
        return result, placed_order, order_type

    result, placed_order, order_type = asyncio.run(_run())

    assert result.success is False
    assert result.failure_code == "MIN_ORDER_SIZE"
    assert result.attempt_consumed is True
    assert placed_order is None
    assert order_type is None


def test_dynamic_fee_math_uses_net_redeemable_shares():
    fee = ml.compute_taker_fee_usdc(shares=4.0, price=0.5, fee_rate=0.072)
    est = ml.estimate_buy_net_shares(amount_usdc=2.0, price=0.5, fee_rate=0.072)

    assert ml.normalize_fee_rate(720) == pytest.approx(0.072)
    assert ml.normalize_fee_rate(7.2) == pytest.approx(0.072)
    assert fee == pytest.approx(0.072)
    assert est["gross_shares"] == pytest.approx(4.0)
    assert est["fee_usdc"] == pytest.approx(0.072)
    assert est["fee_shares"] == pytest.approx(0.144)
    assert est["net_shares"] == pytest.approx(3.856)
    assert est["payout_per_dollar"] == pytest.approx(1.928)


def test_market_client_paper_place_bet_uses_live_like_quote_without_clob_order(monkeypatch):
    class FakeClient:
        def __init__(self):
            self.create_calls = 0
            self.post_calls = 0

        def get_order_book(self, token_id):
            return {
                "bids": [{"price": "0.49", "size": "10"}],
                "asks": [{"price": "0.50", "size": "10"}],
                "min_order_size": "1",
            }

        def create_market_order(self, order_args):
            self.create_calls += 1
            raise AssertionError("paper mode must not create CLOB orders")

        def post_order(self, signed, order_type):
            self.post_calls += 1
            raise AssertionError("paper mode must not post CLOB orders")

    class FakeResponse:
        is_success = True

        def json(self):
            return {"fee_rate": 0.072}

    class FakeHttp:
        async def get(self, *args, **kwargs):
            return FakeResponse()

        async def aclose(self):
            return None

    monkeypatch.setattr(ml, "LIVE_TRADING", False)
    monkeypatch.setattr(ml.MarketClient, "_build_client", lambda self: FakeClient())
    monkeypatch.setattr(ml.MarketClient, "_build_http_client", lambda self: FakeHttp())

    async def _run():
        market = ml.MarketClient()
        result = await market.place_bet("UP", "token-up", 2.0, 0.50)
        create_calls = market._client.create_calls
        post_calls = market._client.post_calls
        await market.close()
        return result, create_calls, post_calls

    result, create_calls, post_calls = asyncio.run(_run())

    assert result.success is True
    assert result.simulated is True
    assert result.price == pytest.approx(0.5)
    assert result.gross_size == pytest.approx(4.0)
    assert result.fee_usdc == pytest.approx(0.072)
    assert result.size == pytest.approx(3.856)
    assert result.payout_per_dollar == pytest.approx(1.928)
    assert result.fee_rate_source == "fee-rate"
    assert create_calls == 0
    assert post_calls == 0


def test_market_client_place_bet_marks_transient_failures_retryable(monkeypatch):
    class FakeClient:
        def get_order_book(self, token_id):
            return {
                "bids": [{"price": "0.49", "size": "10"}],
                "asks": [{"price": "0.50", "size": "10"}],
            }

        def create_market_order(self, order_args):
            return {"signed": True, "price": 0.5}

        def post_order(self, signed, order_type):
            return {"success": False, "errorMsg": "timeout talking to matching engine"}

    class FakeHttp:
        async def aclose(self):
            return None

    async def fake_min_order_size(self, token_id):
        return 1.0

    monkeypatch.setattr(ml, "LIVE_TRADING", True)
    monkeypatch.setattr(ml, "POLY_ETH_PRIVATE_KEY", "0xabc")
    monkeypatch.setattr(ml.MarketClient, "_build_client", lambda self: FakeClient())
    monkeypatch.setattr(ml.MarketClient, "_build_http_client", lambda self: FakeHttp())
    monkeypatch.setattr(ml.MarketClient, "get_min_order_size", fake_min_order_size)

    async def _run():
        market = ml.MarketClient()
        result = await market.place_bet("UP", "token-up", 2.0, 0.50)
        await market.close()
        return result

    result = asyncio.run(_run())

    assert result.success is False
    assert result.failure_code == "TRANSIENT_NETWORK"
    assert result.retryable is True
    assert result.attempt_consumed is False


def test_market_client_place_bet_marks_fok_not_filled_retryable(monkeypatch):
    class FakeClient:
        def get_order_book(self, token_id):
            return {
                "bids": [{"price": "0.49", "size": "10"}],
                "asks": [{"price": "0.50", "size": "10"}],
            }

        def create_market_order(self, order_args):
            return {"signed": True, "price": 0.5}

        def post_order(self, signed, order_type):
            return {"success": False, "errorMsg": "FOK_ORDER_NOT_FILLED_ERROR"}

    class FakeHttp:
        async def aclose(self):
            return None

    async def fake_min_order_size(self, token_id):
        return 1.0

    monkeypatch.setattr(ml, "LIVE_TRADING", True)
    monkeypatch.setattr(ml, "POLY_ETH_PRIVATE_KEY", "0xabc")
    monkeypatch.setattr(ml.MarketClient, "_build_client", lambda self: FakeClient())
    monkeypatch.setattr(ml.MarketClient, "_build_http_client", lambda self: FakeHttp())
    monkeypatch.setattr(ml.MarketClient, "get_min_order_size", fake_min_order_size)

    async def _run():
        market = ml.MarketClient()
        result = await market.place_bet("UP", "token-up", 2.5, 0.50)
        await market.close()
        return result

    result = asyncio.run(_run())

    assert result.success is False
    assert result.failure_code == "NO_IMMEDIATE_LIQUIDITY"
    assert result.retryable is True
    assert result.attempt_consumed is False
