# AI Polybot Trader

An autonomous trading bot for Polymarket **Bitcoin Up/Down 5-minute prediction markets**. It streams live BTC prices from Binance, computes technical indicators, passes all context to an AI model (Grok via OpenRouter), and places fractional-Kelly-sized orders through the Polymarket CLOB — all within a Rich terminal UI showing live filters, odds, positions, and P&L.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [System Boot Flow](#2-system-boot-flow)
3. [Concurrent Async Loops](#3-concurrent-async-loops)
4. [Data Sources](#4-data-sources)
   - [BTC Price Feed (Binance WS)](#41-btc-price-feed-binance-ws)
   - [Price Sampler (5-second bars)](#42-price-sampler-5-second-bars)
   - [Polymarket Market Discovery](#43-polymarket-market-discovery)
   - [Live Odds (REST + WebSocket)](#44-live-odds-rest--websocket)
5. [Market Structure](#5-market-structure)
6. [Technical Indicators](#6-technical-indicators)
   - [F1 — RSI(14)](#61-f1--rsi14)
   - [F2 — MA Crossover (MA5/MA20)](#62-f2--ma-crossover-ma5ma20)
   - [F3 — Momentum (10-tick ROC)](#63-f3--momentum-10-tick-roc)
   - [F4 — Odds Edge](#64-f4--odds-edge)
   - [F5 — Entry Timing](#65-f5--entry-timing)
   - [MACD (12,26,9)](#66-macd-12269)
   - [Bollinger Bands (20,2)](#67-bollinger-bands-202)
   - [CVD — Cumulative Volume Delta](#68-cvd--cumulative-volume-delta)
   - [VWAP](#69-vwap)
7. [Signal Alignment Score](#7-signal-alignment-score)
8. [Decision Pipeline](#8-decision-pipeline)
   - [Phase 1 — Filter Monitoring](#81-phase-1--filter-monitoring)
   - [Phase 2 — Gold Zone Entry (elapsed ≥ 180s)](#82-phase-2--gold-zone-entry-elapsed--180s)
   - [Pre-AI Market Gates](#83-pre-ai-market-gates)
   - [AI Signal (Grok via OpenRouter)](#84-ai-signal-grok-via-openrouter)
   - [Post-AI Gates](#85-post-ai-gates)
9. [Position Sizing — Fractional Kelly](#9-position-sizing--fractional-kelly)
10. [Order Placement and Post-Order Cancel](#10-order-placement-and-post-order-cancel)
11. [Position Resolution](#11-position-resolution)
12. [Blocked Window Tracking](#12-blocked-window-tracking)
13. [Daily Risk Controls](#13-daily-risk-controls)
14. [Logging](#14-logging)
15. [Terminal UI Layout](#15-terminal-ui-layout)
16. [Configuration Reference](#16-configuration-reference)
17. [Setup and Running](#17-setup-and-running)

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│  main.py  — asyncio entry point + Rich Live terminal UI             │
└────────────────────┬────────────────────────────────────────────────┘
                     │ runs
┌────────────────────▼────────────────────────────────────────────────┐
│  TradingBot (bot.py)                                                 │
│                                                                      │
│  btc_feed ──► price_sampler ──► price_history_5s / CVD / VWAP       │
│  market_loop ──► find_active_window() ──► WindowInfo                │
│  odds_ws_loop ──► real-time odds from Polymarket WS                 │
│  trading_loop ──► indicators ──► DecisionMaker ──► AIAgent          │
│                              └──► place_bet()                       │
│  position_monitor_loop ──► should_cancel() ──► cancel_order()       │
│  results_loop ──► _check_positions() ──► _settle_position()         │
│  balance_loop ──► get_balance()                                     │
│  creds_refresh_loop ──► refresh_credentials()                       │
└─────────────────────────────────────────────────────────────────────┘
         │              │              │
  BTCFeed          MarketClient    AIAgent
  (btc_feed.py)   (market_client) (ai_agent.py)
  Binance WS       Polymarket      OpenRouter /
  BTC/USDC         CLOB + Gamma    Grok model
```

---

## 2. System Boot Flow

```
main.py
 └─ validate_config()
 └─ build_layout()  → Rich UI panels
 └─ TradingBot()
      └─ BotState()         # shared state dataclass
      └─ BTCFeed(state)
      └─ MarketClient()
      └─ AIAgent()
      └─ TelegramNotifier()
      └─ DecisionMaker()
 └─ asyncio.gather(all loops)   # 9 coroutines run concurrently
 └─ Rich Live refresh every UI_REFRESH_S
```

---

## 3. Concurrent Async Loops

| Loop | File | Purpose |
|---|---|---|
| `btc_feed.run` | `btc_feed.py` | Stream raw BTC/USDC ticks from Binance WS (~10/s) |
| `_price_sampler` | `bot.py` | Downsample to one tick per 5s; compute CVD per period |
| `_market_loop` | `bot.py` | Poll Polymarket Gamma API every 5s to find active window |
| `_odds_ws_loop` | `bot.py` | Subscribe Polymarket market WS for real-time odds |
| `_trading_loop` | `bot.py` | Compute indicators; execute bets in the gold zone |
| `_position_monitor_loop` | `bot.py` | Watch open live orders; cancel if conditions worsen |
| `_results_loop` | `bot.py` | Settle resolved positions; evaluate blocked windows |
| `_balance_loop` | `bot.py` | Refresh USDC balance every 2 minutes |
| `_creds_refresh_loop` | `bot.py` | Re-derive Polymarket L2 API creds every 23 hours |

All loops are wrapped in `safe_loop()`, which catches exceptions, logs them, and retries after 5 seconds — so a single failure in one loop never crashes the bot.

---

## 4. Data Sources

### 4.1 BTC Price Feed (Binance WS)

**File:** `btc_feed.py`  
**Endpoint:** `wss://stream.binance.com:9443/ws/btcusdc@trade`

- **Why USDC, not USDT?** USDC is 1:1 redeemable for USD, so its price matches the Chainlink BTC/USD oracle that Polymarket uses for resolution. USDT carries a ~0.07% premium (~$50 at $69k BTC) which would skew beat-price comparisons.
- Each raw trade tick contains `p` (price), `T` (timestamp ms), `q` (BTC quantity), and `m` (maker side).
- The `m` field distinguishes buyer-initiated vs seller-initiated trades for CVD:
  - `m=False` → buyer is aggressor → **buy volume**
  - `m=True` → seller is aggressor → **sell volume**
- Stores into `state.price_history` (raw deque, 300 ticks) and `state.price_history_ts` (timestamped, 1200 ticks) for beat-price lookup.

### 4.2 Price Sampler (5-second bars)

**Loop:** `_price_sampler` in `bot.py`

Every 5 seconds:
1. Appends `btc_price` to `price_history_5s` (max 300 = 25 minutes).
2. Snapshots and resets `_tick_buy_vol` / `_tick_sell_vol` accumulators.
3. Computes running CVD: `cvd[t] = cvd[t-1] + buy_vol[t] − sell_vol[t]`.
4. Appends to `buy_vol_5s`, `sell_vol_5s`, `cvd_5s` (all maxlen 300).
5. Persists to `logs/prices_YYYY-MM-DD.jsonl`.

**Why 5-second bars?** Raw ticks at 10/s make MA5 meaningful for only 0.5 seconds. At 5-second resolution: MA5 ≈ 25s, MA20 ≈ 100s, momentum ≈ 50s — all sensible for a 5-minute binary window.

### 4.3 Polymarket Market Discovery

**File:** `market_client.py → find_active_window()`  
**API:** `https://gamma-api.polymarket.com/events/slug/{slug}`

Polymarket BTC Up/Down 5-minute windows use the slug pattern `btc-updown-5m-{unix_ts}` where `unix_ts` is the exact window start time (always a multiple of 300 seconds).

The bot probes three candidate timestamps (current 300s boundary, −300s, +300s) and returns the one where `start_time ≤ now ≤ end_time`.

**Beat price extraction:**  
The "beat price" is the BTC/USD level that determines the Up/Down outcome. It is:
1. Parsed from the market question text ("Will BTC be above $X?").
2. If parsing fails: looked up from `price_history_ts` for the tick closest to `win.start_time` (within 60s).
3. Final fallback: current `btc_price`.

This careful lookup avoids a ~$20–35 error caused by bot detection latency plus BTC movement since window open.

### 4.4 Live Odds (REST + WebSocket)

**REST fallback:** `GET https://clob.polymarket.com/midpoint?token_id=...` — polled every 5s by `_market_loop`.  
**WebSocket primary:** `wss://ws-subscriptions-clob.polymarket.com/ws/market` — pushed in real-time by `_odds_ws_loop`.

The WebSocket subscription message requests `event_type` updates of `price_change`, `book`, and `last_trade_price`. On each message, the mid-price for both the Up and Down token IDs is updated in `state.up_odds` / `state.down_odds`.

The REST update is skipped if it returns the error-fallback value `0.500 / 0.500` to avoid overwriting valid WS data.

---

## 5. Market Structure

Each **Bitcoin Up/Down 5-minute** window is a binary prediction market:

| Field | Value |
|---|---|
| Duration | 300 seconds (5 minutes) |
| Outcome | Is BTC/USD **above** or **below** the beat price at expiry? |
| Resolution source | Chainlink BTC/USD oracle on Polygon |
| Tokens | `up_token_id` (Yes = UP), `down_token_id` (No = DOWN) |
| Odds range | 0.00 – 1.00 (implied probability; payout = 1/odds) |
| Order type | FOK market order (Fill or Kill via `py_clob_client`) |

The bot looks up `condition_id` (32-byte hex market identifier), `up_token_id`, and `down_token_id` from the Gamma API JSON, then places orders directly through the CLOB.

---

## 6. Technical Indicators

**File:** `indicators.py`  
**Input:** `price_history_5s` (5-second sampled prices), `buy_vol_5s`, `sell_vol_5s`, `cvd_5s`

All indicator functions are **pure** (no I/O, no state, no exceptions). They are computed in `run_all_filters()` and bundled into an `IndicatorSnapshot`.

### 6.1 F1 — RSI(14)

**Function:** `compute_rsi(prices, period=14)`  
**Formula:** Wilder's RSI using NumPy:

```
gains_avg  = mean(positive deltas over last 14 bars)
losses_avg = mean(negative deltas over last 14 bars)
RS  = gains_avg / losses_avg
RSI = 100 − (100 / (1 + RS))
```

**Direction vote:**
- RSI < 45 → **UP** (oversold)
- RSI > 55 → **DOWN** (overbought)
- 45–55 → NONE (neutral)

**Gate behavior:** F1 **passes** whenever RSI can be computed (≥15 bars = 75s of history). It is a data-readiness check, not a blocking gate. RSI has the lowest weight of all indicators — 14 bars at 5s intervals = only ~70s of data, not enough for meaningful overbought/oversold on a 5-minute market.

**Minimum data needed:** 15 bars (75 seconds after bot start).

---

### 6.2 F2 — MA Crossover (MA5/MA20)

**Function:** `compute_ma(prices, period)`  
**Formula:** Simple Moving Average of the last N prices.

```
MA5  = mean(last 5 prices)   ≈ 25-second trend
MA20 = mean(last 20 prices)  ≈ 100-second trend
diff_pct = |MA5 − MA20| / MA20 × 100
```

**Direction vote:**
- MA5 > MA20 → **UP** (bullish crossover)
- MA5 < MA20 → **DOWN** (bearish crossover)

**Gate behavior:** F2 **passes** when `diff_pct > 0.01%` (MAs are not flat). Fails when the two averages are essentially equal ("flat market").

**Minimum data needed:** 20 bars (100 seconds).

---

### 6.3 F3 — Momentum (10-tick ROC)

**Function:** `compute_momentum(prices, ticks=10)`  
**Formula:** Rate of Change over 10 bars (50 seconds):

```
momentum_pct = (prices[-1] - prices[-11]) / prices[-11] × 100
```

**Direction vote:**
- momentum > 0 → **UP**
- momentum < 0 → **DOWN**

**Gate behavior:** F3 **passes** when `|momentum| > 0.01%`. Captures any meaningful price drift.

**Minimum data needed:** 11 bars (55 seconds).

---

### 6.4 F4 — Odds Edge

**Function:** `check_f4_odds_edge(up_odds, down_odds)`

Checks whether the market shows a **clear but not extreme** directional lean.

**Logic:**

```
if up_odds >= MAX_BET_ODDS (0.82) or down_odds >= MAX_BET_ODDS:
    FAIL — "too extreme, no payout"

min_lean = 0.5 + MIN_ODDS_EDGE (0.52)
if max(up_odds, down_odds) < min_lean:
    FAIL — "near 50/50, coin-flip"

if up_odds >= 0.52:   PASS, direction = UP
if down_odds >= 0.52: PASS, direction = DOWN
```

**Why this filter matters:** An odds of 0.82 means the market is 82% sure — you'd earn only 22 cents per dollar wagered (1/0.82 − 1). The edge is already priced in. Conversely, 50/50 markets have no crowd signal to follow.

---

### 6.5 F5 — Entry Timing

**Function:** `check_f5_window_timing(elapsed_s)`

**Gate behavior:** Passes when `0 ≤ elapsed_s < MAX_ENTRY_S (270)`.

This is a hard time gate. Even if all other filters pass, F5 prevents entries with less than ~30 seconds remaining — order latency makes fills unreliable this late.

> Note: The actual **bet execution** is stricter than F5 — bets only fire in the Gold Zone (`elapsed_s ≥ 180`). F5 exists to keep the UI honest about the entry window.

---

### 6.6 MACD (12,26,9)

**Function:** `compute_macd(prices, fast=12, slow=26, signal_period=9)`

Computed on **5-second bars**:
- Fast EMA: 12 bars → 60-second trend
- Slow EMA: 26 bars → 130-second trend
- Signal line: 9-bar EMA of the MACD line → 45-second smoothing

```
EMA(n)[t] = price[t] × k + EMA(n)[t-1] × (1 − k)   where k = 2/(n+1)

MACD line  = EMA(12) − EMA(26)
Signal line = EMA(9) of MACD line
Histogram   = MACD line − Signal line
```

**Minimum data needed:** 26 + 9 = 35 bars (175 seconds ≈ 3 minutes).

**Direction vote:**
- Histogram > 0 → **UP** (bullish momentum)
- Histogram < 0 → **DOWN** (bearish momentum)

MACD does not gate the trade; it contributes one vote to the [Signal Alignment Score](#7-signal-alignment-score) and is passed to the AI as a ★★★★ indicator.

---

### 6.7 Bollinger Bands (20,2)

**Function:** `compute_bollinger_bands(prices, period=20, std_mult=2.0)`

Computed on **5-second bars** (20 bars = 100-second lookback):

```
middle    = mean(last 20 prices)
std       = stddev(last 20 prices, ddof=0)
upper     = middle + 2 × std
lower     = middle − 2 × std
bandwidth = (upper − lower) / middle
pct_b     = (price − lower) / (upper − lower)
```

**Minimum data needed:** 20 bars (100 seconds).

**Interpretation for `pct_b`:**
| %B range | Label | Implication |
|---|---|---|
| > 0.90 | Near upper band | Overbought → fade DOWN |
| < 0.10 | Near lower band | Oversold → fade UP |
| 0.45–0.55 | Mid band | Neutral |

> Bollinger Bands are used as a **mean-reversion context** indicator — NOT as a bet trigger in the gold zone (elapsed ≥ 120s), where momentum is more reliable than reversion.

---

### 6.8 CVD — Cumulative Volume Delta

**Functions:** `compute_cvd_divergence(cvd_series, prices, lookback=8)`

CVD accumulates the net difference between buy and sell volume over each 5-second period:

```
CVD[t] = CVD[t-1] + buy_vol[t] − sell_vol[t]
```

Buy/sell classification comes from the Binance `m` (maker) field — a buyer-initiated trade adds volume; a seller-initiated trade subtracts it.

**Divergence detection** over the last 8 bars (40 seconds):

```
price_change = prices[-1] − prices[-8]
cvd_change   = cvd[-1]    − cvd[-8]

Filters: |price_change| ≥ $2 AND |cvd_change| ≥ 0.05 BTC

BULLISH: price_change < 0 AND cvd_change > 0
  → Price fell but buyers dominated = hidden accumulation → lean UP

BEARISH: price_change > 0 AND cvd_change < 0
  → Price rose but sellers dominated = distribution → lean DOWN

NONE: no divergence detected
```

**Why CVD is ★★★★:** It reveals what "smart money" is actually doing beneath the visible price move. A sustained price drop without sell volume dominance often means large players are accumulating — a strong reversal signal.

---

### 6.9 VWAP

**Function:** `compute_vwap(prices, buy_vols, sell_vols)`

Volume-Weighted Average Price using all available 5-second aggregated data:

```
VWAP = Σ(price[i] × total_vol[i]) / Σ(total_vol[i])
```

Where `total_vol[i] = buy_vol[i] + sell_vol[i]`.

**Interpretation:**
- Price > VWAP → trading above institutional fair value → bearish lean (overbought)
- Price < VWAP → trading below fair value → bullish lean (oversold)

Used in combination with RSI for the RSI+VWAP mean-reversion strategy passed to the AI.

---

## 7. Signal Alignment Score

`signal_alignment` counts how many of **6 directional votes** agree with the consensus direction.

| Vote source | Weight | Basis |
|---|---|---|
| F1 RSI direction | 1 | RSI < 45 → UP, > 55 → DOWN |
| F2 MA crossover direction | 1 | MA5 > MA20 → UP, else DOWN |
| F3 Momentum direction | 1 | momentum > 0 → UP, else DOWN |
| F4 Odds edge direction | 1 | leading odds side |
| MACD histogram direction | 1 | histogram > 0 → UP, else DOWN |
| CVD divergence direction | 1 | BULLISH → UP, BEARISH → DOWN |

```python
up_votes   = count(votes == "UP")
down_votes = count(votes == "DOWN")

if up_votes > down_votes:   consensus = "UP",   alignment = up_votes
elif down_votes > up_votes: consensus = "DOWN",  alignment = down_votes
else:                       consensus = "NONE",  alignment = 0
```

**Interpretation:**

| Score | Meaning | AI guidance |
|---|---|---|
| 5–6 / 6 | ★★★ Very strong consensus | High confidence allowed |
| 4 / 6 | ★★ Good consensus | Solid bet |
| 3 / 6 | Moderate | Confirm with gap math |
| 2 / 6 | Weak | Only bet on clear gap math |
| ≤ 1 / 6 | Conflicting | Prefer SKIP |

---

## 8. Decision Pipeline

### 8.1 Phase 1 — Filter Monitoring

Runs every `SIGNAL_COOLDOWN_S` (1 second) throughout the entire 5-minute window. Computes all indicators and updates `state.indicator_snapshot` for the UI. **No AI call, no bet.**

### 8.2 Phase 2 — Gold Zone Entry (elapsed ≥ 180s)

The bot only places bets in the **Gold Zone**: the final ~2 minutes of each window (`elapsed_s ≥ GOLD_ZONE_START_S = 180`).

**Rationale:** BTC needs time to establish a direction. Entering at 180s means:
- 3 minutes of data exist for indicators to be meaningful.
- ~2 minutes remain — enough for the position to resolve without being too late for order latency.
- Market odds often **lag** BTC's actual price position by 15–30 seconds in this window, creating brief mispricings.

The execution also requires `seconds_remaining ≥ LAST_MIN_SECONDS_GUARD (8s)` to account for order latency.

### 8.3 Pre-AI Market Gates

**File:** `decision_maker.py → DecisionMaker.pre_ai_check()`

These gates run **before** the AI is queried, saving API latency on obvious skips.

| Gate | Condition | Trigger |
|---|---|---|
| `GATE_NO_MOVE` | BTC hasn't moved from beat price | `gap_pct < GOLD_ZONE_MIN_MOVE_PCT (0.02%)` |
| `GATE_TOO_SURE` | Market already fully priced | `leading_odds > GATE_TOO_SURE_THRESHOLD (0.87)` |
| `GATE_50_50` | No crowd lean | `max(up_odds, down_odds) < 0.52` |

If any gate fires, the loop records a `BlockedWindow` and continues.

### 8.4 AI Signal (Grok via OpenRouter)

**File:** `ai_agent.py → AIAgent.get_signal()`  
**Model:** `x-ai/grok-4.20-beta` via `https://openrouter.ai/api/v1`  
**Timeout:** 15 seconds (returns SKIP on timeout)

The AI receives a structured user message containing:

```
=== CURRENT WINNER ===     ← which side is WINNING RIGHT NOW
=== WINDOW STATUS ===      ← elapsed/remaining/BTC/beat price
=== PRICE DYNAMICS ===     ← raw velocity, volatility
=== DIP ANALYSIS ===       ← fraction of last 20 bars above/below beat
                             classification: TEMPORARY_DIP | SUSTAINED_MOVE | MIXED | SUSTAINED_ABOVE
=== TECHNICAL INDICATORS ===  ← RSI, MA, Momentum, MACD, %B, VWAP
=== FLOW / SMART MONEY ===    ← CVD divergence, signal alignment
=== MARKET ODDS & EV ===      ← UP/DOWN implied %, EV thresholds
=== RECENT PRICES ===         ← last 100s of 5s prices, each annotated ▲ or ▼
```

**Dip Analysis Classification** (over last 20 × 5s = 100 seconds):

```
above_pct = count(price ≥ beat) / 20 × 100

TEMPORARY_DIP   : above_pct ≥ 60% AND btc currently < beat
                  → BTC was mostly above beat; current dip is transient
SUSTAINED_MOVE  : below_pct ≥ 80%
                  → BTC has been consistently below beat for 80s+
SUSTAINED_ABOVE : above_pct ≥ 80%
MIXED           : neither threshold met
```

**Recovery feasibility** is computed using smoothed velocity (first-half average vs second-half average of the last 20 bars) rather than raw endpoint velocity — this avoids false `IMPOSSIBLE` labels from brief dips at the sampling endpoint:

```
required_rate = gap / seconds_remaining   ($/second needed)
smoothed_vel  = (avg second half - avg first half) / (half × 5s)
ratio         = required_rate / |smoothed_vel|

< 1x → FEASIBLE
1–2x → BORDERLINE
2–3x → HARD
> 3x → IMPOSSIBLE
velocity opposes AND DIP=TEMPORARY_DIP → IMPOSSIBLE-SNAPSHOT (treat as BORDERLINE)
velocity opposes AND DIP=SUSTAINED_MOVE → IMPOSSIBLE
```

**AI output format:**
```json
{"signal": "BUY_UP|BUY_DOWN|SKIP", "confidence": 0.0–0.92, "reason": "one sentence"}
```

Confidence is hard-capped at 0.92 — binary markets always carry uncertainty.

**Temperature:** 0.2 (near-deterministic, consistent reasoning).

### 8.5 Post-AI Gates

**File:** `decision_maker.py → DecisionMaker.evaluate()`

After the AI signal is received:

| Gate | Condition |
|---|---|
| `GATE_AI_HOLD` | AI returned SKIP (not BUY_UP or BUY_DOWN) |
| `GATE_DIR_CONFLICT` | AI bets contrarian to current BTC position AND (dip is TEMPORARY or alignment ≤ 2) AND confidence < 0.78 |
| `GATE_LOW_CONF` | `confidence < GOLD_ZONE_MIN_CONF (0.60)` |

`GATE_DIR_CONFLICT` protects against a common failure mode: BTC dips briefly below beat, AI bets DOWN ("recovery impossible"), but indicators and dip analysis show it's a transient fluctuation. Contrarian bets need confidence ≥ 0.78.

If all gates pass → `TradeDecision(action="BUY", gate="OK")` and the trade executes.

---

## 9. Position Sizing — Fractional Kelly

**File:** `indicators.py → compute_kelly_size()`

The bot uses **quarter-Kelly** position sizing:

```
Full Kelly fraction = (confidence − implied_odds) / (1 − implied_odds)
Quarter Kelly       = full_kelly × KELLY_FRACTION (0.25)
Bet size            = bankroll × quarter_kelly
```

Where:
- `confidence` = AI's probability estimate (0.60–0.92)
- `implied_odds` = current market price for the chosen side (0.50–0.87)
- `bankroll` = USDC collateral balance (live) or `PAPER_BANKROLL_USDC = $200` (paper)

**Bounds:**
- `MIN_BET_USDC = $1.00` (floor)
- `MAX_BET_USDC = $10.00` (ceiling; further capped by `BET_SIZE_USDC` config)

**Example:** confidence=0.72, implied_odds=0.58, bankroll=$200  
```
full_kelly = (0.72 − 0.58) / (1 − 0.58) = 0.333
quarter    = 0.333 × 0.25 = 0.0833
bet        = $200 × 0.0833 = $16.67 → capped at MAX_BET_USDC → $10.00
```

**Why quarter-Kelly?** Full Kelly is mathematically optimal for long-run growth but produces high variance and drawdowns. Quarter-Kelly delivers ~94% of full-Kelly's growth rate with much lower risk of ruin.

---

## 10. Order Placement and Post-Order Cancel

**Order type:** Fill-or-Kill (FOK) market order via `py_clob_client`.

In **paper mode** (`LIVE_TRADING=false`), orders are simulated with ID `SIM-{timestamp}`. No real funds are spent.

In **live mode**, the bot:
1. Signs the market order with `POLY_ETH_PRIVATE_KEY`.
2. POSTs to the Polymarket CLOB.
3. Marks the `condition_id` in `bet_attempted_windows` **before** the order call — preventing retries even if the network fails after the CLOB accepted the order.

**Post-order cancel** (`_position_monitor_loop` + `should_cancel()`):

Runs every `POSITION_MONITOR_INTERVAL_S` seconds for each open live order.

| Cancel trigger | Condition |
|---|---|
| Opposite side near-certain | `opp_odds ≥ CANCEL_ODDS_THRESHOLD (0.95)` |
| Our side collapsed | `pos_odds ≤ 0.05` |
| BTC reversed through beat + buffer | BTC crosses beat by `CANCEL_REVERSAL_BUFFER_PCT` in the wrong direction |
| Confidence drop (opt-in) | `confidence < CANCEL_MIN_CONF (0.45)` + `CANCEL_ON_CONF_DROP=true` |

Cancel does not execute within the last `CANCEL_MIN_SECONDS_GUARD (5s)` — not enough time to process.

---

## 11. Position Resolution

**Loop:** `_results_loop` → `_check_positions()` every 60 seconds.

**Simulated positions:** resolved when the window's `end_time` passes by comparing current BTC vs `window_beat`.

**Live positions:** resolved when the CLOB order status is `MATCHED` (filled). Falls back to `get_recent_trades()` if `get_order()` fails.

**P&L calculation:**
```
WON:  pnl = amount_usdc × (1/entry_price − 1)
           = amount_usdc × (payout_ratio − 1)
LOST: pnl = −amount_usdc
```

**Example:** $5 bet at odds 0.65 (winning):  
```
pnl = $5 × (1/0.65 − 1) = $5 × 0.538 = +$2.69
```

Settled positions update `total_pnl`, `win_count`/`loss_count`, `daily_profit`/`daily_loss`, and optionally trigger a Telegram notification.

In **paper mode**, the bot also writes a separate clean analytics stream:
- **Prediction accuracy**: one final `BUY_UP`/`BUY_DOWN` call per window, compared with the actual winner at expiry.
- **Paper trade win rate**: only simulated trades that were actually executed and then settled.

These metrics are kept separate from legacy `trades_*.jsonl` so old noisy/test close records do not pollute confidence tracking.

---

## 12. Blocked Window Tracking

Every skipped trade is recorded as a `BlockedWindow`:

```python
BlockedWindow(
    window_label="20:00",
    beat_price=84500.0,
    skip_reason="GATE_TOO_SURE: odds 0.89 > 0.87",
    suggested_direction="UP",
    final_btc_price=None,    # filled after window closes
    would_have_won=None,     # True = missed profit; False = correctly avoided loss
)
```

After the window closes, `_resolve_blocked_windows()` retroactively evaluates each skip:
- `would_have_won=False` → filter **correctly blocked** a losing trade (saved money).
- `would_have_won=True` → filter **incorrectly blocked** a winning trade (missed profit).

The **filter accuracy** score (`blocked_accuracy`) = % of blocked trades that would have lost. A high score means the filters are working.

---

## 13. Daily Risk Controls

| Control | Config key | Behavior |
|---|---|---|
| Daily loss limit | `DAILY_BUDGET_USDC` | Halt trading when net loss ≥ limit (0 = disabled) |
| Daily profit target | `DAILY_PROFIT_TARGET_USDC` | Halt trading when profit ≥ target (0 = disabled) |
| Max bets per hour | `MAX_BETS_PER_HOUR = 8` | Hard cap on hourly trade count |
| Min balance | `BET_SIZE_USDC + $0.50` | Skip if insufficient USDC (live only) |

Daily limits reset at **UTC midnight**. If a win during a halted day brings the net loss back below the budget threshold, the halt is automatically lifted.

---

## 14. Logging

**File:** `logger.py`  
**Directory:** `logs/` (auto-created, rotated daily at UTC midnight)

| File | Format | Contents |
|---|---|---|
| `events_YYYY-MM-DD.log` | Plain text | Every `log_event()` call — timestamped line |
| `events_YYYY-MM-DD.jsonl` | JSON Lines | Same events as structured JSON |
| `trades_YYYY-MM-DD.jsonl` | JSON Lines | `open` + `close` records for every trade |
| `signals_YYYY-MM-DD.jsonl` | JSON Lines | Every AI signal (gold zone) with full context |
| `prices_YYYY-MM-DD.jsonl` | JSON Lines | 5-second BTC price + CVD + odds snapshots |
| `paper_analytics_YYYY-MM-DD.jsonl` | JSON Lines | Clean paper-only prediction/trade analytics for restart-safe accuracy stats |

**Trade record fields (open):**
`ts, event, condition_id, direction, token_id, size, entry_price, amount_usdc, window_beat, order_id, simulated, placed_at, window_end_at, elapsed_at_bet, gap_pct_at_bet, ai_confidence, ai_raw_confidence, signal_alignment, window_question`

**Signal record fields:**
`ts, signal, confidence, reason, elapsed_s, up_odds, down_odds, btc_price, beat_price, is_gold_zone, alignment, cvd_divergence, condition_id`

**Paper analytics fields:**
`condition_id, window_end_at, predicted_direction, decision_action, simulated_order_id, actual_winner, prediction_correct, paper_trade_won, confidence, raw_confidence, alignment, resolved_at`

Paper analytics are the only source used to rebuild paper-mode win rate and prediction accuracy after restart. Existing historical `trades_*.jsonl` are **not** backfilled into these metrics because older files may contain synthetic/test rows.

---

## 15. Terminal UI Layout

Built with **Rich** (`main.py`). The layout is:

```
┌─ header (1 row) ──────────────────────────────────────────────────────┐
│ 🐻 BOT ● LIVE/PAPER │ timestamp │ uptime                              │
├─ body (27 rows) ──────────────────────────────────────────────────────┤
│ LEFT COLUMN                  │ RIGHT COLUMN                           │
│ ┌─ POLYMARKET WINDOW ──────┐ │ ┌─ POSITIONS ────────────────────────┐ │
│ │ question, beat, progress │ │ │ open bets with entry/current odds  │ │
│ │ elapsed bar, odds        │ │ └────────────────────────────────────┘ │
│ └──────────────────────────┘ │ ┌─ RESULTS ──────────────────────────┐ │
│ ┌─ MARKET DATA ────────────┐ │ │ paper trades W/L + prediction acc. │ │
│ │ BTC price, VWAP, CVD,    │ │ │ today + persisted stats, balance   │ │
│ │ Bollinger Bands          │ │ └────────────────────────────────────┘ │
│ └──────────────────────────┘ │ ┌─ BLOCKED WINDOWS ──────────────────┐ │
│ ┌─ FILTERS ────────────────┐ │ │ recent skips with filter reasons   │ │
│ │ F1 RSI   F2 MA  F3 Mom   │ │ └────────────────────────────────────┘ │
│ │ F4 Odds  F5 Timing       │ │                                        │
│ │ pass count / alignment   │ │                                        │
│ └──────────────────────────┘ │                                        │
│ ┌─ SIGNAL ─────────────────┐ │                                        │
│ │ last AI signal + conf    │ │                                        │
│ └──────────────────────────┘ │                                        │
├─ logs (9 rows) ───────────────────────────────────────────────────────┤
│ last 7 event log entries                                              │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 16. Configuration Reference

All settings live in `config.py` and can be overridden via environment variables (`.env` file).

### Credentials

| Key | Description |
|---|---|
| `POLY_ETH_PRIVATE_KEY` | Ethereum hex private key — required for live order signing |
| `POLY_API_KEY` / `POLY_SECRET` / `POLY_PASSPHRASE` | Polymarket L2 API credentials (derived automatically if ETH key set) |
| `POLY_FUNDER` | Funder/proxy wallet address |
| `POLY_ADDRESS` | Trader wallet address |
| `OPENROUTER_API_KEY` | OpenRouter API key for AI calls |

### Trading Parameters

| Key | Default | Description |
|---|---|---|
| `LIVE_TRADING` | `false` | `true` = real orders; `false` = paper simulation |
| `BET_SIZE_USDC` | `2.00` | Maximum bet size ceiling (Kelly may bet less) |
| `DAILY_BUDGET_USDC` | `0` | Max daily net loss (0 = disabled) |
| `DAILY_PROFIT_TARGET_USDC` | `0` | Daily profit target to halt (0 = disabled) |
| `MAX_BETS_PER_HOUR` | `8` | Hourly bet cap |

### Filter Thresholds

| Key | Default | Description |
|---|---|---|
| `RSI_PERIOD` | `14` | RSI lookback bars |
| `RSI_LOW` / `RSI_HIGH` | `30` / `70` | Extreme RSI levels (for reference) |
| `MA_SHORT` / `MA_LONG` | `5` / `20` | MA periods in 5s bars |
| `MOMENTUM_TICKS` | `10` | Momentum lookback (10 × 5s = 50s) |
| `MIN_ODDS_EDGE` | `0.02` | Minimum crowd lean (needs > 0.52 to pass F4) |
| `MAX_BET_ODDS` | `0.82` | Upper odds cap — F4 fails above this |

### MACD / Bollinger / CVD

| Key | Default | Description |
|---|---|---|
| `MACD_FAST` / `MACD_SLOW` / `MACD_SIGNAL` | `12` / `26` / `9` | MACD periods on 5s bars |
| `BB_PERIOD` / `BB_STD` | `20` / `2.0` | Bollinger Band period and std multiplier |
| `CVD_DIVERGENCE_LOOKBACK` | `8` | CVD bars for divergence detection (40 seconds) |

### Gold Zone / Entry Window

| Key | Default | Description |
|---|---|---|
| `GOLD_ZONE_START_S` | `180` | Bet execution starts at this elapsed second |
| `GOLD_ZONE_MIN_MOVE_PCT` | `0.02` | BTC must move ≥ 0.02% from beat to bet |
| `GOLD_ZONE_MIN_CONF` | `0.60` | Minimum AI confidence to execute |
| `GOLD_ZONE_MAX_ODDS` | `0.87` | Max leading odds allowed (= GATE_TOO_SURE_THRESHOLD) |
| `LAST_MIN_SECONDS_GUARD` | `8` | Stop at < 8s remaining (order latency) |

### Kelly Position Sizing

| Key | Default | Description |
|---|---|---|
| `KELLY_FRACTION` | `0.25` | Quarter-Kelly multiplier |
| `MIN_BET_USDC` | `1.00` | Floor bet size |
| `MAX_BET_USDC` | `10.00` | Ceiling bet size |
| `PAPER_BANKROLL_USDC` | `200.0` | Simulated bankroll for paper Kelly sizing |

### Post-Order Cancel

| Key | Default | Description |
|---|---|---|
| `CANCEL_ODDS_THRESHOLD` | `0.95` | Cancel when opposite side reaches 95% |
| `CANCEL_MIN_CONF` | `0.45` | Cancel if confidence drops below 45% (opt-in) |
| `CANCEL_ON_CONF_DROP` | `false` | Enable confidence-based cancel |
| `CANCEL_MIN_SECONDS_GUARD` | `5` | Don't cancel within last 5 seconds |

---

## 17. Setup and Running

### Requirements

```bash
pip install -r requirements.txt
```

Key dependencies: `websockets`, `httpx`, `rich`, `numpy`, `py-clob-client`, `python-dotenv`, `certifi`.

### Environment Variables

Create a `.env` file in the project root:

```dotenv
# Required for live trading
POLY_ETH_PRIVATE_KEY=0xabc123...   # 64-char hex Ethereum private key
POLY_FUNDER=0x...                  # Funder wallet address
POLY_ADDRESS=0x...                 # Trader wallet address

# Polymarket L2 API (auto-derived from ETH key; set manually if derivation fails)
POLY_API_KEY=...
POLY_SECRET=...
POLY_PASSPHRASE=...

# AI
OPENROUTER_API_KEY=sk-or-...

# Trading (optional overrides)
LIVE_TRADING=false          # set to true for real orders
BET_SIZE_USDC=2.00
DAILY_BUDGET_USDC=20.00
DAILY_PROFIT_TARGET_USDC=0
```

### Running

```bash
python main.py
```

The Rich terminal UI starts immediately. The bot searches for the active window, then waits silently until `elapsed_s ≥ 180` before considering any trade.

### Running Tests

```bash
pytest tests/
```

Test files:
- `test_indicators.py` — unit tests for all indicator functions
- `test_ai_agent.py` — AI signal parsing and prompt construction
- `test_bot_state.py` — BotState properties and win rate
- `test_market_client.py` — MarketClient helper functions

---

## Full Decision Flow (Summary)

```
Every 1s (_trading_loop)
│
├─ Phase 1 [Always — full window]
│   └─ run_all_filters() → IndicatorSnapshot
│       ├─ F1 RSI(14) + direction vote
│       ├─ F2 MA5/MA20 crossover + direction vote
│       ├─ F3 Momentum(10) + direction vote
│       ├─ F4 Odds edge check + direction vote
│       ├─ F5 Entry timing gate
│       ├─ MACD(12,26,9) histogram + direction vote
│       ├─ Bollinger Bands(20,2) %B
│       ├─ CVD divergence over last 8 bars + direction vote
│       ├─ VWAP
│       └─ signal_alignment = count of votes for consensus direction (max 6)
│   └─ Update UI display
│
└─ Phase 2 [elapsed_s ≥ 180 only — one bet per window]
    │
    ├─ Guard checks:
    │   - daily loss/profit limits not breached
    │   - bets_this_hour < MAX_BETS_PER_HOUR
    │   - balance sufficient (live only)
    │   - seconds_remaining ≥ LAST_MIN_SECONDS_GUARD (8s)
    │   - condition_id not already attempted this window
    │
    ├─ DecisionMaker.pre_ai_check(ctx)
    │   ├─ GATE_NO_MOVE   → gap_pct < 0.02%?  SKIP
    │   ├─ GATE_TOO_SURE  → leading_odds > 0.87?  SKIP
    │   └─ GATE_50_50     → max(odds) < 0.52?  SKIP
    │
    ├─ AIAgent.get_signal()  [Grok via OpenRouter, timeout 15s]
    │   └─ Returns AISignal(signal, confidence, reason, dip_label)
    │
    └─ DecisionMaker.evaluate(ctx)
        ├─ GATE_AI_HOLD      → signal = SKIP?  SKIP
        ├─ GATE_DIR_CONFLICT → contrarian + TEMP_DIP + conf < 0.78?  SKIP
        ├─ GATE_LOW_CONF     → confidence < 0.60?  SKIP
        └─ GATE_OK           → BUY
            └─ compute_kelly_size(confidence, entry_odds, bankroll)
            └─ market.place_bet(direction, token_id, bet_size)
            └─ Record Position + log + Telegram notify
```
