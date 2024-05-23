import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

def s_i(maxi,f_c,A_i,t):
	return np.float32(A_i/maxi*np.cos(2*np.pi*f_c*t))

def adapt(data,dt):
	return np.repeat(data,dt)

def s(maxi,f_c,A,T_e,dt):
	signal = np.array([s_i(maxi,f_c,A[i],i*T_e) for i in range(len(A))],dtype="float32")
	
	print(signal)
	return signal


F_C = 7e3
F_E = 50*F_C
T_E = 1/F_E
R = 1000
dt = int(F_E/R)


print("Loading")
data = adapt(np.fromfile('flag.png', dtype = "uint8"),dt)
print(data)
print("Getting signal")
signal = s(255,F_C,data,T_E,dt)

signal.tofile("flag.raw")

F_C = 7e3
F_E = 50*F_C
T_E = 1/F_E
R = 1000
dt = int(F_E/R)

s_load = np.fromfile('flag.raw',dtype="float32")

s = abs(s_load)
plt.plot([i for i in range(10*dt)], s_load[:10*dt])
plt.plot([i for i in range(10*dt)], s[:10*dt])
plt.show()
def demodulate(s):
	dt = int(F_E/R)
	env = []
	for i in range(0,len(s),dt):
		env.append(np.mean(s[i:i+dt]))
	env = np.array(env,dtype="float64")
	print([env[i]/max(s[dt*i:dt*i+dt]) for i in range(15)])
	#plt.plot([i for i in range(dt*10)],np.repeat(env,dt)[:10*dt])
	#plt.plot([i for i in range(dt*10)],np.fromfile('flag.raw',dtype="float64")[:10*dt])
	env /= max(env)
	env *= 255
	print(max(env))
	#plt.show()
	env = np.round(env)
	print(max(env))
	print(env)
	return env
np.array(demodulate(s),'uint8').tofile("decoded.png")