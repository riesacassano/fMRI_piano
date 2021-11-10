# This script plots WvA scores for HMMs fit to average AM subjects in rep 1. Each ROI is plotted on its own subplot.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

input_filepath = '../data/HMM_WvA_scores/'
output_filepath = '../figures/HMM/'#AM_avg_rep1/'

# currently available ROIs
ROIs = ['A1','MotorCortex','PMC','V1']

subject_group = 'AM'
conds = ['I','8B','2B','1B']
linestyles = ['solid','dashed','dashdot','dotted']
colors = ['C0','C4','C3','C1']
#reps = 3
rep = 'rep1'

n_sec = 240 # total of 240 seconds for each run

# create the figure
fig,ax = plt.subplots(len(ROIs),1,figsize=(8,8))
fig.suptitle('HMM fits for average of %s subjects in rep1'%subject_group)
ax[-1].set_xlabel('total sec / k (approximate event length in sec)')

for jasmine in range(len(ROIs)):
	roi = ROIs[jasmine]

	# load the WvA scores for this ROI
	wva_scores = pd.read_csv(input_filepath+'%s_%s'%(roi,subject_group),index_col=0)

	# reconstruct the k-set from the header
	k_list = wva_scores.columns[2:].tolist()
	k_set = [int(k) for k in k_list]
	el_set = 240 / np.asarray(k_set)

	# label this panel of the figure
	#ax[jasmine].set_xlim(1,k_set[-1]+1)
	#ax[jasmine].set_xticks(k_set)
	#ax[jasmine].set_xticklabels(k_set,fontsize='xx-small',rotation=-90)
	ax[jasmine].set_xticks(range(10,int(n_sec/int(k_set[0]))+10,10))
	ax[jasmine].set_ylabel('%s: model fit\n(within vs across)'%roi,fontsize='x-small')

	for c in range(len(conds)):
		cond = conds[c]
		ls = linestyles[c]
		color = colors[c]

		# select rows from the DataFrame of this condition		
		this_cond_df = wva_scores.loc[wva_scores['cond']==cond]

		# select rep 1 rows from the DataFrame
		this_rep = this_cond_df[this_cond_df['rep']==rep]
		this_rep = this_rep.values.tolist()[0][2:] # just want the values

		# plot the values against approximate event length
		ax[jasmine].plot(el_set,this_rep,label=cond,linestyle=ls,color=color)

		# add a dot to mark the max
		ax[jasmine].scatter(el_set[np.argmax(this_rep)],np.max(this_rep),color=color)

	ax[jasmine].legend(fontsize='x-small')

#plt.show()
#plt.savefig(output_filepath+'%s_k'%subject_group,dpi = 300)
plt.savefig(output_filepath+'rep1_%s_el'%subject_group,dpi = 300)