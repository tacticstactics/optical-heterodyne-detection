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
    prbs1 = np.zeros(samplerate)
    while b1[i]<np.size(prbs1):
        k = b1[i]
        prbs1[k:] = a1[i]
        i=i+1
    
    return prbs1

def prbs_2(phase1, phase2, Ein=np.array([[1],[0]])):

    propagatematrix1 = np.array([[np.exp(1j*phase1),0],[0,np.exp(1j*phase2)]]);

    Eout = np.dot(propagatematrix1,Ein)
    
    return prbs_2

