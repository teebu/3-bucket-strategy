"""
Backtest comparing original B2 vs B2 with IAUI (gold covered call) added.

IAUI model:
  - NAV tracks gold price (GLD/gold futures historical data)
  - Yield: based on gold implied vol (~15-20%/yr historically)
    IAUI-like yield = max(0.08, gold_rolling_vol * 0.65) annualized
  - ROC: ~90%+ (consistent with other NEOS CC products)
  - Covered call on gold: caps upside at ~4-5%/month strike

Key question: does adding 10-15% IAUI to B2 rescue the dot-com scenario
by providing gold appreciation + income when equity markets crash?
"""
import yfinance as yf
import pandas as pd
import numpy as np
import warnings, sys
warnings.filterwarnings('ignore')
from roc_tax_sim import calc_tax, ROC_RATE

# ── Download data ─────────────────────────────────────────────────────────────
print('Downloading data...')
vix_raw = yf.download('^VIX',    start='1995-01-01', progress=False)['Close'].squeeze()
qqq_raw = yf.download('QQQ',     start='1999-03-01', progress=False)['Close'].squeeze()
spy_raw = yf.download('SPY',     start='1993-01-01', progress=False)['Close'].squeeze()
btc_raw = yf.download('BTC-USD', start='2017-01-01', progress=False)['Close'].squeeze()
gld_raw = yf.download('GLD',     start='2004-11-01', progress=False)['Close'].squeeze()
gc_raw  = yf.download('GC=F',    start='1996-01-01', progress=False)['Close'].squeeze()

vix_m = vix_raw.resample('ME').mean()
qqq_m = qqq_raw.resample('ME').last().pct_change()
spy_m = spy_raw.resample('ME').last().pct_change()
btc_m = btc_raw.resample('ME').last().pct_change()
gld_m = gld_raw.resample('ME').last().pct_change()
gc_m  = gc_raw.resample('ME').last().pct_change()

# Gold: use futures for pre-2004, GLD after
gold_m = gc_m.copy()
overlap = gld_m.dropna().index
gold_m.loc[overlap] = gld_m.loc[overlap]

idx = vix_m.dropna().index
qqq_m  = qqq_m.reindex(idx).fillna(0)
spy_m  = spy_m.reindex(idx).fillna(0)
btc_m  = btc_m.reindex(idx).fillna(0)
gold_m = gold_m.reindex(idx).fillna(0)

# Rolling gold realized vol (annualized) for yield estimation
gold_vol_m = gold_m.rolling(12).std() * np.sqrt(12)

print('  Done.\n')

# ── Show gold vs equity in key periods ───────────────────────────────────────
print('Gold vs QQQ in key crisis periods:')
for s, e, lbl in [('2000-01','2002-12','Dot-com 2000-2002'),
                   ('2007-10','2009-03','GFC peak-trough'),
                   ('2020-02','2020-04','COVID crash'),
                   ('2022-01','2022-12','2022 bear market')]:
    m = (idx >= s) & (idx <= e)
    gc  = float((1 + gold_m[m]).prod() - 1)
    qc  = float((1 + qqq_m[m]).prod()  - 1)
    vx  = float(vix_m[m].max())
    print(f'  {lbl:<26}  Gold={gc:+.1%}  QQQ={qc:+.1%}  MaxVIX={vx:.0f}')
print()


# ── CC NAV model ──────────────────────────────────────────────────────────────
def cc_nav(index_ret, cap=0.045, cushion=0.22):
    if index_ret >= 0: return min(index_ret, cap)
    return index_ret * (1.0 - cushion)

def gold_cc_nav(gold_ret, cap=0.04, cushion=0.15):
    # Gold CC: capped upside (calls sold OTM), partial cushion on downside
    if gold_ret >= 0: return min(gold_ret, cap)
    return gold_ret * (1.0 - cushion)


# ── IAUI yield model ──────────────────────────────────────────────────────────
def iaui_yield_monthly(gold_vol_ann):
    # Gold covered call yield based on gold realized vol
    # At 15% gold vol: ~10%/yr (0.83%/mo), at 20%: ~13%/yr
    # Calibrated to IAUI's stated 12.27% at typical gold vol ~18%
    ann_yield = max(0.08, gold_vol_ann * 0.67)
    return ann_yield / 12


# ── Run backtest ──────────────────────────────────────────────────────────────
COMP_BASE = {'QQQI':0.65, 'SPYI':0.25, 'BTCI':0.10}
COMP_GOLD = {'QQQI':0.55, 'SPYI':0.20, 'BTCI':0.10, 'IAUI':0.15}  # replace some QQQI with gold

ROC = {'QQQI':0.958,'SPYI':0.939,'BTCI':0.860,'IAUI':0.920}  # assume similar ROC for IAUI

def run_hist(start_date, b2_start, spend_start, comp, years=20):
    start = pd.Timestamp(start_date)
    dates = idx[idx >= start]
    n_months = min(len(dates), years*12)
    if n_months < 12: return None

    B1 = spend_start*3.0; B3 = 200_000
    b2=float(b2_start); b1=float(B1); b3=float(B3)
    sp=float(spend_start); cuts=0; alive=True; tgt=float(spend_start)
    basis = {k: b2_start*comp.get(k,0) for k in comp}
    prev_inc = b2*0.143*12; monthly_inc_acc = 0.0; year_num = 0
    log = []

    for mi in range(n_months):
        dt = dates[mi]
        vix   = float(vix_m.loc[dt])   if dt in vix_m.index   else 18.0
        qqq   = float(qqq_m.loc[dt])   if dt in qqq_m.index   else 0.0
        spy   = float(spy_m.loc[dt])   if dt in spy_m.index   else 0.0
        btc   = float(btc_m.loc[dt])   if dt in btc_m.index   else 0.0
        gold  = float(gold_m.loc[dt])  if dt in gold_m.index  else 0.0
        gvol  = float(gold_vol_m.loc[dt]) if (dt in gold_vol_m.index and not np.isnan(gold_vol_m.loc[dt])) else 0.18

        b3 = max(0.0, b3*(1.0 + 0.4*spy + 0.6*qqq))

        # B2 NAV by component
        nav_blended = 0.0
        for k in comp:
            w = comp[k]
            if k=='QQQI':   nav_blended += w*(cc_nav(qqq)-0.00125)
            elif k=='SPYI': nav_blended += w*(cc_nav(spy)-0.000417)
            elif k=='BTCI': nav_blended += w*(cc_nav(btc,cap=0.08,cushion=0.30)*0.65)
            elif k=='IAUI': nav_blended += w*gold_cc_nav(gold)
        b2 = max(0.0, b2*(1.0+nav_blended))

        # Monthly yields
        def yld_q(): return max(0.040,-0.010+0.0083*vix)/12
        def yld_s(): return max(0.035,-0.018+0.0077*vix)/12
        def yld_b(): return max(0.100,0.040+0.0025*min(abs(btc)*np.sqrt(12)*1.5*100,200))/12
        def yld_i(): return iaui_yield_monthly(gvol)

        inc_map = {}
        for k in comp:
            w = comp[k]
            etf_val = b2*w
            if k=='QQQI':   inc_map[k] = etf_val*yld_q()
            elif k=='SPYI': inc_map[k] = etf_val*yld_s()
            elif k=='BTCI': inc_map[k] = etf_val*yld_b()
            elif k=='IAUI': inc_map[k] = etf_val*yld_i()

        monthly_inc = sum(inc_map.values())
        monthly_inc_acc += monthly_inc

        for k,inc_k in inc_map.items():
            roc_k = inc_k * ROC.get(k,0.95)
            if roc_k <= basis[k]: basis[k] -= roc_k
            else: basis[k] = 0.0

        monthly_spend = sp/12.0
        net = monthly_inc - monthly_spend
        if net >= 0:
            b2 += net
            for k in comp: basis[k] += net*comp[k]
        else:
            s=abs(net); d=min(b1,s); b1-=d; s-=d
            if s>0:
                d=min(b3,s); b3-=d; s-=d
                if s>0: alive=False; break
        b1 = b1*(1.0+0.015/12)  # 1.5% conservative SPAXX long-run

        if mi%12==11:
            year_num+=1; tgt*=1.03
            if monthly_inc_acc < prev_inc and monthly_inc_acc < 2*sp and b3>200_000:
                g=(b3-200_000)*0.75; b3-=g; b2+=g
                for k in comp: basis[k]+=g*comp[k]
            prev_inc=monthly_inc_acc
            ann_ord = sum(monthly_inc_acc*comp.get(k,0)*(1-ROC.get(k,0.95)) for k in comp)
            tax = calc_tax(ann_ord, 0.0, 1.03**(year_num-1))
            b2 = max(0.0, b2-tax)
            IP = b2_start+B1+B3
            health = (b2+b1+b3)/(IP*(1.03**year_num))
            if health>=0.90:   sp*=1.03; cuts=0
            elif health>=0.75: pass
            elif cuts<5:       sp*=0.85; cuts+=1
            if sp<0.80*tgt:    alive=False
            b1_tgt=sp*3.0
            if b1>b1_tgt*3.0: b2+=(b1-b1_tgt); b1=b1_tgt  # overflow → Income Engine
            log.append({'yr':year_num,'b2':b2,'total':b2+b1+b3,
                        'income':monthly_inc_acc,'spend':sp,'health':health,'alive':alive})
            monthly_inc_acc=0.0
            if not alive: break

    return log, alive


# ── Compare both compositions ─────────────────────────────────────────────────
STARTS = [
    ('Jan 2000 (dot-com peak)', '2000-01-01', 18),
    ('Jan 2007 (pre-GFC)',       '2007-01-01', 17),
    ('Jan 2020 (pre-COVID)',     '2020-01-01', 6),
    ('Jan 2022 (2022 bear)',     '2022-01-01', 4),
]

for b2s, sp0, scen_label in [
    (700_000,   60_000,  'Scenario A  $60k/yr'),
    (1_350_000, 100_000, 'Scenario B  $100k/yr'),
]:
    print('='*75)
    print(f'{scen_label}')
    print(f'  {"Start":<26}  {"BASE 65Q/25S/10B":>18}  {"+IAUI 55Q/20S/10B/15I":>22}')
    print('  '+'-'*70)
    for lbl, start, yrs in STARTS:
        rb, sb = run_hist(start, b2s, sp0, COMP_BASE, yrs)
        rg, sg = run_hist(start, b2s, sp0, COMP_GOLD, yrs)
        def fmt(log, survived):
            if not log: return 'no data'
            min_p = min(r['total'] for r in log)
            return f'{"SURVIVED" if survived else "FAILED":>9}  min=${min_p:>9,.0f}'
        print(f'  {lbl:<26}  {fmt(rb,sb):>28}  {fmt(rg,sg):>28}')

        # Show year-by-year for dot-com
        if '2000' in start:
            print(f'    {"":>3}  {"BASE":^35}  {"WITH IAUI":^35}')
            print(f'    {"Yr":>3}  {"Income":>10}  {"Spend":>8}  {"Health":>7}  {"Income":>10}  {"Spend":>8}  {"Health":>7}')
            for i in range(min(len(rb or []),len(rg or []))):
                rb_r = rb[i]; rg_r = rg[i]
                fb = '!' if rb_r['health']<0.90 else ''
                fg = '!' if rg_r['health']<0.90 else ''
                print(f'    {rb_r["yr"]:>3}  ${rb_r["income"]:>9,.0f}  ${rb_r["spend"]:>7,.0f}  {rb_r["health"]:>6.2f}{fb}  '
                      f'${rg_r["income"]:>9,.0f}  ${rg_r["spend"]:>7,.0f}  {rg_r["health"]:>6.2f}{fg}')
        sys.stdout.flush()
    print()
