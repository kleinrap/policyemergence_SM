'''
This codes takes into account appropriately the floods and is computationally efficient.
It also assesses the policy impact appropriately.
'''

# imports for the policy emergence model
from model_PE import PolicyEmergenceSM
from model_PE_policyImpact3 import policy_impact_evaluation
from model_PE_agents_initialisation import issuetree_creation, policytree_creation

# imports for the policy context model
from model_leveeSD_policies import exo_value_def, policy_implementation
from model_leveeSD_states import states_calculation, saving_stocks

# import other packages
import pandas as pd
import pysd
import numpy as np
import matplotlib.pyplot as plt

# batch run parameters
repetitions_runs = 50
exp_number = 2 # relating to the beliefs
sce_number = 2 # relating to the floods

# running parameters
total_ticks = 21
interval_tick = 1
run_tick = int(total_ticks/interval_tick)
warmup_tick = interval_tick
policy_eval_tick = 5
time_step_SD = 0.0078125

# parameters of the policy context model
'''
Here go all the parameters that are needed to initialise the policy context model
'''

# parameters of the policy emergence model
SM_PMs = 3  # number of policy makers
SM_PMs_aff = [2, 1]  # policy maker distribution per affiliation
SM_PEs = 4  # number of policy entrepreneurs
SM_PEs_aff = [2, 2]  # policy entrepreneur distribution per affiliation
SM_EPs = 0  # number of external parties
SM_EPs_aff = [0, 0]  # external parties distribution per affiliation
resources_aff = [75, 75]  # resources per affiliation agent out of 100
representativeness = [25, 75]  # electorate representativeness per affiliation
w_el_influence = 0

# input profile for preferred states
'''
This can be used for different scenarios for the preferred states (goals) of the policy emergence agents
'''
input_goalProfiles_file_Ex1Be = 'input_goalProfiles_Ex1Be'
goal_input_Ex1Be = pd.read_csv(input_goalProfiles_file_Ex1Be, sep=',')
goal_profiles_Ex1Be = []
for i in range(len(resources_aff)*2):
	goal_profiles_Ex1Be.append(goal_input_Ex1Be.iloc[i].tolist())  # goal profiles for active agents and electorate
# first goal input profile (after change)
input_goalProfiles_file_Ex1Af = 'input_goalProfiles_Ex1Af'
goal_input_Ex1Af = pd.read_csv(input_goalProfiles_file_Ex1Af, sep=',')
goal_profiles_Ex1Af = []
for i in range(len(resources_aff)*2):
	goal_profiles_Ex1Af.append(goal_input_Ex1Af.iloc[i].tolist())  # goal profiles for active agents and electorate

# putting all of the profiles into two list for the different experiments (one for initial goals and one for the
# goals after the mid-change)
goal_profiles = [goal_profiles_Ex1Be, goal_profiles_Ex1Be]
goal_profiles_after = [goal_profiles_Ex1Af, goal_profiles_Ex1Af]

# running a number of experiments
''' changes in the beliefs of the agents '''
for exp_i in range(exp_number):

	for sce_i in range(sce_number):

		# creating the agents for the policy emergence model
		SM_inputs = [SM_PMs, SM_PMs_aff, SM_PEs, SM_PEs_aff, SM_EPs, SM_EPs_aff, resources_aff,
					 representativeness, goal_profiles[exp_i], w_el_influence]

		# running a number of repetitions per experiment
		for rep_runs in range(repetitions_runs):

			# for model run tailoring
			if sce_i == 1 and exp_i >= 1 and rep_runs <= 9:

				''' in case the .mdl file has been modified, re-read_vensim the files '''
				# pysd.read_vensim('Flood_Levees_14_Final.mdl')
				# pysd.read_vensim('Flood_Levees_14_Final_single.mdl')
				# pysd.read_vensim('Flood_Levees_14_Final_pulse.mdl')

				# initialisation of the policy context model
				exo_values = dict()  # exogenous value dictionnary SD model
				if sce_i == 0:
					model_levee = pysd.load('Flood_Levees_14_Final_single.py')
				if sce_i == 1:
					model_levee = pysd.load('Flood_Levees_14_Final_pulse.py')

				# initialisation of the policy emergence model
				model_run_SM = PolicyEmergenceSM(SM_inputs, 10, 10)

				print("\n")
				print("************************")
				print("Start of the simulation:", "\n")
				for i in range(run_tick):

					print(" ")
					print("************************")
					print("Tick number: ", i, ', scenario:', sce_i, ', experiment:', exp_i, ', run number:', rep_runs)

					# warm up time of the levee model
					if i == 0:
						exo_values = exo_value_def(exo_values)
						model_levee_output = \
							model_levee.run(params={'FINAL TIME':interval_tick, 'aging time':exo_values['AT_value'],
													'obsolescence time':exo_values['OT_value'],
													'design time':exo_values['DT_value'],
													'flood perception time':exo_values['FPT_value'],
													'renovation time':exo_values['RT_value'],
													'adjustment time':exo_values['AdT_value'],
													'planning horizon':exo_values['PH_value'],
													'renovation standard':exo_values['RS_value'],
													'construction time':exo_values['CT_value']})
						stocks = saving_stocks(model_levee)
						KPIs = states_calculation(model_levee) # mapping the states
						print(KPIs)

					# policy impact evaluation
					policy_impact_evaluation(model_run_SM, KPIs,policy_eval_tick, i + 1, time_step_SD, stocks, exo_values)

					# running the policy emergence model
					policy_chosen = model_run_SM.step(KPIs)

					'''
					IMPORTANT note relating to pySD
					because of an interference issue with the policy impact evaluation, the SD model has to be reloaded,
					and it has to be restarted at the previous point with all appropriate stocks values that were saved
					it seems that the pySD package overwrites in the backend on the same parameter despite the different
					model. That is it overwrites on the 'current' value. This meant that it would not show the flooding
					event that is introduced in the model.
					this issue should not be one - as discussed on git - this might require more checking at a later stage.
					'''
					exo_values = policy_implementation(policy_chosen, exo_values)  # implementing the policy

					if sce_i == 0:
						model_levee = pysd.load('Flood_Levees_14_Final_single.py')
					if sce_i == 1:
						model_levee = pysd.load('Flood_Levees_14_Final_pulse.py')

					# run of the policy context model for interval_tick ticks
					model_levee_output_inter = \
						model_levee.run(params={'aging time':exo_values['AT_value'],
												'obsolescence time':exo_values['OT_value'],
												'design time':exo_values['DT_value'],
												'flood perception time':exo_values['FPT_value'],
												'renovation time':exo_values['RT_value'],
												'adjustment time':exo_values['AdT_value'],
												'planning horizon':exo_values['PH_value'],
												'renovation standard':exo_values['RS_value'],
												'construction time':exo_values['CT_value']},
										initial_condition=(1 + i,
														  {'Designed Levees':stocks['DL'],
														   'Standard Levees':stocks['SL'],
														   'Old Levees':stocks['OL'],
														   'Current Safety Standard':stocks['CSS'],
														   'Safety SL':stocks['SSL'],
														   'Safety OL':stocks['SOL'],
														   'Anticipated Flood Level':stocks['AFL'],
														   'perceived current safety':stocks['PCS']}),
										return_timestamps=np.linspace(interval_tick + i,
																	  interval_tick + i + interval_tick,
																	  1 // time_step_SD))
					model_levee_output = model_levee_output.append(model_levee_output_inter)
					stocks = saving_stocks(model_levee)
					KPIs = states_calculation(model_levee) # mapping the states

					'''
					Scenario Changes
					In this part of the code, changes can be introduced through scenarios for both the policy context 
					and the policy emergence models
					'''
					# redefining the issue tree basics - hardcoded values for simplicity
					# issuetree_virgin = issuetree_creation(model_run_SM, model_run_SM.len_DC, model_run_SM.len_PC,
				# model_run_SM.len_S, model_run_SM.len_CR)
					# policytree_virgin = policytree_creation(model_run_SM, model_run_SM.len_PC, model_run_SM.len_S,
				# model_run_SM.len_PC, model_run_SM.len_ins)

					# if i == 15:
					# 	pass

					# # checker code
					# for agent in model_run_SM.schedule.agent_buffer(shuffled=False):
					# 	if isinstance(agent, ActiveAgent):
					# 		print(' ')
					# 		print(agent.agent_type, '\n', 'ID', agent.unique_id, 'Aff', agent.affiliation,
				# 		agent.issuetree[agent.unique_id], '\n', agent.policytree[agent.unique_id])

				# print(model_levee_output)
				# model_levee_output.plot()
				# plt.show()

				# model_levee_output.to_csv('O_L1_test_model_' + str(exp_i) + '_Run' + str(rep_runs) + '.csv')

				# output of the data
				# policy context model
				model_levee_output.to_csv('O_L1_model_Sce' + str(sce_i) + '_Exp' + str(exp_i)
										  + '_Run' + str(rep_runs) + '.csv')

				# policy emergence model
				output_SM_model = model_run_SM.datacollector.get_model_vars_dataframe()
				output_SM_model.to_csv('O_PE_model_Sce' + str(sce_i) + '_Exp' + str(exp_i)
									   + '_Run' + str(rep_runs) + '.csv')
				output_SM_agents = model_run_SM.datacollector.get_agent_vars_dataframe()
				output_SM_agents.to_csv('O_PE_agents_Sce' + str(sce_i) + '_Exp' + str(exp_i)
										+ '_Run' + str(rep_runs) + '.csv')