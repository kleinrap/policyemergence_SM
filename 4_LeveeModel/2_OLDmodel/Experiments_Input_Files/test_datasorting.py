import pandas as pd
import matplotlib.pyplot as plt

experiment_input = pd.read_csv("Experiments_LHS_9.data",header=None)

total_length = len(experiment_input.index)
variable = []
for i in range(total_length):
	variable.append(experiment_input[13][i])

print(variable)

ordered_indexes = []
for i in range(total_length):
	index_max = variable.index(max(variable))
	ordered_indexes.append(index_max)
	variable[index_max] = -10

print(ordered_indexes)
print(variable)



cmap = plt.get_cmap('jet_r')