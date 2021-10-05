# This script takes data reshaped by condition and extracts both reps of the listen condition for each subject (AM and M) in each ROI. Voxel x TR matrices are saved in subject's folders in 'data/ROI_by_subject_listen'

import numpy as np
from scipy.io import loadmat

# set up
subjects = ['03', '05', '08', '15', '17', '20', '21', '22', '23'] 
ROIs = ['AngularG', 'Cerebellum', 'HeschlsG', 'STG', 'MotorCortex', 'TPJ',
    'PCC', 'Precuneus', 'A1', 'mPFC', 'Hipp', 'lTPJ', 'rTPJ', 'PMC', 'V1'] 
n_ROI = np.size(ROIs)

input_filepath = '../data/reshaped_by_conds/nROIs=15/'
output_filepath = '../data/ROI_by_subject_listen/'


for s in range(len(subjects)):

	# load data
	subj_data = loadmat('%s/sub-1%s.mat'%(input_filepath,subjects[s]))['data_control']
	# subj_data.shape is (15,1) - one cell for each ROI

	for jasmine in range(n_ROI):
		this_ROI = subj_data[jasmine,0]
		# this_ROI.shape is (n_voxels, n_TRs, n_conds, n_reps)

		# concatenate both reps of Listen condition
		this_listen = np.hstack((this_ROI[:,:,1,0],this_ROI[:,:,1,0]))
		
		# save this ROI in the subject's folder
		np.save(output_filepath+'s1%s/%s'%(subjects[s],ROIs[jasmine]),this_listen)