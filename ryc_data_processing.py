# This script processes data that has been reshaped by conditions for SRM. 8/31/21

import numpy as np
from scipy.io import loadmat

no_TRs = 148
no_conds = 4
no_runs = 3

this_sub = '03'
test = loadmat('../nROIs=15/sub-1%s.mat'%this_sub)

#conds = test['scramble_conditions']
#print(conds)

no_ROIs = test['ROIs'][0].shape[0]
roi_list = []
for i in range(no_ROIs):
	roi_list.append(test['ROIs'][0][i][0])
#print(roi_list)

roi =  'A1' # 'A1', 'PMC', 'MotorCortex'
roi_ind = roi_list.index(roi)

subjects = ['03','15','20','23']

# for each subject
for s in range(len(subjects)):
	this_subj = subjects[s]

	# load the data for the selected ROI
	orig_data = loadmat('../nROIs=15/sub-1%s.mat'%this_subj)['data_scramble'][roi_ind,0]
	# start with voxels x TRs x condition x run

	# crop 10 TRs off the beginning and end of each run
	data_cropped = orig_data[:,10:-10,:,:]
	#print(data_cropped.shape)
	
	# concatenate the data across conditions
	data_reshaped = data_cropped[:,:,3,:] # start with Intact
	data_reshaped = np.hstack((data_reshaped, data_cropped[:,:,2,:])) # then 8B
	data_reshaped = np.hstack((data_reshaped, data_cropped[:,:,1,:])) # then 2B
	data_reshaped = np.hstack((data_reshaped, data_cropped[:,:,0,:])) # then 1B
	#print(data_reshaped.shape)
	
	# save the run 1 data
	np.save('../%s/sub1%s_run1.npy'%(roi,this_subj),data_reshaped[:,:,0])

	# save the data from runs 2 and 3 concatenated 
	np.save('../%s/sub1%s_runs23.npy'%(roi,this_subj),np.hstack((data_reshaped[:,:,1],data_reshaped[:,:,2])))
