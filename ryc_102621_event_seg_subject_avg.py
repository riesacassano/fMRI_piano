# This script runs event segmentation using hidden Markov models on data of average subjects. WvA is implemented based on Jamal's script 'hmm_K_sweep_paper_no_srm.py', as explored in 'ryc_101521_WvA_implementation.ipynb.' This script saves within versus across (WvA) scores for each ROI as CSV in '../data/HMM_WvA_scores/'. It also saves the HMM predicted events for each time point in '../models/HMM_event_seg/'. The models can be used later to calculate event length, plot HMM-predicted boundaries overlaid on TRxTR matrices, or match predicted event boundaries to human annotated boundaries.

import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
import pandas as pd
from brainiak.eventseg.event import EventSegment # make sure you're in virtual environment -> 'source activate venv'

input_filepath = '../data/data_by_run/' # then ROI/subject/cond/repX.npy 
output_filepath_WvA = '../data/HMM_WvA_scores/'
output_filepath_HMM_pred = '../models/HMM_event_seg/' # then ROI/

# subject lists
all_subjects = ['03', '05', '08', '15', '17', '20', '21', '22', '23'] 
AM_subjects = ['03','15','20','23'] 
M_subjects = ['05','08','17','21','22']

# choose group of subjects
group_label = 'AM' # 'M' 'all'

if group_label == 'all': subjects = all_subjects
if group_label == 'AM': subjects = AM_subjects
if group_label == 'M': subjects = M_subjects


# all available ROIs
# ROIs = ['AngularG', 'Cerebellum', 'HeschlsG', 'STG', 'MotorCortex', 'TPJ', 'PCC', 'Precuneus', 'A1', 'mPFC', 'Hipp', 'lTPJ', 'rTPJ', 'PMC', 'V1'] 
# select ROIs
ROIs = ['AngularG','MotorCortex','TPJ','A1','mPFC','Hipp','PMC', 'V1'] 
conds = ['1B','2B','8B','I','Listen']
reps_per_scrambled_cond = 3
reps_per_control_cond = 2

df_header = ['cond','rep']

k_test = np.array((2,4,8))
k_select = np.array((2,3,4,5,8,10,12,15,18,20,22,25,30,35,40)) # 15 values for k
# Jamal uses 10 values when he does the k sweep: (3,5,9,15,20,25,30,35,40,45)
k_all = np.arange(2,41) # include all k values from 2 to 40
k_set = k_select

df_header = df_header + k_set.tolist()


for jasmine in range(len(ROIs)):
	roi = ROIs[jasmine]
	print('starting on %s'%roi)

	# create an empty list to hold WvA values for this ROI
	wva_scores = []

	for c in range(len(conds)):
		cond = conds[c]

		if cond == 'Listen': reps = reps_per_control_cond
		else: reps = reps_per_scrambled_cond

		for r in range(reps):
			rep = 'rep%d'%(r+1)

			# create an empty list to hold all subjects' data
			all_data = []

			# get the data for each subject
			for s in range(len(subjects)):
				sub = 's1%s'% subjects[s]
				this_data = np.load(input_filepath+'%s/%s/%s/%s.npy'%(roi,sub,cond,rep))
				# data.shape is n_voxels x n_TRs for this subject

				all_data.append(this_data)

			# average over all subjects
			data_orig = np.mean(np.asarray(all_data),axis=0)
			# data_orig.shape is n_voxels x n_TRs

			# normalize
			data = StandardScaler().fit_transform(data_orig.T).T
			# each voxel scaled to mean = 0, SD = 1

			# compute the TRxTR correlation matrix here
			cc = np.corrcoef(data.T)
			# cc.shape is n_TRs x n_TRs

			# create empty lists to hold predicted events and WvA scores for this run
			HMM_pred_events = []
			wva_this_run = []

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
				wva_this_run.append(within_across)

			# save the predicted events list as a DataFrame
			all_HMM_pred_events = pd.DataFrame(data=np.asarray(HMM_pred_events).T,columns=k_set)
			model_filename = output_filepath_HMM_pred+'%s/%s_%s_%s'%(roi,group_label,cond,rep)
			all_HMM_pred_events.to_csv(model_filename,index_label='TR')

			# add identifying info to the beginning of the WvA score list
			this_wva_row = [cond, rep] + wva_this_run

			# append WvA score list as a row to the big WvA list
			wva_scores.append(this_wva_row)

			print('%s, %s done'%(cond,rep))


	# convert WvA scores to a DataFrame and save it for this ROI
	wva_df = pd.DataFrame(data = wva_scores, columns = df_header)
	wva_filename = output_filepath_WvA + '%s_%s'%(roi,group_label)
	wva_df.to_csv(wva_filename,index_label='run_index')

	print('done with %s'%roi)
	print()
		