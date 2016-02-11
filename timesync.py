import numpy
from numpy import fft
import matplotlib.pyplot as plt
import scipy
from scipy import special

SAMPLE_RATE = 250e3#samples/second
TRANSMIT_FREQ = 2.4855e9*2*numpy.pi

data = []
real = []
imag = []

#get and process data
def open(filename='GRC scripts/Data/10ps.dat'):
	data = numpy.fromfile(filename, dtype = 'float32')[5000:10000]
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
	impulse = (numpy.argmax(transform4))#get the frequency at which the impulse occurs
	return freq[impulse]

#apply offset frequency and use PLL
def process(offset, data, time):

	#PLL constants
	beta = .1
	alpha =  50

	#PLL storage
	total_error = 0
	pll_res = []

	#Use fft to do initial correction
	offset = offset/4#-9e-10 #offset is raised to the 4th, so when converted it is *4

	for index in range(0, len(data)-1):
		pll_res.append(data[index]*numpy.exp(-1j*offset*SAMPLE_RATE))
		error = pll_res[index].real*pll_res[index].imag
		sample = pll_res[index]
		total_error += error
		offset = offset + beta*error

	return numpy.asarray(pll_res)

def error_calc(data):

	noise = numpy.abs(open('GRC scripts/Data/noise.dat'))
	sigma = numpy.sqrt(numpy.mean(numpy.power(noise,2)))
	A = numpy.mean([x >.005 for x in data])

	error =  0.5-0.5*special.erfc((A/sigma)/numpy.sqrt(2))

	return error

if __name__=='__main__':

	data, time = open()
	offset = fourth(data)
	res = process(offset,data, time)
	print error_calc(res)

	plt.plot(res)
	plt.legend()
	plt.title("Processed Signal")

	plt.show()




