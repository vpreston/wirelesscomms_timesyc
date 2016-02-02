import numpy
from numpy import fft
import matplotlib.pyplot as plt

SAMPLE_RATE = 32e3*2*numpy.pi#samples/second
TRANSMIT_FREQ = 2.4855e9*2*numpy.pi

data = []
real = []
imag = []

def open(filename='GRC scripts/test.dat'):
	data = numpy.fromfile(filename, dtype = 'float32')[2000:]
	real = data[0::2]
	imag = data[1::2]
	t = numpy.linspace(0, len(real)/SAMPLE_RATE,len(real))
	#plt.plot(real)
	#plt.plot(imag)
	#plt.show()
	print real
	return real, t

def fourth(data):
	transform4 = fft.fft(numpy.power(data,4)[0::10])[2:]
	transform = fft.fft(data[0::10])[2:]
	freq = fft.fftfreq(len(data[0::10]),SAMPLE_RATE/10)[2:]# division by 10 is because of downsampling
	impulse = numpy.argmax(transform4)
	print(impulse)
	print(freq[impulse])
	#plt.plot(freq,transform.real, label = "real")
	#plt.plot(freq,transform.imag, label = "imag")
	#plt.plot(freq,transform4.real, label = "real4")
	#plt.plot(freq,transform4.imag, label = "imag4")
	#plt.legend()
	#plt.show()
	return abs(freq[impulse])

def process(offset, data, time):
	offset = offset/4 #offset is raised to the 4th, so when converted it is *4
	res = data*numpy.cos([t*(TRANSMIT_FREQ-offset) for t in time])
	#plt.plot(data)
	#plt.plot(res)
	#plt.show()
	return res


if __name__=='__main__':
	data, time = open()
	offset = fourth(data)
	res = process(offset,data, time)
	#plt.plot(time,data)
	plt.plot(time,res)
	plt.show()
	#open()



