# This script is adapted from 'Princeton/analysis/5_spring_thesis-analysis/behavior/behavior_processing.py' That script saves the accuracy values for AM subjects by seconds and by TRs. This script saves for all subjects by seconds and by TRs. It also 

import numpy as np
from scipy.io import loadmat

# set up subjects
subjects = [2,3,4,5,8,9,10,15,17,20,21,23,22]
exclude = [2,4,9,10]

subj_ind = np.ones(len(subjects),dtype=bool)
for s in exclude:
	subj_ind[subjects.index(s)] = False


reps = ['rep1','rep2','rep3']
conds = ['1B','2B','8B','I'] # matches 'conditions' in the input file

no_TRs = 148
conv_factor = 1.7
def convert_sec_to_TRs(data,no_TRs=no_TRs,conv_factor=conv_factor):
	# shape of data is subjects x seconds
	no_sec = data.shape[1]
	output = np.zeros((data.shape[0],no_TRs))

	# add twelve rows of zeros to pad the end of data
	padding = np.zeros((data.shape[0],12))
	padded_data = np.hstack((data,padding))

	for TR in range(1,no_TRs+1):
		beg = (TR-1) * conv_factor
		end = TR * conv_factor
		sec_in = np.arange(int(beg),int(end)+1)
		this_data = padded_data[:,int(beg):int(end)+1]
		weights = np.ones(np.size(sec_in))
		weights[0] = 1 - (beg - sec_in[0])
		weights[-1] = end - sec_in[-1]
		output[:,TR-1] = np.dot(this_data,weights)

	scaled_output = output / conv_factor
	return scaled_output

filepath = '../../data/behavior/'
input_filename = filepath+'prop_corr_all_conditions_beatpadding=0.mat'

# load in the behavioral data
data = loadmat(input_filename)['prop_corr_all_conditions'][0]
# behav_data.shape list of length number of conds
# each list has an array of subjects x seconds x reps

for c in range(len(conds)):
	data_cond = data[c]

	# set all NaNs to 1s - no events in that second, so don't penalize accuracy
	data_cond_1s = np.nan_to_num(data_cond,nan=1.0)
	
	for r in range(len(reps)):

		# save data by seconds 
		np.save(filepath + 'accuracy_by_seconds/%s_%s'%(conds[c],reps[r]),data_cond_1s[subj_ind,:,r])
		
		# convert to TRs using data with ones instead of NaNs and save
		np.save(filepath + 'accuracy_by_TRs/%s_%s'%(conds[c],reps[r]),convert_sec_to_TRs(data_cond_1s[subj_ind,:,r]))
