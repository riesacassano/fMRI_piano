# This script takes the behavioral data that is in separate .npy files in '../../data/behavior/accuracy_by_seconds/' and collects it into one big DataFrame. The first three columns are identifiers (condition, rep, subject, group) and the next 240 columns are all of the seconds in those runs.

import os
import numpy as np
import pandas as pd

parent_dir = '../../data/behavior/'
input_filepath = os.path.join(parent_dir,'accuracy_by_seconds/')
output_filepath = parent_dir # save directly in the behavior folder

conditions = ['I','8B','2B','1B']
reps = 3
subjects = ['03', '05', '08', '15', '17', '20', '21', '23', '22'] # subjects were in this order in the original behavioral data 
groups = ['AM','M','M','AM','M','AM','M','AM','M']

n_sec = np.arange(1,241)
df_header = ['cond','rep','sub','group'] + n_sec.tolist()


all_data = []

for c in range(len(conditions)):
	cond = conditions[c]

	for r in range(reps):
		rep = 'rep%d'%(r+1)

		# load the .npy file
		data = np.load(input_filepath+'%s_%s.npy'%(cond,rep))

		for s in range(len(subjects)):
			sub = 's1%s'%subjects[s]
			group = groups[s]

			this_data = data[s].tolist() # convert this subject's data to a list
			this_row = [cond,rep,sub,group] + this_data # add identifying information at the front

			all_data.append(this_row) # append it to the big list

# convert the big list to a DataFrame and save as csv
df = pd.DataFrame(data = all_data, columns = df_header)
df.to_csv(output_filepath+'all_data_beatpadding=0')