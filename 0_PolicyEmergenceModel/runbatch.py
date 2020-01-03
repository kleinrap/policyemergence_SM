# imports for the policy emergence model
from model_PE import PolicyEmergenceSM
from model_PE_policyImpact import policy_impact_evaluation
from model_PE_agents_initialisation import issuetree_creation, policytree_creation

# imports for the policy context model
from model_policyContext import PolicyContext

# import other packages
import pandas as pd

# batch run parameters
repetitions_runs = 50
exp_number = 2

# running parameters
total_ticks = 155
interval_tick = 5
run_tick = int(total_ticks/interval_tick)
warmup_tick = interval_tick

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
w_el_influence = 0 # electorate influence parameter

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

# putting all of the profiles into two list for the different experiments (one for initial goals and one for the goals after the mid-change)
goal_profiles = [goal_profiles_Ex1Be, goal_profiles]
goal_profiles_after = [goal_profiles_Ex1Af, goal_profiles_Ex1Af]


# running a number of experiments
''' changes in the beliefs of the agents '''
for exp_i in range(exp_number):

	# creating the agents for the policy emergence model
	SM_inputs = [SM_PMs, SM_PMs_aff, SM_PEs, SM_PEs_aff, SM_EPs, SM_EPs_aff, resources_aff, representativeness, goal_profiles[exp_i], w_el_influence]

	# running a number of repetitions per experiment
	for rep_runs in range(repetitions_runs):

		# for model run tailoring
		if exp_i >= 0 and rep_runs >= 0:

			# initialisation of the policy context model
			model_run_policyContext = PolicyContext(policy_context_inputs_here)

			# initialisation of the policy emergence model
			model_run_SM = PolicyEmergenceSM(SM_inputs, 10, 10)

			print("\n")
			print("************************")
			print("Start of the simulation:", "\n")
			for i in range(run_tick):

				print(" ")
				print("************************")
				print("Tick number: ", i, ', experiment:', exp_i, ', run number:', rep_runs)

				# warm up time
				# this is also used as a warmup time
				if i == 0:
					policy_chosen = [None for ite in range(len(model_run_SM.policy_instruments[0]))]
					for warmup_time in range(warmup_tick):
						KPIs = model_run_policyContext.step(policy_chosen)

				# policy impact evaluation
				policy_impact_evaluation(model_run_SM, model_run_policyContext, KPIs, interval_tick)

				# running the policy emergence model
				policy_chosen = model_run_SM.step(KPIs)

				# run of the policy context model for interval_tick ticks
				for p in range(interval_tick):
					KPIs = model_run_policyContext.step(policy_chosen)
					policy_chosen = [None for ite in range(len(model_run_SM.policy_instruments[0]))] # reset policy after it has been implemented once

				'''
				Scenario Changes
				In this part of the code, changes can be introduced through scenarios for both the policy context and the policy emergence models
				'''
				# redefining the issue tree basics - hardcoded values for simplicity
				issuetree_virgin = issuetree_creation(model_run_SM, model_run_SM.len_DC, model_run_SM.len_PC, model_run_SM.len_S, model_run_SM.len_CR)
				policytree_virgin = policytree_creation(model_run_SM, model_run_SM.len_PC, model_run_SM.len_S, model_run_SM.len_PC, model_run_SM.len_ins)

				if i == 15:
					pass

				# # checker code
				# for agent in model_run_SM.schedule.agent_buffer(shuffled=False):
				# 	if isinstance(agent, ActiveAgent):
				# 		print(' ')
				# 		print(agent.agent_type, '\n', 'ID', agent.unique_id, 'Aff', agent.affiliation, agent.issuetree[agent.unique_id], '\n', agent.policytree[agent.unique_id])


			# output of the data
			# policy context model
			output_policyContext_model = model_run_policyContext.datacollector.get_model_vars_dataframe()
			output_policyContext_model.to_csv('O_context_model_' + str(exp_i) + '_Run' + str(rep_runs) + '.csv')

			# policy emergence model
			output_SM_model = model_run_SM.datacollector.get_model_vars_dataframe()
			output_SM_model.to_csv('O_PE_model_' + str(exp_i) +  '_Run' + str(rep_runs) + '.csv')
			output_SM_agents = model_run_SM.datacollector.get_agent_vars_dataframe()
			output_SM_agents.to_csv('O_PE_agents_' + str(exp_i) + '_Run' + str(rep_runs) + '.csv')