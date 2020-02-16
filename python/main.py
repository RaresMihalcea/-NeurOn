from neuron import *
from dendrite import *
from soma import *

import matplotlib.pyplot as plt
import scipy.fftpack
import numpy as np
import cmath

ilt_flag=1

T=5.01
dt=0.01
t=np.arange(0, T, dt)
M=len(t)
domega=(2*math.pi)/M
omega_list=np.arange(0, ((math.pi *2)/dt), domega)
omega_list = list(omega_list)
omega_list.append(omega_list[-1] + domega)
omega_list=np.array(omega_list)

if ilt_flag == 0:
    omegas=omega_list
else: 
    omegas=omega_list * cmath.sqrt(-1)

green_results = []
ball_and_stick_dendrite = Dendrite(0, 1, 2, 50)
ball_and_stick_geometry = [
    [0, ball_and_stick_dendrite], 
    [ball_and_stick_dendrite, 0]
]
ball_and_stick_soma_index = 0
i=0

for omega in omegas:
    ball_and_stick = Neuron(ball_and_stick_soma_index, ball_and_stick_geometry, omega)
    ball_and_stick.stimulate(omega)
    ball_and_stick.set_measurement_location(0, ball_and_stick_geometry[0][1])
    ball_and_stick.set_input_location(0, ball_and_stick_geometry[0][1])
    green_results.append(ball_and_stick.greens_function())
    i+=1

if ilt_flag == 1: 
    T0=500.01
    dt=0.01
    t=np.arange(0, T0, dt)
    M=len(t)
    #TODO write stimp_amp formula in terms of soma diameter
    stim_Amp=1.591549430918954e+04
    stim_current=-0.2
    I=[]
    for i in t:
        I.append(stim_current*stim_Amp*math.sin(0.003*i**2))
    Om=len(green_results)
    fft_I=scipy.fftpack.fft(I, Om)
    sol_omega=[]
    sol_omega = np.multiply(green_results, fft_I)
    sol=np.fft.ifft(sol_omega)
    sol=sol.real
    sol=sol[0:M]
    x=np.linspace(0, T0, M)
    plt.xlabel("Time (mS)")
    plt.ylabel("Voltage (mV)")
    plt.plot(x, sol)
    plt.show()
else: 
    fig=plt.figure()
    fig.show()
    x = np.linspace(0,10,i)
    plt.xlabel("\u03C9")
    plt.ylabel("G(0, 0, \u03C9)")
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.plot(x, green_results)
    plt.show()