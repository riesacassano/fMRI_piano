# This script generates within-subject TRxTR matrices for all subjects in each rep of the Listen condition. It is adapted from '../Princeton/analysis/5_spring_thesis_analysis/3_listen/scripts/TRxTR_within_subject_L.py' and extends it to all subjects (AM and M) with and without stimulus-determined annotations.

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
#voxels_per_ROI = [562,12,113,513,1362,832,204,1312,516,293,353,382,412,1573,191]
n_TRs = 148

data_filepath = '../data/ROI_by_subject_listen/'
figure_filepath = '../figures/TRxTR_listen_WS/' # then (un)annotated/roi_rep
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


for jasmine in range(len(ROIs)):
	roi = ROIs[jasmine]

	corr_matrices = np.zeros((n_TRs,n_TRs,len(subjects),len(reps)))

	# load data from all subjects and save correlation matrices for each rep
	for s in range(len(subjects)):
		sub = subjects[s]
		
		data = np.load(data_filepath+'%s/%s.npy'%(sub,roi))
		# shape is (n_voxels, n_TRs * 2)

		# reshape the data into reps
		reshaped_data = np.reshape(data,(data.shape[0],n_TRs,-1),order='F')

		# compute correlation matrix for rep 1
		corr_matrices[:,:,s,0] = np.corrcoef(reshaped_data[:,:,0].T)
		# rep 2
		corr_matrices[:,:,s,1] = np.corrcoef(reshaped_data[:,:,1].T)
		# average reps
		corr_matrices[:,:,s,2] = np.corrcoef(np.mean(reshaped_data,axis=-1).T)

	
	# plot each rep
	for r in range(len(reps)):
		rep = reps[r]
		
		# establish overall min and max for heatmap coloring
		this_vmin = np.min(corr_matrices[:,:,:,r])
		this_vmax = np.max(corr_matrices[:,:,:,r])

		# create the figure
		fig, ax = plt.subplots(n_rows,n_cols,sharex=True,sharey=True,figsize=(7.5,7.5))
		fig.suptitle('Within subject pattern correlation, %s of %s, in %s'%(rep,cond,roi))

		# shift the axes and add a colorbar axis
		fig.subplots_adjust(right=0.80)
		cbar_ax = fig.add_axes([0.85,0.12,0.01,0.75])

		# label the y axes of the left panels
		for i in range(n_rows): ax[i,0].set_ylabel('TRs')

		# label the x axes of the bottom panels
		for j in range(n_cols): ax[-1,j].set_xlabel('TRs')

		# fill in each panel of the figure
		for i in range(n_rows):
			for j in range(n_cols):

				# label the panel with the subject
				sub = subs[i,j]
				ax[i,j].set_title(sub)

				# display the matrix
				s = subjects.index(sub)
				im = ax[i,j].imshow(corr_matrices[:,:,s,r],vmin=this_vmin,vmax=this_vmax)

		fig.colorbar(im,cax=cbar_ax)

		#plt.show()
		plt.savefig(figure_filepath+'unannotated/%s_%s'%(roi,rep),dpi=500)

		# add annotations of meaningful boundaries
		for i in range(n_rows):
			for j in range(n_cols):
				draw_boundaries(section_boundaries,ax[i,j])
				draw_boundaries(phrase_boundaries,ax[i,j])
		
		#plt.show()
		plt.savefig(figure_filepath+'annotated/%s_%s'%(roi,rep),dpi=500)

		plt.close(fig)
