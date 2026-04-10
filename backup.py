from __future__ import annotations


# ══════════════════════════════════════════════════════════════════════════════
# Source: config.py
# ══════════════════════════════════════════════════════════════════════════════

import os
from dotenv import load_dotenv

load_dotenv()

# ── Polymarket credentials ──────────────────────────────────────────────────
# POLY_PRIVATE_KEY is the UUID-format Polymarket Relayer API key (NOT an ETH private key).
# It is kept here for reference but NOT passed to ClobClient.
POLY_PRIVATE_KEY = os.getenv("POLY_PRIVATE_KEY", "")
POLY_FUNDER      = os.getenv("POLY_FUNDER", "")
POLY_ADDRESS     = os.getenv("POLY_ADDRESS", "")
POLY_API_KEY     = os.getenv("POLY_API_KEY", "")
POLY_SECRET      = os.getenv("POLY_SECRET", "")
POLY_PASSPHRASE  = os.getenv("POLY_PASSPHRASE", "")

# POLY_ETH_PRIVATE_KEY: actual Ethereum hex private key (64-char hex, with or without 0x prefix).
# Required ONLY for LIVE_TRADING=true (order signing).
# Export from your wallet / Magic.link. Keep secret — never commit.
POLY_ETH_PRIVATE_KEY = os.getenv("POLY_ETH_PRIVATE_KEY", "")

# ── OpenRouter ───────────────────────────────────────────────────────────────
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE    = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL   = "google/gemma-4-26b-a4b-it:free"
AI_TIMEOUT_S       = 15

# ── API base URLs ────────────────────────────────────────────────────────────
CLOB_HOST = "https://clob.polymarket.com"
GAMMA_API = "https://gamma-api.polymarket.com"
CHAIN_ID  = 137

# ── WebSocket URLs ───────────────────────────────────────────────────────────
BINANCE_WS = "wss://stream.binance.com:9443/ws/btcusdc@trade"
MARKET_WS  = "wss://ws-subscriptions-clob.polymarket.com/ws/market"
USER_WS    = "wss://ws-subscriptions-clob.polymarket.com/ws/user"

# ── BTC feed ─────────────────────────────────────────────────────────────────
BTC_HISTORY_SIZE = 300   # rolling ticks kept in memory

# ── Trading parameters ───────────────────────────────────────────────────────
BET_SIZE_USDC             = float(os.getenv("BET_SIZE_USDC", "2.00"))
DAILY_BUDGET_USDC         = float(os.getenv("DAILY_BUDGET_USDC", "0"))          # 0 = disabled
DAILY_PROFIT_TARGET_USDC  = float(os.getenv("DAILY_PROFIT_TARGET_USDC", "0"))   # 0 = disabled
AUTO_CLAIM_THRESHOLD = 4.00   # min winnings before auto-claim note
SIGNAL_COOLDOWN_S    = 1
MAX_BETS_PER_HOUR    = 10
HEARTBEAT_INTERVAL_S = 30     # POST /heartbeats to keep session alive
LIVE_TRADING         = os.getenv("LIVE_TRADING", "false").lower() == "true"

# Tambahkan di config (optional, untuk eksperimen)
LATE_RISK_WINDOW_S     = 90     # final 90 detik = zona berbahaya
LATE_GAP_RISK_PCT      = 0.08   # gap < 0.08% = high reversal risk

# ── Filter thresholds ─────────────────────────────────────────────────────────
RSI_PERIOD      = 14
RSI_LOW         = 30
RSI_HIGH        = 70
MA_SHORT        = 5
MA_LONG         = 20
MOMENTUM_TICKS  = 10
MIN_ODDS_EDGE   = 0.02   # one side must be > 0.52 to show clear market lean
MIN_ENTRY_ODDS  = float(os.getenv("MIN_ENTRY_ODDS", "0.55"))  # skip if chosen side is cheaper than this
MAX_BET_ODDS    = 0.79   # don't bet when implied odds exceed this — market too certain, payout too small
MAX_ENTRY_S     = 270    # normal entry window end; gold zone extends this to 270s

# ── MACD parameters (on 5-second bars) ────────────────────────────────────────
# 12 bars × 5s = 60s fast EMA, 26 bars × 5s = 130s slow EMA, 9 bars = 45s signal
MACD_FAST   = 12
MACD_SLOW   = 26
MACD_SIGNAL = 9

# ── Bollinger Bands (on 5-second bars) ────────────────────────────────────────
BB_PERIOD = 20   # 20 bars × 5s = 100s lookback
BB_STD    = 2.0

# ── CVD / VWAP ────────────────────────────────────────────────────────────────
CVD_DIVERGENCE_LOOKBACK = 8   # bars to detect price vs CVD divergence (40s window)

# ── Kelly position sizing ─────────────────────────────────────────────────────
# Fractional Kelly: bet = bankroll × (conf − implied) / (1 − implied) × KELLY_FRACTION
KELLY_FRACTION      = 0.25     # quarter-Kelly — proven safer than full Kelly
MIN_BET_USDC        = 1.00    # floor (never bet less than this)
MAX_BET_USDC        = 10.00   # ceiling (never bet more than this per trade)
PAPER_BANKROLL_USDC = 200.0   # simulated bankroll in paper mode for Kelly sizing

# ── Last-minute entry window (the ONLY entry window) ─────────────────────────
# The bot waits silently for 2 minutes then fires in the final ~3 minutes.
# Starting at 120s gives more opportunity to catch direction before Polymarket
# fully prices it in (by 180s odds are typically already at 0.99+).
GOLD_ZONE_START_S      = 240    # start looking at 210s elapsed (90s = 1.5 min remaining)
GOLD_ZONE_MIN_MOVE_PCT = 0.02   # BTC must be ≥ 0.02% from beat (~$17 at $85k)
GOLD_ZONE_MIN_CONF     = 0.80   # minimum calibrated confidence to execute a bet
GOLD_ZONE_MAX_ODDS     = 0.82   # leading side must still be ≤ this (not fully priced)
LAST_MIN_SECONDS_GUARD = 12     # stop accepting new bets with < 8s left (order latency)
MIN_SIGNAL_ALIGNMENT   = int(os.getenv("MIN_SIGNAL_ALIGNMENT", "4"))  # require at least 4/6 family-weighted alignment

# ── Beat-relative chop filter ─────────────────────────────────────────────────
# Skip windows where BTC is repeatedly crossing the beat price or spending an
# even split above/below it: this is the no-edge regime for a 5-minute binary.
CHOP_LOOKBACK_S        = int(os.getenv("CHOP_LOOKBACK_S", "90"))
CHOP_MAX_CROSSINGS     = int(os.getenv("CHOP_MAX_CROSSINGS", "2"))
CHOP_BALANCED_LOW      = float(os.getenv("CHOP_BALANCED_LOW", "0.35"))
CHOP_BALANCED_HIGH     = float(os.getenv("CHOP_BALANCED_HIGH", "0.65"))

# ── Decision maker / cancel thresholds ───────────────────────────────────────
# "Too sure" threshold: skip if the leading side is already this confident.
# Override via env to tune without restarting.
GATE_TOO_SURE_THRESHOLD    = float(os.getenv("GATE_TOO_SURE_THRESHOLD", str(GOLD_ZONE_MAX_ODDS)))

# Post-order cancel: cancel a live CLOB order when any of these fire.
CANCEL_ODDS_THRESHOLD      = float(os.getenv("CANCEL_ODDS_THRESHOLD",   "0.95"))  # market fully priced
CANCEL_MIN_CONF            = float(os.getenv("CANCEL_MIN_CONF",         "0.50"))  # confidence collapsed
CANCEL_MIN_SECONDS_GUARD   = int(os.getenv("CANCEL_MIN_SECONDS_GUARD",  "5"))     # too late to matter
CANCEL_ON_CONF_DROP        = os.getenv("CANCEL_ON_CONF_DROP", "true").lower() == "true"

# Price-reversal cancel: pull order if BTC crosses back through beat by this margin.
# e.g. 0.02% at $66k = ~$13 buffer before canceling a wrong-direction bet.
CANCEL_REVERSAL_BUFFER_PCT = float(os.getenv("CANCEL_REVERSAL_BUFFER_PCT", "0.02"))

# How often (seconds) the position monitor loop checks open live orders.
POSITION_MONITOR_INTERVAL_S = int(os.getenv("POSITION_MONITOR_INTERVAL_S", "10"))

# ── Loss streak protection ────────────────────────────────────────────────────
STREAK_HALT_COUNT = 5     # consecutive losses before halting bets
STREAK_PAUSE_MIN  = 30    # minutes to pause after a streak halt

# ── Brownian fair-value edge gate ─────────────────────────────────────────────
# Minimum positive EV required before the AI is even called.
# EV = fair_prob × (1 / market_odds) − 1
# Override via env to tune without restarting.
MINIMUM_EDGE_THRESHOLD = float(os.getenv("MINIMUM_EDGE_THRESHOLD", "0.05"))  # 5% min EV

# ── Telegram notifications ────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN       = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID         = os.getenv("TELEGRAM_CHAT_ID", "")
TELEGRAM_ENABLED         = bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)
TELEGRAM_STATUS_INTERVAL_S = int(os.getenv("TELEGRAM_STATUS_INTERVAL_S", "300"))  # every 5 min

# ── Bandar Push Detection (Anti Whale Push) ─────────────────────────────────
BANDAR_FINAL_SECONDS       = 45      # final 45 detik = zona paling berbahaya
BANDAR_ODDS_VEL_THRESHOLD  = 0.008   # > 8 mOdds/detik = tanda bandar masuk
BANDAR_CVD_ACCEL_THRESHOLD = 0.005   # CVD acceleration ekstrem
LATE_DYNAMIC_MIN_CONF      = 0.85    # min confidence di final <45 detik

# ── UI ────────────────────────────────────────────────────────────────────────
UI_REFRESH_S = 1.0

# ── Startup validation ────────────────────────────────────────────────────────
_BASE_REQUIRED = [
    ("POLY_FUNDER",        POLY_FUNDER),
    ("POLY_ADDRESS",       POLY_ADDRESS),
    ("POLY_API_KEY",       POLY_API_KEY),
    ("POLY_SECRET",        POLY_SECRET),
    ("POLY_PASSPHRASE",    POLY_PASSPHRASE),
    ("OPENROUTER_API_KEY", OPENROUTER_API_KEY),
]

def validate_config() -> list[str]:
    missing = [name for name, val in _BASE_REQUIRED if not val or val.startswith("your-")]
    if LIVE_TRADING and not POLY_ETH_PRIVATE_KEY:
        missing.append("POLY_ETH_PRIVATE_KEY")
    return missing


# ══════════════════════════════════════════════════════════════════════════════
# Source: logger.py
# ══════════════════════════════════════════════════════════════════════════════

"""Persistent file logging — every event, trade, signal, and price sample.

Files written to logs/ (rotated daily at UTC midnight):
  events_YYYY-MM-DD.log    — human-readable text, one line per event
  events_YYYY-MM-DD.jsonl  — same events as structured JSON (one object per line)
  trades_YYYY-MM-DD.jsonl  — trade open and close records
  signals_YYYY-MM-DD.jsonl — every AI signal (monitoring + gold zone)
  prices_YYYY-MM-DD.jsonl  — 5-second BTC price + volume snapshots
  paper_analytics_YYYY-MM-DD.jsonl — clean paper prediction/trade analytics
"""

from collections import defaultdict
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

_UTC = timezone.utc


class BotLogger:
    def __init__(self, log_dir: str | Path = "logs") -> None:
        self._dir = Path(log_dir)
        self._dir.mkdir(parents=True, exist_ok=True)
        self._day: str = ""
        self._ftext = None   # events_*.log  (text)
        self._fjsonl = None  # events_*.jsonl (structured)

    # ── Internals ─────────────────────────────────────────────────────────────

    def _rotate(self) -> None:
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        if today == self._day:
            return
        self._day = today
        if self._ftext:
            self._ftext.close()
        if self._fjsonl:
            self._fjsonl.close()
        self._ftext  = open(self._dir / f"events_{today}.log",   "a", encoding="utf-8")
        self._fjsonl = open(self._dir / f"events_{today}.jsonl", "a", encoding="utf-8")

    def _ts(self) -> str:
        return datetime.now(_UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    def _append(self, filename: str, record: dict) -> None:
        try:
            with open(self._dir / filename, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, default=str) + "\n")
        except Exception:
            pass

    # ── Public API ────────────────────────────────────────────────────────────

    def log_event(self, msg: str, extra: dict | None = None) -> None:
        """Write a text line + JSONL record for every bot event."""
        try:
            self._rotate()
            ts = self._ts()
            self._ftext.write(f"{ts}  {msg}\n")
            self._ftext.flush()
            record: dict = {"ts": ts, "msg": msg}
            if extra:
                record.update(extra)
            self._fjsonl.write(json.dumps(record, default=str) + "\n")
            self._fjsonl.flush()
        except Exception:
            pass

    def log_price(
        self,
        btc_price: float,
        buy_vol: float,
        sell_vol: float,
        cvd: float,
        up_odds: float | None = None,
        down_odds: float | None = None,
    ) -> None:
        """Record a 5-second BTC price + volume snapshot."""
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        self._append(f"prices_{today}.jsonl", {
            "ts":       self._ts(),
            "btc":      btc_price,
            "buy_vol":  round(buy_vol,  6),
            "sell_vol": round(sell_vol, 6),
            "cvd":      round(cvd,      6),
            "up_odds":  up_odds,
            "dn_odds":  down_odds,
        })

    def log_signal(
        self,
        signal,   # AISignal
        *,
        elapsed_s: float,
        up_odds: float | None,
        down_odds: float | None,
        btc_price: float | None,
        beat_price: float,
        is_gold_zone: bool,
        alignment: int = 0,
        cvd_divergence: str = "NONE",
        condition_id: str = "",
    ) -> None:
        """Record an AI signal (monitoring or gold-zone)."""
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        self._append(f"signals_{today}.jsonl", {
            "ts":            self._ts(),
            "signal":        signal.signal,
            "confidence":    signal.confidence,
            "raw_confidence": getattr(signal, "raw_confidence", signal.confidence),
            "reason":        signal.reason,
            "elapsed_s":     elapsed_s,
            "up_odds":       up_odds,
            "down_odds":     down_odds,
            "btc_price":     btc_price,
            "beat_price":    beat_price,
            "is_gold_zone":  is_gold_zone,
            "alignment":     alignment,
            "cvd_divergence": cvd_divergence,
            "condition_id":  condition_id,
        })

    def log_trade_open(self, position, window_question: str = "") -> None:
        """Record a newly placed trade."""
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        self._append(f"trades_{today}.jsonl", {
            "ts":               self._ts(),
            "event":            "open",
            "condition_id":     position.condition_id,
            "direction":        position.direction,
            "token_id":         position.token_id,
            "size":             position.size,
            "entry_price":      position.entry_price,
            "amount_usdc":      position.amount_usdc,
            "window_beat":      position.window_beat,
            "order_id":         position.order_id,
            "simulated":        position.simulated,
            "placed_at":        position.placed_at.isoformat(),
            "window_end_at":    position.window_end_at.isoformat() if position.window_end_at else "",
            "elapsed_at_bet":   position.elapsed_at_bet,
            "gap_pct_at_bet":   position.gap_pct_at_bet,
            "ai_confidence":    position.ai_confidence,
            "ai_raw_confidence": position.ai_raw_confidence,
            "signal_alignment": position.signal_alignment,
            "window_question":  window_question,
        })

    def log_trade_close(self, position) -> None:
        """Record a settled trade outcome."""
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        self._append(f"trades_{today}.jsonl", {
            "ts":           self._ts(),
            "event":        "close",
            "condition_id": position.condition_id,
            "direction":    position.direction,
            "status":       position.status,
            "amount_usdc":  position.amount_usdc,
            "entry_price":  position.entry_price,
            "pnl":          position.pnl,
            "window_beat":  position.window_beat,
            "order_id":     position.order_id,
            "simulated":    position.simulated,
            "placed_at":    position.placed_at.isoformat(),
            "window_end_at": position.window_end_at.isoformat() if position.window_end_at else "",
            "elapsed_at_bet": position.elapsed_at_bet,
            "gap_pct_at_bet": position.gap_pct_at_bet,
            "ai_confidence": position.ai_confidence,
            "ai_raw_confidence": position.ai_raw_confidence,
            "signal_alignment": position.signal_alignment,
        })

    def log_paper_prediction_state(self, record) -> None:
        """Persist the latest paper prediction snapshot for a window."""
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        self._append(f"paper_analytics_{today}.jsonl", {
            "ts":                  self._ts(),
            "event":               "prediction_state",
            "condition_id":        record.condition_id,
            "window_label":        record.window_label,
            "window_end_at":       record.window_end_at.isoformat() if record.window_end_at else "",
            "beat_price":          record.beat_price,
            "predicted_direction": record.predicted_direction,
            "decision_action":     record.decision_action,
            "simulated_order_id":  record.simulated_order_id,
            "confidence":          record.confidence,
            "raw_confidence":      record.raw_confidence,
            "alignment":           record.alignment,
            "paper_trade_won":     record.paper_trade_won,
            "last_updated_at":     record.last_updated_at.isoformat() if record.last_updated_at else "",
        })

    def log_paper_prediction_resolved(self, record) -> None:
        """Persist a resolved paper prediction outcome."""
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        self._append(f"paper_analytics_{today}.jsonl", {
            "ts":                  self._ts(),
            "event":               "prediction_resolved",
            "condition_id":        record.condition_id,
            "window_label":        record.window_label,
            "window_end_at":       record.window_end_at.isoformat() if record.window_end_at else "",
            "beat_price":          record.beat_price,
            "predicted_direction": record.predicted_direction,
            "decision_action":     record.decision_action,
            "simulated_order_id":  record.simulated_order_id,
            "actual_winner":       record.actual_winner,
            "prediction_correct":  record.prediction_correct,
            "paper_trade_won":     record.paper_trade_won,
            "confidence":          record.confidence,
            "raw_confidence":      record.raw_confidence,
            "alignment":           record.alignment,
            "resolved_at":         record.resolved_at.isoformat() if record.resolved_at else "",
        })

    def log_paper_trade_resolved(self, position, won: bool) -> None:
        """Persist a settled simulated trade for clean paper win-rate tracking."""
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        self._append(f"paper_analytics_{today}.jsonl", {
            "ts":                 self._ts(),
            "event":              "paper_trade_resolved",
            "condition_id":       position.condition_id,
            "window_end_at":      position.window_end_at.isoformat() if position.window_end_at else "",
            "simulated_order_id": position.order_id,
            "direction":          position.direction,
            "paper_trade_won":    won,
            "amount_usdc":        position.amount_usdc,
            "entry_price":        position.entry_price,
            "pnl":                position.pnl,
            "placed_at":          position.placed_at.isoformat(),
            "confidence":         position.ai_confidence,
            "raw_confidence":     position.ai_raw_confidence,
            "alignment":          position.signal_alignment,
            "resolved_at":        self._ts(),
        })

    def load_unsettled_trades(self, lookback_days: int = 2) -> list[dict]:
        """Return trade-open records that do not yet have a matching close record."""
        unresolved: dict[str, dict] = {}
        files = sorted(self._dir.glob("trades_*.jsonl"))
        if lookback_days > 0:
            cutoff = (datetime.now(_UTC) - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
            files = [f for f in files if f.stem.rsplit("_", 1)[-1] >= cutoff]

        for path in files:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                        except Exception:
                            continue

                        event = record.get("event")
                        if event not in ("open", "close"):
                            continue

                        key = self._trade_key(record)
                        if event == "open":
                            unresolved[key] = record
                        else:
                            unresolved.pop(key, None)
            except Exception:
                continue

        return list(unresolved.values())

    def find_price_near(self, when: datetime, max_diff_s: float = 90.0) -> float | None:
        """Return the logged BTC price closest to the requested timestamp."""
        try:
            target_ts = when.timestamp()
        except Exception:
            return None

        target_utc = datetime.fromtimestamp(target_ts, _UTC)
        days = {
            target_utc.strftime("%Y-%m-%d"),
            (target_utc - timedelta(days=1)).strftime("%Y-%m-%d"),
            (target_utc + timedelta(days=1)).strftime("%Y-%m-%d"),
        }

        best_diff = max_diff_s + 1.0
        best_price: float | None = None

        for day in sorted(days):
            path = self._dir / f"prices_{day}.jsonl"
            if not path.exists():
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                            raw_ts = record.get("ts")
                            btc = record.get("btc")
                            if raw_ts is None or btc is None:
                                continue
                            rec_ts = datetime.fromisoformat(raw_ts.replace("Z", "+00:00")).timestamp()
                        except Exception:
                            continue

                        diff = abs(rec_ts - target_ts)
                        if diff <= max_diff_s and diff < best_diff:
                            best_diff = diff
                            best_price = float(btc)
            except Exception:
                continue

        return best_price

    def load_recent_outcomes(self, limit: int = 50, lookback_days: int = 7) -> list[dict]:
        """Load recent settled trade outcomes for confidence calibration/history."""
        cutoff = (datetime.now(_UTC) - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
        trade_files = sorted(
            f for f in self._dir.glob("trades_*.jsonl")
            if f.stem.rsplit("_", 1)[-1] >= cutoff
        )
        signal_files = sorted(
            f for f in self._dir.glob("signals_*.jsonl")
            if f.stem.rsplit("_", 1)[-1] >= cutoff
        )

        signals_by_condition: dict[str, list[dict]] = defaultdict(list)
        for path in signal_files:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                        except Exception:
                            continue
                        cid = str(record.get("condition_id", ""))
                        if cid.startswith("0x"):
                            signals_by_condition[cid].append(record)
            except Exception:
                continue
        for records in signals_by_condition.values():
            records.sort(key=lambda rec: str(rec.get("ts", "")))

        opens: list[dict] = []
        closes: dict[str, dict] = {}
        for path in trade_files:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                        except Exception:
                            continue
                        cid = str(record.get("condition_id", ""))
                        if not cid.startswith("0x"):
                            continue
                        event = record.get("event")
                        key = self._trade_key(record)
                        if event == "open":
                            opens.append(record)
                        elif event == "close" and record.get("status") in ("won", "lost"):
                            closes[key] = record
            except Exception:
                continue

        opens.sort(key=lambda rec: str(rec.get("ts", "")))

        def _latest_signal_before(condition_id: str, ts: str) -> dict | None:
            latest = None
            for record in signals_by_condition.get(condition_id, []):
                if str(record.get("ts", "")) <= ts:
                    latest = record
                else:
                    break
            return latest

        outcomes: list[dict] = []
        for open_rec in opens:
            close_rec = closes.get(self._trade_key(open_rec))
            if close_rec is None:
                continue

            signal_rec = _latest_signal_before(
                str(open_rec.get("condition_id", "")),
                str(open_rec.get("ts", "")),
            )

            confidence = open_rec.get("ai_confidence")
            raw_conf = open_rec.get("ai_raw_confidence")
            alignment = open_rec.get("signal_alignment")
            elapsed = None
            if signal_rec:
                if confidence is None:
                    confidence = signal_rec.get("confidence")
                if raw_conf is None:
                    raw_conf = signal_rec.get("raw_confidence", signal_rec.get("confidence"))
                if alignment is None:
                    alignment = signal_rec.get("alignment")
                elapsed = signal_rec.get("elapsed_s")

            outcomes.append({
                "elapsed_at_bet": int(elapsed or 0),
                "gap_pct": float(open_rec.get("gap_pct_at_bet", 0.0) or 0.0),
                "direction": str(open_rec.get("direction", "NONE")),
                "won": close_rec.get("status") == "won",
                "odds": float(open_rec.get("entry_price", 0.0) or 0.0),
                "confidence": float(confidence or 0.0),
                "raw_confidence": float(raw_conf or confidence or 0.0),
                "alignment": int(alignment or 0),
            })

        return outcomes[-limit:]

    def load_paper_analytics(
        self,
        lookback_days: int = 30,
        *,
        today: str | None = None,
    ) -> tuple[dict[str, dict], dict[str, int]]:
        """Load pending paper predictions and aggregate clean paper stats."""
        if today is None:
            today = datetime.now(_UTC).strftime("%Y-%m-%d")

        cutoff = (datetime.now(_UTC) - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
        files = sorted(
            f for f in self._dir.glob("paper_analytics_*.jsonl")
            if f.stem.rsplit("_", 1)[-1] >= cutoff
        )

        pending_by_condition: dict[str, dict] = {}
        resolved_predictions: set[str] = set()
        resolved_paper_trades: set[str] = set()
        trade_results_by_order: dict[str, bool] = {}
        trade_results_by_condition: dict[str, bool] = {}
        counts = {
            "prediction_correct_total": 0,
            "prediction_incorrect_total": 0,
            "prediction_correct_today": 0,
            "prediction_incorrect_today": 0,
            "paper_trade_wins_total": 0,
            "paper_trade_losses_total": 0,
            "paper_trade_wins_today": 0,
            "paper_trade_losses_today": 0,
        }

        def _is_today(record: dict) -> bool:
            raw = str(record.get("resolved_at") or record.get("ts") or "")
            return raw[:10] == today

        for path in files:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            record = json.loads(line)
                        except Exception:
                            continue

                        event = str(record.get("event", ""))
                        condition_id = str(record.get("condition_id", "")).strip()

                        if event == "prediction_state":
                            if condition_id and condition_id not in resolved_predictions:
                                pending_by_condition[condition_id] = record
                            continue

                        if event == "prediction_resolved":
                            if not condition_id or condition_id in resolved_predictions:
                                continue
                            resolved_predictions.add(condition_id)
                            pending_by_condition.pop(condition_id, None)
                            if bool(record.get("prediction_correct")):
                                counts["prediction_correct_total"] += 1
                                if _is_today(record):
                                    counts["prediction_correct_today"] += 1
                            else:
                                counts["prediction_incorrect_total"] += 1
                                if _is_today(record):
                                    counts["prediction_incorrect_today"] += 1

                            paper_trade_won = record.get("paper_trade_won")
                            if isinstance(paper_trade_won, bool):
                                order_id = str(record.get("simulated_order_id", "")).strip()
                                if order_id:
                                    trade_results_by_order[order_id] = paper_trade_won
                                trade_results_by_condition[condition_id] = paper_trade_won
                            continue

                        if event != "paper_trade_resolved":
                            continue

                        order_id = str(record.get("simulated_order_id", "")).strip()
                        unique_key = order_id or f"{condition_id}:{record.get('placed_at', '')}"
                        won = bool(record.get("paper_trade_won"))
                        if unique_key and unique_key not in resolved_paper_trades:
                            resolved_paper_trades.add(unique_key)
                            if won:
                                counts["paper_trade_wins_total"] += 1
                                if _is_today(record):
                                    counts["paper_trade_wins_today"] += 1
                            else:
                                counts["paper_trade_losses_total"] += 1
                                if _is_today(record):
                                    counts["paper_trade_losses_today"] += 1

                        if order_id:
                            trade_results_by_order[order_id] = won
                        if condition_id:
                            trade_results_by_condition[condition_id] = won
            except Exception:
                continue

        for condition_id, record in pending_by_condition.items():
            order_id = str(record.get("simulated_order_id", "")).strip()
            if order_id and order_id in trade_results_by_order:
                record["paper_trade_won"] = trade_results_by_order[order_id]
            elif condition_id in trade_results_by_condition:
                record["paper_trade_won"] = trade_results_by_condition[condition_id]

        return pending_by_condition, counts

    @staticmethod
    def _trade_key(record: dict) -> str:
        order_id = str(record.get("order_id", "")).strip()
        if order_id:
            return order_id
        return ":".join([
            str(record.get("condition_id", "")),
            str(record.get("direction", "")),
            str(record.get("placed_at", "")),
        ])

    def close(self) -> None:
        if self._ftext:
            self._ftext.close()
        if self._fjsonl:
            self._fjsonl.close()


# ══════════════════════════════════════════════════════════════════════════════
# Source: indicators.py
# ══════════════════════════════════════════════════════════════════════════════

"""Technical indicator functions (pure — no I/O, no state).

Enhancement additions (ENHANCEMENT.md):
  - Odds velocity (replacing RSI in the alignment vote) — smart money signal
  - Brownian fair-value model — statistically valid P(UP) / P(DOWN) estimate
  - Kelly streak scaling — reduce bet size during loss streaks

Feeds the five display filters F1–F5 shown in the terminal UI.
All functions return FilterResult or IndicatorSnapshot; never raise.

Enhanced with:
  - MACD (12,26,9) on 5-second bars — momentum crossover confirmation
  - Bollinger Bands (20,2) — squeeze detection + overbought/oversold zones
  - CVD (Cumulative Volume Delta) divergence — smart money flow signal
  - VWAP — volume-weighted fair value benchmark
  - Fractional Kelly position sizing — optimal bet sizing
"""

import math
import time
from dataclasses import dataclass, field
from typing import Optional

import numpy as np



# ── Data structures ───────────────────────────────────────────────────────────

@dataclass
class FilterResult:
    name: str        # "F1" … "F5"
    label: str       # human-readable name shown in UI
    passed: bool
    value: str       # display value, e.g. "54.2"
    reason: str      # why it passed or failed


@dataclass
class IndicatorSnapshot:
    # Core indicators (pre-existing)
    rsi: float | None
    ma_short: float | None
    ma_long: float | None
    momentum_pct: float | None
    filters: list[FilterResult] = field(default_factory=list)
    all_pass: bool = False
    pass_count: int = 0
    direction_bias: str = "NONE"   # "UP" | "DOWN" | "NONE"
    timestamp: float = field(default_factory=time.time)

    # ── MACD (12,26,9 on 5-second bars) ──────────────────────────────────────
    macd_line: float | None = None      # MACD line = EMA(fast) − EMA(slow)
    macd_signal: float | None = None    # signal line = EMA(9) of MACD line
    macd_histogram: float | None = None # histogram = MACD line − signal line

    # ── Bollinger Bands (20,2 on 5-second bars) ───────────────────────────────
    bb_upper: float | None = None
    bb_lower: float | None = None
    bb_pct_b: float | None = None       # 0=at lower band, 0.5=mid, 1.0=at upper
    bb_bandwidth: float | None = None   # (upper−lower)/middle — squeeze proxy

    # ── CVD & VWAP ────────────────────────────────────────────────────────────
    vwap: float | None = None
    cvd_divergence: str = "NONE"        # "BULLISH" | "BEARISH" | "NONE"

    # ── Odds velocity (replaces RSI in the alignment vote) ───────────────────
    # Rate of change of UP odds over the last 30 seconds.
    odds_vel_direction: str = "NONE"   # "UP" | "DOWN" | "NONE"
    odds_vel_value: float = 0.0        # odds/second for the UP token
    odds_vel_accel: float = 0.0        # positive = accelerating toward UP

    # ── Multi-strategy signal summary ─────────────────────────────────────────
    # Family-weighted alignment score:
    # trend family (0-2) + market family (0-2) + flow family (0-2)
    signal_alignment: int = 0           # 0-6 family-weighted alignment
    trend_dir: str = "NONE"
    trend_strength: int = 0
    market_dir: str = "NONE"
    market_strength: int = 0
    flow_dir: str = "NONE"
    flow_strength: int = 0
    ma_dir: str = "NONE"
    momentum_dir: str = "NONE"
    macd_dir: str = "NONE"
    odds_edge_dir: str = "NONE"
    odds_vel_vote_dir: str = "NONE"
    up_score: int = 0
    down_score: int = 0


# ── Core computation helpers ──────────────────────────────────────────────────

def compute_rsi(prices: list[float], period: int = RSI_PERIOD) -> float | None:
    """Wilder's RSI using numpy. Returns None if insufficient data."""
    if len(prices) < period + 1:
        return None
    arr = np.array(prices[-(period + 1):], dtype=float)
    deltas = np.diff(arr)
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)
    avg_gain = float(np.mean(gains))
    avg_loss = float(np.mean(losses))
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))


def compute_ma(prices: list[float], period: int) -> float | None:
    """Simple moving average. Returns None if insufficient data."""
    if len(prices) < period:
        return None
    return float(np.mean(prices[-period:]))


def compute_momentum(prices: list[float], ticks: int = MOMENTUM_TICKS) -> float | None:
    """Rate of change %: (current - N_ago) / N_ago * 100."""
    if len(prices) < ticks + 1:
        return None
    old = prices[-(ticks + 1)]
    cur = prices[-1]
    if old == 0:
        return None
    return (cur - old) / old * 100.0


# ── MACD ──────────────────────────────────────────────────────────────────────

def _compute_ema_series(prices: list[float], period: int) -> list[float]:
    """Full iterative EMA series starting from the first complete SMA window."""
    if len(prices) < period:
        return []
    k = 2.0 / (period + 1)
    seed = float(np.mean(prices[:period]))
    emas = [seed]
    for p in prices[period:]:
        emas.append(p * k + emas[-1] * (1.0 - k))
    return emas


def compute_macd(
    prices: list[float],
    fast: int = MACD_FAST,
    slow: int = MACD_SLOW,
    signal_period: int = MACD_SIGNAL,
) -> tuple[float | None, float | None, float | None]:
    """Return (macd_line, signal_line, histogram) or (None, None, None).

    On 5-second bars: fast=12→60s, slow=26→130s, signal=9→45s.
    Needs at least slow+signal bars = 35 bars = 175s of history.
    """
    if len(prices) < slow + signal_period:
        return None, None, None

    ema_fast = _compute_ema_series(prices, fast)
    ema_slow = _compute_ema_series(prices, slow)

    # Align both series to the same time index
    # ema_fast[i] starts at prices[fast-1], ema_slow[i] starts at prices[slow-1]
    offset = slow - fast   # how far ema_fast is ahead of ema_slow
    macd_series = [ef - es for ef, es in zip(ema_fast[offset:], ema_slow)]

    if len(macd_series) < signal_period:
        return None, None, None

    sig_series = _compute_ema_series(macd_series, signal_period)
    if not sig_series:
        return None, None, None

    macd_line = macd_series[-1]
    signal_line = sig_series[-1]
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


# ── Bollinger Bands ───────────────────────────────────────────────────────────

def compute_bollinger_bands(
    prices: list[float],
    period: int = BB_PERIOD,
    std_mult: float = BB_STD,
) -> tuple[float, float, float, float, float] | None:
    """Return (upper, middle, lower, bandwidth, pct_b) or None.

    pct_b   : 0.0 = price at lower band, 1.0 = price at upper band.
    bandwidth: (upper−lower)/middle — narrow → squeeze, wide → expansion.
    """
    if len(prices) < period:
        return None
    subset = prices[-period:]
    middle = float(np.mean(subset))
    std = float(np.std(subset, ddof=0))
    upper = middle + std_mult * std
    lower = middle - std_mult * std
    span = upper - lower
    bandwidth = span / middle if middle != 0 else 0.0
    pct_b = (prices[-1] - lower) / span if span > 0 else 0.5
    return upper, middle, lower, bandwidth, pct_b


# ── CVD divergence ────────────────────────────────────────────────────────────

def compute_cvd_divergence(
    cvd_series: list[float],
    prices: list[float],
    lookback: int = CVD_DIVERGENCE_LOOKBACK,
) -> str:
    """Detect price vs CVD divergence over the last `lookback` 5-second bars.

    Bullish divergence: price falling but CVD rising → hidden buy pressure → UP
    Bearish divergence: price rising but CVD falling → hidden sell pressure → DOWN

    CVD is the running Cumulative Volume Delta (buy_vol − sell_vol).
    This is the core strategy from share_2.md — CVD strategy had highest P&L
    because it detects when smart money disagrees with the visible price.
    """
    if len(cvd_series) < lookback + 1 or len(prices) < lookback + 1:
        return "NONE"

    price_change = prices[-1] - prices[-lookback]
    cvd_change = cvd_series[-1] - cvd_series[-lookback]

    # Require meaningful moves (at least $2 price move and 0.05 BTC net volume)
    if abs(price_change) < 2.0:
        return "NONE"
    if abs(cvd_change) < 0.05:
        return "NONE"

    if price_change < 0 and cvd_change > 0:
        return "BULLISH"   # price fell but buyers dominated → likely bounce
    if price_change > 0 and cvd_change < 0:
        return "BEARISH"   # price rose but sellers dominated → likely reversal
    return "NONE"


# ── VWAP ──────────────────────────────────────────────────────────────────────

def compute_vwap(
    prices: list[float],
    buy_vols: list[float],
    sell_vols: list[float],
) -> float | None:
    """Volume-Weighted Average Price using 5-second aggregated data.

    Uses all available aligned data. Returns None if no volume history.
    VWAP above current price = bearish context; below = bullish context.
    """
    if not prices or not buy_vols or not sell_vols:
        return None
    n = min(len(prices), len(buy_vols), len(sell_vols))
    if n < 3:
        return None
    total_vol = 0.0
    total_pv = 0.0
    for i in range(n):
        vol = buy_vols[i] + sell_vols[i]
        total_pv += prices[i] * vol
        total_vol += vol
    if total_vol == 0:
        return None
    return total_pv / total_vol


# ── Kelly position sizing ─────────────────────────────────────────────────────

def compute_kelly_size(
    confidence: float,
    implied_odds: float,
    bankroll: float,
    kelly_fraction: float = KELLY_FRACTION,
    min_bet: float = MIN_BET_USDC,
    max_bet: float = MAX_BET_USDC,
    consecutive_losses: int = 0,
) -> float:
    """Fractional Kelly position size in USDC.

    In prediction markets, buying a share at price `c` and winning $1:
    Full Kelly fraction = (confidence − implied_odds) / (1 − implied_odds)
    We use quarter-Kelly (fraction=0.25) for safety.

    Streak scaling: reduce size automatically during a losing streak to protect
    bankroll while the strategy is underperforming.
      3 consecutive losses → ½ size
      4+ consecutive losses → ¼ size

    Reference: share_1.md — f = bankroll × kelly_quarter, kelly_quarter = ((p·b − q)/b)/4
    """
    if implied_odds <= 0 or implied_odds >= 1 or bankroll <= 0:
        return min_bet
    if confidence <= implied_odds:
        return min_bet   # no edge
    full_kelly = (confidence - implied_odds) / (1.0 - implied_odds)
    bet = bankroll * full_kelly * kelly_fraction

    # Reduce size during a losing streak
    if consecutive_losses >= 4:
        bet *= 0.25
    elif consecutive_losses == 3:
        bet *= 0.50

    return max(min_bet, min(max_bet, round(bet, 2)))


# ── Individual filter checks ──────────────────────────────────────────────────

def check_f1_rsi(prices: list[float]) -> tuple[FilterResult, str]:
    """Data-readiness gate: PASSES whenever RSI can be computed (enough price history).
    Direction vote: UP if RSI < 45 (oversold), DOWN if RSI > 55 (overbought).

    Rationale: On 5-second bars (75s of data), RSI extremes (>70/<30) are too
    rare to use as a gate — they fire only ~20% of the time.  RSI is the
    LOWEST-weight indicator; it contributes a direction lean, not a block.
    """
    rsi = compute_rsi(prices)
    if rsi is None:
        return FilterResult("F1", "RSI(14)", False, "n/a", "insufficient data"), "NONE"
    val = f"{rsi:.1f}"
    if rsi < 45:
        return FilterResult("F1", "RSI(14)", True, val, f"RSI={rsi:.1f} oversold → UP"), "UP"
    if rsi > 55:
        return FilterResult("F1", "RSI(14)", True, val, f"RSI={rsi:.1f} overbought → DOWN"), "DOWN"
    return FilterResult("F1", "RSI(14)", True, val, f"RSI={rsi:.1f} neutral"), "NONE"


def check_f2_ma_crossover(prices: list[float]) -> tuple[FilterResult, str]:
    """Returns (FilterResult, direction_bias).
    Passes when there is a clear MA directional signal (not flat/equal).
    """
    ma5  = compute_ma(prices, MA_SHORT)
    ma20 = compute_ma(prices, MA_LONG)
    if ma5 is None or ma20 is None:
        return FilterResult("F2", f"MA{MA_SHORT}/MA{MA_LONG}", False, "n/a", "insufficient data"), "NONE"
    diff_pct = abs(ma5 - ma20) / ma20 * 100 if ma20 != 0 else 0
    passed = diff_pct > 0.01
    if ma5 > ma20:
        direction = "UP"
        val = f"MA{MA_SHORT}>MA{MA_LONG} BULL"
        reason = f"Bullish (+{diff_pct:.3f}%)"
    else:
        direction = "DOWN"
        val = f"MA{MA_SHORT}<MA{MA_LONG} BEAR"
        reason = f"Bearish (-{diff_pct:.3f}%)"
    if not passed:
        reason = "MAs too close (flat)"
    return FilterResult("F2", f"MA{MA_SHORT}/MA{MA_LONG}", passed, val, reason), direction


def check_f3_momentum(prices: list[float]) -> tuple[FilterResult, str]:
    """Passes when |momentum| > 0.01% — captures any meaningful drift."""
    mom = compute_momentum(prices)
    if mom is None:
        return FilterResult("F3", f"Mom({MOMENTUM_TICKS})", False, "n/a", "insufficient data"), "NONE"
    val = f"{mom:+.3f}%"
    passed = abs(mom) > 0.01
    direction = "UP" if mom > 0 else "DOWN"
    reason = f"momentum={mom:+.3f}% {'OK' if passed else 'flat'}"
    return FilterResult("F3", f"Mom({MOMENTUM_TICKS})", passed, val, reason), direction


def check_f4_odds_edge(up_odds: float, down_odds: float) -> tuple[FilterResult, str]:
    """Passes when the market has a clear but not extreme directional lean.

    FAIL — too extreme (>MAX_BET_ODDS): market already priced certainty.
    FAIL — near 50/50: no clear market lean.
    PASS — one side in range: clear lean with usable payout.
    """
    if up_odds >= MAX_BET_ODDS or down_odds >= MAX_BET_ODDS:
        extreme_side = "UP" if up_odds >= MAX_BET_ODDS else "DOWN"
        extreme_val  = up_odds if up_odds >= MAX_BET_ODDS else down_odds
        val = f"UP={up_odds:.3f} DN={down_odds:.3f}"
        return FilterResult(
            "F4", "Odds Edge", False, val,
            f"{extreme_side}={extreme_val:.0%} too extreme (>{MAX_BET_ODDS:.0%})"
        ), "NONE"

    threshold = 0.5 + MIN_ODDS_EDGE
    if up_odds >= threshold:
        direction = "UP"
        passed = True
        val = f"UP={up_odds:.3f}"
        reason = f"Market favors UP ({up_odds:.3f} > {threshold:.3f})"
    elif down_odds >= threshold:
        direction = "DOWN"
        passed = True
        val = f"DOWN={down_odds:.3f}"
        reason = f"Market favors DOWN ({down_odds:.3f} > {threshold:.3f})"
    else:
        direction = "NONE"
        passed = False
        val = f"UP={up_odds:.3f} DN={down_odds:.3f}"
        reason = "near 50/50, no market edge"
    return FilterResult("F4", "Odds Edge", passed, val, reason), direction


def check_f5_window_timing(elapsed_s: int) -> FilterResult:
    """Passes only during first MAX_ENTRY_S seconds of the window."""
    passed = 0 <= elapsed_s < MAX_ENTRY_S
    val = f"{elapsed_s}s"
    reason = f"elapsed {elapsed_s}s {'< ' + str(MAX_ENTRY_S) if passed else '≥ ' + str(MAX_ENTRY_S) + ' (late)'}"
    return FilterResult("F5", "Entry Timing", passed, val, reason)


# ── Odds velocity ─────────────────────────────────────────────────────────────

def compute_odds_velocity(odds_history: list, lookback_s: float = 30.0) -> dict:
    """Rate of change of UP odds over the last lookback_s seconds.

    odds_history entries: (timestamp: float, up_odds: float, down_odds: float)
    Returns: {"vel": float, "direction": str, "acceleration": float}

    Positive vel = odds moving toward UP (smart money entering BUY_UP).
    Negative vel = odds moving toward DOWN.
    Threshold 0.0005 odds/s ≈ 0.5 mOdds/s — noise floor at typical tick rate.
    """
    if len(odds_history) < 4:
        return {"vel": 0.0, "direction": "NONE", "acceleration": 0.0}

    now = odds_history[-1][0]
    cutoff = now - lookback_s

    baseline = None
    for entry in odds_history:
        if entry[0] >= cutoff:
            baseline = entry
            break

    if baseline is None:
        return {"vel": 0.0, "direction": "NONE", "acceleration": 0.0}

    current_up  = odds_history[-1][1]
    baseline_up = baseline[1]
    elapsed     = max(odds_history[-1][0] - baseline[0], 1.0)

    vel = (current_up - baseline_up) / elapsed
    direction = "UP" if vel > 0.0005 else ("DOWN" if vel < -0.0005 else "NONE")

    # Acceleration: first-half vs second-half velocity (momentum building/stalling)
    mid_idx          = len(odds_history) // 2
    mid_up           = odds_history[mid_idx][1]
    mid_ts           = odds_history[mid_idx][0]
    first_half_vel   = (mid_up - baseline_up) / max(mid_ts - baseline[0], 1.0)
    second_half_vel  = (current_up - mid_up)  / max(now - mid_ts, 1.0)
    accel            = second_half_vel - first_half_vel

    return {"vel": vel, "direction": direction, "acceleration": accel}


# ── Brownian fair-value model ──────────────────────────────────────────────────

def compute_fair_probability(
    btc_price: float,
    beat_price: float,
    seconds_remaining: float,
    price_history_5s: list,
) -> dict:
    """Model BTC/USD as Brownian motion to derive a statistically valid P(UP).

    Formula: P(UP) = Φ( gap / (σ × √T) )
      gap = btc_price − beat_price  (positive = currently winning for UP)
      σ   = realized per-second volatility (dollars/second)
      T   = seconds remaining
      Φ   = standard normal CDF

    Returns: {"fair_up", "fair_down", "vol_per_s", "z_score"}

    Why this matters: if fair P(UP) = 0.60 but market odds are 0.75, the market
    has already priced it in — the EV of betting UP is NEGATIVE.  Without this
    model you cannot know whether a bet is +EV before placing it.
    """
    _empty = {"fair_up": 0.5, "fair_down": 0.5, "vol_per_s": 0.0, "z_score": 0.0}
    if seconds_remaining < 5 or len(price_history_5s) < 10 or beat_price <= 0:
        return _empty

    changes = [
        price_history_5s[i] - price_history_5s[i - 1]
        for i in range(1, len(price_history_5s))
    ]
    if not changes:
        return _empty

    variance_5s = sum(c ** 2 for c in changes) / len(changes)
    std_5s      = variance_5s ** 0.5
    vol_per_s   = std_5s / (5 ** 0.5)        # convert 5-second std to per-second
    vol_per_s   = max(vol_per_s, 0.50)       # floor: BTC moves at least $0.50/s on average

    gap     = btc_price - beat_price
    z_score = gap / (vol_per_s * (seconds_remaining ** 0.5))

    def _norm_cdf(z: float) -> float:
        return 0.5 * (1.0 + math.erf(z / math.sqrt(2)))

    fair_up   = _norm_cdf(z_score)
    fair_down = 1.0 - fair_up

    return {
        "fair_up":   fair_up,
        "fair_down": fair_down,
        "vol_per_s": vol_per_s,
        "z_score":   z_score,
    }


def compute_edge(fair_prob: float, market_odds: float) -> float:
    """Expected value per dollar wagered (positive = bet is +EV).

    EV = fair_prob × payout_ratio − 1 = fair_prob / market_odds − 1

    Example: fair_prob=0.70, market_odds=0.72 → EV = 0.70/0.72 − 1 = −2.8% (−EV!)
    Example: fair_prob=0.70, market_odds=0.55 → EV = 0.70/0.55 − 1 = +27% (+EV)
    """
    if market_odds <= 0.0 or market_odds >= 1.0:
        return 0.0
    return fair_prob * (1.0 / market_odds) - 1.0


def compute_beat_chop_metrics(
    prices: list[float],
    beat_price: float,
    lookback_bars: int | None = None,
) -> dict:
    """Describe how noisy BTC has been around the beat price."""
    if beat_price <= 0 or not prices:
        return {"crossings": 0, "above_ratio": 0.0, "below_ratio": 0.0}

    if lookback_bars is None:
        lookback_bars = max(4, CHOP_LOOKBACK_S // 5)

    window = prices[-lookback_bars:]
    states = [1 if price >= beat_price else -1 for price in window]
    above_count = sum(1 for state in states if state > 0)
    below_count = len(states) - above_count

    crossings = 0
    for prev, cur in zip(states, states[1:]):
        if prev != cur:
            crossings += 1

    total = len(states)
    return {
        "crossings": crossings,
        "above_ratio": above_count / total if total else 0.0,
        "below_ratio": below_count / total if total else 0.0,
    }


# ── Main entry point ──────────────────────────────────────────────────────────

def run_all_filters(
    prices: list[float],
    up_odds: float,
    down_odds: float,
    elapsed_s: int,
    buy_vols: list[float] | None = None,
    sell_vols: list[float] | None = None,
    cvd_series: list[float] | None = None,
    odds_history: list | None = None,
) -> IndicatorSnapshot:
    """Run F1–F5 and return a full snapshot with enhanced indicators.

    Family-weighted alignment (0-6 total):
      Trend family  (0-2): MA crossover + momentum + MACD
      Market family (0-2): odds edge + odds velocity
      Flow family   (0-2): CVD divergence

    This caps correlated signals so MA/momentum/MACD do not masquerade as three
    independent confirmations in a 5-minute binary market.
    """
    f1, dir_f1 = check_f1_rsi(prices)  # kept for display, NOT in vote
    f2, dir_f2 = check_f2_ma_crossover(prices)
    f3, dir_f3 = check_f3_momentum(prices)
    f4, dir_f4 = check_f4_odds_edge(up_odds, down_odds)
    f5 = check_f5_window_timing(elapsed_s)

    filters = [f1, f2, f3, f4, f5]
    pass_count = sum(1 for f in filters if f.passed)
    all_pass = pass_count == 5

    # ── MACD direction vote ────────────────────────────────────────────────────
    macd_line, macd_signal_val, macd_histogram = compute_macd(prices)
    dir_macd = "NONE"
    if macd_histogram is not None:
        dir_macd = "UP" if macd_histogram > 0 else "DOWN"

    # ── CVD divergence vote (contrarian smart-money signal) ───────────────────
    cvd_div = "NONE"
    if cvd_series and len(cvd_series) >= CVD_DIVERGENCE_LOOKBACK + 1:
        cvd_div = compute_cvd_divergence(list(cvd_series), prices)
    dir_cvd = {"BULLISH": "UP", "BEARISH": "DOWN"}.get(cvd_div, "NONE")

    # ── Odds velocity vote (replaces RSI) — where smart money is moving ───────
    odds_vel_result = compute_odds_velocity(odds_history or [])
    dir_odds_vel    = odds_vel_result["direction"]

    # ── Family-weighted consensus (caps correlated evidence) ──────────────────
    trend_votes = [dir_f2, dir_f3, dir_macd]
    trend_up = trend_votes.count("UP")
    trend_down = trend_votes.count("DOWN")
    if max(trend_up, trend_down) >= 2:
        trend_dir = "UP" if trend_up > trend_down else "DOWN"
        trend_strength = 2 if max(trend_up, trend_down) == 3 else 1
    else:
        trend_dir = "NONE"
        trend_strength = 0

    market_votes = [dir_f4, dir_odds_vel]
    market_active = [direction for direction in market_votes if direction != "NONE"]
    if len(market_active) == 2 and market_active[0] == market_active[1]:
        market_dir = market_active[0]
        market_strength = 2
    elif len(market_active) == 1:
        market_dir = market_active[0]
        market_strength = 1
    else:
        market_dir = "NONE"
        market_strength = 0

    flow_dir = dir_cvd
    flow_strength = 2 if flow_dir != "NONE" else 0

    up_score = 0
    down_score = 0
    for direction, strength in (
        (trend_dir, trend_strength),
        (market_dir, market_strength),
        (flow_dir, flow_strength),
    ):
        if direction == "UP":
            up_score += strength
        elif direction == "DOWN":
            down_score += strength

    if up_score > down_score:
        consensus = "UP"
        signal_alignment = up_score
    elif down_score > up_score:
        consensus = "DOWN"
        signal_alignment = down_score
    else:
        consensus = "NONE"
        signal_alignment = 0

    # ── Bollinger Bands ───────────────────────────────────────────────────────
    bb_result = compute_bollinger_bands(prices)
    bb_upper = bb_lower = bb_pct_b = bb_bandwidth = None
    if bb_result:
        bb_upper, _, bb_lower, bb_bandwidth, bb_pct_b = bb_result

    # ── VWAP ──────────────────────────────────────────────────────────────────
    vwap = None
    if buy_vols and sell_vols:
        vwap = compute_vwap(prices, buy_vols, sell_vols)

    return IndicatorSnapshot(
        rsi=compute_rsi(prices),
        ma_short=compute_ma(prices, MA_SHORT),
        ma_long=compute_ma(prices, MA_LONG),
        momentum_pct=compute_momentum(prices),
        filters=filters,
        all_pass=all_pass,
        pass_count=pass_count,
        direction_bias=consensus,
        timestamp=time.time(),
        # MACD
        macd_line=macd_line,
        macd_signal=macd_signal_val,
        macd_histogram=macd_histogram,
        # Bollinger Bands
        bb_upper=bb_upper,
        bb_lower=bb_lower,
        bb_pct_b=bb_pct_b,
        bb_bandwidth=bb_bandwidth,
        # CVD & VWAP
        vwap=vwap,
        cvd_divergence=cvd_div,
        # Odds velocity (replaces RSI in votes)
        odds_vel_direction=odds_vel_result["direction"],
        odds_vel_value=odds_vel_result["vel"],
        odds_vel_accel=odds_vel_result["acceleration"],
        # Multi-strategy alignment
        signal_alignment=signal_alignment,
        trend_dir=trend_dir,
        trend_strength=trend_strength,
        market_dir=market_dir,
        market_strength=market_strength,
        flow_dir=flow_dir,
        flow_strength=flow_strength,
        ma_dir=dir_f2,
        momentum_dir=dir_f3,
        macd_dir=dir_macd,
        odds_edge_dir=dir_f4,
        odds_vel_vote_dir=dir_odds_vel,
        up_score=up_score,
        down_score=down_score,
    )


# ══════════════════════════════════════════════════════════════════════════════
# Source: ai_agent.py
# ══════════════════════════════════════════════════════════════════════════════

"""OpenRouter AI agent — Claude Sonnet 4.6 as final trade decision maker.

Always returns an AISignal. On any error / timeout, returns SKIP so the
trading loop is never blocked waiting for the AI.

Enhanced with:
  - MACD histogram signal in context
  - Bollinger Band %B position (mean reversion context)
  - CVD divergence (smart money flow — highest P&L strategy from share_2.md)
  - VWAP relationship (RSI+VWAP strategy)
  - Gold Zone awareness (last 2-min high-conviction entry)
  - Signal alignment count (how many indicators agree)
"""

import inspect
import json
import re
import statistics
import time
from dataclasses import dataclass, field

import certifi
import httpx



@dataclass
class AISignal:
    signal: str         # "BUY_UP" | "BUY_DOWN" | "SKIP"
    confidence: float   # 0.0 – 1.0
    reason: str
    latency_ms: int = 0
    timestamp: float = field(default_factory=time.time)
    dip_label: str = "UNKNOWN"  # TEMPORARY_DIP | SUSTAINED_MOVE | MIXED | SUSTAINED_ABOVE
    raw_confidence: float = 0.0


_SYSTEM_PROMPT = """\
You are an independent expert trading analyst for Polymarket Bitcoin prediction markets.

MARKET STRUCTURE:
- Each window is 300 seconds (5 minutes). At close: is BTC ABOVE or BELOW the beat price?
- Binary outcome — full win or full loss. No partial results.
- BUY_UP   = BTC will close ABOVE beat price
- BUY_DOWN = BTC will close BELOW beat price
- SKIP     = insufficient edge, conflicting signals, or EV-negative

STEP 1 — READ THE CURRENT WINNER FIRST (before any other analysis):
  The user message provides a "CURRENT WINNER" field. This tells you which side is
  CURRENTLY winning based on BTC position vs beat price RIGHT NOW.
  - CURRENT WINNER: DOWN means BTC is below beat — DOWN wins if nothing changes.
  - CURRENT WINNER: UP means BTC is above beat — UP wins if nothing changes.
  This is your prior. Technical indicators show momentum, NOT who is winning.
  Do not confuse bullish momentum with "UP is currently winning".

STEP 2 — RECOVERY FEASIBILITY (read DIP ANALYSIS block first):
  The user message provides "Recovery feasibility" AND a "DIP ANALYSIS" block.
  Feasibility is a SNAPSHOT calculation — velocity at a single moment. It can be
  misleading during brief fluctuations. Always read DIP ANALYSIS first.

  Feasibility ratings (apply ONLY after considering DIP ANALYSIS):
  IMPOSSIBLE-SNAPSHOT (vel opposes): Velocity opposes recovery at this instant.
    If DIP ANALYSIS = TEMPORARY_DIP, treat this as BORDERLINE — the dip may reverse.
    If DIP ANALYSIS = SUSTAINED_MOVE, treat this as a genuine IMPOSSIBLE.
  IMPOSSIBLE (>3x ratio): Required rate is 3x+ current speed. Treat as HARD
    unless DIP ANALYSIS confirms SUSTAINED_MOVE (≥80% of samples on losing side).
  HARD (2–3x): Recovery requires a sustained reversal. Lean CURRENT WINNER,
    but downgrade to BORDERLINE if DIP ANALYSIS = TEMPORARY_DIP.
  BORDERLINE (1–2x): Recovery is possible. Use alignment and other signals.
  FEASIBLE (<1x): Either side could win. Full signal analysis.

DECISION CRITERIA (apply in this priority order):

1. GAP vs TIME vs VELOCITY + DIP ANALYSIS — most predictive (★★★★★):
   Read feasibility AND DIP ANALYSIS together. Neither alone is sufficient.

   a) DIP ANALYSIS = SUSTAINED_MOVE (≥80% of samples on losing side):
      IMPOSSIBLE/HARD feasibility → bet the CURRENT WINNER strongly.
      This is the ONLY case where feasibility alone justifies high confidence.

   b) DIP ANALYSIS = TEMPORARY_DIP (majority of samples were on WINNING side):
      Downgrade IMPOSSIBLE or HARD to BORDERLINE. Do NOT bet against the indicator
      consensus because velocity momentarily opposes recovery — dips reverse fast.
      If alignment ≤ 2/5 AND TEMPORARY_DIP → SKIP or confidence ≤ 0.63.

   c) DIP ANALYSIS = MIXED: use alignment + gap math. Confidence cap 0.75 unless
      alignment ≥ 4 AND feasibility is HARD+.

   A "small" dollar gap can be HARD if velocity opposes, but only when
   DIP ANALYSIS = SUSTAINED_MOVE confirms the move is genuine.

2. MARKET ODDS as ground truth (★★★★★):
   UP=35% means the crowd prices a 35% chance.
   To bet against the crowd you need a specific reason.
   Required: YOUR confidence > implied probability for positive EV.

3. MACD histogram — momentum confirmation (★★★★):
   Histogram > 0 = bullish momentum. Histogram < 0 = bearish momentum.
   On 5-second bars: fast=60s EMA, slow=130s EMA, signal=45s EMA.
   WARNING: bullish MACD only matters if recovery is FEASIBLE or BORDERLINE.

4. CVD divergence — smart money flow (★★★★):
   BULLISH: price fell but buy volume dominated → hidden accumulation → lean UP.
   BEARISH: price rose but sell volume dominated → distribution → lean DOWN.

4b. ODDS VELOCITY — smart money in motion (★★★★):
   Odds rapidly rising toward UP = informed participants entering BUY_UP.
   Velocity > 2 mOdds/s opposing your other signals is a serious warning.
   Acceleration > 0 = momentum building; < 0 = stalling.

4c. STATISTICAL FAIR VALUE — Brownian motion model (★★★★):
   The model computes a mathematical P(UP) from BTC's actual realized volatility.
   EV = fair_prob / market_odds − 1. Positive = +EV bet. Negative = −EV.
   If both EV values are negative, SKIP — you have no mathematical edge.
   Use the EV values to calibrate your confidence (higher EV → higher confidence).

4d. BEAT CHOP / STRIKE WHIPSAW (★★★):
   Frequent beat crossings or a near-even above/below split reduce certainty.
   Treat this as a confidence penalty, not an automatic skip, unless the setup is
   weak everywhere else.

4e. MARKET WARNINGS (advisory, not a hard rule):
   The user message may include code-side warnings such as weak crowd lean, low
   edge, or low alignment. Use them as caution context. Strong gap math + EV can
   still justify a bet if your probability estimate genuinely clears market odds.

5. VWAP position — institutional fair value (★★★):
   Price above VWAP + high RSI → overbought → lean DOWN (mean reversion).
   Price below VWAP + low RSI → oversold → lean UP (mean reversion).

6. Bollinger Band %B — mean reversion context (★★★):
   %B > 0.90 → overbought, fade the move. %B < 0.10 → oversold.
   NOTE: Do NOT bet mean reversion in the gold zone (elapsed ≥ 120s).

7. MA5 vs MA20 alignment — trend direction (★★★)

8. Momentum (50-second ROC) — short-term drift (★★)

9. RSI alone — LOWEST weight (5-second bars = only ~70s of data) (★):
   RSI=100 means recent bars were all up — it does NOT mean BTC is above beat.
   RSI extreme alone is never a reason to override gap+time math.

GOLD ZONE GUIDANCE (when is_gold_zone=true, elapsed ≥ 120s):
  BTC has had 2+ minutes to establish direction. Gap math is now primary.
  Market odds often lag BTC price moves by 15-30 seconds → mispricing opportunity.
  However: only bet if you have GENUINE EDGE. Do not force a bet every window.
  SKIP is correct when recovery is borderline and signals conflict.
  Do NOT bet mean reversion — momentum is near expiry.
  DIP CAUTION: In the gold zone, a TEMPORARY_DIP with IMPOSSIBLE feasibility can
  still reverse — especially if the dip is small (<$20) and indicator consensus is
  opposite to the dip direction. Do not make high-confidence contrarian bets based
  solely on a snapshot velocity during a brief dip.

TEMPORARY DIP vs SUSTAINED MOVE — how to read DIP ANALYSIS:
  TEMPORARY_DIP  (≥60% of samples on WINNING side, currently dipped):
    BTC spent most of the recent window on the winning side. The current losing
    position is a transient fluctuation. Any IMPOSSIBLE/HARD feasibility must be
    treated as BORDERLINE. High-confidence contrarian bets (> 0.68) are NOT
    justified. Require alignment ≥ 3 to bet contrarian at all. If alignment ≤ 2,
    output SKIP.

  SUSTAINED_MOVE  (≥80% of samples on LOSING side):
    BTC has been consistently on the losing side. Feasibility ratings are reliable.
    Full confidence scaling applies.

  MIXED  (between the two thresholds):
    Neither a clear dip nor a sustained move. Use alignment and gap math together.
    Confidence cap: 0.75 unless alignment ≥ 4 AND feasibility is HARD+.

  IMPORTANT: "IMPOSSIBLE — velocity opposes recovery" during a TEMPORARY_DIP does
  NOT mean recovery is impossible. Velocity at a single snapshot inside a 5-minute
  binary market can reverse multiple times. The dip analysis tells you the full
  picture; the velocity snapshot tells you only the current direction.

SIGNAL ALIGNMENT (context, not a hard rule):
  alignment is a FAMILY-WEIGHTED score out of 6, not six independent indicators.
  alignment=5/6 — very strong cross-family consensus.
  alignment=4/6 — solid consensus across at least two families.
  alignment=3/6 — moderate, confirm with gap math first.
  alignment=2/6 — weak, only signal if gap math is clear.
  alignment≤1/6 — conflicting, prefer SKIP.

CONFIDENCE CALIBRATION — CRITICAL:
  Your confidence is YOUR TRUE probability estimate, not a display of conviction.
  Never output 1.0 (100%) — binary markets always have uncertainty.
  Never inflate confidence just because you decided to bet.
  Realistic ranges:
    0.60–0.68 → slight edge, borderline bet
    0.68–0.78 → moderate edge, reasonable bet
    0.78–0.87 → strong edge, good bet
    0.87–0.92 → very strong edge (gap math is overwhelming), rare
  If you find yourself above 0.92, reconsider — you are likely overconfident.

IMPORTANT: Output ONLY the JSON object below — no explanation, no preamble, no markdown:
{"signal": "BUY_UP|BUY_DOWN|SKIP", "confidence": 0.0, "reason": "one sentence"}
"""


class AIAgent:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=OPENROUTER_BASE,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://github.com/polymarket-bot",
                "X-Title": "BTC Polymarket Bot",
                "Content-Type": "application/json",
            },
            timeout=AI_TIMEOUT_S,
            verify=certifi.where(),
        )

    async def get_signal(
        self,
        btc_price: float,
        beat_price: float,
        up_odds: float,
        down_odds: float,
        rsi: float | None,
        ma_short: float | None,
        ma_long: float | None,
        momentum_pct: float | None,
        seconds_remaining: int,
        elapsed_s: int,
        recent_prices: list[float],
        # Enhanced indicators
        macd_histogram: float | None = None,
        bb_pct_b: float | None = None,
        vwap: float | None = None,
        cvd_divergence: str = "NONE",
        signal_alignment: int = 0,
        is_gold_zone: bool = False,
        # Enhancement additions
        odds_vel: dict | None = None,
        beat_crossings: int = 0,
        beat_above_ratio: float = 0.0,
        beat_below_ratio: float = 0.0,
        market_warnings: list[str] | None = None,
        fair_prob: dict | None = None,
        window_history: list | None = None,
        consecutive_losses: int = 0,
    ) -> AISignal:
        t0 = time.time()
        try:
            user_msg, computed_dip_label = self._build_user_message_with_dip(
                btc_price=btc_price,
                beat_price=beat_price,
                up_odds=up_odds,
                down_odds=down_odds,
                rsi=rsi,
                ma_short=ma_short,
                ma_long=ma_long,
                momentum_pct=momentum_pct,
                seconds_remaining=seconds_remaining,
                elapsed_s=elapsed_s,
                recent_prices=recent_prices,
                macd_histogram=macd_histogram,
                bb_pct_b=bb_pct_b,
                vwap=vwap,
                cvd_divergence=cvd_divergence,
                signal_alignment=signal_alignment,
                is_gold_zone=is_gold_zone,
                odds_vel=odds_vel,
                beat_crossings=beat_crossings,
                beat_above_ratio=beat_above_ratio,
                beat_below_ratio=beat_below_ratio,
                market_warnings=market_warnings,
                fair_prob=fair_prob,
                window_history=window_history,
                consecutive_losses=consecutive_losses,
            )
            payload = {
                "model": OPENROUTER_MODEL,
                "messages": [
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {"role": "user",   "content": user_msg},
                ],
                "temperature": 0.2,
                "max_tokens": 300,
            }
            resp = await self._client.post("/chat/completions", json=payload)
            resp.raise_for_status()
            json_body = resp.json()
            if inspect.isawaitable(json_body):
                json_body = await json_body
            content = json_body["choices"][0]["message"]["content"]
            latency = int((time.time() - t0) * 1000)
            signal = self._parse_response(content)
            signal.latency_ms = latency
            signal.dip_label  = computed_dip_label
            return signal

        except httpx.TimeoutException:
            return AISignal("SKIP", 0.0, "AI timeout", int((time.time() - t0) * 1000))
        except Exception as exc:
            return AISignal("SKIP", 0.0, f"AI error: {exc!s:.60}", int((time.time() - t0) * 1000))

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _build_user_message(self, **kw) -> str:
        msg, _ = self._build_user_message_with_dip(**kw)
        return msg

    def _build_user_message_with_dip(self, **kw) -> tuple[str, str]:
        btc  = kw["btc_price"]
        beat = kw["beat_price"]
        gap  = btc - beat
        gap_s = f"+${gap:,.2f}" if gap >= 0 else f"-${abs(gap):,.2f}"
        pos   = "ABOVE" if gap >= 0 else "BELOW"

        # PATCH: Hitung gap_pct di sini supaya bisa dipakai di late risk
        gap_pct = abs(gap) / beat * 100 if beat > 0 else 0.0

        elapsed_s   = kw["elapsed_s"]
        remaining_s = kw["seconds_remaining"]
        total_s     = elapsed_s + remaining_s
        pct_done    = elapsed_s / total_s * 100 if total_s > 0 else 0

        # Price velocity and volatility from recent 5s-sampled prices
        recent = kw["recent_prices"][-20:] if kw["recent_prices"] else []
        if len(recent) >= 2:
            vel = (recent[-1] - recent[0]) / (len(recent) * 5)
            vel_s = f"{vel:+.2f} $/s ({'rising' if vel > 0 else 'falling'})"
        else:
            vel = 0.0
            vel_s = "n/a"

        vol_s = "n/a"
        if len(recent) >= 3:
            vol = statistics.stdev(recent)
            vol_s = f"±${vol:.2f} (1σ of last {len(recent)*5}s)"

        # ── Dip / sustained-move analysis ────────────────────────────────────
        DIP_WINDOW = 20
        dip_prices = recent[-DIP_WINDOW:] if len(recent) >= DIP_WINDOW else recent
        n_dip       = len(dip_prices)
        above_count = sum(1 for p in dip_prices if p >= beat)
        below_count = n_dip - above_count
        above_pct   = above_count / n_dip * 100 if n_dip > 0 else 0.0
        below_pct   = below_count / n_dip * 100 if n_dip > 0 else 0.0

        dip_prices_below = [p for p in dip_prices if p < beat]
        dip_depth = beat - min(dip_prices_below) if dip_prices_below else 0.0

        if n_dip < 4:
            dip_label = "INSUFFICIENT_DATA"
        elif above_pct >= 60.0 and btc < beat:
            dip_label = "TEMPORARY_DIP"
        elif below_pct >= 80.0:
            dip_label = "SUSTAINED_MOVE"
        elif above_pct >= 80.0:
            dip_label = "SUSTAINED_ABOVE"
        else:
            dip_label = "MIXED"

        # Smoothed velocity
        if n_dip >= 6:
            half             = n_dip // 2
            first_half_avg   = statistics.mean(dip_prices[:half])
            second_half_avg  = statistics.mean(dip_prices[half:])
            smoothed_vel     = (second_half_avg - first_half_avg) / (half * 5)
            sv_dir           = "rising" if smoothed_vel > 0 else "falling"
            smoothed_vel_s   = f"{smoothed_vel:+.2f} $/s ({sv_dir}) [half-avg smoothed]"
        else:
            smoothed_vel   = vel
            smoothed_vel_s = vel_s + " [raw — too few samples]"

        current_winner = "DOWN" if gap < 0 else ("UP" if gap > 0 else "TIED")
        losing_side    = "UP" if gap < 0 else ("DOWN" if gap > 0 else "TIED")

        if gap < 0 and remaining_s > 0:
            required_rate = abs(gap) / remaining_s
            recovery_s = f"{losing_side} needs +${abs(gap):,.2f} in {remaining_s}s = +${required_rate:.2f}/s required"
        elif gap > 0 and remaining_s > 0:
            required_rate = gap / remaining_s
            recovery_s = f"{losing_side} needs -${gap:,.2f} in {remaining_s}s = -${required_rate:.2f}/s required"
        else:
            required_rate = 0.0
            recovery_s = "BTC exactly at beat"

        # Feasibility
        abs_smoothed = abs(smoothed_vel) if smoothed_vel != 0 else 0.001
        if gap == 0 or required_rate == 0:
            feasibility_s = "TIED — no recovery needed"
        else:
            ratio = required_rate / abs_smoothed
            vel_opposes = (gap < 0 and smoothed_vel <= 0) or (gap > 0 and smoothed_vel >= 0)
            if vel_opposes:
                if dip_label == "TEMPORARY_DIP":
                    feasibility_s = f"IMPOSSIBLE-SNAPSHOT — smoothed velocity opposes recovery at this instant, BUT DIP ANALYSIS={dip_label} ({above_count}/{n_dip} samples above beat). Treat as BORDERLINE per DIP rules."
                else:
                    feasibility_s = f"IMPOSSIBLE — smoothed velocity moving AWAY from recovery (DIP={dip_label}, {above_count}/{n_dip} above beat)"
            elif ratio > 3.0:
                feasibility_s = f"IMPOSSIBLE ({ratio:.1f}x) — required rate {ratio:.1f}x faster than smoothed velocity"
            elif ratio > 2.0:
                feasibility_s = f"HARD ({ratio:.1f}x) — required rate {ratio:.1f}x faster than smoothed velocity"
            elif ratio > 1.0:
                feasibility_s = f"BORDERLINE ({ratio:.1f}x) — recovery possible if velocity sustains"
            else:
                feasibility_s = f"FEASIBLE ({ratio:.1f}x) — current velocity can cover the gap"

        # PATCH: Late window risk (final 90 detik)
        late_risk_s = ""
        if remaining_s < 90:
            if len(dip_prices) >= 6:
                roc_30s = (dip_prices[-1] - dip_prices[-6]) / dip_prices[-6] * 100
            else:
                roc_30s = 0.0

            bandar_note = " (FINAL 45s = BANDAR PUSH ZONE)" if remaining_s < 45 else ""
            late_risk_s = f"""
                === LATE WINDOW RISK (FINAL {remaining_s}s{bandar_note} — HIGH REVERSAL ZONE) ===
                Gap to beat     : {gap_pct:.3f}%
                Last 30s ROC    : {roc_30s:+.2f}%
                Odds velocity   : {getattr(kw.get('odds_vel', {}), 'vel', 0)*1000:+.1f} mOdds/s
                CVD acceleration: {getattr(kw.get('odds_vel', {}), 'acceleration', 0):+.3f}

                Ini zona klasik whale/bandar push. Hanya boleh BUY jika:
                - Alignment ≥5/6 + velocity sustain sangat kuat
                - Bukan TEMPORARY_DIP
                - Confidence minimal 0.85 (0.90 jika <45 detik)
                Kalau ada tanda odds velocity > 8 mOdds/s atau CVD accel ekstrem → SKIP. Jangan pernah force bet di final 60 detik.
            """

        # MA alignment
        ma5  = kw["ma_short"]
        ma20 = kw["ma_long"]
        if ma5 is not None and ma20 is not None:
            diff = ma5 - ma20
            diff_pct = diff / ma20 * 100 if ma20 != 0 else 0
            ma_dir = "BULLISH (MA5>MA20)" if diff > 0 else "BEARISH (MA5<MA20)"
            ma_s = f"{ma_dir}  diff={diff:+.2f} ({diff_pct:+.3f}%)"
        else:
            ma_s = "n/a"

        rsi_s = f"{kw['rsi']:.1f}" if kw["rsi"] is not None else "n/a"
        mom_s = f"{kw['momentum_pct']:+.3f}%" if kw["momentum_pct"] is not None else "n/a"

        # MACD, BB, VWAP, CVD, dll (tetap sama seperti kode lama kamu)
        macd_h = kw.get("macd_histogram")
        macd_s = f"{macd_h:+.4f}  [{'BULLISH' if macd_h > 0 else 'BEARISH'} momentum]" if macd_h is not None else "n/a (warming up)"

        bb_pct = kw.get("bb_pct_b")
        bb_s = f"{bb_pct:.3f}  [NEAR UPPER BAND (overbought → fade DOWN)]" if bb_pct is not None and bb_pct > 0.90 else \
               f"{bb_pct:.3f}  [NEAR LOWER BAND (oversold → fade UP)]" if bb_pct is not None and bb_pct < 0.10 else \
               f"{bb_pct:.3f}  [MID BAND (neutral)]" if bb_pct is not None else "n/a"

        vwap = kw.get("vwap")
        vwap_s = f"${vwap:,.2f}  (price {'ABOVE' if (btc - vwap) >= 0 else 'BELOW'} VWAP)" if vwap is not None and beat > 0 else "n/a (building)"

        cvd_div = kw.get("cvd_divergence", "NONE")
        cvd_s = "BULLISH divergence ← price fell but buy vol dominated (hidden accumulation → lean UP)" if cvd_div == "BULLISH" else \
                "BEARISH divergence ← price rose but sell vol dominated (distribution → lean DOWN)" if cvd_div == "BEARISH" else \
                "NONE (price and volume flow aligned)"

        alignment = kw.get("signal_alignment", 0)
        align_s = f"{alignment}/6 ★★★ STRONG FAMILY CONSENSUS" if alignment >= 5 else \
                  f"{alignment}/6 ★★ Good family consensus" if alignment >= 4 else \
                  f"{alignment}/6 Moderate family agreement" if alignment >= 3 else \
                  f"{alignment}/6 Weak / conflicting family signals"

        is_gold = kw.get("is_gold_zone", False)
        gold_s = "YES — market odds may lag BTC's actual position. Gap math is primary." if is_gold else "No"

        annotated = [f"{p:,.0f}{'▲' if p >= beat else '▼'}" for p in recent]
        price_series = ", ".join(annotated)

        up_implied   = kw["up_odds"] * 100
        down_implied = kw["down_odds"] * 100

        ov = kw.get("odds_vel") or {}
        odds_vel_s = f"{ov.get('direction','NONE')} at {ov.get('vel',0)*1000:+.2f} mOdds/s  accel={ov.get('acceleration',0)*1000:+.2f} mOdds/s²" if ov.get("direction") != "NONE" else "NONE (odds stable — no smart-money flow detected)"

        fp = kw.get("fair_prob") or {}
        fair_s = f"Model P(UP): {fp.get('fair_up',0.5):.1%} ..." if fp else "n/a (insufficient price history to compute)"

        hist = kw.get("window_history") or []
        history_s = self._format_window_history(hist)

        beat_crossings = int(kw.get("beat_crossings", 0))
        beat_above_ratio = float(kw.get("beat_above_ratio", 0.0))
        beat_below_ratio = float(kw.get("beat_below_ratio", 0.0))
        chop_note = "High chop around beat — reduce confidence unless EV/gap is strong." if beat_crossings >= 4 or 0.45 <= beat_above_ratio <= 0.55 else \
                    "Moderate chop around beat — weigh with gap math." if beat_crossings >= 2 or 0.35 <= beat_above_ratio <= 0.65 else \
                    "Directional regime — not especially choppy."

        market_warnings = kw.get("market_warnings") or []
        warnings_s = "\n".join(f"- {item}" for item in market_warnings[:6]) if market_warnings else "- None"

        # Gabungkan semua ke dalam msg
        msg = f"""\
=== CURRENT WINNER (read this first) ===
CURRENT WINNER: {current_winner} ← BTC is {pos} beat by {gap_s}  [{losing_side} needs to recover]
Recovery need : {recovery_s}
Recovery feas.: {feasibility_s}

=== WINDOW STATUS ===
Progress      : {elapsed_s}s elapsed / {total_s}s total  ({pct_done:.0f}% done)
Time Remaining: {remaining_s}s
Gold Zone     : {gold_s}
BTC Price     : ${btc:,.2f}
Beat Price    : ${beat:,.2f}

=== PRICE DYNAMICS ===
Velocity (raw): {vel_s}
Volatility    : {vol_s}

=== DIP ANALYSIS (last {n_dip*5}s = {n_dip} samples — read BEFORE interpreting feasibility) ===
Above beat    : {above_count}/{n_dip} samples ({above_pct:.0f}%)  ▲
Below beat    : {below_count}/{n_dip} samples ({below_pct:.0f}%)  ▼
Dip depth     : ${dip_depth:,.2f} below beat
Smoothed vel  : {smoothed_vel_s}
Classification: {dip_label}

{late_risk_s}

=== TECHNICAL INDICATORS (momentum only — does NOT indicate who is winning) ===
RSI(14)       : {rsi_s}
MA alignment  : {ma_s}
Momentum(10)  : {mom_s}
MACD histo    : {macd_s}
BB %B         : {bb_s}
VWAP          : {vwap_s}

=== FLOW / SMART MONEY ===
CVD divergence: {cvd_s}
Signal align  : {align_s}

=== ODDS VELOCITY (smart money in motion) ===
{odds_vel_s}

=== BEAT CHOP / STRIKE NOISE ===
Beat crossings: {beat_crossings}
Above/below   : {beat_above_ratio:.0%} / {beat_below_ratio:.0%}
Interpretation: {chop_note}

=== STATISTICAL FAIR VALUE (Brownian model) ===
{fair_s}

=== MARKET WARNINGS (advisory, not auto-skip) ===
{warnings_s}

=== RECENT PERFORMANCE (last {len(hist)} settled bets) ===
{history_s}

=== MARKET ODDS & EV THRESHOLDS ===
UP  implied   : {up_implied:.1f}%  
DOWN implied  : {down_implied:.1f}%  

=== RECENT PRICES last {len(recent)*5}s  (▲=above beat  ▼=below beat) ===
{price_series}

Output your JSON decision now. No explanation — only the JSON object."""

        return msg, dip_label

    @staticmethod
    def _format_window_history(history: list) -> str:
        if not history:
            return "No recent history (first windows of session)."
        lines = []
        for w in history[-5:]:
            outcome = "WON " if w.get("won") else "LOST"
            lines.append(
                f"  [{outcome}] {w.get('direction','?'):4s}  "
                f"elapsed={w.get('elapsed_at_bet',0)}s  "
                f"gap={w.get('gap_pct', 0):+.2f}%  "
                f"odds={w.get('odds', 0):.2f}  "
                f"conf={w.get('confidence', 0):.2f}"
            )
        total = len(history)
        wins  = sum(1 for w in history if w.get("won"))
        wr    = wins / total * 100 if total else 0.0
        lines.append(f"\n  Win rate: {wr:.0f}% over last {total} settled bets")
        if wr < 40 and total >= 3:
            lines.append("  ⚠ Win rate < 40% — prefer SKIP for borderline signals; increase skepticism.")
        elif wr > 65 and total >= 3:
            lines.append("  ✓ Win rate > 65% — strategy is working in current regime.")
        return "\n".join(lines)

    def _parse_response(self, content: str) -> AISignal:
        # Strip markdown code fences if present
        content = re.sub(r"```(?:json)?|```", "", content).strip()

        # Find JSON object
        match = re.search(r'\{.*?\}', content, re.DOTALL)
        if not match:
            return AISignal("SKIP", 0.0, f"parse error: {content[:60]}")

        try:
            data = json.loads(match.group())
        except json.JSONDecodeError:
            return AISignal("SKIP", 0.0, f"invalid JSON: {content[:60]}")

        raw_signal = str(data.get("signal", "SKIP")).upper().strip()
        if raw_signal not in ("BUY_UP", "BUY_DOWN", "SKIP"):
            raw_signal = "SKIP"

        confidence = float(data.get("confidence", 0.0))
        confidence = max(0.0, min(0.92, confidence))   # cap at 92% — never truly certain

        reason = str(data.get("reason", ""))[:120]

        return AISignal(
            signal=raw_signal,
            confidence=confidence,
            reason=reason,
            raw_confidence=confidence,
        )


# ══════════════════════════════════════════════════════════════════════════════
# Source: decision_maker.py
# ══════════════════════════════════════════════════════════════════════════════

"""Pure decision layer for the trading bot.

DecisionMaker is synchronous and stateless — no I/O, no async — so it is
trivially unit-testable independent of market state or network calls.

Flow (called from bot._trading_loop):

  1. bot builds DecisionContext with current market/indicator data (no ai_signal yet)
  2. bot calls DecisionMaker.pre_ai_check(ctx)
       → returns TradeDecision(SKIP) if a market gate fails  (saves AI API call)
       → returns None if all pre-AI gates pass (proceed to AI)
  3. bot fetches AISignal (async), sets ctx.ai_signal
  4. bot calls DecisionMaker.evaluate(ctx)
       → returns TradeDecision(BUY | SKIP) with gate label + reason

Post-order cancel (called from bot._position_monitor_loop):
  5. bot calls DecisionMaker.should_cancel(pos, up_odds, down_odds, seconds_remaining)
       → returns (True, reason) when order should be pulled, (False, "") otherwise
"""

import time
from dataclasses import dataclass, field
from typing import Any




# ── Gate name constants ───────────────────────────────────────────────────────

GATE_NO_MOVE              = "GATE_NO_MOVE"              # BTC hasn't moved enough from beat price
GATE_LOW_ENTRY_ODDS       = "GATE_LOW_ENTRY_ODDS"       # chosen side is too close to a coin flip
GATE_CHOPPY_BEAT          = "GATE_CHOPPY_BEAT"          # BTC is whipsawing around the beat price
GATE_TOO_SURE             = "GATE_TOO_SURE"             # market already fully priced — no edge
GATE_50_50                = "GATE_50_50"                # no crowd lean, pure coin-flip
GATE_ODDS_VEL_CONFLICT    = "GATE_ODDS_VEL_CONFLICT"    # odds racing against indicator consensus
GATE_NO_EDGE              = "GATE_NO_EDGE"              # Brownian model: bet is −EV or < min EV
GATE_DIR_CONFLICT         = "GATE_DIR_CONFLICT"         # AI direction conflicts with indicator consensus
GATE_AI_HOLD              = "GATE_AI_HOLD"              # AI returned SKIP
GATE_LOW_ALIGNMENT        = "GATE_LOW_ALIGNMENT"        # indicator families do not agree enough
GATE_LOW_CONF             = "GATE_LOW_CONF"             # AI confidence below threshold
GATE_OK                   = "OK"                        # all gates passed → BUY


# ── Data classes ─────────────────────────────────────────────────────────────

@dataclass
class DecisionContext:
    """All inputs the DecisionMaker needs to evaluate a potential trade.

    Build this before the AI call (ai_signal=None), pass to pre_ai_check().
    After the AI call, set ai_signal and pass to evaluate().
    """
    win: Any                        # WindowInfo
    elapsed_s: int
    seconds_remaining: int
    btc_price: float
    up_odds: float
    down_odds: float
    snap: Any                       # IndicatorSnapshot
    ai_signal: Any | None = None    # AISignal — set after pre_ai_check passes

    # Dip analysis from the AI user message builder (passed through so the
    # DecisionMaker can apply the same logic independently of the AI call)
    dip_label: str = "UNKNOWN"          # TEMPORARY_DIP | SUSTAINED_MOVE | MIXED | ...
    signal_alignment: int = 0           # family-weighted alignment score (0-6)

    # Brownian fair-value result — pre-computed in bot._trading_loop and passed
    # here so pre_ai_check can gate without recomputing.
    # {"fair_up", "fair_down", "edge_up", "edge_down", "vol_per_s", "z_score"}
    fair_prob: dict = field(default_factory=dict)

    # Configurable thresholds — default to values from config.py
    max_odds_threshold: float = field(default_factory=lambda: GATE_TOO_SURE_THRESHOLD)
    min_conf_threshold: float = field(default_factory=lambda: GOLD_ZONE_MIN_CONF)
    min_move_pct: float       = field(default_factory=lambda: GOLD_ZONE_MIN_MOVE_PCT)
    min_odds_edge: float      = field(default_factory=lambda: MIN_ODDS_EDGE)
    min_entry_odds: float     = field(default_factory=lambda: MIN_ENTRY_ODDS)
    min_signal_alignment: int = field(default_factory=lambda: MIN_SIGNAL_ALIGNMENT)
    chop_max_crossings: int   = field(default_factory=lambda: CHOP_MAX_CROSSINGS)
    chop_balanced_low: float  = field(default_factory=lambda: CHOP_BALANCED_LOW)
    chop_balanced_high: float = field(default_factory=lambda: CHOP_BALANCED_HIGH)
    beat_crossings: int = 0
    beat_above_ratio: float = 0.0
    beat_below_ratio: float = 0.0
    # Minimum alignment required when AI direction conflicts with a temporary-dip bias
    dir_conflict_min_conf: float = 0.78  # contrarian bets need stronger conviction


@dataclass
class TradeDecision:
    """Output of DecisionMaker.evaluate() or pre_ai_check()."""
    action: str        # "BUY" | "SKIP"
    direction: str     # "UP" | "DOWN" | "NONE"
    confidence: float  # 0.0–1.0 (from AI signal when available, else 0)
    reason: str        # human-readable explanation
    gate: str          # which gate fired, e.g. GATE_TOO_SURE or OK
    timestamp: float = field(default_factory=time.time)


# ── Decision maker ────────────────────────────────────────────────────────────

class DecisionMaker:
    """Stateless evaluator — create one instance and reuse across calls."""

    def _check_late_reversal_risk(self, ctx: DecisionContext) -> TradeDecision | None:
        """PATCH: Proteksi khusus final 90 detik — gap kecil = HIGH reversal risk"""
        if ctx.seconds_remaining > LATE_RISK_WINDOW_S:
            return None

        gap_pct = abs(ctx.btc_price - ctx.win.beat_price) / ctx.win.beat_price * 100
        if gap_pct >= LATE_GAP_RISK_PCT:
            return None

        if ctx.signal_alignment < 5:
            return TradeDecision(
                action="SKIP",
                direction=ctx.snap.direction_bias or "NONE",
                confidence=0.0,
                reason=f"LATE_PROXIMITY_RISK: gap={gap_pct:.3f}% < {LATE_GAP_RISK_PCT:.2f}% di final {ctx.seconds_remaining}s (align={ctx.signal_alignment}/6)",
                gate="GATE_LATE_PROXIMITY_RISK",
            )
        return None
    
    def _check_bandar_push(self, ctx: DecisionContext) -> TradeDecision | None:
        """Gate khusus mendeteksi tanda bandar/whale push di final 45 detik"""
        if ctx.seconds_remaining > BANDAR_FINAL_SECONDS:
            return None

        snap = ctx.snap
        if snap is None:
            return None

        # Odds velocity ekstrem
        if abs(snap.odds_vel_value) > BANDAR_ODDS_VEL_THRESHOLD:
            return TradeDecision(
                action="SKIP",
                direction=ctx.snap.direction_bias or "NONE",
                confidence=0.0,
                reason=f"BANDAR_PUSH_DETECTED: odds velocity {snap.odds_vel_value*1000:+.1f} mOdds/s (terlalu ekstrem di final {ctx.seconds_remaining}s)",
                gate="GATE_BANDAR_PUSH",
            )

        # CVD acceleration ekstrem
        if abs(snap.odds_vel_accel) > BANDAR_CVD_ACCEL_THRESHOLD:
            return TradeDecision(
                action="SKIP",
                direction=ctx.snap.direction_bias or "NONE",
                confidence=0.0,
                reason=f"BANDAR_PUSH_DETECTED: CVD acceleration {snap.odds_vel_accel*1000:+.1f} mOdds/s² (smart money ekstrem di final {ctx.seconds_remaining}s)",
                gate="GATE_BANDAR_PUSH",
            )

        return None

    # ── Pre-AI market gates ───────────────────────────────────────────────────

    def pre_ai_check(self, ctx: DecisionContext) -> TradeDecision | None:
        """Run market gates that don't require an AI signal.

        Returns:
            TradeDecision(SKIP)  if a gate fires (caller should not query AI)
            None                 if all gates pass (caller should query AI then call evaluate())
        """
        win = ctx.win
        if win is None or win.beat_price <= 0:
            return TradeDecision(
                action="SKIP", direction="NONE", confidence=0.0,
                reason="no active window or beat price not set",
                gate=GATE_NO_MOVE,
            )

        gap_pct = abs(ctx.btc_price - win.beat_price) / win.beat_price * 100

        # Hard data-quality floor only. The legacy 0.02% threshold was too strict
        # and frequently prevented the AI from seeing otherwise tradable gold-zone
        # setups. Keep a micro-gap guard so we do not query AI on literal tie noise.
        hard_min_move = max(ctx.min_move_pct * 0.25, 0.005)
        if gap_pct < hard_min_move:
            return TradeDecision(
                action="SKIP", direction="NONE", confidence=0.0,
                reason=f"gap={gap_pct:.3f}% < {hard_min_move:.3f}% — micro-move, no edge yet",
                gate=GATE_NO_MOVE,
            )

        is_btc_above = ctx.btc_price > win.beat_price
        leading_odds = ctx.up_odds if is_btc_above else ctx.down_odds
        direction    = "UP" if is_btc_above else "DOWN"

        # Only skip the choppiest strike action before AI. Moderate chop is still
        # passed through to the AI as context instead of being hard-blocked.
        hard_crossings = max(ctx.chop_max_crossings + 2, 4)
        if ctx.beat_crossings > hard_crossings:
            return TradeDecision(
                action="SKIP", direction=direction, confidence=0.0,
                reason=(
                    f"BTC crossed beat {ctx.beat_crossings} times in the recent lookback "
                    f"(hard max {hard_crossings})"
                ),
                gate=GATE_CHOPPY_BEAT,
            )
        
        late_risk = self._check_late_reversal_risk(ctx)
        if late_risk is not None:
            return late_risk
        
        bandar_push = self._check_bandar_push(ctx)
        if bandar_push is not None:
            return bandar_push

        balanced_low = max(ctx.chop_balanced_low, 0.45)
        balanced_high = min(ctx.chop_balanced_high, 0.55)
        if balanced_low <= ctx.beat_above_ratio <= balanced_high:
            return TradeDecision(
                action="SKIP", direction=direction, confidence=0.0,
                reason=(
                    f"BTC split above/below beat {ctx.beat_above_ratio:.0%}/"
                    f"{ctx.beat_below_ratio:.0%} — too balanced around the strike"
                ),
                gate=GATE_CHOPPY_BEAT,
            )

        # GATE_TOO_SURE: market already fully priced — payout too small
        if leading_odds > ctx.max_odds_threshold:
            return TradeDecision(
                action="SKIP", direction=direction, confidence=0.0,
                reason=(
                    f"odds {leading_odds:.3f} > {ctx.max_odds_threshold:.3f} — "
                    f"market too sure, edge gone"
                ),
                gate=GATE_TOO_SURE,
            )

        # Keep only clearly negative-EV windows out of the AI path. Small or modest
        # positive EV is advisory now; the AI receives the full fair-value section.
        if ctx.fair_prob:
            best_edge = max(
                ctx.fair_prob.get("edge_up",   0.0),
                ctx.fair_prob.get("edge_down", 0.0),
            )
            if best_edge < -0.02:
                return TradeDecision(
                    action="SKIP", direction=direction, confidence=0.0,
                    reason=(
                        f"Best EV {best_edge:+.1%} is clearly negative — "
                        f"model P(UP)={ctx.fair_prob.get('fair_up', 0.5):.1%} "
                        f"vs market {ctx.up_odds:.1%}"
                    ),
                    gate=GATE_NO_EDGE,
                )

        return None   # all market gates passed — proceed to AI

    def ai_context_warnings(self, ctx: DecisionContext) -> list[str]:
        """Return advisory warnings for the AI without blocking the query."""
        warnings: list[str] = []
        win = ctx.win
        if win is None or win.beat_price <= 0:
            return warnings

        gap_pct = abs(ctx.btc_price - win.beat_price) / win.beat_price * 100
        if gap_pct < ctx.min_move_pct:
            warnings.append(
                f"Gap is only {gap_pct:.3f}% from beat; legacy no-move floor is {ctx.min_move_pct:.3f}%."
            )

        strongest_odds = max(ctx.up_odds, ctx.down_odds)
        if strongest_odds < ctx.min_entry_odds:
            warnings.append(
                f"Strongest market odds are only {strongest_odds:.3f}; legacy entry floor is {ctx.min_entry_odds:.3f}."
            )

        min_lean = 0.5 + ctx.min_odds_edge
        if strongest_odds < min_lean:
            warnings.append(
                f"Market lean is weak at {strongest_odds:.3f}; legacy 50/50 threshold is {min_lean:.3f}."
            )

        if ctx.beat_crossings > ctx.chop_max_crossings:
            warnings.append(
                f"BTC crossed the beat {ctx.beat_crossings} times; legacy chop max is {ctx.chop_max_crossings}."
            )
        if ctx.chop_balanced_low <= ctx.beat_above_ratio <= ctx.chop_balanced_high:
            warnings.append(
                f"BTC time split is {ctx.beat_above_ratio:.0%}/{ctx.beat_below_ratio:.0%} above/below beat; legacy logic treats that as choppy."
            )

        snap = ctx.snap
        if (snap is not None
                and snap.odds_vel_direction != "NONE"
                and snap.direction_bias != "NONE"
                and snap.odds_vel_direction != snap.direction_bias
                and abs(snap.odds_vel_value) > 0.002):
            warnings.append(
                f"Odds velocity is racing {snap.odds_vel_direction} at {snap.odds_vel_value * 1000:.1f} mOdds/s against indicator bias {snap.direction_bias}."
            )

        if ctx.fair_prob:
            best_edge = max(
                ctx.fair_prob.get("edge_up", 0.0),
                ctx.fair_prob.get("edge_down", 0.0),
            )
            if best_edge < MINIMUM_EDGE_THRESHOLD:
                warnings.append(
                    f"Best fair-value EV is only {best_edge:+.1%}; legacy minimum edge is {MINIMUM_EDGE_THRESHOLD:.0%}."
                )

        if ctx.signal_alignment < ctx.min_signal_alignment:
            warnings.append(
                f"Family alignment is {ctx.signal_alignment}/6; legacy live floor is {ctx.min_signal_alignment}/6."
            )

        return warnings

    # ── Full evaluation (requires ai_signal) ─────────────────────────────────

    def evaluate(self, ctx: DecisionContext) -> TradeDecision:
        """Run all gates including AI signal gates.

        ctx.ai_signal must be set before calling this.
        Returns TradeDecision with action BUY or SKIP.
        """
        # Re-run market gates against the provided snapshot so post-AI checks
        # still honor the same market constraints as pre_ai_check().
        pre = self.pre_ai_check(ctx)
        if pre is not None:
            return pre

        signal = ctx.ai_signal
        if signal is None:
            return TradeDecision(
                action="SKIP", direction="NONE", confidence=0.0,
                reason="ai_signal not set on context",
                gate=GATE_AI_HOLD,
            )

        is_btc_above = ctx.btc_price > ctx.win.beat_price
        direction    = "UP" if is_btc_above else "DOWN"

        # GATE_AI_HOLD: AI chose not to trade
        if signal.signal not in ("BUY_UP", "BUY_DOWN"):
            return TradeDecision(
                action="SKIP", direction="NONE", confidence=signal.confidence,
                reason=f"AI={signal.signal} — hold signal",
                gate=GATE_AI_HOLD,
            )

        # GATE_DIR_CONFLICT: AI direction is contrarian to indicator consensus
        # during a temporary dip — require much higher conviction to override.
        #
        # Scenario: BTC briefly dips below beat, AI bets DOWN ("recovery impossible"),
        # but indicators (RSI, MA, alignment) lean UP and dip analysis shows
        # it's a transient move. Block low-confidence contrarian bets here.
        ai_dir = "UP" if signal.signal == "BUY_UP" else "DOWN"
        selected_odds = ctx.up_odds if ai_dir == "UP" else ctx.down_odds
        if selected_odds <= 0.0 or selected_odds >= 1.0:
            return TradeDecision(
                action="SKIP", direction=ai_dir, confidence=signal.confidence,
                reason=f"{ai_dir} odds {selected_odds:.3f} invalid for execution",
                gate=GATE_LOW_ENTRY_ODDS,
            )

        is_btc_above_beat = ctx.btc_price > ctx.win.beat_price
        natural_dir = "UP" if is_btc_above_beat else "DOWN"

        contrarian = (ai_dir != natural_dir)  # AI bets against current BTC position
        weak_consensus = ctx.signal_alignment <= 2
        is_temp_dip = ctx.dip_label == "TEMPORARY_DIP"

        if contrarian and (is_temp_dip or weak_consensus):
            required = ctx.dir_conflict_min_conf
            if signal.confidence < required:
                return TradeDecision(
                    action="SKIP", direction=ai_dir, confidence=signal.confidence,
                    reason=(
                        f"contrarian {ai_dir} vs {'TEMP_DIP' if is_temp_dip else 'weak'} "
                        f"alignment={ctx.signal_alignment} — "
                        f"need conf≥{required:.0%}, got {signal.confidence:.0%}"
                    ),
                    gate=GATE_DIR_CONFLICT,
                )

        # Dynamic live-entry floor: alignment is advisory now, not a hard wall.
        selected_model_edge = 0.0
        if ctx.fair_prob:
            selected_model_edge = ctx.fair_prob.get(
                "edge_up" if ai_dir == "UP" else "edge_down",
                0.0,
            )

        if ctx.signal_alignment >= ctx.min_signal_alignment:
            base_floor = 0.60
            min_conf_edge = 0.03
        elif ctx.signal_alignment == ctx.min_signal_alignment - 1:
            base_floor = 0.62
            min_conf_edge = 0.05
        elif ctx.signal_alignment == ctx.min_signal_alignment - 2:
            base_floor = 0.66
            min_conf_edge = 0.07
        else:
            base_floor = 0.74
            min_conf_edge = 0.10

        if selected_model_edge >= 0.20:
            min_conf_edge -= 0.01
        if selected_model_edge >= 0.35:
            min_conf_edge -= 0.01
        if ctx.dip_label in ("SUSTAINED_MOVE", "SUSTAINED_ABOVE"):
            min_conf_edge -= 0.01

        min_conf_edge = max(0.02, min_conf_edge)
        required_conf = max(base_floor, selected_odds + min_conf_edge)

        if signal.confidence < required_conf:
            required_conf = base_floor
            if ctx.seconds_remaining < 45:
                required_conf = max(required_conf, LATE_DYNAMIC_MIN_CONF)

            if selected_model_edge >= 0.20:
                required_conf -= 0.01
            if selected_model_edge >= 0.35:
                required_conf -= 0.01
            if ctx.dip_label in ("SUSTAINED_MOVE", "SUSTAINED_ABOVE"):
                required_conf -= 0.01

            required_conf = max(0.60, required_conf)  # safety floor
            required_conf = max(required_conf, selected_odds + min_conf_edge)

            if signal.confidence < required_conf:
                return TradeDecision(
                    action="SKIP", direction=ai_dir, confidence=signal.confidence,
                    reason=(
                        f"conf={signal.confidence:.0%} < req={required_conf:.0%} "
                        f"(odds={selected_odds:.0%}, align={ctx.signal_alignment}/6, "
                        f"EV={selected_model_edge:+.1%}, late_window={ctx.seconds_remaining}s)"
                    ),
                    gate=GATE_LOW_CONF,
                )

        # All gates passed
        ai_dir = "UP" if signal.signal == "BUY_UP" else "DOWN"
        return TradeDecision(
            action="BUY", direction=ai_dir, confidence=signal.confidence,
            reason=f"conf={signal.confidence:.0%} {signal.reason[:80]}",
            gate=GATE_OK,
        )

    # ── Post-order cancel check ───────────────────────────────────────────────

    def should_cancel(
        self,
        pos: "Position",
        current_up_odds: float,
        current_down_odds: float,
        seconds_remaining: int,
        current_confidence: float | None = None,
        current_btc_price: float | None = None,
        beat_price: float | None = None,
    ) -> tuple[bool, str]:
        """Check whether an open live order should be canceled.

        Returns (True, reason) when the order should be pulled, (False, "") otherwise.

        Cancel triggers (any one sufficient):
        1. Market odds fully priced against us
        2. BTC price reversed through beat with buffer (position going wrong way)
        3. Confidence collapsed below cancel floor (opt-in)
        """
        # Guard: only cancel with enough time left to process
        if seconds_remaining < CANCEL_MIN_SECONDS_GUARD:
            return False, ""

        pos_odds = current_up_odds if pos.direction == "UP" else current_down_odds
        opp_odds = current_down_odds if pos.direction == "UP" else current_up_odds

        # Trigger 1: opposite side has become a near-certainty (our side collapsed)
        if opp_odds >= CANCEL_ODDS_THRESHOLD:
            return True, (
                f"opposite side at {opp_odds:.3f} >= {CANCEL_ODDS_THRESHOLD} — "
                f"market certain against our {pos.direction} position"
            )

        # Trigger 2 (mirror): our own side odds fully collapsed
        if pos_odds <= (1.0 - CANCEL_ODDS_THRESHOLD):
            return True, (
                f"position odds {pos_odds:.3f} — our side has collapsed, "
                f"cutting loss on {pos.direction}"
            )

        # Trigger 3: BTC price has reversed through beat with buffer
        # e.g. we bet DOWN when BTC was below beat, but BTC has now crossed
        # back above beat by CANCEL_REVERSAL_BUFFER_PCT — cut the loss early.
        if current_btc_price is not None and beat_price is not None and beat_price > 0:
            buffer = beat_price * CANCEL_REVERSAL_BUFFER_PCT / 100.0
            if pos.direction == "DOWN" and current_btc_price >= beat_price + buffer:
                return True, (
                    f"BTC ${current_btc_price:,.2f} crossed above beat ${beat_price:,.2f} "
                    f"+ buffer ${buffer:.2f} — DOWN bet reversed, cutting"
                )
            if pos.direction == "UP" and current_btc_price <= beat_price - buffer:
                return True, (
                    f"BTC ${current_btc_price:,.2f} crossed below beat ${beat_price:,.2f} "
                    f"- buffer ${buffer:.2f} — UP bet reversed, cutting"
                )

        # Trigger 4: confidence dropped below cancel floor (opt-in)
        if current_confidence is not None and current_confidence < CANCEL_MIN_CONF:
            return True, (
                f"confidence dropped to {current_confidence:.0%} < "
                f"{CANCEL_MIN_CONF:.0%} cancel floor"
            )

        return False, ""


# ══════════════════════════════════════════════════════════════════════════════
# Source: market_client.py
# ══════════════════════════════════════════════════════════════════════════════

"""Polymarket CLOB + Gamma API client wrapper.

All py_clob_client calls are synchronous — every public method here
wraps them with asyncio.run_in_executor so the event loop never blocks.
"""

import asyncio
import json
import math
import re
import ssl
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from functools import partial

import certifi
import httpx
import websockets

_SSL_CTX = ssl.create_default_context(cafile=certifi.where())




# ── Data structures ───────────────────────────────────────────────────────────

@dataclass
class WindowInfo:
    condition_id: str
    question: str
    start_time: datetime
    end_time: datetime
    beat_price: float
    up_token_id: str    # outcome="Yes"
    down_token_id: str  # outcome="No"
    window_label: str   # e.g. "20:00"
    event_id: int = 0


@dataclass
class TradeResult:
    success: bool
    order_id: str | None = None
    error: str | None = None
    simulated: bool = False
    size: float | None = None
    price: float | None = None
    amount_usdc: float | None = None


@dataclass
class ClosedTrade:
    condition_id: str
    direction: str
    size: float
    price: float
    status: str       # CONFIRMED | MATCHED | FAILED
    match_time: str
    transaction_hash: str | None = None


# ── Client ────────────────────────────────────────────────────────────────────

class MarketClient:
    def __init__(self) -> None:
        self._client = self._build_client()
        self._http = httpx.AsyncClient(timeout=15, verify=certifi.where())

    # ── Setup ─────────────────────────────────────────────────────────────────

    def _build_client(self):
        from py_clob_client.client import ClobClient
        from py_clob_client.clob_types import ApiCreds

        eth_key = POLY_ETH_PRIVATE_KEY if POLY_ETH_PRIVATE_KEY else None
        client = ClobClient(
            CLOB_HOST,
            key=eth_key,
            chain_id=CHAIN_ID,
            signature_type=1,    # POLY_PROXY (email/Magic wallet)
            funder=POLY_FUNDER if eth_key else None,
        )

        if eth_key:
            # Derive L2 API credentials from the ETH key.
            # The hardcoded POLY_API_KEY/SECRET/PASSPHRASE are Builder Codes that
            # belong to a different account — deriving from ETH key gives user-level
            # credentials that can read balance, trades, etc.
            try:
                creds = client.create_or_derive_api_creds()
            except Exception:
                # Fallback to configured creds if derivation fails
                creds = ApiCreds(
                    api_key=POLY_API_KEY,
                    api_secret=POLY_SECRET,
                    api_passphrase=POLY_PASSPHRASE,
                )
        else:
            creds = ApiCreds(
                api_key=POLY_API_KEY,
                api_secret=POLY_SECRET,
                api_passphrase=POLY_PASSPHRASE,
            )

        client.set_api_creds(creds)
        return client

    async def _run(self, fn, *args, **kwargs):
        """Run a synchronous py_clob_client call in the thread pool."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, partial(fn, *args, **kwargs))

    async def refresh_credentials(self) -> bool:
        """Re-derive L2 API credentials from the ETH key.

        Polymarket L2 sessions expire roughly every 24 hours. Call this
        periodically to keep the session alive without restarting the bot.
        Returns True on success, False on failure (caller should retry later).
        """
        if not POLY_ETH_PRIVATE_KEY:
            return False
        try:
            creds = await self._run(self._client.create_or_derive_api_creds)
            self._client.set_api_creds(creds)
            return True
        except Exception:
            return False

    # ── Market discovery (slug-probe approach) ────────────────────────────────

    async def find_active_window(self) -> WindowInfo | None:
        """Find the currently active Bitcoin Up or Down 5-minute window.

        BTC Up/Down markets use slug `btc-updown-5m-{unix_ts}` where {unix_ts}
        is the exact window start time (multiple of 300 s).
        The Gamma list endpoint doesn't reliably return current windows, so we
        probe the slug directly.
        """
        now = datetime.now(timezone.utc)
        # 5-minute windows start on exact 300-second boundaries
        base_ts = int(now.timestamp() // 300) * 300

        # Check current window, previous window (in case we're right at the boundary)
        for offset in [0, -300, 300]:
            ts = base_ts + offset
            slug = f"btc-updown-5m-{ts}"
            try:
                resp = await self._http.get(f"{GAMMA_API}/events/slug/{slug}")
                if resp.status_code != 200:
                    continue
                event = resp.json()
                if not isinstance(event, dict):
                    continue

                markets = event.get("markets", [])
                if not markets or not isinstance(markets[0], dict):
                    continue
                m = markets[0]

                # Parse window times
                end_str   = m.get("endDate") or event.get("endDate", "")
                start_str = m.get("eventStartTime") or event.get("startDate", "")
                if not end_str or not start_str:
                    continue

                end_dt   = _parse_iso(end_str)
                start_dt = _parse_iso(start_str)
                if end_dt is None or start_dt is None:
                    continue

                # Must be currently live
                if not (start_dt <= now <= end_dt):
                    continue

                # Token IDs from clobTokenIds (JSON string)
                raw_ids = m.get("clobTokenIds", "[]")
                clob_ids: list[str] = json.loads(raw_ids) if isinstance(raw_ids, str) else raw_ids
                if len(clob_ids) < 2:
                    continue

                # outcomes[0]="Up", outcomes[1]="Down"
                raw_outcomes = m.get("outcomes", '["Up","Down"]')
                outcomes: list[str] = json.loads(raw_outcomes) if isinstance(raw_outcomes, str) else raw_outcomes
                up_idx = next((i for i, o in enumerate(outcomes) if "up" in o.lower()), 0)
                dn_idx = 1 - up_idx

                cond_id = m.get("conditionId", "")
                question = m.get("question", "") or event.get("title", "")
                label = start_dt.strftime("%H:%M")

                return WindowInfo(
                    condition_id=cond_id,
                    question=question,
                    start_time=start_dt,
                    end_time=end_dt,
                    beat_price=_extract_price(question),  # parsed from "Will BTC be above $X?"; 0.0 if not found
                    up_token_id=clob_ids[up_idx],
                    down_token_id=clob_ids[dn_idx],
                    window_label=label,
                )

            except Exception:
                continue

        return None

    # ── Odds ──────────────────────────────────────────────────────────────────

    async def get_odds(self, up_token_id: str, down_token_id: str) -> tuple[float, float]:
        """Return (up_odds, down_odds) as floats via GET /midpoint (two parallel calls)."""
        try:
            r_up, r_dn = await asyncio.gather(
                self._http.get(f"{CLOB_HOST}/midpoint", params={"token_id": up_token_id}),
                self._http.get(f"{CLOB_HOST}/midpoint", params={"token_id": down_token_id}),
                return_exceptions=True,
            )
            def _mid(r) -> float:
                if isinstance(r, Exception) or not r.is_success:
                    return 0.5
                body = r.json()
                # CLOB returns {"mid_price": "0.505"} — "mid" is a legacy alias
                raw = body.get("mid_price") or body.get("mid")
                return float(raw) if raw is not None else 0.5
            up   = _mid(r_up)
            down = _mid(r_dn)
            return up, down
        except Exception:
            return 0.5, 0.5

    # ── Balance ───────────────────────────────────────────────────────────────

    async def get_balance(self) -> float:
        """Return USDC collateral balance."""
        try:
            from py_clob_client.clob_types import AssetType, BalanceAllowanceParams
            result = await self._run(
                self._client.get_balance_allowance,
                BalanceAllowanceParams(
                    asset_type=AssetType.COLLATERAL,
                    signature_type=1,
                ),
            )
            raw = result.get("balance", "0") if isinstance(result, dict) else "0"
            return float(raw) / 1e6   # USDC has 6 decimals
        except Exception:
            return 0.0

    # ── Order placement ───────────────────────────────────────────────────────

    async def place_bet(
        self,
        direction: str,
        token_id: str,
        amount_usdc: float,
        current_odds: float,
    ) -> TradeResult:
        """Place a GTC limit order at current market price. If LIVE_TRADING=false, simulate."""
        if not LIVE_TRADING:
            sim_id = f"SIM-{int(time.time())}"
            price = round(max(0.01, min(0.99, current_odds)), 2)
            size = math.floor((amount_usdc / price) * 100) / 100 if price > 0 else 0.0
            return TradeResult(
                success=True,
                order_id=sim_id,
                simulated=True,
                size=size,
                price=price,
                amount_usdc=amount_usdc,
            )

        if not POLY_ETH_PRIVATE_KEY:
            return TradeResult(
                success=False,
                error="POLY_ETH_PRIVATE_KEY missing — cannot sign orders for live trading. "
                      "Export your Ethereum private key and add it to .env",
            )

        try:
            from py_clob_client.clob_types import OrderArgs, OrderType

            # Use a GTC limit order at the current market price.
            # FAK market orders fail with "no orders found to match with" when the
            # book has no immediate liquidity (common in the final minutes of a window).
            # GTC limit orders rest in the book and fill when matched; the position
            # monitor handles cancellation if conditions deteriorate before fill.
            price = round(max(0.01, min(0.99, current_odds)), 2)
            requested_size = amount_usdc / price if price > 0 else 0.0
            size = math.floor(requested_size * 100) / 100
            min_order_size = await self.get_min_order_size(token_id)

            if min_order_size > 0 and requested_size + 1e-9 < min_order_size:
                min_notional = min_order_size * price
                return TradeResult(
                    success=False,
                    error=(
                        f"requested ${amount_usdc:.2f} buys only {requested_size:.2f} shares "
                        f"at {price:.2f}, below market minimum {min_order_size:.2f} shares "
                        f"(min spend ${min_notional:.2f})"
                    ),
                )

            if min_order_size > 0 and size < min_order_size:
                size = min_order_size

            actual_amount_usdc = round(size * price, 4)

            order_args = OrderArgs(
                token_id=token_id,
                price=price,
                size=size,
                side="BUY",  # direction is encoded in token_id (up_token vs down_token)
            )
            signed = await self._run(self._client.create_order, order_args)
            resp   = await self._run(self._client.post_order, signed, OrderType.GTC)

            if resp and resp.get("success"):
                return TradeResult(
                    success=True,
                    order_id=resp.get("orderID"),
                    size=size,
                    price=price,
                    amount_usdc=actual_amount_usdc,
                )
            else:
                return TradeResult(success=False, error=str(resp.get("errorMsg", "unknown")))
        except Exception as exc:
            return TradeResult(success=False, error=str(exc))

    async def get_min_order_size(self, token_id: str) -> float:
        """Return the market minimum order size from the public order book."""
        try:
            book = await self._run(self._client.get_order_book, token_id)
            raw = getattr(book, "min_order_size", None)
            if raw is None and isinstance(book, dict):
                raw = book.get("min_order_size")
            value = float(raw) if raw is not None else 1.0
            return value if value > 0 else 1.0
        except Exception:
            # Safe fallback: never silently inflate to a large hard-coded size.
            return 1.0

    # ── Heartbeat ─────────────────────────────────────────────────────────────

    async def send_heartbeat(self) -> bool:
        """POST /heartbeats to keep the CLOB session alive."""
        try:
            await self._run(self._client.post_heartbeat)
            return True
        except Exception:
            return False

    # ── Order management ──────────────────────────────────────────────────────

    async def get_order(self, order_id: str) -> dict:
        """GET /order/{orderID} — fetch a single order by ID.

        Returns order dict with key 'status':
          LIVE | MATCHED | CANCELED | CANCELED_MARKET_RESOLVED | INVALID
        Returns empty dict on failure.
        """
        try:
            result = await self._run(self._client.get_order, order_id)
            return result if isinstance(result, dict) else {}
        except Exception:
            return {}

    async def cancel_order(self, order_id: str) -> tuple[bool, str]:
        """DELETE /order — cancel a single open order.

        Returns (True, "") on success.
        Returns (False, reason) on failure, where reason comes from the
        not_canceled map in the API response, e.g. "Order not found or already canceled".
        """
        try:
            result = await self._run(self._client.cancel, {"orderID": order_id})
            if not isinstance(result, dict):
                return False, "unexpected response format"
            if order_id in result.get("canceled", []):
                return True, ""
            reason = result.get("not_canceled", {}).get(order_id, "unknown reason")
            return False, reason
        except Exception as exc:
            return False, str(exc)

    async def cancel_orders(self, order_ids: list[str]) -> dict:
        """DELETE /orders — cancel up to 3000 orders in one call.

        Returns {"canceled": [...], "not_canceled": {...}}.
        """
        try:
            result = await self._run(self._client.cancel_orders, order_ids)
            return result if isinstance(result, dict) else {}
        except Exception:
            return {}

    async def cancel_all_orders(self) -> bool:
        """DELETE /cancel-all — cancel every open order for this account."""
        try:
            await self._run(self._client.cancel_all)
            return True
        except Exception:
            return False

    async def get_user_orders(
        self,
        market: str | None = None,
        asset_id: str | None = None,
    ) -> list[dict]:
        """GET /orders — list open orders, optionally filtered by market or token.

        Returns list of order dicts.
        """
        try:
            from py_clob_client.clob_types import OpenOrderParams
            params = OpenOrderParams(market=market, asset_id=asset_id)
            result = await self._run(self._client.get_orders, params)
            return result.get("data", []) if isinstance(result, dict) else []
        except Exception:
            return []

    async def get_order_scoring(self, order_id: str) -> bool:
        """GET /order-scoring?order_id=... — check if order earns LP rewards."""
        try:
            headers = self._l2_auth_headers("GET", "/order-scoring")
            r = await self._http.get(
                f"{CLOB_HOST}/order-scoring",
                params={"order_id": order_id},
                headers=headers,
            )
            return bool(r.json().get("scoring", False))
        except Exception:
            return False

    def _l2_auth_headers(self, method: str, path: str, body: str = "") -> dict:
        """Build HMAC L2 authentication headers for direct CLOB HTTP calls."""
        import base64
        import hashlib
        import hmac as _hmac

        creds = self._client.creds
        ts = str(int(time.time()))
        msg = ts + method.upper() + path + body
        sig = base64.b64encode(
            _hmac.new(
                creds.api_secret.encode("utf-8"),
                msg.encode("utf-8"),
                hashlib.sha256,
            ).digest()
        ).decode("utf-8")
        return {
            "POLY_ADDRESS":    POLY_ADDRESS,
            "POLY_TIMESTAMP":  ts,
            "POLY_API_KEY":    creds.api_key,
            "POLY_SIGNATURE":  sig,
            "POLY_PASSPHRASE": creds.api_passphrase,
            "Content-Type":    "application/json",
        }

    # ── Trades (position tracking) ────────────────────────────────────────────

    async def get_recent_trades(self, after_ts: float | None = None) -> list[ClosedTrade]:
        """Return trades for our address via GET /trades."""
        try:
            from py_clob_client.clob_types import TradeParams
            params = TradeParams(maker_address=POLY_ADDRESS)
            result = await self._run(self._client.get_trades, params)

            trades = []
            data = result.get("data", []) if isinstance(result, dict) else []
            for t in data:
                trades.append(ClosedTrade(
                    condition_id=t.get("market", ""),
                    direction="UP" if t.get("outcome", "").lower() in ("yes", "up") else "DOWN",
                    size=float(t.get("size", 0)),
                    price=float(t.get("price", 0)),
                    status=t.get("status", "UNKNOWN"),
                    match_time=t.get("match_time", ""),
                    transaction_hash=t.get("transaction_hash"),
                ))
            return trades
        except Exception:
            return []

    # ── Market WebSocket (odds + resolved events) ─────────────────────────────

    async def subscribe_market_ws(
        self,
        up_token_id: str,
        down_token_id: str,
        state: "BotState",
        condition_id: str = "",
    ) -> None:
        """Stream real-time odds updates and market_resolved events.

        Exits when state.window.condition_id no longer matches condition_id
        (so the caller can re-subscribe for the next window).
        """
        sub_msg = json.dumps({
            "assets_ids": [up_token_id, down_token_id],
            "type": "market",
            "initial_dump": True,
            "level": 2,
            "custom_feature_enabled": True,
        })

        while state.running:
            # Exit if the caller's window has been replaced
            if condition_id and (state.window is None or state.window.condition_id != condition_id):
                return

            try:
                async with websockets.connect(
                    MARKET_WS,
                    ssl=_SSL_CTX,
                    ping_interval=None,  # Polymarket server ignores RFC 6455 pings → disable
                    close_timeout=5,
                ) as ws:
                    await ws.send(sub_msg)
                    state.log_event("[MKTWS] Market WebSocket connected")
                    while True:
                        # Exit if window changed
                        if condition_id and (state.window is None or state.window.condition_id != condition_id):
                            return
                        try:
                            raw = await asyncio.wait_for(ws.recv(), timeout=30)
                        except asyncio.TimeoutError:
                            # No message for 30s — connection stale, reconnect
                            state.log_event("[MKTWS] idle 30s, reconnecting…")
                            break
                        msgs = json.loads(raw)
                        if isinstance(msgs, dict):
                            msgs = [msgs]
                        for msg in msgs:
                            etype = msg.get("event_type", "")
                            if etype in ("price_change", "book", "last_trade_price"):
                                _update_odds_from_ws(msg, up_token_id, down_token_id, state)
                            elif etype == "market_resolved":
                                state.log_event(f"[MKTWS] market_resolved: {msg.get('market')}")
                                state.market_resolved_event.set()
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                state.log_event(f"[MKTWS] error: {exc}, reconnecting…")
                await asyncio.sleep(5)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _parse_iso(s: str) -> datetime | None:
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ",
                "%Y-%m-%dT%H:%M:%S+00:00", "%Y-%m-%dT%H:%M:%S"):
        try:
            dt = datetime.strptime(s[:26], fmt[:len(fmt)])
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    try:
        from datetime import datetime as dt2
        return dt2.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def _extract_price(question: str) -> float:
    """Extract dollar amount from question string like 'Will BTC be above $70,845?'"""
    match = re.search(r"\$[\d,]+(?:\.\d+)?", question)
    if match:
        return float(match.group().replace("$", "").replace(",", ""))
    return 0.0


def _update_odds_from_ws(
    msg: dict,
    up_token_id: str,
    down_token_id: str,
    state: "BotState",
) -> None:
    asset = msg.get("asset_id", "")
    price = msg.get("price") or msg.get("last_trade_price")
    if price is None:
        # Try extracting from bids/asks midpoint
        bids = msg.get("bids", [])
        asks = msg.get("asks", [])
        if bids and asks:
            best_bid = float(bids[0].get("price", 0) if isinstance(bids[0], dict) else bids[0])
            best_ask = float(asks[0].get("price", 0) if isinstance(asks[0], dict) else asks[0])
            price = (best_bid + best_ask) / 2
    if price is None:
        return
    price = float(price)
    if asset == up_token_id:
        state.up_odds = price
    elif asset == down_token_id:
        state.down_odds = price
    state.odds_updated_at = time.time()


# ══════════════════════════════════════════════════════════════════════════════
# Source: telegram_notifier.py
# ══════════════════════════════════════════════════════════════════════════════

"""Telegram Bot notification layer.

All public methods are fire-and-forget: they schedule an asyncio task and
return immediately so the trading loop is never blocked waiting for Telegram.

Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env to enable.
If either is missing, every call is a silent no-op.
"""

import asyncio
import html

import certifi
import httpx




class TelegramNotifier:
    def __init__(self) -> None:
        self._enabled = TELEGRAM_ENABLED
        if not self._enabled:
            return
        self._url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        self._client = httpx.AsyncClient(
            timeout=10,
            verify=certifi.where(),
        )
        self._mode = "🟢 LIVE" if LIVE_TRADING else "🟡 PAPER"

    # ── Public fire-and-forget helpers ────────────────────────────────────────

    def notify_window(self, win: "WindowInfo") -> None:
        """New market window detected."""
        if not self._enabled:
            return
        text = (
            f"🆕 <b>New Window</b> | {win.window_label} UTC\n"
            f"Beat: <code>${win.beat_price:,.2f}</code>\n"
            f"Ends: {win.end_time.strftime('%H:%M:%S')} UTC\n"
            f"Mode: {self._mode}"
        )
        self._fire(text)

    def notify_bet(
        self,
        direction: str,
        bet_size: float,
        entry_odds: float,
        win: "WindowInfo",
        order_id: str,
        simulated: bool,
        snap: "IndicatorSnapshot",
    ) -> None:
        """Bet successfully placed."""
        if not self._enabled:
            return
        emoji = "⬆️" if direction == "UP" else "⬇️"
        mode_tag = "PAPER" if simulated else "LIVE"
        payout = bet_size / entry_odds if entry_odds > 0 else 0
        text = (
            f"🎯 <b>BET {direction}</b> {emoji}  [{mode_tag}]\n"
            f"Amount: <code>${bet_size:.2f}</code> @ {entry_odds:.3f}  "
            f"(payout ${payout:.2f})\n"
            f"Window: {win.window_label}  Beat: <code>${win.beat_price:,.2f}</code>\n"
            f"Align: {snap.signal_alignment}/6  CVD: {snap.cvd_divergence}\n"
            f"Order: <code>{order_id}</code>"
        )
        self._fire(text)

    def notify_ai_signal(
        self,
        signal: "AISignal",
        win: "WindowInfo",
        snap: "IndicatorSnapshot",
        *,
        btc_price: float,
        up_odds: float,
        down_odds: float,
        decision: "TradeDecision | None" = None,
    ) -> None:
        """AI returned a signal, regardless of whether the engine placed a bet."""
        if not self._enabled:
            return

        emoji = {
            "BUY_UP": "⬆️",
            "BUY_DOWN": "⬇️",
            "SKIP": "⏸️",
        }.get(signal.signal, "🧠")
        signal_label = html.escape(signal.signal)
        reason = html.escape(signal.reason[:160])
        raw_conf = signal.raw_confidence or signal.confidence
        decision_line = ""
        if decision is not None:
            decision_line = (
                f"\nEngine: <b>{html.escape(decision.action)}</b>  "
                f"<code>{html.escape(decision.gate)}</code>"
            )
            if decision.reason:
                decision_line += f"\nWhy: {html.escape(decision.reason[:140])}"

        text = (
            f"🧠 <b>AI Signal</b> {emoji}  {self._mode}\n"
            f"Signal: <b>{signal_label}</b>  conf=<code>{signal.confidence:.0%}</code>  "
            f"raw=<code>{raw_conf:.0%}</code>\n"
            f"Window: {html.escape(win.window_label)}  Beat: <code>${win.beat_price:,.2f}</code>\n"
            f"BTC: <code>${btc_price:,.2f}</code>  Odds U/D: <code>{up_odds:.3f}/{down_odds:.3f}</code>\n"
            f"Align: {snap.signal_alignment}/6  Dip: {html.escape(signal.dip_label)}  "
            f"CVD: {html.escape(snap.cvd_divergence)}{decision_line}\n"
            f"AI Why: {reason}"
        )
        self._fire(text)

    def notify_result(self, pos: "Position", state: "BotState") -> None:
        """Bet resolved — won or lost."""
        if not self._enabled:
            return
        if pos.status == "won":
            emoji = "✅"
            pnl_s = f"+${pos.pnl:.2f}" if pos.pnl is not None else "?"
        else:
            emoji = "❌"
            pnl_s = f"-${abs(pos.pnl):.2f}" if pos.pnl is not None else "?"
        wr = state.win_rate
        text = (
            f"{emoji} <b>{'WON' if pos.status == 'won' else 'LOST'}</b>  {pnl_s}\n"
            f"Direction: {pos.direction}  Entry: {pos.entry_price:.3f}\n"
            f"Beat was: <code>${pos.window_beat:,.2f}</code>\n"
            f"Record: {state.win_count}W / {state.loss_count}L  "
            f"({wr:.1f}%)  Total PnL: {'+' if state.total_pnl >= 0 else ''}"
            f"${state.total_pnl:.2f}"
        )
        self._fire(text)

    # ── Raw send ──────────────────────────────────────────────────────────────

    async def send(self, text: str) -> None:
        """Awaitable send — use _fire() for fire-and-forget from sync context."""
        if not self._enabled:
            return
        try:
            await self._client.post(
                self._url,
                json={
                    "chat_id": TELEGRAM_CHAT_ID,
                    "text": text,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                },
            )
        except Exception:
            pass   # Telegram failures must never block or crash the trading loop

    # ── Internal ──────────────────────────────────────────────────────────────

    def _fire(self, text: str) -> None:
        """Schedule send as a background task — never awaited, never blocks."""
        try:
            asyncio.get_running_loop().create_task(self.send(text))
        except RuntimeError:
            pass   # no running loop (e.g., called from __init__ context)


# ══════════════════════════════════════════════════════════════════════════════
# Source: btc_feed.py
# ══════════════════════════════════════════════════════════════════════════════

import asyncio
import json
import ssl
import time

import certifi
import websockets



# macOS / Python often lacks system CA certs; use certifi's bundle for WSS
_SSL_CTX = ssl.create_default_context(cafile=certifi.where())


class BTCFeed:
    """Streams BTC/USDC trade prices from Binance WebSocket.

    USDC (not USDT) is used because USDC is redeemable 1:1 for USD, giving
    prices that match Chainlink BTC/USD (Polymarket's resolution source).
    USDT carries a ~0.07% premium (~$50 at $69k BTC) that skews beat price.

    Uses certifi SSL context so TLS handshake works on macOS without
    needing the system keychain. Auto-reconnects on any disconnect.
    """

    def __init__(self, state: "BotState") -> None:
        self.state = state

    async def run(self) -> None:
        while self.state.running:
            try:
                await self._connect_and_stream()
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                self.state.log_event(f"[BTC] reconnecting after error: {exc}")
                self.state.btc_ws_ok = False
                await asyncio.sleep(3)

    async def _connect_and_stream(self) -> None:
        async with websockets.connect(
            BINANCE_WS,
            ssl=_SSL_CTX,
            ping_interval=20,
            ping_timeout=10,
        ) as ws:
            self.state.btc_ws_ok = True
            self.state.log_event("[BTC] Binance WebSocket connected")
            async for raw in ws:
                data = json.loads(raw)
                price = float(data["p"])
                ts = data.get("T", int(time.time() * 1000)) / 1000.0
                self.state.btc_price = price
                self.state.btc_price_time = ts
                self.state.price_history.append(price)
                self.state.price_history_ts.append((ts, price))

                # Volume accumulation for CVD / VWAP
                # "q" = BTC quantity per trade tick (base asset volume)
                # "m" = is buyer the market maker?
                #   True  → seller-initiated (sell pressure) → sell volume
                #   False → buyer-initiated  (buy pressure)  → buy volume
                vol = float(data.get("q", 0.0))
                if data.get("m", True):
                    self.state._tick_sell_vol += vol
                else:
                    self.state._tick_buy_vol += vol


# ══════════════════════════════════════════════════════════════════════════════
# Source: bot.py
# ══════════════════════════════════════════════════════════════════════════════

"""Central bot state and all async orchestration loops."""

import asyncio
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from datetime import timezone as _TZ

_UTC = _TZ.utc   # timezone instance — used everywhere datetime.now(tz) is needed



# ── Data structures ───────────────────────────────────────────────────────────

@dataclass
class Position:
    condition_id: str
    direction: str      # "UP" | "DOWN"
    token_id: str
    size: float         # shares bought (amount_usdc / entry_price)
    entry_price: float  # entry odds (0–1)
    placed_at: datetime
    order_id: str
    status: str = "open"   # "open" | "won" | "lost" | "canceled"
    pnl: float | None = None
    simulated: bool = False
    amount_usdc: float = 0.0   # actual USDC spent on the order (used for correct PnL)
    window_beat: float = 0.0   # beat price of THIS window (not current window)
    window_end_at: datetime | None = None
    elapsed_at_bet: int = 0    # seconds elapsed when bet was placed
    gap_pct_at_bet: float = 0.0  # BTC gap % from beat at time of bet
    ai_confidence: float = 0.0   # AI confidence at time of bet
    ai_raw_confidence: float = 0.0
    signal_alignment: int = 0


@dataclass
class BlockedWindow:
    """Tracks a window where we chose SKIP, to retroactively evaluate quality."""
    window_label: str
    beat_price: float
    skip_reason: str
    suggested_direction: str = "NONE"
    final_btc_price: float | None = None
    would_have_won: bool | None = None   # True = filter correctly blocked (saved loss)


@dataclass
class WindowPredictionRecord:
    condition_id: str
    window_label: str
    window_end_at: datetime | None
    beat_price: float
    predicted_direction: str = "NONE"
    decision_action: str = "blocked"   # "blocked" | "paper_trade"
    simulated_order_id: str = ""
    confidence: float = 0.0
    raw_confidence: float = 0.0
    alignment: int = 0
    actual_winner: str = ""
    prediction_correct: bool | None = None
    paper_trade_won: bool | None = None
    resolved_at: datetime | None = None
    last_updated_at: datetime | None = None


@dataclass
class PaperPerformanceStats:
    prediction_correct_total: int = 0
    prediction_incorrect_total: int = 0
    prediction_correct_today: int = 0
    prediction_incorrect_today: int = 0
    paper_trade_wins_total: int = 0
    paper_trade_losses_total: int = 0
    paper_trade_wins_today: int = 0
    paper_trade_losses_today: int = 0

    def apply_counts(self, counts: dict[str, int]) -> None:
        for key in (
            "prediction_correct_total",
            "prediction_incorrect_total",
            "prediction_correct_today",
            "prediction_incorrect_today",
            "paper_trade_wins_total",
            "paper_trade_losses_total",
            "paper_trade_wins_today",
            "paper_trade_losses_today",
        ):
            setattr(self, key, int(counts.get(key, 0) or 0))

    def reset_today(self) -> None:
        self.prediction_correct_today = 0
        self.prediction_incorrect_today = 0
        self.paper_trade_wins_today = 0
        self.paper_trade_losses_today = 0

    def record_prediction(self, correct: bool) -> None:
        if correct:
            self.prediction_correct_total += 1
            self.prediction_correct_today += 1
        else:
            self.prediction_incorrect_total += 1
            self.prediction_incorrect_today += 1

    def record_paper_trade(self, won: bool) -> None:
        if won:
            self.paper_trade_wins_total += 1
            self.paper_trade_wins_today += 1
        else:
            self.paper_trade_losses_total += 1
            self.paper_trade_losses_today += 1

    @property
    def prediction_total(self) -> int:
        return self.prediction_correct_total + self.prediction_incorrect_total

    @property
    def prediction_today_total(self) -> int:
        return self.prediction_correct_today + self.prediction_incorrect_today

    @property
    def prediction_accuracy(self) -> float:
        total = self.prediction_total
        return (self.prediction_correct_total / total * 100.0) if total else 0.0

    @property
    def prediction_accuracy_today(self) -> float:
        total = self.prediction_today_total
        return (self.prediction_correct_today / total * 100.0) if total else 0.0

    @property
    def paper_trade_total(self) -> int:
        return self.paper_trade_wins_total + self.paper_trade_losses_total

    @property
    def paper_trade_today_total(self) -> int:
        return self.paper_trade_wins_today + self.paper_trade_losses_today

    @property
    def paper_trade_win_rate(self) -> float:
        total = self.paper_trade_total
        return (self.paper_trade_wins_total / total * 100.0) if total else 0.0

    @property
    def paper_trade_win_rate_today(self) -> float:
        total = self.paper_trade_today_total
        return (self.paper_trade_wins_today / total * 100.0) if total else 0.0


@dataclass
class BotState:
    # ── Runtime
    start_time: datetime = field(default_factory=datetime.now)
    running: bool = True

    # ── BTC feed
    btc_price: float | None = None
    btc_price_time: float = 0.0
    btc_ws_ok: bool = False
    price_history: deque = field(default_factory=lambda: deque(maxlen=300))
    # Timestamped tick buffer: (unix_ts, price) — used to look up the BTC price
    # at the exact window open time so beat_price matches Polymarket's Chainlink snapshot.
    # maxlen=1200 covers ~2 minutes at ~10 ticks/sec, safely spanning detection delays.
    price_history_ts: deque = field(default_factory=lambda: deque(maxlen=1200))
    # Time-sampled price history (one price per 5 seconds) — used for all indicators.
    # Raw ticks come at ~10/sec; 10-tick MA5/momentum are meaningless for a 5-min window.
    price_history_5s: deque = field(default_factory=lambda: deque(maxlen=300))

    # ── Volume feed for CVD / VWAP (accumulated per 5-second period) ──────────
    # Raw tick accumulators — reset by price_sampler every 5s
    _tick_buy_vol: float = 0.0    # BTC buy volume since last 5s sample
    _tick_sell_vol: float = 0.0   # BTC sell volume since last 5s sample
    # 5-second sampled volume history
    buy_vol_5s: deque = field(default_factory=lambda: deque(maxlen=300))
    sell_vol_5s: deque = field(default_factory=lambda: deque(maxlen=300))
    # Running CVD (cumulative buy_vol − sell_vol) at each 5s mark
    cvd_5s: deque = field(default_factory=lambda: deque(maxlen=300))

    # ── Current Polymarket window
    window: WindowInfo | None = None
    window_found_at: float = 0.0
    market_resolved_event: asyncio.Event = field(default_factory=asyncio.Event)

    # ── Live odds
    up_odds: float | None = None
    down_odds: float | None = None
    odds_updated_at: float | None = None
    # Timestamped odds history for velocity computation: (ts, up_odds, down_odds)
    odds_history: deque = field(default_factory=lambda: deque(maxlen=120))

    # ── Filters / AI
    indicator_snapshot: IndicatorSnapshot | None = None
    last_signal: AISignal | None = None
    last_filter_time: float = 0.0
    last_pre_ai_decision: TradeDecision | None = None
    last_trade_decision: TradeDecision | None = None
    latest_fair_prob: dict = field(default_factory=dict)
    latest_beat_chop: dict = field(default_factory=dict)
    engine_phase: str = "BOOT"
    engine_gate: str = ""
    engine_reason: str = ""
    engine_updated_at: float = 0.0

    # ── Positions
    positions: list[Position] = field(default_factory=list)
    bets_this_hour: int = 0
    hour_reset_at: float = field(default_factory=time.time)
    # Set of condition_ids where a bet was ATTEMPTED this session (success or fail).
    # Populated BEFORE place_bet is called so that a failed order never retries.
    bet_attempted_windows: set = field(default_factory=set)

    # ── Results
    balance_usdc: float = 0.0
    total_pnl: float = 0.0
    resolved_count: int = 0
    win_count: int = 0
    loss_count: int = 0
    pending_count: int = 0
    claim_log: list[str] = field(default_factory=list)

    # ── Daily limits (reset at midnight UTC)
    daily_loss: float = 0.0           # realized losses today
    daily_profit: float = 0.0         # realized profit today
    daily_day: str = ""               # "YYYY-MM-DD" of current trading day
    daily_halted: bool = False        # True when daily loss limit reached
    daily_profit_halted: bool = False # True when daily profit target reached

    # ── Loss streak protection ──────────────────────────────────────────────
    consecutive_losses: int = 0
    consecutive_wins: int = 0
    streak_pause_until: float = 0.0   # unix timestamp; 0 = not paused

    # ── Window outcome history (for AI historical context) ──────────────────
    # Each entry: {elapsed_at_bet, gap_pct, direction, won, odds, confidence}
    recent_window_outcomes: deque = field(default_factory=lambda: deque(maxlen=50))

    # ── Clean paper analytics ────────────────────────────────────────────────
    paper_prediction_records: dict[str, WindowPredictionRecord] = field(default_factory=dict)
    paper_stats: PaperPerformanceStats = field(default_factory=PaperPerformanceStats)

    # ── BLOCKED tracking
    blocked_windows: list[BlockedWindow] = field(default_factory=list)

    # ── Price tick log for UI streaming (ts, btc, buy_vol, sell_vol, cvd, up_odds, dn_odds)
    price_tick_log: deque = field(default_factory=lambda: deque(maxlen=200))

    # ── Event log (all bot output goes here, no print())
    event_log: list[tuple[datetime, str]] = field(default_factory=list)

    # ── Persistent file logger
    logger: BotLogger = field(default_factory=BotLogger)

    # ── Async lock for list mutations
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    def log_event(self, msg: str) -> None:
        entry = (datetime.now(), msg)
        self.event_log.append(entry)
        if len(self.event_log) > 200:
            self.event_log.pop(0)
        self.logger.log_event(msg)

    def set_engine_status(self, phase: str, gate: str = "", reason: str = "") -> None:
        self.engine_phase = phase
        self.engine_gate = gate
        self.engine_reason = reason
        self.engine_updated_at = time.time()

    @property
    def win_rate(self) -> float:
        total = self.win_count + self.loss_count
        return (self.win_count / total * 100.0) if total > 0 else 0.0

    @property
    def uptime(self) -> str:
        delta = datetime.now() - self.start_time
        m, s = divmod(int(delta.total_seconds()), 60)
        h, m = divmod(m, 60)
        if h:
            return f"{h}h {m}m {s}s"
        return f"{m}m {s}s"

    @property
    def open_positions(self) -> list[Position]:
        return [p for p in self.positions if p.status == "open"]

    @property
    def blocked_win_count(self) -> int:
        """Trades where filter CORRECTLY blocked (would have lost = filter saved money)."""
        return sum(1 for b in self.blocked_windows if b.would_have_won is False)

    @property
    def blocked_loss_count(self) -> int:
        """Trades where filter INCORRECTLY blocked (would have won = missed profit)."""
        return sum(1 for b in self.blocked_windows if b.would_have_won is True)

    @property
    def blocked_resolved(self) -> int:
        return sum(1 for b in self.blocked_windows if b.would_have_won is not None)

    @property
    def blocked_accuracy(self) -> float:
        """% of blocked trades that would have LOST (= filter correctly blocked them)."""
        r = self.blocked_resolved
        if r == 0:
            return 0.0
        return self.blocked_win_count / r * 100.0


# ── Safe loop wrapper ─────────────────────────────────────────────────────────

async def safe_loop(coro_fn, name: str, state: BotState, delay: float = 5.0):
    """Run coro_fn() in a loop; catch exceptions, log, and retry after delay."""
    while state.running:
        try:
            await coro_fn()
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            state.log_event(f"[ERR:{name}] {exc}")
            await asyncio.sleep(delay)


# ── Main bot class ────────────────────────────────────────────────────────────

class TradingBot:
    def __init__(self) -> None:
        self.state    = BotState()
        self.feed     = BTCFeed(self.state)
        self.market   = MarketClient()
        self.ai       = AIAgent()
        self.notifier = TelegramNotifier()
        self.decision = DecisionMaker()

    async def run(self) -> None:
        self.state.log_event("[BOT] Starting up…")
        recovered, skipped = await self._recover_open_positions()
        if recovered:
            self.state.log_event(
                f"[RECOVER] Restored {recovered} unsettled position(s) from logs"
            )
            # Settle any recovered positions whose market already ended before startup.
            await self._check_positions()
        if skipped:
            self.state.log_event(
                f"[RECOVER] Ignored {skipped} log-only position(s) not found on account"
            )
        warmed = self._warm_recent_outcomes()
        if warmed:
            self.state.log_event(
                f"[HISTORY] Warmed {warmed} settled outcomes for calibration/context"
            )
        restored_predictions, warmed_paper = self._warm_paper_analytics()
        if warmed_paper:
            self.state.log_event(
                f"[PAPER] Warmed {warmed_paper} resolved paper analytics entries"
            )
        if restored_predictions:
            self.state.log_event(
                f"[PAPER] Restored {restored_predictions} pending paper prediction(s)"
            )
        if not LIVE_TRADING:
            await self._sync_recovered_paper_positions()
        self.state.daily_day = datetime.now(_UTC).strftime("%Y-%m-%d")
        await asyncio.gather(
            safe_loop(self.feed.run,                  "btc_feed",  self.state),
            safe_loop(self._price_sampler,            "sampler",   self.state),
            safe_loop(self._market_loop,              "market",    self.state),
            safe_loop(self._odds_ws_loop,             "odds_ws",   self.state),
            safe_loop(self._trading_loop,             "trading",   self.state),
            safe_loop(self._position_monitor_loop,    "pos_mon",   self.state),
            safe_loop(self._results_loop,             "results",   self.state),
            safe_loop(self._balance_loop,             "balance",   self.state),
            safe_loop(self._creds_refresh_loop,       "creds",     self.state),
        )

    # ── Market discovery loop ─────────────────────────────────────────────────

    # ── Price sampler (one tick per 5s for indicators) ────────────────────────

    async def _price_sampler(self) -> None:
        """Sample BTC price and volume every 5 seconds into history buffers.

        Raw Binance ticks arrive at ~10/sec; using them directly makes
        MA5/MA20/momentum meaningless (covers only 0.5–2 seconds).
        At 5-second intervals: MA5 ≈ 25s, MA20 ≈ 100s, momentum ≈ 50s.

        Also snapshots accumulated buy/sell volume for CVD and VWAP.
        """
        while self.state.running:
            await asyncio.sleep(5)
            if self.state.btc_price is not None:
                self.state.price_history_5s.append(self.state.btc_price)

            # Record timestamped odds for velocity computation
            if self.state.up_odds is not None and self.state.down_odds is not None:
                self.state.odds_history.append(
                    (time.time(), self.state.up_odds, self.state.down_odds)
                )

            # Snapshot and reset volume accumulators (atomic in asyncio single thread)
            buy_v  = self.state._tick_buy_vol
            sell_v = self.state._tick_sell_vol
            self.state._tick_buy_vol  = 0.0
            self.state._tick_sell_vol = 0.0
            self.state.buy_vol_5s.append(buy_v)
            self.state.sell_vol_5s.append(sell_v)

            # Running CVD: add net delta to previous value
            prev_cvd = self.state.cvd_5s[-1] if self.state.cvd_5s else 0.0
            new_cvd = prev_cvd + buy_v - sell_v
            self.state.cvd_5s.append(new_cvd)

            # Persist price + volume snapshot
            if self.state.btc_price is not None:
                self.state.logger.log_price(
                    btc_price=self.state.btc_price,
                    buy_vol=buy_v,
                    sell_vol=sell_v,
                    cvd=new_cvd,
                    up_odds=self.state.up_odds,
                    down_odds=self.state.down_odds,
                )
                self.state.price_tick_log.append((
                    datetime.now(_UTC),
                    self.state.btc_price,
                    buy_v,
                    sell_v,
                    new_cvd,
                    self.state.up_odds,
                    self.state.down_odds,
                ))

    # ── Market discovery loop ─────────────────────────────────────────────────

    async def _market_loop(self) -> None:
        while self.state.running:
            win = await self.market.find_active_window()

            if win is None:
                if self.state.window is not None:
                    self.state.log_event("[MKT] Window ended, searching for next…")
                    self.state.window = None
                    self.state.up_odds = None
                    self.state.down_odds = None
                    self.state.last_signal = None   # clear signal so UI shows "No signal yet"
                await asyncio.sleep(10)
                continue

            # New window detected
            if (self.state.window is None or
                    win.condition_id != self.state.window.condition_id):
                # beat_price: use the BTC price closest to the window's actual start time.
                # Capturing the CURRENT price causes a ~$20-35 error because:
                #   a) detection delay (bot polls every 5s, window may be 5-10s old)
                #   b) BTC may have moved significantly since window opened
                if win.beat_price == 0.0:
                    start_ts = win.start_time.timestamp()
                    history_ts = list(self.state.price_history_ts)
                    if history_ts:
                        closest = min(history_ts, key=lambda x: abs(x[0] - start_ts))
                        # Only use if within 60 seconds of window start (avoids stale data)
                        if abs(closest[0] - start_ts) < 60:
                            win.beat_price = closest[1]
                    if win.beat_price == 0.0 and self.state.btc_price:
                        win.beat_price = self.state.btc_price
                self.state.window = win
                self.state.window_found_at = time.time()
                self.state.last_signal = None   # clear stale signal from previous window
                self.state.last_pre_ai_decision = None
                self.state.last_trade_decision = None
                self.state.latest_fair_prob = {}
                self.state.latest_beat_chop = {}
                self.state.set_engine_status("NEW_WINDOW", reason="monitoring new window")
                # Only reset the attempt budget for a genuinely NEW window.
                # If this window's condition_id was already attempted, keep the guard
                # so a transient API hiccup (window briefly None then re-detected)
                # cannot produce a second bet on the same window.
                if win.condition_id not in self.state.bet_attempted_windows:
                    self.state.bet_attempted_windows.clear()  # fresh window, fresh attempt budget
                self.state.market_resolved_event.clear()
                self.notifier.notify_window(win)
                self.state.log_event(
                    f"[MKT] Window: {win.question[:55]} | "
                    f"beat=${win.beat_price:,.2f} | ends {win.end_time.strftime('%H:%M:%S UTC')}"
                )
            elif self.state.window.beat_price == 0.0 and self.state.btc_price:
                # Retroactive fallback: BTC feed wasn't ready at detection time
                start_ts = self.state.window.start_time.timestamp()
                history_ts = list(self.state.price_history_ts)
                beat = self.state.btc_price
                if history_ts:
                    closest = min(history_ts, key=lambda x: abs(x[0] - start_ts))
                    if abs(closest[0] - start_ts) < 60:
                        beat = closest[1]
                self.state.window.beat_price = beat
                self.state.log_event(f"[MKT] Beat price set retroactively: ${beat:,.2f}")

            # Poll odds every 5s as REST fallback (WS takes priority when connected).
            # Skip the update if REST returns the error-fallback 0.500/0.500 — that
            # would overwrite valid WebSocket odds with a stale default.
            if win.up_token_id and win.down_token_id:
                up, dn = await self.market.get_odds(win.up_token_id, win.down_token_id)
                if up > 0 and not (abs(up - 0.5) < 0.001 and abs(dn - 0.5) < 0.001):
                    self.state.up_odds = up
                    self.state.down_odds = dn
                    self.state.odds_updated_at = time.time()

            await asyncio.sleep(5)

    # ── Odds WebSocket loop ───────────────────────────────────────────────────

    async def _odds_ws_loop(self) -> None:
        """Subscribe to market WS; re-subscribe when the window changes.

        subscribe_market_ws() exits when the window's condition_id changes,
        so this outer loop naturally picks up each new window.
        """
        while self.state.running:
            win = self.state.window
            if win is None:
                await asyncio.sleep(2)
                continue
            # Blocks until window changes or bot stops
            await self.market.subscribe_market_ws(
                win.up_token_id, win.down_token_id, self.state, win.condition_id
            )

    # ── Trading loop ──────────────────────────────────────────────────────────

    async def _trading_loop(self) -> None:
        while self.state.running:
            await asyncio.sleep(SIGNAL_COOLDOWN_S)
            now = time.time()

            prices    = list(self.state.price_history_5s)
            buy_vols  = list(self.state.buy_vol_5s)
            sell_vols = list(self.state.sell_vol_5s)
            cvd_ser   = list(self.state.cvd_5s)

            # ── PHASE 1: FILTER MONITORING (runs every 10s throughout full window)
            # Filters computed continuously so the UI always shows live F1-F5 status.
            # AI is NOT queried here — signal only fires in the gold zone (Phase 2).
            # ─────────────────────────────────────────────────────────────────────

            win = self.state.window
            elapsed_for_snap = int((datetime.now(_UTC) - win.start_time).total_seconds()) \
                               if win else 9999

            if self.state.btc_price and len(prices) >= 21:
                up_odds_snap   = self.state.up_odds   or 0.5
                down_odds_snap = self.state.down_odds or 0.5
                if not (0.85 <= up_odds_snap + down_odds_snap <= 1.15):
                    up_odds_snap = down_odds_snap = 0.5
                snap_display = run_all_filters(
                    prices, up_odds_snap, down_odds_snap, elapsed_for_snap,
                    buy_vols=buy_vols, sell_vols=sell_vols, cvd_series=cvd_ser,
                    odds_history=list(self.state.odds_history),
                )
                self.state.indicator_snapshot = snap_display
                self.state.last_filter_time = now


            # ── PHASE 2: BET EXECUTION (last minute only — elapsed 240–285s)
            # All bet guards and order placement live here.
            # ─────────────────────────────────────────────────────────────────────

            # Minimum requirements to even consider a bet
            win = self.state.window
            if win is None:
                self.state.set_engine_status("NO_WINDOW", reason="searching for active market")
                continue
            if self.state.btc_price is None:
                self.state.set_engine_status("WAIT_BTC", reason="waiting for BTC feed")
                continue
            if self.state.up_odds is None or self.state.down_odds is None:
                self.state.set_engine_status("WAIT_ODDS", reason="waiting for Polymarket odds")
                continue
            if not (0.85 <= self.state.up_odds + self.state.down_odds <= 1.15):
                odds_sum = self.state.up_odds + self.state.down_odds
                self.state.set_engine_status(
                    "ODDS_DESYNC",
                    reason=(
                        f"odds snapshot not synchronized yet "
                        f"(UP={self.state.up_odds:.3f} DN={self.state.down_odds:.3f} "
                        f"sum={odds_sum:.3f}, expected near 1.000)"
                    ),
                )
                continue

            # Daily limits reset at midnight UTC
            today = datetime.now(_UTC).strftime("%Y-%m-%d")
            if self.state.daily_day != today:
                self.state.daily_day = today
                self.state.daily_loss = 0.0
                self.state.daily_profit = 0.0
                self.state.daily_halted = False
                self.state.daily_profit_halted = False
                self.state.paper_stats.reset_today()
                self.state.log_event(f"[BOT] Daily limits reset for {today}")

            if DAILY_BUDGET_USDC > 0:
                net_loss = self.state.daily_loss - self.state.daily_profit
                if net_loss >= DAILY_BUDGET_USDC:
                    if not self.state.daily_halted:
                        self.state.daily_halted = True
                        msg = (f"[HALT] Daily net loss limit ${DAILY_BUDGET_USDC:.2f} reached "
                               f"(net loss ${net_loss:.2f} today) — no new bets until midnight UTC")
                        self.state.log_event(msg)
                    self.state.set_engine_status("HALT_DAILY_LOSS", reason="daily loss limit reached")
                    continue

            if DAILY_PROFIT_TARGET_USDC > 0 and self.state.daily_profit >= DAILY_PROFIT_TARGET_USDC:
                if not self.state.daily_profit_halted:
                    self.state.daily_profit_halted = True
                    msg = (f"[HALT] Daily profit target ${DAILY_PROFIT_TARGET_USDC:.2f} reached "
                           f"(earned ${self.state.daily_profit:.2f} today) — no new bets until midnight UTC")
                    self.state.log_event(msg)
                self.state.set_engine_status("HALT_DAILY_PROFIT", reason="daily profit target reached")
                continue

            if now - self.state.hour_reset_at > 3600:
                self.state.bets_this_hour = 0
                self.state.hour_reset_at = now

            if self.state.bets_this_hour >= MAX_BETS_PER_HOUR:
                self.state.set_engine_status("RATE_LIMIT", reason="max bets per hour reached")
                continue

            # Streak halt: pause all bets after N consecutive losses
            if now < self.state.streak_pause_until:
                remaining_m = (self.state.streak_pause_until - now) / 60
                self.state.log_event(
                    f"[STREAK_PAUSE] {remaining_m:.0f}m remaining on {self.state.consecutive_losses}-loss halt"
                )
                self.state.set_engine_status("STREAK_PAUSE", reason=f"{remaining_m:.0f}m remaining")
                continue

            if LIVE_TRADING and self.state.balance_usdc < BET_SIZE_USDC + 0.50:
                self.state.set_engine_status("LOW_BALANCE", reason="insufficient balance for next live order")
                continue

            now_utc = datetime.now(_UTC)
            elapsed_s = int((now_utc - win.start_time).total_seconds())
            seconds_remaining = int((win.end_time - now_utc).total_seconds())

            fair_display = compute_fair_probability(
                btc_price=self.state.btc_price,
                beat_price=win.beat_price,
                seconds_remaining=max(0, seconds_remaining),
                price_history_5s=prices,
            )
            if self.state.up_odds is not None and self.state.down_odds is not None:
                fair_display["edge_up"] = compute_edge(fair_display["fair_up"], self.state.up_odds)
                fair_display["edge_down"] = compute_edge(fair_display["fair_down"], self.state.down_odds)
            self.state.latest_fair_prob = fair_display
            self.state.latest_beat_chop = compute_beat_chop_metrics(prices, win.beat_price)

            # ── Last-minute gate: betting only in final 60 seconds ────────────
            if elapsed_s < GOLD_ZONE_START_S:
                self.state.last_pre_ai_decision = None
                self.state.last_trade_decision = None
                self.state.set_engine_status(
                    "WAIT_GOLD_ZONE",
                    reason=f"elapsed={elapsed_s}s < {GOLD_ZONE_START_S}s start",
                )
                continue   # signal is running (Phase 1), but no bet yet

            if seconds_remaining < LAST_MIN_SECONDS_GUARD:
                self.state.set_engine_status(
                    "TOO_LATE",
                    reason=f"seconds_remaining={seconds_remaining}s < {LAST_MIN_SECONDS_GUARD}s guard",
                )
                continue   # too close to expiry for order to settle

            # One bet per window — check both successful positions AND failed attempts.
            # This prevents retrying after a failed placement where the CLOB may
            # have already accepted the order (partial network failure, timeout, etc.).
            bet_ids = (
                {p.condition_id for p in self.state.open_positions}
                | self.state.bet_attempted_windows
            )
            if win.condition_id in bet_ids:
                self.state.set_engine_status("ALREADY_ATTEMPTED", reason="bet already attempted in this window")
                continue

            # Re-capture data fresh — prices/volumes at loop top are up to
            # SIGNAL_COOLDOWN_S (10s) stale by the time Phase 2 runs.
            prices_now    = list(self.state.price_history_5s)
            buy_vols_now  = list(self.state.buy_vol_5s)
            sell_vols_now = list(self.state.sell_vol_5s)
            cvd_ser_now   = list(self.state.cvd_5s)
            btc_price_now = self.state.btc_price
            up_odds_now   = self.state.up_odds
            down_odds_now = self.state.down_odds

            if btc_price_now is None:
                self.state.set_engine_status("WAIT_BTC", reason="waiting for BTC feed")
                continue
            if up_odds_now is None or down_odds_now is None:
                self.state.set_engine_status("WAIT_ODDS", reason="waiting for Polymarket odds")
                continue

            snap = run_all_filters(
                prices_now,
                up_odds_now,
                down_odds_now,
                elapsed_s,
                buy_vols=buy_vols_now,
                sell_vols=sell_vols_now,
                cvd_series=cvd_ser_now,
                odds_history=list(self.state.odds_history),
            )
            self.state.indicator_snapshot = snap
            self.state.last_filter_time = now

            # ── Brownian fair-value model (pre-AI edge gate) ─────────────────
            fair = compute_fair_probability(
                btc_price=btc_price_now,
                beat_price=win.beat_price,
                seconds_remaining=seconds_remaining,
                price_history_5s=prices_now,
            )
            fair["edge_up"]   = compute_edge(fair["fair_up"],   up_odds_now)
            fair["edge_down"] = compute_edge(fair["fair_down"], down_odds_now)
            beat_chop = compute_beat_chop_metrics(prices_now, win.beat_price)
            self.state.latest_fair_prob = fair
            self.state.latest_beat_chop = beat_chop

            # ── Pre-AI market gates (via DecisionMaker) ──────────────────────
            ctx = DecisionContext(
                win=win,
                elapsed_s=elapsed_s,
                seconds_remaining=seconds_remaining,
                btc_price=btc_price_now,
                up_odds=up_odds_now,
                down_odds=down_odds_now,
                snap=snap,
                dip_label="UNKNOWN",  # updated below after AI call
                signal_alignment=snap.signal_alignment,
                beat_crossings=beat_chop["crossings"],
                beat_above_ratio=beat_chop["above_ratio"],
                beat_below_ratio=beat_chop["below_ratio"],
                max_odds_threshold=GATE_TOO_SURE_THRESHOLD,
                fair_prob=fair,
            )
            pre = self.decision.pre_ai_check(ctx)
            if pre is not None:
                self.state.last_pre_ai_decision = pre
                self.state.last_trade_decision = pre
                self.state.set_engine_status("PRE_AI_SKIP", pre.gate, pre.reason)
                self.state.log_event(
                    f"[{pre.gate}] SKIP — {pre.reason}"
                )
                async with self.state._lock:
                    self.state.blocked_windows.append(BlockedWindow(
                        window_label=win.window_label,
                        beat_price=win.beat_price,
                        skip_reason=f"{pre.gate}: {pre.reason}",
                        suggested_direction=pre.direction,
                    ))
                continue

            ai_warnings = self.decision.ai_context_warnings(ctx)

            # ── AI decision (fresh call, last-minute context) ─────────────────
            is_btc_above = btc_price_now > win.beat_price
            leading_odds = up_odds_now if is_btc_above else down_odds_now
            gap_pct = abs(btc_price_now - win.beat_price) / win.beat_price * 100
            side = "UP" if is_btc_above else "DOWN"
            self.state.log_event(
                f"[LAST-MIN] {elapsed_s}s | BTC {gap_pct:.2f}% → {side} "
                f"@ {leading_odds:.3f} | align={snap.signal_alignment} "
                f"CVD={snap.cvd_divergence} | querying AI…"
            )
            self.state.set_engine_status("AI_QUERY", reason="querying AI with gold-zone context")
            signal = await self.ai.get_signal(
                btc_price=btc_price_now,
                beat_price=win.beat_price,
                up_odds=up_odds_now,
                down_odds=down_odds_now,
                rsi=snap.rsi,
                ma_short=snap.ma_short,
                ma_long=snap.ma_long,
                momentum_pct=snap.momentum_pct,
                seconds_remaining=max(0, seconds_remaining),
                elapsed_s=elapsed_s,
                recent_prices=prices_now[-20:],
                macd_histogram=snap.macd_histogram,
                bb_pct_b=snap.bb_pct_b,
                vwap=snap.vwap,
                cvd_divergence=snap.cvd_divergence,
                signal_alignment=snap.signal_alignment,
                is_gold_zone=True,
                odds_vel={
                    "vel":       snap.odds_vel_value,
                    "direction": snap.odds_vel_direction,
                    "acceleration": snap.odds_vel_accel,
                },
                beat_crossings=beat_chop["crossings"],
                beat_above_ratio=beat_chop["above_ratio"],
                beat_below_ratio=beat_chop["below_ratio"],
                market_warnings=ai_warnings,
                fair_prob=fair,
                window_history=list(self.state.recent_window_outcomes),
                consecutive_losses=self.state.consecutive_losses,
            )
            if signal.signal in ("BUY_UP", "BUY_DOWN"):
                chosen_odds = up_odds_now if signal.signal == "BUY_UP" else down_odds_now
                calibrated = self._calibrate_signal_confidence(
                    raw_confidence=signal.confidence,
                    direction="UP" if signal.signal == "BUY_UP" else "DOWN",
                    entry_odds=chosen_odds or 0.0,
                    alignment=snap.signal_alignment,
                )
                signal.raw_confidence = signal.confidence
                if abs(calibrated - signal.confidence) >= 0.001:
                    self.state.log_event(
                        f"[CONF] raw={signal.confidence:.2f} → cal={calibrated:.2f} "
                        f"dir={'UP' if signal.signal == 'BUY_UP' else 'DOWN'} "
                        f"odds={(chosen_odds or 0.0):.3f} align={snap.signal_alignment}"
                    )
                signal.confidence = calibrated
            else:
                signal.raw_confidence = signal.confidence
            self.state.last_signal = signal
            self.state.set_engine_status("AI_DONE", reason=f"{signal.signal} conf={signal.confidence:.0%}")
            self.state.log_event(
                f"[AI/BET] {signal.signal} conf={signal.confidence:.2f} | {signal.reason[:60]}"
            )
            self.state.logger.log_signal(
                signal,
                elapsed_s=elapsed_s,
                up_odds=up_odds_now,
                down_odds=down_odds_now,
                btc_price=btc_price_now,
                beat_price=win.beat_price,
                is_gold_zone=True,
                alignment=snap.signal_alignment,
                cvd_divergence=snap.cvd_divergence,
                condition_id=win.condition_id,
            )

            # ── Full evaluation with AI signal (via DecisionMaker) ────────────
            ctx.ai_signal   = signal
            ctx.dip_label   = signal.dip_label
            ctx.signal_alignment = snap.signal_alignment
            decision = self.decision.evaluate(ctx)
            self.state.last_trade_decision = decision
            self.state.set_engine_status(
                "BUY_READY" if decision.action == "BUY" else "DECISION_SKIP",
                decision.gate,
                decision.reason,
            )
            self.state.log_event(
                f"[DECISION] {decision.action} gate={decision.gate} "
                f"conf={decision.confidence:.0%} dir={decision.direction} | {decision.reason}"
            )
            self.notifier.notify_ai_signal(
                signal,
                win,
                snap,
                btc_price=btc_price_now,
                up_odds=up_odds_now,
                down_odds=down_odds_now,
                decision=decision,
            )

            if signal.signal in ("BUY_UP", "BUY_DOWN"):
                await self._upsert_paper_prediction(
                    win,
                    signal,
                    snap,
                    decision_action="paper_trade" if decision.action == "BUY" else "blocked",
                )

            if decision.action != "BUY":
                async with self.state._lock:
                    self.state.blocked_windows.append(BlockedWindow(
                        window_label=win.window_label,
                        beat_price=win.beat_price,
                        skip_reason=f"{decision.gate}: {decision.reason}",
                        suggested_direction=decision.direction,
                    ))
                continue

            # Mark as attempted BEFORE placement — prevents retrying this window
            # even if the order call fails/times out after the CLOB accepted it.
            async with self.state._lock:
                self.state.bet_attempted_windows.add(win.condition_id)

            await self._place_trade(win, signal, snap, prices_now, is_gold_zone=True)

    async def _place_trade(
        self,
        win,
        signal: "AISignal",
        snap: "IndicatorSnapshot",
        prices: list[float],
        is_gold_zone: bool = False,
    ) -> None:
        """Execute a trade with Kelly-sized position and log the result."""
        direction  = "UP" if signal.signal == "BUY_UP" else "DOWN"
        token_id   = win.up_token_id if direction == "UP" else win.down_token_id
        entry_odds = self.state.up_odds if direction == "UP" else self.state.down_odds
        if entry_odds is None or entry_odds <= 0:
            self.state.log_event(f"[TRADE] Aborted — entry_odds unavailable ({entry_odds})")
            return

        # ── Fractional Kelly position sizing (share_1.md insight) ────────────
        # In live mode use real balance; in paper mode use simulated bankroll.
        bankroll = (
            self.state.balance_usdc
            if (LIVE_TRADING and self.state.balance_usdc > 1.0)
            else PAPER_BANKROLL_USDC
        )
        bet_size = compute_kelly_size(
            confidence=signal.confidence,
            implied_odds=entry_odds,
            bankroll=bankroll,
            max_bet=BET_SIZE_USDC,
            consecutive_losses=self.state.consecutive_losses,
        )
        zone_tag = "GOLD" if is_gold_zone else "NORM"
        self.state.log_event(
            f"[KELLY/{zone_tag}] bankroll=${bankroll:.2f} conf={signal.confidence:.2f} "
            f"implied={entry_odds:.3f} → bet=${bet_size:.2f}"
        )

        result: TradeResult = await self.market.place_bet(
            direction, token_id, bet_size, entry_odds
        )

        if result.success:
            now_utc     = datetime.now(_UTC)
            actual_price = result.price if result.price and result.price > 0 else entry_odds
            actual_amount = result.amount_usdc if result.amount_usdc and result.amount_usdc > 0 else bet_size
            actual_size = result.size if result.size and result.size > 0 else (actual_amount / actual_price)
            elapsed_bet = int((now_utc - win.start_time).total_seconds())
            gap_pct_bet = (
                abs(self.state.btc_price - win.beat_price) / win.beat_price * 100
                if win.beat_price > 0 and self.state.btc_price else 0.0
            )
            pos = Position(
                condition_id=win.condition_id,
                direction=direction,
                token_id=token_id,
                size=actual_size,
                entry_price=actual_price,
                placed_at=datetime.now(),
                order_id=result.order_id or "",
                simulated=result.simulated,
                amount_usdc=actual_amount,
                window_beat=win.beat_price,
                window_end_at=win.end_time,
                elapsed_at_bet=elapsed_bet,
                gap_pct_at_bet=gap_pct_bet,
                ai_confidence=signal.confidence,
                ai_raw_confidence=signal.raw_confidence or signal.confidence,
                signal_alignment=snap.signal_alignment,
            )
            async with self.state._lock:
                self.state.positions.append(pos)
            self.state.bets_this_hour += 1
            if pos.simulated:
                await self._attach_paper_trade_to_prediction(pos)
            self.state.logger.log_trade_open(pos, window_question=win.question)
            mode = "PAPER" if result.simulated else "LIVE"
            if abs(actual_amount - bet_size) >= 0.01:
                self.state.log_event(
                    f"[ORDER] Exchange minimum size adjusted spend from ${bet_size:.2f} "
                    f"to ${actual_amount:.2f}"
                )
            self.state.log_event(
                f"[{mode}/{zone_tag}] BET {direction} ${actual_amount:.2f} @ {actual_price:.3f} "
                f"align={snap.signal_alignment} CVD={snap.cvd_divergence} "
                f"| order={result.order_id}"
            )
            self.state.set_engine_status("ORDER_OPEN", reason=f"{direction} @ {actual_price:.3f} order={result.order_id}")
            self.notifier.notify_bet(
                direction, actual_amount, actual_price, win,
                result.order_id or "—", result.simulated, snap,
            )
        else:
            self.state.set_engine_status("ORDER_FAILED", reason=str(result.error or "unknown placement failure"))
            self.state.log_event(f"[TRADE] Order failed: {result.error}")

    # ── Position monitor loop ─────────────────────────────────────────────────

    async def _position_monitor_loop(self) -> None:
        """Monitor open live orders and cancel if conditions deteriorate.

        Runs every POSITION_MONITOR_INTERVAL_S seconds.
        Only acts on live (non-simulated) orders for the current active window.

        Cancel triggers (any one sufficient):
        - Opposite side has become a near-certainty (CANCEL_ODDS_THRESHOLD)
        - Our side odds have fully collapsed
        - Confidence dropped below cancel floor (opt-in via CANCEL_ON_CONF_DROP)
        """
        while self.state.running:
            await asyncio.sleep(POSITION_MONITOR_INTERVAL_S)

            win = self.state.window
            if win is None:
                continue

            now_utc = datetime.now(_UTC)
            if now_utc >= win.end_time:
                continue   # window resolved — _results_loop handles settlement

            seconds_remaining = int((win.end_time - now_utc).total_seconds())

            async with self.state._lock:
                open_positions = [
                    p for p in self.state.positions
                    if p.status == "open"
                    and not p.simulated
                    and p.condition_id == win.condition_id
                ]

            for pos in open_positions:
                # Skip if order is already matched / gone on the CLOB
                order = await self.market.get_order(pos.order_id)
                if not order:
                    continue  # network error — can't determine status, skip safely
                order_status = order.get("status", "LIVE")
                if order_status != "LIVE":
                    continue

                up_odds   = self.state.up_odds   or 0.5
                down_odds = self.state.down_odds or 0.5

                # Optional: re-query AI confidence before canceling
                fresh_conf: float | None = None
                if CANCEL_ON_CONF_DROP and self.state.indicator_snapshot:
                    snap = self.state.indicator_snapshot
                    prices = list(self.state.price_history_5s)
                    elapsed_s = int((now_utc - win.start_time).total_seconds())
                    try:
                        fresh_signal = await self.ai.get_signal(
                            btc_price=self.state.btc_price or 0,
                            beat_price=win.beat_price,
                            up_odds=up_odds,
                            down_odds=down_odds,
                            rsi=snap.rsi,
                            ma_short=snap.ma_short,
                            ma_long=snap.ma_long,
                            momentum_pct=snap.momentum_pct,
                            seconds_remaining=seconds_remaining,
                            elapsed_s=elapsed_s,
                            recent_prices=prices[-20:],
                            macd_histogram=snap.macd_histogram,
                            bb_pct_b=snap.bb_pct_b,
                            vwap=snap.vwap,
                            cvd_divergence=snap.cvd_divergence,
                            signal_alignment=snap.signal_alignment,
                            is_gold_zone=True,
                        )
                        fresh_conf = fresh_signal.confidence
                    except Exception:
                        pass  # AI failure must not block the monitor loop

                should_cancel, reason = self.decision.should_cancel(
                    pos=pos,
                    current_up_odds=up_odds,
                    current_down_odds=down_odds,
                    seconds_remaining=seconds_remaining,
                    current_confidence=fresh_conf,
                    current_btc_price=self.state.btc_price,
                    beat_price=win.beat_price,
                )

                if not should_cancel:
                    continue

                self.state.log_event(
                    f"[CANCEL] Pulling order={pos.order_id} dir={pos.direction} | {reason}"
                )
                ok, cancel_reason = await self.market.cancel_order(pos.order_id)
                short_id = pos.order_id[:20] + "…"
                if ok:
                    await self._mark_position_canceled(
                        pos,
                        f"order {pos.order_id} canceled successfully before fill",
                    )
                else:
                    # Re-query actual CLOB status to determine correct action
                    recheck = await self.market.get_order(pos.order_id)
                    recheck_status = recheck.get("status", "") if recheck else ""
                    if recheck_status == "MATCHED":
                        self.state.log_event(
                            f"[CANCEL] {short_id} already MATCHED — will settle at window expiry"
                        )
                        # pos.status stays "open"; _check_positions will settle it
                    elif recheck_status in ("CANCELED", "CANCELED_MARKET_RESOLVED"):
                        await self._mark_position_canceled(
                            pos,
                            f"{short_id} already canceled by exchange before fill",
                        )
                    else:
                        self.state.log_event(
                            f"[CANCEL] Could not cancel {short_id} — "
                            f"api='{cancel_reason}' status={recheck_status or 'unknown'} — will retry"
                        )

    # ── Results loop ──────────────────────────────────────────────────────────

    async def _results_loop(self) -> None:
        while self.state.running:
            await asyncio.sleep(60)
            await self._check_positions()
            await self._resolve_paper_predictions()
            await self._resolve_blocked_windows()

    async def _check_positions(self) -> None:
        async with self.state._lock:
            open_positions = [p for p in self.state.positions if p.status == "open"]

        for pos in open_positions:
            beat   = pos.window_beat if pos.window_beat > 0 else 0
            amount = pos.amount_usdc if pos.amount_usdc > 0 else BET_SIZE_USDC
            settlement_btc = self._get_settlement_btc(pos)

            # ── Simulated positions ───────────────────────────────────────────
            # Resolve when the window they were placed in has ended.
            if pos.simulated:
                if not self._position_window_has_ended(pos):
                    continue
                # Window over (or we're in a new window) — evaluate outcome
                if settlement_btc is None or beat <= 0:
                    continue
                btc_up = settlement_btc > beat
                won = (pos.direction == "UP" and btc_up) or \
                      (pos.direction == "DOWN" and not btc_up)
                await self._settle_position(pos, won, amount)
                continue

            # ── Live orders — verify via CLOB GET /order/{orderID} ───────────
            # Only resolve once the window has ended (order may match instantly
            # via FOK, but the payout is determined at expiry).
            if not self._position_window_has_ended(pos):
                continue

            order = await self.market.get_order(pos.order_id)
            order_status = (order.get("status", "") if order else "").upper()

            # MATCHED = order was filled on the CLOB
            if order_status in ("CANCELED", "CANCELED_MARKET_RESOLVED"):
                await self._mark_position_canceled(
                    pos,
                    f"exchange returned {order_status} after window end",
                )
                continue

            matched = order_status in ("MATCHED", "ORDER_STATUS_MATCHED")
            if not matched:
                trades = await self.market.get_recent_trades()
                trade = next(
                    (t for t in trades
                     if t.condition_id == pos.condition_id
                     and t.direction == pos.direction
                     and t.status in ("CONFIRMED", "MATCHED", "MINED")),
                    None,
                )
                if trade is None:
                    continue
                matched = True

            if not matched or settlement_btc is None or beat <= 0:
                continue
            btc_up = settlement_btc > beat
            won = (pos.direction == "UP" and btc_up) or \
                  (pos.direction == "DOWN" and not btc_up)
            await self._settle_position(pos, won, amount)

    async def _settle_position(self, pos: "Position", won: bool, amount: float) -> None:
        """Apply win/loss to a position and fire all downstream notifications."""
        async with self.state._lock:
            pos.status = "won" if won else "lost"
            pos.pnl    = (amount * (1.0 / pos.entry_price - 1)) if won else -amount
            if won:
                self.state.win_count       += 1
                self.state.total_pnl       += pos.pnl or 0
                self.state.daily_profit    += pos.pnl or 0
                self.state.consecutive_wins   += 1
                self.state.consecutive_losses  = 0
                # Un-halt if profit brought net loss back below the limit
                if (self.state.daily_halted and DAILY_BUDGET_USDC > 0
                        and (self.state.daily_loss - self.state.daily_profit) < DAILY_BUDGET_USDC):
                    self.state.daily_halted = False
                    self.state.log_event(
                        f"[BOT] Halt lifted — net loss now "
                        f"${self.state.daily_loss - self.state.daily_profit:.2f} "
                        f"(profit restored budget)"
                    )
            else:
                self.state.loss_count         += 1
                self.state.total_pnl          += pos.pnl or 0
                self.state.daily_loss         += amount
                self.state.consecutive_losses += 1
                self.state.consecutive_wins    = 0
                if self.state.consecutive_losses >= STREAK_HALT_COUNT:
                    self.state.streak_pause_until = time.time() + (STREAK_PAUSE_MIN * 60)
                    self.state.log_event(
                        f"[STREAK_HALT] {self.state.consecutive_losses} consecutive losses — "
                        f"pausing bets for {STREAK_PAUSE_MIN}min"
                    )

            # Record for AI historical context
            self.state.recent_window_outcomes.append({
                "elapsed_at_bet": pos.elapsed_at_bet,
                "gap_pct":        pos.gap_pct_at_bet,
                "direction":      pos.direction,
                "won":            won,
                "odds":           pos.entry_price,
                "confidence":     pos.ai_confidence,
                "raw_confidence": pos.ai_raw_confidence,
                "alignment":      pos.signal_alignment,
            })
            paper_record = None
            if pos.simulated:
                self.state.paper_stats.record_paper_trade(won)
                paper_record = self.state.paper_prediction_records.get(pos.condition_id)
                if paper_record is not None:
                    paper_record.paper_trade_won = won
                    paper_record.simulated_order_id = pos.order_id or paper_record.simulated_order_id
                    paper_record.last_updated_at = datetime.now(_UTC)
            self.state.resolved_count += 1

        self.state.log_event(
            f"[RESULT] {pos.direction} {'WON' if won else 'LOST'} PnL={pos.pnl:+.2f}"
        )
        self.state.logger.log_trade_close(pos)
        if pos.simulated:
            self.state.logger.log_paper_trade_resolved(pos, won)
            if paper_record is not None and paper_record.prediction_correct is None:
                self.state.logger.log_paper_prediction_state(paper_record)
        self.notifier.notify_result(pos, self.state)

        winnings = pos.pnl or 0
        if won and winnings >= AUTO_CLAIM_THRESHOLD:
            msg = f"claim pending ${winnings:.2f} ({pos.condition_id[:8]}…)"
            self.state.claim_log.append(
                f"{datetime.now().strftime('%H:%M:%S')} {msg}"
            )
            self.state.log_event(f"[CLAIM] {msg}")

    async def _mark_position_canceled(self, pos: "Position", reason: str) -> None:
        async with self.state._lock:
            if pos.status != "open":
                return
            pos.status = "canceled"
            pos.pnl = 0.0

        self.state.log_event(f"[CANCEL] {reason}")
        self.state.logger.log_trade_close(pos)

    async def _resolve_paper_predictions(self) -> None:
        """Resolve one final BUY prediction per window in paper mode."""
        if LIVE_TRADING:
            return

        async with self.state._lock:
            pending = [
                rec for rec in self.state.paper_prediction_records.values()
                if rec.prediction_correct is None
                and rec.predicted_direction in ("UP", "DOWN")
                and rec.window_end_at is not None
            ]

        now_utc = datetime.now(_UTC)
        for record in pending:
            if record.window_end_at is None or now_utc < record.window_end_at:
                continue

            settlement_btc = self._get_settlement_btc_for_window(
                condition_id=record.condition_id,
                window_end_at=record.window_end_at,
            )
            if settlement_btc is None or record.beat_price <= 0:
                continue

            actual_winner = "UP" if settlement_btc > record.beat_price else "DOWN"
            correct = record.predicted_direction == actual_winner
            resolved_at = datetime.now(_UTC)

            async with self.state._lock:
                current = self.state.paper_prediction_records.get(record.condition_id)
                if current is None or current.prediction_correct is not None:
                    continue
                current.actual_winner = actual_winner
                current.prediction_correct = correct
                current.resolved_at = resolved_at
                current.last_updated_at = resolved_at
                self.state.paper_stats.record_prediction(correct)
                record_to_log = current

            self.state.logger.log_paper_prediction_resolved(record_to_log)
            self.state.log_event(
                f"[PAPER] Prediction {record_to_log.predicted_direction} "
                f"{'HIT' if correct else 'MISS'} | actual={actual_winner} "
                f"window={record_to_log.window_label}"
            )

    async def _resolve_blocked_windows(self) -> None:
        """Retroactively evaluate skipped windows against actual BTC outcome."""
        win = self.state.window
        if not win or self.state.btc_price is None:
            return

        now = datetime.now(_UTC)
        if now < win.end_time:
            return  # window still open

        btc_up = self.state.btc_price > win.beat_price

        async with self.state._lock:
            for bw in self.state.blocked_windows:
                if bw.would_have_won is not None:
                    continue
                if bw.window_label != win.window_label:
                    continue
                bw.final_btc_price = self.state.btc_price
                if bw.suggested_direction == "NONE":
                    bw.would_have_won = None
                    continue
                bet_up = bw.suggested_direction == "UP"
                # would_have_won=True means the SKIP was a mistake (missed profit)
                # would_have_won=False means the SKIP was correct (avoided loss)
                bw.would_have_won = (bet_up and btc_up) or (not bet_up and not btc_up)

    @staticmethod
    def _recover_key(condition_id: str, direction: str) -> tuple[str, str]:
        return (condition_id.strip(), direction.strip().upper())

    @staticmethod
    def _extract_order_id(payload: dict) -> str:
        return str(
            payload.get("orderID")
            or payload.get("order_id")
            or payload.get("id")
            or ""
        ).strip()

    async def _recover_open_positions(self) -> tuple[int, int]:
        recovered = 0
        skipped = 0
        existing_ids = {p.order_id for p in self.state.positions if p.order_id}
        unresolved = self.state.logger.load_unsettled_trades()

        live_open_order_ids: set[str] = set()
        matched_trade_keys: set[tuple[str, str]] = set()
        if LIVE_TRADING:
            open_orders, recent_trades = await asyncio.gather(
                self.market.get_user_orders(),
                self.market.get_recent_trades(),
            )
            for order in open_orders:
                if isinstance(order, dict):
                    order_id = self._extract_order_id(order)
                    if order_id:
                        live_open_order_ids.add(order_id)
            for trade in recent_trades:
                status = str(getattr(trade, "status", "")).upper()
                if status in ("CONFIRMED", "MATCHED", "MINED"):
                    matched_trade_keys.add(
                        self._recover_key(
                            str(getattr(trade, "condition_id", "")),
                            str(getattr(trade, "direction", "")),
                        )
                    )

        for record in unresolved:
            simulated = bool(record.get("simulated", False))
            # Do not mix paper/live recovery across sessions.
            if LIVE_TRADING and simulated:
                skipped += 1
                continue
            if not LIVE_TRADING and not simulated:
                skipped += 1
                continue

            order_id = str(record.get("order_id", "")).strip()
            if order_id and order_id in existing_ids:
                continue

            if LIVE_TRADING and not simulated:
                order_status = ""
                if order_id:
                    order = await self.market.get_order(order_id)
                    if isinstance(order, dict):
                        order_status = str(order.get("status", "")).upper()

                record_key = self._recover_key(
                    str(record.get("condition_id", "")),
                    str(record.get("direction", "")),
                )
                has_account_evidence = (
                    order_id in live_open_order_ids
                    or order_status in ("LIVE", "MATCHED", "ORDER_STATUS_MATCHED")
                    or record_key in matched_trade_keys
                )
                if not has_account_evidence:
                    skipped += 1
                    continue

            placed_at = self._parse_logged_datetime(record.get("placed_at")) or datetime.now()
            window_end_at = (
                self._parse_logged_datetime(record.get("window_end_at"))
                or self._infer_window_end(placed_at)
            )

            pos = Position(
                condition_id=str(record.get("condition_id", "")),
                direction=str(record.get("direction", "NONE")),
                token_id=str(record.get("token_id", "")),
                size=float(record.get("size", 0.0) or 0.0),
                entry_price=float(record.get("entry_price", 0.0) or 0.0),
                placed_at=placed_at,
                order_id=order_id,
                simulated=simulated,
                amount_usdc=float(record.get("amount_usdc", 0.0) or 0.0),
                window_beat=float(record.get("window_beat", 0.0) or 0.0),
                window_end_at=window_end_at,
                elapsed_at_bet=int(record.get("elapsed_at_bet", 0) or 0),
                gap_pct_at_bet=float(record.get("gap_pct_at_bet", 0.0) or 0.0),
                ai_confidence=float(record.get("ai_confidence", 0.0) or 0.0),
                ai_raw_confidence=float(record.get("ai_raw_confidence", 0.0) or 0.0),
                signal_alignment=int(record.get("signal_alignment", 0) or 0),
            )
            self.state.positions.append(pos)
            if pos.condition_id:
                self.state.bet_attempted_windows.add(pos.condition_id)
            if pos.order_id:
                existing_ids.add(pos.order_id)
            recovered += 1

        return recovered, skipped

    def _position_window_has_ended(self, pos: "Position") -> bool:
        now_utc = datetime.now(_UTC)
        if pos.window_end_at is not None:
            return now_utc.timestamp() >= pos.window_end_at.timestamp()

        active_win = self.state.window
        if active_win and active_win.condition_id == pos.condition_id:
            return now_utc >= active_win.end_time
        return True

    def _get_settlement_btc_for_window(
        self,
        *,
        condition_id: str,
        window_end_at: datetime | None,
    ) -> float | None:
        target = window_end_at
        if target is None:
            active_win = self.state.window
            if active_win and active_win.condition_id == condition_id:
                target = active_win.end_time

        if target is not None:
            history_ts = list(self.state.price_history_ts)
            if history_ts:
                closest = min(history_ts, key=lambda x: abs(x[0] - target.timestamp()))
                if abs(closest[0] - target.timestamp()) <= 90:
                    return closest[1]

            logged_price = self.state.logger.find_price_near(target, max_diff_s=90)
            if logged_price is not None:
                return logged_price

        return self.state.btc_price

    def _get_settlement_btc(self, pos: "Position") -> float | None:
        return self._get_settlement_btc_for_window(
            condition_id=pos.condition_id,
            window_end_at=pos.window_end_at,
        )

    @staticmethod
    def _parse_logged_datetime(raw: object) -> datetime | None:
        if not raw or not isinstance(raw, str):
            return None
        try:
            return datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except Exception:
            return None

    @staticmethod
    def _infer_window_end(placed_at: datetime) -> datetime:
        minute_bucket = (placed_at.minute // 5) * 5
        window_start = placed_at.replace(minute=minute_bucket, second=0, microsecond=0)
        return window_start + timedelta(minutes=5)

    def _warm_recent_outcomes(self) -> int:
        loaded = self.state.logger.load_recent_outcomes(
            limit=self.state.recent_window_outcomes.maxlen or 50
        )
        for outcome in loaded:
            self.state.recent_window_outcomes.append(outcome)
        return len(loaded)

    def _warm_paper_analytics(self) -> tuple[int, int]:
        pending, counts = self.state.logger.load_paper_analytics(
            today=datetime.now(_UTC).strftime("%Y-%m-%d")
        )
        self.state.paper_stats.apply_counts(counts)

        restored = 0
        for raw in pending.values():
            condition_id = str(raw.get("condition_id", "")).strip()
            if not condition_id:
                continue
            self.state.paper_prediction_records[condition_id] = WindowPredictionRecord(
                condition_id=condition_id,
                window_label=str(raw.get("window_label", "")),
                window_end_at=self._parse_logged_datetime(raw.get("window_end_at")),
                beat_price=float(raw.get("beat_price", 0.0) or 0.0),
                predicted_direction=str(raw.get("predicted_direction", "NONE")),
                decision_action=str(raw.get("decision_action", "blocked")),
                simulated_order_id=str(raw.get("simulated_order_id", "")).strip(),
                confidence=float(raw.get("confidence", 0.0) or 0.0),
                raw_confidence=float(raw.get("raw_confidence", 0.0) or 0.0),
                alignment=int(raw.get("alignment", 0) or 0),
                actual_winner=str(raw.get("actual_winner", "")),
                prediction_correct=raw.get("prediction_correct") if isinstance(raw.get("prediction_correct"), bool) else None,
                paper_trade_won=raw.get("paper_trade_won") if isinstance(raw.get("paper_trade_won"), bool) else None,
                resolved_at=self._parse_logged_datetime(raw.get("resolved_at")),
                last_updated_at=self._parse_logged_datetime(raw.get("last_updated_at")),
            )
            restored += 1

        warmed = self.state.paper_stats.prediction_total + self.state.paper_stats.paper_trade_total
        return restored, warmed

    async def _sync_recovered_paper_positions(self) -> None:
        async with self.state._lock:
            open_simulated = [p for p in self.state.positions if p.simulated and p.status == "open"]

        for pos in open_simulated:
            await self._attach_paper_trade_to_prediction(pos)

    async def _upsert_paper_prediction(
        self,
        win: "WindowInfo",
        signal: "AISignal",
        snap: "IndicatorSnapshot",
        *,
        decision_action: str,
    ) -> None:
        if LIVE_TRADING or signal.signal not in ("BUY_UP", "BUY_DOWN"):
            return

        direction = "UP" if signal.signal == "BUY_UP" else "DOWN"
        now_utc = datetime.now(_UTC)

        async with self.state._lock:
            record = self.state.paper_prediction_records.get(win.condition_id)
            if record is None:
                record = WindowPredictionRecord(
                    condition_id=win.condition_id,
                    window_label=win.window_label,
                    window_end_at=win.end_time,
                    beat_price=win.beat_price,
                )
                self.state.paper_prediction_records[win.condition_id] = record
            if record.prediction_correct is not None:
                return

            record.window_label = win.window_label
            record.window_end_at = win.end_time
            record.beat_price = win.beat_price
            record.predicted_direction = direction
            record.decision_action = decision_action
            record.confidence = signal.confidence
            record.raw_confidence = signal.raw_confidence or signal.confidence
            record.alignment = snap.signal_alignment
            record.last_updated_at = now_utc

        self.state.logger.log_paper_prediction_state(record)

    async def _attach_paper_trade_to_prediction(self, pos: "Position") -> None:
        if LIVE_TRADING or not pos.simulated:
            return

        now_utc = datetime.now(_UTC)
        async with self.state._lock:
            record = self.state.paper_prediction_records.get(pos.condition_id)
            if record is None:
                record = WindowPredictionRecord(
                    condition_id=pos.condition_id,
                    window_label="",
                    window_end_at=pos.window_end_at,
                    beat_price=pos.window_beat,
                    predicted_direction=pos.direction,
                )
                self.state.paper_prediction_records[pos.condition_id] = record
            if record.prediction_correct is not None:
                return

            record.window_end_at = pos.window_end_at or record.window_end_at
            record.beat_price = pos.window_beat or record.beat_price
            record.predicted_direction = pos.direction or record.predicted_direction
            record.decision_action = "paper_trade"
            record.simulated_order_id = pos.order_id or record.simulated_order_id
            record.confidence = pos.ai_confidence or record.confidence
            record.raw_confidence = pos.ai_raw_confidence or record.raw_confidence
            record.alignment = pos.signal_alignment or record.alignment
            record.last_updated_at = now_utc

        self.state.logger.log_paper_prediction_state(record)

    @staticmethod
    def _odds_bucket(odds: float) -> str:
        if odds < 0.55:
            return "<0.55"
        if odds < 0.70:
            return "0.55-0.69"
        if odds < 0.80:
            return "0.70-0.79"
        return ">=0.80"

    def _calibrate_signal_confidence(
        self,
        *,
        raw_confidence: float,
        direction: str,
        entry_odds: float,
        alignment: int,
    ) -> float:
        """Deflate LLM confidence toward realized performance and market odds."""
        raw = max(0.0, min(0.92, raw_confidence))
        if entry_odds <= 0.0 or raw <= entry_odds:
            return raw

        trust = 0.55
        if alignment >= 5:
            trust += 0.20
        elif alignment >= 4:
            trust += 0.10

        recent = list(self.state.recent_window_outcomes)[-40:]
        bucket = self._odds_bucket(entry_odds)
        similar = [
            item for item in recent
            if item.get("direction") == direction
            and self._odds_bucket(float(item.get("odds", 0.0) or 0.0)) == bucket
        ]
        if len(similar) >= 3:
            win_rate = sum(1 for item in similar if item.get("won")) / len(similar)
            trust += max(-0.15, min(0.15, (win_rate - 0.5) * 0.6))
        elif recent:
            overall_wr = sum(1 for item in recent if item.get("won")) / len(recent)
            trust += max(-0.08, min(0.08, (overall_wr - 0.5) * 0.4))

        if entry_odds < 0.60:
            trust -= 0.05
        elif 0.70 <= entry_odds < 0.80:
            trust -= 0.03

        trust = max(0.35, min(0.90, trust))
        calibrated = entry_odds + (raw - entry_odds) * trust
        return max(0.0, min(raw, round(calibrated, 4)))

    # ── Balance loop ──────────────────────────────────────────────────────────

    async def _balance_loop(self) -> None:
        while self.state.running:
            bal = await self.market.get_balance()
            if bal > 0:
                self.state.balance_usdc = bal
            await asyncio.sleep(120)

    # ── Credential refresh loop ───────────────────────────────────────────────

    async def _creds_refresh_loop(self) -> None:
        """Re-derive Polymarket L2 session credentials from POLY_ETH_PRIVATE_KEY.

        Polymarket sessions expire roughly every 24 hours. This loop refreshes
        them every 23 hours so the bot never hits an expired-session error.
        On failure it retries every hour until success.
        """
        _REFRESH_INTERVAL_S = 23 * 3600   # refresh before 24-hour expiry
        _RETRY_INTERVAL_S   = 3600        # retry interval on failure

        await asyncio.sleep(_REFRESH_INTERVAL_S)
        while self.state.running:
            ok = await self.market.refresh_credentials()
            if ok:
                self.state.log_event("[CREDS] Polymarket L2 session refreshed")
                await asyncio.sleep(_REFRESH_INTERVAL_S)
            else:
                self.state.log_event("[CREDS] L2 session refresh failed — retrying in 1 h")
                await asyncio.sleep(_RETRY_INTERVAL_S)


# ══════════════════════════════════════════════════════════════════════════════
# Source: main.py
# ══════════════════════════════════════════════════════════════════════════════

"""Entry point — Rich Live terminal UI + asyncio bot runner."""

import asyncio
import sys
import time
from datetime import datetime, timezone

from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text



# ── Layout builder ────────────────────────────────────────────────────────────

def build_layout() -> Layout:
    layout = Layout(name="root")
    # body uses fixed-height panels; keep both left/right sums aligned at 27.
    layout.split_column(
        Layout(name="header", size=1),
        Layout(name="main"),
    )
    # main splits into left_stack (existing panels) and price_log (new, full height)
    layout["main"].split_row(
        Layout(name="left_stack", ratio=2),
        Layout(name="price_log",  ratio=1),
    )
    layout["left_stack"].split_column(
        Layout(name="body", size=27),
        Layout(name="logs"),
    )
    layout["body"].split_row(
        Layout(name="left",  ratio=1),
        Layout(name="right", ratio=1),
    )
    layout["left"].split_column(
        Layout(name="window_panel", size=7),
        Layout(name="market_data",  size=7),
        Layout(name="filters",      size=9),
        Layout(name="signal",       size=4),
    )
    layout["right"].split_column(
        Layout(name="positions", size=6),
        Layout(name="results",   size=12),
        Layout(name="blocked",   size=9),
    )
    return layout


# ── Progress bar helper ───────────────────────────────────────────────────────

def _bar(filled: int, total: int, width: int = 20, char_fill: str = "█", char_empty: str = "─") -> str:
    if total <= 0:
        total = 1
    n = min(int(filled / total * width), width)
    return "[" + char_fill * n + char_empty * (width - n) + "]"


def _win_rate_bar(pct: float, width: int = 20) -> str:
    n = min(int(pct / 100 * width), width)
    filled = "[green]" + "█" * n + "[/green]"
    empty  = "─" * (width - n)
    return "[" + filled + empty + "]"


def _short_gate_label(gate: str | None) -> str:
    if not gate or gate == "—":
        return "—"
    short = gate.removeprefix("GATE_")
    return {
        "LOW_ENTRY_ODDS": "LOW_ODDS",
        "CHOPPY_BEAT": "CHOP",
        "ODDS_VEL_CONFLICT": "VEL_CONFLICT",
        "LOW_ALIGNMENT": "LOW_ALIGN",
        "DIR_CONFLICT": "DIR_CONFLICT",
        "AI_HOLD": "AI_HOLD",
        "LOW_CONF": "LOW_CONF",
        "TOO_SURE": "TOO_SURE",
        "NO_MOVE": "NO_MOVE",
        "NO_EDGE": "NO_EDGE",
        "50_50": "FIFTY",
    }.get(short, short)


def _path_status_markup(state: BotState) -> str:
    phase = state.engine_phase or "BOOT"
    pre = "WAIT"
    ai = "—"
    final = "—"

    if state.last_signal is not None or phase in {
        "AI_QUERY", "AI_DONE", "BUY_READY", "DECISION_SKIP", "ORDER_OPEN", "ORDER_FAILED", "ALREADY_ATTEMPTED",
    }:
        pre = "PASS"
    elif state.last_pre_ai_decision is not None:
        pre = f"SKIP:{_short_gate_label(state.last_pre_ai_decision.gate)}"
    else:
        pre = {
            "NEW_WINDOW": "NEW",
            "WAIT_GOLD_ZONE": "WAIT_ZONE",
            "WAIT_BTC": "WAIT_BTC",
            "WAIT_ODDS": "WAIT_ODDS",
            "ODDS_DESYNC": "ODDS_SYNC",
            "NO_WINDOW": "NO_WIN",
            "TOO_LATE": "TOO_LATE",
            "RATE_LIMIT": "RATE",
            "LOW_BALANCE": "LOW_BAL",
            "HALT_DAILY_LOSS": "HALT_LOSS",
            "HALT_DAILY_PROFIT": "HALT_PROFIT",
            "STREAK_PAUSE": "PAUSE",
        }.get(phase, "WAIT")

    if state.last_signal is not None:
        ai = {
            "BUY_UP": "UP",
            "BUY_DOWN": "DN",
            "SKIP": "SKIP",
        }.get(state.last_signal.signal, state.last_signal.signal)
    elif phase == "AI_QUERY":
        ai = "RUN"

    if state.last_signal is not None:
        if state.last_trade_decision is None:
            final = "WAIT"
        elif state.last_trade_decision.action == "BUY":
            final = "BUY"
        else:
            final = f"SKIP:{_short_gate_label(state.last_trade_decision.gate)}"

    def color_for(status: str) -> str:
        if status in {"PASS", "BUY", "UP"}:
            return "green"
        if status == "DN":
            return "red"
        if status.startswith("SKIP"):
            return "yellow"
        if status in {"RUN", "WAIT", "WAIT_ZONE", "WAIT_BTC", "WAIT_ODDS", "NEW"}:
            return "cyan"
        if status in {"ODDS_SYNC", "TOO_LATE", "LOW_BAL", "HALT_LOSS", "HALT_PROFIT", "RATE", "PAUSE"}:
            return "red"
        return "white"

    return (
        f"P:[{color_for(pre)}]{pre}[/{color_for(pre)}] "
        f"A:[{color_for(ai)}]{ai}[/{color_for(ai)}] "
        f"F:[{color_for(final)}]{final}[/{color_for(final)}]"
    )


# ── Render functions ──────────────────────────────────────────────────────────

def render_header(state: BotState) -> Text:
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    t = Text()
    t.append(" 🐻 BOT", style="bold white")
    t.append(" ")
    if LIVE_TRADING:
        t.append("●", style="bold green")
        t.append(" LIVE ", style="bold green")
    else:
        t.append("●", style="bold yellow")
        t.append(" PAPER ", style="bold yellow")
    t.append(f"│ {now_str} │ {state.uptime} ", style="cyan")
    return t


def render_window_panel(state: BotState) -> Panel:
    win = state.window
    if win is None:
        body = Text("Searching for active Bitcoin Up or Down market…", style="yellow")
        return Panel(body, title="[bold cyan]POLYMARKET WINDOW[/bold cyan]", border_style="blue")

    now = datetime.now(timezone.utc)
    elapsed_s   = int((now - win.start_time).total_seconds())
    remaining_s = max(0, int((win.end_time - now).total_seconds()))
    total_s     = max(1, int((win.end_time - win.start_time).total_seconds()))

    vs_beat = (state.btc_price or win.beat_price) - win.beat_price
    vs_color = "green" if vs_beat >= 0 else "red"
    vs_str   = f"+${vs_beat:,.2f}" if vs_beat >= 0 else f"-${abs(vs_beat):,.2f}"

    bar = _bar(elapsed_s, total_s, width=22)
    remaining_color = "green" if remaining_s > 60 else ("yellow" if remaining_s > 20 else "red")

    t = Table.grid(padding=(0, 1))
    t.add_column(style="cyan",  width=12)
    t.add_column()
    t.add_row("Window ID",  f"[white]{win.window_label}[/white]  │  "
                            f"Remaining: [{remaining_color}]{remaining_s}s[/{remaining_color}]")
    t.add_row("Beat price", f"[white]${win.beat_price:,.2f}[/white]  │  "
                            f"vs beat: [{vs_color}]{vs_str}[/{vs_color}]")
    t.add_row("Progress",   f"[dim]{bar}[/dim]")
    t.add_row("Market",     f"[dim white]{win.question[:55]}[/dim white]")

    return Panel(t, title="[bold cyan]POLYMARKET WINDOW[/bold cyan]", border_style="blue")


def render_market_data(state: BotState) -> Panel:
    ws_ok  = "[bold green]OK[/bold green]" if state.btc_ws_ok else "[bold red]ERR[/bold red]"
    btc_s  = f"${state.btc_price:,.2f}" if state.btc_price else "—"
    up_s   = f"{state.up_odds:.3f}"   if state.up_odds   is not None else "—"
    dn_s   = f"{state.down_odds:.3f}" if state.down_odds is not None else "—"

    odds_age = ""
    if state.odds_updated_at:
        age = int(time.time() - state.odds_updated_at)
        odds_age = f" [dim]{age}s ago[/dim]"

    t = Table.grid(padding=(0, 1))
    t.add_column(style="cyan",  width=12)
    t.add_column()
    t.add_row("BTC Price", f"[bold white]{btc_s}[/bold white]  WS: {ws_ok}")
    t.add_row("Odds",      f"[green]UP={up_s}[/green]  [red]DOWN={dn_s}[/red]{odds_age}")

    if state.window and state.btc_price is not None and state.window.beat_price > 0:
        gap = state.btc_price - state.window.beat_price
        gap_pct = gap / state.window.beat_price * 100
        side = "UP" if gap >= 0 else "DOWN"
        side_color = "green" if side == "UP" else "red"
        gap_color = "green" if gap >= 0 else "red"
        elapsed_s = int((datetime.now(timezone.utc) - state.window.start_time).total_seconds())
        stage = (
            f"[yellow]wait {max(0, GOLD_ZONE_START_S - elapsed_s)}s[/yellow]"
            if elapsed_s < GOLD_ZONE_START_S
            else "[green]gold zone[/green]"
        )
        t.add_row("Winner", f"[{side_color}]{side}[/{side_color}]  │  {stage}")
        t.add_row("Gap", f"[{gap_color}]{gap:+,.2f}[/{gap_color}]  ({gap_pct:+.3f}%)")

    # Price trend from raw ticks; show 5s-sample count for indicator readiness
    prices = list(state.price_history)
    samples = len(state.price_history_5s)
    if len(prices) >= 2:
        diff    = prices[-1] - prices[-2]
        arrow   = "▲" if diff > 0 else ("▼" if diff < 0 else "─")
        color   = "green" if diff > 0 else ("red" if diff < 0 else "white")
        ind_ready = "[green]ready[/green]" if samples >= 21 else f"[yellow]warming {samples}/21[/yellow]"
        t.add_row("Trend", f"[{color}]{arrow} {diff:+.2f}[/{color}]  ind:{ind_ready}")

    return Panel(t, title="[bold cyan]MARKET DATA[/bold cyan]", border_style="blue")


def render_filters(state: BotState) -> Panel:
    snap = state.indicator_snapshot
    if snap is None:
        body = Text("Waiting for price data…", style="yellow")
        return Panel(body, title="[bold cyan]FILTERS[/bold cyan]", border_style="blue")

    t = Table.grid(padding=(0, 1))
    t.add_column(width=5)
    t.add_column(width=18)
    t.add_column(width=14)
    t.add_column()

    for f in snap.filters:
        badge = "[bold green]PASS[/bold green]" if f.passed else "[bold red]FAIL[/bold red]"
        t.add_row(
            f"[cyan]{f.name}[/cyan]",
            f"[white]{f.label}[/white]",
            f"[dim white]{f.value[:13]}[/dim white]",
            badge,
        )

    age = int(time.time() - snap.timestamp)
    bias_color = "green" if snap.direction_bias == "UP" else ("red" if snap.direction_bias == "DOWN" else "yellow")
    pass_color = "green" if snap.pass_count >= 4 else ("yellow" if snap.pass_count >= 3 else "red")
    t.add_row("", f"[dim]Last: {age}s ago[/dim]",
              f"Bias: [{bias_color}]{snap.direction_bias}[/{bias_color}]",
              f"[{pass_color}]{snap.pass_count}/5[/{pass_color}]")
    align_color = "green" if snap.signal_alignment >= MIN_SIGNAL_ALIGNMENT else "yellow"
    trend_color = "green" if snap.trend_dir == "UP" else ("red" if snap.trend_dir == "DOWN" else "white")
    market_color = "green" if snap.market_dir == "UP" else ("red" if snap.market_dir == "DOWN" else "white")
    flow_color = "green" if snap.flow_dir == "UP" else ("red" if snap.flow_dir == "DOWN" else "white")
    t.add_row(
        "",
        f"Live: [{align_color}]{snap.signal_alignment}/6[/{align_color}] need [white]{MIN_SIGNAL_ALIGNMENT}/6[/white]",
        f"T:[{trend_color}]{snap.trend_dir}({snap.trend_strength})[/{trend_color}]"
        f" M:[{market_color}]{snap.market_dir}({snap.market_strength})[/{market_color}]",
        f"F:[{flow_color}]{snap.flow_dir}({snap.flow_strength})[/{flow_color}]",
    )

    title = "[bold cyan]FILTERS[/bold cyan] [dim](≥2/5 for signal · Real Time)[/dim]"
    return Panel(t, title=title, border_style="blue")


def render_signal(state: BotState) -> Panel:
    sig = state.last_signal
    if sig is None:
        body = Text("No signal yet", style="dim")
        return Panel(body, title="[bold cyan]LAST SIGNAL[/bold cyan]", border_style="blue")

    if sig.signal == "BUY_UP":
        sig_text = "[bold bright_green]BUY_UP[/bold bright_green]"
    elif sig.signal == "BUY_DOWN":
        sig_text = "[bold bright_red]BUY_DOWN[/bold bright_red]"
    else:
        sig_text = "[bold yellow]SKIP[/bold yellow]"

    body = Text.from_markup(sig_text)
    return Panel(body, title="[bold cyan]LAST SIGNAL[/bold cyan]", border_style="blue")


def render_positions(state: BotState) -> Panel:
    open_pos = state.open_positions
    title = f"[bold cyan]ACTIVE POSITIONS[/bold cyan] [white]({len(open_pos)} open)[/white]"

    if not open_pos:
        body = Text("– tidak ada posisi aktif", style="dim")
        return Panel(body, title=title, border_style="blue")

    t = Table(show_header=True, header_style="cyan", box=None, padding=(0, 1))
    t.add_column("Dir",    width=5)
    t.add_column("Entry",  width=7)
    t.add_column("Size",   width=8)
    t.add_column("Status", width=8)

    for p in open_pos:
        dir_color = "green" if p.direction == "UP" else "red"
        sim = " [dim]SIM[/dim]" if p.simulated else ""
        t.add_row(
            f"[{dir_color}]{p.direction}[/{dir_color}]",
            f"{p.entry_price:.3f}",
            f"${BET_SIZE_USDC:.2f}",
            f"[yellow]open[/yellow]{sim}",
        )

    return Panel(t, title=title, border_style="blue")


def render_results(state: BotState) -> Panel:
    wr    = state.win_rate
    wr_bar = _win_rate_bar(wr, width=18)
    pnl_color = "green" if state.total_pnl >= 0 else "red"
    pnl_s = f"+${state.total_pnl:.2f}" if state.total_pnl >= 0 else f"-${abs(state.total_pnl):.2f}"
    bal_ok = state.balance_usdc >= AUTO_CLAIM_THRESHOLD
    claim_status = f"[green]OK (thr < ${AUTO_CLAIM_THRESHOLD:.0f})[/green]" if bal_ok \
                   else f"[yellow]LOW (${state.balance_usdc:.2f})[/yellow]"

    last_claim = state.claim_log[-1] if state.claim_log else f"– nothing to claim"
    resolved_pending = len([p for p in state.positions if p.status == "open"])

    t = Table.grid(padding=(0, 1))
    t.add_column(style="cyan", width=12)
    t.add_column()

    t.add_row("Balance",   f"[bold white]$  {state.balance_usdc:.2f} USDC[/bold white]")
    t.add_row("AutoClaim", claim_status)
    t.add_row("Claim log", f"[dim]{last_claim[:50]}[/dim]")
    t.add_row("Bets/hour", f"[white]{state.bets_this_hour}/{MAX_BETS_PER_HOUR}[/white]"
                           f"  │  Bet size: [white]${BET_SIZE_USDC:.2f}[/white]")
    t.add_row("Resolved",  f"[white]{state.resolved_count}[/white] "
                           f"(pending: {resolved_pending}) "
                           f"WIN: [green]{state.win_count}[/green] "
                           f"LOSS: [red]{state.loss_count}[/red]")
    if LIVE_TRADING:
        t.add_row("Win Rate",  f"[white]{wr:.1f}%[/white] {wr_bar}")
    else:
        ps = state.paper_stats
        t.add_row(
            "Paper Trades",
            f"all [green]{ps.paper_trade_wins_total}W[/green]/[red]{ps.paper_trade_losses_total}L[/red] "
            f"({ps.paper_trade_total} · {ps.paper_trade_win_rate:.1f}%)"
        )
        t.add_row(
            "Trades Today",
            f"today [green]{ps.paper_trade_wins_today}W[/green]/[red]{ps.paper_trade_losses_today}L[/red] "
            f"({ps.paper_trade_today_total} · {ps.paper_trade_win_rate_today:.1f}%)"
        )
        t.add_row(
            "Predictions",
            f"all [green]{ps.prediction_correct_total}✓[/green]/[red]{ps.prediction_incorrect_total}✗[/red] "
            f"({ps.prediction_total} · {ps.prediction_accuracy:.1f}%)"
        )
        t.add_row(
            "Pred Today",
            f"today [green]{ps.prediction_correct_today}✓[/green]/[red]{ps.prediction_incorrect_today}✗[/red] "
            f"({ps.prediction_today_total} · {ps.prediction_accuracy_today:.1f}%)"
        )
    t.add_row("Total PnL", f"[{pnl_color}]$  {pnl_s}[/{pnl_color}]")

    # Streak indicator
    if state.streak_pause_until > 0 and time.time() < state.streak_pause_until:
        mins_left = int((state.streak_pause_until - time.time()) / 60) + 1
        streak_s = f"[bold red]HALTED {mins_left}m — {state.consecutive_losses} consecutive losses[/bold red]"
    elif state.consecutive_losses >= 3:
        streak_s = f"[red]⚠ {state.consecutive_losses} losses streak — ½ bet size[/red]"
    elif state.consecutive_losses == 2:
        streak_s = f"[yellow]{state.consecutive_losses} losses in a row[/yellow]"
    elif state.consecutive_wins >= 3:
        streak_s = f"[green]✓ {state.consecutive_wins} wins streak[/green]"
    else:
        streak_s = f"[dim]W{state.consecutive_wins} / L{state.consecutive_losses}[/dim]"
    t.add_row("Streak", streak_s)

    if DAILY_BUDGET_USDC > 0:
        net_loss  = state.daily_loss - state.daily_profit
        remaining = DAILY_BUDGET_USDC - net_loss   # can exceed limit when profits > losses
        if state.daily_halted:
            budget_s = f"[bold red]HALTED — net loss ${net_loss:.2f} hit limit ${DAILY_BUDGET_USDC:.2f}[/bold red]"
        else:
            bud_color = "green" if remaining >= DAILY_BUDGET_USDC else ("yellow" if remaining > 0 else "red")
            budget_s = (
                f"lost=[red]${state.daily_loss:.2f}[/red]  "
                f"won=[green]${state.daily_profit:.2f}[/green]  "
                f"left=[{bud_color}]${remaining:.2f}[/{bud_color}]  "
                f"limit=${DAILY_BUDGET_USDC:.2f}"
            )
        t.add_row("Daily Budget", budget_s)

    if DAILY_PROFIT_TARGET_USDC > 0:
        if state.daily_profit_halted:
            profit_s = f"[bold green]TARGET HIT — ${DAILY_PROFIT_TARGET_USDC:.2f} earned, trading stopped[/bold green]"
        else:
            to_go = max(0.0, DAILY_PROFIT_TARGET_USDC - state.daily_profit)
            prog_color = "green" if to_go == 0 else ("yellow" if state.daily_profit > 0 else "white")
            profit_s = (
                f"earned=[{prog_color}]${state.daily_profit:.2f}[/{prog_color}]"
                f"  to go=[white]${to_go:.2f}[/white]"
                f"  target=${DAILY_PROFIT_TARGET_USDC:.2f}"
            )
        t.add_row("Daily Target", profit_s)

    return Panel(t, title="[bold cyan]RESULTS[/bold cyan]", border_style="blue")


def render_logs(state: BotState) -> Panel:
    """Show the last N bot log events in real time."""
    entries = state.event_log[-60:]   # show as many as fit in the flexible panel

    lines: list[Text] = []
    for ts, msg in entries:
        time_s = ts.strftime("%H:%M:%S")

        # Colour-code by keyword
        if any(k in msg for k in ("[CANCEL]", "[HALT]", "[ERR")):
            msg_style = "bold red"
        elif any(k in msg for k in ("[LIVE/", "[PAPER/", "BET ")):
            msg_style = "bold green"
        elif any(k in msg for k in ("[DECISION]", "[AI/BET]", "[LAST-MIN]")):
            msg_style = "cyan"
        elif any(k in msg for k in ("[GATE", "[GATE_")):
            msg_style = "yellow"
        elif "[MKT]" in msg:
            msg_style = "blue"
        else:
            msg_style = "dim white"

        line = Text()
        line.append(f"{time_s} ", style="dim")
        line.append(msg[:110], style=msg_style)
        lines.append(line)

    if not lines:
        body = Text("No events yet…", style="dim")
    else:
        body = Text("\n").join(lines)

    return Panel(body, title="[bold cyan]BOT LOG[/bold cyan]", border_style="blue")


def render_blocked(state: BotState) -> Panel:
    snap = state.indicator_snapshot
    fair = state.latest_fair_prob or {}
    chop = state.latest_beat_chop or {}
    path_s = _path_status_markup(state)
    age = int(time.time() - state.engine_updated_at) if state.engine_updated_at else 0
    phase = state.engine_phase or "BOOT"
    gate = state.engine_gate or "—"
    phase_color = {
        "ORDER_OPEN": "green",
        "BUY_READY": "green",
        "AI_DONE": "cyan",
        "AI_QUERY": "cyan",
        "PRE_AI_SKIP": "yellow",
        "DECISION_SKIP": "yellow",
        "WAIT_GOLD_ZONE": "cyan",
        "ODDS_DESYNC": "red",
        "LOW_BALANCE": "red",
        "HALT_DAILY_LOSS": "red",
        "HALT_DAILY_PROFIT": "green",
    }.get(phase, "white")

    side = "—"
    side_color = "white"
    gap_s = "—"
    gap_pct_s = "—"
    elapsed_s = 0
    remaining_s = 0
    if state.window and state.btc_price is not None and state.window.beat_price > 0:
        gap = state.btc_price - state.window.beat_price
        gap_pct = gap / state.window.beat_price * 100
        side = "UP" if gap >= 0 else "DOWN"
        side_color = "green" if side == "UP" else "red"
        gap_color = "green" if gap >= 0 else "red"
        gap_s = f"[{gap_color}]{gap:+,.2f}[/{gap_color}]"
        gap_pct_s = f"[{gap_color}]{gap_pct:+.3f}%[/{gap_color}]"
        elapsed_s = int((datetime.now(timezone.utc) - state.window.start_time).total_seconds())
        remaining_s = max(0, int((state.window.end_time - datetime.now(timezone.utc)).total_seconds()))

    fair_up = fair.get("fair_up", 0.5)
    fair_down = fair.get("fair_down", 0.5)
    edge_up = fair.get("edge_up", 0.0)
    edge_down = fair.get("edge_down", 0.0)
    z_score = fair.get("z_score", 0.0)

    align = snap.signal_alignment if snap else 0
    cvd = snap.cvd_divergence if snap else "NONE"
    cvd_color = "green" if cvd == "BULLISH" else ("red" if cvd == "BEARISH" else "white")
    odds_dir = snap.odds_vel_direction if snap else "NONE"
    odds_color = "green" if odds_dir == "UP" else ("red" if odds_dir == "DOWN" else "white")
    odds_vel = (snap.odds_vel_value * 1000) if snap else 0.0
    odds_acc = (snap.odds_vel_accel * 1000) if snap else 0.0
    dip_label = getattr(state.last_signal, "dip_label", "n/a") if state.last_signal else "n/a"
    votes_s = "n/a"
    if snap:
        votes_s = (
            f"MA={snap.ma_dir} Mom={snap.momentum_dir} MACD={snap.macd_dir} "
            f"Odds={snap.odds_edge_dir} OVel={snap.odds_vel_vote_dir} CVD={snap.flow_dir}"
        )

    reason = (state.engine_reason or "waiting for runtime context")[:58]
    body = Text.from_markup(
        f"[{phase_color}]{phase}[/{phase_color}] gate=[cyan]{gate}[/cyan]  [dim]{age}s ago[/dim]\n"
        f"path {path_s}\n"
        f"winner:[{side_color}]{side}[/{side_color}]  gap:{gap_s} ({gap_pct_s})  "
        f"[dim]t[/dim]={elapsed_s}s/{remaining_s}s\n"
        f"fair U/D:[green]{fair_up:.0%}[/green]/[red]{fair_down:.0%}[/red]  "
        f"EV U/D:[green]{edge_up:+.1%}[/green]/[red]{edge_down:+.1%}[/red]  "
        f"z=[white]{z_score:+.2f}[/white]\n"
        f"align:[white]{align}/6[/white]  cvd:[{cvd_color}]{cvd}[/{cvd_color}]  "
        f"ov:[{odds_color}]{odds_dir}[/{odds_color}] {odds_vel:+.1f}m/s  acc={odds_acc:+.1f}\n"
        f"T/M/F=[white]{getattr(snap, 'trend_strength', 0)}/{getattr(snap, 'market_strength', 0)}/{getattr(snap, 'flow_strength', 0)}[/white]  "
        f"need=[white]{MIN_SIGNAL_ALIGNMENT}/6[/white]  [dim]{votes_s[:56]}[/dim]\n"
        f"chop:x=[white]{int(chop.get('crossings', 0))}[/white]  "
        f"above=[white]{chop.get('above_ratio', 0.0):.0%}[/white]  "
        f"dip=[white]{dip_label}[/white]  [dim]{reason}[/dim]"
    )
    return Panel(body, title="[bold cyan]ENGINE[/bold cyan]", border_style="blue")


def render_price_log(state: BotState) -> Panel:
    """Stream the last N 5-second BTC price snapshots."""
    entries = list(state.price_tick_log)[-80:]  # fills flexible full-height panel

    if not entries:
        body = Text("Waiting for price data…", style="dim")
        return Panel(body, title="[bold cyan]PRICES[/bold cyan]", border_style="blue")

    lines: list[Text] = []
    prev_btc = None
    for ts, btc, buy_v, sell_v, cvd, up_odds, dn_odds in entries:
        time_s = ts.strftime("%H:%M:%S")

        if prev_btc is not None:
            arrow = "▲" if btc > prev_btc else ("▼" if btc < prev_btc else "─")
            color = "green" if btc > prev_btc else ("red" if btc < prev_btc else "white")
        else:
            arrow, color = "─", "white"
        prev_btc = btc

        up_s = f"{up_odds:.2f}" if up_odds is not None else "─ "
        dn_s = f"{dn_odds:.2f}" if dn_odds is not None else "─ "
        cvd_color = "green" if cvd >= 0 else "red"
        net_v = buy_v - sell_v
        net_color = "green" if net_v >= 0 else "red"

        line = Text()
        line.append(f"{time_s} ", style="dim")
        line.append(f"{arrow}${btc:>10,.2f} ", style=color)
        line.append("U", style="dim")
        line.append(up_s, style="green")
        line.append(" D", style="dim")
        line.append(dn_s, style="red")
        line.append(" Δ", style="dim")
        line.append(f"{net_v:+.4f}", style=net_color)
        line.append(" cvd=", style="dim")
        line.append(f"{cvd:.2f}", style=cvd_color)
        lines.append(line)

    body = Text("\n").join(lines)
    return Panel(body, title="[bold cyan]PRICES (5s)[/bold cyan]", border_style="blue")


# ── UI updater coroutine ──────────────────────────────────────────────────────

async def update_ui(layout: Layout, state: BotState) -> None:
    while state.running:
        layout["header"].update(render_header(state))
        layout["window_panel"].update(render_window_panel(state))
        layout["market_data"].update(render_market_data(state))
        layout["filters"].update(render_filters(state))
        layout["signal"].update(render_signal(state))
        layout["positions"].update(render_positions(state))
        layout["results"].update(render_results(state))
        layout["blocked"].update(render_blocked(state))
        layout["logs"].update(render_logs(state))
        layout["price_log"].update(render_price_log(state))
        await asyncio.sleep(UI_REFRESH_S)


# ── Entry point ───────────────────────────────────────────────────────────────

async def main() -> None:
    # Validate config
    missing = validate_config()
    if missing:
        console = Console()
        console.print(f"[bold red]ERROR:[/bold red] Missing environment variables:")
        for k in missing:
            console.print(f"  • {k}")
        console.print("\nPlease fill in [cyan].env[/cyan] and restart.")
        sys.exit(1)

    mode_msg = "PAPER TRADING (signals only)" if not LIVE_TRADING else "LIVE TRADING ENABLED"
    Console().print(f"[bold yellow]{mode_msg}[/bold yellow]")

    bot    = TradingBot()
    layout = build_layout()

    with Live(layout, refresh_per_second=2, screen=True):
        await asyncio.gather(
            bot.run(),
            update_ui(layout, bot.state),
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        Console().print("\n[yellow]Bot stopped.[/yellow]")
