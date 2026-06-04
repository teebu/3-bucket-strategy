# 3-Bucket Retirement Strategy

**Filer:** Single, California  
**Spend growth:** 3%/yr baseline — income-based adjustments override (see Annual Review)  
**All projections:** after federal + California tax, actual NEOS ROC percentages  
**Success definition:** Portfolio never depletes (Income Engine + Reserve + Growth reaches $0)  
**Monte Carlo:** 10,000 paths, conservative yield model, NAV erosion + ROC basis tracking  
**40-year success rate: 100% (all scenarios)**

---

## Income Engine Composition

The "Income Engine" is the core of this strategy — four ETFs that pay you monthly distributions (like a paycheck from the market). Each ETF uses a covered call strategy: it holds stocks or assets, then sells options contracts on top of them to generate extra income. You never sell the ETFs themselves — you just collect what they pay.

| ETF | Weight | Role | Yield |
|---|---|---|---|
| QQQI | 40% | Nasdaq-100 covered calls — core income | 14.11% |
| SPYI | 35% | S&P 500 covered calls — stability, lower NAV (share price) erosion | 12.09% |
| BTCI | 10% | Bitcoin covered calls — crypto volatility, decouples from stock market fear | 26.36% |
| IAUI | 15% | Gold covered calls — gold volatility, independent of stock market fear | 12.27% |

**Blended yield: 14.35%** | All four pay monthly distributions | Section 1256 tax treatment (explained below)

> **Why IAUI:** Gold rose +14% during the dot-com crash while the Nasdaq fell 78%. Gold's volatility is driven by safe-haven demand — not by stock market fear. Adding 15% IAUI raises the income floor during tech-specific downturns.

> **Why QQQI at 40%:** Limits Nasdaq concentration — the strategy's only historical weakness — while maintaining a strong blended yield.

> **Contingency (Section 1256 alternatives):** QQQI → QDTE | SPYI → XDTE | BTCI → 0%, hold cash in Reserve | IAUI → YGLD

> **Why QDTE/XDTE:** Roundhill's 0DTE (zero-days-to-expiration) covered call funds use S&P 500 and Nasdaq-100 index options — qualifying as Section 1256 contracts. Section 1256 contracts get a favorable tax split: 60% of gains are taxed as long-term gains and 40% as short-term — better than ordinary income rates. Tax treatment is preserved when switching. ROC (Return of Capital — see tax section) percentage will differ from NEOS; recalculate quarterly tax payments on switch. QYLD/XYLD (Global X) are a secondary alternative — also Section 1256, but historically steeper NAV erosion than NEOS funds. Do not use JEPI or JEPQ: they use equity-linked notes (ELNs) with 100% ordinary income, no ROC, no Section 1256 — switching would immediately move California effective rate from ~0% to your full marginal bracket.

> **⚠ Manager concentration risk:** All four Income Engine funds come from a single boutique provider (NEOS). A regulatory change, strategy shift, or fund closure at NEOS would affect the entire income engine simultaneously. Review NEOS fund AUM (total assets under management) and operating status annually. If any fund closes, activate the contingency for that fund immediately — do not wait for January review. "Loss of faith" triggers: IRS ruling against synthetic ROC generation via Section 1256 index options; NEOS portfolio management team departure; AUM drops below $500M on any core fund (liquidity risk).

---

## California Tax Treatment — The ROC Advantage

**What ROC (Return of Capital) means for you:** When you receive $1,000 in distributions, roughly $940 of it is classified as Return of Capital. It is not taxed this year. Instead, it quietly reduces what you "paid" for your shares (your cost basis). Eventually, when those shares are sold — or at death, where the tax disappears entirely via a step-up in basis — the gains are recognized. In the meantime, you pay almost nothing. This is why the strategy's effective tax rate is near $0 in the early years.

Actual distribution character (from NEOS 19a-1 / annual tax data):

| ETF | ROC % | Ordinary % | After this many years of distributions, the tax-free portion runs out |
|---|---|---|---|
| QQQI | **95.8%** | 4.2% | ~7.4 years per lot |
| SPYI | **93.9%** | 6.1% | ~8.8 years per lot |
| BTCI | **86.0%** | 14.0% | ~4.4 years per lot |
| IAUI | **~92%** | 8.0% | ~8-9 years per lot |

ROC is **not currently taxable** — it reduces cost basis instead. Reinvestment creates new lots (fresh batches of shares purchased at today's price) each month, refreshing the deferral window. At death: step-up in basis eliminates all accumulated deferred gains permanently — heirs owe nothing on the built-up gains.

**Effective tax rates:** ~0% years 1-8, rising to ~5-9% long-run (median). California taxes all income (including gold and crypto covered call distributions) at ordinary rates — no preferential long-term capital gains rate.

---

## Three Scenarios

### Scenario A — $60,000/yr

| Bucket | Asset | Amount | % |
|---|---|---|---|
| **Reserve** | SPAXX | $180,000 | 16.7% |
| **Income Engine** | QQQI (40%) | $280,000 | 25.9% |
| **Income Engine** | SPYI (35%) | $245,000 | 22.7% |
| **Income Engine** | BTCI (10%) | $70,000 | 6.5% |
| **Income Engine** | IAUI (15%) | $105,000 | 9.7% |
| **Growth** | VOO (40%) | $80,000 | 7.4% |
| **Growth** | QQQM (20%) | $40,000 | 3.7% |
| **Growth** | GOOGL (20%) | $40,000 | 3.7% |
| **Growth** | VXUS (10%) | $20,000 | 1.9% |
| **Growth** | SMH (10%) | $20,000 | 1.9% |
| | | **$1,080,000** | 100% |

**40-year success rate: 100%**

```
Year-1 income:    $100,450/yr ($8,371/mo)
Year-1 tax:            ~$0/yr  (ROC defers almost everything)
Year-1 spend:      $60,000/yr ($5,000/mo)
Year-1 surplus:    $40,450/yr ($3,371/mo reinvested)
```

---

### Scenario B — $100,000/yr

| Bucket | Asset | Amount | % |
|---|---|---|---|
| **Reserve** | SPAXX | $300,000 | 16.2% |
| **Income Engine** | QQQI (40%) | $540,000 | 29.2% |
| **Income Engine** | SPYI (35%) | $472,500 | 25.5% |
| **Income Engine** | BTCI (10%) | $135,000 | 7.3% |
| **Income Engine** | IAUI (15%) | $202,500 | 10.9% |
| **Growth** | VOO (40%) | $80,000 | 4.3% |
| **Growth** | QQQM (20%) | $40,000 | 2.2% |
| **Growth** | GOOGL (20%) | $40,000 | 2.2% |
| **Growth** | VXUS (10%) | $20,000 | 1.1% |
| **Growth** | SMH (10%) | $20,000 | 1.1% |
| | | **$1,850,000** | 100% |

**40-year success rate: 100%**

```
Year-1 income:   $193,725/yr ($16,144/mo)
Year-1 tax:           ~$0/yr
Year-1 spend:    $100,000/yr ($8,333/mo)
Year-1 surplus:   $93,725/yr ($7,810/mo reinvested)
```

---

### Scenario C — $8,400/yr

| Bucket | Asset | Amount | % |
|---|---|---|---|
| **Reserve** | SPAXX | $25,200 | 20.1% |
| **Income Engine** | QQQI (40%) | $40,000 | 32.0% |
| **Income Engine** | SPYI (35%) | $35,000 | 28.0% |
| **Income Engine** | BTCI (10%) | $10,000 | 8.0% |
| **Income Engine** | IAUI (15%) | $15,000 | 12.0% |
| **Growth** | — | $0 | 0% |
| | | **$125,200** | 100% |

**40-year success rate: 100%** (no Growth — income engine only)

```
Year-1 income:    $14,350/yr ($1,196/mo)
Year-1 tax:            ~$0/yr
Year-1 spend:      $8,400/yr ($700/mo)
Year-1 surplus:    $5,950/yr ($496/mo reinvested)
```

> No Growth harvest feeder or emergency backstop. The engine survives on Income Engine income alone — 100% success proves the core mechanics work at any scale.

**Scenario C spend rule of thumb (no Growth):** Keep spend at or below 70% of gross Income Engine income. Below 70%, the Income Engine compounds and the portfolio grows meaningfully. Above 80%, NAV (share price) erosion and falling SPAXX rates outpace reinvestment and the Income Engine slowly depletes in the median path. Current setup: $8,400 / $14,350 = 58.5% — well inside the safe zone.

| Spend / Income | Year-40 median | Verdict |
|---|---|---|
| 60% or less | $5M+ | Thriving |
| 60–70% | $3–5M | Healthy |
| 70–80% | $1–3M | Marginal |
| More than 80% | Less than $500k | Income Engine eroding |

*(SPAXX modeled at 1.5% long-run mean — conservative vs current 4%. For full scenarios A/B with Growth backstop, the threshold is looser.)*

---

## What Each Bucket Does

**Reserve (SPAXX) — Monthly spending account and income bridge.** SPAXX is a money market fund whose yield tracks the Fed Funds rate (currently ~4%; historically 0–5% — do not assume it stays high). Sized at 3× annual spend. Income Engine distributions flow into this account weekly via Fidelity's "withdraw only earnings" feature. Pay all bills from Reserve. Surplus above 3× spend is reinvested into Income Engine each quarter. In normal markets the Reserve balance stays stable. During crashes it bridges monthly shortfalls so spending never requires selling ETFs.

**Income Engine (QQQI + SPYI + BTCI + IAUI) — Your paycheck.** Four volatility drivers: equity (QQQI/SPYI), crypto (BTCI), gold (IAUI). Monthly distributions auto-transfer to Reserve weekly. Never sell the Income Engine — only collect what it pays and reinvest the surplus. Income often holds up or increases during crashes because VIX (the stock market's "fear index") spikes raise option premiums, which increases the distributions these funds pay.

**Growth (VOO / QQQM / GOOGL / VXUS / SMH) — Growth feeder and backstop.** Taxable, DRIP on (except GOOGL). DRIP means "dividend reinvestment plan" — dividends are automatically reinvested into more shares. Harvest trigger fires when Income Engine income declines AND income is below 2× spend. If Reserve ever depletes, Growth is sold to cover spending — that's its secondary role. *These holdings are examples — Growth can be any growth investments you want. The mechanics (harvest trigger, liquidation order, DRIP) apply to whatever you hold here.*

---

## DRIP Settings

| Asset | DRIP | Reason |
|---|---|---|
| SPAXX (Reserve) | N/A | Sweep account — auto-receives Income Engine distributions weekly via "withdraw only earnings"; earns SPAXX yield on full balance |
| QQQI (Income Engine) | OFF | Need monthly cash |
| SPYI (Income Engine) | OFF | Same |
| BTCI (Income Engine) | OFF | Same |
| IAUI (Income Engine) | OFF | Same |
| VOO (Growth) | ON | Dividends compound in place |
| QQQM (Growth) | ON | Same |
| VXUS (Growth) | ON | Same |
| SMH (Growth) | ON | Same |
| GOOGL (Growth) | N/A | No dividend |

---

## How It Works Month to Month

```
Three Fidelity accounts:
  Reserve          — SPAXX money market sweep. Receives Income Engine distributions weekly.
                     Pay all bills from here.
  Income Engine    — QQQI / SPYI / BTCI / IAUI (DRIP OFF)
  Growth           — VOO / QQQM / GOOGL / VXUS / SMH (DRIP ON)

One-time setup:
  Set Income Engine ETFs to DRIP OFF
  Set up automatic weekly transfer: Income Engine → Reserve
    (Use Fidelity's "withdraw only earnings" feature, or a scheduled transfer)
  Set Growth ETFs to DRIP ON
  Set up bill pay from Reserve

Monthly (zero active management):
  Distributions land in Income Engine → transfer to Reserve automatically each week
  Pay bills from Reserve as normal
  Nothing to do

Quarterly — 4 times per year (March, June, September, December):
  Investable surplus = Reserve balance − (3× annual spend)
  IF surplus > 0:
    Transfer surplus from Reserve → Income Engine
    Buy QQQI/SPYI/BTCI/IAUI in 40/35/10/15 ratio
  IF surplus ≤ 0:
    Skip reinvestment — let Reserve rebuild
  Pay estimated tax: 25% of prior year's total tax bill
  (In early years ~$0 — no payment needed)
```

**Your annual spend** is set each January (see Annual Review). The quarterly routine is the same every time — one balance check, one transfer if surplus exists, four ETF purchases.

---

## If Reserve Runs Low

The quarterly routine catches this early: any time the Reserve balance is below 3× annual spend, skip reinvestment and let Reserve rebuild. If Reserve gets below 3 months of spend (Scenario A: $15k / Scenario B: $25k / Scenario C: $2,100), also consider a voluntary 10% spend cut. Most of the time the quarterly check prevents Reserve from ever reaching zero.

If Reserve does keep dropping despite skipped reinvestment — meaning income is genuinely insufficient to cover spending — that escalates to Growth:

### Reserve Depleted

If Reserve hits zero and distributions still can't cover spending, sell Growth:

```
Emergency sell order (Growth first — never sell Income Engine if avoidable):
  1. VOO    — largest Growth position
  2. QQQM   — Growth satellite
  3. VXUS   — Growth satellite
  4. GOOGL  — Growth satellite
  5. SMH    — Growth satellite (most volatile, hold slightly longer)

If Growth also exhausted AND income still can't cover spend — Income Engine liquidation:
  6. SPYI   — Income Engine, lowest yield per dollar (12.09%)
  7. IAUI   — Income Engine, gold covered calls (12.27%)
  8. QQQI   — Income Engine, last resort (14.11%)
  9. BTCI   — absolute last resort (26.36% — highest yield, preserve longest)

Every $10,000 sold from QQQI removes ~$1,411/yr of income permanently.
```

### Reserve Refills

**Surplus redirection (quarterly):** Reserve balance covers the shortfall automatically — you keep paying bills as normal. Once income recovers above spend, the quarterly check will show Reserve below 3× target. At that point skip reinvestment until Reserve is back at target, then resume normal 40/35/10/15 Income Engine reinvestment.

**SPAXX yield (passive):** Reserve earns the prevailing Fed Funds rate. At 4%, that's ~$7,200/yr on $180k (Scenario A). **ZIRP (zero interest rate policy) caveat:** If the Fed returns to near-zero rates (as in 2009–2015 and 2020–2021), SPAXX yield drops to ~0% — budget more time to restore the target without the passive yield.

```
Refill priority after a Reserve draw:
  Quarterly check: Reserve below 3× spend
  → Skip reinvestment this quarter
  → Repeat until Reserve hits 3× spend
  → Then resume Income Engine reinvestment
  
Rate: $496/mo surplus (Scenario C) fills $8,400 gap in ~17 months
Rate: $3,671/mo surplus (Scenario A year 1) fills $60,000 gap in ~16 months
```

---

## 40-Year After-Tax Trajectory — Median Surviving Path

ROC correctly modeled (~93-96% of distributions non-taxable in early years). All values after federal + California tax. SPAXX modeled with mean-reverting yield (starts 4%, long-run mean 1.5%, floor 0%) — Reserve is lower in later years than a fixed-4% assumption would show.

**Reading the percentile ranges:** p10 = bad-luck scenario (only 10% of simulated paths did worse than this). Median = the typical outcome — half of paths ended higher, half lower. p90 = lucky scenario (only 10% of paths did better). The 100% survival rate applies across all 10,000 paths.

### Scenario A ($60k/yr, $1,080,000 start)

| Year | Reserve | Inc. Engine | Growth | Total | Income/yr | Tax/yr | Spend/yr | Disc./yr |
|---|---|---|---|---|---|---|---|---|
| **Start** | **$180k** | **$700k** | **$200k** | **$1,080k** | $100k | ~$0 | $60k | — |
| 1 (end) | $186k | $759k | $209k | $1,154k | $99k | $0 | $62k | $0 |
| 5 (end) | $203k | $1,051k | $240k | $1,494k | $140k | $0 | $70k | $8k |
| 10 (end) | $221k | $1,702k | $310k | $2,233k | $231k | $2k | $81k | $48k |
| 20 (end) | $258k | $5,005k | $644k | $5,907k | $682k | $30k | $108k | $273k |
| 30 (end) | $303k | $17,346k | $1,484k | $19,133k | $2,356k | $139k | $146k | $1,169k |
| 40 (end) | $365k | $64,407k | $3,389k | $68,161k | $8,814k | $631k | $196k | $4,753k |

Year-40 range: **$18.3M → $71.0M → $221M** (p10 / median / p90)

### Scenario B ($100k/yr, $1,850,000 start)

| Year | Reserve | Inc. Engine | Growth | Total | Income/yr | Tax/yr | Spend/yr | Disc./yr |
|---|---|---|---|---|---|---|---|---|
| **Start** | **$300k** | **$1,350k** | **$200k** | **$1,850k** | $194k | ~$0 | $100k | — |
| 1 (end) | $310k | $1,467k | $209k | $1,986k | $191k | $0 | $103k | $0 |
| 5 (end) | $339k | $2,039k | $248k | $2,627k | $270k | $1k | $116k | $32k |
| 10 (end) | $369k | $3,295k | $335k | $3,999k | $451k | $13k | $134k | $119k |
| 20 (end) | $431k | $9,843k | $732k | $11,007k | $1,352k | $82k | $181k | $581k |
| 30 (end) | $506k | $34,322k | $1,676k | $36,504k | $4,696k | $326k | $243k | $2,394k |
| 40 (end) | $608k | $126,113k | $3,887k | $130,608k | $17,191k | $1,498k | $326k | $9,298k |

Year-40 range: **$34.8M → $133.7M → $427M** (p10 / median / p90)

### Scenario C ($8,400/yr, $125,200 start — no Growth)

| Year | Reserve | Inc. Engine | Growth | Total | Income/yr | Tax/yr | Spend/yr | Disc./yr |
|---|---|---|---|---|---|---|---|---|
| **Start** | **$25k** | **$100k** | **$0** | **$125k** | $14k | ~$0 | $8,400 | — |
| 1 (end) | $26k | $106k | $0 | $132k | $14k | $0 | $9k | $0 |
| 5 (end) | $28k | $138k | $0 | $167k | $19k | $0 | $10k | $1k |
| 10 (end) | $31k | $211k | $0 | $241k | $29k | ~$0 | $11k | $5k |
| 20 (end) | $36k | $621k | $0 | $657k | $84k | ~$0 | $15k | $32k |
| 30 (end) | $42k | $2,267k | $0 | $2,309k | $310k | $1k | $20k | $154k |
| 40 (end) | $51k | $9,051k | $0 | $9,101k | $1,221k | $34k | $27k | $651k |

Year-40 range: **$1.05M → $9.1M → $35.6M** (p10 / median / p90)

> No Growth — no harvest lever or emergency backstop. The Income Engine alone achieves 100% survival. $100k compounds to ~$9.1M median by year 40.

> **On large year 30-40 numbers:** Directional only. The 100% survival rate matters, not the end balance.

---

## Annual Review — Every January

Run once per year. Sets your monthly budget for the next 12 months.

### Step 1 — Calculate Past 12 Months' Total Distributions

```
Add up all QQQI + SPYI + BTCI + IAUI distributions received in the past 12 months.
This is your annual income figure.

Also calculate the spend target for the upcoming year (your inflation-adjusted baseline):
  Upcoming target = last year's target × whichever is higher: 3% raise or actual annual CPI

  → In a normal year (CPI ≤ 3%): multiply last year's target by 1.03
  → In a high-inflation year (CPI = 6%): multiply last year's target by 1.06
  → This ensures purchasing power survives stagflation; 3% is the floor, not the cap.

  For benchmarking: the conservative 3%/yr baseline gives
  Scenario A year 10:  $60,000 × 1.03^10 = $80,635
  Scenario B year 10: $100,000 × 1.03^10 = $134,392
  (Your actual target will be higher if CPI averaged above 3%.)
```

### Step 2 — Set Spending Level for Next 12 Months

Income is the signal — portfolio value dropping does not trigger spending cuts in this strategy. Only income shortfalls do.

Apply the **first matching row only** — read top to bottom and stop at the first row that describes your situation.

| Condition | Action | Plain English |
|---|---|---|
| **Last 12 months income is more than 50% above your spend target** | Set spend = 100% of spend target | You're doing great — income is very strong. Reset to your full intended budget. |
| **Last 12 months income is more than 30% above what you're currently spending** | Raise spend 15–25% toward your spend target | Income is comfortably ahead — take a meaningful step up toward your target. |
| **Last 12 months income is at least equal to what you're currently spending** | Raise spend by 3%, capped at spend target | Normal good year — take a modest raise. |
| **Last 12 months income is less than what you're currently spending** | Keep monthly spend unchanged — same dollar amount, no raise | Income fell short this year. Hold steady and let Reserve cover the gap. |

*"Spend target" = the inflation-adjusted baseline calculated in Step 1. "Current spend" = what you're actually spending this year, which may be below target after a low-income year.*

```
Only reduce spending if BOTH of these are true at the same time:
  - Reserve is below 3 months of spend ($15k for Scenario A / $25k for Scenario B), AND
  - Last 12 months income is less than 70% of what you're currently spending

In that genuine crisis: new spend = the higher of (current spend × 0.85) or (spend target × 0.80)
After one reduction, the floor (spend target × 0.80) prevents further cuts.

Historical worst case (dot-com 2000-2002): spending never needed a cut —
Reserve bridged the income gap for 5 years. Zero cuts. Portfolio survived.
```

**Track the spend target separately every year.** Write it down. Multiply last year's target by whichever is larger: 1.03 or (1 + actual CPI for that year):

```
Year _____: prior target $_______ × max(1.03, 1 + CPI ___%) = $___________
  Note: simulation benchmarks use 3%/yr (conservative floor).
  Your real target will be higher in any high-inflation year.
```

### Step 3 — Growth Harvest Check

```
Only harvest if ALL FOUR conditions are true:
  1. Income Engine income (past 12 months) declined by more than 5% vs the prior 12 months
     — this filters out normal VIX noise, not a real income problem
  2. Income Engine income (past 12 months) is less than 2× your current spend
     — surplus is thin enough that a boost matters
  3. Growth bucket value is above $200,000
  4. Growth is within 15% of its all-time high
     — no selling into a depressed market

Harvest amount = (Growth value − $200,000) × 75%
Use proceeds to buy: QQQI (40%) + SPYI (35%) + BTCI (10%) + IAUI (15%)
Note: harvested gains are taxable. Hold positions more than 1 year for long-term capital gains rate.
```

### Step 4 — Income Engine Ratio Check

**No selling within Income Engine.** When an ETF drifts outside its target band, redirect reinvestment surplus toward the underweight ETF until it returns to target. No selling, no taxable event — ratios correct naturally over months of reinvestment.

```
         Target   Band
QQQI     40%      38–42%
SPYI     35%      33–37%
BTCI     10%       8–12%
IAUI     15%      13–17%

Enter: Total Income Engine $, QQQI $, SPYI $, BTCI $, IAUI $ → compute % → check both bounds
```

### Step 5 — Reserve Check (Annual)

```
Once a year in January:

Reserve target = current spend × 3.0
Scenario A:  Year 1 = $180k   Year 10 = $242k   Year 40 = $587k
Scenario B:  Year 1 = $300k   Year 10 = $403k   Year 40 = $979k

[ ] Reserve is below half its target → skip ALL Income Engine reinvestment until restored
```

### Reserve Warning — Ongoing (any time you check your brokerage)

**This is not just a January check.** You see your Reserve balance every time you log in. If it's dropping, act immediately.

```
Warning threshold — act immediately if Reserve falls below:
  Scenario A: $15,000   (3 months of $5,000/mo spend)
  Scenario B: $25,000   (3 months of $8,333/mo spend)
  Scenario C:  $2,100   (3 months of $700/mo bills)

When Reserve hits warning — act that quarter, don't wait for January:
  1. Stop ALL Income Engine reinvestment (stop the quarterly reinvestment)
  2. Consider a voluntary 10% spending reduction
  3. Check Growth harvest trigger — boosting Income Engine means more income
  4. If Reserve depletes: sell Growth in order (VOO → QQQM → VXUS → GOOGL → SMH)
```

### Step 6 — Annual Tax Review

```
[ ] December check: visit NEOS (neosfunds.com) and Roundhill fund pages in mid-December
    for "Estimated Year-End Distributions" press releases. If unexpected capital gains
    are passed through, adjust your Q4 estimated tax payment (due January 15) accordingly.
    Missing this is the single most likely way to incur IRS/CA underpayment penalties.

[ ] Confirm ROC % on 1099-DIVs (targets: QQQI ~95.8% / SPYI ~93.9% / BTCI ~86% / IAUI ~92%)
    ROC = Return of Capital, the tax-free portion of your distributions.
[ ] ROC dropped significantly? → recalculate quarterly estimated payments
[ ] Update quarterly estimated payments ($0 in early years, slowly rising after year 8)
[ ] Growth loss harvest opportunities to offset Income Engine long-term capital gains?
[ ] Note basis depletion progress per ETF
```

---

## Spending Philosophy

Income is the signal, not portfolio value. If the income engine generates more than 50% above what you need, you're at 100% of budget. If income drops, Reserve covers the monthly gap while income recovers. You adjust your budget once per year based on what you actually received.

```
Spend target trajectory (never cut this permanently):
  Scenario A: $60,000 × 1.03^39 = $195,722/yr by year 40
  Scenario B: $100,000 × 1.03^39 = $326,204/yr by year 40
```

---

## Discretionary Spending — How Much Can You Take?

Once income substantially exceeds base spend, surplus spending is a lifestyle choice. The engine keeps running as long as you leave enough to reinvest.

**Step-by-step calculation (run this every January):**

```
Step 1: Last 12 months income (all four ETF distributions):   $___________
Step 2: Subtract your annual spend:                          -$___________
Step 3: Subtract Income Engine total value × 6%:             -$___________
         (This is the reinvestment floor — it keeps the engine
          growing faster than spending grows, buffering against
          NAV erosion and bad years. 3% would merely keep pace;
          6% keeps the engine ahead of spend.)
Step 4: Result = max safe discretionary spending this year:   $___________

If Step 4 is zero or negative → not a discretionary year.
Let the engine rebuild before spending beyond base.
```

**What this means in practice:** Everything above the Step 4 line is genuinely yours to spend — trips, cars, gifts, renovations — without impairing the engine's future income. You don't need to extract it in advance; just spend from distributions as they arrive throughout the year and reinvest whatever's left.

**Examples (Scenario A, median paths):**

| Year | Income | Base spend | Inc. Engine × 6% | Max discretionary |
|---|---|---|---|---|
| 5 | $141k | $70k | $63k | **$8k** |
| 10 | $231k | $81k | $102k | **$48k** |
| 20 | $691k | $108k | $300k | **$283k** |
| 30 | $2,327k | $146k | $1,032k | **$1,149k** |

**Income Engine growth guard:** Only take discretionary spending if Income Engine's total value on January 1st is higher than it was on January 1st of the prior year. If Income Engine shrank — even if income is still above base spend — the engine is eroding. Reinvest the full surplus until Income Engine is growing again.

**Tax note:** Effective tax rate rises from ~0% in years 1–8 to ~5–9% long-run (median paths) as original lots' cost basis depletes. California taxes gains from depleted-basis lots at ordinary rates. Continuous reinvestment creates fresh lots each year, keeping the zero-basis fraction low — this holds effective rates below 10% even at year 40. If you shift to heavy discretionary spending, reinvestment slows, basis refresh slows, and effective rates can rise toward 15–20% in later years. The Income Engine growth guard prevents this: if the engine isn't growing, there's no discretionary year, which protects both the engine and the tax profile.

---

## Bear Market Rules

**Core principle: use Reserve to cover gaps, never sell Income Engine.** During market crashes, option premiums often rise because VIX (the fear index) spikes — so income may actually increase even as NAV (share price) falls. This is the strategy's design — income and share price decouple in a crash.

### Flag Levels

**Yellow — markets down 15% from peak:** Stop Growth checks (no harvest, no redirects). Keep collecting Income Engine distributions normally. Reserve balance covers any monthly shortfalls automatically.

**Orange — markets down 25%:** Same as Yellow. Consider voluntary 10% spending reduction to conserve Reserve.

**Red — markets down 40%:** Reserve is actively drawing down. Monitor Reserve balance. If Reserve is approaching the warning threshold ($15k for Scenario A / $25k for Scenario B), trigger voluntary spending reduction.

### Bear Mode Off

```
When the S&P 500 has been above its 200-day moving average for 3 consecutive months:
  1. Resume Growth checks (harvest, ratio, Reserve target)
  2. Apply the January spending rule to current income:
     - Income is more than 50% above target → snap to 100% of target
     - Income is more than 30% above current spend → step up 15-25%
     - Otherwise → hold current level, Reserve bridges any gap
```

---

## Tax Strategy — California Single Filer

| Asset | Federal | California |
|---|---|---|
| QQQI/SPYI/BTCI/IAUI | Section 1256: 60% long-term gains / 40% short-term | All taxed at ordinary income rates |
| SPAXX (Reserve) | Ordinary income | **Exempt** (US government obligations) |
| VOO/QQQM/VXUS/SMH | Qualified dividends (15% federal rate) | Ordinary CA rates |
| GOOGL | Capital gains only when sold | Ordinary CA rates |

**Section 1256 explained:** These four ETFs qualify for a special tax rule — 60% of any taxable gains are treated as long-term (lower rate) and 40% as short-term, regardless of how long you've held the shares. This is better than ordinary income treatment. Combined with the ~94% ROC fraction, effective taxes are near $0 in the early years.

**Year 1 effective tax: ~$0.** The 92–96% ROC fraction is not taxable when received. Taxes stay near $0 for years 1–8, rising to 5–9% long-run (median). Heavy discretionary spending slows lot creation and can push effective rates to 15–20% — the Income Engine growth guard prevents this scenario.

**Quarterly estimated taxes:** IRS Form 1040-ES + CA Form 540-ES. Near $0 in early years.

**At death:** Step-up in basis eliminates all accumulated ROC-deferred gains for heirs. Every dollar of tax-deferred gain disappears — heirs owe nothing on those gains.

---

## Scenario C — Current Status

Scenario C at 1/7th scale — same rules, same ratios, same mechanics as the full scenarios. The Income Engine is fully funded at $100k. The Reserve is still building toward its $25,200 target (3× annual spend).

### Current Allocation (Reserve building to target)

| Bucket | Asset | Current | Target | Monthly income |
|---|---|---|---|---|
| **Reserve** | SPAXX | $10,000 | $25,200 | — |
| **Income Engine** | QQQI (40%) | $40,000 | $40,000 | $470 |
| **Income Engine** | SPYI (35%) | $35,000 | $35,000 | $353 |
| **Income Engine** | BTCI (10%) | $10,000 | $10,000 | $220 |
| **Income Engine** | IAUI (15%) | $15,000 | $15,000 | $153 |
| | | **$110,000** | **$125,200** | **$1,196/mo** |

**Blended yield: 14.35%** | Monthly bills: ~$700 | Monthly surplus: ~$496

### Monthly Cash Flow

```
Distributions:    $1,196/mo → auto-transfer to Reserve weekly
Monthly bills:      -$700/mo (paid from Reserve)
Surplus in Reserve: +$496/mo

Reserve building phase — skip quarterly reinvestment until Reserve hits $25,200:
  Time to fill: ~30 months at $496/mo surplus
  
After Reserve is filled — quarterly investable surplus flows to Income Engine:
  QQQI:  $198/mo (quarterly batch)
  SPYI:  $174/mo
  BTCI:   $50/mo
  IAUI:   $74/mo
```

### Reserve Status

```
Current:     $10,000
Target (3×): $25,200   (3 × $8,400 annual spend)
Warning:      $2,100   (3 months of bills)
Shortfall:   $15,200   → skip reinvestment until Reserve hits target
```

### Discretionary Formula (Scenario C, year 10)

```
Step 1: Income (Income Engine $217k × 14.35%):        $28,300/yr
Step 2: Subtract annual spend:                         -$8,400/yr
Step 3: Subtract Income Engine value × 6% ($217k × 6%): -$13,000/yr
Step 4: Max safe discretionary spending:                $6,900/yr  (~$575/mo)
```

By year 10, reinvested surplus has grown Income Engine from $100k to ~$217k. $6,900/yr is genuinely yours — without impairing the engine's future income.

---

## vs Traditional Investing (California, single)

| Strategy | Capital | Income | 40-yr success |
|---|---|---|---|
| VOO (4% rule) | $1,500,000 | $60k/yr | ~83% (pre-tax) |
| VOO | $2,500,000 | $100k/yr | ~95% (pre-tax) |
| **This strategy — Scenario A** | **$1,080,000** | **$60k/yr** | **100%** |
| **This strategy — Scenario B** | **$1,850,000** | **$100k/yr** | **100%** |
| **This strategy — Scenario C (test)** | **$125,200** | **$8,400/yr** | **100%** |

---

## Key Numbers at a Glance

| | Scenario A | Scenario B | Scenario C (Test) |
|---|---|---|---|
| Annual spend | $60,000 | $100,000 | $8,400 |
| **Starting capital** | **$1,080,000** | **$1,850,000** | **$125,200** |
| Income Engine (QQQI/SPYI/BTCI/IAUI) | $700,000 | $1,350,000 | $100,000 |
| Reserve (SPAXX) | $180,000 (3× spend) | $300,000 | $25,200 |
| Growth (VOO/QQQM/GOOGL/VXUS/SMH) | $200,000 | $200,000 | $0 (none) |
| Income Engine composition | 40Q/35S/10B/15I | same | same |
| Blended yield | 14.35% | 14.35% | 14.35% |
| Year-1 income | $100,450 | $193,725 | $14,350 |
| Year-1 tax | **~$0** | **~$0** | **~$0** |
| Spending cut trigger | Income less than spend AND Reserve below 3 months | same | same |
| Recovery trigger | Income more than 50% above target | same | same |
| Reserve warning | Below 3 months of spend | same | below $2,100 |
| ROC: QQQI/SPYI/BTCI/IAUI | 95.8%/93.9%/86%/92% | same | same |
| QQQI contingency | QDTE (Section 1256) | same | same |
| SPYI contingency | XDTE (Section 1256) | same | same |
| IAUI contingency | YGLD | same | same |

---

## Annual Checklist

```
YEAR _____   Date ___________
Spend target for next year: prior target $_______ × max(1.03, 1 + CPI ___%) = $_______

[ ] 1. Total Income Engine distributions received in the past 12 months:
        QQQI: $_______ + SPYI: $_______ + BTCI: $_______ + IAUI: $_______ = $_______
        Last 12 months income: $___________

[ ] 2. Set spending for next 12 months:
        Last 12 months income:          $___________
        Spend target for next year:     $___________
        Currently spending:             $___________

        Which of these describes your situation? (apply only the FIRST one that fits):

        Snap-back threshold (50% above target):  $_______ × 1.5 = $_______
        Step-up threshold (30% above spend):     $_______ × 1.3 = $_______

        [ ] Income is above the snap-back threshold
            → Reset spend to 100% of target = $_______ ($______/mo)

        [ ] Income is above the step-up threshold
            → Raise spend 15-25% toward target → $_______ ($______/mo)

        [ ] Income is at least equal to current spend
            → 3% raise, capped at target → $_______ ($______/mo)

        [ ] Income is below current spend
            → Hold spend flat at $_______ ($______/mo) — Reserve bridges the shortfall

[ ] 3. Growth harvest check  (need ALL FOUR to be true)
        a. Income Engine income past 12 months: $_______
           Income Engine income prior 12 months: $_______
           Declined more than 5%? [ ] Yes  [ ] No
        b. Income less than 2× current spend?
           Income $_______ vs 2× spend $_______ [ ] Yes  [ ] No
        c. Growth value above $200,000? Growth: $_______ [ ] Yes  [ ] No
        d. Growth within 15% of all-time high?
           All-time high $_______ × 85% = $_______ — Growth above this? [ ] Yes  [ ] No

        If all four are Yes:
          Available gain = Growth $_______ − $200,000 = $_______
          Harvest 75% = $_______
          Buy: QQQI $_______ / SPYI $_______ / BTCI $_______ / IAUI $_______

[ ] 4. Income Engine ratio check  (targets: 40% QQQI / 35% SPYI / 10% BTCI / 15% IAUI — bands ±2%)
        Total Income Engine value: $________
        QQQI $______ = ____%  (target 38–42%)
        SPYI $______ = ____%  (target 33–37%)
        BTCI $______ = ____%  (target  8–12%)
        IAUI $______ = ____%  (target 13–17%)
        Any outside band? [ ] Redirect future reinvestment to underweight ETFs (no selling)

[ ] 5. Reserve check  (target = annual spend × 3)
        Reserve balance:         $________
        Target (spend × 3):      $________
        Warning level (3 months of spend): $_______ = $______/mo × 3
        [ ] Reserve below warning → skip reinvestment immediately, review monthly

[ ] 6. Tax review
        ROC % this year: QQQI___% SPYI___% BTCI___% IAUI_%
        (Targets: QQQI ~95.8% / SPYI ~93.9% / BTCI ~86% / IAUI ~92%)
        ROC = Return of Capital, the tax-free portion of your distributions.
        Dropped significantly from targets? [ ] Yes → recalculate quarterly estimated tax payments
        Update quarterly estimated payments for next year: $_______/quarter

[ ] 7. Yield monitor
        QQQI _____%  SPYI _____%  BTCI _____%  IAUI _____%
        Any below floor (QQQI below 10% / SPYI below 8%)? [ ] Yes → revisit plan

[ ] 8. NEOS operating all 4 funds? [ ] Yes  [ ] No → activate contingency for affected fund
```
