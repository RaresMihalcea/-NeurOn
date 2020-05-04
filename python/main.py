from neuron import *
from dendrite import *
from soma import *

import matplotlib.pyplot as plt
import scipy.fftpack
import numpy as np
import cmath
import sys
import json

# print(sys.argv)

data = json.loads(sys.argv[1])

ilt_flag=data['frequencyDomainFlag']

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

matrix = data['matrix']
geometry=[]
for i in range(len(matrix)):
    geometry.append([])
    for j in range(len(matrix[i])):
        geometry[i].append(0)

for i in range(len(matrix)):
   for j in range(len(matrix[i])):
        if (not isinstance(geometry[i][j], Dendrite)) and matrix[i][j] != 0:
            dendrite = Dendrite(i, j, data['a'], matrix[i][j], data)
            geometry[i][j] = dendrite
            geometry[j][i] = dendrite

soma_index = data['somaIndex']
i=0



if ilt_flag == 0:
    for i in range(len(omegas[0:800])):
        if i == 0:
            neuron = Neuron(soma_index, geometry, omegas[i], data, True)
        else:
            neuron = Neuron(soma_index, geometry, omegas[i], data, False)
        neuron.stimulate(omegas[i])
        neuron.set_measurement_location(data['xDistance'], geometry[data['xFirstNode']][data['xSecondNode']])
        neuron.set_input_location(data['yDistance'], geometry[data['yFirstNode']][data['ySecondNode']])
        green_results.append(neuron.greens_function())
        i+=1
else:
    for i in range(len(omegas)):
        if i == 0:
            neuron = Neuron(soma_index, geometry, omegas[i], data, True)
        else:
            neuron = Neuron(soma_index, geometry, omegas[i], data, False)
        neuron.stimulate(omegas[i])
        neuron.set_measurement_location(data['xDistance'], geometry[data['xFirstNode']][data['xSecondNode']])
        neuron.set_input_location(data['yDistance'], geometry[data['yFirstNode']][data['ySecondNode']])
        green_results.append(neuron.greens_function())
        i+=1

print("Peak Output: {}".format(max(green_results)))
print("Starting Output: {}".format(green_results[0]))
print("Convergence Value: {}".format(green_results[-1]))

# file1 = open("out.txt","w") 

# out = "["
# for i in green_results:
#     out += i
#     out += ','
# out += "]"

# file1.write(out)


if ilt_flag == 1: 
    T0=500.01
    dt=0.01
    t=np.arange(0, T0, dt)
    M=len(t)
    stim_Amp=1*1e5/(math.pi*data['a']*data['C'])
    stim_current=-1 * data['A']
    I=[]
    for i in t:
        I.append(stim_current*stim_Amp*math.sin(data['omega']*i**2))    
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
    plt.yticks(np.arange(-12, 12, step=2))
    plt.xticks(np.arange(0, 500, step=50))
    plt.plot(x, sol)
    plt.show()
elif ilt_flag == 2:
    T0=data['T_total_step'] + 0.01
    dt=0.01
    # (t-del>=0).*((del+tR)-t>=0)
    #  Here del is your start time and del+tR is your end time.
    t=np.arange(0, T0, dt)
    M=len(t)
    stim_Amp=1*1e5/(math.pi*data['a']*data['C'])
    # stim_Amp=1.5915e4
    stim_current=data['omega_step']
    # stim_current = 0.2
    I=[]
    for i in t:
        if i >= data['T_zero'] and i <= data['T_end']:
            I.append(stim_current*stim_Amp)
        else:
            I.append(0)
    Om=len(green_results)
    # fft_I=scipy.fftpack.hfft(I, Om)
    fft_I = np.fft.rfft(I, Om)
    sol_omega=[]
    sol_omega = np.multiply(green_results[0:fft_I.size], fft_I)
    sol=np.fft.irfft(sol_omega)
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
    plt.ylabel("G({}, {}, \u03C9)".format(data['xDistance'], data['yDistance']))
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
    plt.plot(x, green_results)
    plt.show()

print('finished')