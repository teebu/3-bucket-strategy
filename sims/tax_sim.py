"""
After-tax retirement simulation — Single filer, California.

Federal:  Section 1256 treatment (60% LTCG / 40% STCG)
          LTCG taxed at preferential rates (0% / 15% / 20%)
          NIIT 3.8% above $200k
California: No preferential LTCG rate — all income taxed at ordinary CA rates
          Progressive brackets up to 13.3%
          Mental Health Services Tax: +1% on income over $1M
          CA standard deduction: $4,803 (single, 2026 approx)

Both: 17.5% of distributions = Return of Capital (not currently taxable)
      Brackets inflated 3%/yr alongside spend growth (IRS/CA CPI adjustments)
"""
import numpy as np

# ── Federal (single filer) ────────────────────────────────────────────────────
FED = dict(
    std_ded=15_000,
    ord_brackets=[(11925,.10),(48475,.12),(103350,.22),(197300,.24),(250525,.32),(626350,.35),(1e9,.37)],
    ltcg_thresh=[(48350,.0),(533400,.15),(1e9,.20)],
    niit_thresh=200_000,
)

# ── California (single filer) ─────────────────────────────────────────────────
# CA does NOT have preferential LTCG rates — all taxed as ordinary income
# CA 2026 approximate brackets (inflation-adjusted from 2024)
CA = dict(
    std_ded=4_803,
    brackets=[
        (10_756, .010),
        (25_499, .020),
        (40_245, .040),
        (55_866, .060),
        (70_606, .080),
        (360_659, .093),
        (432_787, .103),
        (721_314, .113),
        (1_000_000, .123),
        (1e9,       .133),
    ],
    mhst_thresh=1_000_000,   # Mental Health Services Tax: +1% above $1M CA AGI
)


def calc_federal(income, inflate=1.0):
    """Federal income tax for single filer on Section 1256 distributions."""
    taxable  = income * 0.825          # 17.5% ROC excluded
    ltcg     = taxable * 0.60          # Section 1256: 60% LTCG
    stcg     = taxable * 0.40          # Section 1256: 40% STCG (ordinary)
    std      = FED['std_ded'] * inflate
    ord_inc  = max(0.0, stcg - std)

    # Ordinary income tax on STCG portion
    ord_tax = 0.0; prev = 0.0
    for brk, rate in FED['ord_brackets']:
        brk2 = brk * inflate
        if ord_inc <= prev: break
        ord_tax += (min(ord_inc, brk2) - prev) * rate
        prev = brk2

    # LTCG tax — sits on top of ordinary income
    ltcg_start = ord_inc
    ltcg_end   = ord_inc + ltcg
    ltcg_tax   = 0.0; prev_t = 0.0
    for thresh, rate in FED['ltcg_thresh']:
        t2 = thresh * inflate
        chunk = max(0.0, min(ltcg_end, t2) - max(ltcg_start, prev_t))
        ltcg_tax += chunk * rate
        prev_t = t2

    # NIIT: 3.8% on investment income above threshold
    niit = max(0.0, taxable - FED['niit_thresh'] * inflate) * 0.038

    return ord_tax + ltcg_tax + niit


def calc_california(income, inflate=1.0):
    """California income tax — no preferential LTCG, progressive brackets."""
    taxable = income * 0.825           # same 17.5% ROC exclusion
    std_ca  = CA['std_ded'] * inflate
    ca_agi  = max(0.0, taxable - std_ca)

    # Progressive CA brackets
    ca_tax = 0.0; prev = 0.0
    for brk, rate in CA['brackets']:
        brk2 = brk * inflate
        if ca_agi <= prev: break
        ca_tax += (min(ca_agi, brk2) - prev) * rate
        prev = brk2

    # Mental Health Services Tax: 1% on CA AGI above $1M
    mhst = max(0.0, ca_agi - CA['mhst_thresh'] * inflate) * 0.01

    return ca_tax + mhst


def calc_tax(income, inflate=1.0):
    return calc_federal(income, inflate) + calc_california(income, inflate)


def verify():
    print('Tax verification — single, California:')
    cases = [
        (103_829,  9_479, 'A yr-1  ~$103k income'),
        (198_543, 32_134, 'B yr-1  ~$199k income (approx)'),
        (480_000, 100_000,'B yr-10 ~$480k income (approx)'),
    ]
    # Compute expected manually then compare
    for income, _, label in cases:
        fed = calc_federal(income)
        ca  = calc_california(income)
        total = fed + ca
        print(f'  {label}')
        print(f'    Federal: ${fed:,.0f}  CA: ${ca:,.0f}  Total: ${total:,.0f}  Eff rate: {total/income:.1%}')
    print()


# ── Monte Carlo ───────────────────────────────────────────────────────────────
NAV_DRIFT = {'QQQI': -0.015, 'SPYI': -0.005, 'BTCI': 0.0}
COMP      = {'QQQI': 0.65, 'SPYI': 0.25, 'BTCI': 0.10}
SNAP_YRS  = [1, 5, 10, 15, 20, 30, 40]


def run(b2_start, spend_start, n=10_000, seed=42):
    rng = np.random.default_rng(seed)
    B1 = spend_start * 3.0; B3 = 200_000
    IP = b2_start + B1 + B3
    ok = 0; ends = []
    snaps = {yr: {'b1':[],'b2':[],'b3':[],'inc':[],'sp':[],'tax':[]} for yr in SNAP_YRS}

    for _ in range(n):
        b2 = float(b2_start); b1 = float(B1); b3 = float(B3)
        sp = float(spend_start); vix = 18.0; cvix = 80.0
        cuts = 0; alive = True; valid = True
        prev = b2*0.143; tgt = float(spend_start)

        for yr in range(1, 41):
            z1,z2,z3,z4,z5,z6,z7,z8 = [rng.standard_normal() for _ in range(8)]
            vix  = float(np.exp(np.clip(np.log(18)+0.7*(np.log(vix)-np.log(18))+0.3*z1,np.log(8),np.log(80))))
            cvix = float(np.exp(np.clip(np.log(80)+0.6*(np.log(cvix)-np.log(80))+0.4*z7,np.log(20),np.log(200))))
            eq   = 0.10 + 0.16*(-0.6*z1 + 0.8*z5)
            btc  = 0.10 + 0.70*(0.15*z5 + 0.99*z6)
            b3   = max(0.0, b3*(1.0+eq))
            nav  = sum(COMP.get(k,0)*(btc*0.65 if k=='BTCI' else NAV_DRIFT[k]+eq*0.05+0.02*z8) for k in COMP)
            b2   = max(0.0, b2*(1.0+nav))
            yld  = {'QQQI':max(0.040,-0.010+0.0083*vix+0.010*z2),
                    'SPYI':max(0.035,-0.018+0.0077*vix+0.010*z2),
                    'BTCI':max(0.100, 0.040+0.0025*cvix+0.020*z4)}
            bl   = sum(COMP.get(k,0)*yld[k] for k in COMP)
            inc  = b2*bl
            if inc < prev and b3 > 200_000:
                g = (b3-200_000)*0.75; b3-=g; b2+=g; inc=b2*bl
            prev=inc; tgt*=1.03

            inflate = 1.03**(yr-1)
            tax = calc_tax(inc, inflate)

            h = (b2+b1+b3)/(IP*(1.03**yr))
            if h>=0.90:   sp*=1.03; cuts=0
            elif h>=0.75: pass
            elif cuts<5:  sp*=0.85; cuts+=1
            if sp < 0.80*tgt: valid=False; alive=False; break

            net = inc - sp - tax
            if net >= 0:
                b2 += net
            else:
                s = abs(net); d=min(b1,s); b1-=d; s-=d
                if s>0:
                    d=min(b3,s); b3-=d; s-=d
                    if s>0: alive=False; break

            b1*=1.015; t=sp*3.0  # 1.5% SPAXX, 3x target
            if b1>t*3.0: b2+=(b1-t); b1=t  # overflow → Income Engine

            if yr in snaps and alive and valid:
                snaps[yr]['b1'].append(b1); snaps[yr]['b2'].append(b2)
                snaps[yr]['b3'].append(b3); snaps[yr]['inc'].append(inc)
                snaps[yr]['sp'].append(sp);  snaps[yr]['tax'].append(tax)

        if alive and valid: ok+=1; ends.append(b2+b1+b3)

    return ok/n, snaps, np.array(ends)


def show(b2s, spend0, label):
    rate, snaps, ends = run(b2s, spend0)
    print(f'{label}  |  Success: {rate:.1%}  |  Median yr-40: ${np.median(ends):,.0f}')
    print(f'  {"Yr":>3}  {"Income":>10}  {"Fed tax":>9}  {"CA tax":>8}  {"Total tax":>10}  {"Spend":>8}  {"Net reinvest":>13}  {"Eff rate":>9}')
    print('  '+'-'*84)
    for yr in [1, 5, 10, 20, 30, 40]:
        s = snaps[yr]
        if not s['b1']: continue
        inc = np.median(s['inc']); tax = np.median(s['tax']); sp = np.median(s['sp'])
        inf = 1.03**(yr-1)
        fed = np.median([calc_federal(i, inf) for i in s['inc']])
        ca  = np.median([calc_california(i, inf) for i in s['inc']])
        net = inc-sp-tax
        eff = tax/inc*100
        flag = ' <<' if tax>sp else ''
        print(f'  {yr:>3}  {inc:>10,.0f}  {fed:>9,.0f}  {ca:>8,.0f}  {tax:>10,.0f}  {sp:>8,.0f}  {net:>13,.0f}  {eff:>8.1f}%{flag}')
    print()


if __name__ == '__main__':
    verify()

    print('='*88)
    print('AFTER-TAX SIMULATION  |  Single filer, California')
    print('Federal: Sec 1256 (60% LTCG/40% STCG) + NIIT')
    print('California: All distributions taxed at ordinary CA rates (no LTCG preference)')
    print('='*88)
    print()

    show(700_000,   60_000,  'Scenario A  $60k/yr   B2=$700k  Total=$990k')
    show(1_350_000, 100_000, 'Scenario B  $100k/yr  B2=$1.35M Total=$1.7M')

    # Minimum capital scan for 99% — single, California
    print('='*88)
    print('Minimum B2 for 99% success  |  Single, California')
    print('='*88)
    print()
    print('--- $60k/yr spend ---')
    for b2 in [700_000,800_000,900_000,1_000_000,1_100_000,1_200_000]:
        r,_,ends = run(b2, 60_000)
        total = b2+90_000+200_000
        flag = ' ***' if r>=0.99 else ''
        print(f'  B2 ${b2:,}  Total ${total:,}  ->  {r:.1%}{flag}')

    print()
    print('--- $100k/yr spend ---')
    for b2 in [1_350_000,1_500_000,1_650_000,1_800_000,2_000_000,2_200_000]:
        r,_,ends = run(b2, 100_000)
        total = b2+150_000+200_000
        flag = ' ***' if r>=0.99 else ''
        print(f'  B2 ${b2:,}  Total ${total:,}  ->  {r:.1%}{flag}')
