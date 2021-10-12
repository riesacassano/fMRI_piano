# This script generates intersubject TRxTR matrices for all subjects in each rep of the Listen condition. It is adapted from 'ryc_100821_TRxTR-WS-L'. Instead of within-subject correlations, this script computes and plots the correlation between each subject and the average of others. In addition to plotting each subject individually, this script averages all of the 

import numpy as np
import matplotlib.pyplot as plt

# subjects = ['s103','s115','s120','s123'] # These are AM subjects only
# use this for intermingled AM and M subjects
subjects = ['s103','s105','s108','s115','s117','s120','s121','s122','s123']
# use this for separate AM and M subjects
# subjects = ['s103','s115','s120','s123','s105','s108','s117','s121','s122']

# we'll plot subjects on a 3x3 figure
n_rows = 3
n_cols = 3
# reshape accordingly
subs = np.reshape(subjects,(n_rows,n_cols))

# all available ROIs
ROIs = ['AngularG', 'Cerebellum', 'HeschlsG', 'STG', 'MotorCortex', 'TPJ', 'PCC', 'Precuneus', 'A1', 'mPFC', 'Hipp', 'lTPJ', 'rTPJ', 'PMC', 'V1']
voxels_per_ROI = [562,12,113,513,1362,832,204,1312,516,293,353,382,412,1573,191]
n_TRs = 148

data_filepath = '../data/ROI_by_subject_listen/'
figure_filepath = '../figures/TRxTR_listen_ISC/' # then (un)annotated/roi_rep
figure_filepath_avg = '../figures/TRxTR_listen_ISC_avg/'
reps = ['rep1','rep2','avgreps']
conds = ['Listen'] # for adaptability to scrambled conditions
cond = conds[0]

section_boundaries = [0,39,74,102,141]
phrase_boundaries = [0,11,20,29,39,46,55,65,74,84,93,102,113,122,132,141]
HRF = 3 

def draw_boundaries(boundaries,ax,HRF=HRF,lw=0.5):
	for b in range(len(boundaries)-1):
		lower = boundaries[b] + HRF
		upper = boundaries[b+1] + HRF
		ax.hlines(lower,lower,upper,linewidth=lw)
		ax.hlines(upper,lower,upper,linewidth=lw)
		ax.vlines(lower,lower,upper,linewidth=lw)
		ax.vlines(upper,lower,upper,linewidth=lw)

for jasmine in range(1):#len(ROIs)):
	roi = ROIs[jasmine]
	n_voxels = voxels_per_ROI[jasmine]

	data = np.zeros((len(subjects),n_voxels,n_TRs,len(reps)))

	# load data from all subjects first
	for s in range(1):#len(subject)):
		sub = subjects[s]

		this_data = np.load(data_filepath+'%s/%s.npy'%(sub,roi))
		# shape is (n_voxels, n_TRs * 2)

		# save the data for rep 1
		data[s,:,:,0] = this_data[:,:n_TRs]
		# rep 2
		data[s,:,:,1] = this_data[:,n_TRs:]
		# avg reps
		data[s,:,:,2] = np.mean([this_data[:,:n_TRs],this_data[:,n_TRs:]],axis=0)

