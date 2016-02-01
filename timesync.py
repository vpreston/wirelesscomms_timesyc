import numpy
from numpy import fft
import matplotlib.pyplot as plt

data = []
real = []
imag = []

def open(filename='GRC scripts/test.dat'):
	data = numpy.fromfile(filename, dtype = 'float32')[2000:]
	real = data[0::2]
	imag = data[1::2]
	print numpy.size(data)
	#plt.plot(real)
	#plt.plot(imag)
	#plt.show()
	return real

def fourth(data):
	transform4 = fft.fft(numpy.power(data,4)[0::10])[2:]
	transform = fft.fft(data[0::10])[2:]
	freq = fft.fftfreq(len(data[0::10]))[2:]
	impulse = numpy.argmax(transform4)
	print(impulse)
	print(freq[impulse])
	#plt.plot(freq,transform.real, label = "real")
	#plt.plot(freq,transform.imag, label = "imag")
	plt.plot(freq,transform4.real, label = "real4")
	plt.plot(freq,transform4.imag, label = "imag4")
	plt.legend()
	plt.show()

def convert(hz):
	print("not implemented")






if __name__=='__main__':
	fourth(open())
	#open()



