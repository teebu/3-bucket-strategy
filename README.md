# 3-Bucket Retirement Strategy

A personal early-retirement income system built around covered-call ETFs, with Monte Carlo simulation, historical backtesting, and an interactive rulebook.

**[Full Rulebook →](RULEBOOK.md)**  
**[Interactive HTML Version →](https://teebu.github.io/3-bucket-strategy/)**

> **Disclaimer:** This project is for educational and informational purposes only. Nothing here constitutes financial, investment, tax, or legal advice. Past performance is not indicative of future results. All simulations are models — real outcomes will differ. Consult a qualified financial advisor before making any investment decisions.

---

## What This Is

A complete, rule-based retirement strategy for a single filer in California with a 40+ year horizon. Three named Fidelity accounts, each with one job:

| Account | Asset | Role |
|---|---|---|
| **Reserve** | SPAXX (Fidelity sweep) | 3× annual spend in cash; receives Income Engine distributions weekly; pay all bills from here |
| **Income Engine** | QQQI / SPYI / BTCI / IAUI | Covered-call ETFs generating ~14.35% blended yield — the monthly paycheck |
| **Growth** | VOO / QQQM / GOOGL / VXUS / SMH | Long-term growth; grows via DRIP; partially harvested into Income Engine when income dips |

### Three Scenarios

| | Scenario A | Scenario B | Scenario C |
|---|---|---|---|
| Starting capital | $1,080,000 | $1,850,000 | $125,200 |
| Annual spend | $60,000 | $100,000 | $8,400 |
| Year-1 income | $100,450 | $193,725 | $14,350 |
| 40-yr success rate | **100%** | **100%** | **100%** |
| Year-40 median | **$68M** | **$131M** | **$9.1M** |
| Year-40 p10 / p90 | $18M / $221M | $35M / $427M | $1.0M / $35.6M |

---

## How It Works

**Monthly (zero active management):** Income Engine distributions auto-transfer to Reserve weekly via Fidelity's "withdraw only earnings." Pay bills from Reserve as normal.

**Quarterly:**
1. Investable surplus = Reserve balance − (3× annual spend)
2. If positive → transfer to Income Engine → buy QQQI/SPYI/BTCI/IAUI in 40/35/10/15
3. Pay estimated tax: 25% of prior year's bill (in early years ~$0)

**January:** Annual review — set spend for the year, check Growth harvest trigger, check Income Engine ratios, confirm NEOS operating.

---

## Key Design Decisions

- **Income-based spending rules** — portfolio value dropping never triggers spending cuts; only genuine income shortfall does
- **Reserve bridges monthly gaps** — 3× annual spend buffer means you never need to sell anything in a downturn
- **~94% ROC** from NEOS ETFs means near-zero effective tax for years 1–8 (California included)
- **Step-up at death** eliminates all accumulated deferred gains for heirs
- **6-for-6 historical survival** across every major crash: dot-com, GFC, COVID, 2022 bear

---

## Income Engine Composition

| ETF | Weight | Yield | Why |
|---|---|---|---|
| QQQI | 40% | 14.11% | Nasdaq-100 covered calls — core income |
| SPYI | 35% | 12.09% | S&P 500 covered calls — stability, lower NAV erosion |
| BTCI | 10% | 26.36% | Bitcoin covered calls — crypto volatility decouples from equity fear |
| IAUI | 15% | 12.27% | Gold covered calls — gold rose +14% during the dot-com crash |

All four are NEOS products with Section 1256 tax treatment (60% long-term / 40% short-term gains — better than ordinary income rates).

---

## Files

| File | Purpose |
|---|---|
| [`RULEBOOK.md`](RULEBOOK.md) | Complete strategy rulebook — primary reference |
| [`index.html`](https://teebu.github.io/3-bucket-strategy/) | Interactive HTML version with calculators |

### Simulations (`sims/`)

| File | Purpose |
|---|---|
| [`final_sim.py`](sims/final_sim.py) | **Canonical 40-year Monte Carlo simulation** |
| [`backtest_gold.py`](sims/backtest_gold.py) | Historical backtest with IAUI (gold covered calls) |
| [`japan_sim.py`](sims/japan_sim.py) | Japan lost-decades stress test |
| [`tax_sim.py`](sims/tax_sim.py) | Tax analysis |
| [`roc_tax_sim.py`](sims/roc_tax_sim.py) | ROC tax treatment analysis |

```bash
python -X utf8 sims/final_sim.py       # 40-year Monte Carlo (10,000 paths)
python -X utf8 sims/backtest_gold.py   # Historical backtest
python -X utf8 sims/japan_sim.py       # Japan stress test
```

---

## Notes

- Social Security (~$25–40k/yr at 67) is not modeled — makes the actual numbers more conservative than shown
- ACA subsidies likely in early years due to near-zero taxable income
- SPAXX yield tracks Fed Funds rate (currently ~4%; modeled at 1.5% long-run mean in simulations)

## License

MIT — free to use, modify, and share. See [LICENSE](LICENSE).
