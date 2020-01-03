from model_schelling import Schelling
from model_SM import PolicyEmergenceSM
import matplotlib.pyplot as plt
import copy
import pandas as pd
import os
from model_SM_agents import ActiveAgent

from model_SM_policyImpact import policy_impact_evaluation
from model_module_interface import issue_mapping
from model_SM_agents import TruthAgent

'''
The architecture present here is to be used for performing experiments. A batch runner algorithm will be used such that a set of experiments can be run at the same time.
'''

# batch run parameters
repetitions_runs = 5
exp_number = 0

# running parameters
total_ticks = 15
interval_tick = 5
run_tick = int(total_ticks/interval_tick)
warmup_tick = interval_tick

# parameters of the policy emergence model
SM_PMs = 3  # number of policy makers
SM_PMs_aff = [2, 1]  # policy maker distribution per affiliation
SM_PEs = 5  # number of policy entrepreneurs
SM_PEs_aff = [3, 2]  # policy entrepreneur distribution per affiliation
SM_EPs = 2  # number of external parties
SM_EPs_aff = [1, 1]  # external parties distribution per affiliation
resources_aff = [75, 75]  # resources per affiliation agent out of 100
representativeness = [25, 75]  # electorate representativeness per affiliation
input_goalProfiles_file = 'input_goalProfiles'
goal_input = pd.read_csv(input_goalProfiles_file, sep=',')
goal_profiles = []
for i in range(len(resources_aff)*2):
	goal_profiles.append(goal_input.iloc[i].tolist())  # goal profiles for active agents and electorate
SM_inputs = [SM_PMs, SM_PMs_aff, SM_PEs, SM_PEs_aff, SM_EPs, SM_EPs_aff, resources_aff, representativeness, goal_profiles]

# parameters of the Schelling model
sch_height = 20  # height of the grid - this value must be a multiple of 4
sch_width = 20  # width of the grid - this value must be a multiple of 4
sch_density = 0.8  # agent percentage density on the grid
sch_minority_pc = 0.4  # percentage of type 1 agents compared to type 0
sch_homophilyType0 = 0.7  # homophily of type 0 agents
sch_homophilyType1 = 0.5  # homophily of type 1 agents
sch_movementQuota = 0.30  # initial movement quota
sch_happyCheckRadius = 5  # initial happiness check radius
sch_moveCheckRadius = 10  # initial movement check radius
sch_last_move_quota = 5  # initial last moment quota


# runnin a number of repetitions
for i_runs in range(repetitions_runs):

	# initialisation of the Schelling model
	model_run_schelling = Schelling(sch_height, sch_width, sch_density, sch_minority_pc, sch_homophilyType0, sch_homophilyType1, sch_movementQuota, sch_happyCheckRadius, sch_moveCheckRadius, sch_last_move_quota)

	# initialisation of both models
	model_run_SM = PolicyEmergenceSM(SM_inputs, 10,10)
	for agent in model_run_SM.schedule.agent_buffer(shuffled=True):
		if isinstance(agent, ActiveAgent):
			print(agent.affiliation)

	print("\n")
	print("************************")
	print("Start of the simulation:", "\n")
	for i in range(run_tick):

		print(" ")
		print("************************")
		print("Tick number: ", i)

		# warm up time
		# this is also used as a warmup time
		if i == 0:
			policy_chosen = [None for ite in range(len(model_run_SM.policy_instruments[0]))]
			for warmup_time in range(warmup_tick):
				IssueInit, type0agents, type1agents = model_run_schelling.step(policy_chosen)

		# policy impact evaluation
		policy_impact_evaluation(model_run_SM, model_run_schelling, IssueInit, interval_tick)

		# running the policy emergence model
		if i == 0:
			KPIs = issue_mapping(IssueInit, type0agents, type1agents)
		else:
			KPIs = issue_mapping(KPIs, type0agents, type1agents)
		policy_chosen = model_run_SM.step(KPIs)

		# run of the segregation model for n ticks
		for p in range(interval_tick):
			KPIs, type0agents, type1agents = model_run_schelling.step(policy_chosen)
			policy_chosen = [None for ite in range(len(model_run_SM.policy_instruments[0]))] # reset policy after it has been implemented once

	# output of the data
	# Schelling model
	# printing the data obtained from the Schelling model
	dataPlot_Schelling_model = model_run_schelling.datacollector.get_model_vars_dataframe()
	# dataPlot_Schelling_agents = model_run_schelling.datacollector.get_agent_vars_dataframe()

	dataPlot_Schelling_model.to_csv('O_Sch_model_' + str(exp_number) + '_' + str(i_runs) + '.csv')
	# dataPlot_Schelling_agents.to_csv('O_Sch_agents_', exp_number, '_', i_runs, '.csv')  # agents are not needed a this point

	# policy emergence model
	dataPlot_SM_model = model_run_SM.datacollector.get_model_vars_dataframe()
	dataPlot_SM_agents = model_run_SM.datacollector.get_agent_vars_dataframe()

	dataPlot_SM_model.to_csv('O_SM_model_' + str(exp_number) + '_' + str(i_runs) + '.csv')
	dataPlot_SM_agents.to_csv('O_SM_agents_' + str(exp_number) + '_' + str(i_runs) + '.csv')