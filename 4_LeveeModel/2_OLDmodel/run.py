"""
This is file 0. This file control the entire model including the two main parts: the policy emergence model and the technical model whatever it might be.

Some additional notes and remarks on the model below:
- For the moment, the possibilities to run a multitude of experimentation has been removed from the model.
- It is advised to keep to the backbone+ or the ACF models, the 3S approach is not mature and requires additional work.


NOTE:
- CHANGE THIS! text is added to the part that still need to be changed.
- NOTICE! text is added when a part will need to be changed but not for March 28th proof of concept

WHAT STILL NEEDS TO BE DONE:
- The introduction of ERC does not currently work - this needs to be changed (lookup cannot be changed using PySD)
- [Optional] Completely functionalise the initialisation file

REMARKS:
- Check that the impact of the policy instruments act on the difference of states in the belief systems of the actors when they are graded and not on the overall state (which would make it pass the -1 and 1 limits in some cases.)
- Should a warm up period be introduced for the technical model considering that some of the levee stocks start at 1
- How do agents verify that their causal relations understanding are correct? There is no communications of these causal relations, they only change based on power ... no truth whatsoever.
"""

#####################################################################
# Import of the different modules required for the run of the model #
#####################################################################

#####################################################################
# General imports
import copy
import random
import pandas as pd

#####################################################################
# Policy emergence model imports
from model import PolicyEmergence
from mesa.batchrunner import BatchRunner
from initialisation import initial_values
import matplotlib.pyplot as plt
from datacollection import DataCollector
from agent import Policymakers, Electorate, Externalparties, Truth, Policyentres

#####################################################################
# Technical model imports
import pysd
import numpy as np
from states import states_calculation, states_definition
from policy_implementation import policy_package_implementation
from policy_initialisation import policy_package_initialisation



#####################################################################
####### Initialisations of the different parts of the models ########
#####################################################################

"""
This part of the model contains all the inputs require to initialise the model with external parameters. This is the out of model intialisation that does not require random changes for each run. The in model initialisation is placed in the model run function as it will lead to changes (usually random ones) needed for each run.
"""

#####################################################################
# General initialisation

# Pseudo random generator seed - for verification and validation purposes
# random.seed(42)

# For tailored runs:
min_run_number = 20
max_run_number = 25

# For the total number of steps in years
run_time_year = 20

# Number of repetitions required:
repetition = 5

#####################################################################
# Policy emergence model initialisation

# Input dictionnary containing all inputs related to the policy emergence model
inputs_dict_emergence = dict()

# ACF principle belief of interest
PC_ACF_interest = 0

# Method chosen:
# 0: Backbone, 1: Backbone+, 2: 3S, 3: ACF
# Note right now several parts of the model require that the same method be used for both
# parts of the model - this is mostly related to the input method. This will be changed
# in the future.
AS_theory = 3
PF_theory = AS_theory

# This is set up to use only in the case of exploration
exploration = False
if exploration == True:
	print('WARNING! There are no exploration inputs in this model currently.')

# Choosing the evernal event
# WARNING! At this point, policy emergence external events have been removed
event1 = False
event2 = False
event3 = False
event4 = False

# Reading the experiment input files
# WARNING! At this point, only the ACF is being used for the floods model with only one input file
experiment_input = pd.read_csv("Experiments_LHS_Floods.data",header=None)

# if exploration == True and AS_theory == 0:
# 	experiment_input = pd.read_csv("Exploration_LHS_Backbone.data",header=None)
# if exploration == True and AS_theory == 1:
# 	experiment_input = pd.read_csv("Exploration_LHS_Backbone+.data",header=None)
# if exploration == True and AS_theory == 2:
# 	experiment_input = pd.read_csv("Exploration_LHS_3S.data",header=None)
# if exploration == True and AS_theory == 3:
# 	experiment_input = pd.read_csv("Exploration_LHS_ACF.data",header=None)

run_number_total = len(experiment_input.index)
if exploration == True:
	ticks = 250
else:
	ticks = 500

# NOTICE! - This will need to be much more advanced, and preferably removed from the main step file where it currently resides
events = [0, event1, event2, event3, event4]


# Decision on the number of agents considered
policymaker_number = 6
externalparties_number = 6
agent_inputs = [policymaker_number, externalparties_number]

# Selecting the time step for the policy emergence model (time step interval in years)
time_step_emergence = 1

# initialisation of the dictionnary containing the states for the policy emergence model
emergence_states = dict()

#####################################################################
# Technical model initialisation

# Selecting the time step for the system dynamics model (time step interval in years)
time_step_SD = 0.0078125

inputs_dict_emergence = policy_package_initialisation(inputs_dict_emergence)

states_technical = dict()

technical_param_values = []

# Number of technical model external events considered - Notice, two Vensim files are created for this to avoid having to change the external event from python)
TM_Event = 2


#####################################################################
##################### Running the model #############################
#####################################################################

"""
This is the part of the script that is used to run the model. It contains the running of the model through the different steps but also the collection of the data for the policy emergence model.

Warning:
For the time being, the experimentation part is being removed, only one experiment can be run at a time.
"""

# Setting the number of times the model will need to run

# This sets the repetition considered
for repetition_number in range(repetition):

	# This sets the run considered from the input file
	for run_number in range(run_number_total):

		# This sets which external event for the technical model should be considered
		for tm_event_i in range(TM_Event):

			# This line is used to run different parts of the model on different computers/cores
			if run_number >= min_run_number and run_number < max_run_number:

				print('\n----------------------------------------------------')
				print('----------------------- RUN ' + str(run_number) + ' ---------------------')
				print('----------------------------------------------------\n')

				#####################################################################
				# IN-MODEL INITIALISATION - Policy emergence model

				# Running the function to fill the input dictionary
				initial_values(inputs_dict_emergence, experiment_input, run_number, agent_inputs, AS_theory, PF_theory)

				# Creation of the agent lists required for the policy emergence model
				agent_action_list = []
				for agents in inputs_dict_emergence["Agents"]:
					if type(agents) == Policymakers or type(agents) == Policyentres or type(agents) == Externalparties:
						agent_action_list.append(agents)

				# Assigning the run number of the action agents and the simulation for the policy emergence model
				for agents in agent_action_list:
					agents.run_number = run_number
				inputs_dict_emergence["Run_number"] = run_number

				# Selecting the data that needs to be collected for the policy emergence model
				if AS_theory == 0 or PF_theory == 0:
					datacollector = DataCollector(
						# Model
						{"Run_number": lambda m: m.run_number,
						"Agenda_issue": lambda m: m.agenda_as_issue,
						"Chosen_instrument": lambda m: m.agenda_instrument,
						"Belieftruth_tree": lambda m: m.belieftree_truth
						},
						# Electorate
						{"Run_number": lambda a: a.run_number,
						"Belieftree": lambda a: a.belieftree_electorate,
						"Affiliation" : lambda a: a.affiliation
						},
						# Agents
						{"Run_number": lambda a: a.run_number,
						"Type": lambda a: type(a),
						"Belieftree": lambda a: a.belieftree[0],
						"Affiliation" : lambda a: a.affiliation
						})

				if AS_theory == 1 or PF_theory == 1:
					datacollector = DataCollector(
						# Model
						{"Run_number": lambda m: m.run_number,
						"Agenda_issue": lambda m: m.agenda_as_issue,
						"Chosen_instrument": lambda m: m.agenda_instrument,
						"Belieftruth_tree": lambda m: m.belieftree_truth
						},
						# Electorate
						{"Run_number": lambda a: a.run_number,
						"Belieftree": lambda a: a.belieftree_electorate,
						"Affiliation" : lambda a: a.affiliation
						},
						# Agents
						{"Run_number": lambda a: a.run_number,
						"Type": lambda a: type(a),
						"Belieftree": lambda a: a.belieftree[0],
						"Affiliation" : lambda a: a.affiliation
						},
						#  Links
						{"Agent1": lambda l:l.agent1,
						"Agent2": lambda l:l.agent2,
						"Agent3": lambda l: l.aware
						})

				if AS_theory == 2 or PF_theory == 2:
					datacollector = DataCollector(
						# Model
						{"Run_number": lambda m: m.run_number,
						"Agenda_issue": lambda m: m.agenda_as_issue,
						"Chosen_instrument": lambda m: m.agenda_instrument,
						"Belieftruth_tree": lambda m: m.truthagent.belieftree_truth,
						"Agenda_prob_3S": lambda m: m.agenda_prob_3S_as,
						"Agenda_poli_3S": lambda m: m.agenda_poli_3S_as,
						"Instruments": lambda m: m.instruments,
						"Policies": lambda m: m.policies
						},
						# Electorate
						{"Run_number": lambda a: a.run_number,
						"Belieftree": lambda a: a.belieftree_electorate,
						"Affiliation" : lambda a: a.affiliation
						},
						# Agents
						{"Run_number": lambda a: a.run_number,
						"Type": lambda a: type(a),
						"Belieftree": lambda a: a.belieftree[0],
						"Belieftree_policy": lambda a: a.belieftree_policy[0],
						"Belieftree_instrument": lambda a: a.belieftree_instrument[0],
						"Affiliation" : lambda a: a.affiliation
						},
						#  Links
						{"Agent1": lambda l:l.agent1,
						"Agent2": lambda l:l.agent2,
						"Agent3": lambda l: l.aware,
						},
						# Teams AS
						{"Lead": lambda c: c.lead.unique_id,
						"Issue": lambda c: c.issue,
						"Issue_type": lambda c:c.issue_type,
						"Creation": lambda c: c.creation,
						"Members": lambda c: c.members_id,
						"Resources" : lambda c: c.resources[0]},
						# Teams PF
						{"Lead": lambda c: c.lead.unique_id,
						"Issue": lambda c: c.issue,
						"Issue_type": lambda c:c.issue_type,
						"Creation": lambda c: c.creation,
						"Members": lambda c: c.members_id,
						"Resources" : lambda c: c.resources[0]})

				if AS_theory == 3 or PF_theory == 3:
					datacollector = DataCollector(
						# Model
						{"Run_number": lambda m: m.run_number,
						"Agenda_issue": lambda m: m.agenda_as_issue,
						"Chosen_instrument": lambda m: m.agenda_instrument,
						"Belieftruth_tree": lambda m: m.truthagent.belieftree_truth
						},
						# Electorate
						{"Run_number": lambda a: a.run_number,
						"Belieftree": lambda a: a.belieftree_electorate,
						"Affiliation" : lambda a: a.affiliation
						},
						# Agents
						{"Run_number": lambda a: a.run_number,
						"Type": lambda a: type(a),
						"Belieftree": lambda a: a.belieftree[0],
						"Affiliation" : lambda a: a.affiliation
						},
						#  Links
						{"Agent1": lambda l:l.agent1,
						"Agent2": lambda l:l.agent2,
						"Agent3": lambda l: l.aware,
						},
						# Teams AS
						{},
						# Teams PF
						{},
						# Coalitions AS
						{"Lead": lambda c: c.lead.unique_id,
						"Issue": lambda c: c.issue,
						"Creation": lambda c: c.creation,
						"Members": lambda c: c.members_id,
						"Resources" : lambda c: c.resources[0]},
						# Coalitions PF
						{"Lead": lambda c: c.lead.unique_id,
						"Issue": lambda c: c.issue,
						"Creation": lambda c: c.creation,
						"Members": lambda c: c.members_id,
						"Resources" : lambda c: c.resources[0]
						})

				# This initialise the policy emergence model (runs the __init__ part of the PolicyEmergence file)
				model_emergence = PolicyEmergence(PC_ACF_interest, datacollector, run_number, inputs_dict_emergence, events)

				print('Cleared initialisation of the policy emergence model.')
				print('   ')

				#####################################################################
				# IN-MODEL INITIALISATION - Technical model

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
				# CHANGE THIS! This needs to affect the values in the graph only - ERC changes is currently deactivated in the rest of the code
				ERC_value = 0
				RT_value = 3.5
				AdT_value = 30
				PH_value = 55
				RS_value = 0.2
				CT_value = 5

				# This initialises the technical model and transforms it from vensim to python. (Vary the model depending on the external event being considered)
				if tm_event_i == 0:
					model_technical = pysd.read_vensim('Flood_Levees_14_Final.mdl')
				if tm_event_i == 1:
					model_technical = pysd.read_vensim('Flood_Levees_14_Final_2.mdl')

				print('Cleared initialisation of the technical model.')
				print('   ')
			
				#####################################################################
				# RUNNING THE MODEL

				print('STEP 1 -------------')
				print('   ')

				# Running the technical model first (for one year time step only
				print('TECHNICAL MODEL RUN ---')
				print('   ')
				# CHANGE THIS! - The function that has been commented out is the one with the ERC in it
				# model_technical_output = model_technical.run(params={'FINAL TIME':time_step_emergence, 'aging time':AT_value, 'obsolescence time':OT_value, 'design time':DT_value, 'flood perception time':FPT_value, 'effect on renovation and construction':ERC_value, 'renovation time':RT_value, 'adjustment time':AdT_value, 'planning horizon':PH_value, 'renovation standard':RS_value, 'construction time':CT_value})
				model_technical_output = model_technical.run(params={'FINAL TIME':time_step_emergence, 'aging time':AT_value, 'obsolescence time':OT_value, 'design time':DT_value, 'flood perception time':FPT_value, 'renovation time':RT_value, 'adjustment time':AdT_value, 'planning horizon':PH_value, 'renovation standard':RS_value, 'construction time':CT_value})

				# For loop for the running of the model (-1 as an initial step has already been run)
				for n in range(run_time_year - 1):

					print('STEP ', n+2, ' -------------')
					print('   ')

					# Obtention of the states values from the technical model outputs
					states_technical = states_definition(model_technical, states_technical)

					# Calculation of the states for the policy emergence model
					states_emergence = states_calculation(states_technical, emergence_states)

					# This performs one step of the policy emergence model
					print('   ')
					print('POLICY EMERGENCE MODEL RUN ---')
					print('   ')
					policy_selected = model_emergence.step(AS_theory, PF_theory, states_emergence)

					# This performs the implementation of the policy instruments on the exogenous parameters from the technical model
					if policy_selected != None:
						AT_value, OT_value, DT_value, FPT_value, ERC_value, RT_value, AdT_value, PH_value, RS_value, CT_value = policy_package_implementation(policy_selected, AT_value, OT_value, DT_value, FPT_value, ERC_value, RT_value, AdT_value, PH_value, RS_value, CT_value)

					# This performs 1 years worth of steps for the system dynamics model
					print('   ')
					print('TECHNICAL MODEL RUN ---')
					print('   ')
					# CHANGE THIS - The function that has been commented out is the one with the ERC in it
					# model_technical_output_intermediate = model_technical.run(params={'aging time':AT_value, 'obsolescence time':OT_value, 'design time':DT_value, 'flood perception time':FPT_value, 'effect on renovation and construction':ERC_value, 'renovation time':RT_value, 'adjustment time':AdT_value, 'planning horizon':PH_value, 'renovation standard':RS_value, 'construction time':CT_value}, initial_condition='current', return_timestamps=np.linspace(1+n,1+n+1, 1/0.0078125))
					model_technical_output_intermediate = model_technical.run(params={'aging time':AT_value, 'obsolescence time':OT_value, 'design time':DT_value, 'flood perception time':FPT_value, 'renovation time':RT_value, 'adjustment time':AdT_value, 'planning horizon':PH_value, 'renovation standard':RS_value, 'construction time':CT_value}, initial_condition='current', return_timestamps=np.linspace(1+n,1+n+1, 1/0.0078125))
					model_technical_output = model_technical_output.append(model_technical_output_intermediate)

				model_technical_output.plot()
				# plt.show()

				#####################################################################
				# STORING THE DATA - Technical model
				print('WRITING Technical model to file ----')
				# For the backbone
				if AS_theory == 0:
					model_technical_output.to_csv('1_TM_B_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
				# For the backbone+
				if AS_theory == 1:
					model_technical_output.to_csv('1_TM_B+_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
				# For the 3S
				if AS_theory == 2:
					model_technical_output.to_csv('1_TM_3S_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
				# For the ACF
				if AS_theory == 3:
					model_technical_output.to_csv('1_TM_ACF_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')

				#####################################################################
				# STORING THE DATA - Policy emergence model
				print('WRITING Policy emergence model to file ----')
				# For the backbone
				if AS_theory == 0:
					df_model = model_emergence.datacollector.get_model_vars_dataframe()
					df_model.to_csv('1_model_B_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
					df_electorate = model_emergence.datacollector.get_electorate_vars_dataframe()
					df_electorate.to_csv('1_electorate_B_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
					df_agents = model_emergence.datacollector.get_agent_vars_dataframe()
					df_agents.to_csv('1_agents_B_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
				# For the backbone+
				if AS_theory == 1:
					df_model = model_emergence.datacollector.get_model_vars_dataframe()
					df_model.to_csv('1_model_B+_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
					df_electorate = model_emergence.datacollector.get_electorate_vars_dataframe()
					df_electorate.to_csv('1_electorate_B+_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
					df_agents = model_emergence.datacollector.get_agent_vars_dataframe()
					df_agents.to_csv('1_agents_B+_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
					df_links = model_emergence.datacollector.get_links_vars_dataframe()
					df_links.to_csv('1_links_B+_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
				# For the 3S
				if AS_theory == 2:
					# frames_model.append(model_emergence.datacollector.get_model_vars_dataframe())
					df_model = model_emergence.datacollector.get_model_vars_dataframe()
					df_model.to_csv('1_model_3S_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
					df_electorate = model_emergence.datacollector.get_electorate_vars_dataframe()
					df_electorate.to_csv('1_electorate_3S_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
					# frames_agents.append(model_emergence.datacollector.get_agent_vars_dataframe())
					df_agents = model_emergence.datacollector.get_agent_vars_dataframe()
					df_agents.to_csv('1_agents_3S_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
					# frames_teams_as.append(model_emergence.datacollector.get_team_as_vars_dataframe())
					df_team_as = model_emergence.datacollector.get_team_as_vars_dataframe()
					df_team_as.to_csv('1_teams_as_3S_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
					# frames_teams_pf.append(model_emergence.datacollector.get_team_pf_vars_dataframe())
					df_team_pf = model_emergence.datacollector.get_team_pf_vars_dataframe()
					df_team_pf.to_csv('1_teams_pf_3S_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
					df_links = model_emergence.datacollector.get_links_vars_dataframe()
					df_links.to_csv('1_links_3S_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
				# For the ACF
				if AS_theory == 3 or PF_theory == 3:
					# frames_model.append(model_emergence.datacollector.get_model_vars_dataframe())
					df_model = model_emergence.datacollector.get_model_vars_dataframe()
					df_model.to_csv('1_model_ACF_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
					df_electorate = model_emergence.datacollector.get_electorate_vars_dataframe()
					df_electorate.to_csv('1_electorate_ACF_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
					# frames_agents.append(model_emergence.datacollector.get_agent_vars_dataframe())
					df_agents = model_emergence.datacollector.get_agent_vars_dataframe()
					df_agents.to_csv('1_agents_ACF_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
					# frames_coalitions_as.append(model_emergence.datacollector.get_coalition_as_vars_dataframe())
					df_coalition_as = model_emergence.datacollector.get_coalition_as_vars_dataframe()
					df_coalition_as.to_csv('1_coalitions_as_ACF_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
					df_coalition_pf = model_emergence.datacollector.get_coalition_pf_vars_dataframe()
					df_coalition_pf.to_csv('1_coalitions_pf_ACF_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
					df_links = model_emergence.datacollector.get_links_vars_dataframe()
					df_links.to_csv('1_links_ACF_' + str(repetition_number) + '_' + str(run_number) + '_TMEvent_' + str(tm_event_i) + '.csv')
