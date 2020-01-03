# imports for the policy emergence model
from model_PE import PolicyEmergenceSM
from model_PE_policyImpact import policy_impact_evaluation
from model_PE_agents import ElectorateAgent

# imports for the policy context model
from model_predation import WolfSheepPredation

# import other packages
import pandas as pd

# todo - for same inputs, netlogo and mesa do not put out the same results - mesa community emailed

# batch run parameters
repetitions_runs = 50
sce_number = 6

# running parameters
total_ticks = 1600
interval_tick = 100
run_tick = int(total_ticks/interval_tick)
warmup_tick = interval_tick

# parameters of the policy context model
'''
Here go all the parameters that are needed to initialise the policy context model
'''

# parameters of the policy emergence model
'''for all scenarios'''
resources_aff = [75, 75]  # resources per affiliation agent out of 100
representativeness = [25, 75]  # electorate representativeness per affiliation
w_el_influence = [0, 0, 0, 0, 0, 0.02]  # list - [-] - electorate influence weight constant

'''actor distribution'''
PE_PMs = 3  # number of policy makers
PE_PMs_aff = [2, 1]  # policy maker distribution per affiliation
PE_PEs = 4  # number of policy entrepreneurs
PE_PEs_aff = [2, 2]  # policy entrepreneur distribution per affiliation
PE_EPs = 0  # number of external parties
PE_EPs_aff = [0, 0]  # external parties distribution per affiliation

# input profile for preferred states
'''
This can be used for different scenarios for the preferred states (goals) of the policy emergence agents
'''
input_goalProfiles_file_Ex0Be = 'input_goalProfiles_Ex0Be'
input_goalProfiles_file_Ex1Be = 'input_goalProfiles_Ex1Be'
input_goalProfiles_file_Ex2Be = 'input_goalProfiles_Ex2Be'
input_goalProfiles_file_Ex3Be = 'input_goalProfiles_Ex3Be'
input_goalProfiles_file_Ex4Be = 'input_goalProfiles_Ex4Be'
input_goalProfiles_file_Ex5Be = 'input_goalProfiles_Ex5Be'
goal_input_Ex0Be = pd.read_csv(input_goalProfiles_file_Ex0Be, sep=',')
goal_input_Ex1Be = pd.read_csv(input_goalProfiles_file_Ex1Be, sep=',')
goal_input_Ex2Be = pd.read_csv(input_goalProfiles_file_Ex2Be, sep=',')
goal_input_Ex3Be = pd.read_csv(input_goalProfiles_file_Ex3Be, sep=',')
goal_input_Ex4Be = pd.read_csv(input_goalProfiles_file_Ex4Be, sep=',')
goal_input_Ex5Be = pd.read_csv(input_goalProfiles_file_Ex5Be, sep=',')
goal_profiles_Ex0Be = []
goal_profiles_Ex1Be = []
goal_profiles_Ex2Be = []
goal_profiles_Ex3Be = []
goal_profiles_Ex4Be = []
goal_profiles_Ex5Be = []
for i in range(len(resources_aff)*2):
	goal_profiles_Ex0Be.append(goal_input_Ex0Be.iloc[i].tolist())  # goal profiles for active agents and electorate
	goal_profiles_Ex1Be.append(goal_input_Ex1Be.iloc[i].tolist())  # goal profiles for active agents and electorate
	goal_profiles_Ex2Be.append(goal_input_Ex2Be.iloc[i].tolist())  # goal profiles for active agents and electorate
	goal_profiles_Ex3Be.append(goal_input_Ex3Be.iloc[i].tolist())  # goal profiles for active agents and electorate
	goal_profiles_Ex4Be.append(goal_input_Ex4Be.iloc[i].tolist())  # goal profiles for active agents and electorate
	goal_profiles_Ex5Be.append(goal_input_Ex5Be.iloc[i].tolist())  # goal profiles for active agents and electorate

# first goal input profile (after change)
input_goalProfiles_file_Ex0Af = 'input_goalProfiles_Ex0Af'
input_goalProfiles_file_Ex3Af = 'input_goalProfiles_Ex3Af'
goal_input_Ex0Af = pd.read_csv(input_goalProfiles_file_Ex0Af, sep=',')
goal_input_Ex3Af = pd.read_csv(input_goalProfiles_file_Ex3Af, sep=',')
goal_profiles_Ex0Af = []
goal_profiles_Ex3Af = []
for i in range(len(resources_aff)*2):
	goal_profiles_Ex0Af.append(goal_input_Ex0Af.iloc[i].tolist())  # goal profiles for active agents and electorate
	goal_profiles_Ex3Af.append(goal_input_Ex3Af.iloc[i].tolist())  # goal profiles for active agents and electorate

# putting all of the profiles into two list for the different experiments (one for initial goals and one for the goals
# after the mid-change)
goal_profiles = [goal_profiles_Ex0Be, goal_profiles_Ex1Be, goal_profiles_Ex2Be, goal_profiles_Ex3Be, goal_profiles_Ex4Be,
				 goal_profiles_Ex5Be]
goal_profiles_after = [goal_profiles_Ex0Af, goal_profiles_Ex0Af, goal_profiles_Ex0Af, goal_profiles_Ex3Af,
					   goal_profiles_Ex0Af, goal_profiles_Ex0Af]


# running a number of scenarios
''' changes in the agent distribution '''
for sce_i in range (sce_number):

	# creating the agents for the policy emergence model
	PE_inputs = [PE_PMs, PE_PMs_aff, PE_PEs, PE_PEs_aff, PE_EPs, PE_EPs_aff, resources_aff, representativeness,
				 goal_profiles[sce_i], w_el_influence[sce_i]]


	# running a number of repetitions per experiment
	for rep_runs in range(repetitions_runs):

		# for model run tailoring
		if sce_i >= 0:

			# initialisation of the policy context model
			model_run_predation = WolfSheepPredation(50, 50, 100, 50, 0.04, 0.05, 30, True, 30, 4)

			# initialisation of the policy emergence model
			model_run_PE = PolicyEmergenceSM(PE_inputs, 10, 10)

			print("\n")
			print("************************")
			print("Start of the simulation:", "\n")
			for i in range(run_tick):

				print(" ")
				print("************************")
				print("Tick number: ", i, ', scenario:', sce_i, ', w_el', w_el_influence[sce_i], ', run number:', rep_runs)

				# warm up time
				# this is also used as a warmup time
				if i == 0:
					policy_chosen = [None for ite in range(len(model_run_PE.policy_instruments[0]))]
					for warmup_time in range(warmup_tick):
						KPIs = model_run_predation.step(policy_chosen)

				# policy impact evaluation
				policy_impact_evaluation(model_run_PE, model_run_predation, KPIs, interval_tick)

				# running the policy emergence model
				policy_chosen = model_run_PE.step(KPIs)

				# run of the policy context model for interval_tick ticks
				for p in range(interval_tick):
					KPIs = model_run_predation.step(policy_chosen)
					policy_chosen = [None for ite in range(len(model_run_PE.policy_instruments[0]))]
										# reset policy after it has been implemented once

				'''
				Scenario Changes
				In this part of the code, changes can be introduced through scenarios for both the policy context and
				the policy emergence models
				'''

				# # scenario 3 - electorate preferred state change
				# if i == 8 and sce_i == 3:
				# 	# changing the electorate preferred states values based on the scenarios input
				# 	aff_number = len(resources_aff)
				# 	for elec in model_run_PE.schedule.agent_buffer(shuffled=True):
				# 		if isinstance(elec, ElectorateAgent):
				# 			for issue in range(model_run_PE.len_DC + model_run_PE.len_PC + model_run_PE.len_S):
				# 				if elec.affiliation == 0:
				# 					elec.issuetree_elec[issue] = goal_profiles_after[sce_i][aff_number + 0][1 + issue]
				# 				if elec.affiliation == 1:
				# 					elec.issuetree_elec[issue] = goal_profiles_after[sce_i][aff_number + 1][1 + issue]

			# # checker code
				# for agent in model_run_PE.schedule.agent_buffer(shuffled=False):
				# 	if isinstance(agent, ActiveAgent):
				# 		print(' ')
				# 		print(agent.agent_type, '\n', 'ID', agent.unique_id, 'Aff', agent.affiliation,
			# 		agent.issuetree[agent.unique_id], '\n',
				# 		agent.policytree[agent.unique_id])


			# output of the data
			# policy context model
			output_policyContext_model = model_run_predation.datacollector.get_model_vars_dataframe()
			output_policyContext_model.to_csv('O_Pre_model_Sce' + str(sce_i) + '_Run' + str(rep_runs)
											  + '_el'  + str(w_el_influence[sce_i]) +'.csv')

			# policy emergence model
			output_PE_model = model_run_PE.datacollector.get_model_vars_dataframe()
			output_PE_model.to_csv('O_PE_model_Sce' + str(sce_i) + '_Run' + str(rep_runs)
								   + '_el' + str(w_el_influence[sce_i]) + '.csv')
			output_PE_agents = model_run_PE.datacollector.get_agent_vars_dataframe()
			output_PE_agents.to_csv('O_PE_agents_Sce' + str(sce_i) + '_Run' + str(rep_runs)
									+ '_el' + str(w_el_influence[sce_i]) + '.csv')