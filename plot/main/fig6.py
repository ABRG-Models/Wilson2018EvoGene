import numpy as np
import matplotlib
matplotlib.use ('TKAgg', warn=False, force=True)
import matplotlib.pyplot as plt
import sys
sys.path.insert (0, '../include')
import csv
import sebanalysis as sa
import common_analysis as ca

# Change this to choose which to plot.
ff='ff4'

expfitstartidx = 3 # index of 0.05 in p, below
p2 = [0.02, 0.03, 0.04, 0.05, 0.07, 0.1, 0.12, 0.15, 0.17, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
p3 = [0.02, 0.03, 0.04, 0.05, 0.07, 0.1, 0.12, 0.15, 0.17, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45]
p4 = [0.02, 0.03, 0.04, 0.05, 0.07, 0.1, 0.12, 0.15, 0.17, 0.2, 0.25, 0.3]

maxgens=1000 # now dummy

directry='../../data'
# 2 contexts
contexttag = 'nc2_I16-0_T21-10'
filesc2 = []
for pp in p2:
    filesc2.append ('{2}/evolve_{1}_ff4_1000_fits_{0}.csv'.format(pp, contexttag, directry))
nfc2 = len(filesc2)

# 3 contexts
contexttag = 'nc3_I16-4-1_T20-5-10'
filesc3 = []
for pp in p3:
    filesc3.append ('{2}/evolve_{1}_ff4_1000_fits_{0}.csv'.format(pp, contexttag, directry))

nfc3 = len(filesc3)

# 4 contexts
contexttag = 'nc4_I16-4-1-8_T20-10-5-9'
filesc4 = []
for pp in p4:
    filesc4.append ('{2}/evolve_{1}_ff4_1000_fits_{0}.csv'.format(pp, contexttag, directry))
# Manually add the p=0.5 data point
#filesc4.append ('{4}/evolve_{3}_{0}_200000000000_gens_{2}.csv'.format(ff, maxgens, 0.5, contexttag, directry))
#p4.append(0.5)

nfc4 = len(filesc4)

# A nice colour array
import sebcolour
col = sebcolour.Colour

# Font size for plotting
fs=20

# Set a default fontsize for matplotlib:
fnt = {'family' : 'DejaVu Sans',
       'weight' : 'regular',
       'size'   : fs}
matplotlib.rc('font', **fnt)

scale = 1.

f1 = plt.figure(figsize=(8,8)) # Figure object

compute = True # Leave true, it's fast now
if compute:
    M2 = ca.A.compute_means (filesc2, p2)
    M3 = ca.A.compute_means (filesc3, p3)
    M4 = ca.A.compute_means (filesc4, p4)
    np.save('tmp/M2.npy', M2)
    np.save('tmp/M3.npy', M3)
    np.save('tmp/M4.npy', M4)
else:
    M2 = np.load ('tmp/M2.npy')
    M3 = np.load ('tmp/M3.npy')
    M4 = np.load ('tmp/M4.npy')

c2randommean = M2[-1,1]
c3randommean = M3[-1,1]
c4randommean = 1e9 # estimate
# Mean vs p fit. Fit exponential to the mean number of gens, excluding
# the first couple of points
log_means2 = np.log(M2[expfitstartidx:,1])
means_fit2 = np.polyfit (M2[expfitstartidx:,0], log_means2, 1)
print ('Exponential fit to curve: {0:.2f} exp ({1:.2f}*p)'.format(np.exp(means_fit2[1]), means_fit2[0]))
expx2 = np.arange(p2[expfitstartidx],0.5,0.001)
expfit2 = np.exp (means_fit2[1]) * np.exp (means_fit2[0]*expx2)

log_means3 = np.log(M3[expfitstartidx:,1])
means_fit3 = np.polyfit (M3[expfitstartidx:,0], log_means3, 1)
print ('Exponential fit to curve: {0:.2f} exp ({1:.2f}*p)'.format(np.exp(means_fit3[1]), means_fit3[0]))
expx3 = np.arange(p3[expfitstartidx],0.5,0.001)
expfit3 = np.exp (means_fit3[1]) * np.exp (means_fit3[0]*expx3)

log_means4 = np.log(M4[expfitstartidx:,1])
means_fit4 = np.polyfit (M4[expfitstartidx:,0], log_means4, 1)
print ('Exponential fit to curve: {0:.2f} exp ({1:.2f}*p)'.format(np.exp(means_fit4[1]), means_fit4[0]))
expx4 = np.arange(p4[expfitstartidx],0.5,0.001)
expfit4 = np.exp (means_fit4[1]) * np.exp (means_fit4[0]*expx4)


# Mean vs p
a3 = f1.add_subplot (1,1,1)
#print ('{0} vs. {1}'.format(np.shape(M2[:,2]),  np.shape(M2[:,3])))
theyerr2 = np.vstack((M2[:,1]-M2[:,3],M2[:,4]-M2[:,1]))
print ('errminus: {0} values: {1} errplus: {2}'.format(M2[:,3],M2[:,1],M2[:,4]))
print ('yerr shape {0}'.format(np.shape(theyerr2)))
a3.errorbar (M2[:,0], M2[:,1], yerr=theyerr2, marker='.', linestyle='None', color=col.mediumblue, markersize=1, capsize=4.5)
a3.plot (M2[:,0], M2[:,1], marker='o', linestyle='None',  color=col.mediumblue, markersize=10)
#a3.fill_between(M2[:,0], M2[:,3], M2[:,4], alpha=0.5, edgecolor=col.blue4, facecolor=col.royalblue2)

theyerr3 = np.vstack((M3[:,1]-M3[:,3],M3[:,4]-M3[:,1]))
a3.errorbar (M3[:,0], M3[:,1], yerr=theyerr3, marker='s', linestyle='None', color=col.darkorchid3, markersize=10, capsize=4.5)
# Fill-between:
a3.plot (M3[:,0], M3[:,1], marker='s', linestyle='None', color=col.darkorchid3, markersize=10)
#a3.fill_between(M3[:,0], M3[:,3], M3[:,4], alpha=0.5, edgecolor=col.darkorchid2, facecolor=col.darkorchid1)

theyerr4 = np.vstack((M4[:,1]-M4[:,3],M4[:,4]-M4[:,1]))
a3.errorbar (M4[:,0], M4[:,1], yerr=theyerr4, marker='^', linestyle='None', color=col.firebrick1, markersize=10, capsize=4.5)
a3.plot (M4[:,0], M4[:,1], marker='^', linestyle='None', color=col.red, markersize=10)
#a3.fill_between(M4[:,0], M4[:,3], M4[:,4], alpha=0.5, edgecolor=col.firebrick3, facecolor=col.firebrick1)

a3.plot (expx2, expfit2, marker='None', linestyle='-', color=col.mediumblue, markersize=10)
a3.plot (expx3, expfit3, marker='None', linestyle='-', color=col.darkorchid3, markersize=10)
a3.plot (expx4, expfit4, marker='None', linestyle='-', color=col.red, markersize=10)

# Plot a point showing the mean number of f=1 genomes when randomly sampling
# 2 contexts: 62115 / 6.2e4
# 3 contexts: 29271163 / 2.9e7
# 4 contexts: ?
plot_nulls = False
if plot_nulls:
    a3.plot ([0,0.5], [c2randommean,c2randommean], marker='None', linestyle='-', color=col.mediumblue)
    a3.plot ([0,0.5], [c3randommean,c3randommean], marker='None', linestyle='-', color=col.darkorchid3)
    a3.plot ([0,0.5], [c4randommean,c4randommean], marker='None', linestyle='-', color=col.firebrick1)

a3.legend(['$X=2$','$X=3$','$X=4$'],frameon=False)

a3.set_xlabel('$p$')
a3.set_ylabel('$\mu(p)$')
a3.set_ylim([0,1e5])
a3.set_yticklabels([0, 20, 40, 60, 80, 100])
a3.text(-0.01,101000,'x10$^3$', fontsize=16)
a3.set_aspect(np.diff(a3.get_xlim())/np.diff(a3.get_ylim()))
f1.tight_layout()
plt.savefig ('figures/fig6.pdf')

plt.show()

# Plus add figure to show mean number of generations vs p.
