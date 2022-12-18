
import numpy as np
import matplotlib.pyplot as plt
import mach_zender_interferometer_time_def
from scipy.fft import fft, fftfreq

print('')
print('optical-heterodyne-detection.py')
print('')

samplerate = 2048 # Sampling Frequency

stept = 1/samplerate

tcol = np.linspace(0.0, stept * samplerate, samplerate, endpoint=False)

amp_c = 0.01*np.pi
freq_am = 2
md = 1 # modulation depth. 1 = 100 %
dc_offset = 0 # DC offset

no = 1 # Refractive Index of medium

oplcommon1=100 #Common Path Length 1
oplcommon2=100 #Common Path Length 2

opl1 =100 
opl2= 100

wl1 = 100; #wavelength1
wl2 = 100; #wavelength2

PT1 = 0.5 # PT: Power Transmission of Beam splitter

# Define Input Electric Field: Both 1 and 2 port

#Ein1 = np.array([[1+0j],[1-0j]]) 
Ein1 = np.array([[0.707+0.707j],[-0.707-0.707j]])
#Ein1 = np.array([[1 + 0j],[-1 - 0j]])

#tcol = np.zeros(samplerate)
signalcol = np.zeros(samplerate)

Port1_1_EFcol = np.zeros(samplerate)
Port1_2_EFcol = np.zeros(samplerate)

Port3_1_EFcol = np.zeros(samplerate)
Port3_1_powercol = np.zeros(samplerate)

Port3_2_EFcol = np.zeros(samplerate)
Port3_2_powercol = np.zeros(samplerate)

Power_diffcol = np.zeros(samplerate)


for ii in range(samplerate):
    
    t = tcol[ii]

    signal = amp_c * np.sin(2 * np.pi * freq_am * t) + dc_offset
    signalcol[ii] = signal  
    
    Eout1 = mach_zender_interferometer_time_def.propagate2(wl1, wl2, no, t, t+signal, Ein1)
    

    Port1_1_Eout = Eout1[0,0] # Frequency modulated
    Port1_1_EFcol[ii] = Port1_1_Eout
    
    Port1_2_Eout = Eout1[1,0] # Local Oscillator
    Port1_2_EFcol[ii] = Port1_2_Eout


    Ein2 = Eout1

    Eout2 = mach_zender_interferometer_time_def.beamsplitter(PT1, Ein2)
    Ein3 = Eout2    
   
    Eout3 = mach_zender_interferometer_time_def.propagate2(wl1, wl2, no, oplcommon1, oplcommon2, Ein3)
    
    Port3_1_Eout = Eout3[0,0] # Trans
    Port3_1_EFcol[ii] = Port3_1_Eout

    power3_1 = (np.abs(Port3_1_Eout))**2 # Optical power is calculated as square of absolute electric field strength
    Port3_1_powercol[ii] = power3_1

    Port3_2_Eout = Eout3[1,0] #Reflect
    Port3_2_EFcol[ii] = Port3_2_Eout

    power3_2 = (np.abs(Port3_2_Eout))**2
    Port3_2_powercol[ii] = power3_2
    
    Power_diff = power3_1 - power3_2
    Power_diffcol[ii] = Power_diff
 
 

fig = plt.figure(figsize = (10,6), facecolor='lightblue')

ax1 = fig.add_subplot(4, 1, 1)
ax2 = fig.add_subplot(4, 1, 2)
ax3 = fig.add_subplot(4, 1, 3)
ax4 = fig.add_subplot(4, 1, 4)

ax1.plot(tcol,signalcol)
#ax1.set_ylim(-3,3)
ax1.set_ylabel("RF signal")

ax2.plot(tcol,np.abs(Port1_1_EFcol),tcol,np.abs(Port1_2_EFcol))
ax2.set_ylabel("Real Part of EF")
#ax2.set_ylim(-3, 3)
ax2.grid()


ax3.plot(tcol,Port3_1_powercol,tcol,Port3_2_powercol)
ax3.set_ylabel("Optical Power")
ax3.set_ylim(0,2.1)
ax3.grid()

ax4.plot(tcol,Power_diffcol)
ax4.set_xlabel("time")
ax4.set_ylabel("Power Difference")
ax4.grid()

plt.show()
