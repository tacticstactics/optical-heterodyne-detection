import numpy as np

def prbs_1(samplerate, a1_range = [0,1], b1_range = [10, 50]):

    #a1_range = [0, 1] # amplitude range
    a1 = np.random.rand(samplerate) * (a1_range[1]-a1_range[0]) + a1_range[0] 
    #b1_range = [10, 50] # frequency range
    b1 = np.random.rand(samplerate) *(b1_range[1]-b1_range[0]) + b1_range[0] 
    
    b1 = np.round(b1)
    b1 = b1.astype(int)
    
    b1[0] = 0
    for i in range(1,np.size(b1)):
        b1[i] = b1[i-1]+b1[i]
        
        
    i=0
    random_analog_signal = np.zeros(samplerate)
    while b1[i]<np.size(random_analog_signal):
        k = b1[i]
        random_analog_signal[k:] = a1[i]
    i=i+1
    
    
    # prbs1, Pseudo random digital signal(prbs), type 1
    amp_prbs = 1
    a1 = np.zeros(samplerate)
    
    j = 0
    while j < samplerate:
        a1[j] = amp_prbs
        a1[j+1] = 0
        j = j+2
        
    i=0
    rfsignalcol = np.zeros(samplerate)
    while b1[i]<np.size(rfsignalcol):
        k = b1[i]
        rfsignalcol[k:] = a1[i]
        i=i+1
    
    return rfsignalcol


def prbs_2(samplerate, numberofpointspersymbol = 2 ** 4):
    
    amp_prbs = np.pi
    
    repetitions1 = samplerate / numberofpointspersymbol
    
    rand_int1 = np.random.randint(0, 2, numberofpointspersymbol) # 0 or 1
    
    rfsignalcol = amp_prbs * np.repeat(rand_int1, repetitions1) - 0.5*np.pi

    return rfsignalcol

