"""Compare the confirmation run (L15, r24, k30) with its neighbors.

Usage: python3 -I compare_confirmation.py <data dir> [figure.png]
<data dir> holds one sub-directory per run (kmos_L15r24k30, kmos_L20r24k30,
kmos_L15r24k12, kmos_L20r24k36) with the *_dos.data, *_eigen.data and
*_info.data files. Prints the numbers and writes the figure.
"""
import numpy as np, re, sys
C=sys.argv[1].rstrip("/")+"/"
OUT=sys.argv[2] if len(sys.argv)>2 else "confirmation-L15-r24-k30.png"
runs={"L15k30":"kmos_L15r24k30","L20k30":"kmos_L20r24k30","L15k12":"kmos_L15r24k12","L20k36":"kmos_L20r24k36"}
def dos(n):
    a=np.loadtxt(C+f"{n}/{n}_dos.data",comments="#"); return a[:,0],a[:,1]
def eig(n):
    t=open(C+f"{n}/{n}_eigen.data").read().split("\n")
    ks=[];cur=None
    for l in t:
        if l.startswith("k="): cur=[];ks.append(cur)
        elif l and not l.startswith("#"):
            p=l.split(); cur.append((float(p[1]),float(p[2])))
    return np.array([[e for e,o in k] for k in ks]),np.array([[o for e,o in k] for k in ks])
def info(n):
    s=open(C+f"{n}/{n}_info.data").read()
    return float(re.search(r"Total energy \(eV\) =\s+(\S+)",s).group(1)), int(re.search(r"iteration =\s+(\d+)",s).group(1))
Krow={"kmos_L15r24k30":496,"kmos_L20r24k30":496,"kmos_L15r24k12":108,"kmos_L20r24k36":681}
res={};D={}
for k,n in runs.items():
    E,it=info(n); e,o=eig(n)
    kr=Krow[n]-1
    vbm=e[:,8].max(); cbm=e[:,9].min()
    gapK=e[kr,9]-e[kr,8]
    x,d=dos(n); D[k]=(x,d)
    res[k]=dict(E=E,Epa=E/3,it=it,vbm=vbm,cbm=cbm,gapK=gapK,gapmin=(e[:,9]-e[:,8]).min(),nk=e.shape[0],
      nan=int(np.isnan(e).sum()+np.isnan(d).sum()),occ_min=o.min(),occ_max=o.max(),
      dos_int0=np.trapz(d[x<=0],x[x<=0]),dos_int_tot=np.trapz(d,x), x0=x[0],x1=x[-1], dosmin=d.min())
for k,r in res.items(): print(k,{a:(round(b,8) if isinstance(b,float) else b) for a,b in r.items()})
def cmp(a,b,lo,hi):  # b = denser/larger-vacuum reference
    xa,da=D[a];xb,db=D[b]; assert np.allclose(xa,xb)
    m=(xa>=lo-1e-9)&(xa<=hi+1e-9)
    diff=da[m]-db[m]
    return 100*np.abs(diff).max()/db[m].max(), 100*np.abs(diff).sum()/db[m].sum(), xa[m][np.abs(diff).argmax()], 100*diff/db[m].max(), xa[m]
for a,b in [("L15k30","L20k30"),("L15k30","L20k36"),("L20k30","L20k36"),("L15k12","L20k36")]:
    for lo,hi in [(-6,4),(-18,5)]:
        r=cmp(a,b,lo,hi); print(a,"vs",b,(lo,hi),"maxdev %.4f%% relL1 %.4f%% at %.3f eV"%(r[0],r[1],r[2]))
# left minus right
for a,b in [("L15k30","L20k30"),("L15k30","L20k36"),("L20k30","L20k36"),("L15k12","L20k30"),("L15k12","L20k36")]:
    print(a,b,"dE cell meV %.7f"%((res[a]["E"]-res[b]["E"])*1e3),"per atom %.7f"%((res[a]["Epa"]-res[b]["Epa"])*1e3),"dgapK meV %.7f"%((res[a]["gapK"]-res[b]["gapK"])*1e3))
# figure
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig,ax=plt.subplots(2,1,figsize=(8,7),sharex=True,gridspec_kw=dict(height_ratios=[3,2]))
sty={"L15k30":("C3","-",1.4),"L20k30":("C0","--",1.4),"L20k36":("k",":",1.6)}
lab={"L15k30":"L15 r24 k30 (this run)","L20k30":"L20 r24 k30","L20k36":"L20 r24 k36 (old adopted)"}
for k,(c,ls,lw) in sty.items():
    x,d=D[k]; m=(x>=-6)&(x<=4); ax[0].plot(x[m],d[m],color=c,ls=ls,lw=lw,label=lab[k])
ax[0].set_ylabel("DOS (states/eV/cell)"); ax[0].legend(frameon=False,loc="upper left"); ax[0].set_title("MoS2 monolayer GS DOS (Gaussian 0.1 eV, VBM = 0)")
for a,b,c,l in [("L15k30","L20k30","C0","L15k30 - L20k30 (vacuum, k30)"),("L15k30","L20k36","k","L15k30 - L20k36 (old adopted point)")]:
    r=cmp(a,b,-6,4); ax[1].plot(r[4],r[3],color=c,lw=1.1,label=f"{l}: max {r[0]:.2f}%, rel-L1 {r[1]:.2f}%")
ax[1].axhline(0,color="grey",lw=0.5); ax[1].set_ylabel("difference (% of peak of reference)"); ax[1].set_xlabel("E - E_VBM (eV)"); ax[1].legend(frameon=False,fontsize=8)
ax[1].set_xlim(-6,4); plt.tight_layout(); plt.savefig(OUT,dpi=160)
