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

# ── API base URLs ────────────────────────────────────────────────────────────
CLOB_HOST = "https://clob.polymarket.com"
GAMMA_API = "https://gamma-api.polymarket.com"
DATA_API  = "https://data-api.polymarket.com"
CHAIN_ID  = 137

# ── WebSocket URLs ───────────────────────────────────────────────────────────
BINANCE_WS              = "wss://stream.binance.com:9443/ws/btcusdc@trade"
HYPERLIQUID_WS          = "wss://api.hyperliquid.xyz/ws"
BTC_STALENESS_THRESHOLD_S   = float(os.getenv("BTC_STALENESS_THRESHOLD_S", "5.0"))
HL_DIVERGENCE_THRESHOLD_PCT = float(os.getenv("HL_DIVERGENCE_THRESHOLD_PCT", "0.10"))
MARKET_WS  = "wss://ws-subscriptions-clob.polymarket.com/ws/market"
USER_WS    = "wss://ws-subscriptions-clob.polymarket.com/ws/user"

# ── BTC feed ─────────────────────────────────────────────────────────────────
BTC_HISTORY_SIZE = 300   # rolling ticks kept in memory

# ── Trading parameters ───────────────────────────────────────────────────────
POLYMARKET_TAKER_FEE_RATE = 0.02   # 2% fee deducted from payout on winning taker orders
BET_SIZE_USDC             = float(os.getenv("BET_SIZE_USDC", "2.00"))
DAILY_BUDGET_USDC         = float(os.getenv("DAILY_BUDGET_USDC", "0"))          # 0 = disabled
DAILY_PROFIT_TARGET_USDC  = float(os.getenv("DAILY_PROFIT_TARGET_USDC", "0"))   # 0 = disabled
SIGNAL_COOLDOWN_S    = 1
MAX_BETS_PER_HOUR    = 10
HEARTBEAT_INTERVAL_S = 30     # POST /heartbeats to keep session alive
LIVE_TRADING         = os.getenv("LIVE_TRADING", "false").lower() == "true"
AUTO_CLAIM_THRESHOLD = float(os.getenv("AUTO_CLAIM_THRESHOLD", "0.00"))
AUTO_CLAIM_ENABLED = os.getenv("AUTO_CLAIM_ENABLED", "false").lower() == "true"
AUTO_CLAIM_LIVE_ONLY = os.getenv("AUTO_CLAIM_LIVE_ONLY", "true").lower() == "true"
AUTO_CLAIM_SCAN_INTERVAL_S = int(os.getenv("AUTO_CLAIM_SCAN_INTERVAL_S", "300"))
AUTO_CLAIM_MAX_RETRIES = int(os.getenv("AUTO_CLAIM_MAX_RETRIES", "3"))
POLY_RELAYER_URL = os.getenv("POLY_RELAYER_URL", "https://relayer-v2.polymarket.com/")
POLY_BUILDER_API_KEY = os.getenv("POLY_BUILDER_API_KEY", "")
POLY_BUILDER_SECRET = os.getenv("POLY_BUILDER_SECRET", "")
POLY_BUILDER_PASSPHRASE = os.getenv("POLY_BUILDER_PASSPHRASE", "")
POLY_RELAYER_API_KEY         = os.getenv("POLY_RELAYER_API_KEY", "")
POLY_RELAYER_API_KEY_ADDRESS = os.getenv("POLY_RELAYER_API_KEY_ADDRESS", "")
POLY_CTF_ADDRESS = os.getenv("POLY_CTF_ADDRESS", "0x4d97dcd97ec945f40cf65f87097ace5ea0476045")
POLY_USDC_ADDRESS = os.getenv("POLY_USDC_ADDRESS", "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174")
POLY_CREDS_REFRESH_INTERVAL_S = int(os.getenv("POLY_CREDS_REFRESH_INTERVAL_S", str(23 * 3600)))
POLY_CREDS_REFRESH_RETRY_S = int(os.getenv("POLY_CREDS_REFRESH_RETRY_S", "3600"))
POLY_AUTH_HEALTHCHECK_INTERVAL_S = int(os.getenv("POLY_AUTH_HEALTHCHECK_INTERVAL_S", "300"))
POLY_WS_PING_INTERVAL_S = int(os.getenv("POLY_WS_PING_INTERVAL_S", "10"))
POLY_WS_IDLE_RECONNECT_S = int(os.getenv("POLY_WS_IDLE_RECONNECT_S", "30"))
POLY_HTTP_CLOSE_GRACE_S = int(os.getenv("POLY_HTTP_CLOSE_GRACE_S", "5"))
POLY_FATAL_SESSION_FAILURES = int(os.getenv("POLY_FATAL_SESSION_FAILURES", "3"))

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

# ── Last-minute entry window (reserve first, execute later) ─────────────────
SIGNAL_LOCK_START_S    = int(os.getenv("SIGNAL_LOCK_START_S", "180"))
EXECUTION_START_S      = int(os.getenv("EXECUTION_START_S", "210"))
LATE_EXEC_START_S      = int(os.getenv("LATE_EXEC_START_S", "240"))
GOLD_ZONE_START_S      = EXECUTION_START_S
BET_FREQUENCY_EXPANSION_PHASE = os.getenv("BET_FREQUENCY_EXPANSION_PHASE", "C").strip().upper()
GOLD_ZONE_MIN_MOVE_PCT = 0.02   # BTC must be ≥ 0.02% from beat (~$17 at $85k)
GOLD_ZONE_MIN_CONF     = 0.70   # minimum calibrated confidence to execute a bet
GOLD_ZONE_MAX_ODDS     = 0.82   # leading side must still be ≤ this (not fully priced)
LAST_MIN_SECONDS_GUARD = 12     # stop accepting new bets with < 8s left (order latency)
MIN_SIGNAL_ALIGNMENT   = int(os.getenv("MIN_SIGNAL_ALIGNMENT", "4"))  # require at least 4/6 family-weighted alignment
LIVE_RETRY_MAX_RETRIES = int(os.getenv("LIVE_RETRY_MAX_RETRIES", "2"))
LIVE_RETRY_COOLDOWN_S = float(os.getenv("LIVE_RETRY_COOLDOWN_S", "3"))
LIVE_RETRY_BUFFER_S = int(os.getenv("LIVE_RETRY_BUFFER_S", "5"))
LIVE_RETRY_MIN_SECONDS_REMAINING = LAST_MIN_SECONDS_GUARD + LIVE_RETRY_BUFFER_S

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
# Minimum positive EV required before the signal engine is even queried.
# EV = fair_prob × (1 / market_odds) − 1
# Override via env to tune without restarting.
MINIMUM_EDGE_THRESHOLD = float(os.getenv("MINIMUM_EDGE_THRESHOLD", "0.05"))  # 5% min EV

# ── Telegram notifications ────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN       = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID         = os.getenv("TELEGRAM_CHAT_ID", "")
TELEGRAM_ENABLED         = bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)
TELEGRAM_STATUS_INTERVAL_S = int(os.getenv("TELEGRAM_STATUS_INTERVAL_S", "300"))  # every 5 min
SIGNAL_NOTIFY_MIN_STREAK = int(os.getenv("SIGNAL_NOTIFY_MIN_STREAK", "2"))
SIGNAL_NOTIFY_IMMEDIATE_CONF = float(os.getenv("SIGNAL_NOTIFY_IMMEDIATE_CONF", "0.88"))

# ── Bandar Push Detection (Anti Whale Push) ─────────────────────────────────
BANDAR_FINAL_SECONDS       = 45      # final 45 detik = zona paling berbahaya
BANDAR_ODDS_VEL_THRESHOLD  = 0.008   # > 8 mOdds/detik = tanda bandar masuk
BANDAR_CVD_ACCEL_THRESHOLD = 0.005   # CVD acceleration ekstrem
LATE_DYNAMIC_MIN_CONF      = 0.85    # min confidence di final <45 detik

# ── ML signal engine ─────────────────────────────────────────────────────────
ML_MODELS_DIR             = os.getenv("ML_MODELS_DIR", "artifacts/ml")
ML_PROMOTION_STATE        = os.getenv("ML_PROMOTION_STATE", "shadow").lower()
ML_MIN_TRAIN_ROWS         = int(os.getenv("ML_MIN_TRAIN_ROWS", "500"))
ML_MIN_TRAIN_WINDOWS      = int(os.getenv("ML_MIN_TRAIN_WINDOWS", "50"))
ML_MIN_PROMOTE_ROWS       = int(os.getenv("ML_MIN_PROMOTE_ROWS", "1000"))
ML_MIN_PROMOTE_WINDOWS    = int(os.getenv("ML_MIN_PROMOTE_WINDOWS", "100"))
ML_RETRAIN_HOUR_UTC       = int(os.getenv("ML_RETRAIN_HOUR_UTC", "0"))
ML_RETRAIN_MINUTE_UTC     = int(os.getenv("ML_RETRAIN_MINUTE_UTC", "15"))
ML_MODEL_STALE_HOURS      = int(os.getenv("ML_MODEL_STALE_HOURS", "72"))
ML_AUTO_PROMOTE           = os.getenv("ML_AUTO_PROMOTE", "true").lower() == "true"
PERFORMANCE_HISTORY_FILENAME = os.getenv("PERFORMANCE_HISTORY_FILENAME", "performance_history.json")
ML_PROMOTION_AP_MARGIN    = float(os.getenv("ML_PROMOTION_AP_MARGIN", "0.03"))
ML_PROMOTION_MAX_BRIER    = float(os.getenv("ML_PROMOTION_MAX_BRIER", "0.25"))
ML_PROMOTION_MAX_BRIER_DEGRADE = float(os.getenv("ML_PROMOTION_MAX_BRIER_DEGRADE", "0.01"))
ML_THRESHOLD_MODE         = os.getenv("ML_THRESHOLD_MODE", "auto").strip().lower()
ML_MIN_EXEC_WIN_RATE      = float(os.getenv("ML_MIN_EXEC_WIN_RATE", "0.80"))
ML_TARGET_EXEC_COVERAGE   = float(os.getenv("ML_TARGET_EXEC_COVERAGE", "0.60"))
ML_THRESHOLD_LOOKBACK_DAYS = int(os.getenv("ML_THRESHOLD_LOOKBACK_DAYS", "14"))
ML_THRESHOLD_MIN_WINDOWS  = int(os.getenv("ML_THRESHOLD_MIN_WINDOWS", "40"))
OBSERVE_CARRY_MIN_CONF    = float(os.getenv("OBSERVE_CARRY_MIN_CONF", "0.78"))
SOFT_PENALTY_CONF_BUMP    = float(os.getenv("SOFT_PENALTY_CONF_BUMP", "0.02"))
SOFT_PENALTY_KELLY_MULTIPLIER = float(os.getenv("SOFT_PENALTY_KELLY_MULTIPLIER", "0.50"))
LATE_HARD_RISK_SECONDS    = int(os.getenv("LATE_HARD_RISK_SECONDS", "25"))
ML_PROMOTION_WARN_AP_STD  = float(os.getenv("ML_PROMOTION_WARN_AP_STD", "0.05"))
ML_PROMOTION_BLOCK_AP_STD = float(os.getenv("ML_PROMOTION_BLOCK_AP_STD", "0.08"))
ML_PROMOTION_BLOCK_AP_DROP = float(os.getenv("ML_PROMOTION_BLOCK_AP_DROP", "0.05"))
ML_DRIFT_LOOKBACK_ROWS    = int(os.getenv("ML_DRIFT_LOOKBACK_ROWS", "50"))
ML_DRIFT_CHECK_INTERVAL_MIN = int(os.getenv("ML_DRIFT_CHECK_INTERVAL_MIN", "60"))
ML_DRIFT_AP_DROP          = float(os.getenv("ML_DRIFT_AP_DROP", "0.07"))

# ── UI ────────────────────────────────────────────────────────────────────────
UI_REFRESH_S = 1.0
TRADE_HISTORY_REFRESH_S = 2.0
SETTLEMENT_MAX_DIFF_S = int(os.getenv("SETTLEMENT_MAX_DIFF_S", "15"))
SETTLEMENT_GRACE_PERIOD_S = int(os.getenv("SETTLEMENT_GRACE_PERIOD_S", "300"))  # 5 min grace before accepting Binance-only settlement
SETTLEMENT_POLL_MIN_PRIORITY = int(os.getenv("SETTLEMENT_POLL_MIN_PRIORITY", "300"))  # wait for at least this priority (300 = pyth/gamma; 400 = chainlink ws)
AUDIT_ML_LABELS = os.getenv("AUDIT_ML_LABELS", "false").lower() == "true"
ORACLE_DIVERGENCE_ALERT_USD = float(os.getenv("ORACLE_DIVERGENCE_ALERT_USD", "15.0"))
SKIP_ON_HIGH_DIVERGENCE = os.getenv("SKIP_ON_HIGH_DIVERGENCE", "false").lower() == "true"
MAX_BET_FRACTION = float(os.getenv("MAX_BET_FRACTION", "0.05"))  # 5% of bankroll per trade cap

# ── Startup validation ────────────────────────────────────────────────────────
_BASE_REQUIRED = [
    ("POLY_FUNDER",        POLY_FUNDER),
    ("POLY_ADDRESS",       POLY_ADDRESS),
    ("POLY_API_KEY",       POLY_API_KEY),
    ("POLY_SECRET",        POLY_SECRET),
    ("POLY_PASSPHRASE",    POLY_PASSPHRASE),
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
  signals_YYYY-MM-DD.jsonl — every runtime signal snapshot
  prices_YYYY-MM-DD.jsonl  — 5-second BTC price + volume snapshots
  prediction_analytics_YYYY-MM-DD.jsonl — unified prediction/shadow/trade analytics
  settlements_YYYY-MM-DD.jsonl — market settlement registry for label truth
  claims_YYYY-MM-DD.jsonl — claim discovery/queue/execution lifecycle
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

    @property
    def performance_history_path(self) -> Path:
        return self._dir / PERFORMANCE_HISTORY_FILENAME

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
        row_id: str = "",
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
        """Record a runtime signal decision and its market context."""
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        self._append(f"signals_{today}.jsonl", {
            "ts":            self._ts(),
            "row_id":        row_id,
            "signal":        signal.signal,
            "confidence":    signal.confidence,
            "raw_confidence": getattr(signal, "raw_confidence", signal.confidence),
            "reason":        signal.reason,
            "source":        getattr(signal, "source", "unknown"),
            "model_version": getattr(signal, "model_version", ""),
            "promotion_state": getattr(signal, "promotion_state", ""),
            "prob_up":       getattr(signal, "prob_up", 0.5),
            "prob_down":     getattr(signal, "prob_down", 0.5),
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

    def log_ml_feature(self, feature_row: dict) -> None:
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        self._append(f"ml_features_{today}.jsonl", feature_row)

    def log_ml_label(self, label_row: dict) -> None:
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        self._append(f"ml_labels_{today}.jsonl", label_row)

    def log_settlement(self, settlement_row: dict) -> None:
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        self._append(f"settlements_{today}.jsonl", settlement_row)

    def log_claim_state(self, claim_record) -> None:
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        payload = claim_record.to_record() if hasattr(claim_record, "to_record") else dict(claim_record)
        self._append(f"claims_{today}.jsonl", {
            "ts": self._ts(),
            **payload,
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
            "prediction_row_id": getattr(position, "prediction_row_id", ""),
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
            "prediction_row_id": getattr(position, "prediction_row_id", ""),
            "simulated":    position.simulated,
            "placed_at":    position.placed_at.isoformat(),
            "window_end_at": position.window_end_at.isoformat() if position.window_end_at else "",
            "elapsed_at_bet": position.elapsed_at_bet,
            "gap_pct_at_bet": position.gap_pct_at_bet,
            "ai_confidence": position.ai_confidence,
            "ai_raw_confidence": position.ai_raw_confidence,
            "signal_alignment": position.signal_alignment,
        })

    def log_prediction_state(self, record) -> None:
        """Persist the latest prediction snapshot for a feature row."""
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        self._append(f"prediction_analytics_{today}.jsonl", {
            "ts":                  self._ts(),
            "event":               "prediction_state",
            "row_id":              record.row_id,
            "condition_id":        record.condition_id,
            "window_label":        record.window_label,
            "window_end_at":       record.window_end_at.isoformat() if record.window_end_at else "",
            "beat_price":          record.beat_price,
            "mode":                record.mode,
            "signal":              record.signal,
            "predicted_direction": record.predicted_direction,
            "decision_action":     record.decision_action,
            "executed_order_id":   record.executed_order_id,
            "simulated_order_id":  record.simulated_order_id,
            "confidence":          record.confidence,
            "raw_confidence":      record.raw_confidence,
            "source":              record.source,
            "model_version":       record.model_version,
            "promotion_state":     record.promotion_state,
            "prob_up":             record.prob_up,
            "prob_down":           record.prob_down,
            "alignment":           record.alignment,
            "execution_allowed":   record.execution_allowed,
            "blocked_gate":        record.blocked_gate,
            "blocked_reason":      record.blocked_reason,
            "phase_bucket":        record.phase_bucket,
            "execution_bucket":    record.execution_bucket,
            "seconds_remaining":   record.seconds_remaining,
            "btc_price":           record.btc_price,
            "up_odds":             record.up_odds,
            "down_odds":           record.down_odds,
            "signal_reason":       record.signal_reason,
            "decision_reason":     record.decision_reason,
            "runtime_skip_reason_code": record.runtime_skip_reason_code,
            "decision_skip_reason_code": record.decision_skip_reason_code,
            "candidate_confidence_floor": record.candidate_confidence_floor,
            "execution_required_confidence": record.execution_required_confidence,
            "threshold_profile_version": record.threshold_profile_version,
            "threshold_source":    record.threshold_source,
            "carry_from_observe":  record.carry_from_observe,
            "candidate_phase":     record.candidate_phase,
            "action_phase":        record.action_phase,
            "reservation_locked":  record.reservation_locked,
            "reservation_carried_to_execution": record.reservation_carried_to_execution,
            "soft_penalties_applied": record.soft_penalties_applied,
            "notification_locked": record.notification_locked,
            "notification_sent":   record.notification_sent,
            "notification_signal": record.notification_signal,
            "notification_gate":   record.notification_gate,
            "placement_failure_code": record.placement_failure_code,
            "placement_failure_reason": record.placement_failure_reason,
            "placement_retryable": record.placement_retryable,
            "placement_attempt_consumed": record.placement_attempt_consumed,
            "placement_attempt_count": record.placement_attempt_count,
            "last_attempted_at":   record.last_attempted_at.isoformat() if record.last_attempted_at else "",
            "sample_seq":          record.sample_seq,
            "counterfactual_pnl":  record.counterfactual_pnl,
            "paper_trade_won":     record.paper_trade_won,
            "live_trade_won":      record.live_trade_won,
            "last_updated_at":     record.last_updated_at.isoformat() if record.last_updated_at else "",
        })

    def log_prediction_blocked(self, record) -> None:
        """Persist a blocked BUY prediction for later shadow analysis."""
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        self._append(f"prediction_analytics_{today}.jsonl", {
            "ts":                  self._ts(),
            "event":               "prediction_blocked",
            "row_id":              record.row_id,
            "condition_id":        record.condition_id,
            "window_label":        record.window_label,
            "window_end_at":       record.window_end_at.isoformat() if record.window_end_at else "",
            "beat_price":          record.beat_price,
            "mode":                record.mode,
            "signal":              record.signal,
            "predicted_direction": record.predicted_direction,
            "decision_action":     record.decision_action,
            "confidence":          record.confidence,
            "raw_confidence":      record.raw_confidence,
            "source":              record.source,
            "model_version":       record.model_version,
            "promotion_state":     record.promotion_state,
            "prob_up":             record.prob_up,
            "prob_down":           record.prob_down,
            "alignment":           record.alignment,
            "execution_allowed":   record.execution_allowed,
            "blocked_gate":        record.blocked_gate,
            "blocked_reason":      record.blocked_reason,
            "phase_bucket":        record.phase_bucket,
            "execution_bucket":    record.execution_bucket,
            "seconds_remaining":   record.seconds_remaining,
            "btc_price":           record.btc_price,
            "up_odds":             record.up_odds,
            "down_odds":           record.down_odds,
            "signal_reason":       record.signal_reason,
            "decision_reason":     record.decision_reason,
            "runtime_skip_reason_code": record.runtime_skip_reason_code,
            "decision_skip_reason_code": record.decision_skip_reason_code,
            "candidate_confidence_floor": record.candidate_confidence_floor,
            "execution_required_confidence": record.execution_required_confidence,
            "threshold_profile_version": record.threshold_profile_version,
            "threshold_source":    record.threshold_source,
            "carry_from_observe":  record.carry_from_observe,
            "candidate_phase":     record.candidate_phase,
            "action_phase":        record.action_phase,
            "reservation_locked":  record.reservation_locked,
            "reservation_carried_to_execution": record.reservation_carried_to_execution,
            "soft_penalties_applied": record.soft_penalties_applied,
            "notification_locked": record.notification_locked,
            "notification_sent":   record.notification_sent,
            "notification_signal": record.notification_signal,
            "notification_gate":   record.notification_gate,
            "placement_failure_code": record.placement_failure_code,
            "placement_failure_reason": record.placement_failure_reason,
            "placement_retryable": record.placement_retryable,
            "placement_attempt_consumed": record.placement_attempt_consumed,
            "placement_attempt_count": record.placement_attempt_count,
            "last_attempted_at":   record.last_attempted_at.isoformat() if record.last_attempted_at else "",
            "sample_seq":          record.sample_seq,
            "last_updated_at":     record.last_updated_at.isoformat() if record.last_updated_at else "",
        })

    def log_prediction_resolved(self, record) -> None:
        """Persist a resolved prediction outcome."""
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        self._append(f"prediction_analytics_{today}.jsonl", {
            "ts":                  self._ts(),
            "event":               "prediction_resolved",
            "row_id":              record.row_id,
            "condition_id":        record.condition_id,
            "window_label":        record.window_label,
            "window_end_at":       record.window_end_at.isoformat() if record.window_end_at else "",
            "beat_price":          record.beat_price,
            "mode":                record.mode,
            "signal":              record.signal,
            "predicted_direction": record.predicted_direction,
            "decision_action":     record.decision_action,
            "executed_order_id":   record.executed_order_id,
            "simulated_order_id":  record.simulated_order_id,
            "confidence":          record.confidence,
            "raw_confidence":      record.raw_confidence,
            "source":              record.source,
            "model_version":       record.model_version,
            "promotion_state":     record.promotion_state,
            "prob_up":             record.prob_up,
            "prob_down":           record.prob_down,
            "alignment":           record.alignment,
            "execution_allowed":   record.execution_allowed,
            "blocked_gate":        record.blocked_gate,
            "blocked_reason":      record.blocked_reason,
            "phase_bucket":        record.phase_bucket,
            "execution_bucket":    record.execution_bucket,
            "seconds_remaining":   record.seconds_remaining,
            "btc_price":           record.btc_price,
            "up_odds":             record.up_odds,
            "down_odds":           record.down_odds,
            "signal_reason":       record.signal_reason,
            "decision_reason":     record.decision_reason,
            "runtime_skip_reason_code": record.runtime_skip_reason_code,
            "decision_skip_reason_code": record.decision_skip_reason_code,
            "candidate_confidence_floor": record.candidate_confidence_floor,
            "execution_required_confidence": record.execution_required_confidence,
            "threshold_profile_version": record.threshold_profile_version,
            "threshold_source":    record.threshold_source,
            "carry_from_observe":  record.carry_from_observe,
            "candidate_phase":     record.candidate_phase,
            "action_phase":        record.action_phase,
            "reservation_locked":  record.reservation_locked,
            "reservation_carried_to_execution": record.reservation_carried_to_execution,
            "soft_penalties_applied": record.soft_penalties_applied,
            "notification_locked": record.notification_locked,
            "notification_sent":   record.notification_sent,
            "notification_signal": record.notification_signal,
            "notification_gate":   record.notification_gate,
            "placement_failure_code": record.placement_failure_code,
            "placement_failure_reason": record.placement_failure_reason,
            "placement_retryable": record.placement_retryable,
            "placement_attempt_consumed": record.placement_attempt_consumed,
            "placement_attempt_count": record.placement_attempt_count,
            "last_attempted_at":   record.last_attempted_at.isoformat() if record.last_attempted_at else "",
            "sample_seq":          record.sample_seq,
            "actual_winner":       record.actual_winner,
            "prediction_correct":  record.prediction_correct,
            "counterfactual_pnl":  record.counterfactual_pnl,
            "paper_trade_won":     record.paper_trade_won,
            "live_trade_won":      record.live_trade_won,
            "resolved_at":         record.resolved_at.isoformat() if record.resolved_at else "",
        })

    def log_prediction_trade_failed(self, record) -> None:
        """Persist an attempted trade that failed before opening a position."""
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        self._append(f"prediction_analytics_{today}.jsonl", {
            "ts":                  self._ts(),
            "event":               "prediction_trade_failed",
            "row_id":              record.row_id,
            "condition_id":        record.condition_id,
            "window_label":        record.window_label,
            "window_end_at":       record.window_end_at.isoformat() if record.window_end_at else "",
            "beat_price":          record.beat_price,
            "mode":                record.mode,
            "signal":              record.signal,
            "predicted_direction": record.predicted_direction,
            "decision_action":     record.decision_action,
            "confidence":          record.confidence,
            "raw_confidence":      record.raw_confidence,
            "source":              record.source,
            "model_version":       record.model_version,
            "promotion_state":     record.promotion_state,
            "prob_up":             record.prob_up,
            "prob_down":           record.prob_down,
            "alignment":           record.alignment,
            "execution_allowed":   record.execution_allowed,
            "execution_bucket":    record.execution_bucket,
            "seconds_remaining":   record.seconds_remaining,
            "btc_price":           record.btc_price,
            "up_odds":             record.up_odds,
            "down_odds":           record.down_odds,
            "signal_reason":       record.signal_reason,
            "decision_reason":     record.decision_reason,
            "placement_failure_code": record.placement_failure_code,
            "placement_failure_reason": record.placement_failure_reason,
            "placement_retryable": record.placement_retryable,
            "placement_attempt_consumed": record.placement_attempt_consumed,
            "placement_attempt_count": record.placement_attempt_count,
            "last_attempted_at":   record.last_attempted_at.isoformat() if record.last_attempted_at else "",
            "last_updated_at":     record.last_updated_at.isoformat() if record.last_updated_at else "",
        })

    def log_trade_execution_resolved(self, position, won: bool | None) -> None:
        """Persist a settled executed trade in the unified prediction analytics stream."""
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        self._append(f"prediction_analytics_{today}.jsonl", {
            "ts":                 self._ts(),
            "event":              "paper_trade_resolved" if position.simulated else "live_trade_resolved",
            "prediction_row_id":  getattr(position, "prediction_row_id", ""),
            "condition_id":       position.condition_id,
            "window_end_at":      position.window_end_at.isoformat() if position.window_end_at else "",
            "executed_order_id":  position.order_id,
            "simulated_order_id": position.order_id if position.simulated else "",
            "direction":          position.direction,
            "paper_trade_won":    won if position.simulated else None,
            "live_trade_won":     won if not position.simulated else None,
            "amount_usdc":        position.amount_usdc,
            "entry_price":        position.entry_price,
            "pnl":                position.pnl,
            "placed_at":          position.placed_at.isoformat(),
            "confidence":         position.ai_confidence,
            "raw_confidence":     position.ai_raw_confidence,
            "alignment":          position.signal_alignment,
            "execution_bucket":   getattr(position, "execution_bucket", ""),
            "resolved_at":        self._ts(),
        })

    def log_paper_prediction_state(self, record) -> None:
        self.log_prediction_state(record)

    def log_paper_prediction_resolved(self, record) -> None:
        self.log_prediction_resolved(record)

    def log_paper_trade_resolved(self, position, won: bool | None) -> None:
        self.log_trade_execution_resolved(position, won)

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

    def load_recent_trade_history(self, limit: int = 20, lookback_days: int = 7) -> list[TradeHistoryEntry]:
        """Load recent settled bets for the terminal history panel."""
        cutoff = (datetime.now(_UTC) - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
        trade_files = sorted(
            f for f in self._dir.glob("trades_*.jsonl")
            if f.stem.rsplit("_", 1)[-1] >= cutoff
        )

        opens: dict[str, dict] = {}
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
                        key = self._trade_key(record)
                        if not key:
                            continue
                        event = str(record.get("event", ""))
                        if event == "open":
                            opens[key] = record
                        elif event == "close" and record.get("status") in ("won", "lost"):
                            closes[key] = record
            except Exception:
                continue

        def _parse_dt(raw: object) -> datetime | None:
            if not isinstance(raw, str) or not raw:
                return None
            try:
                return datetime.fromisoformat(raw.replace("Z", "+00:00"))
            except Exception:
                return None

        entries: list[TradeHistoryEntry] = []
        for key, close_rec in closes.items():
            open_rec = opens.get(key, {})
            placed_at = _parse_dt(open_rec.get("placed_at")) or _parse_dt(close_rec.get("placed_at"))
            closed_at = _parse_dt(close_rec.get("ts")) or datetime.now(_UTC)
            status = str(close_rec.get("status", "")).lower()
            simulated = bool(close_rec.get("simulated", open_rec.get("simulated", False)))
            entries.append(TradeHistoryEntry(
                direction=str(close_rec.get("direction") or open_rec.get("direction") or "NONE"),
                amount_usdc=float(close_rec.get("amount_usdc", open_rec.get("amount_usdc", 0.0)) or 0.0),
                pnl=float(close_rec.get("pnl", 0.0) or 0.0),
                status=status,
                placed_at=placed_at,
                closed_at=closed_at,
                simulated=simulated,
                order_id=str(close_rec.get("order_id", open_rec.get("order_id", "")) or ""),
                condition_id=str(close_rec.get("condition_id", open_rec.get("condition_id", "")) or ""),
                entry_price=float(close_rec.get("entry_price", open_rec.get("entry_price", 0.0)) or 0.0),
            ))

        entries.sort(key=lambda entry: entry.closed_at, reverse=True)
        return entries[:limit]

    def load_claim_records(
        self,
        lookback_days: int = 90,
        *,
        today: str | None = None,
    ) -> tuple[dict[str, dict], dict[str, Any]]:
        if today is None:
            today = datetime.now(_UTC).strftime("%Y-%m-%d")

        cutoff = (datetime.now(_UTC) - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
        files = sorted(
            f for f in self._dir.glob("claims_*.jsonl")
            if f.stem.rsplit("_", 1)[-1] >= cutoff
        )

        latest_by_id: dict[str, dict] = {}
        claimed_today: set[str] = set()
        failed_today: set[str] = set()
        last_claim_success_at = ""
        last_claim_error = ""

        for path in files:
            try:
                with open(path, "r", encoding="utf-8") as handle:
                    for line in handle:
                        try:
                            record = json.loads(line)
                        except Exception:
                            continue
                        claim_id = str(record.get("claim_id", "") or "").strip()
                        if not claim_id:
                            continue
                        current = latest_by_id.get(claim_id)
                        record_ts = str(record.get("ts") or "")
                        current_ts = str(current.get("ts") or "") if current else ""
                        if current is None or record_ts >= current_ts:
                            latest_by_id[claim_id] = record

                        status = str(record.get("status", "") or "")
                        if record_ts[:10] == today:
                            if status == "confirmed":
                                claimed_today.add(claim_id)
                                last_claim_success_at = max(last_claim_success_at, record_ts)
                            elif status == "failed":
                                failed_today.add(claim_id)
                                last_claim_error = str(record.get("error_message", "") or record.get("error_code", "") or "")
            except Exception:
                continue

        server_condition_ids = {
            str(record.get("condition_id", "") or "")
            for record in latest_by_id.values()
            if str(record.get("status", "")) != "expected_pending"
        }
        counts = {
            "claimable_total": round(
                sum(
                    float(record.get("claimable_amount", 0.0) or 0.0)
                    for record in latest_by_id.values()
                    if str(record.get("status", "")) in ("discovered", "queued", "submitted", "skipped", "failed")
                ),
                6,
            ),
            "expected_claimable_total": round(
                sum(
                    float(record.get("claimable_amount", 0.0) or 0.0)
                    for record in latest_by_id.values()
                    if str(record.get("status", "")) == "expected_pending"
                    and str(record.get("condition_id", "") or "") not in server_condition_ids
                ),
                6,
            ),
            "pending_claim_count": sum(
                1 for record in latest_by_id.values()
                if str(record.get("status", "")) in ("queued", "submitted")
            ),
            "expected_claim_pending_count": sum(
                1 for record in latest_by_id.values()
                if str(record.get("status", "")) == "expected_pending"
                and str(record.get("condition_id", "") or "") not in server_condition_ids
            ),
            "claimed_today_count": len(claimed_today),
            "failed_today_count": len(failed_today),
            "last_claim_success_at": last_claim_success_at,
            "last_claim_error": last_claim_error,
        }
        return latest_by_id, counts

    def load_prediction_analytics(
        self,
        lookback_days: int = 30,
        *,
        today: str | None = None,
    ) -> tuple[dict[str, dict], dict[str, Any]]:
        """Load pending unified prediction analytics and aggregate summary stats."""
        if today is None:
            today = datetime.now(_UTC).strftime("%Y-%m-%d")

        cutoff = (datetime.now(_UTC) - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
        files = sorted(
            [
                *(
                    f for f in self._dir.glob("prediction_analytics_*.jsonl")
                    if f.stem.rsplit("_", 1)[-1] >= cutoff
                ),
                *(
                    f for f in self._dir.glob("paper_analytics_*.jsonl")
                    if f.stem.rsplit("_", 1)[-1] >= cutoff
                ),
            ],
            key=lambda item: item.name,
        )

        pending_by_id: dict[str, dict] = {}
        resolved_predictions: set[str] = set()
        resolved_trade_keys: set[str] = set()
        trade_results_by_prediction: dict[str, bool] = {}
        trade_results_by_condition: dict[str, bool] = {}
        shadow_by_gate: dict[str, dict[str, float]] = defaultdict(
            lambda: {"count": 0, "resolved": 0, "hits": 0, "misses": 0, "counterfactual_pnl": 0.0}
        )
        counts: dict[str, Any] = {
            "prediction_correct_total": 0,
            "prediction_incorrect_total": 0,
            "prediction_correct_today": 0,
            "prediction_incorrect_today": 0,
            "paper_trade_wins_total": 0,
            "paper_trade_losses_total": 0,
            "paper_trade_wins_today": 0,
            "paper_trade_losses_today": 0,
            "live_trade_wins_total": 0,
            "live_trade_losses_total": 0,
            "live_trade_wins_today": 0,
            "live_trade_losses_today": 0,
            "shadow_by_gate": shadow_by_gate,
        }

        def _prediction_id(record: dict) -> str:
            return str(record.get("row_id") or record.get("prediction_row_id") or record.get("condition_id") or "").strip()

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
                        prediction_id = _prediction_id(record)
                        condition_id = str(record.get("condition_id", "")).strip()

                        if event in ("prediction_state", "prediction_blocked", "prediction_trade_failed"):
                            if prediction_id and prediction_id not in resolved_predictions:
                                pending_by_id[prediction_id] = record
                                gate = str(record.get("blocked_gate", "") or "")
                                if event == "prediction_blocked" and gate:
                                    shadow_by_gate[gate]["count"] += 1
                            continue

                        if event == "prediction_resolved":
                            if not prediction_id or prediction_id in resolved_predictions:
                                continue
                            resolved_predictions.add(prediction_id)
                            pending_by_id.pop(prediction_id, None)

                            correct = record.get("prediction_correct")
                            if isinstance(correct, bool):
                                if correct:
                                    counts["prediction_correct_total"] += 1
                                    if _is_today(record):
                                        counts["prediction_correct_today"] += 1
                                else:
                                    counts["prediction_incorrect_total"] += 1
                                    if _is_today(record):
                                        counts["prediction_incorrect_today"] += 1

                            gate = str(record.get("blocked_gate", "") or "")
                            if gate:
                                shadow_by_gate[gate]["resolved"] += 1
                                if correct is True:
                                    shadow_by_gate[gate]["hits"] += 1
                                elif correct is False:
                                    shadow_by_gate[gate]["misses"] += 1
                                shadow_by_gate[gate]["counterfactual_pnl"] += float(record.get("counterfactual_pnl", 0.0) or 0.0)

                            paper_trade_won = record.get("paper_trade_won")
                            live_trade_won = record.get("live_trade_won")
                            if isinstance(paper_trade_won, bool):
                                trade_results_by_prediction[prediction_id] = paper_trade_won
                                if condition_id:
                                    trade_results_by_condition[condition_id] = paper_trade_won
                            if isinstance(live_trade_won, bool):
                                trade_results_by_prediction[prediction_id] = live_trade_won
                                if condition_id:
                                    trade_results_by_condition[condition_id] = live_trade_won
                            continue

                        if event not in ("paper_trade_resolved", "live_trade_resolved"):
                            continue

                        won_value = record.get("paper_trade_won")
                        if not isinstance(won_value, bool):
                            won_value = record.get("live_trade_won")
                        if not isinstance(won_value, bool):
                            continue

                        order_id = str(record.get("executed_order_id") or record.get("simulated_order_id") or "").strip()
                        unique_key = order_id or f"{condition_id}:{record.get('placed_at', '')}"
                        if unique_key and unique_key not in resolved_trade_keys:
                            resolved_trade_keys.add(unique_key)
                            count_key = "paper_trade" if event == "paper_trade_resolved" else "live_trade"
                            if won_value:
                                counts[f"{count_key}_wins_total"] += 1
                                if _is_today(record):
                                    counts[f"{count_key}_wins_today"] += 1
                            else:
                                counts[f"{count_key}_losses_total"] += 1
                                if _is_today(record):
                                    counts[f"{count_key}_losses_today"] += 1

                        if prediction_id:
                            trade_results_by_prediction[prediction_id] = won_value
                        if condition_id:
                            trade_results_by_condition[condition_id] = won_value
            except Exception:
                continue

        for prediction_id, record in pending_by_id.items():
            condition_id = str(record.get("condition_id", "")).strip()
            if prediction_id in trade_results_by_prediction:
                won = trade_results_by_prediction[prediction_id]
                if str(record.get("mode", "paper")) == "live":
                    record["live_trade_won"] = won
                else:
                    record["paper_trade_won"] = won
            elif condition_id in trade_results_by_condition:
                won = trade_results_by_condition[condition_id]
                if str(record.get("mode", "paper")) == "live":
                    record["live_trade_won"] = won
                else:
                    record["paper_trade_won"] = won

        return pending_by_id, counts

    def load_paper_analytics(
        self,
        lookback_days: int = 30,
        *,
        today: str | None = None,
    ) -> tuple[dict[str, dict], dict[str, Any]]:
        return self.load_prediction_analytics(lookback_days=lookback_days, today=today)

    def compute_recent_participation_metrics(self, limit: int = 24) -> dict[str, Any]:
        files = sorted(self._dir.glob("prediction_analytics_*.jsonl"))
        windows: dict[str, dict[str, Any]] = {}
        for path in files:
            try:
                with open(path, "r", encoding="utf-8") as handle:
                    for line in handle:
                        try:
                            record = json.loads(line)
                        except Exception:
                            continue
                        condition_id = str(record.get("condition_id", "") or "").strip()
                        if not condition_id:
                            continue
                        event = str(record.get("event", "") or "")
                        bucket = windows.setdefault(
                            condition_id,
                            {
                                "resolved_at": "",
                                "has_buy_prediction": False,
                                "reserved_signal": False,
                                "executed_bet": False,
                                "placement_failed": False,
                                "retryable_failure": False,
                                "placement_failure_codes": {},
                                "execution_bucket": "",
                                "won": None,
                                "blocked_by_gate": {},
                            },
                        )
                        signal = str(record.get("signal", "") or "")
                        if signal in ("BUY_UP", "BUY_DOWN"):
                            bucket["has_buy_prediction"] = True
                        if bool(record.get("reservation_locked", False)):
                            bucket["reserved_signal"] = True
                        if str(record.get("execution_bucket", "") or ""):
                            bucket["execution_bucket"] = str(record.get("execution_bucket", "") or "")
                        if event == "prediction_trade_failed":
                            bucket["placement_failed"] = True
                            retryable = bool(record.get("placement_retryable", False))
                            bucket["retryable_failure"] = bucket["retryable_failure"] or retryable
                            failure_code = str(record.get("placement_failure_code", "") or "")
                            if failure_code:
                                bucket["placement_failure_codes"][failure_code] = (
                                    int(bucket["placement_failure_codes"].get(failure_code, 0) or 0) + 1
                                )
                        elif event == "prediction_resolved":
                            resolved_at = str(record.get("resolved_at") or record.get("ts") or "")
                            if resolved_at:
                                bucket["resolved_at"] = resolved_at
                            gate = str(record.get("blocked_gate", "") or "")
                            correct = record.get("prediction_correct")
                            if gate and isinstance(correct, bool):
                                stats = bucket["blocked_by_gate"].setdefault(gate, {"hits": 0, "total": 0})
                                stats["total"] += 1
                                if correct:
                                    stats["hits"] += 1
                            won_value = record.get("paper_trade_won")
                            if not isinstance(won_value, bool):
                                won_value = record.get("live_trade_won")
                            if isinstance(won_value, bool):
                                bucket["executed_bet"] = True
                                bucket["won"] = won_value
                        elif event in ("paper_trade_resolved", "live_trade_resolved"):
                            resolved_at = str(record.get("resolved_at") or record.get("ts") or "")
                            if resolved_at:
                                bucket["resolved_at"] = resolved_at
                            won_value = record.get("paper_trade_won")
                            if not isinstance(won_value, bool):
                                won_value = record.get("live_trade_won")
                            if isinstance(won_value, bool):
                                bucket["executed_bet"] = True
                                bucket["won"] = won_value
            except Exception:
                continue

        resolved_windows = [
            record for record in windows.values()
            if str(record.get("resolved_at", "")).strip()
        ]
        resolved_windows.sort(key=lambda item: str(item.get("resolved_at", "")))
        recent = resolved_windows[-limit:]
        total = len(recent)
        metrics: dict[str, Any] = {
            "window_count": total,
            "buy_prediction_rate": 0.0,
            "reserved_signal_rate": 0.0,
            "executed_bet_rate": 0.0,
            "placement_failed_rate": 0.0,
            "retryable_failure_rate": 0.0,
            "placement_failure_by_code": {},
            "blocked_profitable_rate": {},
            "win_rate_by_execution_bucket": {},
            "threshold_counterfactuals": {},
        }
        if total == 0:
            return metrics

        metrics["buy_prediction_rate"] = round(sum(1 for row in recent if row.get("has_buy_prediction")) / total, 4)
        metrics["reserved_signal_rate"] = round(sum(1 for row in recent if row.get("reserved_signal")) / total, 4)
        metrics["executed_bet_rate"] = round(sum(1 for row in recent if row.get("executed_bet")) / total, 4)
        metrics["placement_failed_rate"] = round(sum(1 for row in recent if row.get("placement_failed")) / total, 4)
        metrics["retryable_failure_rate"] = round(sum(1 for row in recent if row.get("retryable_failure")) / total, 4)

        gate_hits: dict[str, int] = defaultdict(int)
        gate_totals: dict[str, int] = defaultdict(int)
        bucket_wins: dict[str, int] = defaultdict(int)
        bucket_totals: dict[str, int] = defaultdict(int)
        failure_codes: dict[str, int] = defaultdict(int)
        for row in recent:
            for gate, stats in row.get("blocked_by_gate", {}).items():
                gate_hits[gate] += int(stats.get("hits", 0) or 0)
                gate_totals[gate] += int(stats.get("total", 0) or 0)
            for failure_code, count in dict(row.get("placement_failure_codes", {})).items():
                failure_codes[str(failure_code)] += int(count or 0)
            execution_bucket = str(row.get("execution_bucket", "") or "")
            if execution_bucket and isinstance(row.get("won"), bool):
                bucket_totals[execution_bucket] += 1
                if row["won"]:
                    bucket_wins[execution_bucket] += 1

        metrics["blocked_profitable_rate"] = {
            gate: round(gate_hits[gate] / total_count, 4)
            for gate, total_count in gate_totals.items()
            if total_count > 0
        }
        metrics["win_rate_by_execution_bucket"] = {
            bucket: round(bucket_wins[bucket] / total_count, 4)
            for bucket, total_count in bucket_totals.items()
            if total_count > 0
        }
        metrics["placement_failure_by_code"] = dict(sorted(failure_codes.items()))
        tuning_windows = _load_threshold_tuning_windows(self._dir, lookback_days=ML_THRESHOLD_LOOKBACK_DAYS)
        if tuning_windows:
            metrics["threshold_counterfactuals"] = _threshold_counterfactuals(tuning_windows[-limit:])
        return metrics

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

    # Percentage-of-bankroll cap: prevents the hard dollar ceiling from making
    # Kelly non-functional as the bankroll grows or shrinks. The hard max_bet
    # still acts as an absolute floor guard (whichever is lower wins).
    pct_cap = bankroll * MAX_BET_FRACTION
    effective_max = min(max_bet, pct_cap)
    return max(min_bet, min(effective_max, round(bet, 2)))


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


def compute_dip_label(prices: list[float], beat_price: float, btc_price: float) -> str:
    window = prices[-20:] if len(prices) >= 20 else prices
    if len(window) < 4:
        return "INSUFFICIENT_DATA"

    above_count = sum(1 for price in window if price >= beat_price)
    above_pct = above_count / len(window) * 100.0
    below_pct = 100.0 - above_pct

    if above_pct >= 60.0 and btc_price < beat_price:
        return "TEMPORARY_DIP"
    if below_pct >= 80.0:
        return "SUSTAINED_MOVE"
    if above_pct >= 80.0:
        return "SUSTAINED_ABOVE"
    return "MIXED"


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
# Source: signal_types.py
# ══════════════════════════════════════════════════════════════════════════════

"""Signal payload produced by the local ML/fallback runtime."""


@dataclass
class AISignal:
    signal: str         # "BUY_UP" | "BUY_DOWN" | "SKIP"
    confidence: float   # 0.0 – 1.0
    reason: str
    latency_ms: int = 0
    timestamp: float = field(default_factory=time.time)
    dip_label: str = "UNKNOWN"
    raw_confidence: float = 0.0
    source: str = "unknown"
    model_version: str = ""
    prob_up: float = 0.5
    prob_down: float = 0.5
    promotion_state: str = ""
    runtime_skip_reason_code: str = ""
    soft_penalties_applied: list[str] = field(default_factory=list)
    candidate_confidence_floor: float = 0.0
    threshold_profile_version: str = ""
    threshold_source: str = "default"
    candidate_phase: str = ""
    action_phase: str = ""
    carry_from_observe: bool = False


# ══════════════════════════════════════════════════════════════════════════════
# Source: decision_maker.py
# ══════════════════════════════════════════════════════════════════════════════

"""Pure decision layer for the trading bot.

DecisionMaker is synchronous and stateless — no I/O, no async — so it is
trivially unit-testable independent of market state or network calls.

Flow (called from bot._trading_loop):

  1. bot builds DecisionContext with current market/indicator data (no ai_signal yet)
  2. bot calls DecisionMaker.pre_ai_check(ctx)
       → returns TradeDecision(SKIP) if a market gate fails  (saves a model call)
       → returns None if all pre-signal gates pass (proceed to signal engine)
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
GATE_DIR_CONFLICT         = "GATE_DIR_CONFLICT"         # signal direction conflicts with indicator consensus
GATE_AI_HOLD              = "GATE_AI_HOLD"              # signal engine returned SKIP
GATE_LOW_ALIGNMENT        = "GATE_LOW_ALIGNMENT"        # indicator families do not agree enough
GATE_LOW_CONF             = "GATE_LOW_CONF"             # signal confidence below threshold
GATE_OK                   = "OK"                        # all gates passed → BUY
GATE_ALREADY_OPEN         = "GATE_ALREADY_OPEN"         # position already open in this window
GATE_ALREADY_ATTEMPTED    = "GATE_ALREADY_ATTEMPTED"    # window consumed by a successful/terminal attempt
GATE_RETRY_COOLDOWN       = "GATE_RETRY_COOLDOWN"       # waiting before retrying a retryable placement failure
GATE_RETRY_WINDOW_CLOSED  = "GATE_RETRY_WINDOW_CLOSED"  # retry window closed due to remaining time
GATE_RETRY_LIMIT          = "GATE_RETRY_LIMIT"          # retry budget exhausted for this window


# ── Data classes ─────────────────────────────────────────────────────────────

@dataclass
class DecisionContext:
    """All inputs the DecisionMaker needs to evaluate a potential trade.

    Build this before the signal call (ai_signal=None), pass to pre_ai_check().
    After the signal call, set ai_signal and pass to evaluate().
    """
    win: Any                        # WindowInfo
    elapsed_s: int
    seconds_remaining: int
    btc_price: float
    up_odds: float
    down_odds: float
    snap: Any                       # IndicatorSnapshot
    ai_signal: Any | None = None    # AISignal — set after pre_ai_check passes

    # Dip analysis from the signal builder (passed through so the
    # DecisionMaker can apply the same logic independently of the signal call)
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
    required_confidence: float = 0.0
    soft_penalties_applied: list[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)


# ── Decision maker ────────────────────────────────────────────────────────────

class DecisionMaker:
    """Stateless evaluator — create one instance and reuse across calls."""

    def _check_late_reversal_risk(self, ctx: DecisionContext) -> TradeDecision | None:
        """Hard block only for the riskiest late proximity setups."""
        if ctx.seconds_remaining > LATE_RISK_WINDOW_S:
            return None

        gap_pct = abs(ctx.btc_price - ctx.win.beat_price) / ctx.win.beat_price * 100
        if gap_pct >= LATE_GAP_RISK_PCT:
            return None

        if ctx.seconds_remaining < LATE_HARD_RISK_SECONDS:
            return TradeDecision(
                action="SKIP",
                direction=ctx.snap.direction_bias or "NONE",
                confidence=0.0,
                reason=f"LATE_PROXIMITY_RISK: gap={gap_pct:.3f}% < {LATE_GAP_RISK_PCT:.2f}% di final {ctx.seconds_remaining}s (align={ctx.signal_alignment}/6)",
                gate="GATE_LATE_PROXIMITY_RISK",
            )
        return None
    
    def _check_bandar_push(self, ctx: DecisionContext) -> TradeDecision | None:
        """Hard block only for the strongest final-seconds bandar push."""
        if ctx.seconds_remaining > BANDAR_FINAL_SECONDS:
            return None

        snap = ctx.snap
        if snap is None:
            return None

        phase_bucket = _phase_bucket_from_timing(ctx.elapsed_s, ctx.seconds_remaining)
        vel = abs(snap.odds_vel_value)
        accel = abs(snap.odds_vel_accel)
        vel_threshold = BANDAR_ODDS_VEL_THRESHOLD
        accel_threshold = BANDAR_CVD_ACCEL_THRESHOLD
        if not _bet_frequency_phase_at_least("B"):
            hard_multiplier = 1.0
        else:
            hard_multiplier = 1.5 if phase_bucket in ("RESERVE", "EARLY_EXEC") and ctx.seconds_remaining >= LATE_HARD_RISK_SECONDS else 1.0

        if vel > vel_threshold * hard_multiplier:
            return TradeDecision(
                action="SKIP",
                direction=ctx.snap.direction_bias or "NONE",
                confidence=0.0,
                reason=f"BANDAR_PUSH_DETECTED: odds velocity {snap.odds_vel_value*1000:+.1f} mOdds/s (terlalu ekstrem di final {ctx.seconds_remaining}s)",
                gate="GATE_BANDAR_PUSH",
            )

        if accel > accel_threshold * hard_multiplier:
            return TradeDecision(
                action="SKIP",
                direction=ctx.snap.direction_bias or "NONE",
                confidence=0.0,
                reason=f"BANDAR_PUSH_DETECTED: CVD acceleration {snap.odds_vel_accel*1000:+.1f} mOdds/s² (smart money ekstrem di final {ctx.seconds_remaining}s)",
                gate="GATE_BANDAR_PUSH",
            )

        return None

    def soft_penalties(self, ctx: DecisionContext) -> list[str]:
        penalties: list[str] = []
        snap = ctx.snap
        if snap is None:
            return penalties
        phase_bucket = _phase_bucket_from_timing(ctx.elapsed_s, ctx.seconds_remaining)
        if phase_bucket not in ("RESERVE", "EARLY_EXEC"):
            return penalties

        if LATE_HARD_RISK_SECONDS <= ctx.seconds_remaining <= LATE_RISK_WINDOW_S:
            gap_pct = abs(ctx.btc_price - ctx.win.beat_price) / ctx.win.beat_price * 100 if ctx.win and ctx.win.beat_price > 0 else 0.0
            if gap_pct < LATE_GAP_RISK_PCT:
                penalties.append("SOFT_LATE_PROXIMITY_RISK")

        if LATE_HARD_RISK_SECONDS <= ctx.seconds_remaining <= BANDAR_FINAL_SECONDS:
            if not _bet_frequency_phase_at_least("B"):
                return penalties
            if (
                abs(_safe_float(getattr(snap, "odds_vel_value", 0.0), 0.0)) > BANDAR_ODDS_VEL_THRESHOLD
                or abs(_safe_float(getattr(snap, "odds_vel_accel", 0.0), 0.0)) > BANDAR_CVD_ACCEL_THRESHOLD
            ):
                penalties.append("SOFT_BANDAR_PUSH")

        return penalties

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

        # Keep only clearly negative-EV windows out of the signal path. Small or modest
        # positive EV is advisory now; the runtime still receives the full fair-value section.
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

    def apply_execution_policy(self, ctx: DecisionContext) -> TradeDecision:
        """Run post-prediction market and execution-quality gates.

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
        soft_penalties = list(signal.soft_penalties_applied or self.soft_penalties(ctx))
        if selected_odds <= 0.0 or selected_odds >= 1.0:
            return TradeDecision(
                action="SKIP", direction=ai_dir, confidence=signal.confidence,
                reason=f"{ai_dir} odds {selected_odds:.3f} invalid for execution",
                gate=GATE_LOW_ENTRY_ODDS,
                soft_penalties_applied=soft_penalties,
            )

        is_btc_above_beat = ctx.btc_price > ctx.win.beat_price
        natural_dir = "UP" if is_btc_above_beat else "DOWN"

        contrarian = (ai_dir != natural_dir)  # AI bets against current BTC position
        weak_consensus = ctx.signal_alignment <= 2
        is_temp_dip = ctx.dip_label == "TEMPORARY_DIP"
        # Sustained position: price has been on the same side as natural_dir for 80%+ of the window.
        # Betting contrarian against a sustained move requires the same high conviction.
        sustained_contrarian_position = (
            (ai_dir == "DOWN" and ctx.beat_above_ratio >= 0.80) or
            (ai_dir == "UP"  and ctx.beat_below_ratio >= 0.80)
        )

        if contrarian and (is_temp_dip or weak_consensus or sustained_contrarian_position):
            required = ctx.dir_conflict_min_conf
            if signal.confidence < required:
                conflict_reason = (
                    "TEMP_DIP" if is_temp_dip
                    else f"sustained {natural_dir} {ctx.beat_above_ratio if ai_dir == 'DOWN' else ctx.beat_below_ratio:.0%}" if sustained_contrarian_position
                    else "weak"
                )
                return TradeDecision(
                    action="SKIP", direction=ai_dir, confidence=signal.confidence,
                    reason=(
                        f"contrarian {ai_dir} vs {conflict_reason} "
                        f"alignment={ctx.signal_alignment} — "
                        f"need conf≥{required:.0%}, got {signal.confidence:.0%}"
                    ),
                    gate=GATE_DIR_CONFLICT,
                    required_confidence=required,
                    soft_penalties_applied=soft_penalties,
                )

        # Dynamic live-entry floor: alignment is advisory now, not a hard wall.
        phase_bucket = _phase_bucket_from_timing(ctx.elapsed_s, ctx.seconds_remaining)
        selected_model_edge = 0.0
        if ctx.fair_prob:
            selected_model_edge = ctx.fair_prob.get(
                "edge_up" if ai_dir == "UP" else "edge_down",
                0.0,
            )

        if ctx.signal_alignment >= ctx.min_signal_alignment:
            dynamic_floor = 0.60
            min_conf_edge = 0.03
        elif ctx.signal_alignment == ctx.min_signal_alignment - 1:
            dynamic_floor = 0.62
            min_conf_edge = 0.05
        elif ctx.signal_alignment == ctx.min_signal_alignment - 2:
            dynamic_floor = 0.66
            min_conf_edge = 0.07
        else:
            dynamic_floor = 0.74
            min_conf_edge = 0.10

        if selected_model_edge >= 0.20:
            min_conf_edge -= 0.01
        if selected_model_edge >= 0.35:
            min_conf_edge -= 0.01
        if ctx.dip_label in ("SUSTAINED_MOVE", "SUSTAINED_ABOVE"):
            min_conf_edge -= 0.01

        profile_floor = max(
            _safe_float(signal.candidate_confidence_floor, 0.0),
            _threshold_floor_for_bucket(phase_bucket),
        )
        min_conf_edge = max(0.02, min_conf_edge)
        required_conf = max(profile_floor, dynamic_floor, selected_odds + min_conf_edge)
        if "SOFT_LATE_PROXIMITY_RISK" in soft_penalties:
            required_conf += SOFT_PENALTY_CONF_BUMP
        if "SOFT_BANDAR_PUSH" in soft_penalties:
            required_conf += SOFT_PENALTY_CONF_BUMP

        if signal.confidence < required_conf:
            required_conf = max(profile_floor, dynamic_floor)
            if ctx.seconds_remaining < 45:
                required_conf = max(required_conf, LATE_DYNAMIC_MIN_CONF)

            if selected_model_edge >= 0.20:
                required_conf -= 0.01
            if selected_model_edge >= 0.35:
                required_conf -= 0.01
            if ctx.dip_label in ("SUSTAINED_MOVE", "SUSTAINED_ABOVE"):
                required_conf -= 0.01

            required_conf = max(profile_floor, 0.60, required_conf)  # safety floor
            required_conf = max(required_conf, selected_odds + min_conf_edge)
            if "SOFT_LATE_PROXIMITY_RISK" in soft_penalties:
                required_conf += SOFT_PENALTY_CONF_BUMP
            if "SOFT_BANDAR_PUSH" in soft_penalties:
                required_conf += SOFT_PENALTY_CONF_BUMP

            if signal.confidence < required_conf:
                return TradeDecision(
                    action="SKIP", direction=ai_dir, confidence=signal.confidence,
                    reason=(
                        f"conf={signal.confidence:.0%} < req={required_conf:.0%} "
                        f"(odds={selected_odds:.0%}, align={ctx.signal_alignment}/6, "
                        f"EV={selected_model_edge:+.1%}, late_window={ctx.seconds_remaining}s)"
                    ),
                    gate=GATE_LOW_CONF,
                    required_confidence=required_conf,
                    soft_penalties_applied=soft_penalties,
                )

        # All gates passed
        ai_dir = "UP" if signal.signal == "BUY_UP" else "DOWN"
        return TradeDecision(
            action="BUY", direction=ai_dir, confidence=signal.confidence,
            reason=f"conf={signal.confidence:.0%} {signal.reason[:80]}",
            gate=GATE_OK,
            required_confidence=required_conf,
            soft_penalties_applied=soft_penalties,
        )

    def evaluate(self, ctx: DecisionContext) -> TradeDecision:
        return self.apply_execution_policy(ctx)

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
import inspect
import json
import math
import re
import ssl
import time
from contextlib import suppress
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
    failure_code: str = ""
    retryable: bool = False
    attempt_consumed: bool = True


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
        self._session_lock = asyncio.Lock()
        self._client = self._build_client()
        self._http = self._build_http_client()
        self._session_generation = 0
        self._refresh_in_progress = False
        self._creds_refreshed_at = time.time()
        self._last_auth_success_at = 0.0
        self._last_auth_failure_at = 0.0
        self._last_heartbeat_ok_at = 0.0
        self._last_auth_error = ""
        self._consecutive_auth_failures = 0
        self._market_ws_reconnect_requested = False
        self._market_ws_connected = False
        self._last_market_ws_msg_at = 0.0
        self._last_positions_status = ""
        self._last_positions_error = ""
        self._last_positions_user = ""
        self._last_positions_checked_at = 0.0

    # ── Setup ─────────────────────────────────────────────────────────────────

    def _build_http_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(timeout=15, verify=certifi.where())

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

    def can_refresh_credentials(self) -> bool:
        return bool(POLY_ETH_PRIVATE_KEY)

    def has_l2_credentials(self) -> bool:
        creds = getattr(self._client, "creds", None)
        return bool(
            creds
            and getattr(creds, "api_key", "")
            and getattr(creds, "api_secret", "")
            and getattr(creds, "api_passphrase", "")
        )

    @staticmethod
    def _looks_like_auth_error(detail: str) -> bool:
        lowered = str(detail or "").lower()
        needles = (
            "401",
            "403",
            "unauthorized",
            "forbidden",
            "invalid signature",
            "signature",
            "api key",
            "passphrase",
            "not authenticated",
            "not authorized",
        )
        return any(token in lowered for token in needles)

    def _mark_auth_success(self, source: str = "") -> None:
        now = time.time()
        self._last_auth_success_at = now
        self._last_auth_error = ""
        self._consecutive_auth_failures = 0
        if source == "heartbeat":
            self._last_heartbeat_ok_at = now

    def _mark_auth_failure(self, detail: str, *, source: str = "", auth_related: bool | None = None) -> None:
        if auth_related is None:
            auth_related = self._looks_like_auth_error(detail)
        self._last_auth_failure_at = time.time()
        if detail:
            self._last_auth_error = detail
        if auth_related:
            self._consecutive_auth_failures += 1
        elif source == "heartbeat" and not self._last_auth_error:
            self._last_auth_error = "heartbeat failed"

    def request_market_ws_reconnect(self) -> None:
        self._market_ws_reconnect_requested = True

    def consume_market_ws_reconnect_request(self) -> bool:
        pending = self._market_ws_reconnect_requested
        self._market_ws_reconnect_requested = False
        return pending

    def set_market_ws_connected(self, connected: bool) -> None:
        self._market_ws_connected = connected
        if connected:
            self._last_market_ws_msg_at = time.time()

    def touch_market_ws_message(self) -> None:
        self._last_market_ws_msg_at = time.time()

    def session_snapshot(self) -> dict[str, Any]:
        def _fmt(ts: float) -> str:
            if ts <= 0:
                return ""
            return _iso_z(datetime.fromtimestamp(ts, tz=_UTC))

        return {
            "generation": self._session_generation,
            "refresh_in_progress": self._refresh_in_progress,
            "can_refresh_credentials": self.can_refresh_credentials(),
            "has_l2_credentials": self.has_l2_credentials(),
            "creds_refreshed_at": _fmt(self._creds_refreshed_at),
            "last_auth_success_at": _fmt(self._last_auth_success_at),
            "last_auth_failure_at": _fmt(self._last_auth_failure_at),
            "last_heartbeat_ok_at": _fmt(self._last_heartbeat_ok_at),
            "last_auth_error": self._last_auth_error,
            "consecutive_auth_failures": self._consecutive_auth_failures,
            "market_ws_connected": self._market_ws_connected,
            "market_ws_last_message_at": _fmt(self._last_market_ws_msg_at),
            "market_ws_reconnect_requested": self._market_ws_reconnect_requested,
            "last_positions_status": self._last_positions_status,
            "last_positions_error": self._last_positions_error,
            "last_positions_user": self._last_positions_user,
            "last_positions_checked_at": _fmt(self._last_positions_checked_at),
        }

    async def _retire_http_client(self, client: httpx.AsyncClient | None) -> None:
        if client is None:
            return
        if POLY_HTTP_CLOSE_GRACE_S > 0:
            await asyncio.sleep(POLY_HTTP_CLOSE_GRACE_S)
        with suppress(Exception):
            await client.aclose()

    async def _get_client_snapshot(self):
        async with self._session_lock:
            return self._client, self._http, self._session_generation

    @staticmethod
    def _probe_balance_params():
        from py_clob_client.clob_types import AssetType, BalanceAllowanceParams

        return BalanceAllowanceParams(
            asset_type=AssetType.COLLATERAL,
            signature_type=1,
        )

    async def _run(self, fn, *args, **kwargs):
        """Run a synchronous py_clob_client call in the thread pool."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, partial(fn, *args, **kwargs))

    @staticmethod
    def _heartbeat_call_args(client) -> tuple[Any, ...]:
        try:
            param_count = len(inspect.signature(client.post_heartbeat).parameters)
        except (TypeError, ValueError):
            # Newer py-clob-client requires heartbeat_id; default to None when introspection fails.
            return (None,)
        return (None,) if param_count >= 1 else ()

    async def auth_health_check(self) -> tuple[bool, str]:
        """Run a read-only authenticated probe against the active client."""
        client, _, _ = await self._get_client_snapshot()
        try:
            result = await self._run(client.get_balance_allowance, self._probe_balance_params())
            if isinstance(result, dict) and ("balance" in result or "allowance" in result):
                self._mark_auth_success("auth_probe")
                return True, ""
            detail = f"unexpected auth probe response: {type(result).__name__}"
            self._mark_auth_failure(detail, source="auth_probe", auth_related=True)
            return False, detail
        except Exception as exc:
            detail = str(exc)
            self._mark_auth_failure(detail, source="auth_probe")
            return False, detail

    async def refresh_session(self) -> tuple[bool, str]:
        """Build a fresh authenticated client bundle and verify it before swap."""
        if not self.can_refresh_credentials():
            return False, "POLY_ETH_PRIVATE_KEY missing"

        async with self._session_lock:
            if self._refresh_in_progress:
                return False, "refresh already in progress"
            self._refresh_in_progress = True

        new_http: httpx.AsyncClient | None = None
        try:
            new_client = await self._run(self._build_client)
            new_http = self._build_http_client()
            try:
                result = await self._run(new_client.get_balance_allowance, self._probe_balance_params())
                if not (isinstance(result, dict) and ("balance" in result or "allowance" in result)):
                    detail = f"auth probe failed after refresh: {type(result).__name__}"
                    self._mark_auth_failure(detail, source="refresh", auth_related=True)
                    return False, detail
            except Exception as exc:
                detail = str(exc)
                self._mark_auth_failure(detail, source="refresh")
                return False, detail

            async with self._session_lock:
                old_http = self._http
                self._client = new_client
                self._http = new_http
                self._session_generation += 1
                self._creds_refreshed_at = time.time()
                self._refresh_in_progress = False
                self.request_market_ws_reconnect()

            asyncio.create_task(self._retire_http_client(old_http))
            self._mark_auth_success("refresh")
            return True, ""
        finally:
            async with self._session_lock:
                self._refresh_in_progress = False
            if new_http is not None and self._http is not new_http:
                asyncio.create_task(self._retire_http_client(new_http))

    async def refresh_credentials(self) -> bool:
        ok, _ = await self.refresh_session()
        return ok

    async def close(self) -> None:
        _, http_client, _ = await self._get_client_snapshot()
        with suppress(Exception):
            await http_client.aclose()

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
                _, http_client, _ = await self._get_client_snapshot()
                resp = await http_client.get(f"{GAMMA_API}/events/slug/{slug}")
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
            _, http_client, _ = await self._get_client_snapshot()
            r_up, r_dn = await asyncio.gather(
                http_client.get(f"{CLOB_HOST}/midpoint", params={"token_id": up_token_id}),
                http_client.get(f"{CLOB_HOST}/midpoint", params={"token_id": down_token_id}),
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
        client, _, _ = await self._get_client_snapshot()
        try:
            result = await self._run(client.get_balance_allowance, self._probe_balance_params())
            raw = result.get("balance", "0") if isinstance(result, dict) else "0"
            self._mark_auth_success("get_balance")
            return float(raw) / 1e6   # USDC has 6 decimals
        except Exception as exc:
            self._mark_auth_failure(str(exc), source="get_balance")
            return 0.0

    @staticmethod
    def _classify_trade_failure(error_msg: str) -> tuple[str, bool, bool]:
        text = str(error_msg or "").strip()
        lowered = text.lower()
        if not lowered:
            return "PLACEMENT_FAILED", True, False

        if "fok_order_not_filled_error" in lowered or "no immediate liquidity" in lowered:
            return "NO_IMMEDIATE_LIQUIDITY", True, False
        if "market_not_ready" in lowered:
            return "MARKET_NOT_READY", True, False
        if "invalid_order_min_size" in lowered:
            return "MIN_ORDER_SIZE", False, True
        if "invalid_order_not_enough_balance" in lowered:
            return "INSUFFICIENT_BALANCE", False, True
        if "execution_error" in lowered or "delaying_order_error" in lowered or "invalid_order_error" in lowered:
            return "EXECUTION_ERROR", True, False

        if "private key" in lowered or "cannot sign orders" in lowered:
            return "AUTH_MISSING_KEY", False, True
        if (
            "invalid signature" in lowered
            or "l2 header" in lowered
            or "unauthorized" in lowered
            or "forbidden" in lowered
            or "authentication" in lowered
            or "invalid api key" in lowered
            or "nonce" in lowered
        ):
            return "AUTH_FAILURE", True, False
        if (
            "timed out" in lowered
            or "timeout" in lowered
            or "temporarily unavailable" in lowered
            or "connection reset" in lowered
            or "connection aborted" in lowered
            or "connection refused" in lowered
            or "network" in lowered
            or "502" in lowered
            or "503" in lowered
            or "504" in lowered
            or "too many requests" in lowered
            or "rate limit" in lowered
            or "no orders found to match" in lowered
        ):
            return "TRANSIENT_NETWORK", True, False
        if "insufficient" in lowered and ("balance" in lowered or "allowance" in lowered or "fund" in lowered):
            return "INSUFFICIENT_BALANCE", False, True
        if "minimum" in lowered or "min order" in lowered or "too small" in lowered:
            return "MIN_ORDER_SIZE", False, True
        if (
            "market resolved" in lowered
            or "closed" in lowered
            or "expired" in lowered
            or "too late" in lowered
            or "not accepting orders" in lowered
        ):
            return "MARKET_CLOSED", False, True
        return "PLACEMENT_FAILED", True, False

    # ── Order placement ───────────────────────────────────────────────────────

    async def place_bet(
        self,
        direction: str,
        token_id: str,
        amount_usdc: float,
        current_odds: float,
    ) -> TradeResult:
        """Place an order. In live mode use an immediate marketable BUY order."""
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
                failure_code="AUTH_MISSING_KEY",
                retryable=False,
                attempt_consumed=True,
            )

        client, _, _ = await self._get_client_snapshot()
        try:
            from py_clob_client.clob_types import MarketOrderArgs, OrderType

            order_type = OrderType.FOK
            price_hint = round(max(0.01, min(0.99, current_odds)), 2)
            min_order_size = await self.get_min_order_size(token_id)
            actual_amount_usdc = round(amount_usdc, 4)
            if min_order_size > 0 and price_hint > 0:
                min_notional = round(min_order_size * price_hint, 4)
                if actual_amount_usdc + 1e-9 < min_notional:
                    actual_amount_usdc = min_notional

            order_args = MarketOrderArgs(
                token_id=token_id,
                amount=actual_amount_usdc,
                side="BUY",  # direction is encoded in token_id (up_token vs down_token)
                price=0.0,   # let the client derive a worst-price cap from the live book
                order_type=order_type,
            )
            signed = await self._run(client.create_market_order, order_args)
            resp = await self._run(client.post_order, signed, order_type)
            status = str(resp.get("status", "")) if isinstance(resp, dict) else ""
            status_upper = status.upper()
            signed_price = 0.0
            if isinstance(signed, dict):
                signed_price = _safe_float(signed.get("price"), 0.0)
            else:
                signed_price = _safe_float(getattr(signed, "price", 0.0), 0.0)
            effective_price = round(max(0.01, min(0.99, signed_price or price_hint)), 2)
            filled_size = math.floor((actual_amount_usdc / effective_price) * 100) / 100 if effective_price > 0 else 0.0

            if resp and resp.get("success"):
                if status_upper == "LIVE":
                    return TradeResult(
                        success=False,
                        error="market order unexpectedly became a resting LIVE order",
                        failure_code="UNEXPECTED_RESTING_ORDER",
                        retryable=False,
                        attempt_consumed=True,
                    )
                if status_upper == "UNMATCHED":
                    return TradeResult(
                        success=False,
                        error="market order was accepted but did not match immediately",
                        failure_code="NO_IMMEDIATE_LIQUIDITY",
                        retryable=True,
                        attempt_consumed=False,
                    )
                self._mark_auth_success("place_bet")
                return TradeResult(
                    success=True,
                    order_id=resp.get("orderID"),
                    size=filled_size,
                    price=effective_price,
                    amount_usdc=actual_amount_usdc,
                )
            error_msg = str(resp.get("errorMsg", "unknown")) if isinstance(resp, dict) else "unknown"
            self._mark_auth_failure(error_msg, source="place_bet")
            failure_code, retryable, attempt_consumed = self._classify_trade_failure(error_msg)
            return TradeResult(
                success=False,
                error=error_msg,
                failure_code=failure_code,
                retryable=retryable,
                attempt_consumed=attempt_consumed,
            )
        except Exception as exc:
            error_msg = str(exc)
            self._mark_auth_failure(error_msg, source="place_bet")
            failure_code, retryable, attempt_consumed = self._classify_trade_failure(error_msg)
            return TradeResult(
                success=False,
                error=error_msg,
                failure_code=failure_code,
                retryable=retryable,
                attempt_consumed=attempt_consumed,
            )

    async def get_min_order_size(self, token_id: str) -> float:
        """Return the market minimum order size from the public order book."""
        client, _, _ = await self._get_client_snapshot()
        try:
            book = await self._run(client.get_order_book, token_id)
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
        client, _, _ = await self._get_client_snapshot()
        try:
            await self._run(client.post_heartbeat, *self._heartbeat_call_args(client))
            self._mark_auth_success("heartbeat")
            return True
        except Exception as exc:
            self._mark_auth_failure(str(exc), source="heartbeat")
            return False

    # ── Order management ──────────────────────────────────────────────────────

    async def get_order(self, order_id: str) -> dict:
        """GET /order/{orderID} — fetch a single order by ID.

        Returns order dict with key 'status':
          LIVE | MATCHED | CANCELED | CANCELED_MARKET_RESOLVED | INVALID
        Returns empty dict on failure.
        """
        client, _, _ = await self._get_client_snapshot()
        try:
            result = await self._run(client.get_order, order_id)
            self._mark_auth_success("get_order")
            return result if isinstance(result, dict) else {}
        except Exception as exc:
            self._mark_auth_failure(str(exc), source="get_order")
            return {}

    async def cancel_order(self, order_id: str) -> tuple[bool, str]:
        """DELETE /order — cancel a single open order.

        Returns (True, "") on success.
        Returns (False, reason) on failure, where reason comes from the
        not_canceled map in the API response, e.g. "Order not found or already canceled".
        """
        client, _, _ = await self._get_client_snapshot()
        try:
            result = await self._run(client.cancel, {"orderID": order_id})
            if not isinstance(result, dict):
                self._mark_auth_failure("unexpected response format", source="cancel_order", auth_related=False)
                return False, "unexpected response format"
            if order_id in result.get("canceled", []):
                self._mark_auth_success("cancel_order")
                return True, ""
            reason = result.get("not_canceled", {}).get(order_id, "unknown reason")
            self._mark_auth_failure(reason, source="cancel_order")
            return False, reason
        except Exception as exc:
            self._mark_auth_failure(str(exc), source="cancel_order")
            return False, str(exc)

    async def cancel_orders(self, order_ids: list[str]) -> dict:
        """DELETE /orders — cancel up to 3000 orders in one call.

        Returns {"canceled": [...], "not_canceled": {...}}.
        """
        client, _, _ = await self._get_client_snapshot()
        try:
            result = await self._run(client.cancel_orders, order_ids)
            self._mark_auth_success("cancel_orders")
            return result if isinstance(result, dict) else {}
        except Exception as exc:
            self._mark_auth_failure(str(exc), source="cancel_orders")
            return {}

    async def cancel_all_orders(self) -> bool:
        """DELETE /cancel-all — cancel every open order for this account."""
        client, _, _ = await self._get_client_snapshot()
        try:
            await self._run(client.cancel_all)
            self._mark_auth_success("cancel_all_orders")
            return True
        except Exception as exc:
            self._mark_auth_failure(str(exc), source="cancel_all_orders")
            return False

    async def get_user_orders(
        self,
        market: str | None = None,
        asset_id: str | None = None,
    ) -> list[dict]:
        """GET /orders — list open orders, optionally filtered by market or token.

        Returns list of order dicts.
        """
        client, _, _ = await self._get_client_snapshot()
        try:
            from py_clob_client.clob_types import OpenOrderParams
            params = OpenOrderParams(market=market, asset_id=asset_id)
            result = await self._run(client.get_orders, params)
            self._mark_auth_success("get_user_orders")
            return result.get("data", []) if isinstance(result, dict) else []
        except Exception as exc:
            self._mark_auth_failure(str(exc), source="get_user_orders")
            return []

    def _l2_auth_headers(self, creds, method: str, path: str, body: str = "") -> dict:
        """Build HMAC L2 authentication headers for direct CLOB HTTP calls."""
        import base64
        import hashlib
        import hmac as _hmac

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

    async def get_order_scoring(self, order_id: str) -> bool:
        """GET /order-scoring?order_id=... — check if order earns LP rewards."""
        client, http_client, _ = await self._get_client_snapshot()
        try:
            headers = self._l2_auth_headers(client.creds, "GET", "/order-scoring")
            r = await http_client.get(
                f"{CLOB_HOST}/order-scoring",
                params={"order_id": order_id},
                headers=headers,
            )
            if r.is_success:
                self._mark_auth_success("get_order_scoring")
                return bool(r.json().get("scoring", False))
            self._mark_auth_failure(
                f"order scoring http {r.status_code}",
                source="get_order_scoring",
                auth_related=r.status_code in (401, 403),
            )
            return False
        except Exception as exc:
            self._mark_auth_failure(str(exc), source="get_order_scoring")
            return False

    # ── Trades (position tracking) ────────────────────────────────────────────

    async def get_recent_trades(self, after_ts: float | None = None) -> list[ClosedTrade]:
        """Return trades for our address via GET /trades."""
        client, _, _ = await self._get_client_snapshot()
        try:
            from py_clob_client.clob_types import TradeParams
            params = TradeParams(maker_address=POLY_ADDRESS)
            result = await self._run(client.get_trades, params)

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
            self._mark_auth_success("get_recent_trades")
            return trades
        except Exception as exc:
            self._mark_auth_failure(str(exc), source="get_recent_trades")
            return []

    async def get_order_book_snapshot(self, token_id: str) -> dict[str, Any] | None:
        """Return a best-effort public order book snapshot for a token."""
        client, _, _ = await self._get_client_snapshot()
        try:
            book = await self._run(client.get_order_book, token_id)
        except Exception:
            return None
        if isinstance(book, dict):
            return book
        return getattr(book, "__dict__", None)

    async def fetch_market_settlement(self, condition_id: str) -> SettlementRecord | None:
        """Best-effort settlement lookup for a resolved market."""
        if not condition_id:
            return None

        candidates = [
            (f"{GAMMA_API}/markets", {"condition_ids": condition_id}),
            (f"{GAMMA_API}/markets", {"conditionId": condition_id}),
            (f"{GAMMA_API}/markets/{condition_id}", None),
        ]
        for url, params in candidates:
            try:
                _, http_client, _ = await self._get_client_snapshot()
                response = await http_client.get(url, params=params, timeout=2.0)
                if not response.is_success:
                    continue
                payload = response.json()
            except Exception:
                continue

            settlement_price = _extract_settlement_price(payload if isinstance(payload, dict) else {"data": payload})
            if settlement_price is None:
                continue
            resolved_at_raw = _extract_resolved_at(payload if isinstance(payload, dict) else {"data": payload})
            resolved_at = ml_parse_utc_ts(resolved_at_raw) or _utc_now()
            return SettlementRecord(
                condition_id=condition_id,
                resolved_at=_iso_z(resolved_at),
                settlement_price=settlement_price,
                settlement_source="market_settlement_lookup",
                settlement_source_priority=_label_source_priority("market_settlement_lookup"),
                chainlink_settlement_price=settlement_price,
                raw_payload=payload if isinstance(payload, dict) else {"data": payload},
            )
        return None

    async def get_current_positions(
        self,
        *,
        user: str | None = None,
        redeemable: bool | None = None,
        size_threshold: float = 0.0,
        limit: int = 500,
        market: str | None = None,
    ) -> list[dict[str, Any]]:
        """Fetch current user positions from the public Polymarket Data API."""
        user = str(user or POLY_ADDRESS or "").strip()
        self._last_positions_user = _mask_address(user)
        self._last_positions_checked_at = time.time()
        self._last_positions_status = "skipped"
        self._last_positions_error = ""
        if not user:
            self._last_positions_error = "missing user"
            return []

        positions: list[dict[str, Any]] = []
        offset = 0
        page_size = max(1, min(int(limit or 500), 500))
        while True:
            params: dict[str, Any] = {
                "user": user,
                "sizeThreshold": size_threshold,
                "limit": page_size,
                "offset": offset,
            }
            if redeemable is not None:
                params["redeemable"] = str(bool(redeemable)).lower()
            if market:
                params["market"] = market

            try:
                _, http_client, _ = await self._get_client_snapshot()
                response = await http_client.get(
                    f"{DATA_API}/positions",
                    params=params,
                    headers={
                        "Accept": "application/json",
                        "User-Agent": "tradebot-claims/1.0",
                    },
                    timeout=5.0,
                )
                if not response.is_success:
                    self._last_positions_status = f"http_{response.status_code}"
                    self._last_positions_error = str(response.text or "")[:240]
                    return positions
                payload = response.json()
                if not isinstance(payload, list):
                    self._last_positions_status = "bad_payload"
                    self._last_positions_error = f"expected list, got {type(payload).__name__}"
                    return positions
                positions.extend(item for item in payload if isinstance(item, dict))
                self._last_positions_status = "ok"
                self._last_positions_error = ""
                if len(payload) < page_size:
                    return positions
                offset += page_size
                if offset >= 5000:
                    return positions
            except Exception as exc:
                self._last_positions_status = "exception"
                self._last_positions_error = str(exc)[:240]
                return positions

    @staticmethod
    def claim_execution_status() -> tuple[bool, str]:
        if not POLY_ETH_PRIVATE_KEY:
            return False, "POLY_ETH_PRIVATE_KEY missing"
        if not (POLY_RELAYER_API_KEY and POLY_RELAYER_API_KEY_ADDRESS):
            return False, "POLY_RELAYER_API_KEY / POLY_RELAYER_API_KEY_ADDRESS missing"
        try:
            from polymarket_apis.clients.web3_client import PolymarketGaslessWeb3Client  # noqa: F401
        except Exception:
            return False, "polymarket-apis not installed (pip install polymarket-apis)"
        return True, ""

    @staticmethod
    def _binary_redeem_index_sets() -> list[int]:
        return [1, 2]

    @staticmethod
    def _encode_redeem_positions_data(condition_id: str) -> str:
        from eth_abi import encode as abi_encode
        from eth_utils import function_signature_to_4byte_selector, to_checksum_address

        selector = function_signature_to_4byte_selector(
            "redeemPositions(address,bytes32,bytes32,uint256[])"
        )
        condition_hex = str(condition_id or "").removeprefix("0x")
        if len(condition_hex) != 64:
            raise ValueError("invalid condition_id for redeem")
        args = abi_encode(
            ["address", "bytes32", "bytes32", "uint256[]"],
            [
                to_checksum_address(POLY_USDC_ADDRESS),
                b"\x00" * 32,
                bytes.fromhex(condition_hex),
                MarketClient._binary_redeem_index_sets(),
            ],
        )
        return "0x" + (selector + args).hex()

    @staticmethod
    def _build_web3_client():
        from polymarket_apis.clients.web3_client import PolymarketGaslessWeb3Client
        from json import dumps as _json_dumps
        import httpx as _httpx

        class _RelayerClient(PolymarketGaslessWeb3Client):
            def __init__(self, private_key, relayer_api_key, relayer_api_key_address,
                         signature_type=1, chain_id=137):
                super().__init__(private_key, signature_type=signature_type,
                                 relayer_api_key=relayer_api_key, chain_id=chain_id)
                self._relayer_api_key = relayer_api_key
                self._relayer_api_key_address = relayer_api_key_address

            def _execute(self, to, data, operation_name, metadata=None):
                match self.signature_type:
                    case 1:
                        body = self._build_proxy_relay_transaction(to, data, metadata or "")
                    case 2:
                        body = self._build_safe_relay_transaction(to, data, metadata or "")
                    case _:
                        raise ValueError(f"Invalid signature_type: {self.signature_type}")
                headers = {
                    "RELAYER_API_KEY": self._relayer_api_key,
                    "RELAYER_API_KEY_ADDRESS": self._relayer_api_key_address,
                    "Content-Type": "application/json",
                }
                resp = _httpx.post(
                    f"{self.relay_url.rstrip('/')}/submit",
                    headers=headers,
                    content=_json_dumps(body).encode("utf-8"),
                    timeout=30,
                )
                resp.raise_for_status()
                relay_data = resp.json()
                tx_hash = relay_data.get("transactionHash")
                if not tx_hash:
                    raise ValueError(f"No transactionHash in relay response: {relay_data}")
                receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
                return {**dict(receipt), "transactionHash": tx_hash,
                        "id": relay_data.get("transactionID", "")}

        return _RelayerClient(
            private_key=POLY_ETH_PRIVATE_KEY,
            relayer_api_key=POLY_RELAYER_API_KEY,
            relayer_api_key_address=POLY_RELAYER_API_KEY_ADDRESS,
            signature_type=1,
            chain_id=CHAIN_ID,
        )

    @staticmethod
    def _extract_claim_attempt_metadata(payload: Any) -> tuple[str, str]:
        if payload is None:
            return "", ""
        if isinstance(payload, dict):
            tx_hash = str(
                payload.get("transactionHash")
                or payload.get("txHash")
                or payload.get("transaction_hash")
                or payload.get("hash")
                or ""
            )
            request_id = str(payload.get("id") or payload.get("requestId") or payload.get("request_id") or "")
            return tx_hash, request_id
        tx_hash = str(
            getattr(payload, "transactionHash", "")
            or getattr(payload, "txHash", "")
            or getattr(payload, "transaction_hash", "")
            or getattr(payload, "hash", "")
            or ""
        )
        request_id = str(
            getattr(payload, "id", "")
            or getattr(payload, "requestId", "")
            or getattr(payload, "request_id", "")
            or ""
        )
        return tx_hash, request_id

    async def claim_position(self, claim: ClaimRecord) -> ClaimAttemptResult:
        supported, reason = self.claim_execution_status()
        if not supported:
            return ClaimAttemptResult(
                success=False,
                status="failed",
                error_code="executor_unavailable",
                error_message=reason,
            )
        if claim.negative_risk:
            return ClaimAttemptResult(
                success=False,
                status="failed",
                error_code="neg_risk_not_supported",
                error_message="negative-risk claim execution is not implemented",
            )

        try:
            web3_client = await self._run(self._build_web3_client)
            amounts = [0.0, 0.0]
            if 0 <= claim.outcome_index <= 1:
                amounts[claim.outcome_index] = claim.claimable_amount
            receipt = await self._run(
                web3_client.redeem_position,
                condition_id=claim.condition_id,
                amounts=amounts,
                neg_risk=False,
            )
            tx_hash, request_id = self._extract_claim_attempt_metadata(receipt)
            return ClaimAttemptResult(
                success=True,
                status="confirmed",
                tx_hash=tx_hash,
                request_id=request_id,
            )
        except Exception as exc:
            return ClaimAttemptResult(
                success=False,
                status="failed",
                error_code="claim_execution_failed",
                error_message=str(exc),
            )

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
                    self.consume_market_ws_reconnect_request()
                    await ws.send(sub_msg)
                    self.set_market_ws_connected(True)
                    self.touch_market_ws_message()
                    state.log_event("[MKTWS] Market WebSocket connected")
                    while True:
                        # Exit if window changed
                        if condition_id and (state.window is None or state.window.condition_id != condition_id):
                            self.set_market_ws_connected(False)
                            return
                        if self.consume_market_ws_reconnect_request():
                            state.log_event("[MKTWS] session refresh requested, reconnecting…")
                            break
                        try:
                            raw = await asyncio.wait_for(ws.recv(), timeout=POLY_WS_PING_INTERVAL_S)
                        except asyncio.TimeoutError:
                            idle_for = time.time() - self._last_market_ws_msg_at
                            if idle_for >= POLY_WS_IDLE_RECONNECT_S:
                                state.log_event(f"[MKTWS] idle {POLY_WS_IDLE_RECONNECT_S}s, reconnecting…")
                                break
                            try:
                                await ws.send("{}")
                            except Exception:
                                break
                            continue
                        self.touch_market_ws_message()
                        msgs = json.loads(raw)
                        if isinstance(msgs, dict):
                            msgs = [msgs]
                        for msg in msgs:
                            etype = msg.get("event_type", "")
                            if etype in ("price_change", "book", "last_trade_price"):
                                _update_odds_from_ws(msg, up_token_id, down_token_id, state)
                            elif etype == "market_resolved":
                                resolved_condition_id = (
                                    str(msg.get("condition_id") or msg.get("conditionId") or condition_id or "").strip()
                                )
                                settlement_price = _extract_settlement_price(msg)
                                settlement_record: SettlementRecord | None = None
                                if settlement_price is not None and resolved_condition_id:
                                    resolved_at = ml_parse_utc_ts(_extract_resolved_at(msg)) or _utc_now()
                                    settlement_record = SettlementRecord(
                                        condition_id=resolved_condition_id,
                                        resolved_at=_iso_z(resolved_at),
                                        settlement_price=settlement_price,
                                        settlement_source="chainlink_market_resolved",
                                        settlement_source_priority=_label_source_priority("chainlink_market_resolved"),
                                        market_id=str(msg.get("market") or ""),
                                        chainlink_settlement_price=settlement_price,
                                        raw_payload=msg,
                                    )
                                elif resolved_condition_id:
                                    settlement_record = await self.fetch_market_settlement(resolved_condition_id)

                                if settlement_record is not None:
                                    state.logger.log_settlement(settlement_record.to_record())
                                    state.settlement_registry_cache[settlement_record.condition_id] = settlement_record.to_record()
                                    state.log_event(
                                        f"[MKTWS] market_resolved: {settlement_record.condition_id} "
                                        f"settlement={settlement_record.settlement_price:,.2f} "
                                        f"source={settlement_record.settlement_source}"
                                    )
                                else:
                                    state.log_event(f"[MKTWS] market_resolved: {msg.get('market')}")
                                state.market_resolved_event.set()
                    self.set_market_ws_connected(False)
            except asyncio.CancelledError:
                self.set_market_ws_connected(False)
                raise
            except Exception as exc:
                self.set_market_ws_connected(False)
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


def _normalize_book_levels(levels: Any, depth: int = 5) -> list[tuple[float, float]]:
    normalized: list[tuple[float, float]] = []
    if not isinstance(levels, list):
        return normalized
    for raw in levels[:depth]:
        price = 0.0
        size = 0.0
        if isinstance(raw, dict):
            price = _safe_float(raw.get("price") or raw.get("rate"), 0.0)
            size = _safe_float(
                raw.get("size")
                or raw.get("quantity")
                or raw.get("qty")
                or raw.get("amount"),
                0.0,
            )
        elif isinstance(raw, (list, tuple)) and len(raw) >= 2:
            price = _safe_float(raw[0], 0.0)
            size = _safe_float(raw[1], 0.0)
        if price > 0.0 and size > 0.0:
            normalized.append((price, size))
    return normalized


def _compute_ob_imbalance_from_levels(bids: list[tuple[float, float]], asks: list[tuple[float, float]]) -> float:
    bid_qty = sum(size for _, size in bids[:5])
    ask_qty = sum(size for _, size in asks[:5])
    total = bid_qty + ask_qty
    if total <= 0.0:
        return 0.0
    return float(max(-1.0, min(1.0, (bid_qty - ask_qty) / total)))


def _update_odds_from_ws(
    msg: dict,
    up_token_id: str,
    down_token_id: str,
    state: "BotState",
) -> None:
    asset = msg.get("asset_id", "")
    bids = _normalize_book_levels(msg.get("bids", []))
    asks = _normalize_book_levels(msg.get("asks", []))
    if asset and (bids or asks):
        state.order_book_snapshots[asset] = OrderBookSnapshot(
            asset_id=asset,
            bids=bids,
            asks=asks,
            ts=time.time(),
        )
    price = msg.get("price") or msg.get("last_trade_price")
    if price is None:
        # Try extracting from bids/asks midpoint
        if bids and asks:
            best_bid = bids[0][0]
            best_ask = asks[0][0]
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

    def notify_window(self, win: "WindowInfo", state: "BotState | None" = None) -> None:
        """New market window detected."""
        if not self._enabled:
            return
        record_line = ""
        balance_line = ""
        if state is not None:
            record_line = (
                f"Record: Win {state.win_count} / Lose {state.loss_count}  "
                f"Winrate: {state.win_rate:.1f}%\n"
            )
            if state.balance_usdc > 0:
                balance_line = f"Balance: <code>${state.balance_usdc:.2f} USDC</code>\n"
        text = (
            f"🆕 <b>New Window</b> | {win.window_label} UTC\n"
            f"Beat: <code>${win.beat_price:,.2f}</code>\n"
            f"Ends: {win.end_time.strftime('%H:%M:%S')} UTC\n"
            f"{record_line}"
            f"{balance_line}"
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

    def notify_signal(
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
        """Send the latest signal-engine output, regardless of execution result."""
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
        source = html.escape(signal.source or "unknown")
        decision_line = ""
        if decision is not None:
            decision_line = (
                f"\nEngine: <b>{html.escape(decision.action)}</b>  "
                f"<code>{html.escape(decision.gate)}</code>"
            )
            if decision.reason:
                decision_line += f"\nWhy: {html.escape(decision.reason[:140])}"

        text = (
            f"🧠 <b>Signal Engine</b> {emoji}  {self._mode}\n"
            f"Signal: <b>{signal_label}</b>  conf=<code>{signal.confidence:.0%}</code>  "
            f"raw=<code>{raw_conf:.0%}</code>  src=<code>{source}</code>\n"
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
            status_label = "WON"
        elif pos.status == "lost":
            emoji = "❌"
            pnl_s = f"-${abs(pos.pnl):.2f}" if pos.pnl is not None else "?"
            status_label = "LOST"
        else:
            emoji = "➖"
            pnl_s = f"${pos.pnl:.2f}" if pos.pnl is not None else "$0.00"
            status_label = "VOID"
        wr = state.win_rate
        text = (
            f"{emoji} <b>{status_label}</b>  {pnl_s}\n"
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


class HyperliquidFeed:
    """Streams BTC mid-price from Hyperliquid perpetuals WebSocket.

    Uses the ``allMids`` channel which publishes mark mid-prices for all
    perpetual assets. BTC perp tracks spot closely via the funding mechanism,
    providing an independent cross-reference to Binance USDC spot.
    Auto-reconnects on any disconnect, same pattern as BTCFeed.
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
                self.state.log_event(f"[HL] reconnecting after error: {exc}")
                self.state.hl_ws_ok = False
                await asyncio.sleep(3)

    async def _connect_and_stream(self) -> None:
        async with websockets.connect(
            HYPERLIQUID_WS,
            ssl=_SSL_CTX,
            ping_interval=20,
            ping_timeout=10,
        ) as ws:
            sub_msg = json.dumps({
                "method": "subscribe",
                "subscription": {"type": "allMids"},
            })
            await ws.send(sub_msg)
            self.state.hl_ws_ok = True
            self.state.log_event("[HL] Hyperliquid WebSocket connected")
            async for raw in ws:
                try:
                    msg = json.loads(raw)
                    if msg.get("channel") != "allMids":
                        continue
                    mids = msg.get("data", {}).get("mids", {})
                    btc_mid = mids.get("BTC") or mids.get("BTC-USD")
                    if btc_mid is None:
                        continue
                    self.state.hl_btc_price      = float(btc_mid)
                    self.state.hl_btc_price_time = time.time()
                except Exception:
                    pass


class ChainlinkProxyFeed:
    """Polls Pyth Network's Hermes REST API for the BTC/USD price.

    Pyth publishes prices aggregated from multiple high-frequency sources and
    is used by many DeFi protocols as a Chainlink-equivalent oracle. Polling
    it periodically provides a cross-reference that is closer to the oracle
    price Polymarket uses (Chainlink) than Binance USDC spot.

    This feed is best-effort: failures are silently swallowed and the cached
    price expires after PYTH_CACHE_TTL_S seconds. Never blocks trading.
    """

    # BTC/USD price feed ID on Pyth Network (mainnet)
    PYTH_BTC_FEED_ID = "e62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43"
    PYTH_URL = (
        "https://hermes.pyth.network/v2/updates/price/latest"
        f"?ids[]={PYTH_BTC_FEED_ID}&encoding=hex&parsed=true"
    )
    PYTH_CACHE_TTL_S = 10.0  # seconds before cached price is considered stale
    PYTH_POLL_INTERVAL_S = 8.0

    def __init__(self, state: "BotState") -> None:
        self.state = state
        self._client: httpx.AsyncClient | None = None

    async def run(self) -> None:
        self._client = httpx.AsyncClient(timeout=5.0)
        try:
            while self.state.running:
                await self._poll_once()
                await asyncio.sleep(self.PYTH_POLL_INTERVAL_S)
        except asyncio.CancelledError:
            raise
        finally:
            if self._client is not None:
                await self._client.aclose()

    async def _poll_once(self) -> None:
        try:
            assert self._client is not None
            response = await self._client.get(self.PYTH_URL)
            if not response.is_success:
                return
            data = response.json()
            parsed = data.get("parsed", [])
            if not parsed:
                return
            price_data = parsed[0].get("price", {})
            raw_price = price_data.get("price")
            expo = price_data.get("expo", 0)
            if raw_price is None:
                return
            btc_price = float(raw_price) * (10 ** expo)
            if btc_price > 0:
                self.state.pyth_btc_price      = btc_price
                self.state.pyth_btc_price_time = time.time()
        except Exception:
            pass

    def get_price(self) -> float | None:
        """Return cached Pyth BTC price if fresh, else None."""
        if self.state.pyth_btc_price is None:
            return None
        age = time.time() - self.state.pyth_btc_price_time
        if age > self.PYTH_CACHE_TTL_S:
            return None
        return self.state.pyth_btc_price


# ══════════════════════════════════════════════════════════════════════════════
# Source: bot.py
# ══════════════════════════════════════════════════════════════════════════════

"""Central bot state and all async orchestration loops."""

import asyncio
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import partial

from datetime import timezone as _TZ

# ══════════════════════════════════════════════════════════════════════════════
# Source: ml_runtime.py (inlined)
# ══════════════════════════════════════════════════════════════════════════════

import json
import math
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.model_selection import TimeSeriesSplit
from xgboost import XGBClassifier


UTC = timezone.utc
MODEL_NAME = "bandar_avoider_xgb"
FEATURE_SCHEMA_VERSION = "2.0"
LABEL_BUY_UP = "BUY_UP"
LABEL_BUY_DOWN = "BUY_DOWN"
LABEL_SKIP = "SKIP"
PROMOTION_STATES = {"shadow", "assist", "active"}
ML_FEATURE_GLOB = "ml_features_*.jsonl"
ML_LABEL_GLOB = "ml_labels_*.jsonl"
SETTLEMENT_GLOB = "settlements_*.jsonl"
DEFAULT_MODELS_DIR = "artifacts/ml"

MODEL_FEATURE_COLUMNS = [
    "gap_signed_pct",
    "seconds_remaining",
    "signal_alignment",
    "signed_alignment",
    "odds_vel",
    "odds_vel_accel",
    "cvd_divergence",
    "macd_histogram",
    "bb_pct_b",
    "rsi",
    "momentum_pct",
    "is_late_window",
    "is_bandar_zone",
    "is_proximity_risk",
    "is_proximity_risk_above",
    "is_proximity_risk_below",
    "gap_crossed_zero",
    "price_roc_15s",
    "price_roc_30s",
    "cvd_change_last_30s",
    "odds_edge_strength",
    "beat_above_ratio",
    "elapsed_fraction",
    "gap_alignment_interaction",
    "realized_vol_30s",
    "realized_vol_60s",
    "gap_signed_pct_lag1",
    "signal_alignment_lag1",
    "odds_edge_strength_lag1",
    "ob_imbalance",
]

NUMERIC_DEFAULTS = {
    "beat_price": 0.0,
    "btc_price": 0.0,
    "up_odds": 0.5,
    "down_odds": 0.5,
    "gap_pct": 0.0,
    "gap_signed_pct": 0.0,
    "seconds_remaining": 0,
    "signal_alignment": 0,
    "signed_alignment": 0.0,
    "odds_vel": 0.0,
    "odds_vel_accel": 0.0,
    "cvd_divergence": 0,
    "macd_histogram": 0.0,
    "bb_pct_b": 0.5,
    "rsi": 50.0,
    "momentum_pct": 0.0,
    "is_late_window": 0,
    "is_bandar_zone": 0,
    "is_proximity_risk": 0,
    "is_proximity_risk_above": 0,
    "is_proximity_risk_below": 0,
    "gap_crossed_zero": 0,
    "price_roc_15s": 0.0,
    "price_roc_30s": 0.0,
    "cvd_change_last_30s": 0.0,
    "odds_edge_strength": 0.0,
    "elapsed_fraction": 0.0,
    "gap_alignment_interaction": 0.0,
    "realized_vol_30s": 0.0,
    "realized_vol_60s": 0.0,
    "gap_signed_pct_lag1": 0.0,
    "signal_alignment_lag1": 0.0,
    "odds_edge_strength_lag1": 0.0,
    "ob_imbalance": 0.0,
    "beat_above_ratio": 0.5,
    "fair_up": 0.5,
    "fair_down": 0.5,
    "edge_up": 0.0,
    "edge_down": 0.0,
}


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _iso_z(dt: datetime) -> str:
    return dt.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def ml_parse_utc_ts(value: str | datetime | None) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.astimezone(UTC)
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(UTC)
    except Exception:
        return None


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        if isinstance(value, float) and math.isnan(value):
            return default
        return float(value)
    except Exception:
        return default


def _mask_address(value: str) -> str:
    text = str(value or "").strip()
    if len(text) <= 12:
        return text
    return f"{text[:6]}…{text[-4:]}"


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        if isinstance(value, float) and math.isnan(value):
            return default
        return int(value)
    except Exception:
        return default


def encode_cvd_divergence(value: str | int | None) -> int:
    if isinstance(value, int):
        return value
    raw = str(value or "NONE").upper().strip()
    if raw == "BULLISH":
        return 1
    if raw == "BEARISH":
        return -1
    return 0


def decode_cvd_divergence(value: int | str | None) -> str:
    encoded = encode_cvd_divergence(value)
    if encoded > 0:
        return "BULLISH"
    if encoded < 0:
        return "BEARISH"
    return "NONE"


def _clip_probability(value: float) -> float:
    return float(max(0.001, min(0.999, value)))


def _phase_bucket_from_timing(elapsed_s: int, seconds_remaining: int) -> str:
    if seconds_remaining <= 0:
        return "CLOSED"
    if seconds_remaining < LAST_MIN_SECONDS_GUARD:
        return "TOO_LATE"
    if elapsed_s < SIGNAL_LOCK_START_S:
        return "OBSERVE"
    if elapsed_s < EXECUTION_START_S:
        return "RESERVE"
    if elapsed_s < LATE_EXEC_START_S:
        return "EARLY_EXEC"
    return "LATE_EXEC"


def _bet_frequency_phase_at_least(phase: str) -> bool:
    ordering = {"A": 1, "B": 2, "C": 3}
    current = ordering.get(BET_FREQUENCY_EXPANSION_PHASE, 1)
    target = ordering.get(str(phase).strip().upper(), current)
    return current >= target


DEFAULT_RUNTIME_THRESHOLD_PROFILE_VERSION = "rtp_v1"
RUNTIME_THRESHOLD_PHASES = ("OBSERVE", "RESERVE", "EARLY_EXEC", "LATE_EXEC")


def _default_runtime_thresholds() -> dict[str, Any]:
    return {
        "observe": 0.70,
        "reserve": 0.74,
        "early_exec": 0.74,
        "late_exec": 0.76,
        "observe_seed": OBSERVE_CARRY_MIN_CONF,
        "late_risk_bump": SOFT_PENALTY_CONF_BUMP,
        "version": DEFAULT_RUNTIME_THRESHOLD_PROFILE_VERSION,
        "source": "default",
    }


def _normalize_runtime_thresholds(profile: dict[str, Any] | None = None) -> dict[str, Any]:
    normalized = dict(_default_runtime_thresholds())
    payload = dict(profile or {})
    if isinstance(payload.get("runtime_thresholds"), dict):
        payload = {**payload["runtime_thresholds"], **{k: v for k, v in payload.items() if k != "runtime_thresholds"}}
    for key in ("observe", "reserve", "early_exec", "late_exec", "observe_seed", "late_risk_bump"):
        if key in payload:
            normalized[key] = _safe_float(payload.get(key), normalized[key])
    version = str(payload.get("version") or payload.get("threshold_profile_version") or normalized["version"]).strip()
    source = str(payload.get("source") or payload.get("threshold_source") or normalized["source"]).strip().lower()
    if not version:
        version = DEFAULT_RUNTIME_THRESHOLD_PROFILE_VERSION
    if not source:
        source = "default"
    normalized["version"] = version
    normalized["source"] = source
    return normalized


def _threshold_floor_for_bucket(bucket: str, profile: dict[str, Any] | None = None) -> float:
    normalized = _normalize_runtime_thresholds(profile)
    bucket_key = str(bucket or "OBSERVE").strip().upper()
    mapping = {
        "OBSERVE": "observe",
        "RESERVE": "reserve",
        "EARLY_EXEC": "early_exec",
        "LATE_EXEC": "late_exec",
    }
    return _safe_float(normalized.get(mapping.get(bucket_key, "observe")), normalized["observe"])


def _manifest_runtime_threshold_payload(manifest: Any | None) -> dict[str, Any]:
    if manifest is None:
        return _default_runtime_thresholds()
    payload: dict[str, Any] = {}
    if isinstance(getattr(manifest, "runtime_thresholds", None), dict):
        payload.update(getattr(manifest, "runtime_thresholds"))
    metrics = getattr(manifest, "metrics", {}) if hasattr(manifest, "metrics") else {}
    if isinstance(metrics, dict) and isinstance(metrics.get("runtime_thresholds"), dict):
        payload.update(metrics["runtime_thresholds"])
    payload.setdefault("threshold_source", getattr(manifest, "threshold_mode", "") or payload.get("threshold_source", "default"))
    payload.setdefault("threshold_profile_version", payload.get("version", DEFAULT_RUNTIME_THRESHOLD_PROFILE_VERSION))
    return _normalize_runtime_thresholds(payload)


def _iter_prediction_analytics_records(log_dir: str | Path, lookback_days: int = 14) -> list[dict[str, Any]]:
    root = Path(log_dir)
    cutoff = (_utc_now() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")
    files = sorted(
        [
            path for path in root.glob("prediction_analytics_*.jsonl")
            if path.stem.rsplit("_", 1)[-1] >= cutoff
        ],
        key=lambda item: item.name,
    )
    records: list[dict[str, Any]] = []
    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as handle:
                for line in handle:
                    try:
                        records.append(json.loads(line))
                    except Exception:
                        continue
        except Exception:
            continue
    return records


def _load_threshold_tuning_windows(log_dir: str | Path, lookback_days: int = ML_THRESHOLD_LOOKBACK_DAYS) -> list[dict[str, Any]]:
    windows: dict[str, dict[str, Any]] = {}
    for record in _iter_prediction_analytics_records(log_dir, lookback_days=lookback_days):
        if str(record.get("event", "") or "") != "prediction_resolved":
            continue
        condition_id = str(record.get("condition_id", "") or "").strip()
        if not condition_id:
            continue
        resolved_at = str(record.get("resolved_at") or record.get("ts") or "")
        window = windows.setdefault(
            condition_id,
            {
                "condition_id": condition_id,
                "resolved_at": resolved_at,
                "best_candidate": None,
            },
        )
        if resolved_at:
            window["resolved_at"] = resolved_at

        signal = str(record.get("signal", "") or "")
        phase = str(record.get("candidate_phase") or record.get("phase_bucket") or "").upper()
        correct = record.get("prediction_correct")
        if signal not in (LABEL_BUY_UP, LABEL_BUY_DOWN):
            continue
        if phase not in ("RESERVE", "EARLY_EXEC", "LATE_EXEC"):
            continue
        if not isinstance(correct, bool):
            continue

        candidate = {
            "signal": signal,
            "phase": phase,
            "confidence": _safe_float(record.get("confidence"), 0.0),
            "correct": correct,
            "blocked_gate": str(record.get("blocked_gate", "") or ""),
            "threshold_source": str(record.get("threshold_source", "") or ""),
            "threshold_profile_version": str(record.get("threshold_profile_version", "") or ""),
        }
        best = window.get("best_candidate")
        if best is None:
            window["best_candidate"] = candidate
            continue
        best_conf = _safe_float(best.get("confidence"), 0.0)
        cand_conf = _safe_float(candidate.get("confidence"), 0.0)
        if cand_conf > best_conf or (math.isclose(cand_conf, best_conf) and phase == "LATE_EXEC" and best.get("phase") != "LATE_EXEC"):
            window["best_candidate"] = candidate

    rows = list(windows.values())
    rows.sort(key=lambda item: str(item.get("resolved_at", "")))
    return rows


def _evaluate_threshold_profile(
    windows: list[dict[str, Any]],
    profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    normalized = _normalize_runtime_thresholds(profile)
    total_windows = len(windows)
    executed = 0
    hits = 0
    phase_hits: dict[str, int] = defaultdict(int)
    phase_totals: dict[str, int] = defaultdict(int)
    for window in windows:
        candidate = window.get("best_candidate")
        if not isinstance(candidate, dict):
            continue
        threshold = _threshold_floor_for_bucket(str(candidate.get("phase", "")), normalized)
        if _safe_float(candidate.get("confidence"), 0.0) < threshold:
            continue
        executed += 1
        phase = str(candidate.get("phase", "") or "")
        if phase:
            phase_totals[phase] += 1
        if bool(candidate.get("correct")):
            hits += 1
            if phase:
                phase_hits[phase] += 1
    win_rate = (hits / executed) if executed else 0.0
    coverage = (executed / total_windows) if total_windows else 0.0
    return {
        "total_windows": total_windows,
        "executed_windows": executed,
        "coverage": round(coverage, 4),
        "win_rate": round(win_rate, 4),
        "win_rate_by_phase": {
            phase: round(phase_hits[phase] / total, 4)
            for phase, total in phase_totals.items()
            if total > 0
        },
    }


def _threshold_counterfactuals(windows: list[dict[str, Any]], thresholds: tuple[float, ...] = (0.72, 0.74, 0.76, 0.78)) -> dict[str, dict[str, Any]]:
    report: dict[str, dict[str, Any]] = {}
    base = _default_runtime_thresholds()
    for threshold in thresholds:
        profile = {
            **base,
            "reserve": threshold,
            "early_exec": threshold,
            "late_exec": max(threshold, base["late_exec"]),
            "source": "counterfactual",
            "version": f"cf_{threshold:.2f}",
        }
        report[f"{threshold:.2f}"] = _evaluate_threshold_profile(windows, profile)
    return report


def tune_runtime_thresholds_from_shadow_data(
    log_dir: str | Path,
    *,
    lookback_days: int = ML_THRESHOLD_LOOKBACK_DAYS,
    min_win_rate: float = ML_MIN_EXEC_WIN_RATE,
    min_windows: int = ML_THRESHOLD_MIN_WINDOWS,
    coverage_target: float = ML_TARGET_EXEC_COVERAGE,
    threshold_mode: str = ML_THRESHOLD_MODE,
) -> dict[str, Any]:
    mode = str(threshold_mode or "auto").strip().lower()
    default_profile = _default_runtime_thresholds()
    windows = _load_threshold_tuning_windows(log_dir, lookback_days=lookback_days)
    summary: dict[str, Any] = {
        "lookback_days": lookback_days,
        "window_count": len(windows),
        "min_windows": min_windows,
        "min_win_rate": min_win_rate,
        "coverage_target": coverage_target,
        "counterfactual_recent24": _threshold_counterfactuals(windows[-24:]),
        "counterfactual_recent100": _threshold_counterfactuals(windows[-100:]),
    }
    if mode != "auto":
        default_profile["source"] = "default"
        return {
            "runtime_thresholds": default_profile,
            "threshold_mode": mode,
            "threshold_tuning_summary": {**summary, "selected": "default_non_auto"},
            "threshold_source": "default",
        }
    if len(windows) < min_windows:
        default_profile["source"] = "default"
        return {
            "runtime_thresholds": default_profile,
            "threshold_mode": "auto",
            "threshold_tuning_summary": {**summary, "selected": "default_insufficient_windows"},
            "threshold_source": "default",
        }

    values = [round(0.70 + step * 0.01, 2) for step in range(13)]
    best_profile: dict[str, Any] | None = None
    best_eval: dict[str, Any] | None = None
    evaluated_profiles = 0
    for reserve in values:
        for early_exec in values:
            for late_exec in values:
                profile = {
                    **default_profile,
                    "reserve": reserve,
                    "early_exec": early_exec,
                    "late_exec": late_exec,
                    "source": "auto_tuned",
                    "version": f"auto_{reserve:.2f}_{early_exec:.2f}_{late_exec:.2f}",
                }
                evaluation = _evaluate_threshold_profile(windows, profile)
                evaluated_profiles += 1
                if evaluation["executed_windows"] <= 0:
                    continue
                if evaluation["win_rate"] < min_win_rate:
                    continue
                if best_eval is None:
                    best_profile = profile
                    best_eval = evaluation
                    continue
                current_rank = (evaluation["coverage"], evaluation["win_rate"], late_exec, early_exec, reserve)
                best_rank = (
                    best_eval["coverage"],
                    best_eval["win_rate"],
                    _safe_float(best_profile["late_exec"]),
                    _safe_float(best_profile["early_exec"]),
                    _safe_float(best_profile["reserve"]),
                )
                if current_rank > best_rank:
                    best_profile = profile
                    best_eval = evaluation

    summary["evaluated_profiles"] = evaluated_profiles
    if best_profile is None or best_eval is None:
        default_profile["source"] = "default"
        return {
            "runtime_thresholds": default_profile,
            "threshold_mode": "auto",
            "threshold_tuning_summary": {**summary, "selected": "default_guardrail_no_profile"},
            "threshold_source": "default",
        }

    recent24 = _evaluate_threshold_profile(windows[-24:], best_profile)
    recent100 = _evaluate_threshold_profile(windows[-100:], best_profile)
    summary["selected_profile"] = dict(best_profile)
    summary["selected_metrics"] = dict(best_eval)
    summary["selected_recent24"] = recent24
    summary["selected_recent100"] = recent100
    if (
        (recent24["executed_windows"] >= 8 and recent24["win_rate"] < min_win_rate)
        or (recent100["executed_windows"] >= 20 and recent100["win_rate"] < min_win_rate)
    ):
        default_profile["source"] = "default"
        return {
            "runtime_thresholds": default_profile,
            "threshold_mode": "auto",
            "threshold_tuning_summary": {**summary, "selected": "default_auto_reverted"},
            "threshold_source": "default",
        }

    return {
        "runtime_thresholds": _normalize_runtime_thresholds(best_profile),
        "threshold_mode": "auto",
        "threshold_tuning_summary": {**summary, "selected": "auto_tuned"},
        "threshold_source": "auto_tuned",
    }


def _prob_to_signal(prob_up: float, threshold: float = 0.5) -> str:
    if prob_up >= threshold:
        return LABEL_BUY_UP
    return LABEL_BUY_DOWN


def _build_row_id(condition_id: str, ts: str, prefix: str = "live") -> str:
    return f"{prefix}:{condition_id}:{ts}:{uuid.uuid4().hex[:12]}"


def _append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, default=str) + "\n")


LABEL_SOURCE_PRIORITY = {
    "chainlink_market_resolved": 400,
    "market_settlement_lookup": 350,
    "binance_15s": 200,
    "binance_90s": 100,
    "window_resolution": 50,
}


def _label_source_priority(source: str | None) -> int:
    return int(LABEL_SOURCE_PRIORITY.get(str(source or "").strip(), 0))


def _best_record_by_priority(
    current: dict[str, Any] | None,
    candidate: dict[str, Any] | None,
    *,
    source_key: str,
    ts_key: str,
) -> dict[str, Any] | None:
    if candidate is None:
        return current
    if current is None:
        return candidate

    current_priority = _label_source_priority(current.get(source_key))
    candidate_priority = _label_source_priority(candidate.get(source_key))
    if candidate_priority > current_priority:
        return candidate
    if candidate_priority < current_priority:
        return current

    current_ts = ml_parse_utc_ts(current.get(ts_key))
    candidate_ts = ml_parse_utc_ts(candidate.get(ts_key))
    if current_ts is None:
        return candidate
    if candidate_ts is None:
        return current
    return candidate if candidate_ts >= current_ts else current


def _extract_numeric_price(payload: Any, target_keys: set[str]) -> float | None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key.lower() in target_keys:
                raw = _safe_float(value, 0.0)
                if raw > 1000.0:
                    return raw
            nested = _extract_numeric_price(value, target_keys)
            if nested is not None:
                return nested
    elif isinstance(payload, list):
        for item in payload:
            nested = _extract_numeric_price(item, target_keys)
            if nested is not None:
                return nested
    return None


def _extract_string_value(payload: Any, target_keys: set[str]) -> str:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key.lower() in target_keys and value not in (None, ""):
                return str(value)
            nested = _extract_string_value(value, target_keys)
            if nested:
                return nested
    elif isinstance(payload, list):
        for item in payload:
            nested = _extract_string_value(item, target_keys)
            if nested:
                return nested
    return ""


def _extract_settlement_price(payload: dict[str, Any]) -> float | None:
    return _extract_numeric_price(
        payload,
        {
            "settlement_price",
            "settlementprice",
            "oracle_price",
            "oracleprice",
            "resolution_price",
            "resolutionprice",
            "resolved_price",
            "resolvedprice",
            "final_price",
            "finalprice",
        },
    )


def _extract_resolved_at(payload: dict[str, Any]) -> str:
    return _extract_string_value(
        payload,
        {
            "resolved_at",
            "resolvedat",
            "resolution_ts",
            "resolutionts",
            "timestamp",
            "time",
            "ts",
        },
    )


@dataclass
class SettlementRecord:
    condition_id: str
    resolved_at: str
    settlement_price: float
    settlement_source: str = "chainlink_market_resolved"
    settlement_source_priority: int = 0
    market_id: str = ""
    chainlink_settlement_price: float | None = None
    raw_payload: dict[str, Any] = field(default_factory=dict)
    schema_version: str = FEATURE_SCHEMA_VERSION

    def to_record(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SettlementInfo:
    settlement_price: float
    settlement_source: str
    resolved_at: datetime | None
    settlement_source_priority: int
    chainlink_settlement_price: float | None = None
    binance_resolution_diff_s: float | None = None


@dataclass
class ClaimAttemptResult:
    success: bool
    status: str
    tx_hash: str = ""
    request_id: str = ""
    error_code: str = ""
    error_message: str = ""


@dataclass
class ClaimRecord:
    claim_id: str
    condition_id: str
    market_id: str = ""
    asset: str = ""
    outcome: str = ""
    outcome_index: int = -1
    title: str = ""
    end_date: str = ""
    claimable_amount: float = 0.0
    claim_source: str = "positions_api_redeemable"
    status: str = "discovered"
    attempt_count: int = 0
    last_attempt_at: str = ""
    last_seen_at: str = ""
    queued_at: str = ""
    tx_hash: str = ""
    request_id: str = ""
    error_code: str = ""
    error_message: str = ""
    redeemable: bool = False
    mergeable: bool = False
    negative_risk: bool = False
    proxy_wallet: str = ""
    scan_identity: str = ""
    schema_version: str = FEATURE_SCHEMA_VERSION

    def to_record(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SignalFeatures:
    row_id: str
    ts: str
    condition_id: str
    window_start_at: str
    window_end_at: str
    beat_price: float
    btc_price: float
    up_odds: float
    down_odds: float
    gap_pct: float
    gap_signed_pct: float
    seconds_remaining: int
    signal_alignment: int
    signed_alignment: float
    odds_vel: float
    odds_vel_accel: float
    cvd_divergence: int
    macd_histogram: float
    bb_pct_b: float
    rsi: float
    momentum_pct: float
    is_late_window: int
    is_bandar_zone: int
    is_proximity_risk: int
    price_roc_15s: float
    price_roc_30s: float
    cvd_change_last_30s: float
    odds_edge_strength: float
    elapsed_fraction: float = 0.0
    is_proximity_risk_above: int = 0
    is_proximity_risk_below: int = 0
    gap_alignment_interaction: float = 0.0
    realized_vol_30s: float = 0.0
    realized_vol_60s: float = 0.0
    gap_signed_pct_lag1: float = 0.0
    signal_alignment_lag1: float = 0.0
    odds_edge_strength_lag1: float = 0.0
    gap_crossed_zero: int = 0
    ob_imbalance: float = 0.0
    beat_above_ratio: float = 0.5
    fair_up: float = 0.5
    fair_down: float = 0.5
    edge_up: float = 0.0
    edge_down: float = 0.0
    direction_bias: str = "NONE"
    dip_label: str = "UNKNOWN"
    feature_source: str = "live"
    phase_bucket: str = ""
    feature_bars: int = 0
    feature_completeness: float = 0.0
    schema_version: str = FEATURE_SCHEMA_VERSION

    def to_record(self) -> dict[str, Any]:
        return asdict(self)

    def model_record(self) -> dict[str, float]:
        return {
            name: _safe_float(getattr(self, name, NUMERIC_DEFAULTS.get(name, 0.0)), NUMERIC_DEFAULTS.get(name, 0.0))
            for name in MODEL_FEATURE_COLUMNS
        }


@dataclass
class ResolvedLabelRecord:
    row_id: str
    condition_id: str
    resolution_ts: str
    resolved_label: str
    resolved_btc_price: float
    label_source: str = "window_resolution"
    chainlink_settlement_price: float | None = None
    binance_resolution_diff_s: float | None = None
    settlement_source_priority: int = 0
    schema_version: str = FEATURE_SCHEMA_VERSION

    def to_record(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class SignalPrediction:
    signal: str
    confidence: float
    reason: str
    source: str
    model_version: str
    prob_up: float
    prob_down: float
    promotion_state: str
    raw_confidence: float = 0.0
    runtime_skip_reason_code: str = ""
    soft_penalties_applied: list[str] = field(default_factory=list)
    candidate_confidence_floor: float = 0.0
    threshold_profile_version: str = ""
    threshold_source: str = "default"
    candidate_phase: str = ""
    action_phase: str = ""
    shadow: dict[str, Any] | None = None


@dataclass
class ModelManifest:
    model_name: str
    model_version: str
    trained_at: str
    feature_list: list[str]
    training_range: dict[str, str]
    metrics: dict[str, Any]
    promotion_state: str
    artifact_paths: dict[str, str]
    applied_state: str = ""
    activated_at: str = ""
    activation_reason: str = ""
    runtime_thresholds: dict[str, Any] = field(default_factory=dict)
    threshold_mode: str = "default"
    threshold_tuning_summary: dict[str, Any] = field(default_factory=dict)
    coverage_target: float = ML_TARGET_EXEC_COVERAGE
    min_win_rate_target: float = ML_MIN_EXEC_WIN_RATE

    def to_record(self) -> dict[str, Any]:
        return asdict(self)


class IdentityCalibrator:
    def predict(self, values: list[float] | np.ndarray) -> np.ndarray:
        return np.clip(np.asarray(values, dtype=float), 0.0, 1.0)


class ModelRegistry:
    def __init__(self, root_dir: str | Path = DEFAULT_MODELS_DIR, model_name: str = MODEL_NAME) -> None:
        self.root_dir = Path(root_dir)
        self.model_name = model_name
        self.model_dir = self.root_dir / model_name
        self.versions_dir = self.model_dir / "versions"
        self.active_manifest_path = self.model_dir / "active_manifest.json"
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.versions_dir.mkdir(parents=True, exist_ok=True)

    def list_versions(self) -> list[Path]:
        return sorted(
            [path for path in self.versions_dir.iterdir() if path.is_dir()],
            key=lambda item: item.name,
        )

    def latest_version_dir(self) -> Path | None:
        versions = self.list_versions()
        return versions[-1] if versions else None

    def load_manifest(self, path: str | Path | None = None) -> ModelManifest | None:
        manifest_path = Path(path) if path else self.active_manifest_path
        if not manifest_path.exists():
            return None
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            return ModelManifest(**data)
        except Exception:
            return None

    def load_active_bundle(self) -> tuple[Any, Any, ModelManifest] | None:
        manifest = self.load_manifest()
        if manifest is None:
            return None
        try:
            model = joblib.load(manifest.artifact_paths["model"])
            calibrator_path = manifest.artifact_paths.get("calibrator", "")
            calibrator = joblib.load(calibrator_path) if calibrator_path else IdentityCalibrator()
            return model, calibrator, manifest
        except Exception:
            return None

    def save_bundle(
        self,
        *,
        model: Any,
        calibrator: Any,
        metrics: dict[str, Any],
        promotion_state: str,
        activation_reason: str = "train_outcome_model",
    ) -> ModelManifest:
        if promotion_state not in PROMOTION_STATES:
            promotion_state = "shadow"

        schema_suffix = FEATURE_SCHEMA_VERSION.replace(".", "")
        version = f"{_utc_now().strftime('%Y%m%dT%H%M%SZ')}-s{schema_suffix}"
        version_dir = self.versions_dir / version
        version_dir.mkdir(parents=True, exist_ok=True)

        model_path = version_dir / "model.joblib"
        calibrator_path = version_dir / "calibrator.joblib"
        feature_schema_path = version_dir / "feature_schema.json"
        metrics_path = version_dir / "metrics.json"
        manifest_path = version_dir / "manifest.json"

        joblib.dump(model, model_path)
        joblib.dump(calibrator, calibrator_path)
        feature_schema_path.write_text(
            json.dumps(
                {
                    "schema_version": FEATURE_SCHEMA_VERSION,
                    "model_name": self.model_name,
                    "feature_list": MODEL_FEATURE_COLUMNS,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

        manifest = ModelManifest(
            model_name=self.model_name,
            model_version=version,
            trained_at=_iso_z(_utc_now()),
            feature_list=list(MODEL_FEATURE_COLUMNS),
            training_range=metrics.get("training_range", {}),
            metrics=metrics,
            promotion_state=promotion_state,
            artifact_paths={
                "model": str(model_path),
                "calibrator": str(calibrator_path),
                "feature_schema": str(feature_schema_path),
                "metrics": str(metrics_path),
                "manifest": str(manifest_path),
            },
            applied_state=promotion_state,
            activated_at=_iso_z(_utc_now()),
            activation_reason=activation_reason,
            runtime_thresholds=_normalize_runtime_thresholds(metrics.get("runtime_thresholds")),
            threshold_mode=str(metrics.get("threshold_mode", ML_THRESHOLD_MODE) or ML_THRESHOLD_MODE),
            threshold_tuning_summary=dict(metrics.get("threshold_tuning_summary", {}) or {}),
            coverage_target=_safe_float(metrics.get("coverage_target"), ML_TARGET_EXEC_COVERAGE),
            min_win_rate_target=_safe_float(metrics.get("min_win_rate_target"), ML_MIN_EXEC_WIN_RATE),
        )
        manifest_path.write_text(json.dumps(manifest.to_record(), indent=2), encoding="utf-8")
        if promotion_state == "active":
            self.active_manifest_path.write_text(json.dumps(manifest.to_record(), indent=2), encoding="utf-8")
        self.prune_old_versions(keep=6)
        return manifest

    def set_active_version(
        self,
        version: str | None = None,
        promotion_state: str = "active",
        activation_reason: str = "manual",
    ) -> ModelManifest | None:
        if promotion_state not in PROMOTION_STATES:
            promotion_state = "active"

        if version in (None, "", "latest"):
            version_dir = self.latest_version_dir()
        else:
            version_dir = self.versions_dir / version
        if version_dir is None:
            return None

        manifest_path = version_dir / "manifest.json"
        if not manifest_path.exists():
            return None

        manifest = self.load_manifest(manifest_path)
        if manifest is None:
            return None

        manifest.promotion_state = promotion_state
        manifest.applied_state = promotion_state
        manifest.activated_at = _iso_z(_utc_now())
        manifest.activation_reason = activation_reason
        manifest_path.write_text(json.dumps(manifest.to_record(), indent=2), encoding="utf-8")
        self.active_manifest_path.write_text(json.dumps(manifest.to_record(), indent=2), encoding="utf-8")
        return manifest

    def prune_old_versions(self, keep: int = 6) -> None:
        versions = self.list_versions()
        if len(versions) <= keep:
            return
        active = self.load_manifest()
        active_version = active.model_version if active else ""
        removable = [path for path in versions if path.name != active_version]
        to_remove = max(0, len(versions) - keep)
        for version_dir in removable[:to_remove]:
            for child in sorted(version_dir.glob("**/*"), reverse=True):
                if child.is_file():
                    child.unlink(missing_ok=True)
            for child in sorted(version_dir.glob("**/*"), reverse=True):
                if child.is_dir():
                    child.rmdir()
            version_dir.rmdir()


@dataclass
class RuntimePolicy:
    legacy_strict_confidence: float = 0.80
    legacy_strict_edge: float = 0.05
    legacy_strict_spread_floor: float = 0.02
    observe_min_confidence: float = 0.70
    observe_min_edge: float = 0.02
    observe_spread_floor: float = 0.02
    reserve_min_confidence: float = 0.74
    reserve_min_edge: float = 0.02
    reserve_spread_floor: float = 0.015
    early_exec_min_confidence: float = 0.74
    early_exec_min_edge: float = 0.02
    early_exec_spread_floor: float = 0.015
    late_exec_min_confidence: float = 0.76
    late_exec_min_edge: float = 0.03
    late_exec_spread_floor: float = 0.02
    late_window_confidence: float = 0.85
    early_exec_safety_floor: float = 0.74
    late_exec_safety_floor: float = 0.76

    @staticmethod
    def _phase_bucket(features: SignalFeatures) -> str:
        bucket = str(getattr(features, "phase_bucket", "") or "").upper()
        if bucket:
            return bucket
        elapsed_s = int(round(_safe_float(getattr(features, "elapsed_fraction", 0.0), 0.0) * 300.0))
        seconds_remaining = _safe_int(getattr(features, "seconds_remaining", 0), 0)
        return _phase_bucket_from_timing(elapsed_s, seconds_remaining)

    def _thresholds(self, features: SignalFeatures, threshold_profile: dict[str, Any] | None = None) -> tuple[str, float, float, float, float, dict[str, Any]]:
        bucket = self._phase_bucket(features)
        profile = _normalize_runtime_thresholds(threshold_profile)
        if not _bet_frequency_phase_at_least("C"):
            return (
                bucket,
                self.legacy_strict_confidence,
                self.legacy_strict_edge,
                self.legacy_strict_spread_floor,
                self.legacy_strict_confidence,
                {"version": "legacy_phase", "source": "legacy"},
            )
        if bucket == "RESERVE":
            return (
                bucket,
                _safe_float(profile.get("reserve"), self.reserve_min_confidence),
                self.reserve_min_edge,
                self.reserve_spread_floor,
                _safe_float(profile.get("reserve"), self.reserve_min_confidence),
                profile,
            )
        if bucket == "EARLY_EXEC":
            return (
                bucket,
                _safe_float(profile.get("early_exec"), self.early_exec_min_confidence),
                self.early_exec_min_edge,
                self.early_exec_spread_floor,
                self.early_exec_safety_floor,
                profile,
            )
        if bucket == "LATE_EXEC":
            return (
                bucket,
                _safe_float(profile.get("late_exec"), self.late_exec_min_confidence),
                self.late_exec_min_edge,
                self.late_exec_spread_floor,
                max(self.late_exec_safety_floor, _safe_float(profile.get("late_exec"), self.late_exec_min_confidence)),
                profile,
            )
        return (
            bucket,
            _safe_float(profile.get("observe"), self.observe_min_confidence),
            self.observe_min_edge,
            self.observe_spread_floor,
            _safe_float(profile.get("observe"), self.observe_min_confidence),
            profile,
        )

    def decide(
        self,
        features: SignalFeatures,
        prob_up: float,
        prob_down: float,
        reason_prefix: str,
        source: str,
        model_version: str,
        promotion_state: str,
        threshold_profile: dict[str, Any] | None = None,
    ) -> SignalPrediction:
        prob_up = _clip_probability(prob_up)
        prob_down = _clip_probability(prob_down)
        side = LABEL_BUY_UP if prob_up >= prob_down else LABEL_BUY_DOWN
        confidence = prob_up if side == LABEL_BUY_UP else prob_down
        market_odds = features.up_odds if side == LABEL_BUY_UP else features.down_odds
        edge = (confidence / market_odds - 1.0) if 0.0 < market_odds < 1.0 else 0.0
        spread = abs(prob_up - prob_down)
        phase_bucket, candidate_floor, min_edge, spread_floor, safety_floor, profile = self._thresholds(features, threshold_profile=threshold_profile)
        required_conf = max(candidate_floor, safety_floor)
        _proximity_active = features.is_bandar_zone or features.is_proximity_risk or features.is_proximity_risk_above or features.is_proximity_risk_below
        if phase_bucket in ("RESERVE", "EARLY_EXEC", "LATE_EXEC") and _proximity_active:
            bump = _safe_float(profile.get("late_risk_bump"), SOFT_PENALTY_CONF_BUMP)
            # Extra bump for contrarian bets: betting against the current price position.
            if side == LABEL_BUY_UP and features.is_proximity_risk_below:
                bump += SOFT_PENALTY_CONF_BUMP  # UP bet when price is BELOW target
            elif side == LABEL_BUY_DOWN and features.is_proximity_risk_above:
                bump += SOFT_PENALTY_CONF_BUMP  # DOWN bet when price is ABOVE target
            required_conf += bump

        if spread < spread_floor:
            return SignalPrediction(
                signal=LABEL_SKIP,
                confidence=confidence,
                raw_confidence=confidence,
                reason=f"{reason_prefix}: probability spread {spread:.1%} too small",
                source=source,
                model_version=model_version,
                prob_up=prob_up,
                prob_down=prob_down,
                promotion_state=promotion_state,
                runtime_skip_reason_code="RUNTIME_SPREAD_FLOOR",
                candidate_confidence_floor=required_conf,
                threshold_profile_version=str(profile.get("version", "")),
                threshold_source=str(profile.get("source", "default")),
                candidate_phase=phase_bucket,
                action_phase=phase_bucket,
            )

        if edge < min_edge:
            return SignalPrediction(
                signal=LABEL_SKIP,
                confidence=confidence,
                raw_confidence=confidence,
                reason=f"{reason_prefix}: edge {edge:+.1%} below {min_edge:.0%}",
                source=source,
                model_version=model_version,
                prob_up=prob_up,
                prob_down=prob_down,
                promotion_state=promotion_state,
                runtime_skip_reason_code="RUNTIME_EDGE_FLOOR",
                candidate_confidence_floor=required_conf,
                threshold_profile_version=str(profile.get("version", "")),
                threshold_source=str(profile.get("source", "default")),
                candidate_phase=phase_bucket,
                action_phase=phase_bucket,
            )

        if confidence < required_conf:
            return SignalPrediction(
                signal=LABEL_SKIP,
                confidence=confidence,
                raw_confidence=confidence,
                reason=f"{reason_prefix}: candidate confidence {confidence:.0%} below {required_conf:.0%}",
                source=source,
                model_version=model_version,
                prob_up=prob_up,
                prob_down=prob_down,
                promotion_state=promotion_state,
                runtime_skip_reason_code="RUNTIME_CANDIDATE_FLOOR",
                candidate_confidence_floor=required_conf,
                threshold_profile_version=str(profile.get("version", "")),
                threshold_source=str(profile.get("source", "default")),
                candidate_phase=phase_bucket,
                action_phase=phase_bucket,
            )

        return SignalPrediction(
            signal=side,
            confidence=confidence,
            raw_confidence=confidence,
            reason=f"{reason_prefix}: {side} prob={confidence:.0%} edge={edge:+.1%}",
            source=source,
            model_version=model_version,
            prob_up=prob_up,
            prob_down=prob_down,
            promotion_state=promotion_state,
            runtime_skip_reason_code="",
            candidate_confidence_floor=required_conf,
            threshold_profile_version=str(profile.get("version", "")),
            threshold_source=str(profile.get("source", "default")),
            candidate_phase=phase_bucket,
            action_phase=phase_bucket,
        )


class RuntimeSignalEngine:
    def __init__(
        self,
        registry: ModelRegistry | None = None,
        *,
        policy: RuntimePolicy | None = None,
        stale_after_hours: int = 72,
    ) -> None:
        self.registry = registry or ModelRegistry()
        self.policy = policy or RuntimePolicy()
        self.stale_after_hours = stale_after_hours
        self._bundle_lock = threading.RLock()
        self._bundle: tuple[Any, Any, ModelManifest] | None = None
        self._active_manifest_mtime: float = 0.0
        self.reload()

    def _active_manifest_stat_mtime(self) -> float:
        try:
            return self.registry.active_manifest_path.stat().st_mtime
        except Exception:
            return 0.0

    def reload(self) -> ModelManifest | None:
        bundle = self.registry.load_active_bundle()
        if bundle is None:
            return None
        _, _, manifest = bundle
        with self._bundle_lock:
            self._bundle = bundle
            self._active_manifest_mtime = self._active_manifest_stat_mtime()
        return manifest

    def maybe_reload(self) -> ModelManifest | None:
        current_mtime = self._active_manifest_stat_mtime()
        with self._bundle_lock:
            known_mtime = self._active_manifest_mtime
        if current_mtime and current_mtime != known_mtime:
            return self.reload()
        return None

    def current_manifest(self) -> ModelManifest | None:
        with self._bundle_lock:
            if self._bundle is None:
                return None
            return self._bundle[2]

    def _heuristic_probability(self, features: SignalFeatures) -> float:
        prob_up = _safe_float(features.fair_up, 0.5)
        prob_up += 0.12 * math.tanh(features.gap_signed_pct / 0.08)
        prob_up += 0.10 * (features.signed_alignment / 6.0)
        prob_up += 0.05 * math.tanh(features.odds_vel * 1000.0 / 8.0)
        prob_up += 0.05 * math.tanh(features.odds_edge_strength / 0.15)
        prob_up += 0.04 * math.tanh(features.momentum_pct / 0.12)
        prob_up += 0.03 * math.tanh(features.macd_histogram / 25.0)
        prob_up += 0.03 * features.cvd_divergence
        if features.is_proximity_risk_below:
            # Price is BELOW target in final 60s: heavy dampening toward DOWN.
            prob_up = 0.4 * prob_up + 0.20
        elif features.is_proximity_risk_above:
            # Price is just ABOVE target in final 60s: gentle dampening toward 50/50.
            prob_up = 0.5 * prob_up + 0.25
        elif features.is_proximity_risk:
            # Fallback for older feature rows that don't have the split fields.
            prob_up = 0.5 * prob_up + 0.25
        # Sanity cap: price meaningfully below target in final 60s — UP reversal is unlikely.
        # Prevents lagging technicals from inflating UP confidence when gap has clearly crossed down.
        if features.is_late_window and features.gap_signed_pct < -0.02:
            prob_up = min(prob_up, 0.65)
        # Symmetric cap: price meaningfully above target in final 60s — DOWN reversal is unlikely.
        if features.is_late_window and features.gap_signed_pct > 0.02:
            prob_up = max(prob_up, 0.35)  # i.e., DOWN confidence ≤ 65%
        return _clip_probability(prob_up)

    def _predict_model_probability(self, features: SignalFeatures, bundle: tuple[Any, Any, ModelManifest] | None) -> tuple[float, str]:
        if bundle is None:
            return 0.5, "no active model"

        model, calibrator, manifest = bundle
        trained_at = ml_parse_utc_ts(manifest.trained_at)
        if trained_at is not None:
            age_h = (_utc_now() - trained_at).total_seconds() / 3600.0
            if age_h > self.stale_after_hours:
                return 0.5, f"model stale ({age_h:.1f}h)"

        feature_list = list(manifest.feature_list or MODEL_FEATURE_COLUMNS)
        frame = pd.DataFrame(
            [
                {
                    name: _safe_float(
                        getattr(features, name, NUMERIC_DEFAULTS.get(name, 0.0)),
                        NUMERIC_DEFAULTS.get(name, 0.0),
                    )
                    for name in feature_list
                }
            ],
            columns=feature_list,
        )
        if frame.isnull().values.any():
            return 0.5, "feature vector contains NaN"

        raw = model.predict_proba(frame)
        if raw.ndim != 2 or raw.shape[1] < 2:
            return 0.5, "unexpected probability output"

        prob_up = float(raw[0][1])
        try:
            prob_up = float(calibrator.predict([prob_up])[0])
        except Exception:
            pass
        # Sanity cap: price meaningfully below target in final 60s — cap ML UP confidence.
        # Counteracts the model's learned bias of "proximity + bullish technicals = high UP".
        if features.is_late_window and features.gap_signed_pct < -0.02:
            prob_up = min(prob_up, 0.65)
        # Symmetric cap: price meaningfully above target in final 60s — cap ML DOWN confidence.
        if features.is_late_window and features.gap_signed_pct > 0.02:
            prob_up = max(prob_up, 0.35)  # i.e., DOWN confidence ≤ 65%
        return _clip_probability(prob_up), ""

    def predict(self, features: SignalFeatures) -> SignalPrediction:
        self.maybe_reload()
        threshold_profile = _default_runtime_thresholds()
        fallback_prob_up = self._heuristic_probability(features)

        with self._bundle_lock:
            bundle = self._bundle

        if bundle is not None:
            threshold_profile = _manifest_runtime_threshold_payload(bundle[2])

        fallback_prediction = self.policy.decide(
            features,
            fallback_prob_up,
            1.0 - fallback_prob_up,
            reason_prefix="fallback",
            source="fallback",
            model_version="fallback",
            promotion_state="fallback",
            threshold_profile=threshold_profile,
        )

        if bundle is None:
            return fallback_prediction

        _, _, manifest = bundle
        prob_up, error = self._predict_model_probability(features, bundle)
        if error:
            fallback_prediction.reason = f"{fallback_prediction.reason} | model={error}"
            return fallback_prediction

        ml_prediction = self.policy.decide(
            features,
            prob_up,
            1.0 - prob_up,
            reason_prefix="ml",
            source="ml",
            model_version=manifest.model_version,
            promotion_state=manifest.promotion_state,
            threshold_profile=threshold_profile,
        )

        if manifest.promotion_state == "active":
            return ml_prediction

        fallback_prediction.shadow = {
            "signal": ml_prediction.signal,
            "confidence": ml_prediction.confidence,
            "prob_up": ml_prediction.prob_up,
            "prob_down": ml_prediction.prob_down,
            "source": "ml_shadow" if manifest.promotion_state == "shadow" else "ml_assist",
            "model_version": manifest.model_version,
            "promotion_state": manifest.promotion_state,
            "reason": ml_prediction.reason,
        }
        return fallback_prediction


def ml_compute_edge(fair_prob: float, market_odds: float) -> float:
    if market_odds <= 0.0 or market_odds >= 1.0:
        return 0.0
    return fair_prob * (1.0 / market_odds) - 1.0


def ml_compute_rsi(prices: list[float], period: int = 14) -> float | None:
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


def ml_compute_momentum(prices: list[float], ticks: int = 10) -> float | None:
    if len(prices) < ticks + 1:
        return None
    baseline = prices[-(ticks + 1)]
    if baseline == 0:
        return None
    return (prices[-1] - baseline) / baseline * 100.0


def _ema_series(prices: list[float], period: int) -> list[float]:
    if len(prices) < period:
        return []
    k = 2.0 / (period + 1)
    seed = float(np.mean(prices[:period]))
    series = [seed]
    for price in prices[period:]:
        series.append(price * k + series[-1] * (1.0 - k))
    return series


def compute_macd_histogram(prices: list[float], fast: int = 12, slow: int = 26, signal_period: int = 9) -> float | None:
    if len(prices) < slow + signal_period:
        return None
    fast_ema = _ema_series(prices, fast)
    slow_ema = _ema_series(prices, slow)
    offset = slow - fast
    macd = [fast_val - slow_val for fast_val, slow_val in zip(fast_ema[offset:], slow_ema)]
    if len(macd) < signal_period:
        return None
    signal = _ema_series(macd, signal_period)
    if not signal:
        return None
    return float(macd[-1] - signal[-1])


def compute_bb_pct_b(prices: list[float], period: int = 20, std_mult: float = 2.0) -> float | None:
    if len(prices) < period:
        return None
    subset = np.asarray(prices[-period:], dtype=float)
    middle = float(np.mean(subset))
    std = float(np.std(subset, ddof=0))
    upper = middle + std_mult * std
    lower = middle - std_mult * std
    span = upper - lower
    if span <= 0:
        return 0.5
    return float((prices[-1] - lower) / span)


def ml_compute_odds_velocity(odds_history: list[tuple[float, float, float]], lookback_s: float = 30.0) -> tuple[float, float]:
    if len(odds_history) < 4:
        return 0.0, 0.0
    now = odds_history[-1][0]
    cutoff = now - lookback_s
    baseline = None
    for entry in odds_history:
        if entry[0] >= cutoff:
            baseline = entry
            break
    if baseline is None:
        return 0.0, 0.0

    current_up = odds_history[-1][1]
    baseline_up = baseline[1]
    elapsed = max(odds_history[-1][0] - baseline[0], 1.0)
    velocity = (current_up - baseline_up) / elapsed

    mid_idx = len(odds_history) // 2
    mid_up = odds_history[mid_idx][1]
    mid_ts = odds_history[mid_idx][0]
    first_half = (mid_up - baseline_up) / max(mid_ts - baseline[0], 1.0)
    second_half = (current_up - mid_up) / max(now - mid_ts, 1.0)
    acceleration = second_half - first_half
    return float(velocity), float(acceleration)


def ml_compute_fair_probability(btc_price: float, beat_price: float, seconds_remaining: float, prices: list[float]) -> tuple[float, float]:
    if seconds_remaining < 5 or len(prices) < 10 or beat_price <= 0:
        return 0.5, 0.5
    changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    if not changes:
        return 0.5, 0.5
    variance_5s = sum(change ** 2 for change in changes) / len(changes)
    std_5s = variance_5s ** 0.5
    vol_per_s = max(std_5s / math.sqrt(5), 0.50)
    z = (btc_price - beat_price) / (vol_per_s * math.sqrt(seconds_remaining))
    fair_up = 0.5 * (1.0 + math.erf(z / math.sqrt(2)))
    return float(fair_up), float(1.0 - fair_up)


def ml_compute_dip_label(prices: list[float], beat_price: float, btc_price: float) -> str:
    window = prices[-20:] if len(prices) >= 20 else prices
    if len(window) < 4:
        return "INSUFFICIENT_DATA"
    above = sum(1 for price in window if price >= beat_price)
    above_pct = above / len(window) * 100.0
    below_pct = 100.0 - above_pct
    if above_pct >= 60.0 and btc_price < beat_price:
        return "TEMPORARY_DIP"
    if below_pct >= 80.0:
        return "SUSTAINED_MOVE"
    if above_pct >= 80.0:
        return "SUSTAINED_ABOVE"
    return "MIXED"


def compute_legacy_feature_row(
    signal_record: dict[str, Any],
    price_frame: pd.DataFrame,
) -> SignalFeatures | None:
    signal_ts = ml_parse_utc_ts(signal_record.get("ts"))
    if signal_ts is None:
        return None

    beat_price = _safe_float(signal_record.get("beat_price"), 0.0)
    btc_price = _safe_float(signal_record.get("btc_price"), 0.0)
    if beat_price <= 0.0 or btc_price <= 0.0:
        return None

    elapsed_s = _safe_int(signal_record.get("elapsed_s"), 0)
    seconds_remaining = max(0, 300 - elapsed_s)
    window_end_at = signal_ts + timedelta(seconds=seconds_remaining)
    window_start_at = window_end_at - timedelta(seconds=300)

    history = price_frame.loc[
        (price_frame.index >= signal_ts - timedelta(seconds=180))
        & (price_frame.index <= signal_ts)
    ].copy()
    if history.empty:
        return None

    prices = history["btc"].astype(float).tolist()
    cvd_series = history["cvd"].astype(float).tolist() if "cvd" in history else []
    odds_history = [
        (idx.timestamp(), _safe_float(row.get("up_odds"), 0.5), _safe_float(row.get("dn_odds"), 0.5))
        for idx, row in history.tail(12).iterrows()
    ]

    gap_signed_pct = ((btc_price - beat_price) / beat_price * 100.0) if beat_price > 0 else 0.0
    gap_pct = abs(gap_signed_pct)
    signal_alignment = _safe_int(signal_record.get("alignment"), 0)
    direction_bias = "UP" if gap_signed_pct > 0 else ("DOWN" if gap_signed_pct < 0 else "NONE")
    signed_alignment = float(signal_alignment if direction_bias == "UP" else -signal_alignment if direction_bias == "DOWN" else 0.0)
    odds_vel, odds_vel_accel = ml_compute_odds_velocity(odds_history)

    rsi = ml_compute_rsi(prices)
    momentum = ml_compute_momentum(prices)
    macd_histogram = compute_macd_histogram(prices)
    bb_pct_b = compute_bb_pct_b(prices)

    price_roc_15s = 0.0
    price_roc_30s = 0.0
    if len(prices) >= 4 and prices[-4] != 0:
        price_roc_15s = (prices[-1] - prices[-4]) / prices[-4] * 100.0
    if len(prices) >= 7 and prices[-7] != 0:
        price_roc_30s = (prices[-1] - prices[-7]) / prices[-7] * 100.0

    cvd_change_30s = 0.0
    if len(cvd_series) >= 7:
        cvd_change_30s = cvd_series[-1] - cvd_series[-7]

    fair_up, fair_down = ml_compute_fair_probability(btc_price, beat_price, seconds_remaining, prices)
    up_odds = _safe_float(signal_record.get("up_odds"), 0.5)
    down_odds = _safe_float(signal_record.get("down_odds"), 0.5)
    edge_up = ml_compute_edge(fair_up, up_odds)
    edge_down = ml_compute_edge(fair_down, down_odds)
    odds_edge_strength = up_odds - down_odds
    dip_label = ml_compute_dip_label(prices, beat_price, btc_price)
    realized_vol_30s = float(np.std(np.diff(np.array(prices[-7:], dtype=float)) / np.array(prices[-7:-1], dtype=float))) / math.sqrt(5.0) if len(prices) >= 7 and all(p != 0 for p in prices[-7:-1]) else 0.0
    realized_vol_60s = float(np.std(np.diff(np.array(prices[-13:], dtype=float)) / np.array(prices[-13:-1], dtype=float))) / math.sqrt(5.0) if len(prices) >= 13 and all(p != 0 for p in prices[-13:-1]) else 0.0

    return SignalFeatures(
        row_id=_build_row_id(str(signal_record.get("condition_id", "")), str(signal_record.get("ts", "")), prefix="legacy"),
        ts=_iso_z(signal_ts),
        condition_id=str(signal_record.get("condition_id", "")),
        window_start_at=_iso_z(window_start_at),
        window_end_at=_iso_z(window_end_at),
        beat_price=beat_price,
        btc_price=btc_price,
        up_odds=up_odds,
        down_odds=down_odds,
        gap_pct=gap_pct,
        gap_signed_pct=gap_signed_pct,
        seconds_remaining=seconds_remaining,
        signal_alignment=signal_alignment,
        signed_alignment=signed_alignment,
        odds_vel=odds_vel,
        odds_vel_accel=odds_vel_accel,
        cvd_divergence=encode_cvd_divergence(signal_record.get("cvd_divergence")),
        macd_histogram=_safe_float(macd_histogram, 0.0),
        bb_pct_b=_safe_float(bb_pct_b, 0.5),
        rsi=_safe_float(rsi, 50.0),
        momentum_pct=_safe_float(momentum, 0.0),
        is_late_window=1 if seconds_remaining < 60 else 0,
        is_bandar_zone=1 if seconds_remaining < 45 else 0,
        is_proximity_risk=1 if seconds_remaining < 60 and gap_pct < 0.08 else 0,
        is_proximity_risk_above=1 if seconds_remaining < 60 and gap_pct < 0.08 and gap_signed_pct >= 0 else 0,
        is_proximity_risk_below=1 if seconds_remaining < 60 and gap_pct < 0.08 and gap_signed_pct < 0 else 0,
        price_roc_15s=price_roc_15s,
        price_roc_30s=price_roc_30s,
        cvd_change_last_30s=cvd_change_30s,
        odds_edge_strength=odds_edge_strength,
        elapsed_fraction=max(0.0, min(1.0, elapsed_s / 300.0)),
        gap_alignment_interaction=gap_signed_pct * signal_alignment,
        realized_vol_30s=realized_vol_30s,
        realized_vol_60s=realized_vol_60s,
        gap_signed_pct_lag1=0.0,
        signal_alignment_lag1=0.0,
        odds_edge_strength_lag1=0.0,
        ob_imbalance=0.0,
        fair_up=fair_up,
        fair_down=fair_down,
        edge_up=edge_up,
        edge_down=edge_down,
        direction_bias=direction_bias,
        dip_label=dip_label,
        feature_source="legacy_bootstrap",
    )


def load_price_frame(log_dir: str | Path) -> pd.DataFrame:
    records: list[dict[str, Any]] = []
    for path in sorted(Path(log_dir).glob("prices_*.jsonl")):
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                try:
                    record = json.loads(line)
                except Exception:
                    continue
                ts = ml_parse_utc_ts(record.get("ts"))
                if ts is None:
                    continue
                records.append(
                    {
                        "ts": ts,
                        "btc": _safe_float(record.get("btc"), 0.0),
                        "buy_vol": _safe_float(record.get("buy_vol"), 0.0),
                        "sell_vol": _safe_float(record.get("sell_vol"), 0.0),
                        "cvd": _safe_float(record.get("cvd"), 0.0),
                        "up_odds": _safe_float(record.get("up_odds"), 0.5),
                        "dn_odds": _safe_float(record.get("dn_odds"), 0.5),
                    }
                )
    if not records:
        return pd.DataFrame(columns=["btc", "buy_vol", "sell_vol", "cvd", "up_odds", "dn_odds"])
    frame = pd.DataFrame(records).sort_values("ts")
    frame = frame.drop_duplicates(subset=["ts"], keep="last")
    frame = frame.set_index("ts")
    return frame


def load_settlement_registry(log_dir: str | Path) -> dict[str, dict[str, Any]]:
    registry: dict[str, dict[str, Any]] = {}
    for path in sorted(Path(log_dir).glob(SETTLEMENT_GLOB)):
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                try:
                    record = json.loads(line)
                except Exception:
                    continue
                condition_id = str(record.get("condition_id", "")).strip()
                if not condition_id:
                    continue
                registry[condition_id] = _best_record_by_priority(
                    registry.get(condition_id),
                    record,
                    source_key="settlement_source",
                    ts_key="resolved_at",
                ) or record
    return registry


def _find_closest_price_resolution(
    price_frame: pd.DataFrame,
    window_end_at: datetime,
    *,
    max_diff_s: float,
) -> tuple[datetime, float, float] | None:
    if price_frame.empty:
        return None
    lo = window_end_at - timedelta(seconds=max_diff_s)
    hi = window_end_at + timedelta(seconds=max_diff_s)
    candidates = price_frame.loc[(price_frame.index >= lo) & (price_frame.index <= hi)]
    if candidates.empty:
        return None

    ts_values = candidates.index.to_series()
    deltas = (ts_values - window_end_at).abs()
    closest_ts = deltas.idxmin()
    resolved_btc = _safe_float(candidates.loc[closest_ts]["btc"], 0.0)
    if resolved_btc <= 0.0:
        return None
    diff_s = float(abs((closest_ts.to_pydatetime() - window_end_at).total_seconds()))
    return closest_ts.to_pydatetime(), resolved_btc, diff_s


def resolve_label_for_row(
    row: dict[str, Any],
    price_frame: pd.DataFrame,
    max_diff_s: float = 90.0,
    *,
    override_price: float | None = None,
    label_source: str | None = None,
    override_resolution_ts: str | datetime | None = None,
    settlement_source_priority: int | None = None,
) -> ResolvedLabelRecord | None:
    window_end_at = ml_parse_utc_ts(row.get("window_end_at"))
    beat_price = _safe_float(row.get("beat_price"), 0.0)
    if window_end_at is None or beat_price <= 0.0:
        return None

    resolved_btc = 0.0
    resolution_ts = window_end_at
    source = str(label_source or "").strip()
    chainlink_settlement_price: float | None = None
    binance_resolution_diff_s: float | None = None
    source_priority = int(settlement_source_priority or _label_source_priority(source))

    if override_price is not None and override_price > 0.0:
        resolved_btc = float(override_price)
        resolution_ts = ml_parse_utc_ts(override_resolution_ts) or window_end_at
        if "chainlink" in source or "market_settlement" in source:
            chainlink_settlement_price = resolved_btc
    else:
        resolution = _find_closest_price_resolution(price_frame, window_end_at, max_diff_s=min(15.0, max_diff_s))
        source = "binance_15s"
        if resolution is None and max_diff_s > 15.0:
            resolution = _find_closest_price_resolution(price_frame, window_end_at, max_diff_s=max_diff_s)
            source = "binance_90s"
        if resolution is None:
            return None
        resolution_ts, resolved_btc, binance_resolution_diff_s = resolution
        source_priority = _label_source_priority(source)

    if resolved_btc <= 0.0 or math.isclose(resolved_btc, beat_price, rel_tol=0.0, abs_tol=1e-9):
        return None

    label = LABEL_BUY_UP if resolved_btc > beat_price else LABEL_BUY_DOWN
    return ResolvedLabelRecord(
        row_id=str(row.get("row_id", "")),
        condition_id=str(row.get("condition_id", "")),
        resolution_ts=_iso_z(resolution_ts),
        resolved_label=label,
        resolved_btc_price=resolved_btc,
        label_source=source or "window_resolution",
        chainlink_settlement_price=chainlink_settlement_price,
        binance_resolution_diff_s=binance_resolution_diff_s,
        settlement_source_priority=source_priority,
    )


def backfill_ml_labels(log_dir: str | Path) -> int:
    log_dir = Path(log_dir)
    price_frame = load_price_frame(log_dir)
    settlement_registry = load_settlement_registry(log_dir)
    labeled_records: dict[str, dict[str, Any]] = {}
    for path in sorted(log_dir.glob(ML_LABEL_GLOB)):
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                try:
                    record = json.loads(line)
                except Exception:
                    continue
                row_id = str(record.get("row_id", ""))
                if row_id:
                    labeled_records[row_id] = _best_record_by_priority(
                        labeled_records.get(row_id),
                        record,
                        source_key="label_source",
                        ts_key="resolution_ts",
                    ) or record

    appended = 0
    for path in sorted(log_dir.glob(ML_FEATURE_GLOB)):
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                try:
                    record = json.loads(line)
                except Exception:
                    continue
                row_id = str(record.get("row_id", ""))
                if not row_id:
                    continue
                settlement = settlement_registry.get(str(record.get("condition_id", "")).strip())
                label = resolve_label_for_row(
                    record,
                    price_frame,
                    override_price=_safe_float(settlement.get("settlement_price"), 0.0) if settlement else None,
                    label_source=str(settlement.get("settlement_source", "")) if settlement else None,
                    override_resolution_ts=settlement.get("resolved_at") if settlement else None,
                    settlement_source_priority=int(settlement.get("settlement_source_priority", 0)) if settlement else None,
                )
                if label is None:
                    continue
                existing = labeled_records.get(row_id)
                if existing is not None:
                    existing_priority = int(existing.get("settlement_source_priority") or _label_source_priority(existing.get("label_source")))
                    if existing_priority >= label.settlement_source_priority:
                        continue
                label_path = log_dir / f"ml_labels_{label.resolution_ts[:10]}.jsonl"
                _append_jsonl(label_path, label.to_record())
                labeled_records[label.row_id] = label.to_record()
                appended += 1
    return appended


def _load_runtime_dataset(log_dir: str | Path) -> pd.DataFrame:
    log_dir = Path(log_dir)
    feature_records: list[dict[str, Any]] = []
    for path in sorted(log_dir.glob(ML_FEATURE_GLOB)):
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                try:
                    feature_records.append(json.loads(line))
                except Exception:
                    continue
    if not feature_records:
        return pd.DataFrame()

    feature_frame = pd.DataFrame(feature_records)
    if feature_frame.empty:
        return feature_frame

    label_records: dict[str, dict[str, Any]] = {}
    for path in sorted(log_dir.glob(ML_LABEL_GLOB)):
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                try:
                    label = json.loads(line)
                except Exception:
                    continue
                row_id = str(label.get("row_id", ""))
                if row_id:
                    label_records[row_id] = _best_record_by_priority(
                        label_records.get(row_id),
                        label,
                        source_key="label_source",
                        ts_key="resolution_ts",
                    ) or label

    price_frame = load_price_frame(log_dir)
    settlement_registry = load_settlement_registry(log_dir)
    joined: list[dict[str, Any]] = []
    for record in feature_records:
        row_id = str(record.get("row_id", ""))
        label = label_records.get(row_id)
        if label is None:
            settlement = settlement_registry.get(str(record.get("condition_id", "")).strip())
            derived = resolve_label_for_row(
                record,
                price_frame,
                override_price=_safe_float(settlement.get("settlement_price"), 0.0) if settlement else None,
                label_source=str(settlement.get("settlement_source", "")) if settlement else None,
                override_resolution_ts=settlement.get("resolved_at") if settlement else None,
                settlement_source_priority=int(settlement.get("settlement_source_priority", 0)) if settlement else None,
            )
            label = derived.to_record() if derived else None
        if label is None:
            continue
        merged = dict(record)
        merged.update(
            {
                "resolved_label": label["resolved_label"],
                "resolved_btc_price": label["resolved_btc_price"],
                "resolution_ts": label["resolution_ts"],
                "label_source": label.get("label_source", ""),
                "chainlink_settlement_price": label.get("chainlink_settlement_price"),
                "binance_resolution_diff_s": label.get("binance_resolution_diff_s"),
                "settlement_source_priority": label.get("settlement_source_priority", 0),
            }
        )
        joined.append(merged)
    return pd.DataFrame(joined)


def _load_legacy_bootstrap_dataset(log_dir: str | Path) -> pd.DataFrame:
    price_frame = load_price_frame(log_dir)
    settlement_registry = load_settlement_registry(log_dir)
    records: list[dict[str, Any]] = []
    for path in sorted(Path(log_dir).glob("signals_*.jsonl")):
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                try:
                    signal_record = json.loads(line)
                except Exception:
                    continue
                feature_row = compute_legacy_feature_row(signal_record, price_frame)
                if feature_row is None:
                    continue
                settlement = settlement_registry.get(feature_row.condition_id)
                label = resolve_label_for_row(
                    feature_row.to_record(),
                    price_frame,
                    override_price=_safe_float(settlement.get("settlement_price"), 0.0) if settlement else None,
                    label_source=str(settlement.get("settlement_source", "")) if settlement else None,
                    override_resolution_ts=settlement.get("resolved_at") if settlement else None,
                    settlement_source_priority=int(settlement.get("settlement_source_priority", 0)) if settlement else None,
                )
                if label is None:
                    continue
                merged = feature_row.to_record()
                merged.update(
                    {
                        "resolved_label": label.resolved_label,
                        "resolved_btc_price": label.resolved_btc_price,
                        "resolution_ts": label.resolution_ts,
                        "label_source": label.label_source,
                        "chainlink_settlement_price": label.chainlink_settlement_price,
                        "binance_resolution_diff_s": label.binance_resolution_diff_s,
                        "settlement_source_priority": label.settlement_source_priority,
                    }
                )
                records.append(merged)
    return pd.DataFrame(records)


def load_training_dataset(log_dir: str | Path) -> pd.DataFrame:
    runtime_frame = _load_runtime_dataset(log_dir)
    if not runtime_frame.empty:
        return runtime_frame
    return _load_legacy_bootstrap_dataset(log_dir)


def _rolling_return_volatility(values: pd.Series, lookback_returns: int) -> pd.Series:
    returns = values.pct_change()
    return returns.rolling(lookback_returns, min_periods=2).std().fillna(0.0) / math.sqrt(5.0)


def _prepare_training_frame(dataset: pd.DataFrame) -> pd.DataFrame:
    if dataset.empty:
        return dataset
    frame = dataset.copy()
    frame["ts"] = pd.to_datetime(frame["ts"], utc=True)
    if "window_end_at" in frame.columns:
        frame["window_end_at"] = pd.to_datetime(frame["window_end_at"], utc=True, errors="coerce")
    frame = frame.sort_values("ts").reset_index(drop=True)
    frame = frame[frame["resolved_label"].isin([LABEL_BUY_UP, LABEL_BUY_DOWN])].copy()
    for column, default in NUMERIC_DEFAULTS.items():
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(default)
    frame["elapsed_fraction"] = (
        pd.to_numeric(frame.get("elapsed_fraction", pd.Series(index=frame.index)), errors="coerce")
        .fillna((300.0 - pd.to_numeric(frame["seconds_remaining"], errors="coerce").fillna(0.0)) / 300.0)
        .clip(lower=0.0, upper=1.0)
    )
    frame["gap_alignment_interaction"] = pd.to_numeric(
        frame.get("gap_alignment_interaction", frame["gap_signed_pct"] * frame["signal_alignment"]),
        errors="coerce",
    ).fillna(frame["gap_signed_pct"] * frame["signal_alignment"])
    frame["ob_imbalance"] = pd.to_numeric(
        frame.get("ob_imbalance", pd.Series(0.0, index=frame.index)),
        errors="coerce",
    ).fillna(0.0)

    if "condition_id" in frame.columns:
        grouped = frame.groupby("condition_id", sort=False)
        frame["gap_signed_pct_lag1"] = pd.to_numeric(
            frame.get("gap_signed_pct_lag1", pd.Series(np.nan, index=frame.index)),
            errors="coerce",
        )
        frame["signal_alignment_lag1"] = pd.to_numeric(
            frame.get("signal_alignment_lag1", pd.Series(np.nan, index=frame.index)),
            errors="coerce",
        )
        frame["odds_edge_strength_lag1"] = pd.to_numeric(
            frame.get("odds_edge_strength_lag1", pd.Series(np.nan, index=frame.index)),
            errors="coerce",
        )
        frame["gap_signed_pct_lag1"] = frame["gap_signed_pct_lag1"].fillna(grouped["gap_signed_pct"].shift(1)).fillna(0.0)
        frame["signal_alignment_lag1"] = frame["signal_alignment_lag1"].fillna(grouped["signal_alignment"].shift(1)).fillna(0.0)
        frame["odds_edge_strength_lag1"] = frame["odds_edge_strength_lag1"].fillna(grouped["odds_edge_strength"].shift(1)).fillna(0.0)
        frame["realized_vol_30s"] = pd.to_numeric(
            frame.get("realized_vol_30s", pd.Series(np.nan, index=frame.index)),
            errors="coerce",
        )
        frame["realized_vol_60s"] = pd.to_numeric(
            frame.get("realized_vol_60s", pd.Series(np.nan, index=frame.index)),
            errors="coerce",
        )
        computed_vol_30s = grouped["btc_price"].transform(lambda values: _rolling_return_volatility(values.astype(float), 6))
        computed_vol_60s = grouped["btc_price"].transform(lambda values: _rolling_return_volatility(values.astype(float), 12))
        frame["realized_vol_30s"] = frame["realized_vol_30s"].fillna(computed_vol_30s).fillna(0.0)
        frame["realized_vol_60s"] = frame["realized_vol_60s"].fillna(computed_vol_60s).fillna(0.0)

    for column in MODEL_FEATURE_COLUMNS:
        if column not in frame.columns:
            # New feature not yet present in historical logs — backfill with default.
            frame[column] = NUMERIC_DEFAULTS.get(column, 0.0)
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(NUMERIC_DEFAULTS.get(column, 0.0))
    return frame


def _fit_calibrator(probabilities: np.ndarray, labels: np.ndarray) -> Any:
    unique = np.unique(labels)
    if len(unique) < 2 or len(labels) < 25:
        return IdentityCalibrator()
    calibrator = IsotonicRegression(out_of_bounds="clip")
    calibrator.fit(probabilities, labels)
    return calibrator


def _signal_features_from_row(row: Any) -> SignalFeatures:
    return SignalFeatures(
        row_id=str(row.row_id),
        ts=_iso_z(ml_parse_utc_ts(row.ts) or _utc_now()),
        condition_id=str(row.condition_id),
        window_start_at=str(row.window_start_at),
        window_end_at=str(row.window_end_at),
        beat_price=_safe_float(row.beat_price),
        btc_price=_safe_float(row.btc_price),
        up_odds=_safe_float(row.up_odds, 0.5),
        down_odds=_safe_float(row.down_odds, 0.5),
        gap_pct=_safe_float(row.gap_pct, 0.0),
        gap_signed_pct=_safe_float(row.gap_signed_pct, 0.0),
        seconds_remaining=_safe_int(row.seconds_remaining, 0),
        signal_alignment=_safe_int(row.signal_alignment, 0),
        signed_alignment=_safe_float(row.signed_alignment, 0.0),
        odds_vel=_safe_float(row.odds_vel, 0.0),
        odds_vel_accel=_safe_float(row.odds_vel_accel, 0.0),
        cvd_divergence=encode_cvd_divergence(row.cvd_divergence),
        macd_histogram=_safe_float(row.macd_histogram, 0.0),
        bb_pct_b=_safe_float(row.bb_pct_b, 0.5),
        rsi=_safe_float(row.rsi, 50.0),
        momentum_pct=_safe_float(row.momentum_pct, 0.0),
        is_late_window=_safe_int(row.is_late_window, 0),
        is_bandar_zone=_safe_int(row.is_bandar_zone, 0),
        is_proximity_risk=_safe_int(row.is_proximity_risk, 0),
        is_proximity_risk_above=_safe_int(getattr(row, "is_proximity_risk_above", 0), 0),
        is_proximity_risk_below=_safe_int(getattr(row, "is_proximity_risk_below", 0), 0),
        price_roc_15s=_safe_float(row.price_roc_15s, 0.0),
        price_roc_30s=_safe_float(row.price_roc_30s, 0.0),
        cvd_change_last_30s=_safe_float(row.cvd_change_last_30s, 0.0),
        odds_edge_strength=_safe_float(row.odds_edge_strength, 0.0),
        elapsed_fraction=_safe_float(getattr(row, "elapsed_fraction", 0.0), 0.0),
        gap_alignment_interaction=_safe_float(getattr(row, "gap_alignment_interaction", 0.0), 0.0),
        realized_vol_30s=_safe_float(getattr(row, "realized_vol_30s", 0.0), 0.0),
        realized_vol_60s=_safe_float(getattr(row, "realized_vol_60s", 0.0), 0.0),
        gap_signed_pct_lag1=_safe_float(getattr(row, "gap_signed_pct_lag1", 0.0), 0.0),
        signal_alignment_lag1=_safe_float(getattr(row, "signal_alignment_lag1", 0.0), 0.0),
        odds_edge_strength_lag1=_safe_float(getattr(row, "odds_edge_strength_lag1", 0.0), 0.0),
        gap_crossed_zero=_safe_int(getattr(row, "gap_crossed_zero", 0), 0),
        ob_imbalance=_safe_float(getattr(row, "ob_imbalance", 0.0), 0.0),
        fair_up=_safe_float(row.fair_up, 0.5),
        fair_down=_safe_float(row.fair_down, 0.5),
        edge_up=_safe_float(row.edge_up, 0.0),
        edge_down=_safe_float(row.edge_down, 0.0),
        direction_bias=str(getattr(row, "direction_bias", "NONE")),
        dip_label=str(getattr(row, "dip_label", "UNKNOWN")),
        feature_source=str(getattr(row, "feature_source", "dataset")),
    )


def _compute_scale_pos_weight(labels: np.ndarray) -> float:
    positives = int(np.sum(labels == 1))
    negatives = int(np.sum(labels == 0))
    total = positives + negatives
    if positives == 0 or negatives == 0 or total == 0:
        return 1.0
    pos_ratio = positives / total
    if 0.40 <= pos_ratio <= 0.60:
        return 1.0
    return float(negatives / positives)


def _build_xgb_params(labels: np.ndarray) -> dict[str, Any]:
    params = {
        "n_estimators": 320,
        "max_depth": 7,
        "learning_rate": 0.10,
        "subsample": 0.85,
        "colsample_bytree": 0.8,
        "random_state": 42,
        "eval_metric": "logloss",
        "objective": "binary:logistic",
        "n_jobs": 1,
    }
    scale_pos_weight = _compute_scale_pos_weight(labels)
    if abs(scale_pos_weight - 1.0) >= 1e-9:
        params["scale_pos_weight"] = scale_pos_weight
    return params


def _window_split_indices(
    frame: pd.DataFrame,
    *,
    n_splits: int = 5,
    purge_windows: int = 1,
) -> list[tuple[np.ndarray, np.ndarray]]:
    if frame.empty or "condition_id" not in frame.columns:
        return []
    windows = (
        frame.groupby("condition_id", as_index=False)
        .agg(window_end_at=("window_end_at", "max"), first_ts=("ts", "min"))
        .sort_values(["window_end_at", "first_ts", "condition_id"])
        .reset_index(drop=True)
    )
    window_ids = windows["condition_id"].tolist()
    if len(window_ids) < 2:
        return []

    splits: list[tuple[np.ndarray, np.ndarray]] = []
    max_splits = min(n_splits, len(window_ids) - 1)
    if max_splits >= 2:
        splitter = TimeSeriesSplit(n_splits=max_splits, gap=min(purge_windows, max(0, len(window_ids) - 2)))
        for train_window_idx, valid_window_idx in splitter.split(np.arange(len(window_ids))):
            train_ids = set(windows.iloc[train_window_idx]["condition_id"].tolist())
            valid_ids = set(windows.iloc[valid_window_idx]["condition_id"].tolist())
            train_idx = frame.index[frame["condition_id"].isin(train_ids)].to_numpy()
            valid_idx = frame.index[frame["condition_id"].isin(valid_ids)].to_numpy()
            if len(train_idx) and len(valid_idx):
                splits.append((train_idx, valid_idx))
    if splits:
        return splits

    split_idx = max(1, int(len(window_ids) * 0.8))
    if split_idx >= len(window_ids):
        split_idx = len(window_ids) - 1
    train_ids = set(window_ids[:split_idx])
    valid_ids = set(window_ids[split_idx:])
    train_idx = frame.index[frame["condition_id"].isin(train_ids)].to_numpy()
    valid_idx = frame.index[frame["condition_id"].isin(valid_ids)].to_numpy()
    if len(train_idx) and len(valid_idx):
        return [(train_idx, valid_idx)]
    return []


def _policy_metrics(
    frame: pd.DataFrame,
    probabilities: np.ndarray,
    policy: RuntimePolicy,
    *,
    threshold_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    predictions: list[str] = []
    realized_returns: list[float] = []
    for row, prob_up in zip(frame.itertuples(index=False), probabilities):
        features = _signal_features_from_row(row)
        decision = policy.decide(
            features,
            float(prob_up),
            float(1.0 - prob_up),
            reason_prefix="eval",
            source="eval",
            model_version="eval",
            promotion_state="eval",
            threshold_profile=threshold_profile,
        )
        predictions.append(decision.signal)
        if decision.signal == LABEL_SKIP:
            continue
        market_odds = features.up_odds if decision.signal == LABEL_BUY_UP else features.down_odds
        if market_odds <= 0.0 or market_odds >= 1.0:
            continue
        won = str(row.resolved_label) == decision.signal
        realized_returns.append((1.0 / market_odds - 1.0) if won else -1.0)

    traded = [signal for signal in predictions if signal != LABEL_SKIP]
    return {
        "trade_rate": len(traded) / len(predictions) if predictions else 0.0,
        "realized_ev_per_trade": float(np.mean(realized_returns)) if realized_returns else 0.0,
    }


def train_outcome_model(
    *,
    log_dir: str | Path = "logs",
    models_dir: str | Path = DEFAULT_MODELS_DIR,
    promotion_state: str = "shadow",
    min_rows: int = ML_MIN_TRAIN_ROWS,
    min_distinct_windows: int = ML_MIN_TRAIN_WINDOWS,
) -> dict[str, Any]:
    dataset = _prepare_training_frame(load_training_dataset(log_dir))
    if dataset.empty:
        raise ValueError("no training rows available")
    if len(dataset) < min_rows:
        raise ValueError(f"need at least {min_rows} rows, found {len(dataset)}")
    distinct_windows_total = int(dataset["condition_id"].nunique()) if "condition_id" in dataset.columns else 0
    if distinct_windows_total < min_distinct_windows:
        raise ValueError(
            f"need at least {min_distinct_windows} distinct windows, found {distinct_windows_total}"
        )

    splits = _window_split_indices(dataset, n_splits=5, purge_windows=1)
    if not splits:
        raise ValueError("not enough distinct windows for grouped validation")

    y_all = (dataset["resolved_label"] == LABEL_BUY_UP).astype(int).to_numpy()
    if len(np.unique(y_all)) < 2:
        raise ValueError("training dataset must contain both BUY_UP and BUY_DOWN labels")

    oof_raw = np.full(len(dataset), np.nan, dtype=float)
    fold_ap_scores: list[float] = []
    fold_brier_scores: list[float] = []

    for train_idx, valid_idx in splits:
        train_frame = dataset.iloc[train_idx].copy()
        valid_frame = dataset.iloc[valid_idx].copy()
        y_train = (train_frame["resolved_label"] == LABEL_BUY_UP).astype(int).to_numpy()
        y_valid = (valid_frame["resolved_label"] == LABEL_BUY_UP).astype(int).to_numpy()
        if len(np.unique(y_train)) < 2 or len(np.unique(y_valid)) < 2:
            continue

        model = XGBClassifier(**_build_xgb_params(y_train))
        model.fit(train_frame[MODEL_FEATURE_COLUMNS], y_train)
        raw_valid = model.predict_proba(valid_frame[MODEL_FEATURE_COLUMNS])[:, 1]
        oof_raw[valid_idx] = raw_valid
        fold_ap_scores.append(float(average_precision_score(y_valid, raw_valid)))
        fold_brier_scores.append(float(brier_score_loss(y_valid, np.clip(raw_valid, 0.0, 1.0))))

    valid_mask = ~np.isnan(oof_raw)
    if not np.any(valid_mask):
        raise ValueError("grouped validation produced no scored rows")

    scored_frame = dataset.loc[valid_mask].copy()
    y_scored = y_all[valid_mask]
    raw_scored = oof_raw[valid_mask]
    calibrator = _fit_calibrator(raw_scored, y_scored)
    calibrated_scored = np.asarray(calibrator.predict(raw_scored), dtype=float)
    calibrated_scored = np.clip(calibrated_scored, 0.0, 1.0)

    pred_scored = (calibrated_scored >= 0.5).astype(int)
    accuracy = float(accuracy_score(y_scored, pred_scored))
    precision_up, recall_up, _, _ = precision_recall_fscore_support(y_scored, pred_scored, average="binary", zero_division=0)
    precision_down, recall_down, _, _ = precision_recall_fscore_support(1 - y_scored, 1 - pred_scored, average="binary", zero_division=0)
    matrix = confusion_matrix(y_scored, pred_scored).tolist()

    params = _build_xgb_params(y_all)
    model = XGBClassifier(**params)
    model.fit(dataset[MODEL_FEATURE_COLUMNS], y_all)

    threshold_bundle = tune_runtime_thresholds_from_shadow_data(log_dir)
    runtime_thresholds = _normalize_runtime_thresholds(threshold_bundle.get("runtime_thresholds"))
    policy = RuntimePolicy()
    policy_stats = _policy_metrics(scored_frame, calibrated_scored, policy, threshold_profile=runtime_thresholds)
    fallback_engine = RuntimeSignalEngine(ModelRegistry(models_dir), policy=policy)
    fallback_probs = np.asarray(
        [
            fallback_engine._heuristic_probability(_signal_features_from_row(row))  # noqa: SLF001
            for row in scored_frame.itertuples(index=False)
        ],
        dtype=float,
    )
    fallback_policy_stats = _policy_metrics(scored_frame, fallback_probs, policy, threshold_profile=runtime_thresholds)

    feature_importance = {
        name: float(weight)
        for name, weight in zip(MODEL_FEATURE_COLUMNS, model.feature_importances_)
    }

    cv_auc_pr_mean = float(np.mean(fold_ap_scores)) if fold_ap_scores else 0.0
    cv_auc_pr_std = float(np.std(fold_ap_scores)) if fold_ap_scores else 0.0
    cv_brier_mean = float(np.mean(fold_brier_scores)) if fold_brier_scores else 1.0
    auc_pr = float(average_precision_score(y_scored, calibrated_scored))
    brier = float(brier_score_loss(y_scored, calibrated_scored))
    prevalence = float(np.mean(y_scored)) if len(y_scored) else 0.0

    registry = ModelRegistry(models_dir)
    previous_manifest = registry.load_manifest()
    previous_cv_ap = _safe_float(previous_manifest.metrics.get("cv_auc_pr_mean"), 0.0) if previous_manifest else 0.0
    previous_brier = _safe_float(previous_manifest.metrics.get("cv_brier_mean"), 0.0) if previous_manifest else 0.0

    promotion_blocks: list[str] = []
    if len(dataset) < ML_MIN_PROMOTE_ROWS:
        promotion_blocks.append(f"rows_total {len(dataset)} < {ML_MIN_PROMOTE_ROWS}")
    if distinct_windows_total < ML_MIN_PROMOTE_WINDOWS:
        promotion_blocks.append(f"distinct_windows_total {distinct_windows_total} < {ML_MIN_PROMOTE_WINDOWS}")
    if cv_auc_pr_mean < prevalence + ML_PROMOTION_AP_MARGIN:
        promotion_blocks.append(
            f"cv_auc_pr_mean {cv_auc_pr_mean:.3f} < prevalence+margin {(prevalence + ML_PROMOTION_AP_MARGIN):.3f}"
        )
    if cv_brier_mean >= ML_PROMOTION_MAX_BRIER:
        promotion_blocks.append(f"cv_brier_mean {cv_brier_mean:.3f} >= {ML_PROMOTION_MAX_BRIER:.3f}")
    if previous_brier > 0.0 and cv_brier_mean > previous_brier + ML_PROMOTION_MAX_BRIER_DEGRADE:
        promotion_blocks.append(
            f"cv_brier_mean degraded {cv_brier_mean:.3f} > {previous_brier + ML_PROMOTION_MAX_BRIER_DEGRADE:.3f}"
        )
    if policy_stats["realized_ev_per_trade"] <= fallback_policy_stats["realized_ev_per_trade"]:
        promotion_blocks.append("policy EV does not beat fallback EV")
    if cv_auc_pr_std > ML_PROMOTION_BLOCK_AP_STD:
        promotion_blocks.append(f"cv_auc_pr_std {cv_auc_pr_std:.3f} > {ML_PROMOTION_BLOCK_AP_STD:.3f}")
    if previous_cv_ap > 0.0 and cv_auc_pr_mean < previous_cv_ap - ML_PROMOTION_BLOCK_AP_DROP:
        promotion_blocks.append(
            f"cv_auc_pr_mean dropped below active baseline by more than {ML_PROMOTION_BLOCK_AP_DROP:.2f}"
        )
    ready_for_active = not promotion_blocks

    metrics = {
        "rows_total": int(len(dataset)),
        "rows_train": int(len(dataset)),
        "rows_valid": int(np.sum(valid_mask)),
        "distinct_windows_total": distinct_windows_total,
        "class_balance": {
            LABEL_BUY_UP: int((dataset["resolved_label"] == LABEL_BUY_UP).sum()),
            LABEL_BUY_DOWN: int((dataset["resolved_label"] == LABEL_BUY_DOWN).sum()),
        },
        "auc_pr": auc_pr,
        "cv_auc_pr_mean": cv_auc_pr_mean,
        "cv_auc_pr_std": cv_auc_pr_std,
        "cv_average_precision_mean": cv_auc_pr_mean,
        "brier": brier,
        "cv_brier_mean": cv_brier_mean,
        "positive_prevalence": prevalence,
        "accuracy": accuracy,
        "precision_up": float(precision_up),
        "recall_up": float(recall_up),
        "precision_down": float(precision_down),
        "recall_down": float(recall_down),
        "scale_pos_weight": float(params.get("scale_pos_weight", 1.0)),
        "policy_metrics": policy_stats,
        "fallback_policy_metrics": fallback_policy_stats,
        "runtime_thresholds": runtime_thresholds,
        "threshold_mode": threshold_bundle.get("threshold_mode", ML_THRESHOLD_MODE),
        "threshold_tuning_summary": threshold_bundle.get("threshold_tuning_summary", {}),
        "coverage_target": ML_TARGET_EXEC_COVERAGE,
        "min_win_rate_target": ML_MIN_EXEC_WIN_RATE,
        "beats_fallback": policy_stats["realized_ev_per_trade"] > fallback_policy_stats["realized_ev_per_trade"],
        "ready_for_active": ready_for_active,
        "promotion_block_reason": "; ".join(promotion_blocks),
        "confusion_matrix": matrix,
        "feature_importance": feature_importance,
        "best_params": params,
        "search_trials_completed": 0,
        "training_range": {
            "start": _iso_z(dataset["ts"].min().to_pydatetime()),
            "end": _iso_z(dataset["ts"].max().to_pydatetime()),
        },
        "experimental_3class_status": "deferred_until_action_labels_exist",
    }

    manifest = registry.save_bundle(
        model=model,
        calibrator=calibrator,
        metrics=metrics,
        promotion_state=promotion_state,
    )

    return {
        "manifest": manifest.to_record(),
        "metrics": metrics,
    }


def auto_apply_trained_model(
    result: dict[str, Any],
    registry: ModelRegistry,
    *,
    auto_promote: bool = ML_AUTO_PROMOTE,
    fallback_state: str = "shadow",
    activation_reason: str = "auto_train",
) -> dict[str, Any]:
    manifest = result.get("manifest", {}) if isinstance(result, dict) else {}
    version = str(manifest.get("model_version", "")).strip()
    if not version:
        return result

    target_state = str(manifest.get("promotion_state", fallback_state) or fallback_state)
    if target_state not in PROMOTION_STATES:
        target_state = fallback_state if fallback_state in PROMOTION_STATES else "shadow"

    metrics = result.get("metrics", {}) if isinstance(result, dict) else {}
    if auto_promote:
        target_state = "active" if bool(metrics.get("ready_for_active")) else "shadow"

    if target_state != "active":
        manifest["promotion_state"] = target_state
        manifest["applied_state"] = target_state
        result["manifest"] = manifest
        return result

    applied = registry.set_active_version(
        version,
        promotion_state=target_state,
        activation_reason=activation_reason,
    )
    if applied is not None:
        result["manifest"] = applied.to_record()
    return result



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
    prediction_row_id: str = ""
    execution_bucket: str = ""


@dataclass
class TradeHistoryEntry:
    direction: str
    amount_usdc: float
    pnl: float
    status: str
    placed_at: datetime | None
    closed_at: datetime
    simulated: bool = False
    order_id: str = ""
    condition_id: str = ""
    entry_price: float = 0.0


@dataclass
class BlockedWindow:
    """Tracks a window where we chose SKIP, to retroactively evaluate quality."""
    window_label: str = ""
    beat_price: float = 0.0
    skip_reason: str = ""
    row_id: str = ""
    condition_id: str = ""
    suggested_direction: str = "NONE"
    blocked_gate: str = ""
    mode: str = "paper"
    counterfactual_pnl: float | None = None
    final_btc_price: float | None = None
    would_have_won: bool | None = None   # True = filter correctly blocked (saved loss)


@dataclass
class WindowPredictionRecord:
    row_id: str = ""
    condition_id: str = ""
    window_label: str = ""
    window_end_at: datetime | None = None
    beat_price: float = 0.0
    mode: str = "paper"
    signal: str = "SKIP"
    predicted_direction: str = "NONE"
    decision_action: str = "observe"   # "observe" | "blocked" | "paper_trade" | "live_trade" | "model_skip"
    executed_order_id: str = ""
    simulated_order_id: str = ""
    confidence: float = 0.0
    raw_confidence: float = 0.0
    source: str = "unknown"
    model_version: str = ""
    promotion_state: str = ""
    prob_up: float = 0.5
    prob_down: float = 0.5
    alignment: int = 0
    execution_allowed: bool = False
    blocked_gate: str = ""
    blocked_reason: str = ""
    phase_bucket: str = ""
    execution_bucket: str = ""
    seconds_remaining: int = 0
    btc_price: float = 0.0
    up_odds: float = 0.0
    down_odds: float = 0.0
    signal_reason: str = ""
    decision_reason: str = ""
    runtime_skip_reason_code: str = ""
    decision_skip_reason_code: str = ""
    candidate_confidence_floor: float = 0.0
    execution_required_confidence: float = 0.0
    threshold_profile_version: str = ""
    threshold_source: str = "default"
    carry_from_observe: bool = False
    candidate_phase: str = ""
    action_phase: str = ""
    reservation_locked: bool = False
    reservation_carried_to_execution: bool = False
    soft_penalties_applied: list[str] = field(default_factory=list)
    actual_winner: str = ""
    prediction_correct: bool | None = None
    counterfactual_pnl: float | None = None
    paper_trade_won: bool | None = None
    live_trade_won: bool | None = None
    notification_locked: bool = False
    notification_sent: bool = False
    notification_signal: str = ""
    notification_gate: str = ""
    placement_failure_code: str = ""
    placement_failure_reason: str = ""
    placement_retryable: bool = False
    placement_attempt_consumed: bool = False
    placement_attempt_count: int = 0
    last_attempted_at: datetime | None = None
    sample_seq: int = 0
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
    live_trade_wins_total: int = 0
    live_trade_losses_total: int = 0
    live_trade_wins_today: int = 0
    live_trade_losses_today: int = 0

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
            "live_trade_wins_total",
            "live_trade_losses_total",
            "live_trade_wins_today",
            "live_trade_losses_today",
        ):
            setattr(self, key, int(counts.get(key, 0) or 0))

    def reset_today(self) -> None:
        self.prediction_correct_today = 0
        self.prediction_incorrect_today = 0
        self.paper_trade_wins_today = 0
        self.paper_trade_losses_today = 0
        self.live_trade_wins_today = 0
        self.live_trade_losses_today = 0

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
class SessionSignalState:
    condition_id: str = ""
    candidate_signal: str = ""
    candidate_streak: int = 0
    candidate_first_seq: int = -1
    candidate_confidence: float = 0.0
    candidate_phase_bucket: str = ""
    locked_signal: str = ""
    locked_row_id: str = ""
    locked_gate: str = ""
    locked_confidence: float = 0.0
    locked_phase_bucket: str = ""
    reservation_locked: bool = False
    reservation_carry_used: bool = False
    carry_from_observe: bool = False
    telegram_sent: bool = False
    locked_at: datetime | None = None

    def reset(self, condition_id: str = "") -> None:
        self.condition_id = condition_id
        self.candidate_signal = ""
        self.candidate_streak = 0
        self.candidate_first_seq = -1
        self.candidate_confidence = 0.0
        self.candidate_phase_bucket = ""
        self.locked_signal = ""
        self.locked_row_id = ""
        self.locked_gate = ""
        self.locked_confidence = 0.0
        self.locked_phase_bucket = ""
        self.reservation_locked = False
        self.reservation_carry_used = False
        self.carry_from_observe = False
        self.telegram_sent = False
        self.locked_at = None


@dataclass
class ModelActivationStatus:
    active_model_version: str = ""
    active_signal_source: str = "fallback"
    applied_state: str = "fallback"
    activated_at: str = ""
    activation_reason: str = ""
    threshold_profile_version: str = ""

    def to_record(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class WindowExecutionState:
    condition_id: str = ""
    attempt_count: int = 0
    retryable_failures: int = 0
    successful: bool = False
    terminal: bool = False
    last_attempt_at: float = 0.0
    last_failure_code: str = ""
    last_failure_reason: str = ""
    last_retryable: bool = False
    last_attempt_consumed: bool = False
    last_prediction_row_id: str = ""


@dataclass
class DailyHistorySnapshot:
    paper: dict[str, Any]
    live: dict[str, Any]
    status: dict[str, Any]

    def to_record(self) -> dict[str, Any]:
        return {
            "paper": self.paper,
            "live": self.live,
            "status": self.status,
        }


@dataclass
class OrderBookSnapshot:
    asset_id: str = ""
    bids: list[tuple[float, float]] = field(default_factory=list)
    asks: list[tuple[float, float]] = field(default_factory=list)
    ts: float = 0.0


@dataclass
class BotState:
    # ── Runtime
    start_time: datetime = field(default_factory=datetime.now)
    running: bool = True

    # ── BTC feed
    btc_price: float | None = None
    btc_price_time: float = 0.0
    btc_ws_ok: bool = False
    hl_btc_price:      float | None = None
    hl_btc_price_time: float        = 0.0
    hl_ws_ok:          bool         = False
    pyth_btc_price:      float | None = None
    pyth_btc_price_time: float        = 0.0
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
    balance_refresh_event: asyncio.Event = field(default_factory=asyncio.Event)

    # ── Live odds
    up_odds: float | None = None
    down_odds: float | None = None
    odds_updated_at: float | None = None
    # Timestamped odds history for velocity computation: (ts, up_odds, down_odds)
    odds_history: deque = field(default_factory=lambda: deque(maxlen=120))
    order_book_snapshots: dict[str, OrderBookSnapshot] = field(default_factory=dict)
    order_book_refreshing: set[str] = field(default_factory=set)
    settlement_registry_cache: dict[str, dict[str, Any]] = field(default_factory=dict)
    feature_history_by_condition: dict[str, deque] = field(default_factory=lambda: defaultdict(lambda: deque(maxlen=3)))

    # ── Filters / AI
    indicator_snapshot: IndicatorSnapshot | None = None
    last_signal: AISignal | None = None
    last_filter_time: float = 0.0
    last_pre_ai_decision: TradeDecision | None = None
    last_trade_decision: TradeDecision | None = None
    session_signal_state: SessionSignalState = field(default_factory=SessionSignalState)
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
    window_execution_states: dict[str, WindowExecutionState] = field(default_factory=dict)

    # ── Results
    balance_usdc: float = 0.0
    total_pnl: float = 0.0
    total_gross_wins: float = 0.0   # sum of net gain from all winning bets
    total_gross_losses: float = 0.0 # sum of stakes lost from all losing bets
    resolved_count: int = 0
    win_count: int = 0
    loss_count: int = 0
    pending_count: int = 0
    claim_log: list[str] = field(default_factory=list)
    claim_records: dict[str, ClaimRecord] = field(default_factory=dict)
    claimable_total: float = 0.0
    pending_claim_count: int = 0
    expected_claimable_total: float = 0.0
    expected_claim_pending_count: int = 0
    claimed_today_count: int = 0
    failed_today_count: int = 0
    last_claim_success_at: str = ""
    last_claim_error: str = ""
    claim_last_scan_at: float = 0.0
    claim_last_scan_trigger: str = ""
    claim_last_scan_status: str = ""
    claim_last_scan_error: str = ""
    claim_last_scan_candidates: int = 0
    claim_last_scan_identities: list[str] = field(default_factory=list)

    # ── Daily limits (reset at midnight UTC)
    daily_loss: float = 0.0           # realized losses today
    daily_profit: float = 0.0         # realized profit today
    daily_budget_spent_usdc: float = 0.0
    daily_budget_returned_usdc: float = 0.0
    daily_budget_open_keys: set[str] = field(default_factory=set)
    daily_budget_close_keys: set[str] = field(default_factory=set)
    daily_day: str = ""               # "YYYY-MM-DD" of current trading day
    daily_halted: bool = False        # True when daily budget cashflow limit reached
    daily_profit_halted: bool = False # True when daily profit target reached

    # ── Loss streak protection ──────────────────────────────────────────────
    consecutive_losses: int = 0
    consecutive_wins: int = 0
    streak_pause_until: float = 0.0   # unix timestamp; 0 = not paused

    # ── Window outcome history (for AI historical context) ──────────────────
    # Each entry: {elapsed_at_bet, gap_pct, direction, won, odds, confidence}
    recent_window_outcomes: deque = field(default_factory=lambda: deque(maxlen=50))
    trade_history: deque = field(default_factory=lambda: deque(maxlen=20))
    trade_history_last_refresh_at: float = 0.0

    # ── Clean paper analytics ────────────────────────────────────────────────
    paper_prediction_records: dict[str, WindowPredictionRecord] = field(default_factory=dict)
    prediction_records: dict[str, WindowPredictionRecord] = field(default_factory=dict)
    prediction_rows_by_condition: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    paper_stats: PaperPerformanceStats = field(default_factory=PaperPerformanceStats)
    performance_history_cache: dict[str, dict[str, Any]] = field(default_factory=dict)
    model_activation_status: ModelActivationStatus = field(default_factory=ModelActivationStatus)

    # ── ML feature tracking ──────────────────────────────────────────────────
    pending_ml_feature_rows: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))
    ml_last_retrain_day: str = ""
    ml_last_drift_check_key: str = ""

    # ── BLOCKED tracking
    blocked_windows: list[BlockedWindow] = field(default_factory=list)

    # ── Price tick log for UI streaming (ts, btc, buy_vol, sell_vol, cvd, up_odds, dn_odds)
    price_tick_log: deque = field(default_factory=lambda: deque(maxlen=200))
    price_sample_seq: int = 0
    last_prediction_sample_seq: int = -1
    last_prediction_window_id: str = ""
    last_signal_log_signature: tuple | None = None

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
        self.state      = BotState()
        self.feed       = BTCFeed(self.state)
        self.hl_feed    = HyperliquidFeed(self.state)
        self.pyth_feed  = ChainlinkProxyFeed(self.state)
        self.market   = MarketClient()
        self._ml_executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="ml-bg")
        self._ml_bootstrap_done = False
        self.model_registry = ModelRegistry(ML_MODELS_DIR)
        self.signal_engine = RuntimeSignalEngine(
            self.model_registry,
            policy=RuntimePolicy(
                observe_min_confidence=0.80,
                observe_min_edge=0.05,
                reserve_min_confidence=0.78,
                reserve_min_edge=0.04,
                early_exec_min_confidence=0.76,
                early_exec_min_edge=0.03,
                late_exec_min_confidence=GOLD_ZONE_MIN_CONF,
                late_exec_min_edge=MINIMUM_EDGE_THRESHOLD,
                late_window_confidence=LATE_DYNAMIC_MIN_CONF,
            ),
            stale_after_hours=ML_MODEL_STALE_HOURS,
        )
        self.notifier = TelegramNotifier()
        self.decision = DecisionMaker()

    async def run(self) -> None:
        self.state.log_event("[BOT] Starting up…")
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        self.state.daily_day = today
        replayed_budget_events = self._warm_daily_budget_cashflow(today)
        self._sync_daily_budget_halt(log_change=False)
        if replayed_budget_events:
            self.state.log_event(
                f"[BUDGET] Replayed {replayed_budget_events} daily cashflow event(s) "
                f"spent=${self.state.daily_budget_spent_usdc:.2f} "
                f"returned=${self.state.daily_budget_returned_usdc:.2f} "
                f"left=${self._daily_budget_left():.2f}"
            )
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
        warmed_trade_history = self._warm_trade_history()
        if warmed_trade_history:
            self.state.log_event(
                f"[HISTORY] Warmed {warmed_trade_history} settled bets for UI history"
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
        warmed_claims = self._warm_claim_records()
        if warmed_claims:
            self.state.log_event(f"[CLAIM] Warmed {warmed_claims} claim record(s)")
        warmed_expected_claims = self._warm_expected_claims_from_trades()
        if warmed_expected_claims:
            self.state.log_event(
                f"[CLAIM] Warmed {warmed_expected_claims} locally expected pending payout(s)"
            )
        if not LIVE_TRADING:
            await self._sync_recovered_paper_positions()
        self._sync_model_activation_status(reason="startup", allow_auto_promote=True, log_change=True)
        self._refresh_performance_history()
        self._log_startup_continuity_summary()
        try:
            await asyncio.gather(
                safe_loop(self.feed.run,                  "btc_feed",  self.state),
                safe_loop(self.hl_feed.run,               "hl_feed",   self.state),
                safe_loop(self.pyth_feed.run,             "pyth_feed", self.state),
                safe_loop(self._price_sampler,            "sampler",   self.state),
                safe_loop(self._market_loop,              "market",    self.state),
                safe_loop(self._odds_ws_loop,             "odds_ws",   self.state),
                safe_loop(self._trading_loop,             "trading",   self.state),
                safe_loop(self._position_monitor_loop,    "pos_mon",   self.state),
                safe_loop(self._results_loop,             "results",   self.state),
                safe_loop(self._balance_loop,             "balance",   self.state),
                safe_loop(self._claim_manager_loop,       "claims",    self.state),
                safe_loop(self._polymarket_heartbeat_loop,"poly_hb",   self.state),
                safe_loop(self._polymarket_auth_health_loop, "poly_auth", self.state),
                safe_loop(self._creds_refresh_loop,       "creds",     self.state),
                safe_loop(self._ml_maintenance_loop,      "ml_maint",  self.state),
            )
        finally:
            await self.market.close()
            self._ml_executor.shutdown(wait=False, cancel_futures=True)

    @staticmethod
    def _empty_mode_stats() -> dict[str, Any]:
        return {
            "wins": 0,
            "losses": 0,
            "total": 0,
            "win_rate": 0.0,
            "pnl": 0.0,
        }

    @staticmethod
    def _finalize_mode_stats(stats: dict[str, Any]) -> dict[str, Any]:
        wins = int(stats.get("wins", 0) or 0)
        losses = int(stats.get("losses", 0) or 0)
        total = wins + losses
        pnl = round(float(stats.get("pnl", 0.0) or 0.0), 6)
        return {
            "wins": wins,
            "losses": losses,
            "total": total,
            "win_rate": round((wins / total * 100.0) if total else 0.0, 2),
            "pnl": pnl,
        }

    def _reset_daily_budget_cashflow(self) -> None:
        self.state.daily_budget_spent_usdc = 0.0
        self.state.daily_budget_returned_usdc = 0.0
        self.state.daily_budget_open_keys.clear()
        self.state.daily_budget_close_keys.clear()

    def _daily_budget_used(self) -> float:
        return round(self.state.daily_budget_spent_usdc - self.state.daily_budget_returned_usdc, 6)

    def _daily_budget_left(self) -> float:
        if DAILY_BUDGET_USDC <= 0:
            return float("inf")
        return round(DAILY_BUDGET_USDC - self._daily_budget_used(), 6)

    @staticmethod
    def _daily_budget_key_from_position(pos: "Position") -> str:
        return BotLogger._trade_key({
            "order_id": pos.order_id,
            "condition_id": pos.condition_id,
            "direction": pos.direction,
            "placed_at": pos.placed_at.isoformat() if hasattr(pos.placed_at, "isoformat") else str(pos.placed_at),
        })

    @staticmethod
    def _daily_budget_return_amount(*, status: str, amount: float, entry_price: float, pnl: float | None) -> float:
        status_key = str(status or "").strip().lower()
        amount = max(0.0, float(amount or 0.0))
        entry_price = float(entry_price or 0.0)
        pnl_value = float(pnl) if pnl is not None else None
        if status_key == "won":
            if pnl_value is not None:
                return max(0.0, round(amount + pnl_value, 6))
            if entry_price > 0:
                return max(0.0, round(amount / entry_price, 6))
            return 0.0
        if status_key in ("void", "canceled"):
            return amount
        return 0.0

    def _record_daily_budget_open(self, pos: "Position") -> float:
        key = self._daily_budget_key_from_position(pos)
        amount = max(0.0, float(pos.amount_usdc or 0.0))
        if not key or amount <= 0.0 or key in self.state.daily_budget_open_keys:
            return 0.0
        self.state.daily_budget_open_keys.add(key)
        self.state.daily_budget_spent_usdc = round(self.state.daily_budget_spent_usdc + amount, 6)
        return amount

    def _record_daily_budget_close(self, pos: "Position") -> float:
        key = self._daily_budget_key_from_position(pos)
        if not key or key not in self.state.daily_budget_open_keys or key in self.state.daily_budget_close_keys:
            return 0.0
        returned = self._daily_budget_return_amount(
            status=pos.status,
            amount=pos.amount_usdc,
            entry_price=pos.entry_price,
            pnl=pos.pnl,
        )
        self.state.daily_budget_close_keys.add(key)
        self.state.daily_budget_returned_usdc = round(self.state.daily_budget_returned_usdc + returned, 6)
        return returned

    def _record_daily_budget_open_raw(self, record: dict[str, Any]) -> int:
        key = BotLogger._trade_key(record)
        amount = max(0.0, _safe_float(record.get("amount_usdc"), 0.0))
        if not key or amount <= 0.0 or key in self.state.daily_budget_open_keys:
            return 0
        self.state.daily_budget_open_keys.add(key)
        self.state.daily_budget_spent_usdc = round(self.state.daily_budget_spent_usdc + amount, 6)
        return 1

    def _record_daily_budget_close_raw(self, record: dict[str, Any]) -> int:
        key = BotLogger._trade_key(record)
        if not key or key not in self.state.daily_budget_open_keys or key in self.state.daily_budget_close_keys:
            return 0
        returned = self._daily_budget_return_amount(
            status=str(record.get("status", "")),
            amount=_safe_float(record.get("amount_usdc"), 0.0),
            entry_price=_safe_float(record.get("entry_price"), 0.0),
            pnl=_safe_float(record.get("pnl"), 0.0) if record.get("pnl") is not None else None,
        )
        self.state.daily_budget_close_keys.add(key)
        self.state.daily_budget_returned_usdc = round(self.state.daily_budget_returned_usdc + returned, 6)
        return 1

    def _warm_daily_budget_cashflow(self, day_key: str | None = None) -> int:
        self._reset_daily_budget_cashflow()
        day_key = day_key or datetime.now(_UTC).strftime("%Y-%m-%d")
        path = self.state.logger._dir / f"trades_{day_key}.jsonl"
        if not path.exists():
            return 0
        counted = 0
        try:
            with open(path, "r", encoding="utf-8") as handle:
                for line in handle:
                    try:
                        record = json.loads(line)
                    except Exception:
                        continue
                    event = str(record.get("event", "") or "")
                    if event == "open":
                        counted += self._record_daily_budget_open_raw(record)
                    elif event == "close":
                        counted += self._record_daily_budget_close_raw(record)
        except Exception:
            return counted
        return counted

    def _sync_daily_budget_halt(self, *, log_change: bool = False) -> None:
        if DAILY_BUDGET_USDC <= 0:
            self.state.daily_halted = False
            return
        used = self._daily_budget_used()
        should_halt = used >= DAILY_BUDGET_USDC
        if should_halt and not self.state.daily_halted:
            self.state.daily_halted = True
            if log_change:
                self.state.log_event(
                    f"[HALT] Daily budget used ${used:.2f} reached "
                    f"limit ${DAILY_BUDGET_USDC:.2f} — no new bets until midnight UTC"
                )
        elif not should_halt and self.state.daily_halted:
            self.state.daily_halted = False
            if log_change:
                self.state.log_event(
                    f"[BOT] Halt lifted — daily budget left ${self._daily_budget_left():.2f}"
                )

    def _sync_model_activation_status(
        self,
        *,
        reason: str,
        allow_auto_promote: bool,
        log_change: bool,
    ) -> ModelActivationStatus:
        previous = self.state.model_activation_status.to_record()
        manifest = self.model_registry.load_manifest()

        if (
            allow_auto_promote
            and ML_AUTO_PROMOTE
            and manifest is not None
            and manifest.promotion_state != "active"
            and bool(manifest.metrics.get("ready_for_active"))
        ):
            promoted = self.model_registry.set_active_version(
                manifest.model_version,
                promotion_state="active",
                activation_reason=reason,
            )
            if promoted is not None:
                manifest = promoted

        loaded_manifest = self.signal_engine.reload()
        manifest = loaded_manifest or manifest or self.signal_engine.current_manifest()
        runtime_source = "ml" if manifest is not None and manifest.promotion_state == "active" else "fallback"

        status = ModelActivationStatus(
            active_model_version=manifest.model_version if manifest is not None else "",
            active_signal_source=runtime_source,
            applied_state=(manifest.applied_state or manifest.promotion_state) if manifest is not None else "fallback",
            activated_at=manifest.activated_at if manifest is not None else "",
            activation_reason=manifest.activation_reason if manifest is not None else "",
            threshold_profile_version=_manifest_runtime_threshold_payload(manifest).get("version", DEFAULT_RUNTIME_THRESHOLD_PROFILE_VERSION),
        )
        self.state.model_activation_status = status

        if log_change and status.to_record() != previous:
            version = status.active_model_version or "none"
            self.state.log_event(
                f"[ML] Activated model {version} source={status.active_signal_source} "
                f"state={status.applied_state or 'fallback'} "
                f"thresholds={status.threshold_profile_version or DEFAULT_RUNTIME_THRESHOLD_PROFILE_VERSION}"
            )
        return status

    def _build_daily_history_snapshot(
        self,
        day_key: str,
        base: dict[str, Any] | None = None,
        *,
        include_current_status: bool = True,
    ) -> DailyHistorySnapshot:
        base = base or {}
        paper = self._finalize_mode_stats(dict(base.get("paper", self._empty_mode_stats())))
        live = self._finalize_mode_stats(dict(base.get("live", self._empty_mode_stats())))
        if include_current_status:
            market_client = getattr(self, "market", None)
            status = {
                "mode": "live" if LIVE_TRADING else "paper",
                "balance_usdc": round(float(self.state.balance_usdc or 0.0), 6),
                "daily_loss": round(float(self.state.daily_loss or 0.0), 6),
                "daily_profit": round(float(self.state.daily_profit or 0.0), 6),
                "daily_budget_spent_usdc": round(float(self.state.daily_budget_spent_usdc or 0.0), 6),
                "daily_budget_returned_usdc": round(float(self.state.daily_budget_returned_usdc or 0.0), 6),
                "daily_budget_left_usdc": round(float(self._daily_budget_left()), 6) if DAILY_BUDGET_USDC > 0 else None,
                "daily_halted": bool(self.state.daily_halted),
                "daily_profit_halted": bool(self.state.daily_profit_halted),
                "bets_this_hour": int(self.state.bets_this_hour or 0),
                "open_positions": len([p for p in self.state.positions if p.status == "open"]),
                "active_model_version": self.state.model_activation_status.active_model_version,
                "active_signal_source": self.state.model_activation_status.active_signal_source,
                "applied_state": self.state.model_activation_status.applied_state,
                "activation_reason": self.state.model_activation_status.activation_reason,
                "threshold_profile_version": self.state.model_activation_status.threshold_profile_version,
                "claimable_total": round(float(self.state.claimable_total or 0.0), 6),
                "pending_claim_count": int(self.state.pending_claim_count or 0),
                "expected_claimable_total": round(float(self.state.expected_claimable_total or 0.0), 6),
                "expected_claim_pending_count": int(self.state.expected_claim_pending_count or 0),
                "claimed_today_count": int(self.state.claimed_today_count or 0),
                "failed_today_count": int(self.state.failed_today_count or 0),
                "last_claim_success_at": self.state.last_claim_success_at,
                "last_claim_error": self.state.last_claim_error,
                "claim_last_scan_at": self.state.claim_last_scan_at,
                "claim_last_scan_trigger": self.state.claim_last_scan_trigger,
                "claim_last_scan_status": self.state.claim_last_scan_status,
                "claim_last_scan_error": self.state.claim_last_scan_error,
                "claim_last_scan_candidates": int(self.state.claim_last_scan_candidates or 0),
                "claim_last_scan_identities": list(self.state.claim_last_scan_identities),
                "polymarket_session": market_client.session_snapshot() if market_client is not None else {},
                "participation_recent24": self.state.logger.compute_recent_participation_metrics(limit=24),
                "participation_recent100": self.state.logger.compute_recent_participation_metrics(limit=100),
                "updated_at": _iso_z(_utc_now()),
            }
        else:
            status = dict(base.get("status", {}))
        return DailyHistorySnapshot(paper=paper, live=live, status=status)

    def _rebuild_performance_history_cache(self) -> dict[str, dict[str, Any]]:
        history: dict[str, dict[str, Any]] = {}
        seen: set[str] = set()
        history_files = sorted(
            [
                *self.state.logger._dir.glob("prediction_analytics_*.jsonl"),
                *self.state.logger._dir.glob("paper_analytics_*.jsonl"),
            ],
            key=lambda item: item.name,
        )
        for path in history_files:
            try:
                with open(path, "r", encoding="utf-8") as handle:
                    for line in handle:
                        try:
                            record = json.loads(line)
                        except Exception:
                            continue
                        event = str(record.get("event", ""))
                        if event not in ("paper_trade_resolved", "live_trade_resolved"):
                            continue
                        day_key = str(record.get("resolved_at") or record.get("ts") or "")[:10]
                        if not day_key:
                            continue
                        order_id = str(record.get("executed_order_id") or record.get("simulated_order_id") or "").strip()
                        unique_key = order_id or f"{record.get('condition_id', '')}:{record.get('placed_at', '')}:{event}"
                        if unique_key in seen:
                            continue
                        seen.add(unique_key)

                        day_entry = history.setdefault(
                            day_key,
                            {
                                "paper": self._empty_mode_stats(),
                                "live": self._empty_mode_stats(),
                                "status": {},
                            },
                        )
                        bucket = "paper" if event == "paper_trade_resolved" else "live"
                        target = day_entry[bucket]
                        won_value = record.get("paper_trade_won")
                        if not isinstance(won_value, bool):
                            won_value = record.get("live_trade_won")
                        if won_value is True:
                            target["wins"] += 1
                        elif won_value is False:
                            target["losses"] += 1
                        target["pnl"] = float(target.get("pnl", 0.0) or 0.0) + float(record.get("pnl", 0.0) or 0.0)
            except Exception:
                continue

        for day_key, entry in list(history.items()):
            snapshot = self._build_daily_history_snapshot(day_key, entry, include_current_status=False)
            history[day_key] = snapshot.to_record()
        return history

    def _write_performance_history_cache(self, history: dict[str, dict[str, Any]]) -> None:
        path = self.state.logger.performance_history_path
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = path.parent / f".{path.name}.tmp"
        tmp_path.write_text(json.dumps(history, indent=2, sort_keys=True), encoding="utf-8")
        tmp_path.replace(path)

    def _refresh_performance_history(self) -> None:
        history = self._rebuild_performance_history_cache()
        today_key = datetime.now(_UTC).strftime("%Y-%m-%d")
        history[today_key] = self._build_daily_history_snapshot(today_key, history.get(today_key)).to_record()
        self.state.performance_history_cache = history
        self._write_performance_history_cache(history)

    def _log_startup_continuity_summary(self) -> None:
        status = self.state.model_activation_status
        recent24 = self.state.logger.compute_recent_participation_metrics(limit=24)
        recent100 = self.state.logger.compute_recent_participation_metrics(limit=100)
        model_version = status.active_model_version or "none"
        thresholds = status.threshold_profile_version or DEFAULT_RUNTIME_THRESHOLD_PROFILE_VERSION
        self.state.log_event(
            f"[CONTINUITY] mode={'live' if LIVE_TRADING else 'paper'} "
            f"model={model_version} state={status.applied_state or 'fallback'} "
            f"thresholds={thresholds}"
        )
        self.state.log_event(
            f"[CONTINUITY] recent24 buy={recent24.get('buy_prediction_rate', 0.0):.0%} "
            f"exec={recent24.get('executed_bet_rate', 0.0):.0%} "
            f"fail={recent24.get('placement_failed_rate', 0.0):.0%} "
            f"reserve={recent24.get('reserved_signal_rate', 0.0):.0%} "
            f"| recent100 buy={recent100.get('buy_prediction_rate', 0.0):.0%} "
            f"exec={recent100.get('executed_bet_rate', 0.0):.0%} "
            f"fail={recent100.get('placement_failed_rate', 0.0):.0%}"
        )

    async def _refresh_order_book_snapshot(self, token_id: str) -> None:
        try:
            raw = await asyncio.wait_for(self.market.get_order_book_snapshot(token_id), timeout=1.0)
            if not isinstance(raw, dict):
                return
            bids = _normalize_book_levels(raw.get("bids", []))
            asks = _normalize_book_levels(raw.get("asks", []))
            if not bids and not asks:
                return
            self.state.order_book_snapshots[token_id] = OrderBookSnapshot(
                asset_id=token_id,
                bids=bids,
                asks=asks,
                ts=time.time(),
            )
        except Exception as exc:
            self.state.log_event(f"[OB] refresh failed for {token_id[:8]}…: {exc}")
        finally:
            self.state.order_book_refreshing.discard(token_id)

    def _ensure_order_book_snapshot(self, token_id: str) -> None:
        if not token_id:
            return
        current = self.state.order_book_snapshots.get(token_id)
        if current is not None and (time.time() - current.ts) <= 2.0:
            return
        if token_id in self.state.order_book_refreshing:
            return
        self.state.order_book_refreshing.add(token_id)
        asyncio.create_task(self._refresh_order_book_snapshot(token_id))

    def _current_order_book_imbalance(self, token_id: str) -> float:
        snapshot = self.state.order_book_snapshots.get(token_id)
        if snapshot is None:
            return 0.0
        if (time.time() - snapshot.ts) > 2.0:
            return 0.0
        return _compute_ob_imbalance_from_levels(snapshot.bids, snapshot.asks)

    def _build_signal_features(
        self,
        *,
        win: "WindowInfo",
        snap: "IndicatorSnapshot",
        fair: dict,
        beat_chop: dict,
        prices: list[float],
        cvd_ser: list[float],
        btc_price: float,
        up_odds: float,
        down_odds: float,
        elapsed_s: int,
        seconds_remaining: int,
    ) -> SignalFeatures:
        gap_signed_pct = (
            (btc_price - win.beat_price) / win.beat_price * 100.0
            if win.beat_price > 0 else 0.0
        )
        gap_pct = abs(gap_signed_pct)
        direction_bias = "UP" if gap_signed_pct > 0 else "DOWN" if gap_signed_pct < 0 else "NONE"
        signed_alignment = (
            float(snap.signal_alignment)
            if direction_bias == "UP"
            else float(-snap.signal_alignment) if direction_bias == "DOWN"
            else 0.0
        )
        price_roc_15s = 0.0
        price_roc_30s = 0.0
        if len(prices) >= 4 and prices[-4] != 0:
            price_roc_15s = (prices[-1] - prices[-4]) / prices[-4] * 100.0
        if len(prices) >= 7 and prices[-7] != 0:
            price_roc_30s = (prices[-1] - prices[-7]) / prices[-7] * 100.0

        cvd_change_last_30s = 0.0
        if len(cvd_ser) >= 7:
            cvd_change_last_30s = cvd_ser[-1] - cvd_ser[-7]

        dip_label = compute_dip_label(prices, win.beat_price, btc_price)
        feature_bars = len(prices)
        feature_completeness = min(1.0, feature_bars / 20.0)
        elapsed_fraction = max(0.0, min(1.0, elapsed_s / 300.0))
        gap_alignment_interaction = gap_signed_pct * float(snap.signal_alignment)
        returns = np.diff(np.array(prices, dtype=float)) / np.array(prices[:-1], dtype=float) if len(prices) >= 2 and all(p != 0 for p in prices[:-1]) else np.array([], dtype=float)
        realized_vol_30s = float(np.std(returns[-6:]) / math.sqrt(5.0)) if len(returns) >= 2 else 0.0
        realized_vol_60s = float(np.std(returns[-12:]) / math.sqrt(5.0)) if len(returns) >= 2 else 0.0
        previous_features = self.state.feature_history_by_condition.get(win.condition_id)
        previous_row = previous_features[-1] if previous_features else {}
        ob_imbalance = self._current_order_book_imbalance(win.up_token_id)

        return SignalFeatures(
            row_id=f"live:{win.condition_id}:{time.time_ns()}",
            ts=datetime.now(_UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            condition_id=win.condition_id,
            window_start_at=win.start_time.astimezone(_UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            window_end_at=win.end_time.astimezone(_UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            beat_price=win.beat_price,
            btc_price=btc_price,
            up_odds=up_odds,
            down_odds=down_odds,
            gap_pct=gap_pct,
            gap_signed_pct=gap_signed_pct,
            seconds_remaining=max(0, seconds_remaining),
            signal_alignment=snap.signal_alignment,
            signed_alignment=signed_alignment,
            odds_vel=snap.odds_vel_value,
            odds_vel_accel=snap.odds_vel_accel,
            cvd_divergence={"BULLISH": 1, "BEARISH": -1}.get(snap.cvd_divergence, 0),
            macd_histogram=snap.macd_histogram or 0.0,
            bb_pct_b=snap.bb_pct_b if snap.bb_pct_b is not None else 0.5,
            rsi=snap.rsi if snap.rsi is not None else 50.0,
            momentum_pct=snap.momentum_pct if snap.momentum_pct is not None else 0.0,
            is_late_window=1 if seconds_remaining < 60 else 0,
            is_bandar_zone=1 if seconds_remaining < 45 else 0,
            is_proximity_risk=1 if seconds_remaining < 60 and gap_pct < LATE_GAP_RISK_PCT else 0,
            is_proximity_risk_above=1 if seconds_remaining < 60 and gap_pct < LATE_GAP_RISK_PCT and gap_signed_pct >= 0 else 0,
            is_proximity_risk_below=1 if seconds_remaining < 60 and gap_pct < LATE_GAP_RISK_PCT and gap_signed_pct < 0 else 0,
            price_roc_15s=price_roc_15s,
            price_roc_30s=price_roc_30s,
            cvd_change_last_30s=cvd_change_last_30s,
            odds_edge_strength=up_odds - down_odds,
            elapsed_fraction=elapsed_fraction,
            gap_alignment_interaction=gap_alignment_interaction,
            realized_vol_30s=realized_vol_30s,
            realized_vol_60s=realized_vol_60s,
            gap_signed_pct_lag1=_safe_float(previous_row.get("gap_signed_pct"), 0.0),
            signal_alignment_lag1=_safe_float(previous_row.get("signal_alignment"), 0.0),
            odds_edge_strength_lag1=_safe_float(previous_row.get("odds_edge_strength"), 0.0),
            gap_crossed_zero=1 if (
                _safe_float(previous_row.get("gap_signed_pct"), 0.0) > 0 and gap_signed_pct < 0
            ) or (
                _safe_float(previous_row.get("gap_signed_pct"), 0.0) < 0 and gap_signed_pct > 0
            ) else 0,
            ob_imbalance=ob_imbalance,
            beat_above_ratio=_safe_float(beat_chop.get("above_ratio"), 0.5),
            fair_up=fair.get("fair_up", 0.5),
            fair_down=fair.get("fair_down", 0.5),
            edge_up=fair.get("edge_up", 0.0),
            edge_down=fair.get("edge_down", 0.0),
            direction_bias=direction_bias,
            dip_label=dip_label,
            feature_source="live_runtime",
            phase_bucket=self._phase_bucket(elapsed_s, seconds_remaining),
            feature_bars=feature_bars,
            feature_completeness=feature_completeness,
        )

    @staticmethod
    def _phase_bucket(elapsed_s: int, seconds_remaining: int) -> str:
        return _phase_bucket_from_timing(elapsed_s, seconds_remaining)

    def _track_ml_feature_row(self, feature_row: SignalFeatures) -> None:
        self.state.logger.log_ml_feature(feature_row.to_record())
        self.state.pending_ml_feature_rows[feature_row.condition_id].add(feature_row.row_id)
        self.state.feature_history_by_condition[feature_row.condition_id].append(feature_row.model_record())

    def _reset_session_signal_state(self, condition_id: str = "") -> None:
        self.state.session_signal_state.reset(condition_id)

    def _claim_prediction_slot(self, condition_id: str, sample_seq: int) -> bool:
        if (
            condition_id == self.state.last_prediction_window_id
            and sample_seq == self.state.last_prediction_sample_seq
        ):
            return False
        self.state.last_prediction_window_id = condition_id
        self.state.last_prediction_sample_seq = sample_seq
        return True

    def _should_emit_signal_log(self, feature_row: SignalFeatures, signal: AISignal) -> bool:
        signature = (
            feature_row.condition_id,
            feature_row.phase_bucket,
            signal.signal,
            round(signal.confidence, 2),
            round(signal.prob_up, 2),
            round(signal.prob_down, 2),
            signal.source,
        )
        previous = self.state.last_signal_log_signature
        self.state.last_signal_log_signature = signature
        if previous is None:
            return True
        if previous[0] != signature[0] or previous[1] != signature[1]:
            return True
        if previous[2] != signature[2] or previous[6] != signature[6]:
            return True
        if abs(previous[3] - signature[3]) >= 0.05:
            return True
        return False

    async def _run_ml_background(self, func, *args):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self._ml_executor, partial(func, *args))

    async def predict_signal(self, feature_row: SignalFeatures) -> AISignal:
        t0 = time.time()
        prediction = await self._run_ml_background(self.signal_engine.predict, feature_row)
        signal = AISignal(
            signal=prediction.signal,
            confidence=prediction.confidence,
            raw_confidence=prediction.raw_confidence or prediction.confidence,
            reason=prediction.reason[:120],
            latency_ms=int((time.time() - t0) * 1000),
            dip_label=feature_row.dip_label,
            source=prediction.source,
            model_version=prediction.model_version,
            prob_up=prediction.prob_up,
            prob_down=prediction.prob_down,
            promotion_state=prediction.promotion_state,
            runtime_skip_reason_code=prediction.runtime_skip_reason_code,
            soft_penalties_applied=list(prediction.soft_penalties_applied or []),
            candidate_confidence_floor=prediction.candidate_confidence_floor,
            threshold_profile_version=prediction.threshold_profile_version,
            threshold_source=prediction.threshold_source,
            candidate_phase=prediction.candidate_phase,
            action_phase=prediction.action_phase,
        )
        if prediction.shadow:
            self.state.log_event(
                f"[ML/{prediction.shadow.get('promotion_state','shadow').upper()}] "
                f"{prediction.shadow.get('signal','SKIP')} "
                f"U={prediction.shadow.get('prob_up', 0.5):.1%} "
                f"D={prediction.shadow.get('prob_down', 0.5):.1%} "
                f"v={prediction.shadow.get('model_version','')}"
            )
        return signal

    async def _predict_runtime_signal(self, feature_row: SignalFeatures) -> AISignal:
        return await self.predict_signal(feature_row)

    def _prediction_direction(self, signal: AISignal) -> str:
        if signal.signal == "BUY_UP":
            return "UP"
        if signal.signal == "BUY_DOWN":
            return "DOWN"
        return "NONE"

    def _counterfactual_pnl(self, *, direction: str, actual_winner: str, up_odds: float, down_odds: float) -> float | None:
        if direction not in ("UP", "DOWN"):
            return None
        market_odds = up_odds if direction == "UP" else down_odds
        if market_odds <= 0.0 or market_odds >= 1.0:
            return None
        if actual_winner == direction:
            return round(BET_SIZE_USDC * (1.0 / market_odds - 1.0), 6)
        if actual_winner in ("UP", "DOWN"):
            return round(-BET_SIZE_USDC, 6)
        return 0.0

    @staticmethod
    def _classify_window_outcome(beat_price: float, settlement_btc: float | None) -> str:
        if settlement_btc is None or beat_price <= 0:
            return "UNKNOWN"
        if math.isclose(settlement_btc, beat_price, rel_tol=0.0, abs_tol=1e-9):
            return "TIE"
        return "UP" if settlement_btc > beat_price else "DOWN"

    @staticmethod
    def _did_trade_win(direction: str, actual_winner: str) -> bool | None:
        direction = str(direction or "").upper()
        actual_winner = str(actual_winner or "").upper()
        if direction not in ("UP", "DOWN"):
            return None
        if actual_winner == "UP":
            return direction == "UP"
        if actual_winner == "DOWN":
            return direction == "DOWN"
        return None

    @staticmethod
    def _signal_edge(signal: AISignal, up_odds: float, down_odds: float) -> float:
        if signal.signal == "BUY_UP":
            market_odds = up_odds
            probability = signal.confidence
        elif signal.signal == "BUY_DOWN":
            market_odds = down_odds
            probability = signal.confidence
        else:
            return 0.0
        if market_odds <= 0.0 or market_odds >= 1.0:
            return 0.0
        return probability * (1.0 / market_odds) - 1.0

    async def _mark_prediction_notification(
        self,
        row_id: str,
        *,
        locked: bool | None = None,
        sent: bool | None = None,
        signal: str | None = None,
        gate: str | None = None,
        reservation_locked: bool | None = None,
        reservation_carried_to_execution: bool | None = None,
        carry_from_observe: bool | None = None,
    ) -> WindowPredictionRecord | None:
        async with self.state._lock:
            record = self.state.prediction_records.get(row_id)
            if record is None:
                return None
            if locked is not None:
                record.notification_locked = locked
            if sent is not None:
                record.notification_sent = sent
            if signal is not None:
                record.notification_signal = signal
            if gate is not None:
                record.notification_gate = gate
            if reservation_locked is not None:
                record.reservation_locked = reservation_locked
            if reservation_carried_to_execution is not None:
                record.reservation_carried_to_execution = reservation_carried_to_execution
            if carry_from_observe is not None:
                record.carry_from_observe = carry_from_observe
            record.last_updated_at = datetime.now(_UTC)
            self.state.paper_prediction_records[record.condition_id] = record
        self.state.logger.log_prediction_state(record)
        return record

    def _maybe_apply_reserved_signal_carry(
        self,
        *,
        condition_id: str,
        signal: AISignal,
        phase_bucket: str,
    ) -> tuple[AISignal, bool]:
        session = self.state.session_signal_state
        if session.condition_id != condition_id:
            return signal, False
        if not session.reservation_locked or session.reservation_carry_used:
            return signal, False
        if phase_bucket not in ("EARLY_EXEC", "LATE_EXEC"):
            return signal, False

        preferred_signal = signal.signal
        if preferred_signal not in ("BUY_UP", "BUY_DOWN"):
            preferred_signal = LABEL_BUY_UP if signal.prob_up >= signal.prob_down else LABEL_BUY_DOWN
        if preferred_signal != session.locked_signal:
            return signal, False
        if signal.confidence < max(0.0, session.locked_confidence - 0.05):
            return signal, False

        session.reservation_carry_used = True
        if signal.signal == session.locked_signal:
            return signal, True

        carried = AISignal(
            signal=session.locked_signal,
            confidence=signal.confidence,
            raw_confidence=signal.raw_confidence or signal.confidence,
            reason=f"reserve carry: {signal.reason[:96]}",
            latency_ms=signal.latency_ms,
            timestamp=signal.timestamp,
            dip_label=signal.dip_label,
            source=f"{signal.source}_reserve",
            model_version=signal.model_version,
            prob_up=signal.prob_up,
            prob_down=signal.prob_down,
            promotion_state=signal.promotion_state,
            runtime_skip_reason_code=signal.runtime_skip_reason_code,
            soft_penalties_applied=list(signal.soft_penalties_applied or []),
            candidate_confidence_floor=signal.candidate_confidence_floor,
            threshold_profile_version=signal.threshold_profile_version,
            threshold_source=signal.threshold_source,
            candidate_phase=signal.candidate_phase,
            action_phase=signal.action_phase,
            carry_from_observe=session.carry_from_observe,
        )
        return carried, True

    async def _advance_session_signal_state(
        self,
        *,
        condition_id: str,
        signal: AISignal,
        row_id: str,
        sample_seq: int,
        phase_bucket: str,
        signal_edge: float,
        execution_ready: bool,
    ) -> bool:
        session = self.state.session_signal_state
        if session.condition_id != condition_id:
            self._reset_session_signal_state(condition_id)
            session = self.state.session_signal_state

        if session.locked_signal:
            return False

        if phase_bucket in ("CLOSED", "TOO_LATE"):
            session.candidate_signal = ""
            session.candidate_streak = 0
            session.candidate_first_seq = -1
            session.candidate_confidence = 0.0
            session.candidate_phase_bucket = ""
            return False

        if signal.signal not in ("BUY_UP", "BUY_DOWN"):
            if phase_bucket in ("OBSERVE", "RESERVE", "EARLY_EXEC", "LATE_EXEC"):
                session.candidate_signal = ""
                session.candidate_streak = 0
                session.candidate_first_seq = -1
                session.candidate_confidence = 0.0
                session.candidate_phase_bucket = ""
            return False

        if phase_bucket == "OBSERVE" and signal.confidence < OBSERVE_CARRY_MIN_CONF:
            session.candidate_signal = ""
            session.candidate_streak = 0
            session.candidate_first_seq = -1
            session.candidate_confidence = 0.0
            session.candidate_phase_bucket = ""
            return False

        previous_candidate_phase = session.candidate_phase_bucket
        previous_candidate_confidence = session.candidate_confidence
        if session.candidate_signal == signal.signal:
            session.candidate_streak += 1
        else:
            session.candidate_signal = signal.signal
            session.candidate_streak = 1
            session.candidate_first_seq = sample_seq
        session.candidate_confidence = signal.confidence
        session.candidate_phase_bucket = phase_bucket

        if phase_bucket == "OBSERVE":
            return False

        immediate_lock = execution_ready or (
            signal.confidence >= SIGNAL_NOTIFY_IMMEDIATE_CONF and signal_edge > 0.0
        )
        if not immediate_lock and session.candidate_streak < SIGNAL_NOTIFY_MIN_STREAK:
            return False

        carry_from_observe = (
            previous_candidate_phase == "OBSERVE"
            or (previous_candidate_phase == "OBSERVE" and phase_bucket == "RESERVE" and session.candidate_streak >= SIGNAL_NOTIFY_MIN_STREAK)
        )
        if carry_from_observe and signal.confidence < max(0.0, previous_candidate_confidence - 0.05):
            return False

        session.locked_signal = signal.signal
        session.locked_row_id = row_id
        session.locked_confidence = signal.confidence
        session.locked_phase_bucket = phase_bucket
        session.reservation_locked = phase_bucket == "RESERVE"
        session.carry_from_observe = carry_from_observe
        session.locked_at = datetime.now(_UTC)
        await self._mark_prediction_notification(
            row_id,
            locked=True,
            signal=signal.signal,
            reservation_locked=session.reservation_locked,
            carry_from_observe=session.carry_from_observe,
        )
        return True

    async def _emit_locked_signal_notification(
        self,
        *,
        locked_now: bool,
        signal: AISignal,
        win: "WindowInfo",
        snap: "IndicatorSnapshot",
        decision: TradeDecision,
        execution_block: tuple[str, str] | None,
        btc_price: float,
        up_odds: float,
        down_odds: float,
    ) -> bool:
        session = self.state.session_signal_state
        if not locked_now or session.telegram_sent:
            return False

        gate = execution_block[0] if execution_block else (decision.gate or GATE_OK)
        reason = execution_block[1] if execution_block else decision.reason
        session.telegram_sent = True
        session.locked_gate = gate

        if execution_block is None:
            self.notifier.notify_signal(
                signal,
                win,
                snap,
                btc_price=btc_price,
                up_odds=up_odds,
                down_odds=down_odds,
                decision=decision,
            )
        else:
            shadow_notify = getattr(self.notifier, "notify_shadow_signal", None)
            if callable(shadow_notify):
                shadow_notify(
                    signal,
                    win,
                    snap,
                    btc_price=btc_price,
                    up_odds=up_odds,
                    down_odds=down_odds,
                    decision=decision,
                    execution_block=execution_block,
                )

        row_id = session.locked_row_id
        if row_id:
            await self._mark_prediction_notification(
                row_id,
                sent=True,
                signal=session.locked_signal or signal.signal,
                gate=gate,
                carry_from_observe=session.carry_from_observe,
            )
        return True

    def _build_prediction_record(
        self,
        *,
        win: "WindowInfo",
        feature_row: SignalFeatures,
        signal: AISignal,
        snap: "IndicatorSnapshot",
        decision: TradeDecision,
        decision_action: str,
        execution_allowed: bool,
        decision_reason: str = "",
        decision_skip_reason_code: str = "",
        reservation_locked: bool = False,
        reservation_carried_to_execution: bool = False,
    ) -> WindowPredictionRecord:
        return WindowPredictionRecord(
            row_id=feature_row.row_id,
            condition_id=win.condition_id,
            window_label=win.window_label,
            window_end_at=win.end_time,
            beat_price=win.beat_price,
            mode="live" if LIVE_TRADING else "paper",
            signal=signal.signal,
            predicted_direction=self._prediction_direction(signal),
            decision_action=decision_action,
            confidence=signal.confidence,
            raw_confidence=signal.raw_confidence or signal.confidence,
            source=signal.source,
            model_version=signal.model_version,
            promotion_state=signal.promotion_state,
            prob_up=signal.prob_up,
            prob_down=signal.prob_down,
            alignment=snap.signal_alignment,
            execution_allowed=execution_allowed,
            phase_bucket=feature_row.phase_bucket,
            execution_bucket=feature_row.phase_bucket,
            seconds_remaining=feature_row.seconds_remaining,
            btc_price=feature_row.btc_price,
            up_odds=feature_row.up_odds,
            down_odds=feature_row.down_odds,
            signal_reason=signal.reason,
            decision_reason=decision_reason,
            runtime_skip_reason_code=signal.runtime_skip_reason_code,
            decision_skip_reason_code=decision_skip_reason_code,
            candidate_confidence_floor=signal.candidate_confidence_floor,
            execution_required_confidence=decision.required_confidence,
            threshold_profile_version=signal.threshold_profile_version,
            threshold_source=signal.threshold_source,
            carry_from_observe=signal.carry_from_observe,
            candidate_phase=signal.candidate_phase or feature_row.phase_bucket,
            action_phase=signal.action_phase or feature_row.phase_bucket,
            reservation_locked=reservation_locked,
            reservation_carried_to_execution=reservation_carried_to_execution,
            soft_penalties_applied=list(signal.soft_penalties_applied or []),
            notification_signal=signal.signal,
            sample_seq=self.state.price_sample_seq,
            last_updated_at=datetime.now(_UTC),
        )

    async def _store_prediction_record(self, record: WindowPredictionRecord, *, log_event: bool = True) -> None:
        async with self.state._lock:
            self.state.prediction_records[record.row_id] = record
            self.state.prediction_rows_by_condition[record.condition_id].add(record.row_id)
            latest = self.state.paper_prediction_records.get(record.condition_id)
            latest_ts = latest.last_updated_at.timestamp() if latest and latest.last_updated_at else float("-inf")
            record_ts = record.last_updated_at.timestamp() if record.last_updated_at else float("-inf")
            if latest is None or latest_ts <= record_ts:
                self.state.paper_prediction_records[record.condition_id] = record
        if log_event:
            self.state.logger.log_prediction_state(record)

    async def _mark_prediction_blocked(self, row_id: str, *, gate: str, reason: str, decision_action: str = "blocked") -> WindowPredictionRecord | None:
        async with self.state._lock:
            record = self.state.prediction_records.get(row_id)
            if record is None:
                return None
            record.decision_action = decision_action
            record.execution_allowed = False
            record.blocked_gate = gate
            record.blocked_reason = reason
            record.decision_reason = reason
            record.decision_skip_reason_code = gate
            record.last_updated_at = datetime.now(_UTC)
            self.state.paper_prediction_records[record.condition_id] = record

        self.state.logger.log_prediction_blocked(record)
        return record

    async def _mark_prediction_trade_failed(
        self,
        row_id: str,
        *,
        condition_id: str,
        result: TradeResult,
        attempt_count: int,
        attempted_at: datetime | None = None,
    ) -> WindowPredictionRecord | None:
        async with self.state._lock:
            record = self.state.prediction_records.get(row_id) if row_id else None
            if record is None:
                record = self.state.paper_prediction_records.get(condition_id)
            if record is None:
                return None
            record.decision_action = "trade_failed_retryable" if result.retryable and not result.attempt_consumed else "trade_failed"
            record.decision_reason = str(result.error or "trade placement failed")
            record.placement_failure_code = result.failure_code or "PLACEMENT_FAILED"
            record.placement_failure_reason = str(result.error or "")
            record.placement_retryable = bool(result.retryable)
            record.placement_attempt_consumed = bool(result.attempt_consumed)
            record.placement_attempt_count = max(int(attempt_count or 0), int(record.placement_attempt_count or 0))
            record.last_attempted_at = attempted_at or datetime.now(_UTC)
            record.last_updated_at = datetime.now(_UTC)
            self.state.paper_prediction_records[record.condition_id] = record

        self.state.logger.log_prediction_trade_failed(record)
        return record

    async def _attach_trade_to_prediction(self, pos: "Position") -> None:
        row_id = getattr(pos, "prediction_row_id", "") or ""

        async with self.state._lock:
            record = self.state.prediction_records.get(row_id) if row_id else None
            if record is None:
                record = self.state.paper_prediction_records.get(pos.condition_id)
            if record is None:
                return
            record.executed_order_id = pos.order_id or record.executed_order_id
            if pos.simulated:
                record.simulated_order_id = pos.order_id or record.simulated_order_id
                record.decision_action = "paper_trade"
            else:
                record.decision_action = "live_trade"
            record.execution_allowed = True
            record.placement_failure_code = ""
            record.placement_failure_reason = ""
            record.placement_retryable = False
            record.placement_attempt_consumed = True
            record.last_attempted_at = datetime.now(_UTC)
            execution_state = self.state.window_execution_states.get(pos.condition_id)
            if execution_state is not None:
                record.placement_attempt_count = max(
                    int(record.placement_attempt_count or 0),
                    int(execution_state.attempt_count or 0),
                )
            record.last_updated_at = datetime.now(_UTC)
            self.state.paper_prediction_records[record.condition_id] = record

        self.state.logger.log_prediction_state(record)

    async def _record_shadow_block(self, record: WindowPredictionRecord) -> None:
        if record.predicted_direction not in ("UP", "DOWN"):
            return

        self.state.log_event(
            f"[SHADOW] {record.signal} conf={record.confidence:.0%} — blocked by {record.blocked_gate}"
        )
        async with self.state._lock:
            self.state.blocked_windows.append(BlockedWindow(
                row_id=record.row_id,
                condition_id=record.condition_id,
                window_label=record.window_label,
                beat_price=record.beat_price,
                skip_reason=f"{record.blocked_gate}: {record.blocked_reason}",
                suggested_direction=record.predicted_direction,
                blocked_gate=record.blocked_gate,
                mode=record.mode,
            ))

    @staticmethod
    def _should_record_shadow_block(gate: str) -> bool:
        return gate not in {
            GATE_ALREADY_OPEN,
            GATE_ALREADY_ATTEMPTED,
            GATE_RETRY_COOLDOWN,
            GATE_RETRY_WINDOW_CLOSED,
            GATE_RETRY_LIMIT,
            "GATE_DAILY_LOSS_LIMIT",
            "GATE_DAILY_PROFIT_TARGET",
            "GATE_RATE_LIMIT",
            "GATE_STREAK_PAUSE",
            "GATE_LOW_BALANCE",
        }

    def _window_execution_state(self, condition_id: str) -> WindowExecutionState:
        state = self.state.window_execution_states.get(condition_id)
        if state is None:
            state = WindowExecutionState(condition_id=condition_id)
            self.state.window_execution_states[condition_id] = state
        return state

    def _restore_window_execution_state(self, record: WindowPredictionRecord) -> None:
        if not record.condition_id:
            return
        if not record.executed_order_id and not record.placement_failure_code:
            return
        if record.mode != "live" and not record.executed_order_id:
            return

        state = self._window_execution_state(record.condition_id)
        state.last_prediction_row_id = record.row_id or state.last_prediction_row_id
        if record.last_attempted_at is not None:
            state.last_attempt_at = max(state.last_attempt_at, record.last_attempted_at.timestamp())
        state.attempt_count = max(
            int(state.attempt_count or 0),
            int(record.placement_attempt_count or 0),
            1 if (record.executed_order_id or record.placement_failure_code) else 0,
        )

        if record.executed_order_id:
            state.successful = True
            state.terminal = True
            state.last_failure_code = ""
            state.last_failure_reason = ""
            state.last_retryable = False
            state.last_attempt_consumed = True
            return

        if not record.placement_failure_code:
            return

        state.last_failure_code = record.placement_failure_code
        state.last_failure_reason = record.placement_failure_reason
        state.last_retryable = bool(record.placement_retryable)
        state.last_attempt_consumed = bool(record.placement_attempt_consumed)
        if record.placement_retryable:
            state.retryable_failures = max(
                int(state.retryable_failures or 0),
                int(record.placement_attempt_count or 0),
                1,
            )
        state.terminal = bool(record.placement_attempt_consumed)

    def _begin_window_execution_attempt(
        self,
        *,
        condition_id: str,
        row_id: str,
        attempted_at: float | None = None,
    ) -> WindowExecutionState:
        state = self._window_execution_state(condition_id)
        state.attempt_count += 1
        state.last_attempt_at = attempted_at if attempted_at is not None else time.time()
        state.last_prediction_row_id = row_id or state.last_prediction_row_id
        return state

    def _complete_window_execution_attempt(
        self,
        *,
        condition_id: str,
        row_id: str,
        result: TradeResult,
        attempted_at: float | None = None,
    ) -> WindowExecutionState:
        state = self._window_execution_state(condition_id)
        state.last_prediction_row_id = row_id or state.last_prediction_row_id
        if attempted_at is not None:
            state.last_attempt_at = attempted_at
        state.last_failure_code = result.failure_code or ""
        state.last_failure_reason = str(result.error or "")
        state.last_retryable = bool(result.retryable)
        state.last_attempt_consumed = bool(result.attempt_consumed)

        if result.success:
            state.successful = True
            state.terminal = True
            state.last_failure_code = ""
            state.last_failure_reason = ""
            state.last_retryable = False
            state.last_attempt_consumed = True
            return state

        if result.retryable and not result.attempt_consumed:
            state.retryable_failures += 1
            state.terminal = state.retryable_failures > LIVE_RETRY_MAX_RETRIES
        else:
            state.terminal = True
        return state

    def _execution_block(
        self,
        *,
        win: "WindowInfo",
        signal: AISignal,
        decision: TradeDecision,
        elapsed_s: int,
        seconds_remaining: int,
        now: float,
    ) -> tuple[str, str] | None:
        if signal.signal not in ("BUY_UP", "BUY_DOWN"):
            return None

        if elapsed_s < EXECUTION_START_S:
            return ("GATE_EXECUTION_WINDOW", f"elapsed={elapsed_s}s < {EXECUTION_START_S}s start")
        if seconds_remaining < LAST_MIN_SECONDS_GUARD:
            return ("GATE_TOO_LATE", f"seconds_remaining={seconds_remaining}s < {LAST_MIN_SECONDS_GUARD}s guard")
        if decision.action != "BUY":
            return (decision.gate, decision.reason)

        return None

    def _operational_execution_block(
        self,
        *,
        win: "WindowInfo",
        seconds_remaining: int,
        now: float,
    ) -> tuple[str, str] | None:
        if any(p.condition_id == win.condition_id for p in self.state.open_positions):
            return (GATE_ALREADY_OPEN, "open position already active in this window")

        execution_state = self.state.window_execution_states.get(win.condition_id)
        if execution_state is not None:
            if execution_state.successful:
                return (GATE_ALREADY_ATTEMPTED, "bet already opened in this window")
            if execution_state.terminal:
                failure_code = execution_state.last_failure_code or "terminal_failure"
                failure_reason = execution_state.last_failure_reason or "window consumed by terminal placement failure"
                return (
                    GATE_ALREADY_ATTEMPTED,
                    f"{failure_code}: {failure_reason}",
                )
            if LIVE_TRADING and execution_state.retryable_failures > 0:
                if execution_state.retryable_failures > LIVE_RETRY_MAX_RETRIES:
                    return (
                        GATE_RETRY_LIMIT,
                        f"retry budget exhausted after {execution_state.retryable_failures} retryable failure(s)",
                    )
                if seconds_remaining < LIVE_RETRY_MIN_SECONDS_REMAINING:
                    return (
                        GATE_RETRY_WINDOW_CLOSED,
                        f"seconds_remaining={seconds_remaining}s < retry minimum {LIVE_RETRY_MIN_SECONDS_REMAINING}s",
                    )
                cooldown_remaining = LIVE_RETRY_COOLDOWN_S - max(0.0, now - execution_state.last_attempt_at)
                if cooldown_remaining > 0:
                    return (
                        GATE_RETRY_COOLDOWN,
                        f"retry cooldown {cooldown_remaining:.1f}s remaining",
                    )

        if DAILY_BUDGET_USDC > 0:
            self._sync_daily_budget_halt(log_change=True)
            if self.state.daily_halted:
                used = self._daily_budget_used()
                return (
                    "GATE_DAILY_LOSS_LIMIT",
                    f"daily budget used ${used:.2f} hit limit ${DAILY_BUDGET_USDC:.2f}",
                )

        if DAILY_PROFIT_TARGET_USDC > 0 and self.state.daily_profit >= DAILY_PROFIT_TARGET_USDC:
            if not self.state.daily_profit_halted:
                self.state.daily_profit_halted = True
                self.state.log_event(
                    f"[HALT] Daily profit target ${DAILY_PROFIT_TARGET_USDC:.2f} reached "
                    f"(earned ${self.state.daily_profit:.2f} today) — no new bets until midnight UTC"
                )
            return ("GATE_DAILY_PROFIT_TARGET", "daily profit target reached")

        if self.state.bets_this_hour >= MAX_BETS_PER_HOUR:
            return ("GATE_RATE_LIMIT", "max bets per hour reached")

        if now < self.state.streak_pause_until:
            remaining_m = max(1, int((self.state.streak_pause_until - now) / 60))
            return ("GATE_STREAK_PAUSE", f"{remaining_m}m remaining")

        return None

    def _get_window_settlement_info(
        self,
        *,
        condition_id: str,
        window_end_at: datetime | None,
    ) -> SettlementInfo | None:
        cached = self.state.settlement_registry_cache.get(condition_id)
        if cached is None and condition_id:
            cached = load_settlement_registry(self.state.logger._dir).get(condition_id)
            if cached is not None:
                self.state.settlement_registry_cache[condition_id] = cached
        if cached is not None:
            settlement_price = _safe_float(cached.get("settlement_price"), 0.0)
            if settlement_price > 0.0:
                return SettlementInfo(
                    settlement_price=settlement_price,
                    settlement_source=str(cached.get("settlement_source", "")) or "chainlink_market_resolved",
                    resolved_at=ml_parse_utc_ts(cached.get("resolved_at")),
                    settlement_source_priority=int(cached.get("settlement_source_priority", 0)),
                    chainlink_settlement_price=_safe_float(cached.get("chainlink_settlement_price"), 0.0) or settlement_price,
                )

        target = window_end_at
        if target is None:
            active_win = self.state.window
            if active_win and active_win.condition_id == condition_id:
                target = active_win.end_time
        if target is None:
            return None

        history_ts = list(self.state.price_history_ts)
        if history_ts:
            closest = min(history_ts, key=lambda x: abs(x[0] - target.timestamp()))
            diff_s = abs(closest[0] - target.timestamp())
            if diff_s <= 15.0:
                return SettlementInfo(
                    settlement_price=closest[1],
                    settlement_source="binance_15s",
                    resolved_at=datetime.fromtimestamp(closest[0], _UTC),
                    settlement_source_priority=_label_source_priority("binance_15s"),
                    binance_resolution_diff_s=diff_s,
                )
            if diff_s <= 90.0:
                return SettlementInfo(
                    settlement_price=closest[1],
                    settlement_source="binance_90s",
                    resolved_at=datetime.fromtimestamp(closest[0], _UTC),
                    settlement_source_priority=_label_source_priority("binance_90s"),
                    binance_resolution_diff_s=diff_s,
                )

        logged_price_15s = self.state.logger.find_price_near(target, max_diff_s=15.0)
        if logged_price_15s is not None:
            return SettlementInfo(
                settlement_price=logged_price_15s,
                settlement_source="binance_15s",
                resolved_at=target,
                settlement_source_priority=_label_source_priority("binance_15s"),
                binance_resolution_diff_s=0.0,
            )
        logged_price_90s = self.state.logger.find_price_near(target, max_diff_s=90.0)
        if logged_price_90s is not None:
            return SettlementInfo(
                settlement_price=logged_price_90s,
                settlement_source="binance_90s",
                resolved_at=target,
                settlement_source_priority=_label_source_priority("binance_90s"),
                binance_resolution_diff_s=0.0,
            )
        return None

    async def _poll_settlement_after_expiry(
        self,
        *,
        condition_id: str,
        window_end_at: datetime,
    ) -> bool:
        """Poll GAMMA API for Chainlink-equivalent settlement after window expiry.

        Returns True if a high-priority settlement (>= SETTLEMENT_POLL_MIN_PRIORITY)
        was obtained and cached. Non-blocking — returns immediately if already cached
        at sufficient priority. Does nothing if the market has not yet expired or if
        more than SETTLEMENT_GRACE_PERIOD_S seconds have elapsed without a result.
        """
        if not condition_id:
            return False

        # Already have a sufficiently authoritative settlement cached?
        cached = self.state.settlement_registry_cache.get(condition_id)
        if cached is None:
            cached = load_settlement_registry(self.state.logger._dir).get(condition_id)
            if cached is not None:
                self.state.settlement_registry_cache[condition_id] = cached
        if cached is not None:
            cached_priority = int(cached.get("settlement_source_priority", 0))
            if cached_priority >= SETTLEMENT_POLL_MIN_PRIORITY:
                return True

        now_ts = time.time()
        expiry_ts = window_end_at.timestamp()
        if now_ts < expiry_ts:
            return False  # market hasn't expired yet

        elapsed_s = now_ts - expiry_ts
        if elapsed_s > SETTLEMENT_GRACE_PERIOD_S:
            return False  # too late to bother polling

        try:
            record = await self.market.fetch_market_settlement(condition_id)
        except Exception:
            record = None

        if record is not None:
            self.state.logger.log_settlement(record.to_record())
            self.state.settlement_registry_cache[condition_id] = record.to_record()
            self.state.log_event(
                f"[SETTLE_POLL] Chainlink settlement polled for {condition_id[:8]}: "
                f"${record.settlement_price:,.2f} source={record.settlement_source} "
                f"({elapsed_s:.0f}s post-expiry)"
            )
            # Wake up the claim manager immediately so it can scan for redeemable
            # positions without waiting for the next scheduled scan interval.
            self.state.market_resolved_event.set()
            return True

        self.state.log_event(
            f"[SETTLE_POLL] No Chainlink settlement yet for {condition_id[:8]} "
            f"({elapsed_s:.0f}s post-expiry) — will retry"
        )
        return False

    async def _poll_settlements_for_open_positions(self) -> None:
        """For all open positions with expired windows and no high-priority settlement,
        poll GAMMA API to obtain Chainlink-equivalent settlement before resolving."""
        now_ts = time.time()
        async with self.state._lock:
            expired_open = [
                p for p in self.state.positions
                if p.status == "open"
                and p.window_end_at is not None
                and p.window_end_at.timestamp() < now_ts
            ]
        for pos in expired_open:
            cached = self.state.settlement_registry_cache.get(pos.condition_id)
            cached_priority = int(cached.get("settlement_source_priority", 0)) if cached else 0
            if cached_priority < SETTLEMENT_POLL_MIN_PRIORITY and pos.window_end_at is not None:
                await self._poll_settlement_after_expiry(
                    condition_id=pos.condition_id,
                    window_end_at=pos.window_end_at,
                )

    def _resolve_pending_ml_labels(
        self,
        *,
        condition_id: str,
        beat_price: float,
        resolved_btc_price: float | None,
        resolved_at: datetime | None = None,
        settlement_info: SettlementInfo | None = None,
    ) -> None:
        if resolved_btc_price is None or beat_price <= 0:
            return

        row_ids = list(self.state.pending_ml_feature_rows.pop(condition_id, set()))
        if not row_ids:
            return

        if math.isclose(resolved_btc_price, beat_price, rel_tol=0.0, abs_tol=1e-9):
            return

        label = "BUY_UP" if resolved_btc_price > beat_price else "BUY_DOWN"
        resolution_ts = (resolved_at or datetime.now(_UTC)).astimezone(_UTC).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        # AUDIT_ML_LABELS: log side-by-side Binance vs Chainlink outcome comparison.
        # Surfaces how often oracle divergence corrupts ML training labels.
        if AUDIT_ML_LABELS and settlement_info is not None:
            chainlink_price = settlement_info.chainlink_settlement_price or 0.0
            if chainlink_price > 0.0:
                binance_outcome = label
                chainlink_outcome = "BUY_UP" if chainlink_price > beat_price else "BUY_DOWN"
                diverged = binance_outcome != chainlink_outcome
                self.state.log_event(
                    f"[LABEL_AUDIT] cid={condition_id[:8]} beat={beat_price:,.2f} "
                    f"binance_settle={resolved_btc_price:,.2f} chainlink_settle={chainlink_price:,.2f} "
                    f"binance_outcome={binance_outcome} chainlink_outcome={chainlink_outcome} "
                    f"{'*** DIVERGED ***' if diverged else 'match'} "
                    f"source={settlement_info.settlement_source}(p={settlement_info.settlement_source_priority})"
                )

        for row_id in row_ids:
            label_row = ResolvedLabelRecord(
                row_id=row_id,
                condition_id=condition_id,
                resolution_ts=resolution_ts,
                resolved_label=label,
                resolved_btc_price=resolved_btc_price,
                label_source=settlement_info.settlement_source if settlement_info is not None else "window_resolution",
                chainlink_settlement_price=settlement_info.chainlink_settlement_price if settlement_info is not None else None,
                binance_resolution_diff_s=settlement_info.binance_resolution_diff_s if settlement_info is not None else None,
                settlement_source_priority=settlement_info.settlement_source_priority if settlement_info is not None else 0,
            )
            self.state.logger.log_ml_label(label_row.to_record())

    def _backfill_ml_labels_once(self) -> int:
        return backfill_ml_labels(self.state.logger._dir)

    def _train_ml_once(self) -> dict:
        active_manifest = self.model_registry.load_manifest()
        promotion_state = active_manifest.promotion_state if active_manifest else ML_PROMOTION_STATE
        result = train_outcome_model(
            log_dir=self.state.logger._dir,
            models_dir=ML_MODELS_DIR,
            promotion_state="shadow",
            min_rows=ML_MIN_TRAIN_ROWS,
            min_distinct_windows=ML_MIN_TRAIN_WINDOWS,
        )
        result = auto_apply_trained_model(
            result,
            self.model_registry,
            auto_promote=ML_AUTO_PROMOTE,
            fallback_state=promotion_state if promotion_state in PROMOTION_STATES else "shadow",
            activation_reason="scheduled_retrain",
        )
        self.signal_engine.reload()
        return result

    def _check_recent_model_drift_once(self) -> dict[str, Any] | None:
        bundle = self.model_registry.load_active_bundle()
        if bundle is None:
            return None
        model, calibrator, manifest = bundle
        baseline = _safe_float(manifest.metrics.get("cv_auc_pr_mean"), 0.0)
        if baseline <= 0.0:
            return None

        dataset = _prepare_training_frame(load_training_dataset(self.state.logger._dir))
        if dataset.empty or len(dataset) < ML_DRIFT_LOOKBACK_ROWS:
            return None

        recent = dataset.tail(ML_DRIFT_LOOKBACK_ROWS).copy()
        y_recent = (recent["resolved_label"] == LABEL_BUY_UP).astype(int).to_numpy()
        if len(np.unique(y_recent)) < 2:
            return None

        feature_list = list(manifest.feature_list or MODEL_FEATURE_COLUMNS)
        raw = model.predict_proba(recent[feature_list])[:, 1]
        try:
            calibrated = np.asarray(calibrator.predict(raw), dtype=float)
        except Exception:
            calibrated = np.asarray(raw, dtype=float)
        calibrated = np.clip(calibrated, 0.0, 1.0)
        recent_ap = float(average_precision_score(y_recent, calibrated))
        recent_brier = float(brier_score_loss(y_recent, calibrated))
        return {
            "recent_ap": recent_ap,
            "recent_brier": recent_brier,
            "baseline_ap": baseline,
            "drift_detected": recent_ap < baseline - ML_DRIFT_AP_DROP,
        }

    async def _bootstrap_ml_runtime(self) -> None:
        if self._ml_bootstrap_done:
            return

        self._ml_bootstrap_done = True
        self.state.log_event("[ML] Starting background bootstrap")

        try:
            appended_labels = await self._run_ml_background(self._backfill_ml_labels_once)
            if appended_labels:
                self.state.log_event(
                    f"[ML] Backfilled {appended_labels} pending label(s) from feature logs"
                )
        except Exception as exc:
            self.state.log_event(f"[ML] Bootstrap label backfill skipped: {exc}")

        try:
            result = await self._run_ml_background(self._train_ml_once)
            self._sync_model_activation_status(reason="bootstrap", allow_auto_promote=True, log_change=True)
            self._refresh_performance_history()
            manifest = result["manifest"]
            metrics = result["metrics"]
            self.state.log_event(
                f"[ML] Bootstrap trained {manifest['model_version']} state={manifest['promotion_state']} "
                f"ap={metrics.get('auc_pr', 0.0):.3f} "
                f"cv_ap={metrics.get('cv_auc_pr_mean', 0.0):.3f} "
                f"ev={metrics.get('policy_metrics', {}).get('realized_ev_per_trade', 0.0):+.2f}"
            )
        except Exception as exc:
            self.state.log_event(f"[ML] Bootstrap train skipped: {exc}")

    async def _ml_maintenance_loop(self) -> None:
        await self._bootstrap_ml_runtime()
        while self.state.running:
            await asyncio.sleep(60)
            now_utc = datetime.now(_UTC)
            drift_key = now_utc.strftime("%Y-%m-%dT%H")
            if (
                now_utc.minute % ML_DRIFT_CHECK_INTERVAL_MIN == 0
                and self.state.ml_last_drift_check_key != drift_key
            ):
                self.state.ml_last_drift_check_key = drift_key
                try:
                    drift = await self._run_ml_background(self._check_recent_model_drift_once)
                    if drift is not None:
                        self.state.log_event(
                            f"[ML] Drift check ap={drift['recent_ap']:.3f} "
                            f"baseline={drift['baseline_ap']:.3f} "
                            f"brier={drift['recent_brier']:.3f}"
                        )
                        if drift.get("drift_detected"):
                            self.state.log_event("[ML] Drift detected — triggering early retrain")
                            result = await self._run_ml_background(self._train_ml_once)
                            self._sync_model_activation_status(reason="auc_drift_detected", allow_auto_promote=True, log_change=True)
                            self._refresh_performance_history()
                            manifest = result["manifest"]
                            metrics = result["metrics"]
                            self.state.log_event(
                                f"[ML] Drift retrain {manifest['model_version']} state={manifest['promotion_state']} "
                                f"ap={metrics.get('auc_pr', 0.0):.3f} "
                                f"cv_ap={metrics.get('cv_auc_pr_mean', 0.0):.3f}"
                            )
                except Exception as exc:
                    self.state.log_event(f"[ML] Drift check skipped: {exc}")

            if (
                now_utc.hour != ML_RETRAIN_HOUR_UTC
                or now_utc.minute < ML_RETRAIN_MINUTE_UTC
            ):
                continue

            day_key = now_utc.strftime("%Y-%m-%d")
            if self.state.ml_last_retrain_day == day_key:
                continue

            self.state.ml_last_retrain_day = day_key
            self.state.log_event("[ML] Starting scheduled retrain")
            try:
                appended_labels = await self._run_ml_background(self._backfill_ml_labels_once)
                if appended_labels:
                    self.state.log_event(
                        f"[ML] Backfilled {appended_labels} pending label(s) before scheduled retrain"
                    )
                result = await self._run_ml_background(self._train_ml_once)
                self._sync_model_activation_status(reason="scheduled_retrain", allow_auto_promote=True, log_change=True)
                self._refresh_performance_history()
                manifest = result["manifest"]
                metrics = result["metrics"]
                self.state.log_event(
                    f"[ML] Trained {manifest['model_version']} state={manifest['promotion_state']} "
                    f"ap={metrics.get('auc_pr', 0.0):.3f} "
                    f"cv_ap={metrics.get('cv_auc_pr_mean', 0.0):.3f} "
                    f"ev={metrics.get('policy_metrics', {}).get('realized_ev_per_trade', 0.0):+.2f}"
                )
            except Exception as exc:
                self.state.log_event(f"[ML] Scheduled retrain skipped: {exc}")

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
                self.state.price_sample_seq += 1

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
                    self._reset_session_signal_state()
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
                        self.state.log_event(
                            f"[MKT] ⚠ Beat price extraction failed — using Binance spot "
                            f"${win.beat_price:,.2f} as fallback. Oracle divergence risk elevated."
                        )
                self.state.window = win
                self.state.window_found_at = time.time()
                self.state.last_signal = None   # clear stale signal from previous window
                self.state.last_pre_ai_decision = None
                self.state.last_trade_decision = None
                self._reset_session_signal_state(win.condition_id)
                self.state.latest_fair_prob = {}
                self.state.latest_beat_chop = {}
                self.state.feature_history_by_condition.pop(win.condition_id, None)
                self.state.order_book_snapshots.pop(win.up_token_id, None)
                self.state.order_book_snapshots.pop(win.down_token_id, None)
                self.state.set_engine_status("NEW_WINDOW", reason="monitoring new window")
                current_execution_state = self.state.window_execution_states.get(win.condition_id)
                self.state.window_execution_states.clear()
                if current_execution_state is not None:
                    self.state.window_execution_states[win.condition_id] = current_execution_state
                self.state.market_resolved_event.clear()
                self.notifier.notify_window(win, self.state)
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

            prices = list(self.state.price_history_5s)
            buy_vols = list(self.state.buy_vol_5s)
            sell_vols = list(self.state.sell_vol_5s)
            cvd_ser = list(self.state.cvd_5s)

            win = self.state.window
            elapsed_for_snap = int((datetime.now(_UTC) - win.start_time).total_seconds()) if win else 9999
            if self.state.btc_price is not None and self.state.up_odds is not None and self.state.down_odds is not None:
                up_odds_snap = self.state.up_odds or 0.5
                down_odds_snap = self.state.down_odds or 0.5
                if not (0.85 <= up_odds_snap + down_odds_snap <= 1.15):
                    up_odds_snap = down_odds_snap = 0.5
                snap_display = run_all_filters(
                    prices,
                    up_odds_snap,
                    down_odds_snap,
                    elapsed_for_snap,
                    buy_vols=buy_vols,
                    sell_vols=sell_vols,
                    cvd_series=cvd_ser,
                    odds_history=list(self.state.odds_history),
                )
                self.state.indicator_snapshot = snap_display
                self.state.last_filter_time = now

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

            today = datetime.now(_UTC).strftime("%Y-%m-%d")
            if self.state.daily_day != today:
                self.state.daily_day = today
                self.state.daily_loss = 0.0
                self.state.daily_profit = 0.0
                self._reset_daily_budget_cashflow()
                self.state.daily_halted = False
                self.state.daily_profit_halted = False
                self.state.paper_stats.reset_today()
                self.state.log_event(f"[BOT] Daily limits reset for {today}")
                self._refresh_performance_history()

            if now - self.state.hour_reset_at > 3600:
                self.state.bets_this_hour = 0
                self.state.hour_reset_at = now

            now_utc = datetime.now(_UTC)
            elapsed_s = int((now_utc - win.start_time).total_seconds())
            seconds_remaining = int((win.end_time - now_utc).total_seconds())
            if seconds_remaining <= 0:
                self.state.set_engine_status("WINDOW_END", reason="waiting for result resolution")
                continue
            if not self._claim_prediction_slot(win.condition_id, self.state.price_sample_seq):
                continue

            fair_display = compute_fair_probability(
                btc_price=self.state.btc_price,
                beat_price=win.beat_price,
                seconds_remaining=max(0, seconds_remaining),
                price_history_5s=prices,
            )
            fair_display["edge_up"] = compute_edge(fair_display["fair_up"], self.state.up_odds)
            fair_display["edge_down"] = compute_edge(fair_display["fair_down"], self.state.down_odds)
            self.state.latest_fair_prob = fair_display
            self.state.latest_beat_chop = compute_beat_chop_metrics(prices, win.beat_price)

            prices_now = list(self.state.price_history_5s)
            buy_vols_now = list(self.state.buy_vol_5s)
            sell_vols_now = list(self.state.sell_vol_5s)
            cvd_ser_now = list(self.state.cvd_5s)
            btc_price_now = self.state.btc_price
            up_odds_now = self.state.up_odds
            down_odds_now = self.state.down_odds

            if btc_price_now is None:
                self.state.set_engine_status("WAIT_BTC", reason="waiting for BTC feed")
                continue
            _btc_age = now - self.state.btc_price_time
            if _btc_age > BTC_STALENESS_THRESHOLD_S:
                self.state.set_engine_status(
                    "BTC_STALE",
                    reason=f"Binance BTC feed stale ({_btc_age:.1f}s old)",
                )
                continue
            if up_odds_now is None or down_odds_now is None:
                self.state.set_engine_status("WAIT_ODDS", reason="waiting for Polymarket odds")
                continue
            if win.beat_price <= 0:
                self.state.set_engine_status("WAIT_BEAT", reason="beat price not yet resolved")
                continue

            # ── Consensus BTC price: Binance + Hyperliquid cross-reference ────────
            # If both feeds are fresh, average them for a more robust price.
            # If they diverge by more than HL_DIVERGENCE_THRESHOLD_PCT of beat_price,
            # the market is ambiguous — skip the bet cycle.
            _hl_age   = now - self.state.hl_btc_price_time
            _hl_fresh = (
                self.state.hl_btc_price is not None
                and _hl_age < BTC_STALENESS_THRESHOLD_S
            )
            if _hl_fresh:
                _divergence_pct = (
                    abs(btc_price_now - self.state.hl_btc_price)
                    / win.beat_price * 100.0
                )
                if _divergence_pct > HL_DIVERGENCE_THRESHOLD_PCT:
                    self.state.set_engine_status(
                        "PRICE_CONFLICT",
                        reason=(
                            f"Binance ${btc_price_now:,.2f} vs HL ${self.state.hl_btc_price:,.2f} "
                            f"diverge {_divergence_pct:.3f}% > {HL_DIVERGENCE_THRESHOLD_PCT:.2f}%"
                        ),
                    )
                    continue
                btc_price_now = (btc_price_now + self.state.hl_btc_price) / 2.0

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

            fair = compute_fair_probability(
                btc_price=btc_price_now,
                beat_price=win.beat_price,
                seconds_remaining=seconds_remaining,
                price_history_5s=prices_now,
            )
            fair["edge_up"] = compute_edge(fair["fair_up"], up_odds_now)
            fair["edge_down"] = compute_edge(fair["fair_down"], down_odds_now)
            beat_chop = compute_beat_chop_metrics(prices_now, win.beat_price)
            self.state.latest_fair_prob = fair
            self.state.latest_beat_chop = beat_chop
            self._ensure_order_book_snapshot(win.up_token_id)

            feature_row = self._build_signal_features(
                win=win,
                snap=snap,
                fair=fair,
                beat_chop=beat_chop,
                prices=prices_now,
                cvd_ser=cvd_ser_now,
                btc_price=btc_price_now,
                up_odds=up_odds_now,
                down_odds=down_odds_now,
                elapsed_s=elapsed_s,
                seconds_remaining=seconds_remaining,
            )
            self._track_ml_feature_row(feature_row)

            ctx = DecisionContext(
                win=win,
                elapsed_s=elapsed_s,
                seconds_remaining=seconds_remaining,
                btc_price=btc_price_now,
                up_odds=up_odds_now,
                down_odds=down_odds_now,
                snap=snap,
                dip_label=feature_row.dip_label,
                signal_alignment=snap.signal_alignment,
                beat_crossings=beat_chop["crossings"],
                beat_above_ratio=beat_chop["above_ratio"],
                beat_below_ratio=beat_chop["below_ratio"],
                max_odds_threshold=GATE_TOO_SURE_THRESHOLD,
                fair_prob=fair,
            )

            is_btc_above = btc_price_now > win.beat_price
            leading_odds = up_odds_now if is_btc_above else down_odds_now
            gap_pct = abs(btc_price_now - win.beat_price) / win.beat_price * 100
            side = "UP" if is_btc_above else "DOWN"
            self.state.set_engine_status("SIGNAL_QUERY", reason="running ML/fallback signal engine")
            signal = await self.predict_signal(feature_row)
            if signal.source == "fallback" and signal.signal in ("BUY_UP", "BUY_DOWN"):
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

            signal, reservation_carried = self._maybe_apply_reserved_signal_carry(
                condition_id=win.condition_id,
                signal=signal,
                phase_bucket=feature_row.phase_bucket,
            )
            signal.action_phase = feature_row.phase_bucket
            self.state.last_signal = signal
            execution_window_open = feature_row.phase_bucket in ("EARLY_EXEC", "LATE_EXEC")

            self.state.set_engine_status(
                "SIGNAL_DONE",
                reason=f"{signal.signal} conf={signal.confidence:.0%} src={signal.source}",
            )
            if self._should_emit_signal_log(feature_row, signal):
                self.state.log_event(
                    f"[SIGNAL/{feature_row.phase_bucket}] {signal.signal} conf={signal.confidence:.2f} "
                    f"src={signal.source} U={signal.prob_up:.1%} D={signal.prob_down:.1%} "
                    f"| {signal.reason[:60]}"
                )
            self.state.logger.log_signal(
                signal,
                row_id=feature_row.row_id,
                elapsed_s=elapsed_s,
                up_odds=up_odds_now,
                down_odds=down_odds_now,
                btc_price=btc_price_now,
                beat_price=win.beat_price,
                is_gold_zone=execution_window_open,
                alignment=snap.signal_alignment,
                cvd_divergence=snap.cvd_divergence,
                condition_id=win.condition_id,
            )

            ctx.ai_signal = signal
            ctx.dip_label = signal.dip_label
            ctx.signal_alignment = snap.signal_alignment
            signal.soft_penalties_applied = self.decision.soft_penalties(ctx)
            decision = self.decision.apply_execution_policy(ctx)
            self.state.last_pre_ai_decision = decision if decision.gate != GATE_OK else None
            self.state.last_trade_decision = decision

            record = self._build_prediction_record(
                win=win,
                feature_row=feature_row,
                signal=signal,
                snap=snap,
                decision=decision,
                decision_action="observe" if signal.signal in ("BUY_UP", "BUY_DOWN") else "model_skip",
                execution_allowed=execution_window_open and decision.action == "BUY",
                decision_reason=decision.reason,
                decision_skip_reason_code=decision.gate if decision.action != "BUY" else "",
                reservation_carried_to_execution=reservation_carried,
            )
            await self._store_prediction_record(record)
            if reservation_carried:
                await self._mark_prediction_notification(
                    record.row_id,
                    reservation_carried_to_execution=True,
                )

            execution_block = self._execution_block(
                win=win,
                signal=signal,
                decision=decision,
                elapsed_s=elapsed_s,
                seconds_remaining=seconds_remaining,
                now=now,
            )
            signal_edge = self._signal_edge(signal, up_odds_now, down_odds_now)
            locked_now = await self._advance_session_signal_state(
                condition_id=win.condition_id,
                signal=signal,
                row_id=record.row_id,
                sample_seq=self.state.price_sample_seq,
                phase_bucket=feature_row.phase_bucket,
                signal_edge=signal_edge,
                execution_ready=execution_block is None and decision.action == "BUY",
            )
            await self._emit_locked_signal_notification(
                locked_now=locked_now,
                signal=signal,
                win=win,
                snap=snap,
                decision=decision,
                execution_block=execution_block,
                btc_price=btc_price_now,
                up_odds=up_odds_now,
                down_odds=down_odds_now,
            )

            if execution_block is not None:
                gate, reason = execution_block
                if gate == "GATE_EXECUTION_WINDOW":
                    self.state.set_engine_status("DECISION_WAIT", gate, reason)
                    continue
                if signal.signal in ("BUY_UP", "BUY_DOWN"):
                    blocked = await self._mark_prediction_blocked(
                        record.row_id,
                        gate=gate,
                        reason=reason,
                    )
                    if blocked is not None and self._should_record_shadow_block(gate):
                        await self._record_shadow_block(blocked)
                    self.state.set_engine_status("DECISION_SKIP", gate, reason)
                else:
                    self.state.set_engine_status("DECISION_SKIP", decision.gate, decision.reason)
                continue

            if decision.action != "BUY":
                continue

            operational_block = self._operational_execution_block(
                win=win,
                seconds_remaining=seconds_remaining,
                now=now,
            )
            if operational_block is not None:
                gate, reason = operational_block
                self.state.set_engine_status("EXECUTION_HOLD", gate, reason)
                continue

            self.state.log_event(
                f"[EXECUTE] {elapsed_s}s | BTC {gap_pct:.2f}% → {side} "
                f"@ {leading_odds:.3f} | align={snap.signal_alignment} "
                f"CVD={snap.cvd_divergence} | placing {'live' if LIVE_TRADING else 'paper'} order…"
            )
            await self._place_trade(
                win,
                signal,
                snap,
                prices_now,
                is_gold_zone=True,
                prediction_row_id=record.row_id,
            )

    async def _place_trade(
        self,
        win,
        signal: "AISignal",
        snap: "IndicatorSnapshot",
        prices: list[float],
        is_gold_zone: bool = False,
        prediction_row_id: str = "",
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
        if signal.soft_penalties_applied:
            penalized_bet = max(MIN_BET_USDC, round(bet_size * SOFT_PENALTY_KELLY_MULTIPLIER, 2))
            if penalized_bet < bet_size:
                self.state.log_event(
                    f"[KELLY/PENALTY] soft={','.join(signal.soft_penalties_applied)} "
                    f"${bet_size:.2f} -> ${penalized_bet:.2f}"
                )
                bet_size = penalized_bet
        zone_tag = "GOLD" if is_gold_zone else "NORM"

        # ── Oracle divergence check ───────────────────────────────────────────
        # Compare Binance USDC spot (used for trading) against the Pyth
        # Chainlink-proxy price. A large spread near the beat price means the
        # Polymarket oracle could resolve differently from what Binance shows.
        pyth_price = self.state.pyth_btc_price
        binance_price = self.state.btc_price
        if pyth_price is not None and binance_price is not None and binance_price > 0:
            divergence = abs(binance_price - pyth_price)
            if divergence >= ORACLE_DIVERGENCE_ALERT_USD:
                self.state.log_event(
                    f"[ORACLE_DIV] ⚠ Binance=${binance_price:,.2f} Pyth=${pyth_price:,.2f} "
                    f"spread=${divergence:,.2f} (threshold=${ORACLE_DIVERGENCE_ALERT_USD:.0f}) "
                    f"dir={direction} beat=${win.beat_price:,.2f}"
                )
                if SKIP_ON_HIGH_DIVERGENCE:
                    self.state.log_event("[ORACLE_DIV] Trade skipped due to high oracle divergence")
                    return

        attempt_started_at_ts = time.time()
        attempt_started_at = datetime.now(_UTC)
        execution_state = self._begin_window_execution_attempt(
            condition_id=win.condition_id,
            row_id=prediction_row_id,
            attempted_at=attempt_started_at_ts,
        )
        if LIVE_TRADING:
            available_balance = max(0.0, self.state.balance_usdc)
            try:
                min_order_size = await self.market.get_min_order_size(token_id)
            except Exception:
                min_order_size = 0.0
            if min_order_size > 0:
                min_notional = round(min_order_size * entry_odds, 4)
                if bet_size + 1e-9 < min_notional:
                    if available_balance + 1e-9 < min_notional:
                        error_msg = (
                            f"live balance ${available_balance:.2f} below market minimum "
                            f"${min_notional:.2f} ({min_order_size:.2f} shares @ {entry_odds:.2f})"
                        )
                        result = TradeResult(
                            success=False,
                            error=error_msg,
                            failure_code="INSUFFICIENT_BALANCE_MIN_ORDER",
                            retryable=False,
                            attempt_consumed=True,
                        )
                        execution_state = self._complete_window_execution_attempt(
                            condition_id=win.condition_id,
                            row_id=prediction_row_id,
                            result=result,
                            attempted_at=attempt_started_at_ts,
                        )
                        await self._mark_prediction_trade_failed(
                            prediction_row_id,
                            condition_id=win.condition_id,
                            result=result,
                            attempt_count=execution_state.attempt_count,
                            attempted_at=attempt_started_at,
                        )
                        self.state.set_engine_status("ORDER_FAILED", reason=error_msg)
                        self.state.log_event(f"[TRADE] Aborted — {error_msg}")
                        return
                    self.state.log_event(
                        f"[KELLY/MIN_ORDER] ${bet_size:.2f} -> ${min_notional:.2f} "
                        f"({min_order_size:.2f} shares @ {entry_odds:.2f})"
                    )
                    bet_size = min_notional
            if available_balance + 1e-9 < bet_size:
                error_msg = (
                    f"live balance ${available_balance:.2f} below target bet "
                    f"${bet_size:.2f}"
                )
                result = TradeResult(
                    success=False,
                    error=error_msg,
                    failure_code="INSUFFICIENT_BALANCE_PRECHECK",
                    retryable=False,
                    attempt_consumed=True,
                )
                execution_state = self._complete_window_execution_attempt(
                    condition_id=win.condition_id,
                    row_id=prediction_row_id,
                    result=result,
                    attempted_at=attempt_started_at_ts,
                )
                await self._mark_prediction_trade_failed(
                    prediction_row_id,
                    condition_id=win.condition_id,
                    result=result,
                    attempt_count=execution_state.attempt_count,
                    attempted_at=attempt_started_at,
                )
                self.state.set_engine_status("ORDER_FAILED", reason=error_msg)
                self.state.log_event(f"[TRADE] Aborted — {error_msg}")
                return
        if DAILY_BUDGET_USDC > 0:
            daily_budget_left = self._daily_budget_left()
            if bet_size > daily_budget_left + 1e-9:
                error_msg = (
                    f"daily budget left ${daily_budget_left:.2f} below target bet "
                    f"${bet_size:.2f}"
                )
                result = TradeResult(
                    success=False,
                    error=error_msg,
                    failure_code="DAILY_BUDGET_PRECHECK",
                    retryable=False,
                    attempt_consumed=True,
                )
                execution_state = self._complete_window_execution_attempt(
                    condition_id=win.condition_id,
                    row_id=prediction_row_id,
                    result=result,
                    attempted_at=attempt_started_at_ts,
                )
                await self._mark_prediction_trade_failed(
                    prediction_row_id,
                    condition_id=win.condition_id,
                    result=result,
                    attempt_count=execution_state.attempt_count,
                    attempted_at=attempt_started_at,
                )
                self._sync_daily_budget_halt(log_change=True)
                self.state.set_engine_status("ORDER_FAILED", reason=error_msg)
                self.state.log_event(f"[TRADE] Held — {error_msg}")
                return
        self.state.log_event(
            f"[KELLY/{zone_tag}] bankroll=${bankroll:.2f} conf={signal.confidence:.2f} "
            f"implied={entry_odds:.3f} → bet=${bet_size:.2f}"
        )

        result: TradeResult = await self.market.place_bet(
            direction, token_id, bet_size, entry_odds
        )
        execution_state = self._complete_window_execution_attempt(
            condition_id=win.condition_id,
            row_id=prediction_row_id,
            result=result,
            attempted_at=attempt_started_at_ts,
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
                prediction_row_id=prediction_row_id,
                execution_bucket=self._phase_bucket(elapsed_bet, max(0, int((win.end_time - now_utc).total_seconds()))),
            )
            async with self.state._lock:
                self.state.positions.append(pos)
                self._record_daily_budget_open(pos)
            self._sync_daily_budget_halt(log_change=True)
            self.state.bets_this_hour += 1
            await self._attach_trade_to_prediction(pos)
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
            failure_code = result.failure_code or "PLACEMENT_FAILED"
            failure_reason = str(result.error or "unknown placement failure")
            await self._mark_prediction_trade_failed(
                prediction_row_id,
                condition_id=win.condition_id,
                result=result,
                attempt_count=execution_state.attempt_count,
                attempted_at=attempt_started_at,
            )
            self.state.set_engine_status("ORDER_FAILED", reason=f"{failure_code}: {failure_reason}")
            self.state.log_event(
                f"[TRADE] Order failed ({failure_code}) retryable={result.retryable} "
                f"consumed={result.attempt_consumed} attempt={execution_state.attempt_count}: {failure_reason}"
            )

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

                # Optional: re-score the open order before canceling
                fresh_conf: float | None = None
                if CANCEL_ON_CONF_DROP and self.state.indicator_snapshot:
                    snap = self.state.indicator_snapshot
                    prices = list(self.state.price_history_5s)
                    cvd_ser = list(self.state.cvd_5s)
                    elapsed_s = int((now_utc - win.start_time).total_seconds())
                    try:
                        fair = compute_fair_probability(
                            btc_price=self.state.btc_price or 0.0,
                            beat_price=win.beat_price,
                            seconds_remaining=seconds_remaining,
                            price_history_5s=prices,
                        )
                        fair["edge_up"] = compute_edge(fair["fair_up"], up_odds)
                        fair["edge_down"] = compute_edge(fair["fair_down"], down_odds)
                        beat_chop = compute_beat_chop_metrics(prices, win.beat_price)
                        feature_row = self._build_signal_features(
                            win=win,
                            snap=snap,
                            fair=fair,
                            beat_chop=beat_chop,
                            prices=prices,
                            cvd_ser=cvd_ser,
                            btc_price=self.state.btc_price or 0.0,
                            up_odds=up_odds,
                            down_odds=down_odds,
                            elapsed_s=elapsed_s,
                            seconds_remaining=seconds_remaining,
                        )
                        fresh_signal = await self._predict_runtime_signal(feature_row)
                        fresh_conf = fresh_signal.confidence
                    except Exception:
                        pass

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
            await self._poll_settlements_for_open_positions()
            await self._check_positions()
            await self._resolve_prediction_analytics()
            await self._resolve_blocked_windows()

    async def _check_positions(self) -> None:
        async with self.state._lock:
            open_positions = [p for p in self.state.positions if p.status == "open"]

        for pos in open_positions:
            beat   = pos.window_beat if pos.window_beat > 0 else 0
            amount = pos.amount_usdc if pos.amount_usdc > 0 else BET_SIZE_USDC
            settlement_info = self._get_window_settlement_info(
                condition_id=pos.condition_id,
                window_end_at=pos.window_end_at,
            )
            settlement_btc = settlement_info.settlement_price if settlement_info is not None else None

            # ── Settlement priority grace period ──────────────────────────────
            # If we only have a low-priority Binance-based settlement and the
            # window expired recently, wait for the Chainlink/GAMMA poll to
            # complete before locking in a win/loss. This prevents oracle
            # divergence from corrupting win/loss classification and ML labels.
            if settlement_info is not None:
                s_priority = settlement_info.settlement_source_priority
                if s_priority < SETTLEMENT_POLL_MIN_PRIORITY and pos.window_end_at is not None:
                    window_age_s = time.time() - pos.window_end_at.timestamp()
                    if window_age_s < SETTLEMENT_GRACE_PERIOD_S:
                        continue  # wait for higher-priority Chainlink settlement

            # ── Simulated positions ───────────────────────────────────────────
            # Resolve when the window they were placed in has ended.
            if pos.simulated:
                if not self._position_window_has_ended(pos):
                    continue
                # Window over (or we're in a new window) — evaluate outcome
                if settlement_btc is None or beat <= 0:
                    continue
                actual_winner = self._classify_window_outcome(beat, settlement_btc)
                if actual_winner == "UNKNOWN":
                    continue
                await self._settle_position(pos, actual_winner, amount)
                continue

            # ── Live orders — verify via CLOB GET /order/{orderID} ───────────
            # Only resolve once the window has ended (order may match instantly
            # via FOK, but the payout is determined at expiry).
            if not self._position_window_has_ended(pos):
                continue

            order = await self.market.get_order(pos.order_id)
            order_status = (order.get("status", "") if order else "").upper()

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
                    if order_status in ("CANCELED", "CANCELED_MARKET_RESOLVED"):
                        await self._mark_position_canceled(
                            pos,
                            f"exchange returned {order_status} after window end with no fill evidence",
                        )
                    continue
                matched = True

            if not matched or settlement_btc is None or beat <= 0:
                continue
            actual_winner = self._classify_window_outcome(beat, settlement_btc)
            if actual_winner == "UNKNOWN":
                continue
            await self._settle_position(pos, actual_winner, amount)

    async def _settle_position(self, pos: "Position", actual_winner: str, amount: float) -> None:
        """Apply win/loss to a position and fire all downstream notifications."""
        settlement_btc = self._get_settlement_btc(pos)
        settlement_info = self._get_window_settlement_info(
            condition_id=pos.condition_id,
            window_end_at=pos.window_end_at,
        )
        won = self._did_trade_win(pos.direction, actual_winner)
        expected_claim: ClaimRecord | None = None
        async with self.state._lock:
            pos.status = "won" if won is True else "lost" if won is False else "void"
            if won is True:
                fee_rate = POLYMARKET_TAKER_FEE_RATE if not pos.simulated else 0.0
                payout   = amount / pos.entry_price
                pos.pnl  = payout * (1.0 - fee_rate) - amount
            elif won is False:
                pos.pnl  = -amount
            else:
                pos.pnl  = 0.0
            if won is True:
                self.state.win_count           += 1
                self.state.total_pnl           += pos.pnl or 0
                self.state.total_gross_wins    += pos.pnl or 0
                self.state.daily_profit        += pos.pnl or 0
                self.state.consecutive_wins    += 1
                self.state.consecutive_losses   = 0
            elif won is False:
                self.state.loss_count          += 1
                self.state.total_pnl           += pos.pnl or 0
                self.state.total_gross_losses  += amount
                self.state.daily_loss          += amount
                self.state.consecutive_losses += 1
                self.state.consecutive_wins    = 0
                if self.state.consecutive_losses >= STREAK_HALT_COUNT:
                    self.state.streak_pause_until = time.time() + (STREAK_PAUSE_MIN * 60)
                    self.state.log_event(
                        f"[STREAK_HALT] {self.state.consecutive_losses} consecutive losses — "
                        f"pausing bets for {STREAK_PAUSE_MIN}min"
                    )
            self._record_daily_budget_close(pos)

            # Record for AI historical context
            if isinstance(won, bool):
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
                self.state.trade_history.appendleft(TradeHistoryEntry(
                    direction=pos.direction,
                    amount_usdc=pos.amount_usdc if pos.amount_usdc > 0 else amount,
                    pnl=pos.pnl or 0.0,
                    status=pos.status,
                    placed_at=pos.placed_at,
                    closed_at=datetime.now(_UTC),
                    simulated=pos.simulated,
                    order_id=pos.order_id,
                    condition_id=pos.condition_id,
                ))
                if won is True and not pos.simulated:
                    expected_claim = self._expected_claim_record_from_position(pos)
            prediction_record = None
            if pos.prediction_row_id:
                prediction_record = self.state.prediction_records.get(pos.prediction_row_id)
            if pos.simulated:
                if isinstance(won, bool):
                    self.state.paper_stats.record_paper_trade(won)
                if prediction_record is None:
                    prediction_record = self.state.paper_prediction_records.get(pos.condition_id)
                if prediction_record is not None:
                    prediction_record.paper_trade_won = won
                    prediction_record.simulated_order_id = pos.order_id or prediction_record.simulated_order_id
                    prediction_record.executed_order_id = pos.order_id or prediction_record.executed_order_id
                    prediction_record.last_updated_at = datetime.now(_UTC)
                    self.state.paper_prediction_records[pos.condition_id] = prediction_record
            elif prediction_record is not None:
                prediction_record.live_trade_won = won
                prediction_record.executed_order_id = pos.order_id or prediction_record.executed_order_id
                prediction_record.last_updated_at = datetime.now(_UTC)
                self.state.paper_prediction_records[pos.condition_id] = prediction_record
            self.state.resolved_count += 1

        self._sync_daily_budget_halt(log_change=True)
        if expected_claim is not None:
            self._persist_expected_claim_state(expected_claim)
        self.state.log_event(
            f"[RESULT] {pos.direction} {pos.status.upper()} PnL={pos.pnl:+.2f} actual={actual_winner}"
        )
        self._resolve_pending_ml_labels(
            condition_id=pos.condition_id,
            beat_price=pos.window_beat,
            resolved_btc_price=settlement_btc,
            resolved_at=datetime.now(_UTC),
            settlement_info=settlement_info,
        )
        self.state.logger.log_trade_close(pos)
        self.state.logger.log_trade_execution_resolved(pos, won)
        if prediction_record is not None and prediction_record.prediction_correct is None:
            self.state.logger.log_prediction_state(prediction_record)
        self._refresh_performance_history()
        self.notifier.notify_result(pos, self.state)

    async def _mark_position_canceled(self, pos: "Position", reason: str) -> None:
        async with self.state._lock:
            if pos.status != "open":
                return
            pos.status = "canceled"
            pos.pnl = 0.0
            self._record_daily_budget_close(pos)

        self._sync_daily_budget_halt(log_change=True)
        self.state.log_event(f"[CANCEL] {reason}")
        self.state.logger.log_trade_close(pos)

    async def _resolve_prediction_analytics(self) -> None:
        """Resolve all scored BUY predictions after the window closes in any mode."""
        async with self.state._lock:
            pending = [
                rec for rec in self.state.prediction_records.values()
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

            resolved_at = datetime.now(_UTC)
            actual_winner = self._classify_window_outcome(record.beat_price, settlement_btc)
            correct = (
                record.predicted_direction == actual_winner
                if actual_winner in ("UP", "DOWN")
                else None
            )

            counterfactual_pnl = self._counterfactual_pnl(
                direction=record.predicted_direction,
                actual_winner=actual_winner,
                up_odds=record.up_odds,
                down_odds=record.down_odds,
            )

            async with self.state._lock:
                current = self.state.prediction_records.get(record.row_id)
                if current is None or current.prediction_correct is not None:
                    continue
                current.actual_winner = actual_winner
                current.prediction_correct = correct
                current.counterfactual_pnl = counterfactual_pnl
                current.resolved_at = resolved_at
                current.last_updated_at = resolved_at
                self.state.paper_prediction_records[current.condition_id] = current
                if isinstance(correct, bool):
                    self.state.paper_stats.record_prediction(correct)
                record_to_log = current

            self.state.logger.log_prediction_resolved(record_to_log)
            self.state.log_event(
                f"[PRED/{record_to_log.mode.upper()}] {record_to_log.predicted_direction} "
                f"{'HIT' if correct is True else 'MISS' if correct is False else 'TIE'} "
                f"| actual={actual_winner} gate={record_to_log.blocked_gate or '—'} "
                f"window={record_to_log.window_label}"
            )

    async def _resolve_paper_predictions(self) -> None:
        await self._resolve_prediction_analytics()

    async def _resolve_blocked_windows(self) -> None:
        """Retroactively evaluate skipped windows against actual BTC outcome."""
        win = self.state.window
        if not win:
            return

        now = datetime.now(_UTC)
        if now < win.end_time:
            return  # window still open

        settlement_btc = self._get_settlement_btc_for_window(
            condition_id=win.condition_id,
            window_end_at=win.end_time,
        )
        actual_winner = self._classify_window_outcome(win.beat_price, settlement_btc)

        async with self.state._lock:
            for bw in self.state.blocked_windows:
                if bw.would_have_won is not None:
                    continue
                if bw.condition_id and bw.condition_id != win.condition_id:
                    continue
                if not bw.condition_id and bw.window_label != win.window_label:
                    continue
                bw.final_btc_price = settlement_btc
                if bw.suggested_direction == "NONE":
                    bw.would_have_won = None
                    continue
                if actual_winner not in ("UP", "DOWN"):
                    bw.would_have_won = None
                    continue
                bet_up = bw.suggested_direction == "UP"
                # would_have_won=True means the SKIP was a mistake (missed profit)
                # would_have_won=False means the SKIP was correct (avoided loss)
                bw.would_have_won = (bet_up and actual_winner == "UP") or (not bet_up and actual_winner == "DOWN")
                if bw.row_id:
                    prediction = self.state.prediction_records.get(bw.row_id)
                    if prediction is not None:
                        bw.counterfactual_pnl = prediction.counterfactual_pnl

        self._resolve_pending_ml_labels(
            condition_id=win.condition_id,
            beat_price=win.beat_price,
            resolved_btc_price=settlement_btc,
            resolved_at=now,
            settlement_info=self._get_window_settlement_info(
                condition_id=win.condition_id,
                window_end_at=win.end_time,
            ),
        )

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
                prediction_row_id=str(record.get("prediction_row_id", "")).strip(),
            )
            self.state.positions.append(pos)
            if pos.condition_id:
                execution_state = self._window_execution_state(pos.condition_id)
                execution_state.attempt_count = max(int(execution_state.attempt_count or 0), 1)
                execution_state.successful = True
                execution_state.terminal = True
                execution_state.last_attempt_at = max(
                    float(execution_state.last_attempt_at or 0.0),
                    pos.placed_at.timestamp(),
                )
                execution_state.last_prediction_row_id = pos.prediction_row_id or execution_state.last_prediction_row_id
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
        settlement_info = self._get_window_settlement_info(
            condition_id=condition_id,
            window_end_at=window_end_at,
        )
        return settlement_info.settlement_price if settlement_info is not None else None

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

    def _warm_trade_history(self) -> int:
        loaded = self.state.logger.load_recent_trade_history(
            limit=self.state.trade_history.maxlen or 20
        )
        self.state.trade_history.clear()
        self.state.trade_history.extend(loaded)
        return len(loaded)

    def _warm_paper_analytics(self) -> tuple[int, int]:
        pending, counts = self.state.logger.load_prediction_analytics(
            today=datetime.now(_UTC).strftime("%Y-%m-%d")
        )
        self.state.paper_stats.apply_counts(counts)

        restored = 0
        for raw in pending.values():
            row_id = str(raw.get("row_id") or raw.get("condition_id") or "").strip()
            condition_id = str(raw.get("condition_id", "")).strip()
            if not row_id or not condition_id:
                continue
            record = WindowPredictionRecord(
                row_id=row_id,
                condition_id=condition_id,
                window_label=str(raw.get("window_label", "")),
                window_end_at=self._parse_logged_datetime(raw.get("window_end_at")),
                beat_price=float(raw.get("beat_price", 0.0) or 0.0),
                mode=str(raw.get("mode", "paper")),
                signal=str(raw.get("signal", "SKIP")),
                predicted_direction=str(raw.get("predicted_direction", "NONE")),
                decision_action=str(raw.get("decision_action", "observe")),
                executed_order_id=str(raw.get("executed_order_id", "")).strip(),
                simulated_order_id=str(raw.get("simulated_order_id", "")).strip(),
                confidence=float(raw.get("confidence", 0.0) or 0.0),
                raw_confidence=float(raw.get("raw_confidence", 0.0) or 0.0),
                source=str(raw.get("source", "unknown")),
                model_version=str(raw.get("model_version", "")),
                promotion_state=str(raw.get("promotion_state", "")),
                prob_up=float(raw.get("prob_up", 0.5) or 0.5),
                prob_down=float(raw.get("prob_down", 0.5) or 0.5),
                alignment=int(raw.get("alignment", 0) or 0),
                execution_allowed=bool(raw.get("execution_allowed", False)),
                blocked_gate=str(raw.get("blocked_gate", "")),
                blocked_reason=str(raw.get("blocked_reason", "")),
                phase_bucket=str(raw.get("phase_bucket", "")),
                execution_bucket=str(raw.get("execution_bucket", raw.get("phase_bucket", ""))),
                seconds_remaining=int(raw.get("seconds_remaining", 0) or 0),
                btc_price=float(raw.get("btc_price", 0.0) or 0.0),
                up_odds=float(raw.get("up_odds", 0.0) or 0.0),
                down_odds=float(raw.get("down_odds", 0.0) or 0.0),
                signal_reason=str(raw.get("signal_reason", "")),
                decision_reason=str(raw.get("decision_reason", "")),
                runtime_skip_reason_code=str(raw.get("runtime_skip_reason_code", "")),
                decision_skip_reason_code=str(raw.get("decision_skip_reason_code", "")),
                candidate_confidence_floor=float(raw.get("candidate_confidence_floor", 0.0) or 0.0),
                execution_required_confidence=float(raw.get("execution_required_confidence", 0.0) or 0.0),
                threshold_profile_version=str(raw.get("threshold_profile_version", "")),
                threshold_source=str(raw.get("threshold_source", "default")),
                carry_from_observe=bool(raw.get("carry_from_observe", False)),
                candidate_phase=str(raw.get("candidate_phase", raw.get("phase_bucket", ""))),
                action_phase=str(raw.get("action_phase", raw.get("phase_bucket", ""))),
                reservation_locked=bool(raw.get("reservation_locked", False)),
                reservation_carried_to_execution=bool(raw.get("reservation_carried_to_execution", False)),
                soft_penalties_applied=list(raw.get("soft_penalties_applied", []) or []),
                actual_winner=str(raw.get("actual_winner", "")),
                prediction_correct=raw.get("prediction_correct") if isinstance(raw.get("prediction_correct"), bool) else None,
                counterfactual_pnl=float(raw.get("counterfactual_pnl", 0.0)) if raw.get("counterfactual_pnl") is not None else None,
                paper_trade_won=raw.get("paper_trade_won") if isinstance(raw.get("paper_trade_won"), bool) else None,
                live_trade_won=raw.get("live_trade_won") if isinstance(raw.get("live_trade_won"), bool) else None,
                notification_locked=bool(raw.get("notification_locked", False)),
                notification_sent=bool(raw.get("notification_sent", False)),
                notification_signal=str(raw.get("notification_signal", "")),
                notification_gate=str(raw.get("notification_gate", "")),
                placement_failure_code=str(raw.get("placement_failure_code", "")),
                placement_failure_reason=str(raw.get("placement_failure_reason", "")),
                placement_retryable=bool(raw.get("placement_retryable", False)),
                placement_attempt_consumed=bool(raw.get("placement_attempt_consumed", False)),
                placement_attempt_count=int(raw.get("placement_attempt_count", 0) or 0),
                last_attempted_at=self._parse_logged_datetime(raw.get("last_attempted_at")),
                sample_seq=int(raw.get("sample_seq", 0) or 0),
                resolved_at=self._parse_logged_datetime(raw.get("resolved_at")),
                last_updated_at=self._parse_logged_datetime(raw.get("last_updated_at")),
            )
            self.state.prediction_records[row_id] = record
            self.state.prediction_rows_by_condition[condition_id].add(row_id)
            self.state.paper_prediction_records[condition_id] = record
            self._restore_window_execution_state(record)
            restored += 1

        warmed = (
            self.state.paper_stats.prediction_total
            + self.state.paper_stats.paper_trade_total
            + self.state.paper_stats.live_trade_wins_total
            + self.state.paper_stats.live_trade_losses_total
        )
        return restored, warmed

    def _append_claim_log(self, message: str) -> None:
        stamp = datetime.now().strftime("%H:%M:%S")
        self.state.claim_log.append(f"{stamp} {message}")
        if len(self.state.claim_log) > 50:
            self.state.claim_log.pop(0)

    @staticmethod
    def _claim_record_from_raw(raw: dict[str, Any]) -> ClaimRecord:
        return ClaimRecord(
            claim_id=str(raw.get("claim_id", "") or ""),
            condition_id=str(raw.get("condition_id", "") or ""),
            market_id=str(raw.get("market_id", "") or ""),
            asset=str(raw.get("asset", "") or ""),
            outcome=str(raw.get("outcome", "") or ""),
            outcome_index=int(raw.get("outcome_index", -1) or -1),
            title=str(raw.get("title", "") or ""),
            end_date=str(raw.get("end_date", "") or ""),
            claimable_amount=float(raw.get("claimable_amount", 0.0) or 0.0),
            claim_source=str(raw.get("claim_source", "positions_api_redeemable") or "positions_api_redeemable"),
            status=str(raw.get("status", "discovered") or "discovered"),
            attempt_count=int(raw.get("attempt_count", 0) or 0),
            last_attempt_at=str(raw.get("last_attempt_at", "") or ""),
            last_seen_at=str(raw.get("last_seen_at", "") or ""),
            queued_at=str(raw.get("queued_at", "") or ""),
            tx_hash=str(raw.get("tx_hash", "") or ""),
            request_id=str(raw.get("request_id", "") or ""),
            error_code=str(raw.get("error_code", "") or ""),
            error_message=str(raw.get("error_message", "") or ""),
            redeemable=bool(raw.get("redeemable", False)),
            mergeable=bool(raw.get("mergeable", False)),
            negative_risk=bool(raw.get("negative_risk", False)),
            proxy_wallet=str(raw.get("proxy_wallet", "") or ""),
            scan_identity=str(raw.get("scan_identity", "") or ""),
            schema_version=str(raw.get("schema_version", FEATURE_SCHEMA_VERSION) or FEATURE_SCHEMA_VERSION),
        )

    def _sync_claim_runtime_counts(self) -> None:
        today = datetime.now(_UTC).strftime("%Y-%m-%d")
        pending_count = 0
        claimable_total = 0.0
        expected_pending_count = 0
        expected_claimable_total = 0.0
        claimed_today = 0
        failed_today = 0
        last_success = self.state.last_claim_success_at
        last_error = self.state.last_claim_error
        server_condition_ids = {
            record.condition_id
            for record in self.state.claim_records.values()
            if record.status != "expected_pending" and record.condition_id
        }

        for record in self.state.claim_records.values():
            if record.status in ("discovered", "queued", "submitted", "skipped", "failed"):
                claimable_total += float(record.claimable_amount or 0.0)
            if (
                record.status == "expected_pending"
                and record.condition_id not in server_condition_ids
            ):
                expected_claimable_total += float(record.claimable_amount or 0.0)
                expected_pending_count += 1
            if record.status in ("queued", "submitted"):
                pending_count += 1
            if record.status == "confirmed" and record.last_attempt_at[:10] == today:
                claimed_today += 1
                last_success = max(last_success, record.last_attempt_at)
            if record.status == "failed" and record.last_attempt_at[:10] == today:
                failed_today += 1
                if record.error_message:
                    last_error = record.error_message

        self.state.claimable_total = round(claimable_total, 6)
        self.state.pending_claim_count = pending_count
        self.state.expected_claimable_total = round(expected_claimable_total, 6)
        self.state.expected_claim_pending_count = expected_pending_count
        self.state.claimed_today_count = claimed_today
        self.state.failed_today_count = failed_today
        self.state.last_claim_success_at = last_success
        self.state.last_claim_error = last_error

    def _warm_claim_records(self) -> int:
        records, counts = self.state.logger.load_claim_records(
            today=datetime.now(_UTC).strftime("%Y-%m-%d")
        )
        self.state.claim_records = {
            claim_id: self._claim_record_from_raw(raw)
            for claim_id, raw in records.items()
        }
        self.state.last_claim_success_at = str(counts.get("last_claim_success_at", "") or "")
        self.state.last_claim_error = str(counts.get("last_claim_error", "") or "")
        self._sync_claim_runtime_counts()
        return len(self.state.claim_records)

    def _warm_expected_claims_from_trades(self) -> int:
        loaded = self.state.logger.load_recent_trade_history(limit=500, lookback_days=2)
        grouped: dict[str, dict[str, Any]] = {}
        for entry in loaded:
            if entry.status != "won" or entry.simulated:
                continue
            condition_id = str(entry.condition_id or "").strip()
            if not condition_id:
                continue
            claim_id = self._claim_id_from_positions(condition_id, False)
            expected_amount = self._daily_budget_return_amount(
                status="won",
                amount=entry.amount_usdc,
                entry_price=entry.entry_price,
                pnl=entry.pnl,
            )
            if expected_amount <= 0.0:
                continue
            bucket = grouped.setdefault(
                claim_id,
                {
                    "condition_id": condition_id,
                    "amount": 0.0,
                    "last_seen_at": "",
                    "outcomes": set(),
                },
            )
            bucket["amount"] = round(float(bucket["amount"]) + expected_amount, 6)
            bucket["last_seen_at"] = max(
                str(bucket["last_seen_at"] or ""),
                _iso_z(entry.closed_at) if entry.closed_at else "",
            )
            bucket["outcomes"].add(str(entry.direction or "").upper())

        warmed = 0
        for claim_id, item in grouped.items():
            outcomes = sorted(item["outcomes"])
            record = ClaimRecord(
                claim_id=claim_id,
                condition_id=str(item["condition_id"]),
                outcome=" / ".join(outcomes),
                claimable_amount=float(item["amount"] or 0.0),
                claim_source="local_trade_settlement",
                status="expected_pending",
                last_seen_at=str(item["last_seen_at"] or _iso_z(_utc_now())),
                redeemable=False,
                scan_identity="local",
            )
            if self._persist_expected_claim_state(record):
                warmed += 1
        return warmed

    async def _sync_recovered_paper_positions(self) -> None:
        async with self.state._lock:
            open_simulated = [p for p in self.state.positions if p.simulated and p.status == "open"]

        for pos in open_simulated:
            await self._attach_trade_to_prediction(pos)

    async def _upsert_paper_prediction(
        self,
        win: "WindowInfo",
        signal: "AISignal",
        snap: "IndicatorSnapshot",
        *,
        decision_action: str,
    ) -> None:
        if signal.signal not in ("BUY_UP", "BUY_DOWN"):
            return

        row_id = f"legacy:{win.condition_id}:{time.time_ns()}"
        record = WindowPredictionRecord(
            row_id=row_id,
            condition_id=win.condition_id,
            window_label=win.window_label,
            window_end_at=win.end_time,
            beat_price=win.beat_price,
            mode="live" if LIVE_TRADING else "paper",
            signal=signal.signal,
            predicted_direction="UP" if signal.signal == "BUY_UP" else "DOWN",
            decision_action=decision_action,
            confidence=signal.confidence,
            raw_confidence=signal.raw_confidence or signal.confidence,
            source=getattr(signal, "source", "unknown"),
            model_version=getattr(signal, "model_version", ""),
            promotion_state=getattr(signal, "promotion_state", ""),
            prob_up=getattr(signal, "prob_up", 0.5),
            prob_down=getattr(signal, "prob_down", 0.5),
            alignment=snap.signal_alignment,
            execution_allowed=decision_action in ("paper_trade", "live_trade"),
            phase_bucket=self._phase_bucket(int((datetime.now(_UTC) - win.start_time).total_seconds()), int((win.end_time - datetime.now(_UTC)).total_seconds())),
            candidate_confidence_floor=getattr(signal, "candidate_confidence_floor", 0.0),
            threshold_profile_version=getattr(signal, "threshold_profile_version", ""),
            threshold_source=getattr(signal, "threshold_source", "default"),
            candidate_phase=getattr(signal, "candidate_phase", ""),
            action_phase=getattr(signal, "action_phase", ""),
            seconds_remaining=max(0, int((win.end_time - datetime.now(_UTC)).total_seconds())),
            notification_signal=signal.signal,
            sample_seq=int(time.time()),
            last_updated_at=datetime.now(_UTC),
        )
        await self._store_prediction_record(record)

    async def _attach_paper_trade_to_prediction(self, pos: "Position") -> None:
        await self._attach_trade_to_prediction(pos)

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
        """Deflate runtime confidence toward realized performance and market odds."""
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

    @staticmethod
    def _claimable_amount_from_position(position: dict[str, Any]) -> float:
        current_value = float(position.get("currentValue", 0.0) or 0.0)
        cash_pnl = float(position.get("cashPnl", 0.0) or 0.0)
        size = float(position.get("size", 0.0) or 0.0)
        cur_price = float(position.get("curPrice", 0.0) or 0.0)
        fallback_value = size * cur_price if size > 0.0 and cur_price > 0.0 else 0.0
        return round(max(current_value, cash_pnl, fallback_value), 6)

    @staticmethod
    def _claim_id_from_positions(condition_id: str, negative_risk: bool) -> str:
        cid = str(condition_id or "").strip()
        return f"{cid}:neg_risk" if negative_risk else cid

    @staticmethod
    def _claim_scan_label(label: str, user: str) -> str:
        return f"{str(label or 'user')}:{_mask_address(user)}"

    @staticmethod
    def _claim_scan_identities() -> list[tuple[str, str]]:
        identities: list[tuple[str, str]] = []
        seen: set[str] = set()
        for label, user in (("address", POLY_ADDRESS), ("funder", POLY_FUNDER)):
            value = str(user or "").strip()
            key = value.lower()
            if not value or key in seen:
                continue
            seen.add(key)
            identities.append((label, value))
        return identities

    def _has_server_claim_for_condition(self, condition_id: str) -> bool:
        cid = str(condition_id or "").strip()
        if not cid:
            return False
        return any(
            record.condition_id == cid and record.status != "expected_pending"
            for record in self.state.claim_records.values()
        )

    def _expected_claim_record_from_position(self, pos: "Position") -> ClaimRecord | None:
        condition_id = str(pos.condition_id or "").strip()
        if not condition_id:
            return None
        expected_amount = self._daily_budget_return_amount(
            status="won",
            amount=pos.amount_usdc,
            entry_price=pos.entry_price,
            pnl=pos.pnl,
        )
        if expected_amount <= 0.0:
            return None
        return ClaimRecord(
            claim_id=self._claim_id_from_positions(condition_id, False),
            condition_id=condition_id,
            asset=str(pos.token_id or ""),
            outcome=str(pos.direction or ""),
            claimable_amount=expected_amount,
            claim_source="local_trade_settlement",
            status="expected_pending",
            last_seen_at=_iso_z(_utc_now()),
            redeemable=False,
            scan_identity="local",
        )

    def _build_claim_candidates(self, positions: list[dict[str, Any]]) -> dict[str, ClaimRecord]:
        grouped: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
        for position in positions:
            if not isinstance(position, dict):
                continue
            condition_id = str(position.get("conditionId", "") or "").strip()
            if not condition_id:
                continue
            claim_id = self._claim_id_from_positions(
                condition_id,
                bool(position.get("negativeRisk", False)),
            )
            identity = str(
                position.get("_claim_scan_identity")
                or position.get("proxyWallet")
                or "_default"
            )
            grouped[claim_id][identity].append(position)

        now_iso = _iso_z(_utc_now())
        settlement_cache = self.state.settlement_registry_cache
        candidates: dict[str, ClaimRecord] = {}
        for claim_id, identity_groups in grouped.items():
            records = max(
                identity_groups.values(),
                key=lambda items: sum(self._claimable_amount_from_position(item) for item in items),
            )
            first = records[0]
            condition_id = str(first.get("conditionId", "") or "").strip()
            settlement = settlement_cache.get(condition_id, {})
            claimable_amount = round(
                sum(self._claimable_amount_from_position(item) for item in records),
                6,
            )
            market_id = str(settlement.get("market_id", "") or first.get("market", "") or "")
            outcomes = [str(item.get("outcome", "") or "").strip() for item in records if item.get("outcome")]
            outcome_indices = [int(item.get("outcomeIndex", -1) or -1) for item in records]
            candidates[claim_id] = ClaimRecord(
                claim_id=claim_id,
                condition_id=condition_id,
                market_id=market_id,
                asset=str(first.get("asset", "") or ""),
                outcome=" / ".join(sorted({item for item in outcomes if item})) or str(first.get("outcome", "") or ""),
                outcome_index=next((idx for idx in outcome_indices if idx >= 0), -1),
                title=str(first.get("title", "") or ""),
                end_date=str(first.get("endDate", "") or ""),
                claimable_amount=claimable_amount,
                claim_source="positions_api_redeemable",
                status="discovered",
                last_seen_at=now_iso,
                redeemable=any(bool(item.get("redeemable", False)) for item in records),
                mergeable=any(bool(item.get("mergeable", False)) for item in records),
                negative_risk=any(bool(item.get("negativeRisk", False)) for item in records),
                proxy_wallet=str(first.get("proxyWallet", "") or ""),
                scan_identity=str(first.get("_claim_scan_identity", "") or ""),
            )
        return candidates

    def _claim_state_changed(self, current: ClaimRecord | None, candidate: ClaimRecord) -> bool:
        if current is None:
            return True
        return any(
            (
                current.status != candidate.status,
                abs(float(current.claimable_amount or 0.0) - float(candidate.claimable_amount or 0.0)) >= 0.01,
                current.attempt_count != candidate.attempt_count,
                current.tx_hash != candidate.tx_hash,
                current.request_id != candidate.request_id,
                current.error_code != candidate.error_code,
                current.error_message != candidate.error_message,
                current.claim_source != candidate.claim_source,
                current.scan_identity != candidate.scan_identity,
                current.last_seen_at != candidate.last_seen_at and candidate.status in ("confirmed", "failed"),
            )
        )

    def _persist_claim_state(self, record: ClaimRecord) -> None:
        current = self.state.claim_records.get(record.claim_id)
        if not self._claim_state_changed(current, record):
            self.state.claim_records[record.claim_id] = record
            self._sync_claim_runtime_counts()
            return

        self.state.claim_records[record.claim_id] = record
        self.state.logger.log_claim_state(record)
        amount_s = f"${record.claimable_amount:.2f}"
        short = f"{record.condition_id[:8]}…" if record.condition_id else record.claim_id[:12]
        if record.status == "queued":
            msg = f"queued {amount_s} ({short})"
            self._append_claim_log(msg)
            self.state.log_event(f"[CLAIM] {msg}")
        elif record.status == "submitted":
            msg = f"submitted {amount_s} ({short})"
            self._append_claim_log(msg)
            self.state.log_event(f"[CLAIM] {msg}")
        elif record.status == "confirmed":
            msg = f"confirmed {amount_s} ({short})"
            self._append_claim_log(msg)
            self.state.log_event(f"[CLAIM] {msg}")
        elif record.status == "failed":
            detail = record.error_code or record.error_message or "unknown"
            msg = f"failed {amount_s} ({short}) {detail}"
            self._append_claim_log(msg)
            self.state.log_event(f"[CLAIM] {msg}")
        elif record.status == "expected_pending":
            msg = f"expected {amount_s} pending ({short})"
            self._append_claim_log(msg)
            self.state.log_event(f"[CLAIM] {msg}")

        self._sync_claim_runtime_counts()
        self._refresh_performance_history()

    def _persist_expected_claim_state(self, record: ClaimRecord) -> bool:
        if record.status != "expected_pending":
            self._persist_claim_state(record)
            return True
        if self._has_server_claim_for_condition(record.condition_id):
            self._sync_claim_runtime_counts()
            return False
        current = self.state.claim_records.get(record.claim_id)
        if current is not None and current.status != "expected_pending":
            self._sync_claim_runtime_counts()
            return False
        changed = self._claim_state_changed(current, record)
        self._persist_claim_state(record)
        return changed or current is None

    def _claim_execution_block_reason(self) -> str:
        if AUTO_CLAIM_LIVE_ONLY and not LIVE_TRADING:
            return "live-only"
        if not AUTO_CLAIM_ENABLED:
            return "discovery-only"
        status_fn = getattr(self.market, "claim_execution_status", None)
        if callable(status_fn):
            supported, detail = status_fn()
            if not supported:
                return detail or "executor-unavailable"
        snapshot = self.market.session_snapshot()
        if bool(snapshot.get("refresh_in_progress")):
            return "session-refreshing"
        if int(snapshot.get("consecutive_auth_failures", 0) or 0) >= 1:
            return "session-degraded"
        return ""

    async def _scan_and_process_claims(self, *, trigger: str) -> None:
        identities = self._claim_scan_identities()
        self.state.claim_last_scan_at = time.time()
        self.state.claim_last_scan_trigger = trigger
        self.state.claim_last_scan_identities = [
            self._claim_scan_label(label, user) for label, user in identities
        ]
        self.state.claim_last_scan_status = "starting"
        self.state.claim_last_scan_error = ""
        self.state.claim_last_scan_candidates = 0
        if not identities:
            self.state.claim_last_scan_status = "skipped"
            self.state.claim_last_scan_error = "POLY_ADDRESS/POLY_FUNDER missing"
            self._sync_claim_runtime_counts()
            return

        positions: list[dict[str, Any]] = []
        api_statuses: list[str] = []
        api_errors: list[str] = []
        for label, user in identities:
            label_s = self._claim_scan_label(label, user)
            try:
                fetched = await self.market.get_current_positions(
                    user=user,
                    redeemable=True,
                    size_threshold=0.0,
                    limit=500,
                )
            except Exception as exc:
                api_statuses.append(f"{label}:exception")
                api_errors.append(f"{label}:{str(exc)[:120]}")
                continue

            snapshot_fn = getattr(self.market, "session_snapshot", None)
            snapshot = snapshot_fn() if callable(snapshot_fn) else {}
            status = str(snapshot.get("last_positions_status", "") or "ok")
            error = str(snapshot.get("last_positions_error", "") or "")
            api_statuses.append(f"{label}:{status}")
            if error:
                api_errors.append(f"{label}:{error[:120]}")

            for item in fetched:
                if not isinstance(item, dict):
                    continue
                annotated = dict(item)
                annotated["_claim_scan_identity"] = label_s
                annotated["_claim_scan_user"] = _mask_address(user)
                positions.append(annotated)

        candidates = self._build_claim_candidates(positions)
        self.state.claim_last_scan_candidates = len(candidates)
        self.state.claim_last_scan_status = ",".join(api_statuses) or "ok"
        self.state.claim_last_scan_error = "; ".join(api_errors)[:240]

        for claim in candidates.values():
            current = self.state.claim_records.get(claim.claim_id)
            if current is None:
                for stale_id, stale in list(self.state.claim_records.items()):
                    if (
                        stale.status == "expected_pending"
                        and stale.condition_id == claim.condition_id
                        and stale_id != claim.claim_id
                    ):
                        self.state.claim_records.pop(stale_id, None)
            if current is not None and current.status in ("confirmed", "submitted"):
                continue

            if claim.claimable_amount < AUTO_CLAIM_THRESHOLD:
                skipped = ClaimRecord(**{
                    **claim.to_record(),
                    "status": "skipped",
                    "error_code": "below_threshold",
                    "error_message": f"claimable {claim.claimable_amount:.2f} below threshold",
                })
                self._persist_claim_state(skipped)
                continue

            queued_at = current.queued_at if current is not None else claim.last_seen_at
            queued = ClaimRecord(**{
                **claim.to_record(),
                "status": "queued",
                "queued_at": queued_at,
                "attempt_count": current.attempt_count if current is not None else 0,
                "last_attempt_at": current.last_attempt_at if current is not None else "",
                "tx_hash": current.tx_hash if current is not None else "",
                "request_id": current.request_id if current is not None else "",
                "error_code": "",
                "error_message": "",
            })
            self._persist_claim_state(queued)

            block_reason = self._claim_execution_block_reason()
            if block_reason:
                continue

            if queued.attempt_count >= AUTO_CLAIM_MAX_RETRIES:
                continue

            submitted = ClaimRecord(**{
                **queued.to_record(),
                "status": "submitted",
                "attempt_count": queued.attempt_count + 1,
                "last_attempt_at": queued.last_seen_at,
            })
            self._persist_claim_state(submitted)
            result = await self.market.claim_position(submitted)
            final = ClaimRecord(**{
                **submitted.to_record(),
                "status": result.status,
                "tx_hash": result.tx_hash or submitted.tx_hash,
                "request_id": result.request_id or submitted.request_id,
                "error_code": result.error_code,
                "error_message": result.error_message,
                "last_attempt_at": submitted.last_attempt_at or submitted.last_seen_at,
            })
            self._persist_claim_state(final)
            if final.status == "confirmed":
                self.state.balance_refresh_event.set()

        self._sync_claim_runtime_counts()
        # Always log scan result so the user can see the claim manager is running,
        # even when no candidates are found (avoids "auto claim seems dead" confusion).
        mode = "enabled" if AUTO_CLAIM_ENABLED else "discovery"
        error_s = f" error={self.state.claim_last_scan_error}" if self.state.claim_last_scan_error else ""
        self.state.log_event(
            f"[CLAIM] scan {trigger} candidates={len(candidates)} "
            f"claimable=${self.state.claimable_total:.2f} "
            f"pending=${self.state.expected_claimable_total:.2f} "
            f"mode={mode} status={self.state.claim_last_scan_status}{error_s}"
        )
        self._refresh_performance_history()

    async def _claim_manager_loop(self) -> None:
        await self._scan_and_process_claims(trigger="startup")
        while self.state.running:
            triggered = False
            try:
                await asyncio.wait_for(
                    self.state.market_resolved_event.wait(),
                    timeout=AUTO_CLAIM_SCAN_INTERVAL_S,
                )
                triggered = self.state.market_resolved_event.is_set()
            except asyncio.TimeoutError:
                triggered = False
            if triggered:
                self.state.market_resolved_event.clear()
            await self._scan_and_process_claims(
                trigger="market_resolved" if triggered else "scheduled"
            )

    # ── Balance loop ──────────────────────────────────────────────────────────

    async def _balance_loop(self) -> None:
        while self.state.running:
            bal = await self.market.get_balance()
            if bal > 0:
                self.state.balance_usdc = bal
            try:
                await asyncio.wait_for(
                    self.state.balance_refresh_event.wait(),
                    timeout=120,
                )
            except asyncio.TimeoutError:
                pass
            self.state.balance_refresh_event.clear()

    async def _refresh_polymarket_session(self, reason: str) -> bool:
        ok, detail = await self.market.refresh_session()
        snapshot = self.market.session_snapshot()
        if ok:
            self.state.log_event(
                f"[CREDS] Polymarket session refreshed reason={reason} "
                f"gen={snapshot.get('generation', 0)}"
            )
        else:
            suffix = f" ({detail})" if detail else ""
            self.state.log_event(
                f"[CREDS] Polymarket session refresh failed reason={reason}{suffix}"
            )
        self._refresh_performance_history()
        return ok

    async def _polymarket_heartbeat_loop(self) -> None:
        if not LIVE_TRADING:
            while self.state.running:
                await asyncio.sleep(300)
            return

        while self.state.running:
            ok = await self.market.send_heartbeat()
            if not ok:
                snapshot = self.market.session_snapshot()
                detail = snapshot.get("last_auth_error") or "heartbeat failed"
                self.state.log_event(f"[HEARTBEAT] failed: {detail}")
                if snapshot.get("consecutive_auth_failures", 0) >= 1:
                    await self._refresh_polymarket_session("heartbeat_failed")
            await asyncio.sleep(HEARTBEAT_INTERVAL_S)

    async def _polymarket_auth_health_loop(self) -> None:
        if not self.market.can_refresh_credentials():
            while self.state.running:
                await asyncio.sleep(300)
            return

        while self.state.running:
            await asyncio.sleep(POLY_AUTH_HEALTHCHECK_INTERVAL_S)
            ok, detail = await self.market.auth_health_check()
            if ok:
                continue
            self.state.log_event(f"[AUTH] Polymarket auth probe failed: {detail or 'unknown'}")
            refreshed = await self._refresh_polymarket_session("auth_probe_failed")
            if not refreshed:
                snapshot = self.market.session_snapshot()
                failures = int(snapshot.get("consecutive_auth_failures", 0) or 0)
                if failures >= POLY_FATAL_SESSION_FAILURES:
                    self.state.log_event(
                        f"[AUTH] session remains degraded after {failures} auth failure(s)"
                    )

    # ── Credential refresh loop ───────────────────────────────────────────────

    async def _creds_refresh_loop(self) -> None:
        """Re-derive Polymarket L2 session credentials from POLY_ETH_PRIVATE_KEY.

        Polymarket sessions expire roughly every 24 hours. This loop refreshes
        them every 23 hours so the bot never hits an expired-session error.
        On failure it retries every hour until success.
        """
        if not self.market.can_refresh_credentials():
            while self.state.running:
                await asyncio.sleep(300)
            return

        await asyncio.sleep(POLY_CREDS_REFRESH_INTERVAL_S)
        while self.state.running:
            ok = await self._refresh_polymarket_session("scheduled")
            if ok:
                await asyncio.sleep(POLY_CREDS_REFRESH_INTERVAL_S)
            else:
                await asyncio.sleep(POLY_CREDS_REFRESH_RETRY_S)


# ══════════════════════════════════════════════════════════════════════════════
# Source: main.py
# ══════════════════════════════════════════════════════════════════════════════

"""Entry point — Rich Live terminal UI + asyncio bot runner."""

import argparse
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
    # main splits into left_stack (existing panels) and right-side history/prices.
    layout["main"].split_row(
        Layout(name="left_stack", ratio=2),
        Layout(name="price_stack", ratio=1),
    )
    layout["price_stack"].split_column(
        Layout(name="bet_history", size=14),
        Layout(name="price_log"),
    )
    layout["left_stack"].split_column(
        Layout(name="body", size=33),
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
        Layout(name="signal",       size=10),
    )
    layout["right"].split_column(
        Layout(name="positions", size=6),
        Layout(name="results",   size=18),
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
        "SIGNAL_QUERY", "SIGNAL_DONE", "BUY_READY", "DECISION_SKIP", "ORDER_OPEN", "ORDER_FAILED", "ALREADY_ATTEMPTED",
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
    elif phase == "SIGNAL_QUERY":
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
    hl_price_s = f"${state.hl_btc_price:,.2f}" if state.hl_btc_price else "—"
    hl_ws_s    = "[bold green]OK[/bold green]" if state.hl_ws_ok else "[bold red]ERR[/bold red]"
    t.add_row("HL BTC", f"[bold white]{hl_price_s}[/bold white]  WS: {hl_ws_s}")
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
    ml_status = state.model_activation_status
    is_fallback = ml_status.active_signal_source != "ml"

    if sig is None:
        if is_fallback:
            body = Text.from_markup(
                "[bold yellow]⚠ ML ENGINE: FALLBACK HEURISTIC ACTIVE[/bold yellow]\n"
                "[dim]No trained model loaded — labels may be biased by oracle divergence[/dim]\n"
                "[dim]No signal yet[/dim]"
            )
        else:
            body = Text("No signal yet", style="dim")
        return Panel(body, title="[bold cyan]LAST SIGNAL[/bold cyan]", border_style="blue")

    if sig.signal == "BUY_UP":
        sig_text = "[bold bright_green]BUY_UP[/bold bright_green]"
    elif sig.signal == "BUY_DOWN":
        sig_text = "[bold bright_red]BUY_DOWN[/bold bright_red]"
    else:
        sig_text = "[bold yellow]SKIP[/bold yellow]"

    source = getattr(sig, "source", "unknown")
    conf = getattr(sig, "confidence", 0.0)
    probs = f"U={getattr(sig, 'prob_up', 0.5):.0%} D={getattr(sig, 'prob_down', 0.5):.0%}"
    fallback_line = "\n[bold yellow]⚠ FALLBACK HEURISTIC[/bold yellow] [dim](no active ML model)[/dim]" if is_fallback else ""
    body = Text.from_markup(f"{sig_text}\n[white]{conf:.0%}[/white] [dim]{source} {probs}[/dim]{fallback_line}")
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
    pnl_sign = "+" if state.total_pnl >= 0 else "-"
    pnl_s = f"{pnl_sign}${abs(state.total_pnl):.2f}"
    last_claim = state.claim_log[-1] if state.claim_log else f"– nothing to claim"
    resolved_pending = len([p for p in state.positions if p.status == "open"])
    claim_mode = "[green]EXEC[/green]" if AUTO_CLAIM_ENABLED else "[yellow]DISCOVERY[/yellow]"
    scan_bits = []
    if state.claim_last_scan_candidates or state.claim_last_scan_at:
        scan_bits.append(f"scan={state.claim_last_scan_candidates}")
    if state.claim_last_scan_at:
        scan_age = max(0, int(time.time() - state.claim_last_scan_at))
        scan_bits.append(f"{scan_age}s")
    if state.claim_last_scan_status:
        scan_bits.append(str(state.claim_last_scan_status)[:30])
    if state.claim_last_scan_error:
        scan_bits.append("err")
    if state.claim_last_scan_identities:
        scan_bits.append("ids=" + "/".join(state.claim_last_scan_identities)[:34])
    scan_s = ("  " + " ".join(scan_bits)) if scan_bits else ""
    _thr_s = f"  thr=${AUTO_CLAIM_THRESHOLD:.2f}" if AUTO_CLAIM_THRESHOLD > 0 else ""
    claim_summary = (
        f"{claim_mode}  amt=[white]${state.claimable_total:.2f}[/white]"
        f"  pending=[yellow]${state.expected_claimable_total:.2f}[/yellow]"
        f"  p=[white]{state.pending_claim_count}[/white]"
        f"  ok=[green]{state.claimed_today_count}[/green]"
        f"  fail=[red]{state.failed_today_count}[/red]"
        f"{_thr_s}{scan_s}"
    )
    show_claim_log = bool(state.claim_log) and "nothing to claim" not in last_claim.lower()

    t = Table.grid(padding=(0, 1))
    t.add_column(style="cyan", width=12)
    t.add_column()

    t.add_row("Balance",   f"[bold white]$  {state.balance_usdc:.2f} USDC[/bold white]")
    if DAILY_BUDGET_USDC > 0:
        budget_used = state.daily_budget_spent_usdc - state.daily_budget_returned_usdc
        remaining = DAILY_BUDGET_USDC - budget_used   # can exceed limit after profitable returns
        if state.daily_halted:
            budget_s = f"[bold red]HALTED — cash used ${budget_used:.2f} hit limit ${DAILY_BUDGET_USDC:.2f}[/bold red]"
        else:
            bud_color = "green" if remaining >= DAILY_BUDGET_USDC else ("yellow" if remaining > 0 else "red")
            budget_s = (
                f"spent=[red]${state.daily_budget_spent_usdc:.2f}[/red]  "
                f"returned=[green]${state.daily_budget_returned_usdc:.2f}[/green]  "
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

    t.add_row("Claims",    claim_summary)
    if show_claim_log:
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
    pnl_breakdown = (
        f"  [dim](wins [green]+${state.total_gross_wins:.2f}[/green]"
        f"  losses [red]-${state.total_gross_losses:.2f}[/red])[/dim]"
    )
    t.add_row("Net Profit", f"[{pnl_color}]{pnl_s}[/{pnl_color}]{pnl_breakdown}")

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
        elif any(k in msg for k in ("[DECISION]", "[SIGNAL]", "[LAST-MIN]")):
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
        "SIGNAL_DONE": "cyan",
        "SIGNAL_QUERY": "cyan",
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
    ml_status = state.model_activation_status
    is_fallback = ml_status.active_signal_source != "ml"
    ml_line = (
        "\n[bold yellow]⚠ ML: FALLBACK HEURISTIC ACTIVE[/bold yellow] [dim](oracle divergence risk)[/dim]"
        if is_fallback else ""
    )
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
        f"{ml_line}"
    )
    return Panel(body, title="[bold cyan]ENGINE[/bold cyan]", border_style="blue")


def render_bet_history(state: BotState) -> Panel:
    entries = list(state.trade_history)[:10]
    if not entries:
        body = Text("No settled bets yet", style="dim")
        return Panel(body, title="[bold cyan]BET HISTORY[/bold cyan]", border_style="blue")

    _WIB = timezone(timedelta(hours=7))
    table = Table(show_header=True, header_style="cyan", box=None, padding=(0, 1))
    table.add_column("Time", width=6)
    table.add_column("WIB", width=6)
    table.add_column("Dir", width=5)
    table.add_column("Amount", width=8, justify="right")
    table.add_column("P/L", width=8, justify="right")
    table.add_column("Status", width=7)

    for entry in entries:
        direction = entry.direction.upper()
        dir_color = "green" if direction == "UP" else "red" if direction == "DOWN" else "white"
        pnl_color = "green" if entry.pnl > 0 else "red" if entry.pnl < 0 else "white"
        pnl_s = f"+${entry.pnl:.2f}" if entry.pnl >= 0 else f"-${abs(entry.pnl):.2f}"
        status = entry.status.lower()
        status_label = "WIN" if status == "won" else "LOSE" if status == "lost" else status.upper()
        status_color = "green" if status == "won" else "red" if status == "lost" else "white"
        wib_time = entry.closed_at.astimezone(_WIB).strftime("%H:%M")

        table.add_row(
            entry.closed_at.strftime("%H:%M"),
            wib_time,
            f"[{dir_color}]{direction}[/{dir_color}]",
            f"${entry.amount_usdc:.2f}",
            f"[{pnl_color}]{pnl_s}[/{pnl_color}]",
            f"[{status_color}]{status_label}[/{status_color}]",
        )

    return Panel(table, title="[bold cyan]BET HISTORY[/bold cyan]", border_style="blue")


def _trade_history_key(entry: TradeHistoryEntry) -> str:
    if entry.order_id:
        return entry.order_id
    return ":".join([
        entry.condition_id,
        entry.direction,
        entry.closed_at.isoformat(),
    ])


def _trade_history_signature(entry: TradeHistoryEntry) -> tuple:
    return (
        _trade_history_key(entry),
        entry.direction,
        round(entry.amount_usdc, 8),
        round(entry.pnl, 8),
        entry.status,
        entry.closed_at.isoformat(),
        entry.simulated,
    )


def refresh_trade_history_from_logs(state: BotState, *, force: bool = False) -> int:
    now_ts = time.time()
    if not force and now_ts - state.trade_history_last_refresh_at < TRADE_HISTORY_REFRESH_S:
        return 0
    state.trade_history_last_refresh_at = now_ts

    try:
        loaded = state.logger.load_recent_trade_history(
            limit=state.trade_history.maxlen or 20
        )
    except Exception:
        return 0

    if not loaded:
        return 0

    maxlen = state.trade_history.maxlen or 20
    merged: dict[str, TradeHistoryEntry] = {
        _trade_history_key(entry): entry
        for entry in list(state.trade_history)
    }
    for entry in loaded:
        merged[_trade_history_key(entry)] = entry

    latest = sorted(merged.values(), key=lambda entry: entry.closed_at, reverse=True)[:maxlen]
    before = [_trade_history_signature(entry) for entry in state.trade_history]
    after = [_trade_history_signature(entry) for entry in latest]
    if before != after:
        state.trade_history.clear()
        state.trade_history.extend(latest)
    return len(loaded)


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
        refresh_trade_history_from_logs(state)
        layout["bet_history"].update(render_bet_history(state))
        layout["price_log"].update(render_price_log(state))
        await asyncio.sleep(UI_REFRESH_S)


# ── Entry point ───────────────────────────────────────────────────────────────

async def run_bot() -> None:
    # Validate config
    missing = validate_config()
    if missing:
        console = Console()
        console.print(f"[bold red]ERROR:[/bold red] Missing environment variables:")
        for k in missing:
            console.print(f"  • {k}")
        console.print("\nPlease fill in [cyan].env[/cyan] and restart.")
        sys.exit(1)

    mode_msg = "PAPER TRADING (simulated execution)" if not LIVE_TRADING else "LIVE TRADING ENABLED"
    Console().print(f"[bold yellow]{mode_msg}[/bold yellow]")

    bot    = TradingBot()
    layout = build_layout()

    with Live(layout, refresh_per_second=2, screen=True):
        await asyncio.gather(
            bot.run(),
            update_ui(layout, bot.state),
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Polymarket BTC trade bot with ML signal engine")
    subparsers = parser.add_subparsers(dest="command")

    train_parser = subparsers.add_parser("train-ml", help="Train the XGBoost outcome model from logs")
    train_parser.add_argument("--min-rows", type=int, default=ML_MIN_TRAIN_ROWS)
    train_parser.add_argument("--min-windows", type=int, default=ML_MIN_TRAIN_WINDOWS)
    train_parser.add_argument(
        "--promotion-state",
        choices=["shadow", "assist", "active"],
        default=ML_PROMOTION_STATE,
    )

    label_parser = subparsers.add_parser("label-ml", help="Backfill missing ML label files from price logs")
    label_parser.add_argument("--log-dir", default="logs")

    promote_parser = subparsers.add_parser("promote-ml", help="Switch the active model version or promotion stage")
    promote_parser.add_argument("--version", default="latest")
    promote_parser.add_argument(
        "--state",
        choices=["shadow", "assist", "active"],
        default="active",
    )

    args = parser.parse_args()

    try:
        if args.command == "train-ml":
            appended = backfill_ml_labels("logs")
            try:
                result = train_outcome_model(
                    log_dir="logs",
                    models_dir=ML_MODELS_DIR,
                    promotion_state=args.promotion_state,
                    min_rows=args.min_rows,
                    min_distinct_windows=args.min_windows,
                )
                result = auto_apply_trained_model(
                    result,
                    ModelRegistry(ML_MODELS_DIR),
                    auto_promote=ML_AUTO_PROMOTE,
                    fallback_state=args.promotion_state,
                    activation_reason="cli_train",
                )
            except Exception as exc:
                Console().print(f"[red]train-ml failed[/red] {exc}")
                sys.exit(1)
            else:
                manifest = result["manifest"]
                metrics = result["metrics"]
                Console().print(
                    f"[green]trained[/green] {manifest['model_version']} "
                    f"state={manifest['promotion_state']} "
                    f"rows={metrics.get('rows_total', 0)} "
                    f"windows={metrics.get('distinct_windows_total', 0)} "
                    f"ap={metrics.get('auc_pr', 0.0):.3f} "
                    f"cv_ap={metrics.get('cv_auc_pr_mean', 0.0):.3f} "
                    f"ev={metrics.get('policy_metrics', {}).get('realized_ev_per_trade', 0.0):+.2f} "
                    f"labels_backfilled={appended}"
                )
        elif args.command == "label-ml":
            appended = backfill_ml_labels(args.log_dir)
            Console().print(f"[green]labels_backfilled[/green] {appended}")
        elif args.command == "promote-ml":
            registry = ModelRegistry(ML_MODELS_DIR)
            manifest = registry.set_active_version(
                args.version,
                promotion_state=args.state,
                activation_reason="cli_promote",
            )
            if manifest is None:
                Console().print("[red]no model version found to promote[/red]")
                sys.exit(1)
            Console().print(
                f"[green]active_model[/green] {manifest.model_version} state={manifest.promotion_state}"
            )
        else:
            asyncio.run(run_bot())
    except KeyboardInterrupt:
        Console().print("\n[yellow]Bot stopped.[/yellow]")
