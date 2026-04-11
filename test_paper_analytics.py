import asyncio
from collections import deque
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest
from rich.console import Console

import trade_full as tf


class DummyNotifier:
    def __init__(self) -> None:
        self.signal_calls = []
        self.shadow_calls = []
        self.bet_calls = []

    def notify_signal(self, signal, win, snap, **kwargs) -> None:
        self.signal_calls.append((signal.signal, win.condition_id, kwargs))
        return None

    def notify_shadow_signal(self, signal, win, snap, **kwargs) -> None:
        self.shadow_calls.append((signal.signal, win.condition_id, kwargs))
        return None

    def notify_bet(self, direction, bet_size, entry_odds, win, order_id, simulated, snap) -> None:
        self.bet_calls.append((direction, bet_size, entry_odds, simulated))
        return None

    def notify_result(self, pos, state) -> None:
        return None


class DummyMarket:
    def __init__(self, positions=None, claim_result=None) -> None:
        self._positions = list(positions or [])
        self._claim_result = claim_result or tf.ClaimAttemptResult(success=False, status="failed")
        self.claim_calls = []

    async def get_current_positions(self, **_kwargs):
        return list(self._positions)

    async def claim_position(self, claim):
        self.claim_calls.append(claim.claim_id)
        return self._claim_result

    def session_snapshot(self):
        return {
            "refresh_in_progress": False,
            "consecutive_auth_failures": 0,
        }


def make_bot(tmp_path):
    bot = tf.TradingBot.__new__(tf.TradingBot)
    bot.state = tf.BotState(logger=tf.BotLogger(tmp_path / "logs"))
    bot.notifier = DummyNotifier()
    bot.decision = tf.DecisionMaker()
    bot.market = DummyMarket()
    return bot


def make_window(*, condition_id: str, beat_price: float, end_time: datetime) -> tf.WindowInfo:
    return tf.WindowInfo(
        condition_id=condition_id,
        question="BTC Up or Down?",
        start_time=end_time - timedelta(minutes=5),
        end_time=end_time,
        beat_price=beat_price,
        up_token_id="up-token",
        down_token_id="down-token",
        window_label=end_time.strftime("%H:%M"),
    )


def make_position(*, condition_id: str, direction: str, order_id: str, now: datetime) -> tf.Position:
    return tf.Position(
        condition_id=condition_id,
        direction=direction,
        token_id="token",
        size=4.0,
        entry_price=0.5,
        placed_at=now - timedelta(minutes=4),
        order_id=order_id,
        simulated=True,
        amount_usdc=2.0,
        window_beat=100.0,
        window_end_at=now - timedelta(seconds=5),
        elapsed_at_bet=240,
        gap_pct_at_bet=0.15,
        ai_confidence=0.82,
        ai_raw_confidence=0.86,
        signal_alignment=5,
    )


def test_load_paper_analytics_rebuilds_clean_stats_and_pending_records(tmp_path):
    logger = tf.BotLogger(tmp_path / "logs")
    now = datetime.now(timezone.utc)

    resolved = tf.WindowPredictionRecord(
        row_id="row-resolved",
        condition_id="0xresolved",
        window_label="12:00",
        window_end_at=now - timedelta(seconds=1),
        beat_price=100.0,
        mode="paper",
        signal="BUY_UP",
        predicted_direction="UP",
        decision_action="paper_trade",
        executed_order_id="SIM-RESOLVED",
        simulated_order_id="SIM-RESOLVED",
        confidence=0.81,
        raw_confidence=0.84,
        alignment=4,
        actual_winner="UP",
        prediction_correct=True,
        paper_trade_won=True,
        resolved_at=now,
        last_updated_at=now,
    )
    pending = tf.WindowPredictionRecord(
        row_id="row-pending",
        condition_id="0xpending",
        window_label="12:05",
        window_end_at=now + timedelta(minutes=1),
        beat_price=100.0,
        mode="paper",
        signal="BUY_DOWN",
        predicted_direction="DOWN",
        decision_action="paper_trade",
        executed_order_id="SIM-PENDING",
        simulated_order_id="SIM-PENDING",
        confidence=0.79,
        raw_confidence=0.82,
        alignment=4,
        last_updated_at=now,
    )

    logger.log_paper_prediction_resolved(resolved)
    logger.log_paper_prediction_state(pending)
    logger.log_paper_trade_resolved(
        make_position(
            condition_id="0xresolved",
            direction="UP",
            order_id="SIM-RESOLVED",
            now=now,
        ),
        True,
    )
    logger.log_paper_trade_resolved(
        make_position(
            condition_id="0xpending",
            direction="DOWN",
            order_id="SIM-PENDING",
            now=now,
        ),
        False,
    )

    pending_records, counts = logger.load_paper_analytics(today=now.strftime("%Y-%m-%d"))

    assert counts["prediction_correct_total"] == 1
    assert counts["prediction_incorrect_total"] == 0
    assert counts["paper_trade_wins_total"] == 1
    assert counts["paper_trade_losses_total"] == 1
    assert pending_records["row-pending"]["predicted_direction"] == "DOWN"
    assert pending_records["row-pending"]["paper_trade_won"] is False
    assert "row-resolved" not in pending_records


def test_each_buy_prediction_snapshot_is_resolved_independently(tmp_path):
    async def run_case():
        bot = make_bot(tmp_path)
        end_time = datetime.now(timezone.utc) - timedelta(seconds=1)
        win = make_window(condition_id="0xwindow", beat_price=100.0, end_time=end_time)
        snap = SimpleNamespace(signal_alignment=4)

        await bot._upsert_paper_prediction(
            win,
            SimpleNamespace(signal="BUY_UP", confidence=0.76, raw_confidence=0.8),
            snap,
            decision_action="blocked",
        )
        await bot._upsert_paper_prediction(
            win,
            SimpleNamespace(signal="BUY_DOWN", confidence=0.83, raw_confidence=0.87),
            snap,
            decision_action="blocked",
        )

        bot.state.price_history_ts = deque([(win.end_time.timestamp(), 95.0)], maxlen=10)

        await bot._resolve_paper_predictions()
        await bot._resolve_paper_predictions()

        record = bot.state.paper_prediction_records["0xwindow"]
        assert record.predicted_direction == "DOWN"
        assert record.actual_winner == "DOWN"
        assert record.prediction_correct is True
        assert bot.state.paper_stats.prediction_total == 2
        assert bot.state.paper_stats.prediction_correct_total == 1
        assert bot.state.paper_stats.prediction_incorrect_total == 1

    asyncio.run(run_case())


def test_settling_simulated_trade_updates_paper_trade_stats(tmp_path):
    async def run_case():
        bot = make_bot(tmp_path)
        now = datetime.now(timezone.utc)
        pos = make_position(
            condition_id="0xtrade",
            direction="UP",
            order_id="SIM-TRADE",
            now=now,
        )
        bot.state.paper_prediction_records[pos.condition_id] = tf.WindowPredictionRecord(
            row_id="row-trade",
            condition_id=pos.condition_id,
            window_label="12:10",
            window_end_at=pos.window_end_at,
            beat_price=pos.window_beat,
            mode="paper",
            signal="BUY_UP",
            predicted_direction=pos.direction,
            decision_action="paper_trade",
            executed_order_id=pos.order_id,
            simulated_order_id=pos.order_id,
            confidence=pos.ai_confidence,
            raw_confidence=pos.ai_raw_confidence,
            alignment=pos.signal_alignment,
            last_updated_at=now,
        )
        bot.state.prediction_records["row-trade"] = bot.state.paper_prediction_records[pos.condition_id]
        pos.prediction_row_id = "row-trade"

        await bot._settle_position(pos, "UP", pos.amount_usdc)

        assert pos.status == "won"
        assert bot.state.paper_stats.paper_trade_wins_total == 1
        assert bot.state.paper_stats.paper_trade_losses_total == 0
        assert bot.state.paper_prediction_records[pos.condition_id].paper_trade_won is True

        analytics_path = next((tmp_path / "logs").glob("prediction_analytics_*.jsonl"))
        contents = analytics_path.read_text(encoding="utf-8")
        assert "paper_trade_resolved" in contents
        history = (tmp_path / "logs" / "performance_history.json").read_text(encoding="utf-8")
        assert pos.window_end_at.strftime("%Y-%m-%d") in history

    asyncio.run(run_case())


def test_blocked_shadow_prediction_logs_gate_and_counterfactual(tmp_path):
    async def run_case():
        bot = make_bot(tmp_path)
        now = datetime.now(timezone.utc)
        record = tf.WindowPredictionRecord(
            row_id="row-shadow",
            condition_id="0xshadow",
            window_label="12:15",
            window_end_at=now - timedelta(seconds=1),
            beat_price=100.0,
            mode="live",
            signal="BUY_UP",
            predicted_direction="UP",
            decision_action="blocked",
            confidence=0.68,
            raw_confidence=0.71,
            blocked_gate="GATE_LATE_PROXIMITY_RISK",
            blocked_reason="late proximity risk",
            up_odds=0.60,
            down_odds=0.40,
            last_updated_at=now,
        )
        bot.state.prediction_records[record.row_id] = record
        bot.state.paper_prediction_records[record.condition_id] = record
        bot.state.price_history_ts = deque([(record.window_end_at.timestamp(), 101.0)], maxlen=10)

        await bot._resolve_prediction_analytics()

        resolved = bot.state.prediction_records["row-shadow"]
        assert resolved.actual_winner == "UP"
        assert resolved.prediction_correct is True
        assert resolved.counterfactual_pnl is not None

        analytics_path = next((tmp_path / "logs").glob("prediction_analytics_*.jsonl"))
        contents = analytics_path.read_text(encoding="utf-8")
        assert "prediction_resolved" in contents
        assert "GATE_LATE_PROXIMITY_RISK" in contents

    asyncio.run(run_case())


def test_render_results_hides_prediction_rows_in_paper_mode(tmp_path, monkeypatch):
    monkeypatch.setattr(tf, "LIVE_TRADING", False)
    bot = make_bot(tmp_path)
    bot.state.balance_usdc = 0.73
    bot.state.paper_stats.paper_trade_wins_total = 3
    bot.state.paper_stats.paper_trade_losses_total = 1
    bot.state.paper_stats.paper_trade_wins_today = 1
    bot.state.paper_stats.paper_trade_losses_today = 0
    bot.state.claimable_total = 5.5
    bot.state.pending_claim_count = 1
    bot.state.claimed_today_count = 2
    bot.state.failed_today_count = 0

    panel = tf.render_results(bot.state)
    console = Console(record=True, width=120)
    console.print(panel)
    text = console.export_text()

    assert "Paper Trades" in text
    assert "Trades Today" in text
    assert "Predictions" not in text
    assert "Pred Today" not in text
    assert "Claims" in text
    assert "AutoClaim" not in text
    assert "Daily Budget" in text
    assert "lost=$" in text
    assert "won=$" in text
    assert "left=$" in text
    assert "Claim log" not in text


def test_render_results_shows_real_claim_log_without_hiding_budget_rows(tmp_path):
    bot = make_bot(tmp_path)
    bot.state.balance_usdc = 0.73
    bot.state.claimable_total = 5.5
    bot.state.pending_claim_count = 1
    bot.state.claimed_today_count = 2
    bot.state.failed_today_count = 1
    bot.state.claim_log.append("12:00:00 queued $5.50 (0xabc…)")

    panel = tf.render_results(bot.state)
    console = Console(record=True, width=120)
    console.print(panel)
    text = console.export_text()

    assert "Claim log" in text
    assert "queued $5.50" in text
    assert "Daily Budget" in text
    assert "left=$" in text


def test_claim_scan_queues_redeemable_positions_in_discovery_mode(tmp_path, monkeypatch):
    async def run_case():
        bot = make_bot(tmp_path)
        bot.market = DummyMarket(
            positions=[
                {
                    "conditionId": "0xabc",
                    "asset": "asset-up",
                    "outcome": "Yes",
                    "outcomeIndex": 0,
                    "currentValue": 6.25,
                    "redeemable": True,
                    "mergeable": False,
                    "negativeRisk": False,
                    "title": "BTC above?",
                }
            ]
        )
        monkeypatch.setattr(tf, "POLY_ADDRESS", "0x123")
        monkeypatch.setattr(tf, "AUTO_CLAIM_ENABLED", False)
        monkeypatch.setattr(tf, "AUTO_CLAIM_LIVE_ONLY", True)
        monkeypatch.setattr(tf, "AUTO_CLAIM_THRESHOLD", 4.0)

        await bot._scan_and_process_claims(trigger="test")

        claim = bot.state.claim_records["0xabc"]
        assert claim.status == "queued"
        assert bot.state.pending_claim_count == 1
        assert bot.state.claimable_total == 6.25
        assert bot.market.claim_calls == []

    asyncio.run(run_case())


def test_claim_scan_executes_confirmed_claim_when_enabled(tmp_path, monkeypatch):
    async def run_case():
        bot = make_bot(tmp_path)
        bot.market = DummyMarket(
            positions=[
                {
                    "conditionId": "0xdef",
                    "asset": "asset-up",
                    "outcome": "Yes",
                    "outcomeIndex": 0,
                    "currentValue": 7.0,
                    "redeemable": True,
                    "mergeable": False,
                    "negativeRisk": False,
                    "title": "BTC above?",
                }
            ],
            claim_result=tf.ClaimAttemptResult(
                success=True,
                status="confirmed",
                tx_hash="0xtx",
                request_id="req-1",
            ),
        )
        monkeypatch.setattr(tf, "POLY_ADDRESS", "0x123")
        monkeypatch.setattr(tf, "AUTO_CLAIM_ENABLED", True)
        monkeypatch.setattr(tf, "AUTO_CLAIM_LIVE_ONLY", True)
        monkeypatch.setattr(tf, "LIVE_TRADING", True)
        monkeypatch.setattr(tf, "AUTO_CLAIM_THRESHOLD", 4.0)

        await bot._scan_and_process_claims(trigger="test")

        claim = bot.state.claim_records["0xdef"]
        assert claim.status == "confirmed"
        assert claim.tx_hash == "0xtx"
        assert bot.market.claim_calls == ["0xdef"]
        assert bot.state.claimed_today_count == 1

    asyncio.run(run_case())


def test_stable_buy_sends_single_shadow_notification(tmp_path):
    async def run_case():
        bot = make_bot(tmp_path)
        win = make_window(
            condition_id="0xnotify",
            beat_price=100.0,
            end_time=datetime.now(timezone.utc) + timedelta(seconds=30),
        )
        snap = SimpleNamespace(signal_alignment=5, cvd_divergence="BULLISH")
        signal = tf.AISignal(
            signal="BUY_UP",
            confidence=0.82,
            raw_confidence=0.84,
            reason="stable signal",
            dip_label="SUSTAINED_ABOVE",
            source="ml",
        )

        row1 = tf.WindowPredictionRecord(
            row_id="row-1",
            condition_id=win.condition_id,
            window_label=win.window_label,
            window_end_at=win.end_time,
            beat_price=win.beat_price,
            signal="BUY_UP",
            predicted_direction="UP",
            confidence=signal.confidence,
            raw_confidence=signal.raw_confidence,
            source=signal.source,
            up_odds=0.55,
            down_odds=0.45,
            last_updated_at=datetime.now(timezone.utc),
        )
        row2 = tf.WindowPredictionRecord(
            row_id="row-2",
            condition_id=win.condition_id,
            window_label=win.window_label,
            window_end_at=win.end_time,
            beat_price=win.beat_price,
            signal="BUY_UP",
            predicted_direction="UP",
            confidence=signal.confidence,
            raw_confidence=signal.raw_confidence,
            source=signal.source,
            up_odds=0.55,
            down_odds=0.45,
            last_updated_at=datetime.now(timezone.utc),
        )
        bot.state.prediction_records[row1.row_id] = row1
        bot.state.prediction_records[row2.row_id] = row2
        bot.state.paper_prediction_records[win.condition_id] = row2

        first = await bot._advance_session_signal_state(
            condition_id=win.condition_id,
            signal=signal,
            row_id=row1.row_id,
            sample_seq=1,
            phase_bucket="EARLY_EXEC",
            signal_edge=0.08,
            execution_ready=False,
        )
        second = await bot._advance_session_signal_state(
            condition_id=win.condition_id,
            signal=signal,
            row_id=row2.row_id,
            sample_seq=2,
            phase_bucket="EARLY_EXEC",
            signal_edge=0.08,
            execution_ready=False,
        )

        assert first is False
        assert second is True

        emitted = await bot._emit_locked_signal_notification(
            locked_now=True,
            signal=signal,
            win=win,
            snap=snap,
            decision=tf.TradeDecision(action="SKIP", direction="UP", confidence=0.82, reason="blocked", gate="GATE_LATE_PROXIMITY_RISK"),
            execution_block=("GATE_LATE_PROXIMITY_RISK", "late proximity"),
            btc_price=100.2,
            up_odds=0.55,
            down_odds=0.45,
        )
        emitted_again = await bot._emit_locked_signal_notification(
            locked_now=False,
            signal=tf.AISignal(signal="SKIP", confidence=0.0, reason="hold"),
            win=win,
            snap=snap,
            decision=tf.TradeDecision(action="SKIP", direction="NONE", confidence=0.0, reason="hold", gate="GATE_AI_HOLD"),
            execution_block=("GATE_LATE_PROXIMITY_RISK", "late proximity"),
            btc_price=100.2,
            up_odds=0.55,
            down_odds=0.45,
        )

        assert emitted is True
        assert emitted_again is False
        assert len(bot.notifier.shadow_calls) == 1
        assert len(bot.notifier.signal_calls) == 0
        assert bot.state.session_signal_state.telegram_sent is True
        assert bot.state.prediction_records["row-2"].notification_sent is True

    asyncio.run(run_case())


def test_place_trade_opens_simulated_position_in_paper_mode(tmp_path):
    class StubMarket:
        async def place_bet(self, direction, token_id, amount_usdc, current_odds):
            return tf.TradeResult(
                success=True,
                order_id="SIM-123",
                simulated=True,
                size=round(amount_usdc / current_odds, 4),
                price=current_odds,
                amount_usdc=amount_usdc,
            )

    async def run_case():
        bot = make_bot(tmp_path)
        bot.market = StubMarket()
        now = datetime.now(timezone.utc)
        win = make_window(condition_id="0xpaper", beat_price=100.0, end_time=now + timedelta(minutes=1))
        snap = SimpleNamespace(signal_alignment=5, cvd_divergence="BULLISH")
        signal = tf.AISignal(
            signal="BUY_UP",
            confidence=0.84,
            raw_confidence=0.86,
            reason="paper trade",
            dip_label="SUSTAINED_ABOVE",
            source="ml",
        )
        bot.state.up_odds = 0.56
        bot.state.down_odds = 0.44

        await bot._place_trade(
            win,
            signal,
            snap,
            prices=[100.0, 100.1],
            is_gold_zone=True,
            prediction_row_id="row-paper",
        )

        assert len(bot.state.positions) == 1
        assert bot.state.positions[0].simulated is True
        assert bot.state.positions[0].prediction_row_id == "row-paper"
        assert len(bot.notifier.bet_calls) == 1

    asyncio.run(run_case())


def test_place_trade_lifts_live_bet_to_market_minimum(tmp_path, monkeypatch):
    class StubMarket:
        def __init__(self):
            self.bet_calls = []

        async def get_min_order_size(self, token_id):
            return 5.0

        async def place_bet(self, direction, token_id, amount_usdc, current_odds):
            self.bet_calls.append((direction, token_id, amount_usdc, current_odds))
            return tf.TradeResult(
                success=True,
                order_id="LIVE-123",
                simulated=False,
                size=5.0,
                price=current_odds,
                amount_usdc=amount_usdc,
            )

    async def run_case():
        bot = make_bot(tmp_path)
        bot.market = StubMarket()
        bot.state.balance_usdc = 14.51
        now = datetime.now(timezone.utc)
        win = make_window(condition_id="0xlive-min", beat_price=100.0, end_time=now + timedelta(minutes=1))
        snap = SimpleNamespace(signal_alignment=5, cvd_divergence="BULLISH")
        signal = tf.AISignal(
            signal="BUY_UP",
            confidence=0.93,
            raw_confidence=0.93,
            reason="live trade",
            dip_label="SUSTAINED_ABOVE",
            source="ml",
        )
        bot.state.up_odds = 0.50
        bot.state.down_odds = 0.50

        monkeypatch.setattr(tf, "LIVE_TRADING", True)

        await bot._place_trade(
            win,
            signal,
            snap,
            prices=[100.0, 100.1],
            is_gold_zone=True,
            prediction_row_id="row-live-min",
        )

        assert bot.market.bet_calls == [("UP", "up-token", 2.5, 0.5)]
        assert len(bot.state.positions) == 1
        assert bot.state.positions[0].simulated is False
        assert bot.state.positions[0].amount_usdc == 2.5

    asyncio.run(run_case())


def test_retryable_live_trade_failure_allows_later_retry_in_same_window(tmp_path, monkeypatch):
    class StubMarket:
        def __init__(self):
            self.bet_calls = 0

        async def get_min_order_size(self, token_id):
            return 1.0

        async def place_bet(self, direction, token_id, amount_usdc, current_odds):
            self.bet_calls += 1
            if self.bet_calls == 1:
                return tf.TradeResult(
                    success=False,
                    error="timeout talking to matching engine",
                    failure_code="TRANSIENT_NETWORK",
                    retryable=True,
                    attempt_consumed=False,
                )
            return tf.TradeResult(
                success=True,
                order_id="LIVE-RETRY",
                simulated=False,
                size=4.0,
                price=current_odds,
                amount_usdc=amount_usdc,
            )

    async def run_case():
        bot = make_bot(tmp_path)
        bot.market = StubMarket()
        bot.state.balance_usdc = 20.0
        now = datetime.now(timezone.utc)
        win = make_window(condition_id="0xretry-live", beat_price=100.0, end_time=now + timedelta(minutes=1))
        snap = SimpleNamespace(signal_alignment=5, cvd_divergence="BULLISH")
        signal = tf.AISignal(
            signal="BUY_UP",
            confidence=0.93,
            raw_confidence=0.93,
            reason="retry me",
            dip_label="SUSTAINED_ABOVE",
            source="ml",
        )
        record = tf.WindowPredictionRecord(
            row_id="row-live-retry",
            condition_id=win.condition_id,
            window_label=win.window_label,
            window_end_at=win.end_time,
            beat_price=win.beat_price,
            mode="live",
            signal="BUY_UP",
            predicted_direction="UP",
            confidence=signal.confidence,
            raw_confidence=signal.raw_confidence,
            source="ml",
            last_updated_at=now,
        )
        bot.state.prediction_records[record.row_id] = record
        bot.state.paper_prediction_records[record.condition_id] = record
        bot.state.up_odds = 0.55
        bot.state.down_odds = 0.45

        monkeypatch.setattr(tf, "LIVE_TRADING", True)

        await bot._place_trade(
            win,
            signal,
            snap,
            prices=[100.0, 100.1],
            is_gold_zone=True,
            prediction_row_id=record.row_id,
        )

        execution_state = bot.state.window_execution_states[win.condition_id]
        assert len(bot.state.positions) == 0
        assert execution_state.attempt_count == 1
        assert execution_state.retryable_failures == 1
        assert execution_state.terminal is False

        decision = tf.TradeDecision(action="BUY", direction="UP", confidence=signal.confidence, reason="ok", gate=tf.GATE_OK)
        strategy_block_now = bot._execution_block(
            win=win,
            signal=signal,
            decision=decision,
            elapsed_s=250,
            seconds_remaining=45,
            now=execution_state.last_attempt_at,
        )
        blocked_now = bot._operational_execution_block(
            win=win,
            seconds_remaining=45,
            now=execution_state.last_attempt_at,
        )
        strategy_block_later = bot._execution_block(
            win=win,
            signal=signal,
            decision=decision,
            elapsed_s=253,
            seconds_remaining=40,
            now=execution_state.last_attempt_at + tf.LIVE_RETRY_COOLDOWN_S + 0.2,
        )
        blocked_later = bot._operational_execution_block(
            win=win,
            seconds_remaining=40,
            now=execution_state.last_attempt_at + tf.LIVE_RETRY_COOLDOWN_S + 0.2,
        )

        assert strategy_block_now is None
        assert blocked_now is not None
        assert blocked_now[0] == tf.GATE_RETRY_COOLDOWN
        assert strategy_block_later is None
        assert blocked_later is None

        await bot._place_trade(
            win,
            signal,
            snap,
            prices=[100.0, 100.2],
            is_gold_zone=True,
            prediction_row_id=record.row_id,
        )

        execution_state = bot.state.window_execution_states[win.condition_id]
        record_after = bot.state.paper_prediction_records[win.condition_id]
        assert len(bot.state.positions) == 1
        assert execution_state.attempt_count == 2
        assert execution_state.successful is True
        assert execution_state.terminal is True
        assert record_after.executed_order_id == "LIVE-RETRY"
        assert record_after.placement_failure_code == ""

        analytics_path = next((tmp_path / "logs").glob("prediction_analytics_*.jsonl"))
        contents = analytics_path.read_text(encoding="utf-8")
        assert "prediction_trade_failed" in contents

    asyncio.run(run_case())


def test_nonretryable_live_trade_failure_consumes_window(tmp_path, monkeypatch):
    class StubMarket:
        async def get_min_order_size(self, token_id):
            return 1.0

        async def place_bet(self, direction, token_id, amount_usdc, current_odds):
            return tf.TradeResult(
                success=False,
                error="insufficient balance on exchange",
                failure_code="INSUFFICIENT_BALANCE",
                retryable=False,
                attempt_consumed=True,
            )

    async def run_case():
        bot = make_bot(tmp_path)
        bot.market = StubMarket()
        bot.state.balance_usdc = 20.0
        now = datetime.now(timezone.utc)
        win = make_window(condition_id="0xterminal-live", beat_price=100.0, end_time=now + timedelta(minutes=1))
        snap = SimpleNamespace(signal_alignment=5, cvd_divergence="BULLISH")
        signal = tf.AISignal(
            signal="BUY_UP",
            confidence=0.91,
            raw_confidence=0.91,
            reason="terminal fail",
            dip_label="SUSTAINED_ABOVE",
            source="ml",
        )
        record = tf.WindowPredictionRecord(
            row_id="row-live-terminal",
            condition_id=win.condition_id,
            window_label=win.window_label,
            window_end_at=win.end_time,
            beat_price=win.beat_price,
            mode="live",
            signal="BUY_UP",
            predicted_direction="UP",
            confidence=signal.confidence,
            raw_confidence=signal.raw_confidence,
            source="ml",
            last_updated_at=now,
        )
        bot.state.prediction_records[record.row_id] = record
        bot.state.paper_prediction_records[record.condition_id] = record
        bot.state.up_odds = 0.55
        bot.state.down_odds = 0.45

        monkeypatch.setattr(tf, "LIVE_TRADING", True)

        await bot._place_trade(
            win,
            signal,
            snap,
            prices=[100.0, 100.1],
            is_gold_zone=True,
            prediction_row_id=record.row_id,
        )

        execution_state = bot.state.window_execution_states[win.condition_id]
        decision = tf.TradeDecision(action="BUY", direction="UP", confidence=signal.confidence, reason="ok", gate=tf.GATE_OK)
        strategy_block = bot._execution_block(
            win=win,
            signal=signal,
            decision=decision,
            elapsed_s=252,
            seconds_remaining=40,
            now=datetime.now(timezone.utc).timestamp(),
        )
        blocked = bot._operational_execution_block(
            win=win,
            seconds_remaining=40,
            now=datetime.now(timezone.utc).timestamp(),
        )

        assert len(bot.state.positions) == 0
        assert execution_state.terminal is True
        assert strategy_block is None
        assert blocked is not None
        assert blocked[0] == tf.GATE_ALREADY_ATTEMPTED
        assert "INSUFFICIENT_BALANCE" in blocked[1]

    asyncio.run(run_case())


def test_live_low_balance_records_trade_failure_without_strategy_block(tmp_path, monkeypatch):
    class StubMarket:
        async def get_min_order_size(self, token_id):
            return 1.0

        async def place_bet(self, direction, token_id, amount_usdc, current_odds):
            raise AssertionError("place_bet should not run when balance is below target bet")

    async def run_case():
        bot = make_bot(tmp_path)
        bot.market = StubMarket()
        bot.state.balance_usdc = 0.75
        now = datetime.now(timezone.utc)
        win = make_window(condition_id="0xlow-balance", beat_price=100.0, end_time=now + timedelta(minutes=1))
        snap = SimpleNamespace(signal_alignment=5, cvd_divergence="BULLISH")
        signal = tf.AISignal(
            signal="BUY_UP",
            confidence=0.91,
            raw_confidence=0.91,
            reason="low balance",
            dip_label="SUSTAINED_ABOVE",
            source="ml",
        )
        record = tf.WindowPredictionRecord(
            row_id="row-low-balance",
            condition_id=win.condition_id,
            window_label=win.window_label,
            window_end_at=win.end_time,
            beat_price=win.beat_price,
            mode="live",
            signal="BUY_UP",
            predicted_direction="UP",
            decision_action="observe",
            confidence=signal.confidence,
            raw_confidence=signal.raw_confidence,
            source="ml",
            execution_allowed=True,
            last_updated_at=now,
        )
        bot.state.prediction_records[record.row_id] = record
        bot.state.paper_prediction_records[record.condition_id] = record
        bot.state.up_odds = 0.55
        bot.state.down_odds = 0.45

        monkeypatch.setattr(tf, "LIVE_TRADING", True)

        decision = tf.TradeDecision(action="BUY", direction="UP", confidence=signal.confidence, reason="ok", gate=tf.GATE_OK)
        strategy_block = bot._execution_block(
            win=win,
            signal=signal,
            decision=decision,
            elapsed_s=250,
            seconds_remaining=45,
            now=datetime.now(timezone.utc).timestamp(),
        )

        await bot._place_trade(
            win,
            signal,
            snap,
            prices=[100.0, 100.1],
            is_gold_zone=True,
            prediction_row_id=record.row_id,
        )

        updated = bot.state.paper_prediction_records[win.condition_id]
        analytics_path = next((tmp_path / "logs").glob("prediction_analytics_*.jsonl"))
        contents = analytics_path.read_text(encoding="utf-8")

        assert strategy_block is None
        assert len(bot.state.positions) == 0
        assert updated.execution_allowed is True
        assert updated.blocked_gate == ""
        assert updated.placement_failure_code == "INSUFFICIENT_BALANCE_PRECHECK"
        assert "prediction_trade_failed" in contents
        assert "prediction_blocked" not in contents

    asyncio.run(run_case())


def test_check_positions_does_not_cancel_filled_live_order_when_exchange_status_is_canceled(tmp_path):
    class StubMarket:
        async def get_order(self, order_id):
            return {"status": "CANCELED"}

        async def get_recent_trades(self):
            return [
                tf.ClosedTrade(
                    condition_id="0xfilled-canceled",
                    direction="UP",
                    size=5.0,
                    price=0.5,
                    status="MATCHED",
                    match_time=datetime.now(timezone.utc).isoformat(),
                )
            ]

        def session_snapshot(self):
            return {"refresh_in_progress": False, "consecutive_auth_failures": 0}

    async def run_case():
        bot = make_bot(tmp_path)
        bot.market = StubMarket()
        now = datetime.now(timezone.utc)
        pos = tf.Position(
            condition_id="0xfilled-canceled",
            direction="UP",
            token_id="up-token",
            size=5.0,
            entry_price=0.5,
            placed_at=now - timedelta(minutes=4),
            order_id="LIVE-CANCELED",
            simulated=False,
            amount_usdc=2.5,
            window_beat=100.0,
            window_end_at=now - timedelta(seconds=5),
            elapsed_at_bet=240,
            gap_pct_at_bet=0.15,
            ai_confidence=0.82,
            ai_raw_confidence=0.86,
            signal_alignment=5,
            prediction_row_id="row-live-canceled",
        )
        bot.state.positions.append(pos)
        bot.state.price_history_ts = deque([(pos.window_end_at.timestamp(), 100.3)], maxlen=10)

        await bot._check_positions()

        assert pos.status == "won"
        assert pos.pnl == pytest.approx(2.5)

    asyncio.run(run_case())


def test_tie_settlement_is_void_not_down_win(tmp_path):
    async def run_case():
        bot = make_bot(tmp_path)
        now = datetime.now(timezone.utc)
        pos = make_position(
            condition_id="0xtie",
            direction="DOWN",
            order_id="SIM-TIE",
            now=now,
        )
        bot.state.positions.append(pos)
        bot.state.price_history_ts = deque([(pos.window_end_at.timestamp(), pos.window_beat)], maxlen=10)

        await bot._check_positions()

        assert pos.status == "void"
        assert pos.pnl == 0.0
        assert bot.state.win_count == 0
        assert bot.state.loss_count == 0
        assert bot.state.paper_stats.paper_trade_total == 0

    asyncio.run(run_case())


def test_settlement_requires_close_aligned_price_sample(tmp_path):
    bot = make_bot(tmp_path)
    bot.state.btc_price = 150.0
    target = datetime.now(timezone.utc) - timedelta(minutes=1)

    settlement = bot._get_settlement_btc_for_window(
        condition_id="0xlate",
        window_end_at=target,
    )

    assert settlement is None


def test_observe_phase_buy_does_not_lock(tmp_path):
    async def run_case():
        bot = make_bot(tmp_path)
        signal = tf.AISignal(signal="BUY_UP", confidence=0.82, raw_confidence=0.84, reason="observe", source="ml")
        row = tf.WindowPredictionRecord(row_id="row-observe", condition_id="0xobserve")
        bot.state.prediction_records[row.row_id] = row

        locked = await bot._advance_session_signal_state(
            condition_id="0xobserve",
            signal=signal,
            row_id=row.row_id,
            sample_seq=1,
            phase_bucket="OBSERVE",
            signal_edge=0.08,
            execution_ready=False,
        )

        assert locked is False
        assert bot.state.session_signal_state.locked_signal == ""

    asyncio.run(run_case())


def test_reserve_buy_locks_and_carries_into_execute(tmp_path):
    async def run_case():
        bot = make_bot(tmp_path)
        reserve_signal = tf.AISignal(signal="BUY_UP", confidence=0.82, raw_confidence=0.84, reason="reserve", source="ml")
        row1 = tf.WindowPredictionRecord(
            row_id="row-reserve-1",
            condition_id="0xreserve",
            signal="BUY_UP",
            predicted_direction="UP",
            confidence=reserve_signal.confidence,
            raw_confidence=reserve_signal.raw_confidence,
            source="ml",
            up_odds=0.55,
            down_odds=0.45,
            last_updated_at=datetime.now(timezone.utc),
        )
        row2 = tf.WindowPredictionRecord(
            row_id="row-reserve-2",
            condition_id="0xreserve",
            signal="BUY_UP",
            predicted_direction="UP",
            confidence=reserve_signal.confidence,
            raw_confidence=reserve_signal.raw_confidence,
            source="ml",
            up_odds=0.55,
            down_odds=0.45,
            last_updated_at=datetime.now(timezone.utc),
        )
        bot.state.prediction_records[row1.row_id] = row1
        bot.state.prediction_records[row2.row_id] = row2

        first = await bot._advance_session_signal_state(
            condition_id="0xreserve",
            signal=reserve_signal,
            row_id=row1.row_id,
            sample_seq=1,
            phase_bucket="RESERVE",
            signal_edge=0.08,
            execution_ready=False,
        )
        locked = await bot._advance_session_signal_state(
            condition_id="0xreserve",
            signal=reserve_signal,
            row_id=row2.row_id,
            sample_seq=2,
            phase_bucket="RESERVE",
            signal_edge=0.08,
            execution_ready=False,
        )
        carried_signal, carried = bot._maybe_apply_reserved_signal_carry(
            condition_id="0xreserve",
            signal=tf.AISignal(
                signal="SKIP",
                confidence=0.79,
                raw_confidence=0.81,
                reason="confidence floor",
                source="ml",
                prob_up=0.79,
                prob_down=0.21,
                runtime_skip_reason_code="RUNTIME_CONFIDENCE_FLOOR",
            ),
            phase_bucket="EARLY_EXEC",
        )

        assert first is False
        assert locked is True
        assert bot.state.session_signal_state.reservation_locked is True
        assert carried is True
        assert carried_signal.signal == "BUY_UP"
        assert carried_signal.source.endswith("_reserve")

    asyncio.run(run_case())


def test_execution_window_opens_at_210_seconds(tmp_path, monkeypatch):
    monkeypatch.setattr(tf, "LIVE_TRADING", False)
    bot = make_bot(tmp_path)
    win = make_window(condition_id="0xwindow", beat_price=100.0, end_time=datetime.now(timezone.utc) + timedelta(minutes=1))
    signal = tf.AISignal(signal="BUY_UP", confidence=0.82, raw_confidence=0.84, reason="buy", source="ml")
    decision = tf.TradeDecision(action="BUY", direction="UP", confidence=0.82, reason="ok", gate=tf.GATE_OK)

    blocked_209 = bot._execution_block(
        win=win,
        signal=signal,
        decision=decision,
        elapsed_s=209,
        seconds_remaining=91,
        now=datetime.now(timezone.utc).timestamp(),
    )
    blocked_210 = bot._execution_block(
        win=win,
        signal=signal,
        decision=decision,
        elapsed_s=210,
        seconds_remaining=90,
        now=datetime.now(timezone.utc).timestamp(),
    )

    assert blocked_209 is not None
    assert blocked_209[0] == "GATE_EXECUTION_WINDOW"
    assert blocked_210 is None


def test_soft_bandar_push_only_hard_blocks_under_30_seconds():
    previous = tf.BET_FREQUENCY_EXPANSION_PHASE
    tf.BET_FREQUENCY_EXPANSION_PHASE = "B"
    try:
        decision = tf.DecisionMaker()
        snap = SimpleNamespace(direction_bias="UP", odds_vel_value=0.009, odds_vel_accel=0.0)
        ctx_soft = tf.DecisionContext(
            win=SimpleNamespace(beat_price=100.0),
            elapsed_s=220,
            seconds_remaining=40,
            btc_price=100.2,
            up_odds=0.58,
            down_odds=0.42,
            snap=snap,
        )
        ctx_hard = tf.DecisionContext(
            win=SimpleNamespace(beat_price=100.0),
            elapsed_s=275,
            seconds_remaining=25,
            btc_price=100.2,
            up_odds=0.58,
            down_odds=0.42,
            snap=snap,
        )

        assert decision._check_bandar_push(ctx_soft) is None
        assert "SOFT_BANDAR_PUSH" in decision.soft_penalties(ctx_soft)
        hard = decision._check_bandar_push(ctx_hard)
        assert hard is not None
        assert hard.gate == "GATE_BANDAR_PUSH"
    finally:
        tf.BET_FREQUENCY_EXPANSION_PHASE = previous


def test_soft_late_proximity_risk_only_hard_blocks_inside_final_25_seconds():
    previous = tf.BET_FREQUENCY_EXPANSION_PHASE
    tf.BET_FREQUENCY_EXPANSION_PHASE = "B"
    try:
        decision = tf.DecisionMaker()
        snap = SimpleNamespace(direction_bias="UP")
        ctx_soft = tf.DecisionContext(
            win=SimpleNamespace(beat_price=100.0),
            elapsed_s=220,
            seconds_remaining=40,
            btc_price=100.05,
            up_odds=0.58,
            down_odds=0.42,
            snap=snap,
            signal_alignment=4,
        )
        ctx_mid = tf.DecisionContext(
            win=SimpleNamespace(beat_price=100.0),
            elapsed_s=220,
            seconds_remaining=40,
            btc_price=100.02,
            up_odds=0.58,
            down_odds=0.42,
            snap=snap,
            signal_alignment=3,
        )
        ctx_hard = tf.DecisionContext(
            win=SimpleNamespace(beat_price=100.0),
            elapsed_s=280,
            seconds_remaining=20,
            btc_price=100.02,
            up_odds=0.58,
            down_odds=0.42,
            snap=snap,
            signal_alignment=5,
        )

        assert decision._check_late_reversal_risk(ctx_soft) is None
        assert "SOFT_LATE_PROXIMITY_RISK" in decision.soft_penalties(ctx_soft)
        assert decision._check_late_reversal_risk(ctx_mid) is None
        hard = decision._check_late_reversal_risk(ctx_hard)
        assert hard is not None
        assert hard.gate == "GATE_LATE_PROXIMITY_RISK"
    finally:
        tf.BET_FREQUENCY_EXPANSION_PHASE = previous


def test_warm_paper_analytics_restores_pending_live_trade_failure_state(tmp_path):
    bot = make_bot(tmp_path)
    now = datetime.now(timezone.utc)
    record = tf.WindowPredictionRecord(
        row_id="row-live-failure",
        condition_id="0xrestore-live",
        window_label="12:40",
        window_end_at=now + timedelta(minutes=1),
        beat_price=100.0,
        mode="live",
        signal="BUY_UP",
        predicted_direction="UP",
        decision_action="trade_failed_retryable",
        confidence=0.86,
        raw_confidence=0.88,
        source="ml",
        placement_failure_code="TRANSIENT_NETWORK",
        placement_failure_reason="timeout talking to matching engine",
        placement_retryable=True,
        placement_attempt_consumed=False,
        placement_attempt_count=1,
        last_attempted_at=now,
        last_updated_at=now,
    )

    bot.state.logger.log_prediction_trade_failed(record)

    restored, warmed = bot._warm_paper_analytics()
    execution_state = bot.state.window_execution_states[record.condition_id]
    restored_record = bot.state.prediction_records[record.row_id]

    assert restored == 1
    assert warmed == 0
    assert restored_record.placement_failure_code == "TRANSIENT_NETWORK"
    assert restored_record.placement_retryable is True
    assert execution_state.retryable_failures == 1
    assert execution_state.terminal is False


def test_prediction_state_logs_structured_skip_reason_codes(tmp_path):
    bot = make_bot(tmp_path)
    now = datetime.now(timezone.utc)
    record = tf.WindowPredictionRecord(
        row_id="row-skip-code",
        condition_id="0xskip",
        window_label="12:30",
        window_end_at=now,
        beat_price=100.0,
        signal="SKIP",
        predicted_direction="NONE",
        confidence=0.77,
        raw_confidence=0.79,
        runtime_skip_reason_code="RUNTIME_CANDIDATE_FLOOR",
        decision_skip_reason_code="GATE_LOW_CONF",
        execution_bucket="EARLY_EXEC",
        candidate_confidence_floor=0.74,
        execution_required_confidence=0.78,
        threshold_profile_version="test_v1",
        threshold_source="auto_tuned",
        last_updated_at=now,
    )

    bot.state.logger.log_prediction_state(record)

    analytics_path = next((tmp_path / "logs").glob("prediction_analytics_*.jsonl"))
    contents = analytics_path.read_text(encoding="utf-8")

    assert "RUNTIME_CANDIDATE_FLOOR" in contents
    assert "GATE_LOW_CONF" in contents
    assert "EARLY_EXEC" in contents
    assert "auto_tuned" in contents
