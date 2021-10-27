# This script plots WvA scores for HMMs fit to average AM subjects.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

input_filepath = '../data/HMM_WvA_scores/'
output_filepath = '../figures/HMM'

# currently available ROIs
ROIs = ['A1','AngularG','Hipp','MotorCortex','mPFC','PMC','TPJ','V1']

subject_group = 'AM'
conds = ['I','8B','2B','1B','Listen']
reps_per_scrambled_cond = 3
reps_per_control_cond = 2


for jasmine in range(1):#len(ROIs)):
	roi = ROIs[jasmine]

	# load the WvA scores for this ROI
	wva_scores = pd.read_csv(input_filepath+'%s_%s'%(roi,subject_group),index_col=0)

	# reconstruct the k-set from the header
	k_list = wva_scores.columns[2:].tolist()
	k_set = [int(k) for k in k_list]

	# create the figure
	fig,ax = plt.subplots(1,5,sharey=True,figsize=(14,5))
	ax[0].set_ylabel('model fit (within vs across)')
	fig.suptitle('HMM fits for average of %s subjects in %s'%(subject_group,roi))

	for c in range(1):#len(conds)):
		cond = conds[c]

		if cond == 'Listen': reps = reps_per_control_cond
		else: reps = reps_per_scrambled_cond
		
		# select rows from the DataFrame of this condition
		this_cond_df = wva_scores.loc[wva_scores['cond']==cond]

		# label this panel of the figure
		ax[c].set_xlabel('k')
		ax[c].set_xlim(1,k_set[-1]+1)
		ax[c].set_xticks(k_set)
		ax[c].set_xticklabels(k_set,fontsize='xx-small')
		ax[c].set_title('%s'%cond)

		# plot each rep
		for r in range(1):#len(reps)):
			rep = 'rep%d'%(r+1)
			this_rep = this_cond_df[this_cond_df['rep']==rep]
			this_rep = this_rep.values.tolist()[0][2:] # just want the values

			# plot the values against the k
			ax[c].plot(k_set,this_rep,label=rep)

		ax[c].legend()

	plt.show()