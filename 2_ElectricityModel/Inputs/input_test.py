import pickle
import time

# loading the load curve
print('Loading the load curve')
start = time.time()
with open('input_load_input.pkl', 'rb') as f:
    load_input = pickle.load(f)

load = load_input[0]
load_factor = load_input[1]

end = time.time()
print('Time:', end-start)
print(' ')

# loading the solar from input data
print('Loading the solar input data')
start = time.time()
with open('input_solar_conditions.pkl', 'rb') as f:
    solar_conditions = pickle.load(f)

end = time.time()
print('Time:', end-start)
print(' ')

# loading the wind from input data
print('Loading the wind input data')
start = time.time()
with open('input_wind_conditions.pkl', 'rb') as f:
    wind_conditions = pickle.load(f)
end = time.time()
print('Time:', end-start)
print(' ')


# loading the run of river from input data
print('Loading the run of river input data')
start = time.time()
with open('input_ror.pkl', 'rb') as f:
    ror_conditions = pickle.load(f)
end = time.time()
print('Time:', end-start)
print(' ')


# loading the foreign electricity prices from input data
print('Loading the foreign electricity prices')
start = time.time()
with open('input_price_foreign.pkl', 'rb') as f:
    price_foreign = pickle.load(f)
price_FR = price_foreign[0]
price_DE = price_foreign[1]
price_IT = price_foreign[2]
end = time.time()
print('Time:', end-start)
print(' ')


# loading the foreign border capacities
print('Loading the foreign border capacities')
start = time.time()
with open('input_capacity_foreign.pkl', 'rb') as f:
    capacity_foreign = pickle.load(f)
end = time.time()
capacity_ex = capacity_foreign[0]
capacity_im = capacity_foreign[1]
print('Time:', end-start)
print(' ')

