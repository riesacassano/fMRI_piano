# This script runs event segmentation using hidden Markov models on data from individual subjects. This script saves within versus across (WvA) scores for each ROI as CSV in '../data/HMM_WvA_scores/'. It also saves the HMM predicted events for each time point in '../models/HMM_event_seg/'. The models can be used later to calculate event length, plot HMM-predicted boundaries overlaid on TRxTR matrices, or match predicted event boundaries to human annotated boundaries.

import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
import pandas as pd
#from brainiak.eventseg.event import EventSegment

input_filepath = '../data/' 
output_filepath_WvA = '../data/HMM_WvA_scores'
output_filepath_HMM_pred = '../models/HMM_event_seg' # then ROI sub-folder

subjects = ['03', '05', '08', '15', '17', '20', '21', '22', '23'] 
ROIs = ['AngularG', 'Cerebellum', 'HeschlsG', 'STG', 'MotorCortex', 'TPJ',
    'PCC', 'Precuneus', 'A1', 'mPFC', 'Hipp', 'lTPJ', 'rTPJ', 'PMC', 'V1'] 
n_ROI = len(ROIs)
