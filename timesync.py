import numpy
from numpy import fft
import matplotlib.pyplot as plt

SAMPLE_RATE = 250e3#samples/second
TRANSMIT_FREQ = 2.4855e9*2*numpy.pi

data = []
real = []
imag = []

def open(filename='GRC scripts/test.dat'):
	data = numpy.fromfile(filename, dtype = 'float32')[2000:20000]
	real = data[0::2]
	imag = data[1::2]
	data = real+1j*imag
	# print data
	t = numpy.linspace(0, len(data), len(data))
	return data, t

def fourth(data):
	#data = data[0::10]#downsample data so FFT finishes in reasonable time
	transform4 = fft.fft(numpy.power(data,4))
	# transform2 = fft.fft(numpy.power(data,2))[2:]
	#transform = fft.fft(data)[2:]
	freq = fft.fftfreq(len(data),SAMPLE_RATE)
	freq = [f*2*numpy.pi for f in freq]
	impulse = (numpy.argmax(transform4))
	print(impulse)
	# plt.plot(abs(transform4), label = "FFT")
	# plt.legend()
	# plt.show()
	return freq[impulse]

def process(offset, data, time):
	offset = offset/4#-9e-10 #offset is raised to the 4th, so when converted it is *4
	# print(offset)
	#print(data)
	res = data*numpy.exp(-1j*offset*time*SAMPLE_RATE)
	# filtered = res
	# filtered[(filtered.real+filtered.imag) > 0] = 1
	# filtered[(filtered.real+filtered.imag) <= 0] = -1 #filtering like this actually gives a really clean signal
	rms = numpy.sqrt(numpy.mean(numpy.square(res))) 
	w = res/rms
	error = w.real*w.imag
	beta = 0.00005
	shift = beta*error
	pll_res = res*numpy.exp(-1j*time*shift)
	pll_res = pll_res.real + pll_res.imag
	# print(res)
	# plt.plot(data, label="data")
	# plt.plot(res,label="results")
	# plt.legend()
	# plt.show()
	return pll_res

if __name__=='__main__':
	data, time = open()
	offset = fourth(data)
	res = process(offset,data, time)
	print(res)
	#plt.plot(time,data)
	# plt.axis([0,9000,-1.1,1.1])
	plt.plot(res.real, label="Real")
	plt.plot(res.imag, label = "Imaginary")
	# plt.legend()
	#plt.plot(abs(res), label= "Absolute Value")
	# plt.scatter(res.real,res.imag)
	plt.show()
	#open()



