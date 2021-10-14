import numpy as np
#import matplotlib.pyplot as plt

#subjects = ['03','15','20','23']

# Load the PMC data for run 1
#run1_data = []
#for s in range(len(subjects)):
#	this_subj = subjects[s]
#	data = np.load('../A1/sub1%s_run1.npy'%this_subj)
#	avg_data = np.average(data, axis=0)
#	run1_data.append(avg_data)

#fig,ax = plt.subplots()
#for s in range(len(subjects)):
#	ax.plot(run1_data[s])
#plt.show()

subj = '03'
roi = 'A1'
filepath = '../data/ROI_by_subject_listen/'

test = np.load(filepath+'s1%s/%s.npy'%(subj,roi))
print(test.shape)