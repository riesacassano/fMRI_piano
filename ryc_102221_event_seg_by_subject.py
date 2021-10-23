# This script runs event segmentation using hidden Markov models on data from individual subjects. WvA is implemented based on Jamal's script 'hmm_K_sweep_paper_no_srm.py', as explored in 'ryc_101521_WvA_implementation.ipynb.' This script saves within versus across (WvA) scores for each ROI as CSV in '../data/HMM_WvA_scores/'. It also saves the HMM predicted events for each time point in '../models/HMM_event_seg/'. The models can be used later to calculate event length, plot HMM-predicted boundaries overlaid on TRxTR matrices, or match predicted event boundaries to human annotated boundaries.

import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
import pandas as pd
from brainiak.eventseg.event import EventSegment # make sure you're in virtual environment -> 'source activate venv'

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

k_test = np.array((2,4,8))
k_select = np.array((2,3,4,5,8,10,12,15,18,20,22,25,30,35,40)) # 15 values for k
# Jamal uses 10 values when he does the k sweep: (3,5,9,15,20,25,30,35,40,45)
k_all = np.arange(2,41) # include all k values from 2 to 40
k_set = k_test

df_header = df_header + k_set.tolist()


for jasmine in range(1):#len(ROIs)):
	roi = ROIs[jasmine]

	# create the DataFrame to hold WvA values for this ROI
	wva_scores = []

	for s in range(1):#len(subjects)):
		sub = 's1%s'%subjects[s]

		for c in range(1):#len(conds)-1):
			#cond = conds[c]
			cond = conds[-1]

			if cond == 'Listen': reps = reps_per_control_cond
			else: reps = reps_per_scrambled_cond

			for r in range(reps):
				rep = 'rep%d'%(r+1)

				# grab the data from the folder
				data_filename = input_filepath+'%s/%s/%s/%s.npy'%(roi,sub,cond,rep)
				data = np.load(data_filename)
				# data.shape is n_voxels x n_TRs for this run

				# compute the TRxTR correlation matrix here
				cc = np.corrcoef(data.T)
				# cc.shape is n_TRs x n_TRs

				# create empty lists to hold predicted events and WvA scores for this subject/cond/rep
				HMM_pred_events = []
				wva_this_scr = []

				# run event segmentation with different numbers of events
				for k in k_set:
					# fit the model
					ev = EventSegment(k)
					ev.fit(data.T)
					#print('model with k = %d fit'%k) # for testing only

					# get model's prediction of event for each time point
					events = np.argmax(ev.segments_[0],axis=1)
					HMM_pred_events.append(events)

					# create a mask to only look at values up to max event length
					max_event_length = stats.mode(events)[1][0]
					local_mask = np.zeros(cc.shape, dtype=bool)
					for i in range(1,max_event_length):
						local_mask[np.diag(np.ones(cc.shape[0]-i, dtype=bool), i)] = True

					# compute within versus across score and append to the list for this subject/cond/rep
					same_event = events[:,np.newaxis] == events
					within = cc[same_event*local_mask].mean()
					across = cc[(~same_event)*local_mask].mean()
					within_across = within - across
					wva_this_scr.append(within_across)

				# save the predicted events list as a DataFrame
				all_HMM_pred_events = pd.DataFrame(data=np.asarray(HMM_pred_events).T,columns=k_set)
				model_filename = output_filepath_HMM_pred+'%s/%s_%s_%s'%(roi,sub,cond,rep)
				all_HMM_pred_events.to_csv(model_filename,index_label='TR')

				# add identifying info to the beginning of the WvA score list
				this_wva_row = [sub, group[s], cond, rep] + wva_this_scr

				# append WvA score list as a row to the big WvA list
				wva_scores.append(this_wva_row)

				print('%s done'%rep)


	# convert WvA scores to a DataFrame and save it for this ROI
	wva_df = pd.DataFrame(data = wva_scores, columns = df_header)
	wva_filename = output_filepath_WvA + '%s'%roi
	wva_df.to_csv(wva_filename)

		