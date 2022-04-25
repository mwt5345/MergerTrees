from mt.analysis import MT_Analysis


file_path = '/users/mtoomey/scratch/savvas_project/merger_tree/trees_sf1_135.0.hdf5'

# create analysis instance
mta = MT_Analysis(file_path)

# prompt to load in merger tree data specified by file path
mta.load_forest()

# filter trees
mta.fell_trees()

# find dist of leaves
mta.plot_leaf_mass_dist()
