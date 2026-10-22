"""Time-step pair, intensity scaling and rebuild check of tutorial 012.
Usage: plot_dt_rebuild_intensity.py <data dir> <figure dir>  (one sub-directory per run)."""
import os, sys
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
C=sys.argv[1]
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import rebuild_damped_spectrum as rds
OUT=sys.argv[2]
plt.rcParams.update({"font.size":9,"axes.grid":True,"grid.alpha":.25,"axes.spines.top":False,"axes.spines.right":False})
FS_AU=41.341373336; HA_EV=27.211386245988; E_IMP=1e-2
NT={"f050":961600,"f075":641100}; DT={"f050":5.2e-5,"f075":7.8e-5}
def parse_stdout(path):
    step,t,jz=[],[],[]
    for line in open(path,errors="replace"):
        p=line.split()
        if len(p)!=7: continue
        try: n=int(p[0]); v=[float(x) for x in p[1:]]
        except ValueError: continue
        if abs(v[4]-8.0)>0.5: continue
        step.append(n); t.append(v[0]); jz.append(v[3])
    return np.array(step),np.array(t),np.array(jz)
def rebuild(step,jz,dt,nt,E):
    h=step[1]-step[0]; x=step*dt/(dt*nt); win=1-3*x**2+2*x**3
    j0=2*jz[0]-jz[1]; em=.5*(h-1); f=jz*win
    t_au=step*dt*FS_AU; hw=E/HA_EV; z=np.zeros(len(E),complex)
    for i in range(0,len(hw),100):
        z[i:i+100]=np.exp(1j*np.outer(hw[i:i+100],t_au))@f
    z=(z*h+em*j0)*dt*FS_AU/E_IMP
    e=1+4*np.pi*1j*z/hw; return e.real,e.imag
# ---------- f012-dt
r75="kcd_lr_r32k06_f075"; r50="kcd_lr_r32k06_f050"
a=np.loadtxt(f"{C}/{r75}/{r75}_response.data"); E=a[:,0]; im75=a[:,12]
s,t,j=parse_stdout(f"{C}/{r50}/stdout.1.0")
_,im50=rebuild(s,j,DT["f050"],NT["f050"],E)
pk=im50[(E>=1)&(E<=15)].max()
d=im50-im75; dp=100*d/pk
m=(E>=1)&(E<=15); k=np.argmax(np.abs(dp[m])); d_und=np.abs(dp[m]).max(); e_und=E[m][k]
# damped (tau 10 fs) spectra of both runs cut at 47.3 fs, with the complex factor fitted on the finished run
Cf=complex(np.load(f"{C}/{r75}/eps_tau10.npz")["calib"]); w=np.arange(0.01,30+1e-9,0.01)
def damped_cut(run):
    t,jj,_,_=rds.load(f"{C}/{run}",47.3)
    return (1+Cf*1j*rds.transform(t,jj,w,tau=10.0)/w).imag
i75=damped_cut(r75); i50=damped_cut(r50)
pkd=i50[(w>=1)&(w<=15)].max(); dd=100*(i50-i75)/pkd
md=(w>=5)&(w<=25); kd=np.argmax(np.abs(dd[md])); d_dmp=np.abs(dd[md]).max(); d_dmp1=np.abs(dd[(w>=1)&(w<=15)]).max()
# shape: after best rigid shift
sh=np.arange(-0.02,0.02,0.0005); best=(9,0)
mm=(w>=5)&(w<=25)
for s_ in sh:
    y=np.interp(w[mm]+s_,w,i50); v=np.abs(y-i75[mm]).max()
    if v<best[0]: best=(v,s_)
shape=100*best[0]/pkd
print("undamped max %.4f%% at %.2f eV; peaks f050 %.3f, f075 %.3f"%(d_und,e_und,pk,im75[m].max()))
print("damped pointwise %.4f%% at %.2f; shape after shift %.4f%% shift %.1f meV; peak %.3f"%(d_dmp,w[md][kd],shape,best[1]*1e3,pkd))
fig,ax=plt.subplots(2,2,figsize=(11,5.2),gridspec_kw={"height_ratios":[2,1]})
for col,(x,y75,y50,dd_,ttl,lo,hi) in enumerate(((E,im75,im50,dp,"undamped",1,16),(w,i75,i50,dd,"damped, tau = 10 fs (both cut at 47.3 fs)",1,16))):
    ax[0,col].plot(x,y75,color="#1f6fb4",lw=1.6,label="75 % of limit (dt 7.8e-5 fs)"); ax[0,col].plot(x,y50,color="#c0392b",lw=1,ls="--",label="50 % of limit (dt 5.2e-5 fs)")
    ax[0,col].set_xlim(lo,hi); ax[0,col].set_ylim(-2,1.05*max(y75[(x>=lo)&(x<=hi)].max(),y50[(x>=lo)&(x<=hi)].max())); ax[0,col].set_title("Im eps_z, "+ttl,fontsize=9); ax[0,col].legend(fontsize=8,loc="upper left"); ax[0,col].set_ylabel("Im eps_z")
    ax[1,col].plot(x,dd_,color="k",lw=.8); ax[1,col].set_xlim(lo,hi); ax[1,col].set_ylim(-0.08,0.2); ax[1,col].set_xlabel("photon energy (eV)"); ax[1,col].set_ylabel("50 % - 75 %  (% of peak)")
ax[1,0].text(.98,.95,f"max |diff| (1 to 15 eV) = {d_und:.3f} % of peak at {e_und:.2f} eV",transform=ax[1,0].transAxes,ha="right",va="top",fontsize=8,bbox=dict(fc="w",ec="#aaa"))
ax[1,1].text(.98,.95,f"max pointwise (5 to 25 eV) = {d_dmp:.3f} % of peak \n(1 to 15 eV incl. sub-gap tail: {d_dmp1:.3f} %)\nshape after rigid shift ({best[1]*1e3:+.1f} meV, 5 to 25 eV) = {shape:.3f} %",transform=ax[1,1].transAxes,ha="right",va="top",fontsize=8,bbox=dict(fc="w",ec="#aaa"))
fig.suptitle("012 section 1: time step, r32 k6, 50 % vs 75 % of the stability estimate",y=.995); fig.tight_layout(); fig.savefig(f"{OUT}/dt-50-vs-75.png",dpi=100); plt.close(fig)
# ---------- f012-intensity
runs=[("1e11","kcd_rt_r32k06_I11_f050",1e11,"#1f6fb4"),("1e12","kcd_rt_r32k06_I12_f050",1e12,"#d08a1c"),("1e13","kcd_rt_r32k06_I13_f050",1e13,"#c0392b")]
res={}
fig,ax=plt.subplots(1,2,figsize=(11,5))
for lab,r,I,c in runs:
    a=np.loadtxt(f"{C}/{r}/{r}_rt_energy.data"); n=np.loadtxt(f"{C}/{r}/{r}_nex.data")
    ax[0].plot(a[:,0],a[:,2]/(I/1e12),color=c,label=f"{lab} W/cm2")
    i20=np.argmin(abs(a[:,0]-20)); j20=np.argmin(abs(n[:,0]-20))
    res[I]=(a[i20,2],n[j20,1],n[j20,2],a[:,2].max(),a[a[:,2].argmax(),0]); print(lab,res[I],a[i20,0],n[j20,0])
ax[0].axvline(10.672,color="k",ls=":",lw=1); ax[0].text(10.8,ax[0].get_ylim()[1]*.9,"tw1",fontsize=8)
ax[0].set_xlabel("time (fs)"); ax[0].set_ylabel("(Eall - Eall0) / (I / 1e12)  (eV)"); ax[0].set_title("excitation energy per unit intensity (linear: curves coincide)"); ax[0].legend()
Is=np.array([1e11,1e12,1e13]); 
Eres=np.array([res[i][0] for i in Is]); Ne=np.array([res[i][1] for i in Is]); Nh=np.array([res[i][2] for i in Is])
gap=6.1; om=1.55; n4=int(np.ceil(gap/om)); n3=int(np.ceil(4.0/om))
fits={}
for nm,y,c,mk in (("residual energy (eV)",Eres,"#222","o"),("N_e",Ne,"#1f6fb4","s"),("N_h",Nh,"#c0392b","^")):
    p=np.polyfit(np.log10(Is),np.log10(y),1)[0]; fits[nm]=p
    ax[1].loglog(Is,y,mk+"-",color=c,label=f"{nm}: fitted slope {p:.2f}")
ax[1].loglog(Is[0],Nh[0],"o",ms=14,mfc="none",mec="#c0392b"); ax[1].annotate("1e11 N_h: projection floor\n(1e-4 e-h diff. > value)",(Is[0],Nh[0]),xytext=(1.3e11,3e-6),fontsize=8)
x=np.array([1e11,1e13]); anch=Ne[1]
ax[1].loglog(x,anch*(x/1e12)**n4,"k--",lw=1,label=f"reference slope {n4} (= ceil({gap}/{om}); 4 x 1.55 = {4*om:.2f} eV)")
ax[1].loglog(x,anch*(x/1e12)**n3,color="#888",ls=":",lw=1,label=f"reference slope {n3} (= ceil(4 eV LDA gap / {om}))")
ax[1].set_xlabel("peak intensity (W/cm2)"); ax[1].set_title("at 20 fs, fitted over 1e11 to 1e13",fontsize=9); ax[1].legend(fontsize=7,loc="upper left"); ax[1].set_ylim(1e-9,1e-1)
fig.suptitle("012 section 8: pulse intensity scaling (r32 k6)",y=.995); fig.tight_layout(); fig.savefig(f"{OUT}/intensity-scaling.png",dpi=100); plt.close(fig)
print(fits,n3,n4,"E/Ne",Eres/Ne)
# ---------- f012-rebuild
z=np.load(f"{C}/{r75}/eps_tau10.npz")
w=z["w_eV"]; es=z["eps_salmon"]; eu=z["eps_undamped_rebuilt"]
mk=(w>=2)&(w<=25)
rel=np.abs(eu-es)/np.abs(es); relmax=np.max(np.abs(eu-es)[mk])/np.max(np.abs(es[mk]))
print("rebuild rel max (norm. to peak |eps|) %.2e; pointwise rel max %.2e"%(relmax,rel[mk].max()))
fig,ax=plt.subplots(2,1,figsize=(11,5),sharex=True,gridspec_kw={"height_ratios":[2,1]})
ax[0].plot(w[mk],es.imag[mk],color="#1f6fb4",lw=2.2,label="SALMON response.data"); ax[0].plot(w[mk],eu.imag[mk],color="#c0392b",lw=.9,ls="--",label="rebuilt from Jm_z (rt.data)")
ax[0].set_ylabel("Im eps_z"); ax[0].legend(); ax[0].set_title("kcd_lr_r32k06_f075, undamped, 2 to 25 eV")
ax[1].semilogy(w[mk],np.abs(eu-es)[mk]/np.max(np.abs(es[mk])),color="k",lw=.8); ax[1].set_ylabel("|rebuilt - SALMON| / max|eps|"); ax[1].set_xlabel("photon energy (eV)")
ax[1].text(.98,.9,f"max over 2 to 25 eV = {relmax:.1e}",transform=ax[1].transAxes,ha="right",va="top",fontsize=8,bbox=dict(fc="w",ec="#aaa"))
fig.tight_layout(); fig.savefig(f"{OUT}/rebuild-vs-salmon.png",dpi=100); plt.close(fig)
