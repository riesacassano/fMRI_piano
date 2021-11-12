# This notebook plots HMM-predicted boundaries for s103 rep 3 of Intact in Motor Cortex and s115 rep1 of Intact in V1. Best k is taken from average subjects k sweep (k = 12 and k = 26, based on plots). Plotting is borrowed from BrainIAK tutorial.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

subj = 's103'
cond = 'I'
rep = 'rep3' 
roi = 'MotorCortex'
k = 12
title_text = 'subject 103, rep 3 of Intact\nin motor cortex, k = 12'

subj = 's115'
cond = 'I'
rep = 'rep1'
roi = 'V1'
k = 26
title_text = 'subject 115, rep 1 of Intact\nin primary visual cortex (V1), k = 26'


data_filepath = '../data/data_by_run/%s/%s/%s/%s.npy' %(roi,subj,cond,rep)
model_filepath = '../models/HMM_event_seg/all_reps_avg_AM/%s/AM_%s_%s.txt' %(roi,cond,rep)

# load run data
data = np.load(data_filepath)

# compute correlation matrix (TRxTR)
cc = np.corrcoef(data.T)

# load HMM-predicted event boundaries
HMM_pred_df = pd.read_csv(model_filepath)

# grab the right column
pred_seg = HMM_pred_df['%d'%k]



def plot_tt_similarity_matrix(ax, data_matrix, bounds, n_TRs, title_text):
    ax.imshow(np.corrcoef(data_matrix.T), cmap='viridis')
    ax.set_title(title_text,fontsize='xx-large')
    ax.set_xlabel('time point (TR)',fontsize='x-large')
    ax.set_ylabel('time point (TR)',fontsize='x-large')
    # plot the boundaries 
    bounds_aug = np.concatenate(([0],bounds,[n_TRs]))
    for i in range(len(bounds_aug)-1):
        rect = patches.Rectangle(
            (bounds_aug[i],bounds_aug[i]),
            bounds_aug[i+1]-bounds_aug[i],
            bounds_aug[i+1]-bounds_aug[i],
            linewidth=2,edgecolor='w',facecolor='none'
        )
        ax.add_patch(rect)


# extract the boundaries 
#bounds = np.where(np.diff(np.argmax(pred_seg, axis=1)))[0]
bounds = np.where(np.diff(pred_seg))[0]

# plot in function above
f, ax = plt.subplots(1,1, figsize = (6,6))
n_TRs = 148
plot_tt_similarity_matrix(ax, data, bounds, n_TRs, title_text)
f.tight_layout()
#plt.show()
plt.savefig('../figures/HMM/%s_%s_example'%(subj,roi),dpi=300)