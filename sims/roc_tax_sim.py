"""
Corrected after-tax simulation using actual NEOS ROC percentages.

Actual distribution character (from NEOS 19a-1 / annual tax data):
  QQQI: 95.8% ROC, 4.2% ordinary dividends (2024 full year)
  SPYI: 93.9% ROC, 6.1% ordinary dividends (2024 full year)
  BTCI: 86.0% ROC, 14.0% other/ordinary (FY2025; recent shows 95%+)

Key insight:
  ROC reduces cost basis — NOT currently taxable.
  Once cost basis reaches $0, further ROC becomes an immediate capital gain.
  Reinvestment continuously creates new lots with fresh basis.
  At death: step-up eliminates all accumulated deferred gains.

Federal tax:
  Ordinary dividends: taxed at ordinary income rates + standard deduction
  Excess ROC (basis depleted): taxed as LTCG (preferential federal rates)
  NIIT: 3.8% on investment income above $200k (single)

California:
  All income (ordinary + LTCG) taxed at ordinary CA rates — no LTCG preference
  CA standard deduction: ~$4,803 (single, 2026)
  MHST: +1% on CA AGI above $1M
"""
import numpy as np, sys

# ── 2026 federal tax parameters (single filer) ─────────────────────────────
FED_STD   = 15_000
FED_ORD   = [(11925,.10),(48475,.12),(103350,.22),(197300,.24),(250525,.32),(626350,.35),(1e9,.37)]
FED_LTCG  = [(48350,.0),(533400,.15),(1e9,.20)]
FED_NIIT  = 200_000

# ── California (single filer) ──────────────────────────────────────────────
CA_STD    = 4_803
CA_BRACKETS = [(10756,.010),(25499,.020),(40245,.040),(55866,.060),(70606,.080),
               (360659,.093),(432787,.103),(721314,.113),(1_000_000,.123),(1e9,.133)]
CA_MHST   = 1_000_000

# ── NEOS actual ROC rates ──────────────────────────────────────────────────
ROC_RATE  = {'QQQI': 0.958, 'SPYI': 0.939, 'BTCI': 0.860}
# Non-ROC = ordinary dividends (taxable as ordinary income)
# When basis hits 0: ROC becomes LTCG (federal preferred, CA ordinary)

# ── B2 composition ─────────────────────────────────────────────────────────
NAV_DRIFT = {'QQQI': -0.015, 'SPYI': -0.005, 'BTCI': 0.0}
COMP      = {'QQQI': 0.65, 'SPYI': 0.25, 'BTCI': 0.10}
SNAP_YRS  = [1, 5, 10, 15, 20, 30, 40]


def calc_tax(ordinary, ltcg, inflate=1.0):
    """
    Federal + California tax on separate ordinary income and LTCG streams.
    ordinary = ordinary dividends (always taxable)
    ltcg     = excess ROC capital gains (from basis-depleted lots)
    """
    std    = FED_STD * inflate
    ord_in = max(0.0, ordinary - std)

    # Federal ordinary income tax
    ord_tax = 0.0; prev = 0.0
    for brk, rate in FED_ORD:
        b2 = brk * inflate
        if ord_in <= prev: break
        ord_tax += (min(ord_in, b2) - prev) * rate
        prev = b2

    # Federal LTCG (stacked on ordinary income)
    ltcg_start = ord_in; ltcg_end = ord_in + ltcg
    ltcg_tax = 0.0; prev_t = 0.0
    for thresh, rate in FED_LTCG:
        t2 = thresh * inflate
        chunk = max(0.0, min(ltcg_end, t2) - max(ltcg_start, prev_t))
        ltcg_tax += chunk * rate
        prev_t = t2

    # NIIT (3.8% on investment income above threshold)
    total_inv = ordinary + ltcg
    niit = max(0.0, total_inv - FED_NIIT * inflate) * 0.038

    # California — all at ordinary rates (no LTCG preference)
    ca_std = CA_STD * inflate
    ca_inc = max(0.0, total_inv - ca_std)
    ca_tax = 0.0; prev = 0.0
    for brk, rate in CA_BRACKETS:
        b2 = brk * inflate
        if ca_inc <= prev: break
        ca_tax += (min(ca_inc, b2) - prev) * rate
        prev = b2
    mhst = max(0.0, ca_inc - CA_MHST * inflate) * 0.01
    ca_tax += mhst

    return ord_tax + ltcg_tax + niit + ca_tax


def run(b2_start, spend_start, n=10_000, seed=42):
    rng = np.random.default_rng(seed)
    B1 = spend_start * 1.5
    B3 = 200_000
    IP = b2_start + B1 + B3
    ok = 0; ends = []
    snaps = {yr: {'b1':[],'b2':[],'b3':[],'inc':[],'sp':[],
                  'tax':[],'ord':[],'ltcg':[],'basis_total':[]} for yr in SNAP_YRS}

    for _ in range(n):
        b2  = float(b2_start)
        b1  = float(B1); b3 = float(B3)
        sp  = float(spend_start); vix = 18.0; cvix = 80.0
        cuts = 0; alive = True; valid = True
        prev = b2 * 0.143; tgt = float(spend_start)

        # Cost basis per ETF component (starts = purchase price)
        basis = {k: b2_start * COMP[k] for k in COMP}

        for yr in range(1, 41):
            z1,z2,z3,z4,z5,z6,z7,z8 = [rng.standard_normal() for _ in range(8)]
            vix  = float(np.exp(np.clip(np.log(18)+0.7*(np.log(vix)-np.log(18))+0.3*z1, np.log(8), np.log(80))))
            cvix = float(np.exp(np.clip(np.log(80)+0.6*(np.log(cvix)-np.log(80))+0.4*z7, np.log(20), np.log(200))))
            eq   = 0.10 + 0.16*(-0.6*z1 + 0.8*z5)
            btc  = 0.10 + 0.70*(0.15*z5 + 0.99*z6)
            b3   = max(0.0, b3*(1.0 + eq))

            # B2 NAV change (QQQI/SPYI drift + BTCI tracks BTC)
            nav = sum(COMP.get(k,0)*(btc*0.65 if k=='BTCI' else NAV_DRIFT[k]+eq*0.05+0.02*z8) for k in COMP)
            b2  = max(0.0, b2*(1.0 + nav))
            # NAV changes don't affect cost basis — basis is what you paid

            yld = {'QQQI': max(0.040, -0.010+0.0083*vix+0.010*z2),
                   'SPYI': max(0.035, -0.018+0.0077*vix+0.010*z2),
                   'BTCI': max(0.100,  0.040+0.0025*cvix+0.020*z4)}

            # Income per ETF, tax character
            inc = 0.0; ordinary_income = 0.0; ltcg_income = 0.0
            for k in COMP:
                etf_val = b2 * COMP[k]
                etf_inc = etf_val * yld[k]
                inc    += etf_inc
                roc     = etf_inc * ROC_RATE[k]
                ordinary_income += etf_inc * (1.0 - ROC_RATE[k])

                # Apply ROC to basis
                if roc <= basis[k]:
                    basis[k] -= roc          # deferred — reduces basis
                else:
                    ltcg_income += roc - basis[k]   # excess ROC = immediate LTCG
                    basis[k] = 0.0

            # B3 harvest trigger (income declined AND < 2× spend)
            if inc < prev and inc < 2.0*sp and b3 > 200_000:
                g = (b3-200_000)*0.75; b3 -= g; b2 += g; inc = b2 * sum(COMP[k]*yld[k] for k in COMP)
                for k in COMP:
                    basis[k] += g * COMP[k]   # harvest = new purchase = new basis

            prev = inc; tgt *= 1.03

            # Tax
            inflate = 1.03**(yr - 1)
            tax = calc_tax(ordinary_income, ltcg_income, inflate)

            # Guardrail
            h = (b2+b1+b3) / (IP*(1.03**yr))
            if h >= 0.90:   sp *= 1.03; cuts = 0
            elif h >= 0.75: pass
            elif cuts < 5:  sp *= 0.85; cuts += 1
            if sp < 0.80*tgt:
                valid = False; alive = False; break

            # Cash flow: income → pay taxes + spend, reinvest surplus
            net = inc - sp - tax
            if net >= 0:
                b2 += net
                for k in COMP:
                    basis[k] += net * COMP[k]   # new purchases = new basis
            else:
                s = abs(net); d = min(b1,s); b1 -= d; s -= d
                if s > 0:
                    d = min(b3,s); b3 -= d; s -= d
                    if s > 0: alive = False; break

            b1 *= 1.04
            t = sp * 1.5
            if b1 > t*1.5: b3 += (b1-t); b1 = t

            if yr in snaps and alive and valid:
                snaps[yr]['b1'].append(b1);  snaps[yr]['b2'].append(b2)
                snaps[yr]['b3'].append(b3);  snaps[yr]['inc'].append(inc)
                snaps[yr]['sp'].append(sp);   snaps[yr]['tax'].append(tax)
                snaps[yr]['ord'].append(ordinary_income)
                snaps[yr]['ltcg'].append(ltcg_income)
                snaps[yr]['basis_total'].append(sum(basis.values()))

        if alive and valid:
            ok += 1; ends.append(b2+b1+b3)

    return ok/n, snaps, np.array(ends)


def show(b2s, spend0, label):
    rate, snaps, ends = run(b2s, spend0)
    print(label)
    print(f'  Success: {rate:.1%}   Median yr-40: ${np.median(ends):,.0f}')
    print(f'  {"Yr":>3}  {"Income":>10}  {"Ordinary":>10}  {"LTCG":>9}  {"Tax":>8}  {"Spend":>8}  {"Basis":>12}  {"Net reinvest":>12}')
    print('  '+'-'*88)
    for yr in [1,5,10,15,20,30,40]:
        s = snaps[yr]
        if not s['b1']: continue
        inc  = np.median(s['inc']); tax = np.median(s['tax']); sp = np.median(s['sp'])
        b2v  = np.median(s['b2']); ord_ = np.median(s['ord']); ltcg_ = np.median(s['ltcg'])
        bas  = np.median(s['basis_total']); net = inc-sp-tax; eff = tax/inc*100
        flag = ' <<' if tax>sp else ''
        print(f'  {yr:>3}  {inc:>10,.0f}  {ord_:>10,.0f}  {ltcg_:>9,.0f}  {tax:>8,.0f}  {sp:>8,.0f}  {bas:>12,.0f}  {net:>12,.0f}{flag}  ({eff:.1f}%)')
    print()


if __name__ == '__main__':
    print('='*90)
    print('CORRECTED TAX MODEL  |  Single, California')
    print('QQQI 95.8% ROC / SPYI 93.9% ROC / BTCI 86% ROC  (actual NEOS data)')
    print('ROC defers tax until basis depleted; excess ROC = LTCG (fed) / ordinary (CA)')
    print('Reinvestment continuously creates new lots with fresh basis')
    print('='*90)
    print()

    show(800_000,   60_000,  'Scenario A  $60k/yr  B2=$800k  Total=$1,090,000')
    show(2_000_000, 100_000, 'Scenario B  $100k/yr B2=$2.0M  Total=$2,350,000')

    print('='*90)
    print('Minimum B2 for 99% success  |  Single, California, corrected ROC model')
    print('='*90)
    print()
    print('--- $60k/yr spend ---')
    for b2 in [400_000,500_000,550_000,600_000,650_000,700_000,750_000,800_000]:
        r,_,ends = run(b2, 60_000)
        total = b2+90_000+200_000
        flag = ' ***' if r>=0.99 else ''
        print(f'  B2 ${b2:,}  Total ${total:,}  ->  {r:.1%}{flag}')
        sys.stdout.flush()

    print()
    print('--- $100k/yr spend ---')
    for b2 in [800_000,900_000,1_000_000,1_100_000,1_200_000,1_350_000,1_500_000]:
        r,_,ends = run(b2, 100_000)
        total = b2+150_000+200_000
        flag = ' ***' if r>=0.99 else ''
        print(f'  B2 ${b2:,}  Total ${total:,}  ->  {r:.1%}{flag}')
        sys.stdout.flush()
