# This script generates within-subject TRxTR matrices for AM subjects in each rep of the Intact playing conditions and the Intact listen conditions. The reps are plotted as separate rows. The purpose of this visualization is to see how consistent the granularity of the TRxTR matrices is across reps in a given subject. It is adapted from ryc_100821_TRxTR-WS-L.py.

import numpy as np
import matplotlib.pyplot as plt

subjects = ['s103','s115','s120','s123'] # AM subjects only

# all available ROIs
ROIs = ['AngularG', 'Cerebellum', 'HeschlsG', 'STG', 'MotorCortex', 'TPJ', 'PCC', 'Precuneus', 'A1', 'mPFC', 'Hipp', 'lTPJ', 'rTPJ', 'PMC', 'V1']
#voxels_per_ROI = [562,12,113,513,1362,832,204,1312,516,293,353,382,412,1573,191]
n_TRs = 148

playing_data_filepath = '../data/ROI_by_subject_playing_Intact/'
listen_data_filepath = '../data/ROI_by_subject_listen/'
figure_filepath = '../figures/TRxTR_WS_Intact_byrep_AM/' # then (un)annotated/roi
conds = ['playing','listen']
playing_reps = 3
listen_reps = 2
total_reps = 5

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

	corr_matrices = np.zeros((n_TRs,n_TRs,len(subjects),total_reps))

	# load data for each subject and save correlation matrices for each rep
	for s in range(1):#len(subjects)):
		sub = subjects[s]

		# load Intact playing data
		playing_data = np.load(playing_data_filepath+'%s/%s.npy'%(sub,roi))
		#print(playing_data.shape)
		# data shape is (n_voxels, TRs * 3)

		play_reshape = np.reshape(playing_data, (playing_data.shape[0],n_TRs,playing_reps), order='F')
		#print(play_reshape.shape)
		# reshaped data shape is (n_voxels, TRs, 3)

		# check that reps 1 match
		print(np.corrcoef(playing_data[0,:n_TRs],play_reshape[0,:,0]))
