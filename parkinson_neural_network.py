from math import exp

# the data input is a dataset array in line 34  dataset = [[HNR,RPDE,DFA,PPE,STATUS]]
# STATUS is 0(no parkinson ) or 1( parkinson), if you dont have a estimeation remove.
# Calculate neuron activation for an input
def activate(weights, inputs):
	activation = weights[-1]
	for i in range(len(weights)-1):
		activation += weights[i] * inputs[i]
	return activation

# Transfer neuron activation
def transfer(activation):
	return 1.0 / (1.0 + exp(-activation))

# Forward propagate input to a network output
def forward_propagate(network, row):
	inputs = row
	for layer in network:
		new_inputs = []
		for neuron in layer:
			activation = activate(neuron['weights'], inputs)
			neuron['output'] = transfer(activation)
			new_inputs.append(neuron['output'])
		inputs = new_inputs
	return inputs

# Make a prediction with a network
def predict(network, row):
	outputs = forward_propagate(network, row)
	return outputs.index(max(outputs))

# Test making predictions with the network
dataset = [[0.079633,-0.234945,-0.144857,-0.643293,0]]
# rede neural treinada ---->  epoch=99999, lrate=0.350, error=6.004


network = [
[{'weights': [-0.24337357195494397, 1.018425743728825, -0.33349121207208915, 2.2049825838785186, -1.4204303512569345]},
{'weights': [-9.418302889153404, 8.807514020007815, -4.499461696258751, 12.69831835025589, 7.784476393943458]},
{'weights': [6.823430805360738, 5.986813438122784, -0.44862335870765113, -2.9913639923826163, -3.8006939935495723]},
{'weights': [-8.006668463341128, 5.590259280919226, -34.4963344874688, -16.943797653574357, -6.216896786650359]},
{'weights': [28.03883599019286, -16.214056798185894, 12.31772446190762, 15.851570991960413, 1.7456463032436078]},
{'weights': [18.634147704819775, 15.166940994104452, -14.118567620479046, 26.932575877725014, 17.902094156539707]},
{'weights': [27.6628885896468, 25.6104787225711, 24.926901924388964, 11.413271754370374, 0.06836841425524581]},
{'weights': [-37.089760010148154, 1.0417045582958337, 12.002547483943816, 8.209243898631325, 9.920702668642463]}],
[{'weights': [-0.15664241580610222, -15.417158535620143, 7.941296977960385, 26.2031485419118, -20.791091987131733, -27.67774640470994, 29.460651452122363, -24.23361193643314, 7.6767293935493095]},
{'weights': [0.7909103321633123, 15.379812555229186, -7.928213037316231, -26.213832526607092, 20.790820042343988, 27.667963418853763, -29.48000657029136, 24.229296147794376, -7.685249962277584]}]]


def neuralnet_main(row):
	prediction = predict(network, row)
	return prediction