# This script is adapted from '../Princeton/analysis/5_spring_thesis_analysis/2+3_pattern/scripts/plot_for_Ebio.py'. It plots mean and SEM of pattern correlation values for A1, motor cortex, and PMC. It generates one plot each for playing and listening, and one combined plot.

import numpy as np
import matplotlib.pyplot as plt

data_filepath = '../data/spatial_ISC_one_val/' # then listen/playing, ROI.npy
output_filepath = '../figures/pattern_correlation/'

ROIs = ['A1','MotorCortex','PMC']

levels = ['section','half-section','phrase','half-phrase']
ticks = range(len(levels))

# playing
cond = 'I'
rep = 'rep1'

# load the mean and SEM values for playing
play_values = np.zeros((len(ROIs),len(levels),2))
for jasmine in range(len(ROIs)):
	roi = ROIs[jasmine]
	play_values[jasmine,:,:] = np.load(data_filepath+'playing/%s.npy'%roi)[:,-2:]

# significance levels from the bootstrap
play_sig_levels = [['','','*','*'],['','','**','**'],['','.','','']]

# listening
cond = 'Listen'
rep = 'avgreps'

# load the mean and SEM values for listening
listen_values = np.zeros((len(ROIs),len(levels),2))

for jasmine in range(len(ROIs)):
	roi = ROIs[jasmine]
	listen_values[jasmine,:,:] = np.load(data_filepath+'listen/%s.npy'%roi)[:,-2:]

# significance levels from the bootstrap
listen_sig_levels = [['','.','',''],['','','',''],['.','.','','']]


# plot just the playing values on three separate subplots
filename = 'A1_MC_PMC_playing'

fig,ax = plt.subplots(1,len(ROIs),figsize=(15,5),sharey=True)
fig.suptitle('Average pattern correlation values, rep1 of Intact, playing')
ax[0].set_ylabel('correlation')

for jasmine in range(len(ROIs)):
	ax[jasmine].plot(ticks,play_values[jasmine,:,0],color='black')
	ax[jasmine].errorbar(ticks,play_values[jasmine,:,0],yerr=play_values[jasmine,:,1],alpha=0.5,capsize=4,color='black')
	
	ax[jasmine].set_xticks(ticks)
	ax[jasmine].set_xticklabels(levels, fontsize='x-small')
	ax[jasmine].set_xlim(ticks[0]-0.5, ticks[-1]+0.5)
	ax[jasmine].hlines(0,ticks[0]-0.5, ticks[-1]+0.5,alpha=0.2,color='black')

	for level in range(len(levels)):
		y = play_values[jasmine,level,0] + play_values[jasmine,level,1] + 0.01
		sigmarker = play_sig_levels[jasmine][level]
		if sigmarker == '.': ax[jasmine].scatter(level,y,c='black',s=1.2)
		else: ax[jasmine].text(level, y, sigmarker, ha='center')
	
	ax[jasmine].set_title('%s'%ROIs[jasmine])

max_y = np.max(play_values[:,:,0])
max_err = play_values[:,:,1].flatten()[np.argmax(play_values[:,:,0])]
ax[0].set_ylim(top = max_y + max_err + 0.02)

#plt.show()
#plt.savefig(output_filepath+filename,dpi=300)
plt.close(fig)



# plot just the listen values on three separate subplots
filename = 'A1_MC_PMC_listen'

fig,ax = plt.subplots(1,len(ROIs),figsize=(15,5),sharey=True)
fig.suptitle('Average pattern correlation values, avgreps of Listen')
ax[0].set_ylabel('correlation')

for jasmine in range(len(ROIs)):
	ax[jasmine].plot(ticks,listen_values[jasmine,:,0],color='black')
	ax[jasmine].errorbar(ticks,listen_values[jasmine,:,0],yerr=listen_values[jasmine,:,1],alpha=0.5,capsize=4,color='black')
	
	ax[jasmine].set_xticks(ticks)
	ax[jasmine].set_xticklabels(levels, fontsize='x-small')
	ax[jasmine].set_xlim(ticks[0]-0.5, ticks[-1]+0.5)
	ax[jasmine].hlines(0,ticks[0]-0.5, ticks[-1]+0.5,alpha=0.2,color='black')

	for level in range(len(levels)):
		y = listen_values[jasmine,level,0]+listen_values[jasmine,level,1]+0.01
		sigmarker = listen_sig_levels[jasmine][level]
		if sigmarker == '.': ax[jasmine].scatter(level,y,c='black',s=1.2)
		else: ax[jasmine].text(level, y, sigmarker, ha='center')
	
	ax[jasmine].set_title('%s'%ROIs[jasmine])

max_y = np.max(listen_values[:,:,0])
max_err = listen_values[:,:,1].flatten()[np.argmax(listen_values[:,:,0])]
ax[0].set_ylim(top = max_y + max_err + 0.02)

#plt.show()
#plt.savefig(output_filepath+filename,dpi=300)
plt.close(fig)



# plot playing and listen values combined on three separate subplots
filename = 'A1_MC_PMC_combined'

fig,ax = plt.subplots(1,len(ROIs),figsize=(15,5),sharey=True)
fig.suptitle('Average pattern correlation values')
ax[0].set_ylabel('correlation')

for jasmine in range(len(ROIs)):
	ax[jasmine].plot(ticks,play_values[jasmine,:,0],color='C0',label='playing')
	ax[jasmine].errorbar(ticks,play_values[jasmine,:,0],yerr=play_values[jasmine,:,1],alpha=0.5,capsize=4,color='C0')

	ax[jasmine].plot(ticks,listen_values[jasmine,:,0],color='C2',linestyle='dashed',label='listen')
	ax[jasmine].errorbar(ticks,listen_values[jasmine,:,0],yerr=listen_values[jasmine,:,1],linestyle='dashed',alpha=0.5,capsize=4,color='C2')
	
	ax[jasmine].set_xticks(ticks)
	ax[jasmine].set_xticklabels(levels, fontsize='x-small')
	ax[jasmine].set_xlim(ticks[0]-0.5, ticks[-1]+0.5)
	ax[jasmine].hlines(0,ticks[0]-0.5, ticks[-1]+0.5,alpha=0.2,color='black')

	for level in range(len(levels)):
		y = play_values[jasmine,level,0] + play_values[jasmine,level,1] + 0.01
		sigmarker = play_sig_levels[jasmine][level]
		if sigmarker == '.': ax[jasmine].scatter(level, y, c='C0', s=1.2)
		else: ax[jasmine].text(level, y, sigmarker, ha='center', c='C0')

		y = listen_values[jasmine,level,0]+listen_values[jasmine,level,1]+0.01
		sigmarker = listen_sig_levels[jasmine][level]
		if sigmarker == '.': ax[jasmine].scatter(level,y,c='C2',s=1.2)
		else: ax[jasmine].text(level, y, sigmarker, ha='center', c='C2')
	
	ax[jasmine].legend(fontsize='small')
	ax[jasmine].set_title('%s'%ROIs[jasmine])

max_y = np.max(play_values[:,:,0])
max_err = play_values[:,:,1].flatten()[np.argmax(play_values[:,:,0])]
ax[0].set_ylim(top = max_y + max_err + 0.02)

#plt.show()
plt.savefig(output_filepath+filename,dpi=300)
#plt.close(fig)