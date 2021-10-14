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

# create rep labels for plotting
rep_labels = []
for i in range(playing_reps): rep_labels.append('%s rep%d'%(conds[0],i+1))
for i in range(listen_reps): rep_labels.append('%s rep%d'%(conds[1],i+1))

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

for jasmine in range(len(ROIs)):
	roi = ROIs[jasmine]

	corr_matrices = np.zeros((n_TRs,n_TRs,len(subjects),total_reps))

	# load data for each subject and save correlation matrices for each rep
	for s in range(len(subjects)):
		sub = subjects[s]

		# load Intact playing data and reshape
		playing_data = np.load(playing_data_filepath+'%s/%s.npy'%(sub,roi))
		# data shape is (n_voxels, n_TRs * 3)
		play_reshape = np.reshape(playing_data, (playing_data.shape[0],n_TRs,playing_reps), order='F')
		# reshaped data shape is (n_voxels, n_TRs, 3)

		# load listen data and reshape
		listen_data = np.load(listen_data_filepath+'%s/%s.npy'%(sub,roi))
		# data shape is (n_voxels, n_TRs * 2)
		listen_reshape = np.reshape(listen_data, (listen_data.shape[0],n_TRs,listen_reps), order='F')
		# reshaped data shape is (n_voxels, n_TRs, 2)

		# stack 'em
		this_data = np.dstack((play_reshape,listen_reshape))
		# stacked data shape is (n_voxels, n_TRs, 5)

		# compute and save the correlation matrices for each rep
		for r in range(total_reps):
			corr_matrices[:,:,s,r] = np.corrcoef(this_data[:,:,r].T)

	# create the figure
	fig, ax = plt.subplots(total_reps,len(subjects),sharex=True,sharey=True,figsize=(6.5,7.5))
	fig.suptitle('Within subject pattern correlation, Intact in %s'%roi)

	# add column labels for subjects and x label
	for s in range(len(subjects)): 
		ax[0,s].set_title(subjects[s])
		ax[-1,s].set_xlabel('TRs')
	
	# add row labels for reps
	for r in range(total_reps): 
		ax[r,0].set_ylabel(rep_labels[r]+'\nTRs')

	# shift the axes to make room for the colorbars at the bottom
	fig.subplots_adjust(bottom=0.15)

	# set the parameters for the colorbar axes
	cb_xmin = [0.135,0.3375,0.5425,0.745] # only parameter that changes across subjects
	cb_ymin = 0.07
	cb_w = 0.15
	cb_h = 0.01
	# Is there a way to not hard-code this? Parameters depend on figsize

	# fill in each panel of the figure
	for s in range(len(subjects)):
		# establish overall min and max for this subject for heatmap coloring
		this_vmin = np.min(corr_matrices[:,:,s,:])
		this_vmax = np.max(corr_matrices[:,:,s,:]) 

		# plot each rep
		for r in range(total_reps):
			im = ax[r,s].imshow(corr_matrices[:,:,s,r],vmin=this_vmin,vmax=this_vmax)

		# add the colorbar for each subject at the bottom of their column
		cax = fig.add_axes([cb_xmin[s],cb_ymin,cb_w,cb_h])
		fig.colorbar(im,cax=cax,orientation='horizontal',ticks=[this_vmin,0,this_vmax],format='%.1f')

	#plt.show()
	plt.savefig(figure_filepath+'unannotated/%s'%roi,dpi=500)

	# add annotations of meaningful boundaries
	for s in range(len(subjects)): 
		for r in range(total_reps):
			draw_boundaries(section_boundaries,ax[r,s])
			draw_boundaries(phrase_boundaries,ax[r,s])
		
	#plt.show()
	plt.savefig(figure_filepath+'annotated/%s'%roi,dpi=500)

	plt.close(fig)
	print('%s done!'%roi)


