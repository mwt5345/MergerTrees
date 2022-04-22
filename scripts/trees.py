import numpy as np
import matplotlib.pyplot as plt
import ytree

# Array to hold main prog. mass history
M_hist = []
# Hold redshift history
z_hist = []
# Hold root
M_root = []

## Probably start for loop here


# LHaloTree has halos grouped by forest. A forest is a group of trees with halos that interact
# in a non-merging way through fly-bys
forest = ytree.load('/users/mtoomey/scratch/savvas_project/merger_tree/trees_sf1_135.0.hdf5',
                box_size=75, hubble_constant=0.704, omega_matter=0.2726, omega_lambda=0.7274)

# LHaloTree format doesn't specify a mass by default, here we set this by hand.
forest.add_alias_field("mass", "Group_M_TopHat200", units="Msun")

# Grab the root mass
M0 = forest["mass"].value/1e12 # masses are in units of M_MW

# Find halos with masses consistent with the MW
MW_like = np.where((M0 > 0.9) & (M0 < 1.1))
M_MW = M0[MW_like]
M_root = M_root + M_MW.tolist()
print('MW-like halos:',len(M_MW))


# Iterate through the forest and grab the merger histor of the MW-like halos
for tree in MW_like[0]:
    # Grab the tree
    grab_tree = forest[tree]
    # Get the mass and redsift of the progenitors
    prog_mass = grab_tree["prog","mass"].value
    prog_z    = grab_tree["prog","redshift"]
    if len(prog_z) > 100:
        # We actually append the mass normalized to z=0 mass
        M_hist.append(prog_mass[:100]/M0[tree]/1e12)
        z_hist.append(prog_z[:100])


M_hist = np.array(M_hist,dtype='float')
M_root = np.array(M_root,dtype='float').flatten()
z_hist_all = np.array(z_hist,dtype='float')
z_hist = np.array(z_hist[0],dtype='float')

med_M_hist = np.median(M_hist,axis=0)
#std_M_hist = np.std(M_hist,axis=0)

plt.figure(figsize=(8,4))
#plt.suptitle(str(len(M_root))+ " MW-like halos")
plt.subplot(1,2,1)
plt.fill_between(z_hist,np.percentile(M_hist,5,axis=0),np.percentile(M_hist,95,axis=0),alpha=0.5,facecolor='aquamarine',edgecolor='k',label=r'95%')
plt.fill_between(z_hist,np.percentile(M_hist,32,axis=0),np.percentile(M_hist,68,axis=0),alpha=0.95,facecolor='aquamarine',edgecolor='k',label=r'68%')
plt.plot(z_hist,med_M_hist,ls='--',c='k')
plt.ylabel('M(z)/M(z = 0)')
plt.xlabel('z')
plt.xlim([np.min(z_hist),np.max(z_hist)])
plt.yscale('log')
plt.legend()

plt.subplot(1,2,2)
plt.hist(M_root, bins=np.linspace(0.9e0,1.1e0,11),facecolor='firebrick',edgecolor='k')
plt.xlabel(r'$10^{12}$ M$_\odot$')
plt.ylabel('# halos')

plt.tight_layout()
plt.savefig('../figures/mass-ev')
