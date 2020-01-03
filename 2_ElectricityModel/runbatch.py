# imports for the policy emergence model
from model_PE import PolicyEmergenceSM
from model_PE_agents import ElectorateAgent
from model_PE_policyImpact import policy_impact_evaluation
from model_PE_agents_initialisation import issuetree_creation, policytree_creation

# imports for the policy context model
from model_elec import Electricity

# import other packages
import pandas as pd
import time

'''
The architecture present here is to be used for performing simulations

At the moment: 2 scenarios

- The scenarios introduce change in the model:
	\item Scenario 1: Undefined
	\item Scenario 2: Undefined
	
TO DO:
- Remove all instances of policy families
- Split the electorate influence as a separate scenarios 
'''

# Simulation run time (hybrid): 9120.056344270706

# batch run parameters
repetitions_runs = 50

# running parameters
total_ticks = 27
interval_tick = 3

evaluation_tick = interval_tick
run_tick = int(total_ticks/interval_tick)
warmup_tick = interval_tick

# parameters of the electricity model
# none here it seems

# parameters of the policy emergence model
'''for all scenarios'''
resources_aff = [75, 75]  # resources per affiliation agent out of 100
representativeness = [25, 75]  # electorate representativeness per affiliation
w_el_influence = [0.00, 0.05, 0.50]  # float - [-] - electorate influence weight constant

'''scenario actor distribution'''
SM_PMs = 3  # number of policy makers
SM_PMs_aff = [2, 1]  # policy maker distribution per affiliation
SM_PEs = 4  # number of policy entrepreneurs
SM_PEs_aff = [2, 2]  # policy entrepreneur distribution per affiliation
SM_EPs = 0  # number of external parties
SM_EPs_aff = [0, 0]  # external parties distribution per affiliation

# input profile for preferred states
'''
This can be used for different scenarios for the preferred states (goals) of the policy emergence agents
'''
input_goalProfiles_file = 'input_goalProfiles'

goal_input = pd.read_csv(input_goalProfiles_file, sep=',')

goal_profiles = []

for i in range(len(resources_aff) * 2):
	goal_profiles.append(goal_input.iloc[i].tolist())  # goal profiles for active agents and electorate

# demand growth profile
demand_growth = [0.00, 0.015, 0.03]

for demand_ite in range(len(demand_growth)):
	# running a number of scenarios
	''' changes in the agent distribution '''
	for w_el_i in range(len(w_el_influence)):

		# creating the agents for the policy emergence model
		PE_inputs = [SM_PMs, SM_PMs_aff, SM_PEs, SM_PEs_aff, SM_EPs, SM_EPs_aff, resources_aff, representativeness,
					 goal_profiles, w_el_influence[w_el_i]]

		# running a number of repetitions per scenario
		for rep_runs in range(repetitions_runs):

			# for model run tailoring
			if demand_ite >= 0 and w_el_i >= 0 and rep_runs == 0:

				start = time.time()

				# initialisation of the electricity model
				model_run_elec = Electricity(demand_growth[demand_ite], 10, 10)

				# initialisation of the policy emergence model
				model_run_PE = PolicyEmergenceSM(PE_inputs, 10, 10)

				print("\n")
				print("************************")
				print("Start of the simulation:", "\n")
				for i in range(run_tick):

					print(" ")
					print("************************")
					print("Tick number: ", i, ', w_el:', w_el_i, ', demand:', demand_growth[demand_ite],
						  '%, run number:', rep_runs)

					# warm up time
					# this is also used as a warmup time
					if i == 0:
						policy_chosen = [None for ite in range(len(model_run_PE.policy_instruments[0]))]
						for warmup_time in range(warmup_tick):
							KPIs = model_run_elec.step(policy_chosen)

					# policy impact evaluation
					policy_impact_evaluation(model_run_PE, model_run_elec, KPIs, evaluation_tick)

					# running the policy emergence model
					policy_chosen = model_run_PE.step(KPIs)

					# run of the policy context model for interval_tick ticks
					for p in range(interval_tick):
						KPIs = model_run_elec.step(policy_chosen)
						policy_chosen = [None for ite in range(len(model_run_PE.policy_instruments[0]))] # reset policy
					# after it has been implemented once

					# dataPlot_Elec_model = model_run_elec.datacollector.get_model_vars_dataframe()
					# dataPlot_Elec_model.plot("step", ["electricity price"])
					# plt.show()

					'''
					Scenario Changes
					In this part of the code, changes can be introduced through scenarios for both the policy context
					and the policy emergence models
					'''
					# redefining the issue tree basics - hardcoded values for simplicity
					issuetree_virgin = issuetree_creation(model_run_PE, model_run_PE.len_DC, model_run_PE.len_PC,
														  model_run_PE.len_S, model_run_PE.len_CR)
					policytree_virgin = policytree_creation(model_run_PE, model_run_PE.len_PC, model_run_PE.len_S,
															model_run_PE.len_PC, model_run_PE.len_ins)


					# # checker code
					# for agent in model_run_PE.schedule.agent_buffer(shuffled=False):
					# 	if isinstance(agent, ActiveAgent):
					# 		print(' ')
					# 		print(agent.agent_type, '\n', 'ID', agent.unique_id, 'Aff', agent.affiliation,
					# 		agent.issuetree[agent.unique_id], '\n', agent.policytree[agent.unique_id])

				# output of the data
				# policy context model
				output_policyContext_model = model_run_elec.datacollector.get_model_vars_dataframe()
				output_policyContext_model.to_csv('O_E1_model_' + str(demand_growth[demand_ite])
												  + '_w_el' + str(w_el_influence[w_el_i])
												  + '_Run' + str(rep_runs) + '.csv')

				# policy emergence model
				output_SM_model = model_run_PE.datacollector.get_model_vars_dataframe()
				output_SM_model.to_csv('O_SM_model_' + str(demand_growth[demand_ite])
									   + '_w_el' + str(w_el_influence[w_el_i])
									   + '_Run' + str(rep_runs) + '.csv')
				output_SM_agents = model_run_PE.datacollector.get_agent_vars_dataframe()
				output_SM_agents.to_csv('O_SM_agents_' + str(demand_growth[demand_ite])
										+ '_w_el' + str(w_el_influence[w_el_i])
										+ '_Run' + str(rep_runs) + '.csv')

				end = time.time()

				print('Simulation run time (hybrid):', end - start)
				print(' ')


'''
Run times -
22.10.0219 - 1713: 27 years - 7836.05 seconds - 130.6 minutes [laptop]
23.10.0219 - 1630: 27 years - 7855.05 seconds - 130.9 minutes [laptop]
24.10.0219 - 0930: 27 years - 7707.10 seconds - 128.4 minutes [laptop]
24.10.0219 - 1100: 27 years - 7258.28 seconds - 121.0 minutes [laptop]
25.10.0219 - 1830: 27 years - 6725.77 seconds - 112.1 minutes [server EPFL]
19.11.2019 - 0600: 27 years - 3176.71 seconds - 52.90 minutes [laptop]
19.11.2019 - 0643: 27 years - 3329.72 seconds - 55.48 minutes [laptop]

8018
'''