# This script plots k against event length. It computes event lengths from all of the HMMs for average of AM subjects (saved in '../models/HMM_event_seg/'). All conditions, reps, and ROIs are included. This plot is simply to visualize the relationship between k and event length. 

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

for jasmine in range(1):#len(ROIs)):
	roi = ROIs[jasmine]

	for c in range(1):#len(conds)):
		cond = conds[c]

		if cond == 'Listen': reps = reps_per_control_cond
		else: reps = reps_per_scrambled_cond

		for r in range(1):#reps):
			rep = 'rep%d'%(r+1)

			# load the HMM event segments for this ROI, condition, and rep
			this_HMM = pd.read_csv(input_filepath+'%s/%s_%s_%s'%(roi,group_label,cond,rep),index_col=0)

			# for each k, compute average event length
			this_avg_event_length = []

			#for k in k_set:
			for trilby in range(1):
				
				events = this_HMM[k]
				print(