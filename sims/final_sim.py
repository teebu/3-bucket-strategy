"""
Final simulation — all updated rules.

Accounts:
  Reserve (SPAXX):            3× annual spend. Receives Income Engine distributions
                              weekly. Surplus above 3× spend invested quarterly into
                              Income Engine.
  Income Engine (B2):         40% QQQI / 35% SPYI / 10% BTCI / 15% IAUI. DRIP OFF.
  Growth (B3):                VOO/QQQM/GOOGL/VXUS/SMH (b3_start=0 for Scenario C).

Quarterly reinvestment note:
  The sim uses annual steps. Quarterly vs immediate reinvestment produces identical
  year-end balances because all surplus is invested in Income Engine by Dec 31 either
  way. The only unmodeled cost is the opportunity cost of surplus sitting in SPAXX
  for ~7.5 months on average (~$3k/yr on Scenario A) — already excluded since the
  sim doesn't model within-year compounding of surplus.

Spending rules (income-based, no NAV cuts):
  Income > 1.5× spend target → snap to 100% of spend target
  Income > 1.3× current spend  → step up 15-25% toward spend target
  Income >= current spend       → 3% raise, capped at spend target
  Income < current spend        → hold spend, Reserve bridges monthly gap
  Only cut if Reserve < 3mo spend AND income < 70% of spend (genuine crisis)

Reserve target: spend × 3.0
SPAXX: mean-reverting to 1.5% long-run (starts 4%, speed=0.3, vol=0.8%, floor=0%).
Growth harvest: income declined >5% AND income < 2× spend AND Growth > $200k AND within 15% of ATH.

Tax: California single filer, actual NEOS ROC percentages.
"""
import numpy as np

ROC       = {'QQQI':0.958, 'SPYI':0.939, 'BTCI':0.860, 'IAUI':0.920}
NAV_DRIFT = {'QQQI':-0.015,'SPYI':-0.005,'BTCI':0.0,   'IAUI':0.0}
COMP      = {'QQQI':0.40,  'SPYI':0.35,  'BTCI':0.10,  'IAUI':0.15}

FED_STD  = 15_000
FED_ORD  = [(11925,.10),(48475,.12),(103350,.22),(197300,.24),(250525,.32),(626350,.35),(1e9,.37)]
FED_LTCG = [(48350,.0),(533400,.15),(1e9,.20)]
FED_NIIT = 200_000
CA_STD   = 4_803
CA_BRKT  = [(10756,.010),(25499,.020),(40245,.040),(55866,.060),(70606,.080),
            (360659,.093),(432787,.103),(721314,.113),(1_000_000,.123),(1e9,.133)]
CA_MHST  = 1_000_000

def calc_tax(ordinary, ltcg, inflate=1.0):
    std=FED_STD*inflate; oi=max(0.0,ordinary-std)
    ot=0.0; prev=0.0
    for b,r in FED_ORD:
        b2=b*inflate
        if oi<=prev: break
        ot+=(min(oi,b2)-prev)*r; prev=b2
    ls=oi; le=oi+ltcg; lt=0.0; pt=0.0
    for th,r in FED_LTCG:
        t2=th*inflate
        lt+=max(0.0,min(le,t2)-max(ls,pt))*r; pt=t2
    niit=max(0.0,(ordinary+ltcg)-FED_NIIT*inflate)*0.038
    ca_std=CA_STD*inflate; ca=max(0.0,(ordinary+ltcg)-ca_std)
    ct=0.0; prev=0.0
    for b,r in CA_BRKT:
        b2=b*inflate
        if ca<=prev: break
        ct+=(min(ca,b2)-prev)*r; prev=b2
    mhst=max(0.0,ca-CA_MHST*inflate)*0.01
    return ot+lt+niit+ct+mhst


def run(b2_start, spend_start, b3_start=200_000, n=10_000, seed=42):
    rng        = np.random.default_rng(seed)
    B1_START   = spend_start * 3.0
    B3_START   = b3_start
    ok=0; ends=[]
    SNAP_YRS   = [1,5,10,15,20,30,40]
    snaps      = {yr:{'b1':[],'b2':[],'b3':[],'inc':[],'sp':[],
                      'tax':[],'b1draw':[]} for yr in SNAP_YRS}

    for _ in range(n):
        b2  = float(b2_start); b1 = float(B1_START); b3 = float(B3_START)
        sp  = float(spend_start)
        orig_tgt = float(spend_start)   # spend target — grows 3%/yr with CPI floor
        alive=True; valid=True
        prev=b2*0.143
        basis={k:b2_start*COMP[k] for k in COMP}
        b3_ath = float(B3_START)        # B3 all-time high — protects harvest in low-VIX bear markets
        annual_b1_draw=0.0
        sgov_rate = 0.040               # starts at current rate, mean-reverts to 1.5% long-run

        for yr in range(1,41):
            z=[rng.standard_normal() for _ in range(11)]
            z1,z2,z3,z4,z5,z6,z7,z8,z9,z10,z11=z
            # SGOV: mean-revert to 1.5% long-run (speed=0.3, vol=0.8%, floor=0%)
            sgov_rate=float(np.clip(sgov_rate+0.3*(0.015-sgov_rate)+0.008*z11,0.0,0.08))
            vix =float(np.exp(np.clip(np.log(18)+0.7*(np.log(vix if yr>1 else 18)-np.log(18))+0.3*z1,np.log(8),np.log(80)))) if yr>1 else float(np.exp(np.clip(np.log(18)+0.3*z1,np.log(8),np.log(80))))
            cvix=float(np.exp(np.clip(np.log(80)+0.6*(np.log(cvix if yr>1 else 80)-np.log(80))+0.4*z7,np.log(20),np.log(200)))) if yr>1 else float(np.exp(np.clip(np.log(80)+0.4*z7,np.log(20),np.log(200))))
            gvol=float(np.clip((gvol if yr>1 else 0.18)+0.5*((gvol if yr>1 else 0.18)-0.18)+0.03*(0.3*z1+0.95*z9),0.08,0.45)) if yr>1 else float(np.clip(0.18+0.03*(0.3*z1+0.95*z9),0.08,0.45))
            eq  =0.10+0.16*(-0.6*z1+0.8*z5)
            btc =0.10+0.70*(0.15*z5+0.99*z6)
            gold=0.06+0.18*(-0.2*z1+0.98*z10)

            b3=max(0.0,b3*(1.0+eq))
            b3_ath=max(b3_ath,b3)

            nav=0.0
            for k in COMP:
                w=COMP[k]
                if k=='QQQI':   nav+=w*(min(eq*0.7,0.045)+min(eq,0)*0.3+NAV_DRIFT[k])
                elif k=='SPYI': nav+=w*(min(eq*0.6,0.040)+min(eq,0)*0.25+NAV_DRIFT[k])
                elif k=='BTCI': nav+=w*(btc*0.65)
                elif k=='IAUI': nav+=w*(min(gold*0.85,0.04)+min(gold,0)*0.20)
            b2=max(0.0,b2*(1.0+nav))

            yld={'QQQI':max(0.040,-0.010+0.0083*vix+0.010*z2),
                 'SPYI':max(0.035,-0.018+0.0077*vix+0.010*z2),
                 'BTCI':max(0.100, 0.040+0.0025*cvix+0.020*z4),
                 'IAUI':max(0.080, gvol*0.67+0.010*z8)}
            inc=sum(b2*COMP[k]*yld[k] for k in COMP)

            # B3 harvest: income declined >5% AND below 2× spend AND B3 within 15% of ATH
            if inc<prev*0.95 and inc<2.0*sp and b3>200_000 and b3>=b3_ath*0.85:
                g=(b3-200_000)*0.75; b3-=g; b2+=g
                inc=sum(b2*COMP[k]*yld[k] for k in COMP)
                for k in COMP: basis[k]+=g*COMP[k]
            prev=inc; orig_tgt*=1.03

            # ROC basis update — LTCG accrues when basis hits zero (lot-depletion tax)
            ltcg=0.0
            for k in COMP:
                roc=b2*COMP[k]*yld[k]*ROC[k]
                gain=max(0.0,roc-basis[k])  # ROC in excess of remaining basis = LTCG
                ltcg+=gain
                basis[k]=max(0.0,basis[k]-roc)

            # Annual cash flow: B1 bridges shortfall
            if inc>=sp:
                surplus=inc-sp
                b2+=surplus
                for k in COMP: basis[k]+=surplus*COMP[k]
            else:
                shortfall=sp-inc
                b1_draw=min(b1,shortfall); b1-=b1_draw; annual_b1_draw+=b1_draw
                rem=shortfall-b1_draw
                if rem>0:
                    d=min(b3,rem); b3-=d; rem-=d
                    if rem>0: alive=False; break
            b1=b1*(1+sgov_rate/12)**12  # annual SGOV compounding at stochastic rate

            # Annual tax — Section 1256 ordinary portion + LTCG from depleted-basis lots
            inflate=1.03**(yr-1)
            ord_inc=sum(b2*COMP[k]*yld[k]*(1-ROC[k]) for k in COMP)
            tax=calc_tax(ord_inc,ltcg,inflate)
            b2=max(0.0,b2-tax)

            # Income-based spending rule (set for next year)
            if inc>1.5*orig_tgt:
                sp=orig_tgt
            elif inc>1.3*sp:
                gap=orig_tgt-sp
                sp=min(sp+min(sp*0.15,gap*0.25),orig_tgt)
            elif inc>=sp:
                sp=min(sp*1.03,orig_tgt)
            # else: hold sp, B1 will bridge

            # Crisis cut only if B1 critically low AND income severely depressed
            b1_3mo=sp*3.0/12
            if b1<b1_3mo and inc<sp*0.70:
                sp=max(sp*0.85,orig_tgt*0.80)

            # B1 target and redirect
            b1_target=sp*3.0
            if b1<b1_target*0.5:
                needed=b1_target-b1; b1+=needed; b2=max(0.0,b2-needed)

            if yr in SNAP_YRS and alive and valid:
                snaps[yr]['b1'].append(b1); snaps[yr]['b2'].append(b2)
                snaps[yr]['b3'].append(b3); snaps[yr]['inc'].append(inc)
                snaps[yr]['sp'].append(sp);  snaps[yr]['tax'].append(tax)
                snaps[yr]['b1draw'].append(annual_b1_draw)
            annual_b1_draw=0.0

            if not alive: break

        if alive: ok+=1; ends.append(b2+b1+b3)

    ep=np.array(ends)
    return ok/n, snaps, ep


if __name__=='__main__':
    import sys
    print('='*85)
    print('FINAL SIMULATION — all updated rules')
    print('B2: 40Q/35S/10B/15I  |  Reserve: 3× spend  |  Income-based spending')
    print('California single filer  |  Actual NEOS ROC percentages')
    print('SGOV: mean-reverting to 1.5% long-run (starts 4%, vol=0.8%, floor=0%)')
    print('='*85)
    print()

    for b2s,sp0,b3s,label in [
        (700_000,   60_000,  200_000, 'Scenario A  $60k/yr   B2=$700k  Reserve=$180k  B3=$200k  Total=$1,080k'),
        (1_350_000, 100_000, 200_000, 'Scenario B  $100k/yr  B2=$1.35M Reserve=$300k  B3=$200k  Total=$1,850k'),
        (100_000,   8_400,   0,       'Scenario C  $8.4k/yr  B2=$100k  Reserve=$25.2k B3=$0     Total=$125.2k'),
    ]:
        rate,snaps,ends=run(b2s,sp0,b3_start=b3s)
        ep=np.array(ends)
        print(f'{label}')
        print(f'  Success: {rate:.1%}   p10: ${np.percentile(ep,10):,.0f}   Median: ${np.median(ep):,.0f}   p90: ${np.percentile(ep,90):,.0f}')
        print(f'  {"Yr":>3}  {"B1":>9}  {"B2":>12}  {"B3":>9}  {"Total":>12}  {"Income":>10}  {"Tax":>7}  {"Spend":>9}  {"B1 drawn":>9}')
        print('  '+'-'*97)
        for yr in [1,5,10,20,30,40]:
            s=snaps[yr]
            if not s['b1']: continue
            b1v=np.median(s['b1']); b2v=np.median(s['b2']); b3v=np.median(s['b3'])
            inc=np.median(s['inc']); tax=np.median(s['tax']); spv=np.median(s['sp'])
            b1d=np.median(s['b1draw']); tot=b1v+b2v+b3v
            print(f'  {yr:>3}  ${b1v:>8,.0f}  ${b2v:>11,.0f}  ${b3v:>8,.0f}  ${tot:>11,.0f}  ${inc:>9,.0f}  ${tax:>6,.0f}  ${spv:>8,.0f}  ${b1d:>8,.0f}')
        sys.stdout.flush()
        print()
