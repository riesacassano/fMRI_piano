# This script generates intersubject TRxTR matrices for all subjects in each rep of the Listen condition. It is adapted from 'ryc_100821_TRxTR-WS-L'. Instead of within-subject correlations, this script computes and plots the correlation between each subject and the average of others. In addition to plotting each subject individually, this script averages all of the 

import numpy as np
import matplotlib.pyplot as plt

# subjects = ['s103','s115','s120','s123'] # These are AM subjects only
# use this for intermingled AM and M subjects
subjects = ['s103','s105','s108','s115','s117','s120','s121','s122','s123']
# use this for separate AM and M subjects
# subjects = ['s103','s115','s120','s123','s105','s108','s117','s121','s122']
sub_range = np.arange(len(subjects))

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

for jasmine in range(len(ROIs)):
	roi = ROIs[jasmine]
	n_voxels = voxels_per_ROI[jasmine]

	# load data from all subjects first
	data = np.zeros((len(subjects),n_voxels,n_TRs,len(reps)))

	for s in range(len(subjects)):
		sub = subjects[s]

		this_data = np.load(data_filepath+'%s/%s.npy'%(sub,roi))
		# shape is (n_voxels, n_TRs * 2)

		# save the data for rep 1
		data[s,:,:,0] = this_data[:,:n_TRs]
		# rep 2
		data[s,:,:,1] = this_data[:,n_TRs:]
		# avg reps
		data[s,:,:,2] = np.mean([this_data[:,:n_TRs],this_data[:,n_TRs:]],axis=0)


	# compute correlation matrices between each subject and the average of other subjects
	corr_matrices = np.zeros((n_TRs,n_TRs,len(subjects),len(reps)))

	for s in range(len(subjects)):
		for r in range(len(reps)):
			this_sub = data[s,:,:,r]
			avg_others = np.mean(data[sub_range[sub_range != s],:,:,r],axis=0)

			corr_matrices[:,:,s,r] = np.corrcoef(this_sub.T,avg_others.T)[:n_TRs,n_TRs:]


	# plot each rep
	for r in range(len(reps)):
		rep = reps[r]
		
		# establish overall min and max for heatmap coloring
		this_vmin = np.min(corr_matrices[:,:,:,r])
		this_vmax = np.max(corr_matrices[:,:,:,r])

		# create the figure
		fig, ax = plt.subplots(n_rows,n_cols,sharex=True,sharey=True,figsize=(7.5,7.5))
		fig.suptitle('Intersubject pattern correlation, %s of %s, in %s'%(rep,cond,roi))

		# shift the axes and add a colorbar axis
		fig.subplots_adjust(right=0.80)
		cbar_ax = fig.add_axes([0.85,0.12,0.01,0.75])

		# fill in each panel of the figure
		for i in range(n_rows):
			for j in range(n_cols):

				# label the panel with the subject
				sub = subs[i,j]
				ax[i,j].set_title(sub)

				# label the x and y axes
				ax[i,j].set_xlabel('avg others TRs')
				ax[i,j].set_ylabel('%s TRs'%sub)

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


		# plot the average of all intersubject matrices
		fig, ax = plt.subplots()
		ax.set_title('Average intersubject pattern correlation,\n %s of %s, in %s'%(rep,cond,roi))
		ax.set_xlabel('avg others TRs')
		ax.set_ylabel('target subj TRs')

		im = ax.imshow(np.mean(corr_matrices[:,:,:,r],axis=2))
		fig.colorbar(im)

		plt.savefig(figure_filepath_avg+'unannotated/%s_%s'%(roi,rep),dpi=500)			
		
		# add annotations of meaningful boundaries
		draw_boundaries(section_boundaries,ax)
		draw_boundaries(phrase_boundaries,ax)

		#plt.show()
		plt.savefig(figure_filepath_avg+'annotated/%s_%s'%(roi,rep),dpi=500)	

		plt.close(fig)
	
	print('%s done!'%roi)

