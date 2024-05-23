import numpy as np
import matplotlib.pyplot as plt

def QAM16(symbol):
	return -3+2*(symbol>>2)+1j*(3-2*(symbol&0b11))
def DEQAM16(code):
	return round((np.real(code)+3)*2)+round(-1*(np.imag(code)-3)/2)
def adapt(data,dt):
	return np.repeat(data,dt)

def map_bytes(bytes_list):
	mapped_symbols = []
	for b in bytes_list:
		mapped_symbols += [QAM16(b>>4),QAM16(b&0b1111)]
	return mapped_symbols

def fft_inv(T,N,X,t):
	return sum([X[k]*np.exp(2j*np.pi*k*t/T) for k in range(N)])

def fft(T,N,X,k):
	return np.mean([X[t]*np.exp(-1*2j*np.pi*k*t*T_E/T) for t in range(int(T*F_E))])


NB_SOUS_PORTEUSES = 8
F_C = 7e3
F_E = int(50*F_C)
T_E = 1/F_E
R = 1000
T = 1/R
"""
print(F_E*T)
print("Loading")
data = np.fromfile('flag.png', dtype = "uint8")
modulated = []
print(len(data)%4)
for i in range(0,len(data),4):
	mapped = np.array(map_bytes(data[i:i+4]))
	#print(len(mapped))
	modulated += [fft_inv(T,NB_SOUS_PORTEUSES,mapped,t*T_E) for t in range(int(F_E*T))]

#print(modulated)
plt.plot([t*T_E for t in range(5*int(F_E*T))],modulated[:5*int(F_E*T)])
plt.show()
np.array(modulated,dtype='complex64').tofile("flag.iq")


"""
test = np.fromfile('flag.png', dtype = "uint8")
print(np.array(map_bytes(test[0:4])))
data = np.fromfile('flag.iq', dtype = "complex64")
demodulated = []
for i in range(0,len(data),int(F_E*T)):
	demodulated += [fft(T,NB_SOUS_PORTEUSES,data[i:i+int(F_E*T)],k) for k in range(8)]
print(demodulated[:5])
output = []
for i in range(0,len(demodulated),2):
	output.append((DEQAM16(demodulated[i])*16)+DEQAM16(demodulated[i+1]))
print(output[:10])
print(len(output))

np.array(output,dtype='uint8').tofile('decoded.png')
plt.plot([t*T_E for t in range(5*int(F_E*T))],demodulated[:5*int(F_E*T)])
plt.show()