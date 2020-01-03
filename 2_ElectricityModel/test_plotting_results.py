'''
This file is used to plot the results mostly for verification and validation purposes at this point
'''

import pandas as pd
import matplotlib.pyplot as plt

data_read = pd.read_csv('test_results_monthly.csv', sep=',')

ticks = []
for i in range(len(data_read['demand'])):
    ticks.append(i)

plt.figure()
plt.title('Price')
plt.plot(ticks, data_read['electricity price'])
plt.xlim([0, 204])
plt.ylim([0, 100])

plt.figure()
plt.plot(ticks, data_read['demand'], label='Demand')
plt.plot(ticks, data_read['supply_hydro'], label='Hydro')

plt.plot(ticks, data_read['supply_hydrop'], label = 'Hydrop')
plt.plot(ticks, data_read['supply_solar'], label='Solar')
plt.plot(ticks, data_read['supply_wind'], label='Wind')
plt.plot(ticks, data_read['supply_LTC'], label='LTC')
plt.plot(ticks, data_read['supply_NTC'], label='NTC')
plt.plot(ticks, data_read['supply_waste'], label='Waste')
plt.plot(ticks, data_read['supply_CCGT'], label='CCGT')
plt.plot(ticks, data_read['supply_runofriver'], label='ROR')
plt.plot(ticks, data_read['supply_nuclear'], label='Nuclear')
plt.legend()

plt.figure()
plt.title('Hydro and Hydrop reservoirs')
plt.plot(ticks, data_read['reservoir_level'])
plt.plot(ticks, data_read['reservoir_capacity_total_water'])

plt.figure()
plt.title('Waste reservoirs')
plt.plot(ticks, data_read['reservoir_level_waste'])

plt.figure()
plt.title('Investment techs')
plt.plot(ticks, data_read['demand'])
plt.plot(ticks, data_read['supply_solar'], label='Solar')
plt.plot(ticks, data_read['supply_wind'], label='Wind')
plt.plot(ticks, data_read['supply_CCGT'], label='CCGT')
plt.legend()
plt.xlim([0, 204])
plt.ylim([0, 21000])

plt.figure()
plt.title('Demands')
plt.plot(ticks, data_read['demand'], label = 'Demand')
plt.plot(ticks, data_read['elastic_demand'], label = 'Elastic demand')
plt.legend()
plt.xlim([0, 204])
plt.ylim([0, 21000])

plt.figure()
plt.plot(ticks, data_read['demand'], label='demand')
plt.plot(ticks, data_read['elastic_demand'], label='elastic demand')
plt.plot(ticks, data_read['demand_NTC'], label='NTC demand')
plt.plot(ticks, data_read['demand_NTC_FR'], label='NTC FR demand')
plt.plot(ticks, data_read['demand_NTC_IT'], label='NTC IT demand')
plt.plot(ticks, data_read['demand_NTC_DE'], label='NTC DE demand')
plt.xlim([0, 204])
plt.ylim([0, 21000])
plt.legend()

plt.figure()
plt.plot(ticks, data_read['demand'], label='demand')
plt.plot(ticks, data_read['supply_NTC'], label='NTC supply')
plt.plot(ticks, data_read['supply_NTC_FR'], label='NTC FR supply')
plt.plot(ticks, data_read['supply_NTC_IT'], label='NTC IT supply')
plt.plot(ticks, data_read['supply_NTC_DE'], label='NTC DE supply')
plt.xlim([0, 204])
plt.ylim([0, 10000])
plt.legend()


# plt.plot(ticks, data_read[''])

plt.show()