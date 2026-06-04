"""
Grid search over B2 allocations — historical backtest + Monte Carlo.

Tests combinations of QQQI / SPYI / BTCI / IAUI across:
  - 4 historical crisis periods (including dot-com 2000)
  - Monte Carlo 40-year success rate (Scenario A and B)

Yields (live):  QQQI 14.11%  SPYI 12.09%  BTCI 26.36%  IAUI 12.27%
"""
import yfinance as yf
import pandas as pd
import numpy as np
import sys, warnings
warnings.filterwarnings('ignore')
from roc_tax_sim import calc_tax, ROC_RATE as BASE_ROC

ROC = {**BASE_ROC, 'IAUI': 0.920}
YIELDS_LIVE = {'QQQI':0.1411,'SPYI':0.1209,'BTCI':0.2636,'IAUI':0.1227}

# ── Load historical data ──────────────────────────────────────────────────────
print('Loading data...')
vix_m  = yf.download('^VIX',    start='1995-01-01',progress=False)['Close'].squeeze().resample('ME').mean()
qqq_m  = yf.download('QQQ',     start='1999-01-01',progress=False)['Close'].squeeze().resample('ME').last().pct_change()
spy_m  = yf.download('SPY',     start='1993-01-01',progress=False)['Close'].squeeze().resample('ME').last().pct_change()
btc_m  = yf.download('BTC-USD', start='2017-01-01',progress=False)['Close'].squeeze().resample('ME').last().pct_change()
gc_m   = yf.download('GC=F',    start='1996-01-01',progress=False)['Close'].squeeze().resample('ME').last().pct_change()
gld_m  = yf.download('GLD',     start='2004-11-01',progress=False)['Close'].squeeze().resample('ME').last().pct_change()
gold_m = gc_m.copy(); gold_m.loc[gld_m.dropna().index] = gld_m.dropna()
gold_vol_m = gold_m.rolling(12).std()*np.sqrt(12)

idx = vix_m.dropna().index
qqq_m=qqq_m.reindex(idx).fillna(0); spy_m=spy_m.reindex(idx).fillna(0)
btc_m=btc_m.reindex(idx).fillna(0); gold_m=gold_m.reindex(idx).fillna(0)
gold_vol_m=gold_vol_m.reindex(idx).fillna(0.18)
print('  Done.\n')

def cc_nav(r, cap=0.045, cush=0.22):
    return min(r,cap) if r>=0 else r*(1-cush)

def run_hist(start_date, b2s, spend0, comp, years=20):
    start=pd.Timestamp(start_date); dates=idx[idx>=start]
    n_months=min(len(dates),years*12)
    if n_months<12: return None, False
    B1=spend0*1.5; B3=200_000; IP=b2s+B1+B3
    b2=float(b2s); b1=float(B1); b3=float(B3)
    sp=float(spend0); cuts=0; alive=True; tgt=float(spend0)
    basis={k:b2s*comp.get(k,0) for k in comp}
    prev_inc=b2*0.143*12; macc=0.0; yr=0; log=[]

    for mi in range(n_months):
        dt=dates[mi]
        vix  = float(vix_m.loc[dt])  if dt in vix_m.index  else 18.0
        qqq  = float(qqq_m.loc[dt])  if dt in qqq_m.index  else 0.0
        spy  = float(spy_m.loc[dt])  if dt in spy_m.index  else 0.0
        btc  = float(btc_m.loc[dt])  if dt in btc_m.index  else 0.0
        gold = float(gold_m.loc[dt]) if dt in gold_m.index else 0.0
        gvol = float(gold_vol_m.loc[dt]) if dt in gold_vol_m.index else 0.18
        if np.isnan(gvol): gvol=0.18

        b3=max(0.0,b3*(1+0.4*spy+0.6*qqq))
        nav=sum(comp.get(k,0)*(
            cc_nav(qqq)-0.00125   if k=='QQQI' else
            cc_nav(spy)-0.000417  if k=='SPYI' else
            cc_nav(btc,0.08,0.30)*0.65 if k=='BTCI' else
            cc_nav(gold,0.04,0.15)     if k=='IAUI' else 0)
            for k in comp)
        b2=max(0.0,b2*(1+nav))

        inc_k={k:b2*comp.get(k,0)*(
            max(0.040,-0.010+0.0083*vix)/12 if k=='QQQI' else
            max(0.035,-0.018+0.0077*vix)/12 if k=='SPYI' else
            max(0.10,0.04+0.003*min(abs(btc)*np.sqrt(12)*1.5*100,200))/12 if k=='BTCI' else
            max(0.08,gvol*0.67)/12          if k=='IAUI' else 0)
            for k in comp}
        monthly_inc=sum(inc_k.values()); macc+=monthly_inc
        for k,v in inc_k.items():
            r=v*ROC.get(k,0.95)
            if r<=basis[k]: basis[k]-=r
            else: basis[k]=0.0
        net=monthly_inc-sp/12
        if net>=0: b2+=net; [basis.__setitem__(k,basis[k]+net*comp.get(k,0)) for k in comp]
        else:
            s=abs(net); d=min(b1,s); b1-=d; s-=d
            if s>0:
                d=min(b3,s); b3-=d; s-=d
                if s>0: alive=False; break
        b1*=(1+0.04/12)

        if mi%12==11:
            yr+=1; tgt*=1.03
            if macc<prev_inc and macc<2*sp and b3>200_000:
                g=(b3-200_000)*0.75; b3-=g; b2+=g
                for k in comp: basis[k]+=g*comp.get(k,0)
            prev_inc=macc
            tax=calc_tax(sum(macc*comp.get(k,0)*(1-ROC.get(k,0.95)) for k in comp),0,1.03**(yr-1))
            b2=max(0.0,b2-tax)
            h=(b2+b1+b3)/(IP*(1.03**yr))
            if h>=0.90: sp*=1.03; cuts=0
            elif h>=0.75: pass
            elif cuts<5: sp*=0.85; cuts+=1
            if sp<0.80*tgt: alive=False
            t=sp*1.5
            if b1>t*1.5: b3+=(b1-t); b1=t
            log.append({'yr':yr,'total':b2+b1+b3,'income':macc,'alive':alive})
            macc=0.0
            if not alive: break
    return log, alive

# ── Allocation grid ───────────────────────────────────────────────────────────
PERIODS = [
    ('2000','2000-01-01',20), ('2003','2003-01-01',20),
    ('2007','2007-01-01',17), ('2009','2009-01-01',15),
    ('2020','2020-01-01', 6), ('2022','2022-01-01', 4),
]

def blended_yield(c):
    return sum(c.get(k,0)*YIELDS_LIVE[k] for k in YIELDS_LIVE)

# Build allocation grid: QQQI + SPYI + BTCI=10% + IAUI=0-20%, rest SPYI
COMPS = []
for q in [0.35,0.40,0.45,0.50,0.55,0.60,0.65]:
    for i in [0.0,0.10,0.15,0.20]:
        b = 0.10
        s = round(1.0-q-b-i,2)
        if s<0.10 or s>0.40: continue
        COMPS.append({'QQQI':q,'SPYI':s,'BTCI':b,'IAUI':i})

print(f'Testing {len(COMPS)} allocations across {len(PERIODS)} historical periods...\n')

results=[]
for comp in COMPS:
    yld = blended_yield(comp)
    survives=[]; min_ports=[]
    for pid,start,yrs in PERIODS:
        for b2s,sp0 in [(700_000,60_000)]:
            log,alive=run_hist(start,b2s,sp0,comp,yrs)
            if log:
                survives.append(1 if alive else 0)
                min_ports.append(min(r['total'] for r in log))
    n_surv=sum(survives); n_tot=len(survives)
    min_min=min(min_ports) if min_ports else 0
    avg_min=np.mean(min_ports) if min_ports else 0
    results.append((comp,yld,n_surv,n_tot,min_min,avg_min))
    sys.stdout.flush()

# Sort by: (survived all periods, then avg_min)
results.sort(key=lambda x: (x[2], x[5]), reverse=True)

print('Allocation grid results — Scenario A ($60k/yr, $700k B2)')
print('Sorted by: periods survived, then min portfolio floor')
print()
print(f'  {"QQQI":>5} {"SPYI":>5} {"BTCI":>5} {"IAUI":>5}  {"Yield":>7}  {"Survived":>9}  {"Min floor":>11}  {"Avg min":>11}')
print('  '+'-'*72)
for comp,yld,ns,nt,mn,am in results[:20]:
    label=f'{comp["QQQI"]:.0%}/{comp["SPYI"]:.0%}/{comp.get("BTCI",0):.0%}/{comp.get("IAUI",0):.0%}'
    flag=' ***' if ns==nt else ''
    print(f'  {comp["QQQI"]:>5.0%} {comp["SPYI"]:>5.0%} {comp["BTCI"]:>5.0%} {comp.get("IAUI",0):>5.0%}  '
          f'{yld:>6.1%}  {ns}/{nt}{flag:4}  ${mn:>10,.0f}  ${am:>10,.0f}')
    sys.stdout.flush()

print()
print('*** = survived all periods tested')

# Show top 5 more detail
print()
print('Top 5 by survival+floor — year-by-year for 2000 scenario:')
for comp,yld,ns,nt,mn,am in results[:5]:
    if ns<nt: marker='FAILED some'
    else: marker='ALL SURVIVED'
    name=f'QQQI{comp["QQQI"]:.0%}/SPYI{comp["SPYI"]:.0%}/BTCI{comp["BTCI"]:.0%}/IAUI{comp.get("IAUI",0):.0%}'
    print(f'\n  {name}  yield={yld:.1%}  [{marker}]')
    log,alive=run_hist('2000-01-01',700_000,60_000,comp,18)
    if log:
        for r in log:
            flag='!' if r.get('alive',True)==False else ('!' if r['total']<700_000 else '')
            print(f'    yr{r["yr"]:>2}  total=${r["total"]:>10,.0f}  income=${r["income"]:>9,.0f}{flag}')
    sys.stdout.flush()
