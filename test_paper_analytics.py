import asyncio
import json
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
        self.shadow_order_open_calls = []
        self.shadow_order_result_calls = []
        self.bet_calls = []
        self.result_calls = []

    def notify_signal(self, signal, win, snap, **kwargs) -> None:
        self.signal_calls.append((signal.signal, win.condition_id, kwargs))
        return None

    def notify_shadow_signal(self, signal, win, snap, **kwargs) -> None:
        self.shadow_calls.append((signal.signal, win.condition_id, kwargs))
        return None

    def notify_shadow_order_opened(self, order) -> None:
        self.shadow_order_open_calls.append(order)
        return None

    def notify_shadow_order_result(self, order) -> None:
        self.shadow_order_result_calls.append(order)
        return None

    def notify_bet(self, direction, bet_size, entry_odds, win, order_id, simulated, snap, **kwargs) -> None:
        self.bet_calls.append((direction, bet_size, entry_odds, simulated, kwargs))
        return None

    def notify_result(self, pos, state) -> None:
        self.result_calls.append((pos.direction, pos.status, pos.pnl, pos.simulated))
        return None


class DummyMarket:
    def __init__(self, positions=None, claim_result=None) -> None:
        self._positions = positions if callable(positions) else list(positions or [])
        self._claim_result = claim_result or tf.ClaimAttemptResult(success=False, status="failed")
        self.claim_calls = []
        self.position_calls = []
        self._last_positions_status = "ok"
        self._last_positions_error = ""

    async def get_current_positions(self, **kwargs):
        self.position_calls.append(kwargs)
        self._last_positions_status = "ok"
        self._last_positions_error = ""
        if callable(self._positions):
            return list(self._positions(kwargs))
        return list(self._positions)

    async def claim_position(self, claim):
        self.claim_calls.append(claim.claim_id)
        return self._claim_result

    def session_snapshot(self):
        return {
            "refresh_in_progress": False,
            "consecutive_auth_failures": 0,
            "last_positions_status": self._last_positions_status,
            "last_positions_error": self._last_positions_error,
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


def make_execution_quote(
    *,
    token_id: str = "up-token",
    amount_usdc: float = 2.0,
    price: float = 0.56,
    mid_price: float | None = None,
    min_order_size: float = 1.0,
    spread: float = 0.01,
    liquidity_source: str = "orderbook",
) -> tf.ExecutionQuote:
    est = tf.estimate_buy_net_shares(amount_usdc, price, tf.POLYMARKET_CRYPTO_TAKER_FEE_RATE)
    return tf.ExecutionQuote(
        token_id=token_id,
        amount_usdc=amount_usdc,
        mid_price=mid_price if mid_price is not None else max(0.01, min(0.99, price - spread / 2)),
        best_bid=max(0.01, price - spread),
        best_ask=price,
        avg_price=price,
        spread=spread,
        gross_shares=est["gross_shares"],
        net_shares=est["net_shares"],
        fee_usdc=est["fee_usdc"],
        fee_shares=est["fee_shares"],
        fee_rate=tf.POLYMARKET_CRYPTO_TAKER_FEE_RATE,
        fee_rate_source="fee-rate",
        min_order_size=min_order_size,
        enough_liquidity=True,
        liquidity_source=liquidity_source,
    )


def store_locked_buy_record(bot, win, signal, *, row_id: str = "row-shadow") -> tf.WindowPredictionRecord:
    now = datetime.now(timezone.utc)
    direction = "UP" if signal.signal == "BUY_UP" else "DOWN"
    record = tf.WindowPredictionRecord(
        row_id=row_id,
        condition_id=win.condition_id,
        window_label=win.window_label,
        window_end_at=win.end_time,
        beat_price=win.beat_price,
        mode="paper",
        signal=signal.signal,
        predicted_direction=direction,
        confidence=signal.confidence,
        raw_confidence=signal.raw_confidence or signal.confidence,
        source=signal.source,
        last_updated_at=now,
    )
    bot.state.prediction_records[record.row_id] = record
    bot.state.paper_prediction_records[record.condition_id] = record
    bot.state.session_signal_state.reset(win.condition_id)
    bot.state.session_signal_state.locked_signal = signal.signal
    bot.state.session_signal_state.locked_row_id = record.row_id
    return record


_WIB = timezone(timedelta(hours=7), "WIB")


def _wib_ts(year: int, month: int, day: int, hour: int, minute: int = 0) -> float:
    return datetime(year, month, day, hour, minute, tzinfo=_WIB).timestamp()


def test_telegram_notifier_formats_shadow_signal_hold():
    notifier = tf.TelegramNotifier.__new__(tf.TelegramNotifier)
    notifier._enabled = True
    notifier._mode = "PAPER"
    sent = []
    notifier._fire = sent.append
    now = datetime.now(timezone.utc)
    win = make_window(condition_id="0xshadow-telegram", beat_price=100.0, end_time=now + timedelta(minutes=1))
    snap = SimpleNamespace(signal_alignment=5, cvd_divergence="BULLISH")
    signal = tf.AISignal(
        signal="BUY_UP",
        confidence=0.84,
        raw_confidence=0.86,
        reason="held signal",
        dip_label="SUSTAINED_ABOVE",
        source="ml",
    )

    notifier.notify_shadow_signal(
        signal,
        win,
        snap,
        btc_price=100.4,
        up_odds=0.58,
        down_odds=0.42,
        execution_block=(tf.GATE_NET_EDGE, "net edge below threshold"),
    )

    assert len(sent) == 1
    assert "Signal Held" in sent[0]
    assert tf.GATE_NET_EDGE in sent[0]
    assert "net edge below threshold" in sent[0]


def test_execution_block_notification_dedupes_per_window(tmp_path):
    bot = make_bot(tmp_path)
    now = datetime.now(timezone.utc)
    win = make_window(condition_id="0xblock-dedupe", beat_price=100.0, end_time=now + timedelta(minutes=1))
    bot.state.session_signal_state.reset(win.condition_id)
    snap = SimpleNamespace(signal_alignment=4, cvd_divergence="NONE")
    signal = tf.AISignal(
        signal="BUY_DOWN",
        confidence=0.8,
        raw_confidence=0.82,
        reason="held",
        dip_label="SUSTAINED_BELOW",
        source="ml",
    )

    first = bot._notify_execution_block_once(
        win=win,
        signal=signal,
        snap=snap,
        gate=tf.GATE_BET_SESSION,
        reason="outside session",
        btc_price=99.8,
        up_odds=0.47,
        down_odds=0.53,
    )
    second = bot._notify_execution_block_once(
        win=win,
        signal=signal,
        snap=snap,
        gate=tf.GATE_NET_EDGE,
        reason="net edge low",
        btc_price=99.7,
        up_odds=0.46,
        down_odds=0.54,
    )

    assert first is True
    assert second is False
    assert len(bot.notifier.shadow_calls) == 1
    assert bot.notifier.shadow_calls[0][2]["blocked_gate"] == tf.GATE_BET_SESSION


@pytest.mark.parametrize(
    "gate",
    [tf.GATE_EXECUTION_WINDOW, tf.GATE_NET_EDGE, tf.GATE_MIN_ORDER_RISK, tf.GATE_BET_SESSION],
)
def test_shadow_order_opens_for_locked_blocked_buy_without_affecting_paper_accounting(tmp_path, monkeypatch, gate):
    async def run_case():
        monkeypatch.setattr(tf, "LIVE_TRADING", False)
        monkeypatch.setattr(tf, "SHADOW_ORDERS_ENABLED", True)
        bot = make_bot(tmp_path)
        now = datetime.now(timezone.utc)
        win = make_window(condition_id=f"0xshadow-{gate.lower()}", beat_price=100.0, end_time=now + timedelta(minutes=1))
        snap = SimpleNamespace(signal_alignment=5, cvd_divergence="BULLISH")
        signal = tf.AISignal(
            signal="BUY_UP",
            confidence=0.84,
            raw_confidence=0.86,
            reason="locked shadow",
            dip_label="SUSTAINED_ABOVE",
            source="ml",
        )
        record = store_locked_buy_record(bot, win, signal, row_id=f"row-{gate.lower()}")
        bot.state.up_odds = 0.56
        bot.state.down_odds = 0.44
        quote = make_execution_quote(token_id=win.up_token_id, amount_usdc=tf.BET_SIZE_USDC, price=0.56)

        order = await bot._open_shadow_order(
            win=win,
            signal=signal,
            snap=snap,
            gate=gate,
            reason=f"{gate} blocked",
            prediction_row_id=record.row_id,
            quote=quote,
        )
        duplicate = await bot._open_shadow_order(
            win=win,
            signal=signal,
            snap=snap,
            gate=gate,
            reason=f"{gate} blocked again",
            prediction_row_id=record.row_id,
            quote=quote,
        )

        assert order is not None
        assert duplicate is order
        assert order.shadow_order_id.startswith("SHADOW-")
        assert order.blocked_gate == gate
        assert order.entry_price == pytest.approx(0.56)
        assert order.size == pytest.approx(quote.net_shares)
        assert len(bot.state.positions) == 0
        assert bot.state.bets_this_hour == 0
        assert bot.state.daily_budget_spent_usdc == 0.0
        assert bot.state.paper_stats.paper_trade_total == 0
        assert bot.state.paper_stats.shadow_order_total == 0
        assert len(bot.notifier.shadow_order_open_calls) == 1
        updated = bot.state.paper_prediction_records[win.condition_id]
        assert updated.shadow_order_id == order.shadow_order_id
        assert updated.shadow_order_status == "open"
        assert updated.blocked_gate == gate

        analytics_path = next((tmp_path / "logs").glob("prediction_analytics_*.jsonl"))
        contents = analytics_path.read_text(encoding="utf-8")
        assert "shadow_order_opened" in contents
        assert order.shadow_order_id in contents

    asyncio.run(run_case())


def test_shadow_order_resolves_with_clean_pnl_and_inclusive_up_tie(tmp_path, monkeypatch):
    async def run_case():
        monkeypatch.setattr(tf, "LIVE_TRADING", False)
        monkeypatch.setattr(tf, "SHADOW_ORDERS_ENABLED", True)
        bot = make_bot(tmp_path)
        now = datetime.now(timezone.utc)
        win = make_window(condition_id="0xshadow-resolve", beat_price=100.0, end_time=now - timedelta(seconds=5))
        snap = SimpleNamespace(signal_alignment=5, cvd_divergence="BULLISH")
        signal = tf.AISignal(
            signal="BUY_UP",
            confidence=0.84,
            raw_confidence=0.86,
            reason="resolve shadow",
            dip_label="SUSTAINED_ABOVE",
            source="ml",
        )
        record = store_locked_buy_record(bot, win, signal, row_id="row-shadow-resolve")
        bot.state.up_odds = 0.50
        bot.state.down_odds = 0.50
        quote = make_execution_quote(token_id=win.up_token_id, amount_usdc=tf.BET_SIZE_USDC, price=0.50)
        order = await bot._open_shadow_order(
            win=win,
            signal=signal,
            snap=snap,
            gate=tf.GATE_EXECUTION_WINDOW,
            reason="before execution window",
            prediction_row_id=record.row_id,
            quote=quote,
        )
        assert order is not None
        bot.state.settlement_registry_cache[win.condition_id] = {
            "settlement_price": win.beat_price,
            "settlement_source": "chainlink_market_resolved",
            "settlement_source_priority": tf._label_source_priority("chainlink_market_resolved"),
        }

        await bot._check_shadow_orders()

        resolved = bot.state.shadow_orders[win.condition_id]
        expected_pnl = quote.net_shares - quote.amount_usdc
        assert resolved.status == "won"
        assert resolved.won is True
        assert resolved.actual_winner == "UP"
        assert resolved.pnl == pytest.approx(expected_pnl)
        assert resolved.settlement_source == "chainlink_market_resolved"
        assert resolved.settlement_low_confidence is False
        assert len(bot.state.positions) == 0
        assert bot.state.bets_this_hour == 0
        assert bot.state.daily_budget_spent_usdc == 0.0
        assert bot.state.paper_stats.paper_trade_total == 0
        assert bot.state.paper_stats.shadow_order_wins_total == 1
        assert len(bot.notifier.shadow_order_result_calls) == 1
        updated = bot.state.paper_prediction_records[win.condition_id]
        assert updated.shadow_order_id == order.shadow_order_id
        assert updated.shadow_order_won is True
        assert updated.shadow_order_pnl_usdc == pytest.approx(expected_pnl)

        analytics_path = next((tmp_path / "logs").glob("prediction_analytics_*.jsonl"))
        contents = analytics_path.read_text(encoding="utf-8")
        assert "shadow_order_resolved" in contents
        assert "chainlink_market_resolved" in contents

    asyncio.run(run_case())


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


def test_daily_budget_cashflow_win_uses_gross_return_but_target_uses_profit(tmp_path, monkeypatch):
    async def run_case():
        monkeypatch.setattr(tf, "DAILY_BUDGET_USDC", 7.0)
        monkeypatch.setattr(tf, "DAILY_PROFIT_TARGET_USDC", 1.0)
        bot = make_bot(tmp_path)
        now = datetime.now(timezone.utc)
        pos = make_position(
            condition_id="0xbudget-win",
            direction="UP",
            order_id="SIM-BUDGET-WIN",
            now=now,
        )
        pos.entry_price = 0.8
        pos.size = 2.5
        pos.amount_usdc = 2.0

        bot._record_daily_budget_open(pos)
        await bot._settle_position(pos, "UP", pos.amount_usdc)

        assert pos.status == "won"
        assert pos.pnl == pytest.approx(0.5)
        assert bot.state.daily_profit == pytest.approx(0.5)
        assert bot.state.daily_budget_spent_usdc == pytest.approx(2.0)
        assert bot.state.daily_budget_returned_usdc == pytest.approx(2.5)
        assert bot._daily_budget_left() == pytest.approx(7.5)

        panel = tf.render_results(bot.state)
        console = Console(record=True, width=120)
        console.print(panel)
        text = console.export_text()
        assert "returned=$2.50" in text
        assert "left=$7.50" in text
        assert "earned=$0.50" in text

    asyncio.run(run_case())


def test_daily_budget_cashflow_loss_spends_without_return(tmp_path, monkeypatch):
    async def run_case():
        monkeypatch.setattr(tf, "DAILY_BUDGET_USDC", 7.0)
        bot = make_bot(tmp_path)
        now = datetime.now(timezone.utc)
        pos = make_position(
            condition_id="0xbudget-loss",
            direction="UP",
            order_id="SIM-BUDGET-LOSS",
            now=now,
        )

        bot._record_daily_budget_open(pos)
        await bot._settle_position(pos, "DOWN", pos.amount_usdc)

        assert pos.status == "lost"
        assert pos.pnl == pytest.approx(-2.0)
        assert bot.state.daily_loss == pytest.approx(2.0)
        assert bot.state.daily_profit == pytest.approx(0.0)
        assert bot.state.daily_budget_spent_usdc == pytest.approx(2.0)
        assert bot.state.daily_budget_returned_usdc == pytest.approx(0.0)
        assert bot._daily_budget_left() == pytest.approx(5.0)

    asyncio.run(run_case())


def test_daily_budget_halt_lifts_after_gross_return(tmp_path, monkeypatch):
    async def run_case():
        monkeypatch.setattr(tf, "DAILY_BUDGET_USDC", 2.0)
        bot = make_bot(tmp_path)
        now = datetime.now(timezone.utc)
        pos = make_position(
            condition_id="0xbudget-halt-lift",
            direction="UP",
            order_id="SIM-BUDGET-HALT-LIFT",
            now=now,
        )
        pos.entry_price = 0.8
        pos.size = 2.5
        pos.amount_usdc = 2.0

        bot._record_daily_budget_open(pos)
        bot._sync_daily_budget_halt()

        assert bot.state.daily_halted is True

        await bot._settle_position(pos, "UP", pos.amount_usdc)

        assert bot.state.daily_budget_spent_usdc == pytest.approx(2.0)
        assert bot.state.daily_budget_returned_usdc == pytest.approx(2.5)
        assert bot._daily_budget_left() == pytest.approx(2.5)
        assert bot.state.daily_halted is False

    asyncio.run(run_case())


def test_daily_budget_cashflow_canceled_trade_returns_stake(tmp_path, monkeypatch):
    async def run_case():
        monkeypatch.setattr(tf, "DAILY_BUDGET_USDC", 7.0)
        bot = make_bot(tmp_path)
        now = datetime.now(timezone.utc)
        pos = make_position(
            condition_id="0xbudget-cancel",
            direction="UP",
            order_id="SIM-BUDGET-CANCEL",
            now=now,
        )

        bot._record_daily_budget_open(pos)
        await bot._mark_position_canceled(pos, "test cancel")

        assert pos.status == "canceled"
        assert bot.state.daily_budget_spent_usdc == pytest.approx(2.0)
        assert bot.state.daily_budget_returned_usdc == pytest.approx(2.0)
        assert bot._daily_budget_left() == pytest.approx(7.0)

    asyncio.run(run_case())


def test_daily_budget_cashflow_replays_today_trade_log(tmp_path, monkeypatch):
    monkeypatch.setattr(tf, "DAILY_BUDGET_USDC", 7.0)
    bot = make_bot(tmp_path)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    placed_at = datetime.now(timezone.utc).isoformat()
    open_record = {
        "event": "open",
        "condition_id": "0xbudget-replay",
        "direction": "UP",
        "order_id": "SIM-BUDGET-REPLAY",
        "placed_at": placed_at,
        "amount_usdc": 2.0,
        "entry_price": 0.8,
    }
    close_record = {
        "event": "close",
        "condition_id": "0xbudget-replay",
        "direction": "UP",
        "order_id": "SIM-BUDGET-REPLAY",
        "placed_at": placed_at,
        "status": "won",
        "amount_usdc": 2.0,
        "entry_price": 0.8,
        "pnl": 0.5,
    }
    path = tmp_path / "logs" / f"trades_{day}.jsonl"
    path.write_text(
        json.dumps(open_record) + "\n" + json.dumps(close_record) + "\n",
        encoding="utf-8",
    )

    counted = bot._warm_daily_budget_cashflow(day)
    bot._sync_daily_budget_halt()

    assert counted == 2
    assert bot.state.daily_budget_spent_usdc == pytest.approx(2.0)
    assert bot.state.daily_budget_returned_usdc == pytest.approx(2.5)
    assert bot._daily_budget_left() == pytest.approx(7.5)
    assert bot.state.daily_halted is False


def test_load_recent_trade_history_joins_settled_trade_records(tmp_path):
    logger = tf.BotLogger(tmp_path / "logs")
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    base = datetime.now(timezone.utc).replace(microsecond=0)
    path = tmp_path / "logs" / f"trades_{day}.jsonl"
    records = [
        {
            "ts": (base - timedelta(minutes=5)).isoformat(),
            "event": "open",
            "condition_id": "0xhist-win",
            "direction": "UP",
            "order_id": "SIM-HIST-WIN",
            "placed_at": (base - timedelta(minutes=5)).isoformat(),
            "amount_usdc": 2.0,
            "entry_price": 0.8,
            "simulated": True,
        },
        {
            "ts": (base - timedelta(minutes=4)).isoformat(),
            "event": "close",
            "condition_id": "0xhist-win",
            "direction": "UP",
            "order_id": "SIM-HIST-WIN",
            "placed_at": (base - timedelta(minutes=5)).isoformat(),
            "status": "won",
            "amount_usdc": 2.0,
            "entry_price": 0.8,
            "pnl": 0.5,
            "simulated": True,
        },
        {
            "ts": (base - timedelta(minutes=3)).isoformat(),
            "event": "open",
            "condition_id": "0xhist-loss",
            "direction": "DOWN",
            "order_id": "SIM-HIST-LOSS",
            "placed_at": (base - timedelta(minutes=3)).isoformat(),
            "amount_usdc": 3.0,
            "entry_price": 0.6,
            "simulated": False,
        },
        {
            "ts": (base - timedelta(minutes=2)).isoformat(),
            "event": "close",
            "condition_id": "0xhist-loss",
            "direction": "DOWN",
            "order_id": "SIM-HIST-LOSS",
            "placed_at": (base - timedelta(minutes=3)).isoformat(),
            "status": "lost",
            "amount_usdc": 3.0,
            "entry_price": 0.6,
            "pnl": -3.0,
            "simulated": False,
        },
        {
            "ts": (base - timedelta(minutes=1)).isoformat(),
            "event": "close",
            "condition_id": "0xhist-cancel",
            "direction": "UP",
            "order_id": "SIM-HIST-CANCEL",
            "status": "canceled",
            "amount_usdc": 1.0,
            "pnl": 0.0,
        },
    ]
    path.write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")

    history = logger.load_recent_trade_history(limit=10)

    assert len(history) == 2
    assert history[0].condition_id == "0xhist-loss"
    assert history[0].direction == "DOWN"
    assert history[0].amount_usdc == pytest.approx(3.0)
    assert history[0].pnl == pytest.approx(-3.0)
    assert history[0].status == "lost"
    assert history[0].simulated is False
    assert history[1].condition_id == "0xhist-win"
    assert history[1].direction == "UP"
    assert history[1].amount_usdc == pytest.approx(2.0)
    assert history[1].pnl == pytest.approx(0.5)
    assert history[1].status == "won"
    assert history[1].simulated is True


def test_render_bet_history_shows_win_loss_amount_and_pnl(tmp_path):
    state = tf.BotState(logger=tf.BotLogger(tmp_path / "logs"))
    now = datetime.now(timezone.utc).replace(microsecond=0)
    for idx in range(21, 32):
        won = idx % 2 == 0
        state.trade_history.appendleft(tf.TradeHistoryEntry(
            direction="UP" if won else "DOWN",
            amount_usdc=float(idx),
            pnl=0.5 if won else -3.0,
            status="won" if won else "lost",
            placed_at=now - timedelta(minutes=idx),
            closed_at=now + timedelta(minutes=idx),
            simulated=won,
            order_id=f"SIM-{idx}",
            condition_id=f"0x{idx}",
        ))

    panel = tf.render_bet_history(state)
    console = Console(record=True, width=100)
    console.print(panel)
    text = console.export_text()

    assert "BET HISTORY" in text
    assert "UP" in text
    assert "DOWN" in text
    assert "$31.00" in text
    assert "$22.00" in text
    assert "$21.00" not in text
    assert "+$0.50" in text
    assert "-$3.00" in text
    assert "WIN" in text
    assert "LOSE" in text


def test_update_ui_updates_bet_history_and_price_panels(tmp_path, monkeypatch):
    async def run_case():
        monkeypatch.setattr(tf, "UI_REFRESH_S", 0.01)
        monkeypatch.setattr(tf, "TRADE_HISTORY_REFRESH_S", 0.01)
        state = tf.BotState(logger=tf.BotLogger(tmp_path / "logs"))
        now = datetime.now(timezone.utc).replace(microsecond=0)
        state.trade_history.append(tf.TradeHistoryEntry(
            direction="UP",
            amount_usdc=2.0,
            pnl=0.5,
            status="won",
            placed_at=now - timedelta(minutes=5),
            closed_at=now,
            simulated=True,
            order_id="SIM-WIN",
            condition_id="0xwin",
        ))
        state.price_tick_log.append((now, 100.0, 0.2, 0.1, 0.1, 0.55, 0.45))
        layout = tf.build_layout()

        task = asyncio.create_task(tf.update_ui(layout, state))
        await asyncio.sleep(0.02)

        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        placed_at = now.isoformat()
        close_at = (now + timedelta(minutes=1)).isoformat()
        path = tmp_path / "logs" / f"trades_{day}.jsonl"
        records = [
            {
                "ts": placed_at,
                "event": "open",
                "condition_id": "0xui-new",
                "direction": "DOWN",
                "order_id": "SIM-UI-NEW",
                "placed_at": placed_at,
                "amount_usdc": 4.0,
                "entry_price": 0.5,
                "simulated": True,
            },
            {
                "ts": close_at,
                "event": "close",
                "condition_id": "0xui-new",
                "direction": "DOWN",
                "order_id": "SIM-UI-NEW",
                "placed_at": placed_at,
                "status": "lost",
                "amount_usdc": 4.0,
                "entry_price": 0.5,
                "pnl": -4.0,
                "simulated": True,
            },
        ]
        path.write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")
        await asyncio.sleep(0.04)
        state.running = False
        await task

        assert "BET HISTORY" in str(layout["bet_history"].renderable.title)
        assert "PRICES" in str(layout["price_log"].renderable.title)
        assert state.trade_history[0].condition_id == "0xui-new"

        console = Console(record=True, width=100)
        console.print(layout["bet_history"].renderable)
        text = console.export_text()
        assert "$4.00" in text
        assert "-$4.00" in text
        assert "LOSE" in text

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
    monkeypatch.setattr(tf, "DAILY_BUDGET_USDC", 7.0)
    bot = make_bot(tmp_path)
    bot.state.balance_usdc = 0.73
    bot.state.daily_budget_spent_usdc = 2.0
    bot.state.daily_budget_returned_usdc = 2.5
    bot.state.paper_stats.paper_trade_wins_total = 3
    bot.state.paper_stats.paper_trade_losses_total = 1
    bot.state.paper_stats.paper_trade_wins_today = 1
    bot.state.paper_stats.paper_trade_losses_today = 0
    bot.state.claimable_total = 5.5
    bot.state.pending_claim_count = 1
    bot.state.expected_claimable_total = 2.5
    bot.state.expected_claim_pending_count = 1
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
    assert "spent=$" in text
    assert "returned=$" in text
    assert "left=$" in text
    assert "pending=$2.50" in text
    assert "Claim log" not in text


def test_render_results_shows_real_claim_log_without_hiding_budget_rows(tmp_path, monkeypatch):
    monkeypatch.setattr(tf, "DAILY_BUDGET_USDC", 7.0)
    bot = make_bot(tmp_path)
    bot.state.balance_usdc = 0.73
    bot.state.daily_budget_spent_usdc = 2.0
    bot.state.daily_budget_returned_usdc = 2.5
    bot.state.claimable_total = 5.5
    bot.state.pending_claim_count = 1
    bot.state.expected_claimable_total = 2.5
    bot.state.expected_claim_pending_count = 1
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
    assert "spent=$" in text
    assert "returned=$" in text
    assert "left=$" in text
    assert "pending=$2.50" in text


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
        monkeypatch.setattr(tf, "POLY_FUNDER", "")
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
        monkeypatch.setattr(tf, "POLY_FUNDER", "")
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
        assert bot.state.claimable_total == pytest.approx(0.0)
        assert bot.state.expected_claimable_total == pytest.approx(0.0)

    asyncio.run(run_case())


def test_live_win_creates_local_expected_pending_claim(tmp_path):
    async def run_case():
        bot = make_bot(tmp_path)
        now = datetime.now(timezone.utc)
        pos = make_position(
            condition_id="0xlivewin",
            direction="UP",
            order_id="LIVE-WIN-1",
            now=now,
        )
        pos.simulated = False
        pos.entry_price = 0.8
        pos.amount_usdc = 2.0
        pos.size = 2.5

        await bot._settle_position(pos, "UP", pos.amount_usdc)

        claim = bot.state.claim_records["0xlivewin"]
        assert claim.status == "expected_pending"
        assert claim.claim_source == "local_trade_settlement"
        assert claim.claimable_amount == pytest.approx(2.5)
        assert bot.state.claimable_total == pytest.approx(0.0)
        assert bot.state.expected_claimable_total == pytest.approx(2.5)
        assert bot.state.expected_claim_pending_count == 1

        panel = tf.render_results(bot.state)
        console = Console(record=True, width=120)
        console.print(panel)
        text = console.export_text()
        assert "amt=$0.00" in text
        assert "pending=$2.50" in text

    asyncio.run(run_case())


def test_paper_settlement_notifies_clean_win_and_loss(tmp_path):
    async def run_case():
        bot = make_bot(tmp_path)
        now = datetime.now(timezone.utc)
        win_pos = make_position(
            condition_id="0xpaperwin",
            direction="UP",
            order_id="SIM-WIN",
            now=now,
        )
        win_pos.size = 3.856
        win_pos.amount_usdc = 2.0
        win_pos.fee_usdc = 0.072

        loss_pos = make_position(
            condition_id="0xpaperloss",
            direction="DOWN",
            order_id="SIM-LOSS",
            now=now,
        )
        loss_pos.size = 3.856
        loss_pos.amount_usdc = 2.0

        await bot._settle_position(win_pos, "UP", win_pos.amount_usdc)
        await bot._settle_position(loss_pos, "UP", loss_pos.amount_usdc)

        assert win_pos.status == "won"
        assert win_pos.pnl == pytest.approx(1.856)
        assert loss_pos.status == "lost"
        assert loss_pos.pnl == pytest.approx(-2.0)
        assert bot.notifier.result_calls == [
            ("UP", "won", pytest.approx(1.856), True),
            ("DOWN", "lost", pytest.approx(-2.0), True),
        ]

    asyncio.run(run_case())


def test_server_claim_candidate_moves_expected_pending_to_claimable(tmp_path, monkeypatch):
    async def run_case():
        bot = make_bot(tmp_path)
        bot._persist_expected_claim_state(tf.ClaimRecord(
            claim_id="0xserver",
            condition_id="0xserver",
            claimable_amount=2.5,
            claim_source="local_trade_settlement",
            status="expected_pending",
            last_seen_at=datetime.now(timezone.utc).isoformat(),
        ))
        bot.market = DummyMarket(
            positions=[
                {
                    "conditionId": "0xserver",
                    "asset": "asset-up",
                    "outcome": "Yes",
                    "outcomeIndex": 0,
                    "currentValue": 2.5,
                    "redeemable": True,
                    "mergeable": False,
                    "negativeRisk": False,
                    "title": "BTC above?",
                }
            ]
        )
        monkeypatch.setattr(tf, "POLY_ADDRESS", "0x123")
        monkeypatch.setattr(tf, "POLY_FUNDER", "")
        monkeypatch.setattr(tf, "AUTO_CLAIM_ENABLED", False)
        monkeypatch.setattr(tf, "AUTO_CLAIM_THRESHOLD", 1.0)

        await bot._scan_and_process_claims(trigger="test")

        claim = bot.state.claim_records["0xserver"]
        assert claim.status == "queued"
        assert claim.claim_source == "positions_api_redeemable"
        assert claim.claimable_amount == pytest.approx(2.5)
        assert bot.state.claimable_total == pytest.approx(2.5)
        assert bot.state.expected_claimable_total == pytest.approx(0.0)
        assert bot.state.pending_claim_count == 1

    asyncio.run(run_case())


def test_claim_scan_queries_address_and_funder_and_dedupes_candidates(tmp_path, monkeypatch):
    async def run_case():
        def positions_for_user(kwargs):
            value = 1.0 if kwargs.get("user") == "0xaddr" else 3.0
            return [
                {
                    "conditionId": "0xdup",
                    "asset": "asset-up",
                    "outcome": "Yes",
                    "outcomeIndex": 0,
                    "currentValue": value,
                    "redeemable": True,
                    "mergeable": False,
                    "negativeRisk": False,
                    "title": "BTC above?",
                }
            ]

        bot = make_bot(tmp_path)
        bot.market = DummyMarket(positions=positions_for_user)
        monkeypatch.setattr(tf, "POLY_ADDRESS", "0xaddr")
        monkeypatch.setattr(tf, "POLY_FUNDER", "0xfund")
        monkeypatch.setattr(tf, "AUTO_CLAIM_ENABLED", False)
        monkeypatch.setattr(tf, "AUTO_CLAIM_THRESHOLD", 1.0)

        await bot._scan_and_process_claims(trigger="test")

        users = [call["user"] for call in bot.market.position_calls]
        assert users == ["0xaddr", "0xfund"]
        assert bot.state.claim_last_scan_candidates == 1
        assert bot.state.claim_last_scan_identities == ["address:0xaddr", "funder:0xfund"]
        claim = bot.state.claim_records["0xdup"]
        assert claim.claimable_amount == pytest.approx(3.0)
        assert bot.state.claimable_total == pytest.approx(3.0)

    asyncio.run(run_case())


def test_claim_scan_records_positions_api_error(tmp_path, monkeypatch):
    class ErrorMarket(DummyMarket):
        async def get_current_positions(self, **kwargs):
            self.position_calls.append(kwargs)
            self._last_positions_status = "http_502"
            self._last_positions_error = "bad gateway"
            return []

    async def run_case():
        bot = make_bot(tmp_path)
        bot.market = ErrorMarket()
        monkeypatch.setattr(tf, "POLY_ADDRESS", "0x123")
        monkeypatch.setattr(tf, "POLY_FUNDER", "")
        monkeypatch.setattr(tf, "AUTO_CLAIM_ENABLED", False)

        await bot._scan_and_process_claims(trigger="test")

        assert bot.state.claim_last_scan_candidates == 0
        assert bot.state.claim_last_scan_status == "address:http_502"
        assert "bad gateway" in bot.state.claim_last_scan_error

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


def test_paper_buy_signal_sends_signal_notification(tmp_path):
    async def run_case():
        bot = make_bot(tmp_path)
        now = datetime.now(timezone.utc)
        win = make_window(condition_id="0xsignal-paper", beat_price=100.0, end_time=now + timedelta(minutes=1))
        snap = SimpleNamespace(signal_alignment=5, cvd_divergence="BULLISH")
        signal = tf.AISignal(
            signal="BUY_UP",
            confidence=0.88,
            raw_confidence=0.89,
            reason="paper buy signal",
            dip_label="SUSTAINED_ABOVE",
            source="ml",
        )
        decision = tf.TradeDecision(
            action="BUY",
            direction="UP",
            confidence=signal.confidence,
            reason="ok",
            gate=tf.GATE_OK,
        )

        emitted = await bot._emit_locked_signal_notification(
            locked_now=True,
            signal=signal,
            win=win,
            snap=snap,
            decision=decision,
            execution_block=None,
            btc_price=100.4,
            up_odds=0.58,
            down_odds=0.42,
        )

        assert emitted is True
        assert bot.notifier.signal_calls == [
            (
                "BUY_UP",
                win.condition_id,
                {
                    "btc_price": 100.4,
                    "up_odds": 0.58,
                    "down_odds": 0.42,
                    "decision": decision,
                },
            )
        ]
        assert bot.notifier.shadow_calls == []
        assert bot.state.session_signal_state.telegram_sent is True

    asyncio.run(run_case())


def test_place_trade_opens_simulated_position_in_paper_mode(tmp_path, monkeypatch):
    class StubMarket:
        async def get_execution_quote(self, direction, token_id, amount_usdc, current_odds):
            return make_execution_quote(token_id=token_id, amount_usdc=amount_usdc, price=current_odds)

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
        monkeypatch.setattr(tf, "LIVE_TRADING", False)
        bot = make_bot(tmp_path)
        bot.market = StubMarket()
        bot.state.balance_usdc = 0.0
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
        direction, bet_size, entry_odds, simulated, kwargs = bot.notifier.bet_calls[0]
        assert direction == "UP"
        assert bet_size > 0
        assert entry_odds == pytest.approx(0.56)
        assert simulated is True
        assert kwargs["expected_payout"] == pytest.approx(bot.state.positions[0].size)
        assert all(
            "INSUFFICIENT_BALANCE_PRECHECK" not in message
            for _, message in bot.state.event_log
        )

    asyncio.run(run_case())


def test_place_trade_skips_when_midpoint_edge_disappears_at_best_ask(tmp_path, monkeypatch):
    class StubMarket:
        async def get_execution_quote(self, direction, token_id, amount_usdc, current_odds):
            est = tf.estimate_buy_net_shares(amount_usdc, 0.70, 0.072)
            return tf.ExecutionQuote(
                token_id=token_id,
                amount_usdc=amount_usdc,
                mid_price=0.55,
                best_bid=0.68,
                best_ask=0.70,
                avg_price=0.70,
                spread=0.02,
                gross_shares=est["gross_shares"],
                net_shares=est["net_shares"],
                fee_usdc=est["fee_usdc"],
                fee_shares=est["fee_shares"],
                fee_rate=0.072,
                fee_rate_source="fee-rate",
                min_order_size=1.0,
                enough_liquidity=True,
                liquidity_source="orderbook",
            )

        async def place_bet(self, direction, token_id, amount_usdc, current_odds):
            raise AssertionError("place_bet should not run when ask-level net EV is below the gate")

    async def run_case():
        monkeypatch.setattr(tf, "LIVE_TRADING", False)
        bot = make_bot(tmp_path)
        bot.market = StubMarket()
        now = datetime.now(timezone.utc)
        win = make_window(condition_id="0xask-edge", beat_price=100.0, end_time=now + timedelta(minutes=1))
        snap = SimpleNamespace(signal_alignment=5, cvd_divergence="BULLISH")
        signal = tf.AISignal(
            signal="BUY_UP",
            confidence=0.75,
            raw_confidence=0.75,
            reason="ask edge",
            dip_label="SUSTAINED_ABOVE",
            source="ml",
        )
        record = tf.WindowPredictionRecord(
            row_id="row-ask-edge",
            condition_id=win.condition_id,
            window_label=win.window_label,
            window_end_at=win.end_time,
            beat_price=win.beat_price,
            mode="paper",
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

        await bot._place_trade(
            win,
            signal,
            snap,
            prices=[100.0, 100.1],
            is_gold_zone=True,
            prediction_row_id=record.row_id,
        )

        updated = bot.state.paper_prediction_records[win.condition_id]
        assert len(bot.state.positions) == 0
        assert updated.blocked_gate == tf.GATE_NET_EDGE
        assert updated.mid_odds == pytest.approx(0.55)
        assert updated.best_ask == pytest.approx(0.70)
        assert updated.net_edge < tf.MIN_NET_EDGE
        assert len(bot.notifier.shadow_calls) == 1
        assert bot.notifier.shadow_calls[0][2]["blocked_gate"] == tf.GATE_NET_EDGE

    asyncio.run(run_case())


def test_place_trade_allows_non_orderbook_execution_quote_in_paper_mode(tmp_path, monkeypatch):
    class StubMarket:
        async def get_execution_quote(self, direction, token_id, amount_usdc, current_odds):
            return make_execution_quote(
                token_id=token_id,
                amount_usdc=amount_usdc,
                price=current_odds,
                liquidity_source="legacy_odds_fallback",
            )

        async def place_bet(self, direction, token_id, amount_usdc, current_odds):
            est = tf.estimate_buy_net_shares(amount_usdc, current_odds, tf.POLYMARKET_CRYPTO_TAKER_FEE_RATE)
            return tf.TradeResult(
                success=True,
                order_id="SIM-FALLBACK",
                simulated=True,
                size=est["net_shares"],
                gross_size=est["gross_shares"],
                price=current_odds,
                amount_usdc=amount_usdc,
                fee_usdc=est["fee_usdc"],
                fee_rate=tf.POLYMARKET_CRYPTO_TAKER_FEE_RATE,
                fee_rate_source="fee-rate",
                payout_per_dollar=est["payout_per_dollar"],
                liquidity_source="legacy_odds_fallback",
            )

    async def run_case():
        monkeypatch.setattr(tf, "LIVE_TRADING", False)
        monkeypatch.setattr(tf, "ALLOW_FALLBACK_EXECUTION_QUOTES", False)
        bot = make_bot(tmp_path)
        bot.market = StubMarket()
        now = datetime.now(timezone.utc)
        win = make_window(condition_id="0xfallback-quote", beat_price=100.0, end_time=now + timedelta(minutes=1))
        snap = SimpleNamespace(signal_alignment=5, cvd_divergence="BULLISH")
        signal = tf.AISignal(
            signal="BUY_UP",
            confidence=0.91,
            raw_confidence=0.91,
            reason="quote fallback",
            dip_label="SUSTAINED_ABOVE",
            source="ml",
        )
        record = tf.WindowPredictionRecord(
            row_id="row-fallback-quote",
            condition_id=win.condition_id,
            window_label=win.window_label,
            window_end_at=win.end_time,
            beat_price=win.beat_price,
            mode="paper",
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

        await bot._place_trade(
            win,
            signal,
            snap,
            prices=[100.0, 100.1],
            is_gold_zone=True,
            prediction_row_id=record.row_id,
        )

        updated = bot.state.paper_prediction_records[win.condition_id]
        assert len(bot.state.positions) == 1
        assert bot.state.positions[0].simulated is True
        assert updated.blocked_gate == ""
        assert updated.simulated_order_id == "SIM-FALLBACK"
        assert len(bot.notifier.bet_calls) == 1
        assert updated.liquidity_source == "legacy_odds_fallback"

    asyncio.run(run_case())


def test_place_trade_blocks_non_orderbook_execution_quote_in_live_mode(tmp_path, monkeypatch):
    class StubMarket:
        async def get_execution_quote(self, direction, token_id, amount_usdc, current_odds):
            return make_execution_quote(
                token_id=token_id,
                amount_usdc=amount_usdc,
                price=current_odds,
                liquidity_source="legacy_odds_fallback",
            )

        async def place_bet(self, direction, token_id, amount_usdc, current_odds):
            raise AssertionError("live fallback quotes must be blocked before order placement")

    async def run_case():
        monkeypatch.setattr(tf, "LIVE_TRADING", True)
        monkeypatch.setattr(tf, "ALLOW_FALLBACK_EXECUTION_QUOTES", False)
        bot = make_bot(tmp_path)
        bot.market = StubMarket()
        bot.state.balance_usdc = 200.0
        now = datetime.now(timezone.utc)
        win = make_window(condition_id="0xlive-fallback-quote", beat_price=100.0, end_time=now + timedelta(minutes=1))
        snap = SimpleNamespace(signal_alignment=5, cvd_divergence="BULLISH")
        signal = tf.AISignal(
            signal="BUY_UP",
            confidence=0.91,
            raw_confidence=0.91,
            reason="live quote fallback",
            dip_label="SUSTAINED_ABOVE",
            source="ml",
        )
        record = tf.WindowPredictionRecord(
            row_id="row-live-fallback-quote",
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

        await bot._place_trade(
            win,
            signal,
            snap,
            prices=[100.0, 100.1],
            is_gold_zone=True,
            prediction_row_id=record.row_id,
        )

        updated = bot.state.paper_prediction_records[win.condition_id]
        assert len(bot.state.positions) == 0
        assert updated.blocked_gate == tf.GATE_EXECUTION_QUOTE
        assert updated.liquidity_source == "legacy_odds_fallback"

    asyncio.run(run_case())


def test_place_trade_records_oracle_divergence_gate(tmp_path, monkeypatch):
    class StubMarket:
        async def get_execution_quote(self, direction, token_id, amount_usdc, current_odds):
            return make_execution_quote(token_id=token_id, amount_usdc=amount_usdc, price=current_odds)

        async def place_bet(self, direction, token_id, amount_usdc, current_odds):
            raise AssertionError("oracle divergence should block before dummy/live order placement")

    async def run_case():
        monkeypatch.setattr(tf, "LIVE_TRADING", False)
        monkeypatch.setattr(tf, "SKIP_ON_HIGH_DIVERGENCE", True)
        monkeypatch.setattr(tf, "ORACLE_DIVERGENCE_ALERT_USD", 15.0)
        bot = make_bot(tmp_path)
        bot.market = StubMarket()
        bot.state.btc_price = 120.0
        bot.state.pyth_btc_price = 100.0
        now = datetime.now(timezone.utc)
        win = make_window(condition_id="0xoracle-div", beat_price=100.0, end_time=now + timedelta(minutes=1))
        snap = SimpleNamespace(signal_alignment=5, cvd_divergence="BULLISH")
        signal = tf.AISignal(
            signal="BUY_UP",
            confidence=0.91,
            raw_confidence=0.91,
            reason="oracle divergence",
            dip_label="SUSTAINED_ABOVE",
            source="ml",
        )
        record = tf.WindowPredictionRecord(
            row_id="row-oracle-div",
            condition_id=win.condition_id,
            window_label=win.window_label,
            window_end_at=win.end_time,
            beat_price=win.beat_price,
            mode="paper",
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

        await bot._place_trade(
            win,
            signal,
            snap,
            prices=[100.0, 100.1],
            is_gold_zone=True,
            prediction_row_id=record.row_id,
        )

        updated = bot.state.paper_prediction_records[win.condition_id]
        assert len(bot.state.positions) == 0
        assert updated.blocked_gate == tf.GATE_ORACLE_DIVERGENCE
        assert updated.net_edge >= tf.MIN_NET_EDGE

    asyncio.run(run_case())


def test_place_trade_skips_when_market_minimum_exceeds_risk_cap(tmp_path, monkeypatch):
    class StubMarket:
        def __init__(self):
            self.bet_calls = []

        async def get_execution_quote(self, direction, token_id, amount_usdc, current_odds):
            return make_execution_quote(
                token_id=token_id,
                amount_usdc=amount_usdc,
                price=current_odds,
                min_order_size=5.0,
            )

        async def get_min_order_size(self, token_id):
            return 5.0

        async def place_bet(self, direction, token_id, amount_usdc, current_odds):
            raise AssertionError("place_bet should not run when market minimum exceeds risk cap")

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
        record = tf.WindowPredictionRecord(
            row_id="row-live-min",
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

        monkeypatch.setattr(tf, "LIVE_TRADING", True)

        await bot._place_trade(
            win,
            signal,
            snap,
            prices=[100.0, 100.1],
            is_gold_zone=True,
            prediction_row_id="row-live-min",
        )

        updated = bot.state.paper_prediction_records[win.condition_id]
        assert bot.market.bet_calls == []
        assert len(bot.state.positions) == 0
        assert updated.blocked_gate == tf.GATE_MIN_ORDER_RISK
        assert bot.state.engine_gate == tf.GATE_MIN_ORDER_RISK

    asyncio.run(run_case())


def test_operational_execution_block_enforces_weekday_wib_bet_session(tmp_path, monkeypatch):
    monkeypatch.setattr(tf, "BET_SESSION_WIB_ENABLED", True)
    monkeypatch.setattr(tf, "BET_SESSION_WEEKDAYS_ONLY", True)
    monkeypatch.setattr(tf, "BET_SESSION_START_HOUR_WIB", 13)
    monkeypatch.setattr(tf, "BET_SESSION_END_HOUR_WIB", 5)
    monkeypatch.setattr(tf, "DAILY_BUDGET_USDC", 0)
    monkeypatch.setattr(tf, "DAILY_PROFIT_TARGET_USDC", 0)

    bot = make_bot(tmp_path)
    win = make_window(
        condition_id="0xwib-session",
        beat_price=100.0,
        end_time=datetime(2026, 4, 13, 7, 0, tzinfo=timezone.utc),
    )

    assert bot._operational_execution_block(
        win=win,
        seconds_remaining=45,
        now=_wib_ts(2026, 4, 13, 13, 0),
    ) is None
    assert bot._operational_execution_block(
        win=win,
        seconds_remaining=45,
        now=_wib_ts(2026, 4, 14, 4, 59),
    ) is None
    assert bot._operational_execution_block(
        win=win,
        seconds_remaining=45,
        now=_wib_ts(2026, 4, 18, 4, 59),
    ) is None

    blocked_before = bot._operational_execution_block(
        win=win,
        seconds_remaining=45,
        now=_wib_ts(2026, 4, 13, 12, 59),
    )
    blocked_monday_morning = bot._operational_execution_block(
        win=win,
        seconds_remaining=45,
        now=_wib_ts(2026, 4, 13, 4, 59),
    )
    blocked_weekend = bot._operational_execution_block(
        win=win,
        seconds_remaining=45,
        now=_wib_ts(2026, 4, 18, 5, 0),
    )

    assert blocked_before[0] == tf.GATE_BET_SESSION
    assert blocked_monday_morning[0] == tf.GATE_BET_SESSION
    assert blocked_weekend[0] == tf.GATE_BET_SESSION


def test_retryable_live_trade_failure_allows_later_retry_in_same_window(tmp_path, monkeypatch):
    monkeypatch.setattr(tf, "BET_SESSION_WIB_ENABLED", False)

    class StubMarket:
        def __init__(self):
            self.bet_calls = 0

        async def get_execution_quote(self, direction, token_id, amount_usdc, current_odds):
            return make_execution_quote(token_id=token_id, amount_usdc=amount_usdc, price=current_odds)

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
        async def get_execution_quote(self, direction, token_id, amount_usdc, current_odds):
            return make_execution_quote(token_id=token_id, amount_usdc=amount_usdc, price=current_odds)

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
        async def get_execution_quote(self, direction, token_id, amount_usdc, current_odds):
            return make_execution_quote(token_id=token_id, amount_usdc=amount_usdc, price=current_odds)

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


def test_daily_budget_preflight_holds_trade_without_strategy_block(tmp_path, monkeypatch):
    class StubMarket:
        async def get_execution_quote(self, direction, token_id, amount_usdc, current_odds):
            return make_execution_quote(token_id=token_id, amount_usdc=amount_usdc, price=current_odds)

        async def place_bet(self, direction, token_id, amount_usdc, current_odds):
            raise AssertionError("place_bet should not run when daily budget left is too small")

    async def run_case():
        monkeypatch.setattr(tf, "DAILY_BUDGET_USDC", 7.0)
        monkeypatch.setattr(tf, "LIVE_TRADING", False)
        monkeypatch.setattr(tf, "compute_kelly_size", lambda **_kwargs: 2.0)
        bot = make_bot(tmp_path)
        bot.market = StubMarket()
        bot.state.daily_budget_spent_usdc = 6.0
        now = datetime.now(timezone.utc)
        win = make_window(condition_id="0xbudget-hold", beat_price=100.0, end_time=now + timedelta(minutes=1))
        snap = SimpleNamespace(signal_alignment=5, cvd_divergence="BULLISH")
        signal = tf.AISignal(
            signal="BUY_UP",
            confidence=0.91,
            raw_confidence=0.91,
            reason="budget hold",
            dip_label="SUSTAINED_ABOVE",
            source="ml",
        )
        record = tf.WindowPredictionRecord(
            row_id="row-budget-hold",
            condition_id=win.condition_id,
            window_label=win.window_label,
            window_end_at=win.end_time,
            beat_price=win.beat_price,
            mode="paper",
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
        assert updated.placement_failure_code == "DAILY_BUDGET_PRECHECK"
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
        bot.state.settlement_registry_cache[pos.condition_id] = {
            "settlement_price": 100.3,
            "settlement_source": "chainlink_market_resolved",
            "settlement_source_priority": tf._label_source_priority("chainlink_market_resolved"),
        }

        await bot._check_positions()

        assert pos.status == "won"
        assert pos.pnl == pytest.approx(2.5)

    asyncio.run(run_case())


def test_equal_settlement_resolves_up_not_void(tmp_path):
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
        bot.state.settlement_registry_cache[pos.condition_id] = {
            "settlement_price": pos.window_beat,
            "settlement_source": "chainlink_market_resolved",
            "settlement_source_priority": tf._label_source_priority("chainlink_market_resolved"),
        }

        await bot._check_positions()

        assert pos.status == "lost"
        assert pos.pnl == pytest.approx(-2.0)
        assert bot.state.win_count == 0
        assert bot.state.loss_count == 1
        assert bot.state.paper_stats.paper_trade_total == 1

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
