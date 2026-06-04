import numpy as np
from final_sim import calc_tax, ROC, NAV_DRIFT, COMP

def run(b2_start, spend_start, n=10_000, seed=42):
    rng = np.random.default_rng(seed)
    B1 = spend_start * 2.0; B3_START = 200_000
    harvest_counts=[]; harvest_amounts=[]; harvest_years=[]; b3_ends=[]; ok=0

    for _ in range(n):
        b2=float(b2_start); b1=float(B1); b3=float(B3_START)
        sp=float(spend_start); orig_tgt=float(spend_start)
        vix=18.0; cvix=80.0; gvol=0.18; alive=True
        prev=b2*0.143
        basis={k:b2_start*COMP[k] for k in COMP}
        sim_n=0; sim_amt=0.0; sim_yrs=[]

        for yr in range(1,41):
            z=[rng.standard_normal() for _ in range(10)]
            z1,z2,z3,z4,z5,z6,z7,z8,z9,z10=z
            vix=float(np.exp(np.clip(np.log(18)+0.7*(np.log(vix)-np.log(18))+0.3*z1,np.log(8),np.log(80))))
            cvix=float(np.exp(np.clip(np.log(80)+0.6*(np.log(cvix)-np.log(80))+0.4*z7,np.log(20),np.log(200))))
            gvol=float(np.clip(gvol+0.5*(gvol-0.18)+0.03*(0.3*z1+0.95*z9),0.08,0.45))
            eq=0.10+0.16*(-0.6*z1+0.8*z5); btc=0.10+0.70*(0.15*z5+0.99*z6)
            gold=0.06+0.18*(-0.2*z1+0.98*z10)
            b3=max(0.0,b3*(1.0+eq))
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
                 'BTCI':max(0.100,0.040+0.0025*cvix+0.020*z4),
                 'IAUI':max(0.080,gvol*0.67+0.010*z8)}
            inc=sum(b2*COMP[k]*yld[k] for k in COMP)
            orig_tgt*=1.03
            if inc<prev and inc<2.0*sp and b3>200_000:
                g=(b3-200_000)*0.75; b3-=g; b2+=g
                inc=sum(b2*COMP[k]*yld[k] for k in COMP)
                for k in COMP: basis[k]+=g*COMP[k]
                sim_n+=1; sim_amt+=g; sim_yrs.append(yr)
            prev=inc
            for k in COMP:
                r=b2*COMP[k]*yld[k]*ROC[k]; basis[k]=max(0.0,basis[k]-r)
            msp=sp/12
            if inc>=msp:
                s=inc-msp; b2+=s
                for k in COMP: basis[k]+=s*COMP[k]
            else:
                sh=msp-inc; d=min(b1,sh); b1-=d; sh-=d
                if sh>0:
                    d=min(b3,sh); b3-=d; sh-=d
                    if sh>0: alive=False; break
            b1=b1*(1+0.04/12)**12
            inf=1.03**(yr-1)
            oi=sum(b2*COMP[k]*yld[k]*(1-ROC[k]) for k in COMP)
            tax=calc_tax(oi,0.0,inf); b2=max(0.0,b2-tax)
            if inc>1.5*orig_tgt:    sp=orig_tgt
            elif inc>1.3*sp:
                gap=orig_tgt-sp; sp=min(sp+min(sp*0.15,gap*0.25),orig_tgt)
            elif inc>=sp: sp=min(sp*1.03,orig_tgt)
            if b1<sp*0.25 and inc<sp*0.70: sp=max(sp*0.85,orig_tgt*0.80)
            b1t=max(sp*2.0,orig_tgt*1.0)
            if b1>b1t*3.0: b3+=(b1-b1t); b1=b1t
            if b1<b1t*0.5:
                nd=b1t-b1; b1+=nd; b2=max(0.0,b2-nd)
            if not alive: break

        harvest_counts.append(sim_n); harvest_amounts.append(sim_amt)
        if sim_yrs: harvest_years.extend(sim_yrs)
        if alive: ok+=1; b3_ends.append(b3)

    hc=np.array(harvest_counts); ha=np.array(harvest_amounts)
    hy=np.array(harvest_years); b3e=np.array(b3_ends)
    print(f'  Success: {ok/n:.1%}')
    print(f'  Sims with any harvest:     {int(np.sum(hc>0)):,} / {n:,}  ({np.mean(hc>0):.1%})')
    print(f'  Harvests per 40yr sim:     p10={np.percentile(hc,10):.0f}  median={np.median(hc):.0f}  p90={np.percentile(hc,90):.0f}  mean={hc.mean():.1f}')
    print(f'  Amount per harvest event:  median=${np.median(ha[ha>0]):,.0f}' if any(ha>0) else '  No harvests')
    print(f'  Total harvested / sim:     median=${np.median(ha):,.0f}')
    if len(hy):
        print('  When harvests fire (decade breakdown):')
        for lo,hi,lbl in [(1,10,'yrs  1-10'),(11,20,'yrs 11-20'),(21,30,'yrs 21-30'),(31,40,'yrs 31-40')]:
            cnt=int(np.sum((hy>=lo)&(hy<=hi)))
            print(f'    {lbl}: {cnt:,} events  ({cnt/len(hy):.0%} of all harvests)')
    else:
        print('  No harvest events occurred')
    if len(b3e):
        print(f'  B3 at year 40:             p10=${np.percentile(b3e,10):,.0f}  median=${np.median(b3e):,.0f}  p90=${np.percentile(b3e,90):,.0f}')

print('B3 Harvest Frequency  |  Final rules  |  40Q/35S/10B/15I')
print('Trigger: income declined AND income < 2x spend AND B3 > 200k')
print()
print('Scenario A  60k/yr  B2=700k  B1=120k  Total=1,020k')
run(700_000, 60_000)
print()
print('Scenario B  100k/yr  B2=1.35M  B1=200k  Total=1,750k')
run(1_350_000, 100_000)
