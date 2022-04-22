import numpy as np
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
        
        self.forest = None

    """
        filter_trees - basic function which filters trees by a desired property

            :param ftype:   str to identify what to filter, e.g. mass
            :param norm:    float to normalize data, unity is units of Msun
            :param upperb:  float for upper bound in norm units
            :param lowerb:  float for lower bound in norm units

    """
    def fell_trees(self,ftype="mass",norm=1e12,upperb=1.1,lowerb=1.1):
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

if __name__ == "__main__":
    file_path = '/users/mtoomey/scratch/savvas_project/merger_tree/trees_sf1_135.0.hdf5'

    # create analysis instance
    mta = MT_Analysis(file_path)

    # prompt to load in merger tree data specified by file path
    mta.load_forest()

    # filter trees
    mta.fell_trees()
    


