"""
Japan Lost-Decades stress test — deterministic single path.

Worst-case scenario for a U.S. retiree: equity markets follow the Nikkei
post-1989 pattern — a deep crash followed by 12+ years of suppressed
volatility and flat/declining prices, then a belated recovery.

This is the hardest environment for covered-call strategies because:
  1. NAV drops 50–60% over 3 years
  2. VIX normalizes to historically LOW levels during stagnation
     → option premiums collapse TWICE (less NAV × lower yield rate)
  3. No NAV recovery for 15+ years

Path modeled:
  Phase 1  yr  1– 3  CRASH        equity −25/−20/−15%   VIX=45/40/35  cvix=100/90/80
  Phase 2  yr  4–15  STAGNATION   equity −2%/yr          VIX=12        cvix=65
  Phase 3  yr 16–20  RECOVERY     equity +5%/yr          VIX=18        cvix=65
  Phase 4  yr 21–40  BULL         equity +6%/yr          VIX=20        cvix=65

BTCI (crypto): semi-independent
  Crash years: correlated risk-off (NAV = equity × 1.5)
  Stagnation+: independent recovery/growth (+15%/yr NAV)

IAUI (gold): benefits from monetary stress
  Crash years: +10%/yr NAV (safe-haven demand)
  Stagnation:  +4%/yr
  Recovery+:   +3%/yr
"""

import sys

ROC       = {'QQQI': 0.958, 'SPYI': 0.939, 'BTCI': 0.860, 'IAUI': 0.920}
NAV_DRIFT = {'QQQI':-0.015, 'SPYI':-0.005, 'BTCI': 0.0,   'IAUI': 0.0}
COMP      = {'QQQI': 0.40,  'SPYI': 0.35,  'BTCI': 0.10,  'IAUI': 0.15}

FED_STD  = 15_000
FED_ORD  = [(11925,.10),(48475,.12),(103350,.22),(197300,.24),(250525,.32),(626350,.35),(1e9,.37)]
FED_LTCG = [(48350,.0),(533400,.15),(1e9,.20)]
FED_NIIT = 200_000
CA_STD   = 4_803
CA_BRKT  = [(10756,.010),(25499,.020),(40245,.040),(55866,.060),(70606,.080),
            (360659,.093),(432787,.103),(721314,.113),(1_000_000,.123),(1e9,.133)]
CA_MHST  = 1_000_000


def calc_tax(ordinary, ltcg, inflate=1.0):
    std = FED_STD * inflate
    oi  = max(0.0, ordinary - std)
    ot  = 0.0; prev = 0.0
    for b, r in FED_ORD:
        b2 = b * inflate
        if oi <= prev: break
        ot += (min(oi, b2) - prev) * r; prev = b2
    ls = oi; le = oi + ltcg; lt = 0.0; pt = 0.0
    for th, r in FED_LTCG:
        t2 = th * inflate
        lt += max(0.0, min(le, t2) - max(ls, pt)) * r; pt = t2
    niit = max(0.0, (ordinary + ltcg) - FED_NIIT * inflate) * 0.038
    ca_std = CA_STD * inflate
    ca = max(0.0, (ordinary + ltcg) - ca_std)
    ct = 0.0; prev = 0.0
    for b, r in CA_BRKT:
        b2 = b * inflate
        if ca <= prev: break
        ct += (min(ca, b2) - prev) * r; prev = b2
    mhst = max(0.0, ca - CA_MHST * inflate) * 0.01
    return ot + lt + niit + ct + mhst


# ── Deterministic Japan path ──────────────────────────────────────────────────

EQUITY_PATH = (
    [-0.25, -0.20, -0.15]             # yr  1–3:  crash
    + [-0.02] * 12                    # yr  4–15: stagnation
    + [+0.05] * 5                     # yr 16–20: recovery
    + [+0.06] * 20                    # yr 21–40: bull
)

VIX_PATH = (
    [45.0, 40.0, 35.0]                # crash spike
    + [12.0] * 12                     # suppressed — the killer
    + [18.0] * 5
    + [20.0] * 20
)

CVIX_PATH = (
    [100.0, 90.0, 80.0]               # crypto crash chaos
    + [65.0] * 37
)

GOLD_RETURN_PATH = (
    [0.10, 0.10, 0.10]                # safe-haven surge
    + [0.04] * 12
    + [0.03] * 25
)


def b2_nav_change(eq, gold, yr):
    """Weighted NAV return for B2 under Japan path."""
    nav = 0.0
    for k, w in COMP.items():
        if k == 'QQQI':
            nav += w * (min(eq * 0.7, 0.045) + min(eq, 0) * 0.30 + NAV_DRIFT[k])
        elif k == 'SPYI':
            nav += w * (min(eq * 0.6, 0.040) + min(eq, 0) * 0.25 + NAV_DRIFT[k])
        elif k == 'BTCI':
            # Crash: correlated risk-off. Stagnation+: independent crypto growth.
            btc = (eq * 1.5) if yr <= 3 else 0.15
            nav += w * btc
        elif k == 'IAUI':
            # Gold: capped upside (CC structure), but positive NAV drift in stress
            nav += w * (min(gold * 0.85, 0.04) + min(gold, 0) * 0.20)
    return nav


def yields(vix, cvix):
    return {
        'QQQI': max(0.040, -0.010 + 0.0083 * vix),
        'SPYI': max(0.035, -0.018 + 0.0077 * vix),
        'BTCI': max(0.100,  0.040 + 0.0025 * cvix),
        'IAUI': max(0.080,  0.18  * 0.67),          # gold vol stable
    }


def run(b2_start, spend_start, label, b3_start=200_000):
    B1_START = spend_start * 3.0

    b2       = float(b2_start)
    b1       = float(B1_START)
    b3       = float(b3_start)
    b3_ath   = float(b3_start)   # all-time high for Growth (harvest condition 4)
    sp       = float(spend_start)
    orig_tgt = float(spend_start)
    basis    = {k: b2_start * COMP[k] for k in COMP}
    prev_inc = b2 * 0.1435   # ~starting blended yield

    total_b1_drawn = 0.0
    total_b3_drawn = 0.0
    crisis_cuts    = 0

    W = 118  # line width
    print()
    print('=' * W)
    print(f'  Japan Lost-Decades Stress Test — {label}')
    print('=' * W)
    print(f'  {"Yr":>3}  {"Phase":<12}  {"B1 bal":>9}  {"B2":>12}  {"B3":>9}  {"Total":>12}  '
          f'{"Income":>9}  {"Tgt/yr":>8}  {"Inc%":>6}  {"Spend":>9}  {"B1draw":>8}  Notes')
    print('  ' + '-' * (W - 2))

    survived = True

    for yr in range(1, 41):
        eq   = EQUITY_PATH[yr - 1]
        vix  = VIX_PATH[yr - 1]
        cvix = CVIX_PATH[yr - 1]
        gold = GOLD_RETURN_PATH[yr - 1]

        phase = ('CRASH' if yr <= 3 else
                 'STAGNATION' if yr <= 15 else
                 'RECOVERY' if yr <= 20 else
                 'BULL')

        # B3 follows equity directly (no covered-call cushion)
        b3 = max(0.0, b3 * (1.0 + eq))
        b3_ath = max(b3_ath, b3)   # update ATH after nav change

        # B2 NAV
        nav = b2_nav_change(eq, gold, yr)
        b2  = max(0.0, b2 * (1.0 + nav))

        # Income
        yld = yields(vix, cvix)
        inc = sum(b2 * COMP[k] * yld[k] for k in COMP)

        # B3 harvest: all four conditions from rulebook
        #   1. income declined  2. income < 2× spend  3. B3 > $200k
        #   4. Growth within 15% of ATH (no selling into depressed market)
        notes = []
        if (inc < prev_inc and inc < 2.0 * sp
                and b3 > 200_000 and b3 >= b3_ath * 0.85):
            g = (b3 - 200_000) * 0.75
            b3 -= g; b2 += g
            inc = sum(b2 * COMP[k] * yld[k] for k in COMP)
            for k in COMP: basis[k] += g * COMP[k]
            notes.append(f'harvest${g/1000:.0f}k')

        orig_tgt *= 1.03   # inflation-adjusted target

        # ROC basis depletion
        for k in COMP:
            roc = b2 * COMP[k] * yld[k] * ROC[k]
            basis[k] = max(0.0, basis[k] - roc)

        # Annual cash flow — proper annual accounting
        b1_drawn = 0.0
        b3_drawn = 0.0
        if inc >= sp:
            surplus = inc - sp
            b2 += surplus
            for k in COMP: basis[k] += surplus * COMP[k]
        else:
            shortfall = sp - inc
            draw = min(b1, shortfall)
            b1 -= draw; b1_drawn = draw; total_b1_drawn += draw
            rem = shortfall - draw
            if rem > 0:
                b3_d = min(b3, rem); b3 -= b3_d; b3_drawn = b3_d
                total_b3_drawn += b3_d; rem -= b3_d
                if rem > 0:
                    survived = False
                    print(f'  {yr:>3}  *** DEPLETED — portfolio exhausted in year {yr} ***')
                    break

        # SGOV interest on B1
        b1 *= 1.005  # 0.5% SPAXX — ZIRP stress test

        # Tax
        inflate  = 1.03 ** (yr - 1)
        ord_inc  = sum(b2 * COMP[k] * yld[k] * (1 - ROC[k]) for k in COMP)
        tax      = calc_tax(ord_inc, 0.0, inflate)
        b2       = max(0.0, b2 - tax)

        # Spending rule — first matching row wins
        if inc > 1.5 * orig_tgt:
            sp = orig_tgt
            notes.append('snap100%')
        elif inc > 1.3 * sp:
            gap = orig_tgt - sp
            sp  = min(sp + min(sp * 0.15, gap * 0.25), orig_tgt)
            notes.append('stepup')
        elif inc >= sp:
            sp = min(sp * 1.03, orig_tgt)
        # else: hold — B1 bridges

        # Crisis cut (rare — only genuine income crisis)
        if b1 < sp * 3.0 / 12 and inc < sp * 0.70:
            old = sp
            sp  = max(sp * 0.85, orig_tgt * 0.80)
            crisis_cuts += 1
            notes.append(f'CUT${old/1000:.0f}k→${sp/1000:.0f}k')

        # B1 management
        b1_target = sp * 3.0
        if b1 > b1_target * 3.0:
            excess = b1 - b1_target; b2 += excess; b1 = b1_target  # overflow → Income Engine
        if b1 < b1_target * 0.5:
            needed = b1_target - b1; b1 += needed; b2 = max(0.0, b2 - needed)

        pct = inc / orig_tgt * 100
        if b1_drawn > 0: notes.append(f'B1-${b1_drawn/1000:.1f}k')
        if b3_drawn > 0: notes.append(f'B3-${b3_drawn/1000:.1f}k')

        print(f'  {yr:>3}  {phase:<12}  ${b1:>8,.0f}  ${b2:>11,.0f}  ${b3:>8,.0f}  '
              f'${b1+b2+b3:>11,.0f}  ${inc:>8,.0f}  ${orig_tgt:>7,.0f}  '
              f'{pct:>5.0f}%  ${sp:>8,.0f}  ${b1_drawn:>7,.0f}  '
              + '  '.join(notes))

        prev_inc = inc

    print()
    if survived:
        total = b1 + b2 + b3
        print(f'  Result: SURVIVED 40 years')
        print(f'  Final portfolio: ${total:,.0f}')
    else:
        print(f'  Result: DEPLETED')
    print(f'  Cumulative B1 drawn: ${total_b1_drawn:,.0f}')
    print(f'  Cumulative B3 drawn: ${total_b3_drawn:,.0f}')
    print(f'  Crisis spending cuts: {crisis_cuts}')


if __name__ == '__main__':
    print()
    print('Japan Lost-Decades Stress Test')
    print('Equity crash −25/−20/−15%, then 12yr stagnation at VIX=12, then slow recovery')
    print('This is the worst historically documented developed-market environment.')
    print()

    run(700_000,   60_000,  'Scenario A  $60k/yr   B2=$700k   B1=$180k  Total=$1,080k')
    run(1_350_000, 100_000, 'Scenario B  $100k/yr  B2=$1.35M  B1=$300k  Total=$1,850k')
    run(100_000,   8_400,   'Scenario C  $8,400/yr B2=$100k   B1=$25.2k Total=$125.2k', b3_start=0)
