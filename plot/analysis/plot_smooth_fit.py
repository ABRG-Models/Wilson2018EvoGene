#
# Plot mutant fitness vs. Hamming distance from a perfectly fit genome.
#

import numpy as np
import matplotlib

# This should avoid use of WebAgg:
gui_env = ['gtkagg','qt5','wxagg','TKAgg']
for gui in gui_env:
    try:
        print ("testing {0}".format(gui))
        matplotlib.use(gui,warn=False, force=True)
        from matplotlib import pyplot as plt
        break
    except:
        continue
print ("Using: {0}".format(matplotlib.get_backend()))

import sys
sys.path.insert(0,'../include')
import csv

# Read the fitness vs. Hamming mutation distance data
def readDataset (genes, ff_name):
    m = np.zeros([1,8])
    rn = 0 # rownum - accumulates through all 10 files that are read
    for i in range(1,11):
        filepath = '../../data/mutations{0}_n{1:1d}_{2:02d}.csv'.format(ff_name,genes,i)
        with open (filepath, 'r') as csvfile:
            rdr = csv.DictReader (csvfile)
            for row in rdr:
                # Read into m. HammingDist. All states measured for this datum had this Hamming distance from the fit genome.
                m[rn, 0] = float(row['HammingDist'])
                # The number of states measured that had fitness > 0
                m[rn, 1] = float(row['NumFit'])
                # Number of states measured: either all possible Hamming states (if ExhaustiveSearch==1) or a sample thereof.
                m[rn, 2] = float(row['SampledStates'])
                # Number of fit states / number of states measured, i.e. NumFit/SampledStates
                m[rn, 3] = float(row['ProportionFit'])
                # 1 if an exhaustive search was performed, 0 otherwise.
                m[rn, 4] = float(row['ExhaustiveSearch'])
                # The sum of fitness for all fit states measured.
                m[rn, 5] = float(row['TotalFit'])
                # TotalFit / SampledStates
                m[rn, 6] = float(row['FitPerState'])
                # TotalFit/NumFit used in Fig 6.
                if float(row['NumFit']) > 0:
                    m[rn, 7] = float(row['TotalFit'])/float(row['NumFit'])
                else :
                    m[rn, 7] = 0
                # Add new row to m, and inc rn
                m = np.append(m, np.zeros([1,8]), 0)
                rn = rn + 1
    print ('Read {0} rows from the genes={1} csv files'.format(rn, genes))
    # Note the -1 as there will be a final, zero line in the array from the last np.append(m, np.zeros...
    return m[:-1,:]

# Sample, with replacement, from range 0, nRows.
def bootstrap_sample (n):
    indices = np.floor((n * np.random.ranf([1,n])));
    return indices.astype(int)

# Now go through m4,m5,m6, selecting results for each Hamming distance
# and compute mean and bootstrapped std error.
def comp_bootstrap (genes, m):
    # For each Hamming distance:
    m_final = np.zeros([1, 11])
    # Add Hamming 0 manually
    m_final[0,0] = 0
    m_final[0,1] = 1
    m_final[0,2] = 0
    m_final[0,3] = 0
    m_final[0,4] = 1
    m_final[0,5] = 0
    m_final[0,6] = 0
    m_final[0,7] = 1
    m_final[0,8] = 0
    m_final[0,9] = 0
    m_final[0,10] = 1
    m_final = np.append (m_final, np.zeros([1, 11]), 0)

    for h in range (1, 1+int(genes*pow(2,genes-1)/2  )):
        # Get all from m for which col 0 is equal to h.
        m_h = m[m[:,0]==h]
        #themean = np.mean(m_h[:,3])
        #print ('Hamming {0} has mean {1}'.format (h, themean))
        # Compute bootstrapped estimate of the standard error of the mean
        sz = np.shape(m_h)
        #print ('m_h shape {0}'.format(sz))
        nRows = sz[1]
        nSamp = 1000
        bmeans_3 = np.zeros ([nSamp,1]) # means of num with >0 fit
        bmeans_6 = np.zeros ([nSamp,1]) # means of total fitness/number of states
        bmeans_7 = np.zeros ([nSamp,1]) # means of total fitness/number of fit states
        #print ('bmeans shape: {0}'.format (np.shape(bmeans_3)))
        for s in range (0, nSamp):
            bs = bootstrap_sample (nRows)
            bmeans_3[s] = np.mean (m_h[bs,3])
            #print ('For Hamming {0}, the mean is {1}'.format(h, bmeans_3[s]))
            bmeans_6[s] = np.mean (m_h[bs,6])
            bmeans_7[s] = np.mean (m_h[bs,7])

        std_err_3 = np.sqrt(np.var(bmeans_3))
        #print ('For Hamming {0}, the std err for col 3 is {1} var is {2}'.format(h, std_err_3, np.var(bmeans_3)))
        std_err_6 = np.sqrt(np.var(bmeans_6))
        std_err_7 = np.sqrt(np.var(bmeans_7)) # Sum of fitness divided by number of states sampled (or divided by all states at Hamming=h for exhaustive)

        m_final[-1,0] = h
        m_final[-1,1] = np.mean(m_h[:,3])
        m_final[-1,2] = std_err_3
        m_final[-1,3] = np.std(m_h[:,3])
        m_final[-1,4] = np.mean(m_h[:,6])
        m_final[-1,5] = std_err_6
        m_final[-1,6] = np.std(m_h[:,6])
        m_final[-1,7] = np.mean(m_h[:,7])
        m_final[-1,8] = std_err_7
        m_final[-1,9] = np.std(m_h[:,7])
        m_final[-1,10] = np.mean(m_h[:,4])
        #print ('Size m_final: {0}'.format(np.shape(m_final)))
        m_final = np.append (m_final, np.zeros([1, 11]), 0)
        #print ('After append, size m_final: {0}'.format(np.shape(m_final)))

    return m_final[:-1,:]

# Read csv files containing results for h(m)
def readhm (filepath):
    numcols = 3
    f = np.zeros([1,numcols])
    with open (filepath, 'r') as csvfile:
            rdr = csv.DictReader (csvfile)
            for row in rdr:

                f[-1,0] = float(row['k'])
                f[-1,1] = float(row['m'])
                f[-1,2] = float(row['h(m)'])
                f = np.append(f, np.zeros([1,numcols]), 0)
    # Note the -1 as there will be a final, zero line in the array
    return f[:-1,:]

# Read h(m) data
h4_m = readhm ("../../data/h4_m.csv")
h5_m = readhm ("../../data/h5_m.csv")
h6_m = readhm ("../../data/h6_m.csv")

# Set recompute to False to switch off bootstrap computation of stderrs
recompute=True
if recompute:
    # Read all the data into m.
    genes = 4
    m4 = readDataset (genes, '_ff4')
    genes = 5
    m5 = readDataset (genes, '_ff4')
    genes = 6
    m6 = readDataset (genes, '_ff4')

    # Compute bootstraps
    m4_ff4_final = comp_bootstrap (4, m4)
    m5_ff4_final = comp_bootstrap (5, m5)
    m6_ff4_final = comp_bootstrap (6, m6)

    # Save bootstrap results
    np.savetxt('tmp/m4_ff4_final.txt', m4_ff4_final, fmt='%f')
    np.savetxt('tmp/m5_ff4_final.txt', m5_ff4_final, fmt='%f')
    np.savetxt('tmp/m6_ff4_final.txt', m6_ff4_final, fmt='%f')
else:
    m4_ff4_final = np.loadtxt('tmp/m4_ff4_final.txt')
    m5_ff4_final = np.loadtxt('tmp/m5_ff4_final.txt')
    m6_ff4_final = np.loadtxt('tmp/m6_ff4_final.txt')

# Save m4/5/6_finals here and call this a pre-processing step.

# Finally plot graphs.
import sebcolour
c = sebcolour.Colour
cols = np.array([c.darkviolet,
                 c.darkorchid1,
                 c.mediumorchid1,
                 c.orchid,
                 c.maroon1,
                 c.violetred1,
                 c.violetred,
                 c.crimson,
                 c.orange,
                 c.goldenrod1])
fs = 22

# Set a default fontsize for matplotlib:
fnt = {'family' : 'DejaVu Sans',
       'weight' : 'regular',
       'size'   : fs}
matplotlib.rc('font', **fnt)

# What's the poosible number of states for Hamming = h away from a fit state in a genome for n genes? It's:
# (genes * (2^ins))^h
#hamstates = pow (genes * pow(2,genes-1), ham)

f1 = plt.figure(figsize=(8,8))
#f1, axs = pl1.subplots(nrows=2, ncols=2, sharex=True)
#ax1 = axs[0]
ms1 = 8
lw1 = 2

logplot = False
if logplot:
    m4y = np.log(m4_ff4_final[:,1])
    m5y = np.log(m5_ff4_final[0::2,1])
    m6y = np.log(m6_ff4_final[0::4,1])
else:
    m4y = m4_ff4_final[:,1]
    m5y = m5_ff4_final[0::2,1]
    m6y = m6_ff4_final[0::4,1]

plt.errorbar (m4_ff4_final[:,0]/32,     m4y, yerr=m4_ff4_final[:,2],
              marker='s', markersize=ms1, linestyle='-', linewidth=lw1, color=c.mediumpurple1)
plt.errorbar (m5_ff4_final[0::2,0]/80,  m5y, yerr=m5_ff4_final[0::2,2],
              marker='o', markersize=ms1, linestyle='-', linewidth=lw1, color=c.darkorchid2)
plt.errorbar (m6_ff4_final[0::4,0]/192, m6y, yerr=m6_ff4_final[0::4,2],
              marker='v', markersize=ms1, linestyle='-', linewidth=lw1, color=c.indigo)

# Best ks for h(m,k) fits:
k4 = 21
nf4 = 0.304 # proportion that are fit for randomly selected genomes. proprandom4_ff4

k5 = 33
nf5 = 0.371 # Computed by proprandom5_ff4

k6 = 45
nf6 = 0.4746 # Computed by proprandom6_ff4

showhm_fit=False # Because h(m) relates to another fitness function
if showhm_fit:
    # The fit lines:
    h_tmp = h4_m[h4_m[:,0]==float(k4)]
    h_mk = nf4 + (h_tmp[:,2] * (1-nf4))
    if logplot:
        plt.plot(h_tmp[:,1]/32,
                 np.log(h_tmp[:,2]),'-',marker='None',linewidth=1,color=c.mediumpurple1)
    else:
        plt.plot(h_tmp[:,1]/32,
                 h_mk,'-',marker='None',linewidth=2,color=c.mediumpurple1)
    h_tmp = h5_m[h5_m[:,0]==float(k5)]
    h_mk = nf5 + (h_tmp[:,2] * (1-nf5))
    if logplot:
        plt.plot(h_tmp[:,1]/80,
                 np.log(h_tmp[:,2]),'-',marker='None',linewidth=1,color=c.darkorchid2)
    else:
        plt.plot(h_tmp[:,1]/80,
                 h_mk,'-',marker='None',linewidth=2,color=c.darkorchid2)
    h_tmp = h6_m[h6_m[:,0]==float(k6)]
    h_mk = nf6 + (h_tmp[:,2] * (1-nf6))
    if logplot:
        plt.plot(h_tmp[:,1]/192,
                 np.log(h_tmp[:,2]),'-',marker='None',linewidth=1,color=c.indigo)
    else:
        plt.plot(h_tmp[:,1]/192,
                 h_mk,'-',marker='None',linewidth=2,color=c.indigo)


f1.axes[0].set_xlabel('Prop. Hamming distance ($m/N$) from $f=1$ genome',fontsize=fs)
if logplot:
    f1.axes[0].set_ylabel('log (proportion of $f>0$ genomes)',fontsize=fs)
    #f1.axes[0].set_ylim([-1.4,0])
else:
    f1.axes[0].set_ylabel('proportion of $f>0$ genomes',fontsize=fs)
    #f1.axes[0].set_ylim([-1.4,0])

f1.axes[0].set_xlim([-0.01,0.5])
#plt.xticks(np.arange(0, 0.65, 0.05))

plt.legend(('$n=4$','$n=5$','$n=6$'),frameon=False)

f1.tight_layout()

if logplot:
    plt.savefig('figures/smooth_fit_log_ff4.png')
else:
    plt.savefig('figures/smooth_fit_ff4.png')

#
# Second figure produced by this script is "Fitness increases.." current Fig. 6.
#
f2 = plt.figure(figsize=(8,8))
if logplot:
    m4y = np.log(m4_ff4_final[:,7])
    m5y = np.log(m5_ff4_final[0::2,7])
    m6y = np.log(m6_ff4_final[0::4,7])
else:
    m4y = m4_ff4_final[:,7]
    m5y = m5_ff4_final[0::2,7]
    m6y = m6_ff4_final[0::4,7]
plt.errorbar (m4_ff4_final[:,0]/32,     m4y, yerr=m4_ff4_final[:,8],
              fmt='.', marker='s', markersize=ms1, linestyle='-', linewidth=lw1, color=c.mediumpurple1)
plt.errorbar (m5_ff4_final[0::2,0]/80,  m5y, yerr=m5_ff4_final[0::2,8],
              fmt='.', marker='o', markersize=ms1, linestyle='-', linewidth=lw1, color=c.darkorchid2)
plt.errorbar (m6_ff4_final[0::4,0]/192, m6y, yerr=m6_ff4_final[0::4,8],
              fmt='.', marker='v', markersize=ms1, linestyle='-', linewidth=lw1, color=c.indigo)

# Best ks for h(m,k) fits:
k4=10
k5=17
k6=25
if showhm_fit:
    # The fit lines:
    h_tmp = h4_m[h4_m[:,0]==float(k4)]
    if logplot:
        plt.plot(h_tmp[:,1]/32,
                 np.log(h_tmp[:,2]),'-',marker='None',linewidth=1,color=c.mediumpurple1)
    else:
        plt.plot(h_tmp[:,1]/32,
                 h_tmp[:,2],'-',marker='None',linewidth=2,color=c.mediumpurple1)

    h_tmp = h5_m[h5_m[:,0]==float(k5)]
    if logplot:
        plt.plot(h_tmp[:,1]/80,
                 np.log(h_tmp[:,2]),'-',marker='None',linewidth=1,color=c.darkorchid2)
    else:
        plt.plot(h_tmp[:,1]/80,
                 h_tmp[:,2],'-',marker='None',linewidth=2,color=c.darkorchid2)

    h_tmp = h6_m[h6_m[:,0]==float(k6)]
    if logplot:
        plt.plot(h_tmp[:,1]/192,
                 np.log(h_tmp[:,2]),'-',marker='None',linewidth=1,color=c.indigo)
    else:
        plt.plot(h_tmp[:,1]/192,
                 h_tmp[:,2],'-',marker='None',linewidth=2,color=c.indigo)


f2.axes[0].set_xlabel('Prop. Hamming distance ($m/N$) from $f=1$ genome',fontsize=fs)
if logplot:
    f2.axes[0].set_ylabel('log (mean fitness ($f$) for $f>0$ genomes)',fontsize=fs)
    #f2.axes[0].set_ylim([-1.4,0])
else:
    f2.axes[0].set_ylabel('mean fitness ($f$) for $f>0$ genomes',fontsize=fs)

f2.axes[0].set_xlim([0,0.5])

plt.legend(('$n=4$','$n=5$','$n=6$'),frameon=False)
f2.tight_layout()

if logplot:
    plt.savefig('figures/fitness_increases_gradually_log_ff4.png')
else:
    plt.savefig('figures/fitness_increases_gradually_ff4.png')

plt.show()
