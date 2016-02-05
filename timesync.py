import numpy
from numpy import fft
import matplotlib.pyplot as plt

SAMPLE_RATE = 250e3#samples/second
TRANSMIT_FREQ = 2.4855e9*2*numpy.pi

data = []
real = []
imag = []

def open(filename='GRC scripts/Data/close.dat'):
	data = numpy.fromfile(filename, dtype = 'float32')[2000:20000]
	real = data[0::2]
	imag = data[1::2]
	data = real+1j*imag
	t = numpy.linspace(0, len(data), len(data))
	#plt.plot(real)
	#plt.plot(imag)
	#plt.show()
	return data, t

def fourth(data):
	#data = data[0::10]#downsample data so FFT finishes in reasonable time
	transform4 = fft.fft(numpy.power(data,4))
	# transform2 = fft.fft(numpy.power(data,2))[2:]
	#transform = fft.fft(data)[2:]
	freq = fft.fftfreq(len(data),SAMPLE_RATE)
	freq = [f*2*numpy.pi for f in freq]
	impulse = (numpy.argmax(transform4))#*2*numpy.pi)/len(transform4)
	print(impulse)
	#plt.plot(abs(transform4))
	#plt.show()
	return freq[impulse]

def process(offset, data, time):
	offset = offset/4 #offset is raised to the 4th, so when converted it is *4
	#print(offset)
	#print(data)
	res = data*numpy.exp(-1j*offset*time)
	#print(numpy.exp(1j*offset*time))
	print(res)
	plt.plot(data, label="data")
	plt.plot(res,label="results")
	plt.legend()
	plt.show()
	return res


if __name__=='__main__':
	data, time = open()
	offset = fourth(data)
	res = process(offset,data, time)
	print(res)
	#plt.plot(time,data)
	# plt.axis([0,0.35,-0.002,0.002])
	#plt.plot(time,res.real)
	#plt.plot(time,res.imag)
	#plt.plot(filtered)
	plt.show()
	#open()



