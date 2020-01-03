'''
This is a file used to process the Results files from the electricity model
'''

import pandas as pd

input_file = 'test_results.csv'
results = pd.read_csv(input_file)
results_head = results.columns # getting the column names
print(results.head())
print(results.columns)

# supply: [solar, wind, CCGT, hydro, hydrop, nuclear, waste, runofriver,
#         LTC, NTC, NTC_FR, NTC_DE, NTC_IT]
# deand: [demand_met, hydrop, NTC, NTC_FR, NTC_DE, NTC_IT]

demand = []
supply = []

# saving the paremeters in different arrays
for index, row in results.iterrows():
    demand.append(row['demand_array'])
    supply.append(row['supply'])

# splitting lists
supply_solar = []
supply_wind = []
supply_CCGT = []
supply_hydro = []
supply_hydrop = []
supply_nuclear = []
supply_waste = []
supply_runofriver = []
supply_LTC = []
supply_NTC = []
supply_NTC_FR = []
supply_NTC_DE = []
supply_NTC_IT = []

elastic_demand = []
demand_hydrop = []
demand_NTC = []
demand_NTC_FR = []
demand_NTC_DE = []
demand_NTC_IT = []

for i in range(len(demand)):
    if i % 8760 == 0:
        print(i/8760)
    supply_solar.append(eval(supply[i])[0])
    supply_wind.append(eval(supply[i])[1])
    supply_CCGT.append(eval(supply[i])[2])
    supply_hydro.append(eval(supply[i])[3])
    supply_hydrop.append(eval(supply[i])[4])
    supply_nuclear.append(eval(supply[i])[5])
    supply_waste.append(eval(supply[i])[6])
    supply_runofriver.append(eval(supply[i])[7])
    supply_LTC.append(eval(supply[i])[8])
    supply_NTC.append(eval(supply[i])[9])
    supply_NTC_FR.append(eval(supply[i])[10])
    supply_NTC_DE.append(eval(supply[i])[11])
    supply_NTC_IT.append(eval(supply[i])[12])

    elastic_demand.append(eval(demand[i])[0])
    demand_hydrop.append(eval(demand[i])[1])
    demand_NTC.append(eval(demand[i])[2])
    demand_NTC_FR.append(eval(demand[i])[3])
    demand_NTC_DE.append(eval(demand[i])[4])
    demand_NTC_IT.append(eval(demand[i])[5])


# constructing a new intermediate panda
inter_results_df = results.drop(['Unnamed: 0','step','demand_array', 'supply'], axis = 1)
inter_results_df['supply_solar'] = supply_solar
inter_results_df['supply_wind'] = supply_wind
inter_results_df['supply_CCGT'] = supply_CCGT
inter_results_df['supply_hydro'] = supply_hydro
inter_results_df['supply_hydrop'] = supply_hydrop
inter_results_df['supply_nuclear'] = supply_nuclear
inter_results_df['supply_waste'] = supply_waste
inter_results_df['supply_runofriver'] = supply_runofriver
inter_results_df['supply_LTC'] = supply_LTC
inter_results_df['supply_NTC'] = supply_NTC
inter_results_df['supply_NTC_FR'] = supply_NTC_FR
inter_results_df['supply_NTC_DE'] = supply_NTC_DE
inter_results_df['supply_NTC_IT'] = supply_NTC_IT
inter_results_df['elastic_demand'] = elastic_demand
inter_results_df['demand_hydrop'] = demand_hydrop
inter_results_df['demand_NTC'] = demand_NTC
inter_results_df['demand_NTC_FR'] = demand_NTC_FR
inter_results_df['demand_NTC_DE'] = demand_NTC_DE
inter_results_df['demand_NTC_IT'] = demand_NTC_IT

inter_results_df_head = inter_results_df.columns # getting the column names

# aggregating all columns
results_agg = []
for j in range(len(inter_results_df_head)):
    results_agg.append([])
    monthly = []
    name = inter_results_df_head[j]
    monthly_len = int((len(inter_results_df[name])-1)/730)
    print(inter_results_df_head[j])
    for i in range(monthly_len):
        monthly_calc = 0
        for p in range(730): # number of hours in a month
            monthly_calc += inter_results_df[name][i*730 + p]
        monthly.append(monthly_calc/730)
    results_agg[j] = monthly

# making a new panda
results_df = pd.DataFrame(results_agg, inter_results_df_head) # recreating the panda 
results_df = results_df.T # transposing the panda

# saving the new panda
results_df.to_csv('test_results_monthly.csv')