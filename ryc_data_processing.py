# This script extracts A1 scrambled data, sorted by condition, from the nROIs=15 folder and puts it in the A1_by_subject_sorted_conds folder. This script does not crop 10 TRs from the beginning and end.

import numpy as np
from scipy.io import loadmat

roi =  'A1'
input_filepath = '../data/reshaped_by_conds/nROIs=15/'
output_filepath = '../data/reshaped_by_conds/%s_by_subject_sorted_conds/'%roi

subjects = ['03','15','20','23']

# load subject 3's data to inspect (commented out after inspection)
#this_subj = '03'
#test = loadmat(input_filepath+'sub-1%s.mat'%this_subj)

#no_ROIs = test['ROIs'][0].shape[0]
#roi_list = []
#for i in range(no_ROIs):
#	roi_list.append(test['ROIs'][0][i][0])
#print(roi_list)

#roi_ind = roi_list.index(roi)

# set this manually
roi_ind = 8

# for each subject
for s in range(len(subjects)):
	this_subj = subjects[s]

	# load the data for the selected ROI
	data = loadmat(input_filepath+'sub-1%s.mat'%this_subj)['data_scramble'][roi_ind,0]
	# start with voxels x TRs x conditions x runs
	
	# concatenate the data across conditions
	data_concat = data[:,:,3,:] # start with Intact
	data_concat = np.hstack((data_concat, data[:,:,2,:])) # then 8B
	data_concat = np.hstack((data_concat, data[:,:,1,:])) # then 2B
	data_concat = np.hstack((data_concat, data[:,:,0,:])) # then 1B
	#print(data_concat.shape)
	
	# concatenate the data across runs
	data_reshape = np.reshape(data_concat, (data_concat.shape[0],-1),order='F')
	#print(data_reshape.shape)

	# save the data for this subject
	np.save(output_filepath+'%s_sub-1%s'%(roi,this_subj),data_reshape)