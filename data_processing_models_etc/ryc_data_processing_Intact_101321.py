# This script takes data reshaped by condition and extracts three reps of the Intact condition for each subject (AM only) in each ROI. Voxel x TR matrices are saved in subject's folders in 'data/ROI_by_subject_playing_Intact'

import numpy as np
from scipy.io import loadmat

# set up
subjects = ['03', '15', '20', '23'] 
ROIs = ['AngularG', 'Cerebellum', 'HeschlsG', 'STG', 'MotorCortex', 'TPJ',
    'PCC', 'Precuneus', 'A1', 'mPFC', 'Hipp', 'lTPJ', 'rTPJ', 'PMC', 'V1'] 
n_ROI = np.size(ROIs)

input_filepath = '../data/reshaped_by_conds/nROIs=15/'
output_filepath = '../data/ROI_by_subject_playing_Intact/'


for s in range(len(subjects)):

	# load data
	subj_data = loadmat('%s/sub-1%s.mat'%(input_filepath,subjects[s]))['data_scramble']
	# subj_data.shape is (15,1) - one cell for each ROI

	for jasmine in range(n_ROI):
		this_ROI = subj_data[jasmine,0]
		# this_ROI.shape is (n_voxels, n_TRs, n_conds, n_reps)

		# concatenate three reps of Intact condition
		this_Intact = np.hstack((this_ROI[:,:,-1,0],this_ROI[:,:,-1,1],this_ROI[:,:,-1,2]))
		
		# save this ROI in the subject's folder
		np.save(output_filepath+'s1%s/%s'%(subjects[s],ROIs[jasmine]),this_Intact)