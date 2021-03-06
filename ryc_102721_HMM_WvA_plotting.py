# This script plots WvA scores for HMMs fit to average AM subjects.
# Update: instead of plotting against k, plot against total seconds / k to approximate event lengths.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

input_filepath = '../data/HMM_WvA_scores/'
output_filepath = '../figures/HMM/AM_avg/'

# currently available ROIs
#ROIs = ['A1','AngularG','Hipp','MotorCortex','mPFC','PMC','TPJ','V1']
ROIs = ['A1','MotorCortex','PMC','V1']

subject_group = 'AM'
conds = ['I','8B','2B','1B','Listen']
reps_per_scrambled_cond = 3
reps_per_control_cond = 2

n_sec = 240 # total of 240 seconds for each run

for jasmine in range(len(ROIs)):
	roi = ROIs[jasmine]

	# load the WvA scores for this ROI
	wva_scores = pd.read_csv(input_filepath+'%s_%s'%(roi,subject_group),index_col=0)

	# reconstruct the k-set from the header
	k_list = wva_scores.columns[2:].tolist()
	k_set = [int(k) for k in k_list]
	el_set = 240 / np.asarray(k_set)

	# create the figure
	fig,ax = plt.subplots(5,1,figsize=(6,8.5))
	fig.suptitle('HMM fits for average of %s subjects in %s'%(subject_group,roi))
	ax[-1].set_xlabel('k (number of events)')
	#ax[-1].set_xlabel('total sec / k (approximate event length in sec)')

	for c in range(len(conds)):
		cond = conds[c]

		if cond == 'Listen': reps = reps_per_control_cond
		else: reps = reps_per_scrambled_cond
		
		# select rows from the DataFrame of this condition
		this_cond_df = wva_scores.loc[wva_scores['cond']==cond]

		# label this panel of the figure
		ax[c].set_xlim(1,k_set[-1]+1)
		ax[c].set_xticks(k_set)
		ax[c].set_xticklabels(k_set,fontsize='xx-small',rotation=-90)
		#ax[c].set_xticks(range(10,int(n_sec/int(k_set[0]))+10,10))
		ax[c].set_ylabel('%s: model fit\n(within vs across)'%cond,fontsize='x-small')

		# plot each rep
		for r in range(reps):
			rep = 'rep%d'%(r+1)
			this_rep = this_cond_df[this_cond_df['rep']==rep]
			this_rep = this_rep.values.tolist()[0][2:] # just want the values	

			# plot the values against the k
			ax[c].plot(k_set,this_rep,label=rep)
			#ax[c].plot(el_set,this_rep,label=rep)

			# add a dot to mark the max
			ax[c].scatter(k_set[np.argmax(this_rep)],np.max(this_rep))
			#ax[c].scatter(el_set[np.argmax(this_rep)],np.max(this_rep))

		ax[c].legend(fontsize='x-small')

	#plt.show()
	plt.savefig(output_filepath+'%s_%s_k'%(roi,subject_group),dpi = 300)
	#plt.savefig(output_filepath+'%s_%s_el'%(roi,subject_group),dpi = 300)