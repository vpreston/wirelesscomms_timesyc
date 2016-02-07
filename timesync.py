import numpy
from numpy import fft
import matplotlib.pyplot as plt
import scipy

SAMPLE_RATE = 250e3#samples/second
TRANSMIT_FREQ = 2.4855e9*2*numpy.pi

data = []
real = []
imag = []

#get and process data
def open(filename='GRC scripts/test.dat'):
	data = numpy.fromfile(filename, dtype = 'float32')[2000:40000]
	real = data[0::2]
	imag = data[1::2]
	data = real+1j*imag
	# print data
	t = numpy.linspace(0, len(data), len(data))
	return data, t

#find offset frequency
def fourth(data):
	transform4 = fft.fft(numpy.power(data,4))
	freq = fft.fftfreq(len(data),SAMPLE_RATE)
	freq = [f*2*numpy.pi for f in freq]#convert frequency to radians
	impulse = (numpy.argmax(transform4))#get the frequency at which the impulse occurs
	return freq[impulse]

#apply offset frequency and use PLL
def process(offset, data, time):

	#PLL constants
	beta = 0.00005
	alpha = .00005

	#Use fft to do initial correction
	offset = offset/4#-9e-10 #offset is raised to the 4th, so when converted it is *4
	res = data*numpy.exp(-1j*offset*time*SAMPLE_RATE)

	# filtering code for error checking
	# filtered = res
	# filtered[(filtered.real+filtered.imag) > 0] = 1
	# filtered[(filtered.real+filtered.imag) <= 0] = -1 #filtering like this actually gives a really clean signal 

	#PLL implementation
	rms = numpy.sqrt(numpy.mean(numpy.square(res))) #get root mean squared error estimate
	w = res/rms #get error
	error = w.real*w.imag
	shift = beta*error
	integral = sum(error)*alpha
	pll_res = res*numpy.exp(-1j*time*(shift+integral))
	pll_res = pll_res.real + pll_res.imag

	return pll_res

if __name__=='__main__':

	data, time = open()
	offset = fourth(data)
	res = process(offset,data, time)

	plt.plot(res.real, label="Real")
	plt.plot(res.imag, label = "Imaginary")
	plt.legend()

	plt.show()




