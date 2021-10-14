# This script constructs matrices against which to compare TRxTR matrices. Section and phrase boundaries were borrowed from '../Princeton/analysis/5_spring_thesis_analysis/meaningful boundaries.xlsx' and copied here. The segment boundaries are used in a slightly different way - instead of a TR that marks a boundary, both beginning and end TRs are used. This means that some TRs are double counted. This allows for more precise construction of the model at segment beginnings and ends. These matrices account for HRF.

import numpy as np
import matplotlib.pyplot as plt

# test the method
#test_v1 = np.array([1,1,0,0,0,0])
#test_outer1 = np.outer(test_v1,test_v1)
#test_v2 = np.array([0,0,1,1,0,0])
#test_outer2 = np.outer(test_v2,test_v2)
#big_test = test_outer1 + test_outer2
#print(big_test)

output_filepath = 'data/models/'

# boundaries copied from 'meaningful boundaries.xlsx' and reformatted
I_section = [[1,39],[39,74],[75,102],[103,141]]
I_phrase = [[1,11],[11,20],[21,29],[30,39],[39,46],[46,55],[56,65],[65,74],[75,84],[84,93],[94,102],[103,113],[114,122],[123,132],[132,141]]
phrase_8B = [[1,11],[11,20],[21,29],[30,39],[39,49],[50,59],[59,68],[69,78],[78,87],[88,96],[97,106],[106,115],[116,125],[125,132],[132,141]]

# set filenames and titles here
segment_options = [I_section, I_phrase, phrase_8B]
filenames = ['I_section_strict', 'I_phrase_strict', 'phrase_8B_strict']
titles = ['Intact sections (strict)', 'Intact phrases (strict)', '8B phrases (strict)']

n_TRs = 148
HRF = 3


# choose which segments to use 
choice = 2
segments = segment_options[choice]
filename = filenames[choice]
title = titles[choice]

# create the big matrix
model = np.zeros((n_TRs,n_TRs))

for s in range(len(segments)):

	# grab the lower and upper bounds and shift for HRF
	lower_bound = segments[s][0] + HRF
	upper_bound = segments[s][1] + HRF

	# create a vector of zeros of length n_TRs
	this_seg = np.zeros(n_TRs)

	# fill in with ones between lower and upper bounds, including both bounds
	this_seg[lower_bound:upper_bound+1] = 1

	# take outer product of vector with itself
	this_seg_outer = np.outer(this_seg, this_seg)
	
	# add this to overall model
	model = model + this_seg_outer

# There are some corners where the segments overlap - set these to 1.
#diag = np.diag(model)
#new_diag = np.where(diag > 1, 1, diag)
#np.fill_diagonal(model,new_diag)

# could also just set the whole diagonal equal to 1
np.fill_diagonal(model,1)

# save the model as npy array
np.save(output_filepath+filename,model)

# visualize the model and save it
fig,ax = plt.subplots()
ax.set_xlabel('TRs')
ax.set_ylabel('TRs')
ax.set_title(title)
im = ax.imshow(model)
fig.colorbar(im)
#plt.show()
plt.savefig(output_filepath+filename,dpi=300)