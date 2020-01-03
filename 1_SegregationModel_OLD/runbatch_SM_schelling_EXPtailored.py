from model_schelling import Schelling
from model_SM import PolicyEmergenceSM
import matplotlib.pyplot as plt
import copy
import pandas as pd
import os

from model_SM_policyImpact import policy_impact_evaluation
from model_module_interface import issue_mapping
from model_SM_agents import TruthAgent, ActiveAgent, ElectorateAgent
from model_SM_agents_initialisation import issuetree_creation, policytree_creation

'''
The architecture present here is to be used for performing experiments. A batch runner algorithm will be used such that a set of experiments can be run at the same time.


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
exp_number = 0

# running parameters
total_ticks = 155
interval_tick = 5
run_tick = int(total_ticks/interval_tick)
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
SM_PMs = 3  # number of policy makers
SM_PMs_aff = [2, 1]  # policy maker distribution per affiliation
SM_PEs = 4  # number of policy entrepreneurs
SM_PEs_aff = [2, 2]  # policy entrepreneur distribution per affiliation
SM_EPs = 0  # number of external parties
SM_EPs_aff = [0, 0]  # external parties distribution per affiliation
resources_aff = [75, 75]  # resources per affiliation agent out of 100
representativeness = [25, 75]  # electorate representativeness per affiliation

# first goal input profile
input_goalProfiles_file_Ex1Be = 'input_goalProfiles_Ex1Be'
goal_input_Ex1Be = pd.read_csv(input_goalProfiles_file_Ex1Be, sep=',')
goal_profiles_Ex1Be = []
for i in range(len(resources_aff)*2):
	goal_profiles_Ex1Be.append(goal_input_Ex1Be.iloc[i].tolist())  # goal profiles for active agents and electorate
# first goal input profile (after change)
input_goalProfiles_file_Ex1Af = 'input_goalProfiles_Ex3Af'
goal_input_Ex1Af = pd.read_csv(input_goalProfiles_file_Ex1Af, sep=',')
goal_profiles_Ex1Af = []
for i in range(len(resources_aff)*2):
	goal_profiles_Ex1Af.append(goal_input_Ex1Af.iloc[i].tolist())  # goal profiles for active agents and electorate


# second goal input profile
input_goalProfiles_file_Ex2 = 'input_goalProfiles_Ex2'
goal_input_Ex2 = pd.read_csv(input_goalProfiles_file_Ex2, sep=',')
goal_profiles_Ex2 = []
for i in range(len(resources_aff)*2):
	goal_profiles_Ex2.append(goal_input_Ex2.iloc[i].tolist())  # goal profiles for active agents and electorate

# third goal input profile (before change)
input_goalProfiles_file_Ex3Be = 'input_goalProfiles_Ex3Be'
goal_input_Ex3Be = pd.read_csv(input_goalProfiles_file_Ex3Be, sep=',')
goal_profiles_Ex3Be = []
for i in range(len(resources_aff)*2):
	goal_profiles_Ex3Be.append(goal_input_Ex3Be.iloc[i].tolist())  # goal profiles for active agents and electorate
# third goal input profile (after change)
input_goalProfiles_file_Ex3Af = 'input_goalProfiles_Ex3Af'
goal_input_Ex3Af = pd.read_csv(input_goalProfiles_file_Ex3Af, sep=',')
goal_profiles_Ex3Af = []
for i in range(len(resources_aff)*2):
	goal_profiles_Ex3Af.append(goal_input_Ex3Af.iloc[i].tolist())  # goal profiles for active agents and electorate

# fourth goal input profile (before change)
input_goalProfiles_file_Ex4Be = 'input_goalProfiles_Ex4Be'
goal_input_Ex4Be = pd.read_csv(input_goalProfiles_file_Ex4Be, sep=',')
goal_profiles_Ex4Be = []
for i in range(len(resources_aff)*2):
	goal_profiles_Ex4Be.append(goal_input_Ex4Be.iloc[i].tolist())  # goal profiles for active agents and electorate
# fourth goal input profile (after change)
input_goalProfiles_file_Ex4Af = 'input_goalProfiles_Ex4Af'
goal_input_Ex4Af = pd.read_csv(input_goalProfiles_file_Ex4Af, sep=',')
goal_profiles_Ex4Af = []
for i in range(len(resources_aff)*2):
	goal_profiles_Ex4Af.append(goal_input_Ex4Af.iloc[i].tolist())  # goal profiles for active agents and electorate

# putting all of the profiles into two list for the different experiments (one for initial goals and one for the goals after the mid-change)
goal_profiles = [goal_profiles_Ex1Be, goal_profiles_Ex2, goal_profiles_Ex3Be, goal_profiles_Ex4Be]
goal_profiles_after = [goal_profiles_Ex3Af, 0, goal_profiles_Ex3Af, goal_profiles_Ex4Af]


# running a number of experiments
''' changes in the beliefs of the agents '''
for exp_i in range(4):

	# running a number of scenarios
	''' changes in the agent distribution '''
	for sce_i in range (4):

		# creating the agents for the policy emergence model
		SM_inputs = [SM_PMs, SM_PMs_aff, SM_PEs, SM_PEs_aff, SM_EPs, SM_EPs_aff, resources_aff, representativeness, goal_profiles[exp_i]]

		# running a number of repetitions per experiment
		for rep_runs in range(repetitions_runs):

			# for model run tailoring
			if exp_i == 0 and sce_i == 3 and rep_runs >= 0:

				# initialisation of the Schelling model
				model_run_schelling = Schelling(sch_height, sch_width, sch_density, sch_minority_pc, sch_homophilyType0, sch_homophilyType1, sch_movementQuota, sch_happyCheckRadius, sch_moveCheckRadius, sch_last_move_quota)

				# initialisation of the policy emergence model
				model_run_SM = PolicyEmergenceSM(SM_inputs, 10,10)

				print("\n")
				print("************************")
				print("Start of the simulation:", "\n")
				for i in range(run_tick):

					print(" ")
					print("************************")
					print("Tick number: ", i, ', experiment:', exp_i, ', scenario:', sce_i, ', run number:', rep_runs)

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

					'''
					Below are all the changes related to the SCENARIOS AND EXPERIMENTS
					These changes are happening at the midway point of the simulation.
					Three scenarios are being considered. The details are provided in the formalisation report.
					One of the experiment is also included as it contains a change in the causal relations of the agents of affiliation 1 mid-simulation.
					'''
					# redefining the issue tree basics - hardcoded values for simplicity
					issuetree_virgin = issuetree_creation(model_run_SM, model_run_SM.len_DC, model_run_SM.len_PC, model_run_SM.len_S, model_run_SM.len_CR)
					policytree_virgin = policytree_creation(model_run_SM, model_run_SM.len_PC, model_run_SM.len_S, model_run_SM.len_PC, model_run_SM.len_ins)

					'''
					Scenario 0 - Changes
					- One PM from affiliation 0 to 1 with corresponding goal changes
					- Two PEs added to affiliation 0 with corresponding goals
					'''
					if i == 15 and sce_i == 0:

						change = True
						obtained = True
						for agent in model_run_SM.schedule.agent_buffer(shuffled=False):
							# changing the policy maker
							if isinstance(agent, ActiveAgent) and agent.agent_type == 'policymaker' and agent.affiliation == 0 and change == True:
								_unique_id = agent.unique_id

								agent.affiliation = 1
								for issue in range(7): # seven is hardcoded here - issue goals replacement
									# changing the goals to the goals of the new affiliation
									# goal_profiles[Experiment][affiliation][issue + 1]
									agent.issuetree[_unique_id][issue][1] = goal_profiles[exp_i][1][issue + 1]
								change = False  # stop the for loop once one agent has been changed

							# adapting the size of the issuetree and the policytree
							if isinstance(agent, ActiveAgent):
								for added_tree in range(2):  # number of added agents
									agent.issuetree.append(issuetree_virgin)
									agent.policytree.append(policytree_virgin)

							# obtaining the issue tree for the policy entrepreneur
							if isinstance(agent, ActiveAgent) and agent.affiliation == 0 and obtained == True:
								_unique_id = copy.deepcopy(agent.unique_id)
								_issuetree_0 = copy.deepcopy(agent.issuetree)
								_issuetree_0[_unique_id] = _issuetree_0[_unique_id + 1]  # making sure to reset the issue tree
								_policytree_0 = copy.deepcopy(agent.policytree)
								_policytree_0[_unique_id] = _policytree_0[_unique_id + 1]  # making sure to reset the policy tree
								obtained = False

						# adding two PEs to affiliation 0
						x = 55
						y = 55
						unique_id = model_run_SM.number_activeagents
						for add_PEs in range(2):
							agent_type = 'policyentrepreneur'
							affiliation = 0
							resources = 0  # not important for this model
							issuetree = copy.deepcopy(_issuetree_0)
							# introducing the issues
							for issue in range(7): # seven is hardcoded here - caural relations replacement
								# changing the goals to the goals of the new affiliation
								# goal_profiles[Experiment][affiliation][issue + 1]
								issuetree[unique_id][issue][1] = goal_profiles[exp_i][affiliation][issue + 1]
							for CR in range(10): # ten is hardcoded here - issues replacement
								# goal_profiles[Experiment][affiliation][issue + 1]
								issuetree[unique_id][7 + CR][0] = goal_profiles[exp_i][affiliation][7 + CR + 1]

							policytree = copy.deepcopy(_policytree_0)

							agent = ActiveAgent((x, y), unique_id, model_run_SM, agent_type, resources, affiliation, issuetree, policytree)
							model_run_SM.preference_update(agent, unique_id)  # updating the issue tree preferences
							model_run_SM.grid.position_agent(agent, (x, y))
							model_run_SM.schedule.add(agent)

							# update of the standard inputs
							y += 1
							unique_id += 1

					'''
					Scenario 1 - Changes
					- Two PEs added to affiliation 1 with corresponding goals
					'''
					if i == 15 and sce_i == 1:

						obtained = True
						for agent in model_run_SM.schedule.agent_buffer(shuffled=False):
							# adapting the size of the issuetree and the policytree
							if isinstance(agent, ActiveAgent):
								for added_tree in range(2):  # number of added agents
									agent.issuetree.append(issuetree_virgin)
									agent.policytree.append(policytree_virgin)

							# obtaining the issue tree for thepolicy entrepreneur
							if isinstance(agent, ActiveAgent) and agent.affiliation == 1 and obtained == True:
								_unique_id = copy.deepcopy(agent.unique_id)
								_issuetree_0 = copy.deepcopy(agent.issuetree)
								_issuetree_0[_unique_id] = _issuetree_0[_unique_id + 1]  # making sure to reset the issue tree
								_policytree_0 = copy.deepcopy(agent.policytree)
								_policytree_0[_unique_id] = _policytree_0[_unique_id + 1]  # making sure to reset the policy tree
								obtained = False

						# adding two PEs to affiliation 0
						x = 55
						y = 55
						unique_id = model_run_SM.number_activeagents
						for add_PEs in range(2):
							agent_type = 'policyentrepreneur'
							affiliation = 1
							resources = 0  # not important for this model
							issuetree = copy.deepcopy(_issuetree_0)
							# introducing the issues
							for issue in range(7): # seven is hardcoded here - caural relations replacement
								# changing the goals to the goals of the new affiliation
								# goal_profiles[Experiment][affiliation][issue + 1]
								issuetree[unique_id][issue][1] = goal_profiles[exp_i][affiliation][issue + 1]
							for CR in range(10): # ten is hardcoded here - issues replacement
								# goal_profiles[Experiment][affiliation][issue + 1]
								issuetree[unique_id][7 + CR][0] = goal_profiles[exp_i][affiliation][7 + CR + 1]

							policytree = copy.deepcopy(_policytree_0)

							agent = ActiveAgent((x, y), unique_id, model_run_SM, agent_type, resources, affiliation, issuetree, policytree)
							model_run_SM.preference_update(agent, unique_id)  # updating the issue tree preferences
							model_run_SM.grid.position_agent(agent, (x, y))
							model_run_SM.schedule.add(agent)

							# update of the standard inputs
							y += 1
							unique_id += 1

					'''
					Scenario 2 - Changes
					- One PM from affiliation 0 to 1 with corresponding goal changes
					'''
					if i == 15 and sce_i == 2:

						change = True
						for agent in model_run_SM.schedule.agent_buffer(shuffled=False):
							# changing the policy maker
							if isinstance(agent, ActiveAgent) and agent.agent_type == 'policymaker' and agent.affiliation == 0 and change == True:
								_unique_id = agent.unique_id

								agent.affiliation = 1
								for issue in range(7): # seven is hardcoded here - issue goals replacement
									# changing the goals to the goals of the new affiliation
									# goal_profiles[Experiment][affiliation][issue + 1]
									agent.issuetree[_unique_id][issue][1] = goal_profiles[exp_i][1][issue + 1]
								change = False  # stop the for loop once one agent has been changed

					'''
					Scenario 3 - Changes
					- Change the electorate values for their goals
					'''
					if i == 15 and sce_i == 3:

						for agent in model_run_SM.schedule.agent_buffer(shuffled=False):
							if isinstance(agent, ElectorateAgent) :
								for issue in range(7):
									agent.issuetree_elec[issue] = goal_profiles_after[exp_i][2+agent.affiliation][issue + 1]

					# # checker code
					# for agent in model_run_SM.schedule.agent_buffer(shuffled=False):
					# 	if isinstance(agent, ActiveAgent):
					# 		print(' ')
					# 		print(agent.agent_type, '\n', 'ID', agent.unique_id, 'Aff', agent.affiliation, agent.issuetree[agent.unique_id], '\n', agent.policytree[agent.unique_id])


				# output of the data
				# Schelling model
				output_Schelling_model = model_run_schelling.datacollector.get_model_vars_dataframe()
				output_Schelling_model.to_csv('O_Sch_model_' + str(exp_i) + '_Sce' + str(sce_i) + '_Run' + str(rep_runs) + '.csv')
				# dataPlot_Schelling_agents = model_run_schelling.datacollector.get_agent_vars_dataframe()
				# dataPlot_Schelling_agents.to_csv('O_Sch_agents_' + str(exp_i) + '_Sce' + str(sce_i) + '_Run' + str(rep_runs) + '.csv')  # agents are not needed a this point

				# policy emergence model
				output_SM_model = model_run_SM.datacollector.get_model_vars_dataframe()
				output_SM_model.to_csv('O_SM_model_Exp' + str(exp_i) + '_Sce' + str(sce_i) + '_Run' + str(rep_runs) + '.csv')
				output_SM_agents = model_run_SM.datacollector.get_agent_vars_dataframe()
				output_SM_agents.to_csv('O_SM_agents_' + str(exp_i) + '_Sce' + str(sce_i) + '_Run' + str(rep_runs) + '.csv')