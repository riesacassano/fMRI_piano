# This script plots k against median event length. It computes event lengths (EL) from all of the HMMs for average of AM subjects (saved in '../models/HMM_event_seg/'). All conditions, reps, and ROIs are included. This plot is simply to visualize the relationship between k and event length. SD of event lengths is also plotted. Average is not used, because average event length is just n_TRs / k. Median is actually informative.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

input_filepath = '../models/HMM_event_seg/'
output_filepath = '../figures/HMM/AM_avg/'

# lists below copied from 'ryc_102621_event_seg_subject_avg.py' so we don't have to reconstruct
ROIs = ['AngularG','MotorCortex','TPJ','A1','mPFC','Hipp','PMC', 'V1'] 
group_label = 'AM'
conds = ['1B','2B','8B','I','Listen']
reps_per_scrambled_cond = 3
reps_per_control_cond = 2
k_set = np.array((2,3,4,5,8,10,12,15,18,20,22,25,30,35,40))

conversion_factor = 1.7 # 1TR = 1.7s

avg_el_all = []
sd_el_all = []

for jasmine in range(len(ROIs)):
	roi = ROIs[jasmine]

	for c in range(len(conds)):
		cond = conds[c]

		if cond == 'Listen': reps = reps_per_control_cond
		else: reps = reps_per_scrambled_cond

		for r in range(reps):
			rep = 'rep%d'%(r+1)

			# load the HMM event segments for this ROI, condition, and rep
			this_HMM = pd.read_csv(input_filepath+'%s/%s_%s_%s'%(roi,group_label,cond,rep),index_col=0)

			# for each k, compute average event length and SD of event lengths with conversion to seconds
			this_avg_el = []
			this_sd_el = []

			#for trilby in range(3):
			#	k = k_set[trilby]
			for k in k_set:
				events = this_HMM['%d'%k].to_numpy()
				_,counts = np.unique(events,return_counts=True)
				this_avg_el.append(np.median(counts)*conversion_factor)
				this_sd_el.append(np.std(counts)*conversion_factor)

			avg_el_all.append(this_avg_el)
			sd_el_all.append(this_sd_el)

avg_el_all = np.asarray(avg_el_all)
sd_el_all = np.asarray(sd_el_all)

avg_el_all = np.flip(avg_el_all,axis=1) # reverse the order of the columns for plotting
sd_el_all = np.flip(sd_el_all,axis=1)

#print(avg_el_all)

fig,ax = plt.subplots(figsize=(7,7))
ax.boxplot(avg_el_all,vert=False,labels=np.flip(k_set))
#plt.show()

fig,ax = plt.subplots(figsize=(7,7))
ax.boxplot(sd_el_all,vert=False,labels=np.flip(k_set))
plt.show()