
import mne
import sys
import os.path
import numpy as np
import os
import matplotlib.pyplot as plt
mne.viz.set_browser_backend('matplotlib', verbose=None)

"For Taini .dat files"
number_of_channels = 16
sample_rate = 250.4
sample_datatype = 'int16'
display_decimation = 1


"Calculate start and end samples from RECORDS SAMPLES"
start_sample=16346113
end_sample=37980672

tmin = start_sample/sample_rate
tmax = end_sample/sample_rate

"To load the data, put file location and name below using double back to front slash"
filename="C:\\Users\\niamh\\OneDrive\\Desktop\\\SCN2A_EEG\\BL\\SCN2A\\SCN2A_477\\TAINI_1044_C_SCN2A_477_BL-2024_01_26-0000.dat"

def load_dat(filename):
    '''Load a .dat file by interpreting it as int16 and then de-interlacing the 16 channels'''
    
    print("Loading_" + filename)

    # Load the raw (1-D) data
    dat_raw = np.fromfile(filename, dtype=sample_datatype)

    # Reshape the (2-D) per channel data
    step = number_of_channels * display_decimation
    dat_chans = [dat_raw[c::step] for c in range(number_of_channels)]

    # Build the time array
    t = np.arange(len(dat_chans[0]), dtype=float) / display_decimation

    data=np.array(dat_chans)
    print(len(data))
    del(dat_chans)
    
    n_channels=16

    channel_names=['1', '2', '3', '4', '5', 
                           '6', '7', '8', '9', '10', 
                           '11', '12', '13', '14', '15', '16']
    channel_types=['emg','misc','eeg','misc','misc','misc','emg','misc','misc','misc','misc','misc','eeg','misc','misc','eeg']
        
    'This creates the info that goes with the channels, which is names, sampling rate, and channel types.'
    info = mne.create_info(channel_names, sample_rate, channel_types)
    
    'This makes the object that contains all the data and info about the channels.'
    'Computations like plotting, averaging, power spectrums can be performed on this object'
    
    custom_raw = mne.io.RawArray(data, info)
    
    return custom_raw

custom_raw = load_dat(filename)  

'Creates interactive plot for full raw .dat file'
'comment out to replace with other interactive plots'
custom_raw.plot(None, 60, 0, 16, scalings = "auto", order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options = "true")

'Creates interactive plot with colour coding for channel types and cropping for a single 24 hour baseline (ZT 0 to ZT 23)'
colors=dict(mag='darkblue', grad='b', eeg='k', eog='k', ecg='m',
      emg='g', ref_meg='steelblue', misc='steelblue', stim='b',
     resp='k', chpi='k')
'remove comment to plot'
#custom_raw.crop(tmin, tmax).plot(None, 60, 0, 16,color = colors, scalings = "auto", order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], show_options = "true" )

@author: Alfredo Gonzalez-Sulser, University of Edinburgh
