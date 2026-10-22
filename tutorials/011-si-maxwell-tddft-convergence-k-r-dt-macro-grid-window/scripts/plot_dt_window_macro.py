#!/usr/bin/env python3
"""Time step, propagation window and macro grid figures.

usage: plot_dt_window_macro.py <data dir> <output figure dir>

<data dir> holds one sub-directory per run, laid out as for make_figures.py.
Writes dt-pairs.png, propagation-window.png and macro-grid.png.
"""
import glob, os, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
D=sys.argv[1]
OUT=sys.argv[2]
os.makedirs(OUT,exist_ok=True)
plt.rcParams.update({"font.size":9,"axes.grid":True,"grid.alpha":.25,"axes.spines.top":False,"axes.spines.right":False})
def wave(r): return np.loadtxt(f"{D}/{r}/{r}_wave.data")
def mfiles(r,kind):
    for sub in (f"{r}_m/m*","m*"):
        f=sorted(glob.glob(f"{D}/{r}/{sub}/{r}_{kind}.data"))
        if f: return f
def rt_energy_mean(r):
    fs=mfiles(r,"rt_energy"); a=[np.loadtxt(f) for f in fs]
    return a[0][:,0], np.mean([x[:,2] for x in a],axis=0), np.array([x[-1,2] for x in a])
def RT(r,tmax=None):
    a=wave(r); t=a[:,0]
    if tmax: m=t<=tmax+1e-9; a=a[m]; t=t[m]
    n=np.trapz(a[:,3]**2,t); return np.trapz(a[:,6]**2,t)/n, np.trapz(a[:,9]**2,t)/n
def pu(r):
    a=np.loadtxt(f"{D}/{r}/{r}_rt_energy.data"); return a[:,0],a[:,2]
# ---------------- dt-pairs
pairs=[("r12 k4 (multiscale film mean)","ksl_ms_r12k04_m8h50_d002","ksl_ms_r12k04_m8h50_d001","dt 0.002 fs","dt 0.001 fs","ms","+0.05 %"),
       ("r20 k4 (multiscale film mean)","ksl_ms_r20k04_m8h50_d001","ksl_ms_r20k04_m8h50_d0005","dt 0.001 fs","dt 0.0005 fs","ms","+0.05 %"),
       ("r24 k8 (single cell)","ksl_pu_r24k08_d001","ksl_pu_r24k08_d0005","dt 0.001 fs","dt 0.0005 fs","pu","-3e-5 rel")]
fig,ax=plt.subplots(2,3,figsize=(11,5),sharex=True)
res=[]
for j,(ttl,a,b,la,lb,kind,readme) in enumerate(pairs):
    if kind=="ms":
        ta,ea,fa=rt_energy_mean(a); tb,eb,fb=rt_energy_mean(b)
        ra,rb=RT(a,16),RT(b,16)
        txt=f"final: {ea[-1]:.5f} to {eb[-1]:.5f} eV ({100*(eb[-1]/ea[-1]-1):+.3f} %)\nR {ra[0]:.4f} to {rb[0]:.4f}, T {ra[1]:.4f} to {rb[1]:.4f}\nREADME: {readme}, R,T 1e-4"
    else:
        ta,ea=pu(a); tb,eb=pu(b)
        txt=f"final: {ea[-1]:.5f} to {eb[-1]:.5f} eV (rel {eb[-1]/ea[-1]-1:+.1e})\nREADME: {readme}"
    ax[0,j].plot(ta,ea,color="#1f6fb4",lw=1.6,label=la); ax[0,j].plot(tb,eb,color="#c0392b",lw=1.1,ls="--",label=lb)
    ax[0,j].set_title(ttl); ax[0,j].legend(fontsize=8,loc="upper left")
    ax[0,j].text(.98,.04,txt,transform=ax[0,j].transAxes,ha="right",va="bottom",fontsize=7.5,bbox=dict(fc="w",ec="#aaa"))
    d=eb-np.interp(tb,ta,ea) if True else 0
    ax[1,j].plot(tb,d*1e3,color="k",lw=1); ax[1,j].set_xlabel("time (fs)")
    ax[1,j].set_title(f"fine - coarse: max {np.abs(d).max()*1e3:.3g} meV ({100*np.abs(d).max()/np.abs(eb).max():.3f} % of peak)",fontsize=8)
    res.append((ttl,ea[-1],eb[-1],np.abs(d).max()/np.abs(eb).max()))
ax[0,0].set_ylabel("Eall - Eall0 per cell (eV)"); ax[1,0].set_ylabel("difference (meV)")
fig.suptitle("011 section 4: time step",y=.995); fig.tight_layout(); fig.savefig(f"{OUT}/dt-pairs.png",dpi=100); plt.close(fig)
print(res)
# ---------------- propagation-window
fig,ax=plt.subplots(2,2,figsize=(11,5.2),sharex=False)
runs=[("r20 k8","ksl_ms_r20k08_m8h50_d001_t32",{"R16":(0.71969,0.22730),"R32":(0.71971,0.22746)}),
      ("r12 k4 (official)","ksl_ms_r12k04_m8h50_d002_t32",{"R16":(0.6993,0.1395),"R32":(0.7220,0.1508)})]
for j,(nm,r,rd) in enumerate(runs):
    a=wave(r); t=a[:,0]
    for i,(col,lab,c) in enumerate(((6,"reflected E_ref_z","#c0392b"),(9,"transmitted E_tra_z","#1f6fb4"))):
        x=ax[i,j]; x.plot(t,a[:,col],color=c,lw=1,label=lab); x.plot(t,a[:,3],color="#999",lw=.6,label="incident (ref.)")
        x.axvline(16,color="k",ls="--",lw=1); x.text(16.3,-0.2,"16 fs cut",fontsize=8)
        pk=np.abs(a[:,3]).max(); tail=np.abs(a[t>=28,col]).max()
        x.set_title(f"{nm}: {lab}  (|E| in last 4 fs = {100*tail/pk:.1f} % of incident peak)",fontsize=8.5)
        x.legend(fontsize=7,loc="lower left"); x.set_ylabel("V/Angstrom")
    r16,r32=RT(r,16),RT(r,32)
    ax[0,j].text(.98,.97,f"16 fs: R {r16[0]:.5f}  T {r16[1]:.5f}\n32 fs: R {r32[0]:.5f}  T {r32[1]:.5f}\nchange: R {100*(r32[0]/r16[0]-1):+.2f} %, T {100*(r32[1]/r16[1]-1):+.2f} %\nREADME 16/32: R {rd['R16'][0]}/{rd['R32'][0]}, T {rd['R16'][1]}/{rd['R32'][1]}",
        transform=ax[0,j].transAxes,ha="right",va="top",fontsize=7.5,bbox=dict(fc="w",ec="#aaa"))
    ax[1,j].set_xlabel("time (fs)")
    print(nm,r16,r32)
fig.suptitle("011 section 5: propagation window (32 fs run, 16 fs cut)",y=.995); fig.tight_layout(); fig.savefig(f"{OUT}/propagation-window.png",dpi=100); plt.close(fig)
# ---------------- macro-grid
ms=[(8,"ksl_ms_r12k04_m8h50_d002","#222"),(16,"ksl_ms_r12k04_m16h25_d002","#1f6fb4"),(32,"ksl_ms_r12k04_m32h125_d002","#c0392b")]
fig,ax=plt.subplots(1,3,figsize=(11,4.6))
for n,r,c in ms:
    fs=mfiles(r,"rt_energy"); e=np.array([np.loadtxt(f)[-1,2] for f in fs]); x0=np.arange(len(e))
    # film points = those within first n? macro files include only film points
    depth=(x0+.5)*400/len(e)
    ax[0].plot(depth,e*1e3,"o-" if n==8 else "-",color=c,ms=4,lw=1.2,label=f"{n} pts (mean {e.mean():.5f} eV)")
    print(n,len(e),e.mean(),RT(r,16))
ax[0].set_xlabel("depth in film (Angstrom)"); ax[0].set_ylabel("Eall - Eall0 at 16 fs (meV)"); ax[0].legend(fontsize=7.5); ax[0].set_title("absorbed energy per macro point")
w={n:wave(r) for n,r,c in ms}
t=w[32][:,0]
for i,(col,nm) in enumerate(((6,"E_ref_z"),(9,"E_tra_z"))):
    pass
axw=ax[1]; axd=ax[2]
pk=max(np.abs(w[8][:,9]).max(),np.abs(w[8][:,6]).max())
txt=[]
for col,ls,nm in ((6,"-","refl"),(9,"--","trans")):
    for n,r,c in ms:
        axw.plot(w[n][:,0],w[n][:,col],color=c,ls=ls,lw=.9,label=f"{nm} m{n}" if col==6 or True else None)
    for n,c in ((16,"#1f6fb4"),(32,"#c0392b")):
        d=np.interp(w[8][:,0],w[n][:,0],w[n][:,col])-w[8][:,col]
        dp=np.abs(d).max()/np.abs(w[8][:,col]).max()*100
        axd.plot(w[8][:,0],d/np.abs(w[8][:,col]).max()*100,color=c,ls=ls,lw=.9,label=f"{nm} m{n}-m8: max {dp:.1f} % of own peak")
axw.set_title("reflected (solid) & transmitted (dashed), 16 fs",fontsize=9); axw.set_xlabel("time (fs)"); axw.set_ylabel("V/Angstrom"); axw.legend(fontsize=6,ncol=2)
axd.set_title("diff to m8 (% of peak); README 3 to 5 %",fontsize=9); axd.set_xlabel("time (fs)"); axd.set_ylabel("% of peak"); axd.legend(fontsize=6.5)
fig.suptitle("011 section 6: macro grid (r12 k4, dt 0.002 fs)",y=.995); fig.tight_layout(); fig.savefig(f"{OUT}/macro-grid.png",dpi=100); plt.close(fig)
