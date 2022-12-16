

import numpy as np
import matplotlib.pyplot as plt

import mach_zender_interferometer_time_def

print('')
print('optical-heterodyne-detection.py')
print('')

samplerate = 2048 # Sampling Frequency

stept = 1/samplerate

amp_c = 2*3.14
freq_am = 2
md = 1 # modulation depth. 1 = 100 %
dc_offset = 0 # DC offset

no = 1 # Refractive Index of medium

oplcommon1=100 #Common Path Length 1
oplcommon2=100 #Common Path Length 2

opl1 =100 
opl2= 100

wl = 7.80; #wavelength

PT1 = 0.5 # PT: Power Transmission of Beam splitter

# Define Input Electric Field: Both 1 and 2 port

#Ein1 = np.array([[1+0j],[1-0j]]) 
#Ein1 = np.array([[0.707+0.707j],[-0.707-0.707j]])
Ein1 = np.array([[1 + 0j],[-1 - 0j]])

tcol = np.zeros(samplerate)
signalcol = np.zeros(samplerate)

Port1_powercol = np.zeros(samplerate)
Port1_EFcol = np.zeros(samplerate)

Port2_powercol = np.zeros(samplerate)
Port2_EFcol = np.zeros(samplerate)

Power_diffcol = np.zeros(samplerate)


for ii in range(samplerate):
    
    t = stept * ii
    tcol[ii] = t

    signal = amp_c * np.sin(2 * np.pi * freq_am * t) + dc_offset
    signalcol[ii] = signal  
    
    Eout1 = mach_zender_interferometer_time_def.propagate1(wl, no, opl1, opl2+signal, Ein1)
    Ein2 = Eout1
    
    Eout2 = mach_zender_interferometer_time_def.beamsplitter(PT1, Ein2)
    Ein3 = Eout2    
   
    Eout3 = mach_zender_interferometer_time_def.propagate1(wl, no, oplcommon1, oplcommon2, Ein3)
    
    Port1_Eout = Eout3[0,0] # Trans

    Port1_EFcol[ii] = Port1_Eout

    power_11 = (np.abs(Port1_Eout))**2 # Optical power is calculated as square of absolute electric field strength
    Port1_powercol[ii] = power_11    
    
    Port2_Eout = Eout3[1,0] #Reflect
    power_22 = (np.abs(Port2_Eout))**2
    
    Port2_powercol[ii] = power_22
    Port2_EFcol[ii] = Port2_Eout

    Power_diff = power_11 - power_22
    Power_diffcol[ii] = Power_diff
 
 

fig = plt.figure(figsize = (10,6), facecolor='lightblue')

ax1 = fig.add_subplot(3, 1, 1)
ax2 = fig.add_subplot(3, 1, 2)
ax3 = fig.add_subplot(3, 1, 3)

ax1.plot(tcol,signalcol)
#ax1.set_ylim(-3,3)
ax1.set_ylabel("RF signal")

ax2.plot(tcol,Port1_powercol,tcol,Port2_powercol)

ax2.set_ylabel("Optical Power")
ax2.set_ylim(0,2.1)
ax2.grid()

ax3.plot(tcol,Power_diffcol)
ax3.set_xlabel("time")
ax3.set_ylabel("Power Difference")
#ax3.set_ylim(-2,2)
ax3.grid()

plt.show()
