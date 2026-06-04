# 3-Bucket Retirement Strategy — Project Context

## Who This Is For
- **Single filer, under the age of 50, California**
- Long investment horizon — 40+ years of retirement ahead
- Roth IRA: contributing $7k/yr to SMH/GOOGL/QQQM — separate, never touch until 60
- Other retirement accounts exist — not included in any portfolio totals
- Social Security at 67: ~$25-40k/yr — not modeled, makes strategy more robust than numbers show
- ACA note: near-zero taxable income in early years (ROC defers everything) → possible subsidies

## Key Files

| File | Purpose |
|---|---|
| `RULEBOOK.md` | The complete strategy rulebook — primary reference |
| `index.html` | Interactive HTML version with calculators — primary viewing format |
| `sims/final_sim.py` | **The canonical simulation** — all final rules, run this for benchmarks |
| `sims/backtest_gold.py` | Historical backtest with IAUI |
| `sims/japan_sim.py` | Japan lost-decades stress test |
| `sims/tax_sim.py` | Tax analysis script |
| `sims/roc_tax_sim.py` | ROC tax treatment analysis |

**When updating the rulebook, ALWAYS update both `RULEBOOK.md` AND `index.html` together.**

---

## Strategy

### Three Accounts (Fidelity)

| Account | Asset | Amount (A) | Amount (B) | Amount (C) | Role |
|---|---|---|---|---|---|
| Reserve | SPAXX (sweep) | **$180,000** (3× spend) | **$300,000** | **$25,200** | Spending account — receives Income Engine distributions weekly via "withdraw only earnings"; surplus reinvested quarterly into Income Engine |
| Income Engine | QQQI/SPYI/BTCI/IAUI (DRIP OFF) | $700,000 | $1,350,000 | $100,000 | Covered-call ETFs — monthly distributions fund all spending |
| Growth | VOO/QQQM/GOOGL/VXUS/SMH (DRIP ON) | $200,000 | $200,000 | $0 | Self-growing via equity + DRIP; harvested into Income Engine when income dips |

### Three Scenarios

| | Scenario A | Scenario B | Scenario C |
|---|---|---|---|
| Annual spend | $60,000 | $100,000 | $8,400 |
| Starting capital | **$1,080,000** | **$1,850,000** | **$125,200** |
| Year-1 income | $100,450 | $193,725 | $14,350 |
| Year-1 tax | ~$0 | ~$0 | ~$0 |
| 40-yr success | **100%** | **100%** | **100%** |
| Year-40 median | $68M | $131M | $9.1M |
| Year-40 p10/p90 | $18M / $221M | $35M / $427M | $1.0M / $35.6M |

### Income Engine Composition

| ETF | Weight | Yield | Why |
|---|---|---|---|
| QQQI | 40% | 14.11% | Nasdaq-100 covered calls — core income |
| SPYI | 35% | 12.09% | S&P 500 covered calls — stability, lower NAV erosion |
| BTCI | 10% | 26.36% | Bitcoin covered calls — crypto volatility, independent of equity VIX |
| IAUI | 15% | 12.27% | Gold covered calls — gold rose +14% during dot-com crash |

**Blended yield: 14.35%** | All NEOS products | Section 1256 tax treatment (60% LTCG / 40% STCG federal)

---

## Tax Treatment

NEOS ROC (Return of Capital) percentages — from 19a-1 / annual tax data:

| ETF | ROC % |
|---|---|
| QQQI | 95.8% |
| SPYI | 93.9% |
| BTCI | 86.0% |
| IAUI | ~92% |

~94% of distributions reduce cost basis rather than generating taxable income — near-zero effective tax in years 1–8. Step-up at death eliminates all accumulated deferred gains for heirs. California taxes all income at ordinary rates — no preferential capital gains rate.

SPAXX: California state-tax exempt (US government obligations).

---

## Operations

### Monthly (zero active management)
Income Engine distributions → auto-transfer to Reserve weekly via Fidelity "withdraw only earnings." Pay bills from Reserve.

### Quarterly
1. Investable surplus = Reserve balance − (3× annual spend)
2. If positive → transfer to Income Engine → buy QQQI/SPYI/BTCI/IAUI in 40/35/10/15
3. Pay estimated tax: 25% of prior year's total tax bill

### January
Annual review — set spend, check Growth harvest, check Income Engine ratios, confirm NEOS operating.

---

## Spending Rules (Income-Based — No NAV Cuts)

| Condition | Action |
|---|---|
| Income is more than 50% above spend target | Reset spend to 100% of spend target |
| Income is more than 30% above current spend | Step up 15–25% toward spend target |
| Income is at least equal to current spend | 3% raise, capped at spend target |
| Income is below current spend | Hold spend flat — Reserve bridges monthly gap |
| Reserve below 3 months spend AND income below 70% of spend | Crisis cut: max(spend×0.85, target×0.80) |

**Key principle: Portfolio value dropping never triggers spending cuts. Only a genuine income crisis does.**

---

## 40-Year Benchmark (sims/final_sim.py, median paths, B1=3× spend, SPAXX→1.5% long-run)

### Scenario A ($60k/yr, $1,080k start)

| Year | Reserve | Inc. Engine | Growth | Total | Income | Tax | Spend |
|---|---|---|---|---|---|---|---|
| Start | $180k | $700k | $200k | $1,080k | $100k | ~$0 | $60k |
| 1 | $186k | $759k | $209k | $1,154k | $99k | $0 | $62k |
| 5 | $203k | $1,051k | $240k | $1,494k | $140k | $0 | $70k |
| 10 | $221k | $1,702k | $310k | $2,233k | $231k | $2k | $81k |
| 20 | $258k | $5,005k | $644k | $5,907k | $682k | $30k | $108k |
| 30 | $303k | $17,346k | $1,484k | $19,133k | $2,356k | $139k | $146k |
| 40 | $365k | $64,407k | $3,389k | $68,161k | $8,814k | $631k | $196k |

**p10: $18M | Median: $71M | p90: $221M**

### Scenario B ($100k/yr, $1,850k start)

| Year | Reserve | Inc. Engine | Growth | Total | Income | Tax | Spend |
|---|---|---|---|---|---|---|---|
| Start | $300k | $1,350k | $200k | $1,850k | $194k | ~$0 | $100k |
| 1 | $310k | $1,467k | $209k | $1,986k | $191k | $0 | $103k |
| 5 | $339k | $2,039k | $248k | $2,627k | $270k | $1k | $116k |
| 10 | $369k | $3,295k | $335k | $3,999k | $451k | $13k | $134k |
| 20 | $431k | $9,843k | $732k | $11,007k | $1,352k | $82k | $181k |
| 30 | $506k | $34,322k | $1,676k | $36,504k | $4,696k | $326k | $243k |
| 40 | $608k | $126,113k | $3,887k | $130,608k | $17,191k | $1,498k | $326k |

**p10: $35M | Median: $134M | p90: $427M**

### Scenario C ($8,400/yr, $125,200 start — no Growth)

| Year | Reserve | Inc. Engine | Growth | Total | Income | Tax | Spend |
|---|---|---|---|---|---|---|---|
| Start | $25k | $100k | $0 | $125k | $14k | ~$0 | $8,400 |
| 1 | $26k | $106k | $0 | $132k | $14k | $0 | $9k |
| 10 | $31k | $211k | $0 | $241k | $29k | ~$0 | $11k |
| 20 | $36k | $621k | $0 | $657k | $84k | ~$0 | $15k |
| 40 | $51k | $9,051k | $0 | $9,101k | $1,221k | $34k | $27k |

**p10: $1.0M | Median: $9.1M | p90: $35.6M**

---

## Historical Backtest Results (all periods survived)

| Period | Scenario A | Scenario B | Notes |
|---|---|---|---|
| Jan 2000 (dot-com peak) | ✅ 86% min spend | ✅ 90% min spend | Only period with any spend reduction |
| Jan 2003 (post-crash) | ✅ 98% | ✅ 100% | Easy recovery |
| Jan 2007 (pre-GFC) | ✅ 98% | ✅ 100% | VIX spike boosted income in 2008 |
| Jan 2009 (GFC bottom) | ✅ 100% | ✅ 100% | Started at the bottom |
| Jan 2020 (pre-COVID) | ✅ 100% | ✅ 100% | Sharp crash, fast recovery |
| Jan 2022 (2022 bear) | ✅ 100% | ✅ 96% | Elevated VIX kept income high |

**6 for 6 survival. Reserve bridged the gap in the dot-com crash — no forced cuts in any scenario.**

---

## Growth Rules

- Harvest trigger (all 4 must be true): Income Engine income declined >5% AND income < 2× spend AND Growth > $200k AND Growth within 15% of all-time high
- Harvest: 75% of (Growth − $200k) → buy 40/35/10/15 QQQI/SPYI/BTCI/IAUI
- Expected fires: 2–4 times over 40 years
- DRIP on: VOO, QQQM, VXUS, SMH | GOOGL: N/A (no dividend)
- SMH capped at 10% of Growth ($20k)
- Growth never receives active contributions — grows via DRIP + equity appreciation only

## Reserve Rules

- Starting: 3× annual spend
- Target: spend × 3 (grows as spend grows)
- Warning: Reserve < 3 months of spend → skip quarterly reinvestment immediately
- If Reserve depletes: sell Growth (VOO→QQQM→VXUS→GOOGL→SMH), then Income Engine (SPYI→IAUI→QQQI→BTCI)
- Reserve surplus above 3× spend → transfer to Income Engine quarterly (this is the reinvestment mechanism)

## Income Engine Ratio Bands (no selling — redirect reinvestment only)

| ETF | Target | Band |
|---|---|---|
| QQQI | 40% | 38–42% |
| SPYI | 35% | 33–37% |
| BTCI | 10% | 8–12% |
| IAUI | 15% | 13–17% |

---

## Key Decisions (Don't Re-Litigate)

1. **No XQQI** — leveraged, short track record, too risky
2. **No HYBI** — not needed with IAUI providing cross-asset diversification
3. **IAUI at 15%** — gold covered calls, critical for dot-com-type Nasdaq crashes; gold rose +14% during 2000–2002
4. **BTCI at 10%** — crypto volatility independent of equity VIX, provides floor yield in calm equity markets
5. **QQQI at 40%** — limits Nasdaq concentration, the strategy's only historical weakness
6. **Reserve = 3× spend** — covers the safety buffer AND the working capital flowing through the account
7. **Income-based spending rules** — NAV drops don't cut spending; only income crisis does
8. **Recovery = snap-back when income > 1.5× target** — use income, not portfolio health ratio, for recovery
9. **Growth harvest threshold = 2× spend** — prevents unnecessary CA capital gains taxes when income is healthy
10. **No selling within Income Engine to rebalance** — only redirect reinvestment; avoids CA capital gains
11. **3% static raises** — prevents compounding spending beyond income capacity
12. **Section 1256 distributions are mostly ROC** (~94%) — almost no tax in years 1–8; verified from NEOS 19a-1 data
13. **3-account Fidelity structure** — Reserve/Income Engine/Growth are separate named accounts; clarity without complexity
14. **Reserve overflow → Income Engine** — all surplus goes to Income Engine; Growth is self-contained

## Scenario C
$100k Income Engine, $25,200 Reserve, no Growth. Monthly distributions ~$1,196. Monthly bills ~$700. Surplus ~$496/mo flows to Reserve, reinvested quarterly into Income Engine. Same rules, same mechanics as the full scenarios — at 1/7th scale.

## Discretionary Spending Formula

When income substantially exceeds base spend, surplus is yours to spend without impairing the engine:

```
Step 1: Last 12 months income:                       $___________
Step 2: Subtract annual spend:                       -$___________
Step 3: Subtract Income Engine value × 6%:           -$___________
Step 4: Max safe discretionary (if positive):         $___________
```

Income Engine × 6% reinvests at twice the pace of spend growth — buffers NAV erosion and bad years. If Step 4 is zero or negative, it's not a discretionary year.

---

## Simulations

```bash
python -X utf8 sims/final_sim.py          # 40-year Monte Carlo (10,000 paths, 3 scenarios)
python -X utf8 sims/backtest_gold.py      # historical backtest with IAUI
python -X utf8 sims/japan_sim.py          # Japan lost-decades stress test
```
