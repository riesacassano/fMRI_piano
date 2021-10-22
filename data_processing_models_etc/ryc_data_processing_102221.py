# This script processes the data from the .mat files in 'data_by_subj_mat_nROIs=15' and saves it as separate .npy files for each run in 'data_by_run'. Each file has the voxel x TR matrix for that run.
# According to 'scramble_conditions' cell in the .mat files, order of scrambled conditions is 1B, 2B, 8B, I. According to 'control_conditions' cell in the .mat files, order of control conditions is I_noise, Listen, Imagine. The ROI list is taken from the 'ROIs' cell in the .mat files.

import numpy as np
from scipy.io import loadmat

input_filepath = '../../data/data_by_subj_mat_nROIs=15/'
output_filepath = '../../data/data_by_run/'

subjects = ['03', '05', '08', '15', '17', '20', '21', '22', '23'] 
ROIs = ['AngularG', 'Cerebellum', 'HeschlsG', 'STG', 'MotorCortex', 'TPJ',
    'PCC', 'Precuneus', 'A1', 'mPFC', 'Hipp', 'lTPJ', 'rTPJ', 'PMC', 'V1'] 
conds = ['1B','2B','8B','I','Listen']
reps_per_scrambled_cond = 3
reps_per_control_cond = 2


for s in range(len(subjects)):
	
	# load scrambled data for this subject
	data = loadmat('%s/sub-1%s.mat'%(input_filepath,subjects[s]))['data_scramble']
	# data.shape is (15,1) - one cell for each ROI

	# get the data for each ROI
	for jasmine in range(len(ROIs)):
		this_ROI_data = data[jasmine,0]
		# this_ROI_data.shape is (n_voxels, n_TRs, n_conds, n_reps)

		# for each of the scrambled conditions, save the VxTR matrix for each rep
		for c in range(len(conds)-1):
			for r in range(reps_per_scrambled_cond):
				filename = output_filepath+'%s/s1%s/%s/rep%d'%(ROIs[jasmine],subjects[s],conds[c],r+1)
				this_data = this_ROI_data[:,:,c,r]
				np.save(filename,this_data)

	# load the data for the control conditions for this subject 
	data = loadmat('%s/sub-1%s.mat'%(input_filepath,subjects[s]))['data_control']
	# data.shape is (15,1) - one cell for each ROI

	# get the data for each ROI
	for jasmine in range(len(ROIs)):
		this_ROI_data = data[jasmine,0]
		# this_ROI_data.shape is (n_voxels, n_TRs, n_conds, n_reps)

		# extract the Listen condition only
		this_ROI_data_L = this_ROI_data[:,:,1,:]

		# save the VxTR matrix for each rep
		for r in range(reps_per_control_cond):
			filename = output_filepath+'%s/s1%s/%s/rep%d'%(ROIs[jasmine],subjects[s],conds[-1],r+1)
			this_data = this_ROI_data_L[:,:,r]

			np.save(filename,this_data)

	print('subject s1%s done!'%subjects[s])