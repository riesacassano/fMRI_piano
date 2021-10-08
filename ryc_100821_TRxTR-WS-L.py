# This script generates within-subject TRxTR matrices for all subjects in each rep of the Listen condition. It is adapted from '../Princeton/analysis/5_spring_thesis_analysis/3_listen/scripts/TRxTR_within_subject_L.py' and extends it to all subjects (AM and M) with and without stimulus-determined annotations.

import numpy as np
import matplotlib.pyplot as plt

# subjects = ['s103','s115','s120','s123'] # These are AM subjects only
# use this for intermingled AM and M subjects
subjects = ['s103','s105','s108','s115','s117','s120','s121','s122','s123']
# use this for separate AM and M subjects
# subjects = ['s103','s115','s120','s123','s105','s108','s117','s121','s122']

# all available ROIs
ROIs = ['AngularG', 'Cerebellum', 'HeschlsG', 'STG', 'MotorCortex', 'TPJ', 'PCC', 'Precuneus', 'A1', 'mPFC', 'Hipp', 'lTPJ', 'rTPJ', 'PMC', 'V1']
voxels_per_ROI = [562,12,113,513,1362,832,204,1312,516,293,353,382,412,1573,191]

data_filepath = '../data/ROI_by_subject_listen/'
rep = ['rep1','rep2','avgreps']


# test to load a subject
test_sub = subjects[0]
test_roi = ROIs[8]
test = np.load(data_filepath+'%s/%s.npy'%(test_sub,test_roi))
print(test.shape)
# test shape is (no_voxels, no_TRs * 2)