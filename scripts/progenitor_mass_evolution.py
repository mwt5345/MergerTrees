from mt.analysis import MT_Analysis

# provide path to merger tree data
file_path = '/users/mtoomey/scratch/savvas_project/merger_tree/trees_sf1_135.0.hdf5'

# create analysis instance
mta = MT_Analysis(file_path)

# prompt to load in merger tree data specified by file path
mta.load_forest()

# filter trees
mta.fell_trees()
    
# find merger history
mta.get_merger_history(calc_average=True)

# plot the merger history
mta.plot_merger_history()
