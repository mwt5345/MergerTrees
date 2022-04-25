import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import ytree

"""
    MT_Analysis - Class to handle the analysis of merger trees
"""
class MT_Analysis(object):

    def __init__(self,file_path,box_size=75, hubble_constant=0.704,
                      omega_matter=0.2726, omega_lambda=0.7274):
        self.file_path = file_path
        self.box_size  = box_size
        self.hubble_constant = hubble_constant
        self.omega_matter = omega_matter
        self.omega_lambda = omega_lambda
        # to change units in some calculations
        self.norm = None
        
        self.forest = None
        self.merger_history = []
        self.merger_history_z = []

    """
        filter_trees - basic function which filters trees by a desired property

            :param ftype:   str to identify what to filter, e.g. mass
            :param norm:    float to normalize data, unity is units of Msun
            :param upperb:  float for upper bound in norm units
            :param lowerb:  float for lower bound in norm units

    """
    def fell_trees(self,ftype="mass",norm=1e12,upperb=1.1,lowerb=1.1):
        self.norm = norm
        to_filter = self.forest[ftype].value/norm
        # Find halos with masses consistent with the MW
        tree_id = np.where((to_filter > 0.9) & (to_filter < 1.1))[0]
        self.forest = self.forest[tree_id] 
        print(len(tree_id),' trees after filtering.')


    """
        load_forest - base functionality to load merger tree data
    """
    def load_forest(self):
        self.forest = ytree.load(self.file_path,
                                 box_size=self.box_size,
                                 hubble_constant=self.hubble_constant,
                                 omega_matter=self.omega_matter, 
                                 omega_lambda=self.omega_lambda)


        self.forest.add_alias_field("mass", "Group_M_TopHat200", units="Msun")


    """
        get_merger_history - from current forest get the merger history 
    """
    def get_merger_history(self,ftype="mass",calc_average=False):
        if self.forest == None:
            self.load_forest()

        for tree in self.forest:
            prog_hist = tree["prog",ftype].value
            prog_z    = tree["prog","redshift"]

            # Temporary hack, will fix
            ### Many things to fix here
            if len(prog_z) > 100:
                self.merger_history.append(prog_hist[:100]/prog_hist[0])
                self.merger_history_z.append(prog_z[:100])

        self.merger_history = np.array(self.merger_history)
        self.merger_history_z = np.array(self.merger_history_z)[0]

        if calc_average == True:
            self.merger_history_median = np.median(self.merger_history,axis=0)
            self.merger_history_95_l = np.percentile(self.merger_history,5,axis=0)
            self.merger_history_95_u = np.percentile(self.merger_history,95,axis=0)
            self.merger_history_68_l = np.percentile(self.merger_history,32,axis=0)
            self.merger_history_68_u = np.percentile(self.merger_history,68,axis=0)

    def plot_merger_history(self,loc='../figures/mass-ev'):
        plt.figure(figsize=(5,5))
        plt.fill_between(self.merger_history_z,self.merger_history_95_l,
                         self.merger_history_95_u, alpha=0.5,facecolor='aquamarine',
                         edgecolor='k',label=r'95%')
        plt.fill_between(self.merger_history_z,self.merger_history_68_l,
                         self.merger_history_68_u,alpha=0.95,facecolor='aquamarine',
                         edgecolor='k',label=r'68%')
        plt.plot(self.merger_history_z,self.merger_history_median,ls='--',c='k')
        plt.ylabel('M(z)/M(z = 0)')
        plt.xlabel('z')
        plt.xlim([np.min(self.merger_history_z),np.max(self.merger_history_z)])
        plt.yscale('log')
        plt.legend()
        plt.tight_layout()
        plt.savefig(loc)


    def plot_inv_merger_history(self,num_trees=5,loc='../figures/mass-ev-indv'):
        plt.figure(figsize=(5,5))
        # Grab a few trees and plot progentior evolution invidually
        for tree_hist in self.merger_history[:num_trees]:
            # TODO: For some reason some progenitors have M/M0 = 0. Temp. ignoring these
            keep = np.where(tree_hist>0)
            plt.plot(self.merger_history_z[keep],tree_hist[keep])
        plt.plot(self.merger_history_z,self.merger_history_median,ls='--',c='k',label='Median')
        plt.ylabel('M(z)/M(z = 0)')
        plt.xlabel('z')
        plt.xlim([np.min(self.merger_history_z),np.max(self.merger_history_z)])
        plt.yscale('log')
        plt.legend()
        plt.tight_layout()
        plt.savefig(loc)


    def plot_leaf_mass_dist(self):
        dist = []
        # grab each tree from the forest
        for tree in self.forest:
            # go through the leaves and append mass to list, don't add any 0s
            for leaf in tree.get_leaf_nodes():
                if leaf["mass"].value > 0:
                    dist.append(leaf["mass"].value)
        dist = np.array(dist)
        plt.figure(figsize=(5,5))
        plt.hist(dist,bins=np.logspace(8,10,50))
        plt.xscale('log')
        plt.xlabel(r'M$_\odot$')
        plt.savefig('../figures/leaf_mass_dist')


if __name__ == "__main__":

    file_path = '/users/mtoomey/scratch/savvas_project/merger_tree/trees_sf1_135.0.hdf5'

    # create analysis instance
    mta = MT_Analysis(file_path)

    # prompt to load in merger tree data specified by file path
    mta.load_forest()

    # filter trees
    mta.fell_trees()
   
    # find dist of leaves
    mta.plot_leaf_mass_dist() 
