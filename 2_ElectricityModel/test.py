# import pandas as pd


# # loading the solar from input data
# inputFile_solar = 'solar.csv'
# input_solar = pd.read_csv(inputFile_solar, sep=',')
# # input_solar = input_solar.drop(0) # dropping the line with the years
# solar_conditions = []
# # below is a very slow loop that could be sped up - would np.array be better?
# for i in range(3):
# 	for j in range(8760):
# 		solar_conditions.append(input_solar.iloc[j][1+i])

# total_number_points = len(solar_conditions)

# stepCount = 100230
# print(solar_conditions[stepCount%total_number_points], stepCount%total_number_points)


for i in range(8760*10):
	print(i)
	if i % int(9 * 24 * 12) == 0: # maitenance month * 30 days * 24 hours
		print(i, int(9 * 24 * 12))