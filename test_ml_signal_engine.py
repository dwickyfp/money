import json
from datetime import datetime, timedelta, timezone

import trade_full as ml


UTC = timezone.utc


def _write_jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, default=str) + "\n")


def _sample_feature(*, direction: str, ts: datetime, idx: int = 0) -> ml.SignalFeatures:
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
        seconds_remaining=50,
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
        fair_up=fair_up,
        fair_down=fair_down,
        edge_up=ml.compute_edge(fair_up, up_odds),
        edge_down=ml.compute_edge(fair_down, down_odds),
        direction_bias=direction,
        dip_label="SUSTAINED_ABOVE" if direction == "UP" else "SUSTAINED_MOVE",
        feature_source="test",
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
