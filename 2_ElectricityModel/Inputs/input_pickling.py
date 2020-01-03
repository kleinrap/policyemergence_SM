import pandas as pd
import time
import pickle

eur_to_chf = 1.10

# loading the load curve
print('Loading the load curve')
start = time.time()
inputFile_load = 'load.csv'
input_load = pd.read_csv(inputFile_load, sep=',')
input_load = input_load.drop(0) # dropping the line with the years
load = []
load_factor = []
# below is a very slow loop that could be sped up - would np.array be better?
for i in range(3):
# for i in range(run_input):
	for j in range(8760):
		load.append(input_load.iloc[j][1+i])
		load_factor.append(input_load.iloc[j][7+i])
end = time.time()
print('Time:', end-start)
print(' ')

load_input = [load, load_factor]
with open('input_load_input.pkl', 'wb') as f:
	pickle.dump(load_input, f)


# loading the solar from input data
print('Loading the solar input data')
start = time.time()
inputFile_solar = 'solar.csv'
input_solar = pd.read_csv(inputFile_solar, sep=',')
solar_conditions = []
# below is a very slow loop that could be sped up - would np.array be better?
for i in range(3):
	for j in range(8760):
		solar_conditions.append(input_solar.iloc[j][1+i])
end = time.time()
print('Time:', end-start)
print(' ')

with open('input_solar_conditions.pkl', 'wb') as f:
	pickle.dump(solar_conditions, f)

# loading the wind from input data
print('Loading the wind input data')
start = time.time()
inputFile_wind = 'wind.csv'
input_wind = pd.read_csv(inputFile_wind, sep=',')
wind_conditions = []
# below is a very slow loop that could be sped up - would np.array be better?
for i in range(3):
	for j in range(8760):
		wind_conditions.append(input_wind.iloc[j][1+i])
end = time.time()
print(' ')
print('Time:', end-start)

with open('input_wind_conditions.pkl', 'wb') as f:
	pickle.dump(wind_conditions, f)



# loading the hydro from input data
print('Loading the hydro input data')
start = time.time()
inputFile_hydro = 'hydro.csv'
input_hydro = pd.read_csv(inputFile_hydro, sep=',')
hydro_conditions = []
# below is a very slow loop that could be sped up - would np.array be better?
for i in range(5):
	for j in range(8760):
		hydro_conditions.append(input_hydro.iloc[j][1+i])
end = time.time()
print(' ')
print('Time:', end-start)

with open('input_hydro_conditions.pkl', 'wb') as f:
	pickle.dump(hydro_conditions, f)

# loading the run of river from input data
print('Loading the run of river input data')
start = time.time()
inputFile_ror = 'ror.csv'
input_ror = pd.read_csv(inputFile_ror, sep=',')
ror_conditions = []
# below is a very slow loop that could be sped up - would np.array be better?
for i in range(4):
	for j in range(8760):
		ror_conditions.append(input_ror.iloc[j][1+i])
end = time.time()
print('Time:', end-start)
print(' ')

with open('input_ror.pkl', 'wb') as f:
	pickle.dump(ror_conditions, f)


# loading the foreign electricity prices from input data
print('Loading the foreign electricity prices')
start = time.time()
inputFile_foreign = 'foreign.csv'
input_foreign = pd.read_csv(inputFile_foreign, sep=',')
input_foreign = input_foreign.drop(0) # dropping the line with the years
price_FR = []
price_DE = []
price_IT = []
# below is a very slow loop that could be sped up - would np.array be better?
for i in range(2):
# for i in range(run_input):
	for j in range(8760):
		price_FR.append(input_foreign.iloc[j][11+i] * eur_to_chf)
		price_DE.append(input_foreign.iloc[j][14+i] * eur_to_chf)
		price_IT.append(input_foreign.iloc[j][17+i] * eur_to_chf)
end = time.time()
print('Time:', end-start)
print(' ')

price_foreign = [price_FR, price_DE, price_IT]

with open('input_price_foreign.pkl', 'wb') as f:
	pickle.dump(price_foreign, f)


# loading the french border capacity of river from input data
print('Loading the French border capacity')
start = time.time()
inputFile_capacity_fr = 'ntcfr.csv'
input_capacity_fr = pd.read_csv(inputFile_capacity_fr, sep=',')
input_capacity_fr = input_capacity_fr.drop(0) # dropping the line with the years
capacity_fr_im = []
capacity_fr_ex = []
# below is a very slow loop that could be sped up - would np.array be better?
for i in range(3):
# for i in range(run_input):
	for j in range(8760):
		capacity_fr_ex.append(input_capacity_fr.iloc[j][1+i] * input_capacity_fr.iloc[j][7+i])
		capacity_fr_im.append(input_capacity_fr.iloc[j][4+i] * input_capacity_fr.iloc[j][10+i])
end = time.time()
print('Time:', end-start)
print(' ')

# loading the german border capacity of river from input data
print('Loading the German border capacity')
start = time.time()
inputFile_capacity_de = 'ntcde.csv'
input_capacity_de = pd.read_csv(inputFile_capacity_de, sep=',')
input_capacity_de = input_capacity_de.drop(0) # dropping the line with the years
capacity_de_im = []
capacity_de_ex = []
# below is a very slow loop that could be sped up - would np.array be better?
for i in range(3):
# for i in range(run_input):
	for j in range(8760):
		capacity_de_ex.append(input_capacity_de.iloc[j][1+i] * input_capacity_de.iloc[j][7+i])
		capacity_de_im.append(input_capacity_de.iloc[j][4+i] * input_capacity_de.iloc[j][10+i])
end = time.time()
print('Time:', end-start)
print(' ')


# loading the italian border capacity of river from input data
print('Loading the Italian border capacity')
start = time.time()
inputFile_capacity_it = 'ntcit.csv'
input_capacity_it = pd.read_csv(inputFile_capacity_it, sep=',')
input_capacity_it = input_capacity_it.drop(0) # dropping the line with the years
capacity_it_im = []
capacity_it_ex = []
# below is a very slow loop that could be sped up - would np.array be better?
for i in range(2):
	for j in range(8760):
		capacity_it_ex.append(float(input_capacity_it.iloc[j][1+i]) * input_capacity_it.iloc[j][7+i])
		capacity_it_im.append(float(input_capacity_it.iloc[j][4+i]) * input_capacity_it.iloc[j][10+i])
end = time.time()
print('Time:', end-start)
print(' ')

capacity_ex = [capacity_fr_ex, capacity_de_ex, capacity_it_ex]
capacity_im = [capacity_fr_im, capacity_de_im, capacity_it_im]

capacity_foreign = [capacity_ex, capacity_im]

with open('input_capacity_foreign.pkl', 'wb') as f:
    pickle.dump(capacity_foreign, f)

