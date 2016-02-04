import numpy
from numpy import fft
import matplotlib.pyplot as plt

SAMPLE_RATE = 32e3#samples/second
TRANSMIT_FREQ = 2.4855e9*2*numpy.pi

data = []
real = []
imag = []

def open(filename='GRC scripts/test.dat'):
	data = numpy.fromfile(filename, dtype = 'float32')[2000:4000]
	real = data[0::2]
	imag = data[1::2]
	t = numpy.linspace(0, len(real)/SAMPLE_RATE,len(real))
	#plt.plot(real)
	#plt.plot(imag)
	#plt.show()
	return real, t

def fourth(data):
	#data = data[0::10]#downsample data so FFT finishes in reasonable time
	#transform4 = fft.fft(numpy.power(data,4))[2:]
	transform2 = fft.fft(numpy.power(data,2))[2:]
	#transform = fft.fft(data)
	freq = fft.fftfreq(len(data),SAMPLE_RATE)[2:]# division by 10 is because of downsampling
	freq = [f*2*numpy.pi for f in freq]
	impulse = numpy.argmax(transform2)
	#print(impulse)
	#print(freq[impulse])
	#plt.plot(freq,transform.real, label = "real")
	#plt.plot(freq,transform.imag, label = "imag")
	#plt.plot(freq,transform4.real, label = "real4")
	#plt.plot(freq,transform4.imag, label = "imag4")
	#plt.legend()
	return freq[impulse]

def process(offset, data, time):
	offset = offset/2 #offset is raised to the 4th, so when converted it is *4
	res = data*numpy.exp(1j*offset*TRANSMIT_FREQ)
	#plt.plot(data)
	#plt.plot(res)
	#plt.show()
	filtered = [1 if r > 0 else -1 for r in res]
	return res, filtered


if __name__=='__main__':
	data, time = open()
	offset = fourth(data)
	res, filtered = process(offset,data, time)
	#plt.plot(time,data)
	plt.axis([0,.035,-1.5,1.5])
	plt.plot(time,res)
	plt.plot(time,filtered)
	plt.show()
	#open()



