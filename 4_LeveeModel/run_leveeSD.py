import pysd
import numpy as np
import matplotlib.pyplot as plt
from model_leveeSD_policies import exo_value_def
from model_leveeSD_states import saving_stocks

#####################################################################
# Technical model initialisation

time_step_SD = 0.0078125 # SD time step
run_time_year = 20 # total length of the simulation
interval_tick = 1 # interval of the simulation
exo_values = dict() # initialisation of the dict

# loading the SD model
model_levee = pysd.read_vensim('Flood_Levees_14_Final_pulse.mdl')

#####################################################################
# RUNNING THE MODEL

# running the first step
exo_values = exo_value_def(exo_values) # getting the values
model_levee_output = model_levee.run(params={'FINAL TIME':interval_tick,
											 'aging time':exo_values['AT_value'],
											 'obsolescence time':exo_values['OT_value'],
											 'design time':exo_values['DT_value'],
											 'flood perception time':exo_values['FPT_value'],
											 'renovation time':exo_values['RT_value'],
											 'adjustment time':exo_values['AdT_value'],
											 'planning horizon':exo_values['PH_value'],
											 'renovation standard':exo_values['RS_value'],
											 'construction time':exo_values['CT_value']})

stocks = saving_stocks(model_levee)

# model_levee_output_intermediate = \
# 		model_levee.run(params={'aging time':exo_values['AT_value'],
# 								'obsolescence time':exo_values['OT_value'],
# 								'design time':exo_values['DT_value'],
# 								'flood perception time':exo_values['FPT_value'],
# 								'renovation time':exo_values['RT_value'],
# 								'adjustment time':exo_values['AdT_value'],
# 								'planning horizon':exo_values['PH_value'],
# 								'renovation standard':exo_values['RS_value'],
# 								'construction time':exo_values['CT_value']},
# 						initial_condition=(1,
# 										  {'Designed Levees':stocks['DL'],
# 										   'Standard Levees':stocks['SL'],
# 										   'Old Levees':stocks['OL'],
# 										   'Current Safety Standard':stocks['CSS'],
# 										   'Safety SL':stocks['SSL'],
# 										   'Safety OL':stocks['SOL'],
# 										   'Anticipated Flood Level':stocks['AFL'],
# 										   'perceived current safety':stocks['PCS']}),
# 						return_timestamps=np.linspace(interval_tick,
# 													  interval_tick + interval_tick,
# 													  1//time_step_SD))

# model_levee_output = model_levee_output.append(model_levee_output_intermediate) # saving the data

for n in range(run_time_year):
	# todo - ERC not implemented as it is a lookup at the moment
	model_levee_output_intermediate = \
		model_levee.run(params={'aging time':exo_values['AT_value'],
								'obsolescence time':exo_values['OT_value'],
								'design time':exo_values['DT_value'],
								'flood perception time':exo_values['FPT_value'],
								'renovation time':exo_values['RT_value'],
								'adjustment time':exo_values['AdT_value'],
								'planning horizon':exo_values['PH_value'],
								'renovation standard':exo_values['RS_value'],
								'construction time':exo_values['CT_value']},
						initial_condition='current',
						return_timestamps=np.linspace(interval_tick + n,
													  interval_tick + n + interval_tick,
													  1//time_step_SD))

	model_levee_output = model_levee_output.append(model_levee_output_intermediate) # saving the data



model_levee_output.to_csv('O_L1_alone_Sce1.csv') # saving the results

model_levee_output.plot()
plt.show()


