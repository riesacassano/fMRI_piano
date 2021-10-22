# This script runs event segmentation using hidden Markov models on data from individual subjects. This script saves within versus across (WvA) scores for each ROI as CSV in '../data/HMM_WvA_scores/'. It also saves the HMM predicted events for each time point in '../models/HMM_event_seg/'. The models can be used later to calculate event length, plot HMM-predicted boundaries overlaid on TRxTR matrices, or match predicted event boundaries to human annotated boundaries.

import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
import pandas as pd
#from brainiak.eventseg.event import EventSegment

input_filepath = '../data/data_by_run/' # then ROI/subject/cond/repX.npy 
output_filepath_WvA = '../data/HMM_WvA_scores/'
output_filepath_HMM_pred = '../models/HMM_event_seg/' # then ROI/

subjects = ['03', '05', '08', '15', '17', '20', '21', '22', '23'] 
group = ['AM','M','M','AM','M','AM','M','M','AM']

ROIs = ['AngularG', 'Cerebellum', 'HeschlsG', 'STG', 'MotorCortex', 'TPJ',
    'PCC', 'Precuneus', 'A1', 'mPFC', 'Hipp', 'lTPJ', 'rTPJ', 'PMC', 'V1'] 
conds = ['1B','2B','8B','I','Listen']
reps_per_scrambled_cond = 3
reps_per_control_cond = 2

df_header = ['subject','group','cond','rep']

k_select = np.array((2,3,4,5,8,10,12,15,18,20,22,25,30,35,40)) # 15 values for k
# Jamal uses 10 values when he does the k sweep: (3,5,9,15,20,25,30,35,40,45)
k_all = np.arange(2,41) # include all k values from 2 to 40
k_set = k_select

df_header = df_header + k_set.tolist()


for jasmine in range(1):#len(ROIs)):
	roi = ROIs[jasmine]

	# create the array to hold WvA values for this ROI
	wva_scores = pd.DataFrame(columns = df_header)
	print(wva_scores)

	for s in range(1):#len(subjects)):
		sub = subjects[s]

		# scrambled conditions first
		for c in range(1):#len(conds)-1):

			for r in range(reps_per_scrambled_cond):



		# then Listen condition



# in each SCR loop: grab data from folder

# inside k loop:
# run event seg for each k
# append HMM predictions to some pred_events list
# compute WvA
# append WvA to this_SCR list

# after k loop:
# append this_SCR list to DF (when data is appended to DF, use ignore_index=True)
# gather (reshape?) pred_events and save for this SCR

# after SCR loop, save DF		