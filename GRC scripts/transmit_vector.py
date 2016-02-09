import numpy as np

def make_vector(vector_length, upsample):
	elements = np.round(np.random.rand(vector_length))
	elements = (elements * 2 - 1) / 100
	output_vector = []
	for value in elements:
		for i in range(upsample):
			output_vector.append(value)
	output_vector = np.array(output_vector)
	return output_vector

to_file = make_vector(100,100)
np.save('transmit_this', to_file)
