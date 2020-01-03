from model_schelling import Schelling
from model_SM import PolicyEmergenceSM
import pandas as pd

from model_SM_policyImpact import policy_impact_evaluation
from model_module_interface import issue_mapping

'''
The architecture present here is to be used for performing experiments. A batch runner algorithm will be used such that
a set of experiments can be run at the same time.

At the moment: 3 experiments and 4 scenarios

- The scenarios introduce change in the model:
	\item Scenario 1: Switch of the decision making power balance in the policy formulation step (from affiliation 1 to 2)
	\item Scenario 2: Switch of the decision making power balance in the agenda setting step (from affiliation 1 to 2)
	\item Scenario 3: Switch of the decision making power balance in both steps (from affiliation 1 to 2)
- The experiments relate to the beliefs of the agents - both initialisation and mid-time changes (goals for the agents):

TO DO:
- Remove all instances of policy families
- Split the electorate influence as a separate experiment 
'''

# batch run parameters
repetitions_runs = 50
sce_number = 4

# running parameters
total_ticks = 155
interval_tick = 5
run_tick = int(total_ticks / interval_tick)
warmup_tick = interval_tick

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

# parameters of the policy emergence model
'''for all scenarios'''
resources_aff = [75, 75]  # resources per affiliation agent out of 100
representativeness = [25, 75]  # electorate representativeness per affiliation

'''scenario 0'''
SM_PMs0 = 3  # number of policy makers
SM_PMs_aff0 = [2, 1]  # policy maker distribution per affiliation
SM_PEs0 = 4  # number of policy entrepreneurs
SM_PEs_aff0 = [2, 2]  # policy entrepreneur distribution per affiliation
SM_EPs0 = 0  # number of external parties
SM_EPs_aff0 = [0, 0]  # external parties distribution per affiliation

'''scenario 1'''
SM_PMs1 = 3  # number of policy makers
SM_PMs_aff1 = [1, 2]  # policy maker distribution per affiliation
SM_PEs1 = 6  # number of policy entrepreneurs
SM_PEs_aff1 = [4, 2]  # policy entrepreneur distribution per affiliation
SM_EPs1 = 0  # number of external parties
SM_EPs_aff1 = [0, 0]  # external parties distribution per affiliation

'''scenario 2'''
SM_PMs2 = 3  # number of policy makers
SM_PMs_aff2 = [2, 1]  # policy maker distribution per affiliation
SM_PEs2 = 4  # number of policy entrepreneurs
SM_PEs_aff2 = [2, 2]  # policy entrepreneur distribution per affiliation
SM_EPs2 = 0  # number of external parties
SM_EPs_aff2 = [0, 0]  # external parties distribution per affiliation

'''scenario 4'''
SM_PMs3 = 3  # number of policy makers
SM_PMs_aff3 = [2, 1]  # policy maker distribution per affiliation
SM_PEs3 = 4  # number of policy entrepreneurs
SM_PEs_aff3 = [2, 2]  # policy entrepreneur distribution per affiliation
SM_EPs3 = 0  # number of external parties
SM_EPs_aff3 = [0, 0]  # external parties distribution per affiliation

'''grouping'''
SM_PMs = [SM_PMs0, SM_PMs1, SM_PMs2, SM_PMs3]  # number of policy makers
SM_PMs_aff = [SM_PMs_aff0, SM_PMs_aff1, SM_PMs_aff2, SM_PMs_aff3]  # policy maker distribution per affiliation
SM_PEs = [SM_PEs0, SM_PEs1, SM_PEs2, SM_PEs3]  # number of policy entrepreneurs
SM_PEs_aff = [SM_PEs_aff0, SM_PEs_aff1, SM_PEs_aff2, SM_PEs_aff3]  # policy entrepreneur distribution per affiliation
SM_EPs = [SM_EPs0, SM_EPs1, SM_EPs2, SM_EPs3]  # number of external parties
SM_EPs_aff = [SM_EPs_aff0, SM_EPs_aff1, SM_EPs_aff2, SM_EPs_aff3]  # external parties distribution per affiliation

# input profile for preferred states
'''
This can be used for different scenarios for the preferred states (goals) of the policy emergence agents
'''
input_goalProfiles_file_Ex1Be = 'input_goalProfiles_Ex1Be'
input_goalProfiles_file_Ex2Be = 'input_goalProfiles_Ex2Be'
input_goalProfiles_file_Ex3Be = 'input_goalProfiles_Ex3Be'
input_goalProfiles_file_Ex4Be = 'input_goalProfiles_Ex4Be'
goal_input_Ex1Be = pd.read_csv(input_goalProfiles_file_Ex1Be, sep=',')
goal_input_Ex2Be = pd.read_csv(input_goalProfiles_file_Ex2Be, sep=',')
goal_input_Ex3Be = pd.read_csv(input_goalProfiles_file_Ex3Be, sep=',')
goal_input_Ex4Be = pd.read_csv(input_goalProfiles_file_Ex4Be, sep=',')
goal_profiles_Ex1Be = []
goal_profiles_Ex2Be = []
goal_profiles_Ex3Be = []
goal_profiles_Ex4Be = []
for i in range(len(resources_aff) * 2):
    goal_profiles_Ex1Be.append(goal_input_Ex1Be.iloc[i].tolist())  # goal profiles for active agents and electorate
    goal_profiles_Ex2Be.append(goal_input_Ex2Be.iloc[i].tolist())  # goal profiles for active agents and electorate
    goal_profiles_Ex3Be.append(goal_input_Ex3Be.iloc[i].tolist())  # goal profiles for active agents and electorate
    goal_profiles_Ex4Be.append(goal_input_Ex4Be.iloc[i].tolist())  # goal profiles for active agents and electorate

# putting all of the profiles into two list for the different experiments (one for initial goals and one
# for the goals after the mid-change)
goal_profiles = [goal_profiles_Ex1Be, goal_profiles_Ex2Be, goal_profiles_Ex3Be, goal_profiles_Ex4Be]

# running a number of scenarios
''' changes in the agent distribution '''
for sce_i in range(sce_number):

    # creating the agents for the policy emergence model
	SM_inputs = [SM_PMs[sce_i], SM_PMs_aff[sce_i], SM_PEs[sce_i], SM_PEs_aff[sce_i], SM_EPs[sce_i], SM_EPs_aff[sce_i],
				 resources_aff, representativeness, goal_profiles[sce_i]]

	# running a number of repetitions per scenario
	for rep_runs in range(repetitions_runs):

        # for model run tailoring
		if sce_i >= 0 and rep_runs >= 0:

			# initialisation of the Schelling model
			model_run_schelling = Schelling(sch_height, sch_width, sch_density, sch_minority_pc, sch_homophilyType0,
											sch_homophilyType1, sch_movementQuota, sch_happyCheckRadius,
											sch_moveCheckRadius, sch_last_move_quota)

			# initialisation of the policy emergence model
			model_run_PE = PolicyEmergenceSM(SM_inputs, 10, 10)

			print("\n")
			print("************************")
			print("Start of the simulation:", "\n")
			for i in range(run_tick):

				print(" ")
				print("************************")
				print("Tick number: ", i, ', scenario:', sce_i, ', run number:', rep_runs)

				# warm up time
				# this is also used as a warmup time
				if i == 0:
					policy_chosen = [None for ite in range(len(model_run_PE.policy_instruments[0]))]
					for warmup_time in range(warmup_tick):
						IssueInit, type0agents, type1agents = model_run_schelling.step(policy_chosen)

				# policy impact evaluation
				policy_impact_evaluation(model_run_PE, model_run_schelling, IssueInit, interval_tick)

				# running the policy emergence model
				if i == 0:
					KPIs = issue_mapping(IssueInit, type0agents, type1agents)
				else:
					KPIs = issue_mapping(KPIs, type0agents, type1agents)
				policy_chosen = model_run_PE.step(KPIs)

				# run of the segregation model for n ticks
				for p in range(interval_tick):
					KPIs, type0agents, type1agents = model_run_schelling.step(policy_chosen)
					policy_chosen = [None for ite in range(
						len(model_run_PE.policy_instruments[0]))]  # reset policy after it has been implemented once

				'''
				Below are all the changes related to the SCENARIOS AND EXPERIMENTS
				These changes are happening at the midway point of the simulation.
				Three scenarios are being considered. The details are provided in the formalisation report.
				One of the experiment is also included as it contains a change in the causal relations of the agents
				of affiliation 1 mid-simulation.
				'''

			# # checker code
			# for agent in model_run_PE.schedule.agent_buffer(shuffled=False):
			# 	if isinstance(agent, ActiveAgent):
			# 		print(' ')
			# 		print(agent.agent_type, '\n', 'ID', agent.unique_id, 'Aff', agent.affiliation,
			# 		agent.issuetree[agent.unique_id], '\n', agent.policytree[agent.unique_id])

			# output of the data
			# Schelling model
			output_Schelling_model = model_run_schelling.datacollector.get_model_vars_dataframe()
			output_Schelling_model.to_csv(
				'O_Sch_model_Sce' + str(sce_i) + '_Run' + str(rep_runs) + '.csv')
			# dataPlot_Schelling_agents = model_run_schelling.datacollector.get_agent_vars_dataframe()
			# dataPlot_Schelling_agents.to_csv('O_Sch_agents_Sce' + str(sce_i) + '_Run' + str(rep_runs) + '.csv')
			# agents are not needed a this point

			# policy emergence model
			output_SM_model = model_run_PE.datacollector.get_model_vars_dataframe()
			output_SM_model.to_csv('O_PE_model_Sce' + str(sce_i) + '_Run' + str(rep_runs) + '.csv')
			output_SM_agents = model_run_PE.datacollector.get_agent_vars_dataframe()
			output_SM_agents.to_csv('O_PE_agents_Sce' + str(sce_i) + '_Run' + str(rep_runs) + '.csv')