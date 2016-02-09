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
	data = numpy.fromfile(filename, dtype = 'float32')[5000:45000]
	real = data[0::2]
	imag = data[1::2]
	data = real+1j*imag

	t = numpy.linspace(0, len(data), len(data))
	return data, t

#find offset frequency
def fourth(data):
	transform4 = fft.fft(numpy.power(data,4))
	freq = fft.fftfreq(len(data),SAMPLE_RATE)
	freq = [f*2*numpy.pi for f in freq]#convert frequency to radians
	# plt.plot(freq,transform4)
	# plt.xlabel("Frequency (radians)")
	# plt.ylabel("V^4")
	# plt.show()
	impulse = (numpy.argmax(transform4))#get the frequency at which the impulse occurs
	return freq[impulse]

#apply offset frequency and use PLL
def process(offset, data, time):

	#PLL constants
	beta = 0.1
	alpha =  50

	#PLL storage
	total_error = 0
	pll_res = []

	#Use fft to do initial correction
	offset = offset/4#-9e-10 #offset is raised to the 4th, so when converted it is *4
	# res = data*numpy.exp(-1j*offset*time*SAMPLE_RATE)

	# filtering code for error checking
	# filtered = res
	# filtered[(filtered.real+filtered.imag) > 0] = 1
	# filtered[(filtered.real+filtered.imag) <= 0] = -1 #filtering like this actually gives a really clean signal 

	#PLL implementation
	# rms = numpy.sqrt(numpy.mean(numpy.square(res))) #get root mean squared error estimate
	# w = res/rms #get error
	# error = w.real*w.imag
	# shift = beta*error
	# integral = sum(error)*alpha
	# pll_res = res*numpy.exp(-1j*time*(shift+integral))
	# pll_res = pll_res.real + pll_res.imag

	for index in range(0, len(data)-1):
		pll_res.append(data[index]*numpy.exp(-1j*offset*SAMPLE_RATE))
		error = pll_res[index].real*pll_res[index].imag
		total_error += error
		offset = offset + beta*error

	return pll_res

# def error_calc(data):
# 	data = abs(data)
# 	amp = numpy.mean(data)
# 	noise = open



if __name__=='__main__':

	data, time = open()
	# plt.plot(data,time)
	# plt.xlabel("Time (s/250000)")
	# plt.ylabel("Received Signal (V)")
	# plt.title("Unprocessed")
	offset = fourth(data)
	res = process(offset,data, time)
	#print(interpret(res))

	# plt.plot(res.real, label="Real")
	# plt.plot(res.imag, label = "Imaginary")
	plt.plot(res)
	plt.legend()

	plt.show()




