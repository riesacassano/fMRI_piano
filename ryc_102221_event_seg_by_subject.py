# This script runs event segmentation using hidden Markov models on data from individual subjects. WvA is implemented based on Jamal's script 'hmm_K_sweep_paper_no_srm.py', as explored in 'ryc_101521_WvA_implementation.ipynb.' This script saves within versus across (WvA) scores for each ROI as CSV in '../data/HMM_WvA_scores/'. It also saves the HMM predicted events for each time point in '../models/HMM_event_seg/'. The models can be used later to calculate event length, plot HMM-predicted boundaries overlaid on TRxTR matrices, or match predicted event boundaries to human annotated boundaries.
# Update 11/9/21: Add timing. Remove M subjects. Select ROIs only. No Listen condition. New k set. Add normalizing step.
# s115: "mean of empty slice"

import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
import pandas as pd
from brainiak.eventseg.event import EventSegment # make sure you're in virtual environment -> 'source activate venv'
import time

input_filepath = '../data/data_by_run/' # then ROI/subject/cond/repX.npy 
output_filepath_WvA = '../data/HMM_WvA_scores/'
output_filepath_HMM_pred = '../models/HMM_event_seg/rep1_ind_AM/' # then ROI/

subjects = ['03','15','20','23'] 

ROIs = ['MotorCortex','A1','PMC','V1']
conds = ['1B','2B','8B','I']
reps = 1

df_header = ['subject','cond','rep']

k_test = np.array((2,4,8))
k_all = np.arange(2,41) # include all k values from 2 to 40

k_low = np.arange(3,19)
k_mid = np.arange(20,34,2)
k_high = np.array((35,40,45,52,60))
k_select = np.hstack((k_low,k_mid,k_high))
# Jamal uses 10 values when he does the k sweep: (3,5,9,15,20,25,30,35,40,45)
# This k set has 28 values

k_set = k_select

df_header = df_header + k_set.tolist()


for jasmine in range(len(ROIs)):
	roi = ROIs[jasmine]
	print('starting on %s'%roi)

	# create an empty list to hold WvA values for this ROI
	wva_scores = []

	for s in range(len(subjects)):
		sub = 's1%s'%subjects[s]
		print()
		print('starting on %s'%sub)

		for c in range(len(conds)):
			cond = conds[c]

			for r in range(reps):
				rep = 'rep%d'%(r+1)

				start = time.time()

				# grab the data from the folder
				data_filename = input_filepath+'%s/%s/%s/%s.npy'%(roi,sub,cond,rep)
				data_orig = np.load(data_filename)
				# data_orig.shape is n_voxels x n_TRs for this run

				# normalize
				data = StandardScaler().fit_transform(data_orig.T).T
				# each voxel scaled to mean = 0, SD = 1

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
					across = cc[(~same_event)*local_mask].mean() # "mean of empty slice"
					within_across = within - across
					wva_this_scr.append(within_across)

				# save the predicted events list as a DataFrame
				all_HMM_pred_events = pd.DataFrame(data=np.asarray(HMM_pred_events).T,columns=k_set)
				model_filename = output_filepath_HMM_pred+'%s/%s_%s_%s'%(roi,sub,cond,rep)
				all_HMM_pred_events.to_csv(model_filename,index_label='TR')

				# add identifying info to the beginning of the WvA score list
				this_wva_row = [sub, cond, rep] + wva_this_scr

				# append WvA score list as a row to the big WvA list
				wva_scores.append(this_wva_row)

				end = time.time()

				print('%s, %s done (%f seconds)'%(cond,rep,end-start))


	# convert WvA scores to a DataFrame and save it for this ROI
	wva_df = pd.DataFrame(data = wva_scores, columns = df_header)
	wva_filename = output_filepath_WvA + '%s_AM_ind'%roi
	wva_df.to_csv(wva_filename)

	print('done with %s'%roi)
	print()
		