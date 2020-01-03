# General imports
import copy
import random
import pandas as pd


#####################################################################
# Technical model imports
import pysd
import numpy as np
import matplotlib.pyplot as plt
from model_leveeSD_states import states_calculation, states_definition
from model_leveeSD_policy_implementation import policy_package_implementation


#####################################################################
####### Initialisations of the different parts of the models ########
#####################################################################

"""
This part of the model contains all the inputs require to initialise the model with external parameters. This is the out of model intialisation that does not require random changes for each run. The in model initialisation is placed in the model run function as it will lead to changes (usually random ones) needed for each run.
"""

#####################################################################
# General initialisation

#####################################################################
# Policy emergence model initialisation

# Input dictionnary containing all inputs related to the policy emergence model
inputs_dict_emergence = dict()

repetition = 10

# Selecting the time step for the policy emergence model (time step interval in years)
time_step_emergence = 1/10

# initialisation of the dictionnary containing the states for the policy emergence model
emergence_states = dict()

#####################################################################
# Technical model initialisation

# Selecting the time step for the system dynamics model (time step interval in years)
time_step_SD = 0.0078125
run_time_year = 20
time_step_emergence = 1

#####################################################################
# IN-MODEL INITIALISATION - Technical model

states_technical = dict()
states_technical['AT_state'] = 0
states_technical['OT_state'] = 0
states_technical['DT_state'] = 0
states_technical['FPT_state'] = 0
states_technical['ERC_state'] = 0
states_technical['RT_state'] = 0
states_technical['AdT_state'] = 0
states_technical['PH_state'] = 0
states_technical['RS_state'] = 0
states_technical["SLS_state"] = 0
states_technical["OLS_state"] = 0
states_technical["SL_state"] = 0
states_technical["OL_state"] = 0
states_technical['IP_state'] = 0
states_technical['Sa_state'] = 0

# These are the initial values for the exogenous parameters that can be changed through the model policy instruments and packages
AT_value = 20
OT_value = 25
DT_value = 2.5
FPT_value = 0.5
# todo - CHANGE THIS! This needs to affect the values in the graph only - ERC changes is currently deactivated in the rest of the code
ERC_value = 0
RT_value = 3.5
AdT_value = 30
PH_value = 55
RS_value = 0.2
CT_value = 5


'''
Inputs: model_levee, exogenous parameters, time_step_emergence, n

1. run the model for one year
2. obtention of the data from the model (states_definition - change that name!)
3. convert the states to [0,1]

output: the states

'''

def model_levee_one_year():

	# This initialises the technical model and transforms it from vensim to python. (Vary the model depending on the external event being considered)

	model_levee = pysd.read_vensim('Flood_Levees_14_Final_2.mdl')

	print('Cleared initialisation of the technical model.')
	print('   ')

	#####################################################################
	# RUNNING THE MODEL

	print('MONTH 1 -------------')
	print('   ')

	# Running the technical model first (for one year time step only
	print('TECHNICAL MODEL RUN ---')
	print('   ')
	# CHANGE THIS! - The function that has been commented out is the one with the ERC in it
	# model_levee_output = model_levee.run(params={'FINAL TIME':time_step_emergence, 'aging time':AT_value, 'obsolescence time':OT_value, 'design time':DT_value, 'flood perception time':FPT_value, 'effect on renovation and construction':ERC_value, 'renovation time':RT_value, 'adjustment time':AdT_value, 'planning horizon':PH_value, 'renovation standard':RS_value, 'construction time':CT_value})
	model_levee_output = model_levee.run(params={'FINAL TIME':time_step_emergence, 'aging time':AT_value, 'obsolescence time':OT_value, 'design time':DT_value, 'flood perception time':FPT_value, 'renovation time':RT_value, 'adjustment time':AdT_value, 'planning horizon':PH_value, 'renovation standard':RS_value, 'construction time':CT_value})

	print(model_levee_output)

	# For loop for the running of the model (-1 as an initial step has already been run)
	for n in range(run_time_year - 1):
		# n is now in months in this approach

		print('MONTH ', n+2, ' -------------')
		print('   ')

		# Obtention of the states values from the technical model outputs
		states_technical = states_definition(model_levee, states_technical)

		# Calculation of the states for the policy emergence model
		states_emergence = states_calculation(states_technical, emergence_states)

		# This performs 1 years worth of steps for the system dynamics model
		print('   ')
		print('TECHNICAL MODEL RUN ---')
		print('   ')
		# CHANGE THIS - The function that has been commented out is the one with the ERC in it
		# model_levee_output_intermediate = model_levee.run(params={'aging time':AT_value, 'obsolescence time':OT_value, 'design time':DT_value, 'flood perception time':FPT_value, 'effect on renovation and construction':ERC_value, 'renovation time':RT_value, 'adjustment time':AdT_value, 'planning horizon':PH_value, 'renovation standard':RS_value, 'construction time':CT_value}, initial_condition='current', return_timestamps=np.linspace(1+n,1+n+1, 1/time_step_SD))
		print(0.09+n*0.1)
		print(np.linspace((1+n)*0.01,(1+n+1)*0.01, 10))
		print(len(np.linspace((1+n)*0.01,(1+n+1)*0.01, 10)))
		# model_levee_output_intermediate = model_levee.run(params={'FINAL TIME':0.099+n*0.1,'TIME STEP': 0.001, 'aging time':AT_value, 'obsolescence time':OT_value, 'design time':DT_value, 'flood perception time':FPT_value, 'renovation time':RT_value, 'adjustment time':AdT_value, 'planning horizon':PH_value, 'renovation standard':RS_value, 'construction time':CT_value}, initial_condition='current', return_timestamps=np.linspace((1+n)*0.01,(1+n+1)*0.01, 10))
		model_levee_output_intermediate = model_levee.run(params={'aging time':AT_value, 'obsolescence time':OT_value, 'design time':DT_value, 'flood perception time':FPT_value, 'renovation time':RT_value, 'adjustment time':AdT_value, 'planning horizon':PH_value, 'renovation standard':RS_value, 'construction time':CT_value}, initial_condition='current', return_timestamps=np.linspace(1+n,1+n+1, 1/0.0078125))

		print(model_levee_output_intermediate)

		# saving the results
		model_levee_output = model_levee_output.append(model_levee_output_intermediate)
