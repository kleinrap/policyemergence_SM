from agent import Agent
import random
import copy
from agent import Policymakers, Policyentres

# Creation of the truth agents
# class Truth(Agent):

# 	def __init__(self, pos, belieftree_truth):
# 		# super().__init__(unique_id, model)
# 		self.pos = pos
# 		# self.model = model
# 		self.belieftree_truth = belieftree_truth

# 	def __str__(self):
# 		return 'Position: [' + str(self.pos[0]) + ',' + str(self.pos[1]) + '], Belief tree: ' + str(self.belieftree_truth)

# # Creation of the electorate agents
# class Electorate(Agent):

# 	def __init__(self, run_number, pos, affiliation, belieftree_electorate, representation):
# 		# super().__init__(unique_id, model)
# 		self.run_number = run_number
# 		self.pos = pos
# 		# self.model = model
# 		self.affiliation = affiliation
# 		self.belieftree_electorate = belieftree_electorate
# 		self.representation = representation

# 	def electorate_influence(self, agent, master_list, affiliation_number, electorate_influence_coefficient):

# 		"""
# 		Electorate influence function
# 		===========================

# 		This function calculates the influence of the electorates 
# 		on the policy makers. It is dependent on the affiliations
# 		of each of the agents. The electorate can only influence
# 		policy makers with whom they share their affiliations.

# 		"""

# 		self.master_list = master_list

# 		policymaker_list = []
# 		for agents in self.master_list:
# 			if type(agents) == Policymakers:
# 				policymaker_list.append(agents)

# 		policymaker_number = len(policymaker_list)
# 		# policymaker_list = self.master_list[Policymakers]
# 		# Looking through all affiliations
# 		for i in range(affiliation_number):
# 			# Selecting one affiliation
# 			if self.affiliation == i:
# 				# Selection of the policy maker:
# 				for j in range(policymaker_number):
# 					# checking of the affiliation match of the policy maker
# 					if policymaker_list[j].affiliation == i:
# 						# Now we can change the tree of the policy makers
# 						for k in range(len(self.belieftree_electorate)):
# 							# print('Before change: ' + str(policymaker_list[j].belieftree[0][k][1]))
# 							policymaker_list[j].belieftree[0][k][1] = policymaker_list[j].belieftree[0][k][1] + \
# 							  (self.belieftree_electorate[k][1] - policymaker_list[j].belieftree[0][k][1]) * electorate_influence_coefficient
# 							# Again the oneminusone check does not work here
# 							policymaker_list[j].belieftree[0][k][1] = \
# 								self.one_minus_one_check(policymaker_list[j].belieftree[0][k][1])
# 							# print('Afters change: ' + str(policymaker_list[j].belieftree[0][k][1]))
# 						# print(policymaker_list[j].pos)
# 				# print(self.belieftree_electorate)
# 				# print(self.affiliation)
# 				# print(self.pos)

# 	def one_minus_one_check(self, to_be_checked_parameter):

# 		"""
# 		One minus one check function
# 		===========================

# 		This function checks that a certain values does not got over one
# 		and does not go below one due to the randomisation.
		
# 		"""

# 		checked_parameter = 0
# 		if to_be_checked_parameter > 1:
# 			checked_parameter = 1
# 		elif to_be_checked_parameter < -1:
# 			checked_parameter = -1
# 		else:
# 			checked_parameter = to_be_checked_parameter
# 		return checked_parameter

# 	def electorate_states_update(self, agent, master_list, affiliation_weights):

# 		"""
# 		The electorate states update function
# 		===========================

# 		This function uses the agent, the master list and the affiliation weight
# 		to update the states of the electorate belief tree. This is done using the
# 		states of the external parties depending on their affiliation and is therefore
# 		impacted by the affiliation weights.

# 		It is also assumed that the initial belief of the electorate is equal
# 		to their aim in the first tick.

# 		"""

# 		#' Addition of more than 3 affiliation will lead to unreported errors!')
# 		if len(affiliation_weights) != 3:
# 			print('WARNING - THIS CODE DOESNT WORK FOR MORE OR LESS THAN 3 AFFILIATIONS')

# 		# Defining the external party list along with the truth agent relation
# 		externalparties_list = []
# 		for agents in master_list:
# 			if type(agents) == Truth:
# 				truthagent = agents
# 			if type(agents) == Externalparties:
# 				externalparties_list.append(agents)

# 		# Going through the different external parties:
# 		belief_sum_ep = [0 for k in range(len(truthagent.belieftree_truth))]
# 		for i in range(len(truthagent.belieftree_truth)):
# 			# This is used because in some cases, the external parties will have no impact on the agent (None values in the states of the EP)
# 			actual_length_ep = 0
# 			for j in range(len(externalparties_list)):
# 				# This line is added in case the EP has None states
# 				if externalparties_list[j].belieftree[i][0] != 'No':
# 					actual_length_ep += 1
# 					# Currently, the state of the policy makers is initialised as being equal to their initial aim:
# 					if agent.belieftree_electorate[i][0] == None:
# 						# print('Triggered - changed to: ' + str(agent.belieftree[0][i][1]))
# 						agent.belieftree_electorate[i][0] = agent.belieftree_electorate[i][1]
# 					# If they have the same affiliation, add without weight
# 					if externalparties_list[j].affiliation == agent.affiliation:
# 						# print('AFFILIATIONS ARE EQUAL')
# 						# print('issue ' + str(i+1) + ': ' + str(externalparties_list[j].belieftree[0][i][0]) +  /
# 						# ' and affiliation: ' + str(externalparties_list[j].affiliation) + '  ' + str(externalparties_list[j].unique_id))
# 						# print('This is the sum: ' + str(belief_sum_ep[i]))
# 						belief_sum_ep[i] = belief_sum_ep[i] + (externalparties_list[j].belieftree[0][i][0] - agent.belieftree_electorate[i][0])
# 						# print('The sum is equal to: ' + str(belief_sum_ep))
# 						# print('The change in state belief is equal to: ' + str(belief_sum_ep[i] / len(externalparties_list)))
# 					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 1) or \
# 					   (externalparties_list[j].affiliation == 1 and agent.affiliation == 0):
# 						# print('AFFILIATION 1 AND 2')
# 						belief_sum_ep[i] = belief_sum_ep[i] + \
# 						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree_electorate[i][0]) * affiliation_weights[0]
# 					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 2) or \
# 					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 0):
# 						# print('AFFILIATION 1 AND 3')
# 						belief_sum_ep[i] = belief_sum_ep[i] + \
# 						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree_electorate[i][0]) * affiliation_weights[1]
# 					if (externalparties_list[j].affiliation == 1 and agent.affiliation == 2) or \
# 					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 1):
# 						# print('AFFILIATION 2 AND 3')
# 						belief_sum_ep[i] = belief_sum_ep[i] + \
# 						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree_electorate[i][0]) * affiliation_weights[2]
# 			agent.belieftree_electorate[i][0] = agent.belieftree_electorate[i][0] + belief_sum_ep[i] / actual_length_ep

# 	# def __str__(self):
# 	# 	return 'Affiliation: ' + str(self.affiliation) + ', Position: [' + str(self.pos[0]) + \
# 	# 	',' + str(self.pos[1]) + '], Electorate belief tree: ' + str(self.belieftree_electorate)

# # Creation of the external party agents
# class Externalparties(Agent):

# 	def __init__(self, run_number, agent_id, unique_id, pos, network_strategy, affiliation, resources, belieftree, instrument_preferences, belieftree_policy, belieftree_instrument, select_as_issue, select_pinstrument, select_issue_3S_as, \
# 		select_problem_3S_as, select_policy_3S_as, select_issue_3S_pf, select_problem_3S_pf, select_policy_3S_pf, team_as, team_pf, coalition_as, coalition_pf):
# 		# super().__init__(unique_id, model)
# 		self.run_number = run_number
# 		self.agent_id = agent_id
# 		self.unique_id = unique_id
# 		self.pos = pos
# 		self.network_strategy = network_strategy
# 		self.affiliation = affiliation
# 		self.resources = resources
# 		self.belieftree = belieftree
# 		self.instrument_preferences = instrument_preferences
# 		self.belieftree_policy = belieftree_policy
# 		self.belieftree_instrument = belieftree_instrument
# 		self.select_as_issue = select_as_issue
# 		self.select_pinstrument = select_pinstrument
# 		self.select_issue_3S_as = select_issue_3S_as
# 		self.select_problem_3S_as = select_problem_3S_as
# 		self.select_policy_3S_as = select_policy_3S_as
# 		self.select_issue_3S_pf = select_issue_3S_pf
# 		self.select_problem_3S_pf = select_problem_3S_pf
# 		self.select_policy_3S_pf = select_policy_3S_pf
# 		self.team_as = team_as
# 		self.team_pf = team_pf
# 		self.coalition_as = coalition_as
# 		self.coalition_pf = coalition_pf

# 	def external_parties_states_update(self, agent, master_list, no_interest_states):

# 		"""
# 		The external parties states update function
# 		===========================

# 		This function uses the truth agent to update the states of the external parties
# 		belief tree.

# 		Note: Ultimately, this would need to include the external parties lack of interests
# 		for some of the states.

# 		"""

# 		for agents in master_list:
# 			if type(agents) == Truth:
# 				truthagent = agents

# 		# print('Before: '  + str(agent.belieftree[0]))
# 		for i in range(len(truthagent.belieftree_truth)):
# 			# print(no_interest_states[agent.agent_id][i])
# 			if no_interest_states[agent.agent_id][i] == 1:
# 				# print('Value i: ' + str(i) + ' is being changed')
# 				agent.belieftree[0][i][0] = truthagent.belieftree_truth[i]
# 			# print('HERE!')
# 			else:
# 				agent.belieftree[0][i][0] = 'No'

# 		# print('After: '  + str(agent.belieftree[0]))
# 		# print('State updated!')
	
# 	# def __str__(self):
# 	# 	return 'EXTERNAL PARTIES - ' + 'Affiliation: ' + str(self.affiliation) + ', Resources: ' + str(self.resources) + \
# 	# 	', Position: [' + str(self.pos[0]) + \
# 	# 	',' + str(self.pos[1]) + '], ID: ' + str(self.unique_id) + ', Problem selected + 1: ' + str(self.select_problem) + \
# 	# 	', Policy selected + 1: ' + str(self.select_policy) + ', Belief tree: ' + str(self.belieftree)

# 	# Simple print with ID
# 	def __str__(self):
# 		return 'External party: ' + str(self.unique_id)

# 	def external_parties_actions_as(self, agents, agent_action_list, causalrelation_number, \
# 		affiliation_weights, deep_core, mid_level, secondary, electorate_number, action_agent_number, master_list, link_list):

		

# 		"""
# 		The external parties actions function (agenda setting)
# 		===========================

# 		This function is used to perform the different active actions of the
# 		external parties during the agenda setting.

# 		It is split in two main parts:
# 		1. All active actions (blanket framing, blanket state influence and 
# 		blanket aim influence)
# 		2. Electorate influence - on the aims

# 		"""

# 		len_PC = len(deep_core)
# 		len_ML = len(mid_level)
# 		len_S = len(secondary)

# 		############################################################################################################
# 		############################################################################################################
# 		#### TEST ##################################################################################################
# 		############################################################################################################
# 		############################################################################################################

# 		# self.print_test()

# 		# # Selecting the relevant causal relations
# 		# cw_of_interest = []
# 		# for cw_choice in range(len(deep_core)):
# 		# 		cw_of_interest.append(len_PC + len_ML + len_S + (agents.select_as_issue - len_PC) + cw_choice * len(mid_level))

# 		# self.influence_actions_AS(agents, agent_action_list, link_list, cw_of_interest, affiliation_weights, action_agent_number, len_PC, len_ML, len_S)

# 		############################################################################################################
# 		############################################################################################################
# 		############################################################################################################


# 		# Assignment of the resources for the two main types of actions:
# 		agents.resources_actions_EInfluence = agents.resources_actions * 0.2

# 		############################################################################################################
# 		# 1. Blanket framing, grading of actions and implementation of the best actions until resources run out 
# 		# 100% of the resources (from actions)

# 		# This will need to be adjusted at a later point
# 		actionWeight = 1

# 		# Selecting the relevant causal relations
# 		cw_of_interest = []
# 		for cw_choice in range(len(deep_core)):
# 				cw_of_interest.append(len_PC + len_ML + len_S + (agents.select_as_issue - len_PC) + cw_choice * len(mid_level))

# 		# Making sure that there are enough resources
# 		while agents.resources_actions > 0.001:

# 			####################################
# 			# Grading of all the possible actions

# 			total_agent_grades = []

# 			# For the causal relations
# 			for cw in cw_of_interest:
# 				cw_grade_list = []
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					# Going through all of the links
# 					for links in link_list:
# 						# Check that the list has an awareness level
# 						if links.aware != -1:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 								# Make sure to look at the right direction of the conflict level
# 								if links.agent1 == agents:
									
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										cw_grade = links.conflict_level[0][cw][0] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										cw_grade = links.conflict_level[0][cw][0] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										cw_grade = links.conflict_level[0][cw][0] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										cw_grade = links.conflict_level[0][cw][0] * links.aware * actionWeight * affiliation_weights[2]

# 									cw_grade_list.append(cw_grade)

# 								if links.agent2 == agents:
									
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										cw_grade = links.conflict_level[1][cw][0] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										cw_grade = links.conflict_level[1][cw][0] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										cw_grade = links.conflict_level[1][cw][0] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										cw_grade = links.conflict_level[1][cw][0] * links.aware * actionWeight * affiliation_weights[2]
									
# 									cw_grade_list.append(cw_grade)

# 						# If the link has a negative awareness, set the grade of the action to 0
# 						else:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 								cw_grade_list.append(0)

# 				total_agent_grades.append(sum(cw_grade_list))

# 			# For the state on the selected issue
# 			state_grade_list = []
# 			# Going through all active agents
# 			for agent_inspected in agent_action_list:
# 				for links in link_list:
# 					# Check that the list has an awareness level
# 					if links.aware != -1:
# 						# Check that only the link of interest is selected
# 						if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:

# 							# Make sure to look at the right direction of the conflict level
# 							if links.agent1 == agents:
							
# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									state_grade = links.conflict_level[0][agents.select_as_issue][0] * links.aware * actionWeight

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									state_grade = links.conflict_level[0][agents.select_as_issue][0] * links.aware * actionWeight * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									state_grade = links.conflict_level[0][agents.select_as_issue][0] * links.aware * actionWeight * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									state_grade = links.conflict_level[0][agents.select_as_issue][0] * links.aware * actionWeight * affiliation_weights[2]

# 								state_grade_list.append(state_grade)

# 							if links.agent2 == agents:
							
# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									state_grade = links.conflict_level[1][agents.select_as_issue][0] * links.aware * actionWeight

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									state_grade = links.conflict_level[1][agents.select_as_issue][0] * links.aware * actionWeight * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									state_grade = links.conflict_level[1][agents.select_as_issue][0] * links.aware * actionWeight * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									state_grade = links.conflict_level[1][agents.select_as_issue][0] * links.aware * actionWeight * affiliation_weights[2]
							
# 								state_grade_list.append(state_grade)

# 					# If the link has a negative awareness, set the grade of the action to 0
# 					else:
# 						# Check that only the link of interest is selected
# 						if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 							state_grade_list.append(0)

# 			total_agent_grades.append(sum(state_grade_list))

# 			# For the aim on the selected issue
# 			aim_grade_list = []
# 			# Going through all active agents
# 			for agent_inspected in agent_action_list:
# 				for links in link_list:
# 					# Check that the list has an awareness level
# 					if links.aware != -1:
# 						# Check that only the link of interest is selected
# 						if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:

# 							# Make sure to look at the right direction of the conflict level
# 							if links.agent1 == agents:

# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									aim_grade = links.conflict_level[0][agents.select_as_issue][1] * links.aware * actionWeight

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									aim_grade = links.conflict_level[0][agents.select_as_issue][1] * links.aware * actionWeight * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									aim_grade = links.conflict_level[0][agents.select_as_issue][1] * links.aware * actionWeight * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									aim_grade = links.conflict_level[0][agents.select_as_issue][1] * links.aware * actionWeight * affiliation_weights[2]

# 								aim_grade_list.append(aim_grade)

# 							if links.agent2 == agents:
							
# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									aim_grade = links.conflict_level[1][agents.select_as_issue][1] * links.aware * actionWeight

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									aim_grade = links.conflict_level[1][agents.select_as_issue][1] * links.aware * actionWeight * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									aim_grade = links.conflict_level[1][agents.select_as_issue][1] * links.aware * actionWeight * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									aim_grade = links.conflict_level[1][agents.select_as_issue][1] * links.aware * actionWeight * affiliation_weights[2]
							
# 								aim_grade_list.append(aim_grade)

# 					# If the link has a negative awareness, set the grade of the action to 0
# 					else:
# 						# Check that only the link of interest is selected
# 						if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 							aim_grade_list.append(0)

# 			total_agent_grades.append(sum(aim_grade_list))

# 			####################################
# 			# Select of the best action

# 			best_action = total_agent_grades.index(max(total_agent_grades))

# 			####################################
# 			# Application of the action selected

# 			# Implementation of a causal relation blanket action
# 			if best_action < len(cw_of_interest):
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					# Making sure that the agent does not count itself
# 					if agents != agent_inspected:

# 						# print(' ')
# 						# print('Before: ', agent_inspected.belieftree[0][cw_of_interest[best_action]][0])

# 						# Same affiliation
# 						if agents.affiliation == agent_inspected.affiliation:
# 							agent_inspected.belieftree[0][cw_of_interest[best_action]][0] += (agents.belieftree[0][cw_of_interest[best_action]][0] - agent_inspected.belieftree[0][cw_of_interest[best_action]][0]) * \
# 								agents.resources[0] * 0.1 / action_agent_number
						
# 						# Affiliation 1 and 2
# 						if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 							agent_inspected.belieftree[0][cw_of_interest[best_action]][0] += (agents.belieftree[0][cw_of_interest[best_action]][0] - agent_inspected.belieftree[0][cw_of_interest[best_action]][0]) * \
# 								agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number
						
# 						# Affiliation 1 and 3
# 						if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 							agent_inspected.belieftree[0][cw_of_interest[best_action]][0] += (agents.belieftree[0][cw_of_interest[best_action]][0] - agent_inspected.belieftree[0][cw_of_interest[best_action]][0]) * \
# 								agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
						
# 						# Affiliation 2 and 3
# 						if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 							agent_inspected.belieftree[0][cw_of_interest[best_action]][0] += (agents.belieftree[0][cw_of_interest[best_action]][0] - agent_inspected.belieftree[0][cw_of_interest[best_action]][0]) * \
# 								agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 						# print('After ', agent_inspected.belieftree[0][cw_of_interest[best_action]][0])

# 						# Checks and transfer of partial knowledge
# 						# 1-1 check
# 						agent_inspected.belieftree[0][cw_of_interest[best_action]][0] = self.one_minus_one_check(agent_inspected.belieftree[0][cw_of_interest[best_action]][0])
# 						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 						agents.belieftree[1 + agent_inspected.unique_id][cw_of_interest[best_action]][0] = agent_inspected.belieftree[0][cw_of_interest[best_action]][0] + (random.random()/2) - 0.25
# 						# 1-1 check
# 						agents.belieftree[1 + agent_inspected.unique_id][cw_of_interest[best_action]][0] = self.one_minus_one_check(agents.belieftree[1 + agent_inspected.unique_id][cw_of_interest[best_action]][0])
# 						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 						agent_inspected.belieftree[1 + agents.unique_id][cw_of_interest[best_action]][0] = agents.belieftree[0][cw_of_interest[best_action]][0] + (random.random()/2) - 0.25
# 						# 1-1 check
# 						agent_inspected.belieftree[1 + agents.unique_id][cw_of_interest[best_action]][0] =self.one_minus_one_check(agent_inspected.belieftree[1 + agents.unique_id][cw_of_interest[best_action]][0])

# 			# Implementation of a state influence blanket action
# 			if best_action == len(cw_of_interest):
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					# Making sure that the agent does not count itself
# 					if agents != agent_inspected:

# 						# print(' ')
# 						# print('Before: ', agent_inspected.belieftree[0][agents.select_as_issue][0])

# 						# Same affiliation
# 						if agents.affiliation == agent_inspected.affiliation:
# 							agent_inspected.belieftree[0][agents.select_as_issue][0] += (agents.belieftree[0][agents.select_as_issue][0] - agent_inspected.belieftree[0][agents.select_as_issue][0]) * \
# 								agents.resources[0] * 0.1 / action_agent_number
						
# 						# Affiliation 1 and 2
# 						if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 							agent_inspected.belieftree[0][agents.select_as_issue][0] += (agents.belieftree[0][agents.select_as_issue][0] - agent_inspected.belieftree[0][agents.select_as_issue][0]) * \
# 								agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number
						
# 						# Affiliation 1 and 3
# 						if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 							agent_inspected.belieftree[0][agents.select_as_issue][0] += (agents.belieftree[0][agents.select_as_issue][0] - agent_inspected.belieftree[0][agents.select_as_issue][0]) * \
# 								agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
						
# 						# Affiliation 2 and 3
# 						if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 							agent_inspected.belieftree[0][agents.select_as_issue][0] += (agents.belieftree[0][agents.select_as_issue][0] - agent_inspected.belieftree[0][agents.select_as_issue][0]) * \
# 								agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 						# print('After: ', agent_inspected.belieftree[0][agents.select_as_issue][0])

# 						# Checks and transfer of partial knowledge
# 						# 1-1 check
# 						agent_inspected.belieftree[0][agents.select_as_issue][0] = self.one_minus_one_check(agent_inspected.belieftree[0][agents.select_as_issue][0])
# 						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 						agents.belieftree[1 + agent_inspected.unique_id][agents.select_as_issue][0] = agent_inspected.belieftree[0][agents.select_as_issue][0] + (random.random()/2) - 0.25
# 						# 1-1 check
# 						agents.belieftree[1 + agent_inspected.unique_id][agents.select_as_issue][0] = self.one_minus_one_check(agents.belieftree[1 + agent_inspected.unique_id][agents.select_as_issue][0])
# 						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 						agent_inspected.belieftree[1 + agents.unique_id][agents.select_as_issue][0] = agents.belieftree[0][agents.select_as_issue][0] + (random.random()/2) - 0.25
# 						# 1-1 check
# 						agent_inspected.belieftree[1 + agents.unique_id][agents.select_as_issue][0] = self.one_minus_one_check(agent_inspected.belieftree[1 + agents.unique_id][agents.select_as_issue][0])

# 			# Implementation of a state influence blanket action
# 			if best_action == len(cw_of_interest) + 1:
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					# Making sure that the agent does not count itself
# 					if agents != agent_inspected:

# 						# print(' ')
# 						# print('Before: ', agent_inspected.belieftree[0][agents.select_as_issue][1])

# 						# Same affiliation
# 						if agents.affiliation == agent_inspected.affiliation:
# 							agent_inspected.belieftree[0][agents.select_as_issue][1] += (agents.belieftree[0][agents.select_as_issue][1] - agent_inspected.belieftree[0][agents.select_as_issue][1]) * \
# 								agents.resources[0] * 0.1 / action_agent_number
						
# 						# Affiliation 1 and 2
# 						if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 							agent_inspected.belieftree[0][agents.select_as_issue][1] += (agents.belieftree[0][agents.select_as_issue][1] - agent_inspected.belieftree[0][agents.select_as_issue][1]) * \
# 								agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number
						
# 						# Affiliation 1 and 3
# 						if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 							agent_inspected.belieftree[0][agents.select_as_issue][1] += (agents.belieftree[0][agents.select_as_issue][1] - agent_inspected.belieftree[0][agents.select_as_issue][1]) * \
# 								agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
						
# 						# Affiliation 2 and 3
# 						if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 							agent_inspected.belieftree[0][agents.select_as_issue][1] += (agents.belieftree[0][agents.select_as_issue][1] - agent_inspected.belieftree[0][agents.select_as_issue][1]) * \
# 								agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 						# print('After: ', agent_inspected.belieftree[0][agents.select_as_issue][1])

# 						# Checks and transfer of partial knowledge
# 						# 1-1 check
# 						agent_inspected.belieftree[0][agents.select_as_issue][1] = self.one_minus_one_check(agent_inspected.belieftree[0][agents.select_as_issue][1])
# 						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 						agents.belieftree[1 + agent_inspected.unique_id][agents.select_as_issue][1] = agent_inspected.belieftree[0][agents.select_as_issue][1] + (random.random()/2) - 0.25
# 						# 1-1 check
# 						agents.belieftree[1 + agent_inspected.unique_id][agents.select_as_issue][1] = self.one_minus_one_check(agents.belieftree[1 + agent_inspected.unique_id][agents.select_as_issue][1])
# 						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 						agent_inspected.belieftree[1 + agents.unique_id][agents.select_as_issue][1] = agents.belieftree[0][agents.select_as_issue][1] + (random.random()/2) - 0.25
# 						# 1-1 check
# 						agent_inspected.belieftree[1 + agents.unique_id][agents.select_as_issue][1] = self.one_minus_one_check(agent_inspected.belieftree[1 + agents.unique_id][agents.select_as_issue][1])

# 			# Updating the resources after each action has been implemented
# 			agents.resources_actions -= agents.resources[0] * 0.1

# 		############################################################################################################
# 		# 2. Electorate influence, grading of actions and implementation of the best actions until resources run out 
# 		# 20% of the resources (from actions)

# 		# Making sure that there are enough resources
# 		while agents.resources_actions_EInfluence > 0.001:

# 			actions_EP_grades_EInfluence = []
# 			# FIRST - Calculation of the best option
# 			for issue_num in range(len_PC + len_ML):
# 				actions_EP_grades_EInfluence_ind = []
# 				# Going through all agents that are electorate from the master_list
# 				agents_electorate = []
# 				for agents_run in master_list:
# 					if type(agents_run) == Electorate:
# 						agents_electorate.append(agents_run)

# 				for agents_el in agents_electorate:

# 					# Setting grade to 0 if the external party has no interest in the issue:
# 					if agents.belieftree[0][issue_num][0] == 'No':
# 						issue_num_grade	 = 0 

# 					# Calculate a grade if the external party has an interest in the issue
# 					else:
# 						# Memorising the original belief values
# 						original_belief = [0,0,0]
# 						original_belief[0] = copy.copy(agents_el.belieftree_electorate[issue_num][0])
# 						original_belief[1] = copy.copy(agents_el.belieftree_electorate[issue_num][1])
# 						original_belief[2] = copy.copy(agents_el.belieftree_electorate[issue_num][2])

# 						if agents.affiliation == agents_el.affiliation:
# 							# Perfoming the action
# 							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
# 								* agents.resources[0] * 0.1 / electorate_number
# 							# Update of the preference
# 							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
# 							# Calculation of the new gradec
# 							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

# 						# Affiliation 1 and 2
# 						if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
# 							# Perfoming the action
# 							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
# 								* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number
# 							# Update of the preference
# 							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
# 							# Calculation of the new gradec
# 							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

# 						# Affiliation 1 and 3
# 						if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
# 							# Perfoming the action
# 							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
# 								* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number
# 							# Update of the preference
# 							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
# 							# Calculation of the new gradec
# 							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

# 						# Affiliation 2 and 3
# 						if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
# 							# Perfoming the action
# 							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
# 								* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number
# 							# Update of the preference
# 							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
# 							# Calculation of the new grade
# 							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

# 						# Restoring the initial values
# 						agents_el.belieftree_electorate[issue_num][0] = original_belief[0]
# 						agents_el.belieftree_electorate[issue_num][1] = original_belief[1]
# 						agents_el.belieftree_electorate[issue_num][2] = original_belief[2]


# 						# Re-updating the preference levels
# 						self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)

# 					actions_EP_grades_EInfluence_ind.append(issue_num_grade)

# 				actions_EP_grades_EInfluence.append(sum(actions_EP_grades_EInfluence_ind))

# 			# Choose the action that leads to the minimum amount of difference between the EP and the electorates
# 			best_EInfluence = actions_EP_grades_EInfluence.index(min(actions_EP_grades_EInfluence))
			
# 			# SECOND - Changing the aims of all the agents for the best choice
# 			for agents_el in agents_electorate:


# 				if agents.affiliation == agents_el.affiliation:
# 					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
# 					* agents.resources[0] * 0.1 / electorate_number

# 				# Affiliation 1 and 2
# 				if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
# 					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
# 						* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number

# 					# Affiliation 1 and 3
# 				if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
# 					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
# 						* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number

# 				# Affiliation 2 and 3
# 				if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
# 					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
# 						* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number

# 				# 1-1 check
# 				agents_el.belieftree_electorate[best_EInfluence][1] = self.one_minus_one_check(agents_el.belieftree_electorate[best_EInfluence][1])

# 				# Re-updating the preference levels
# 				self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)

# 			agents.resources_actions_EInfluence -= agents.resources[0] * 0.1
# 			# agents.resources_actions -= agents.resources[0] * 0.1

# 	def external_parties_actions_pf(self, agents, agent_action_list, causalrelation_number, \
# 		affiliation_weights, deep_core, mid_level, secondary, electorate_number, action_agent_number, agenda_as_issue, instruments, master_list, link_list):

# 		"""
# 		The external parties actions function (policy formulation)
# 		===========================

# 		This function is used to perform the different active actions of the
# 		external parties during the policy formulation.

# 		It is split in two main parts:
# 		1. All active actions (blanket framing, blanket state influence and 
# 		blanket aim influence)
# 		2. Electorate influence - on the aims

# 		Note: This function is the same as the agenda setting function but adjusted
# 		for the change of selected issues.

# 		"""

# 		len_PC = len(deep_core)
# 		len_ML = len(mid_level)
# 		len_S = len(secondary)

# 		# Here are the modifications related to the policy formulation
# 		# Looking for the relevant causal relations for the policy formulation
# 		cw_of_interest = []
# 		# We only consider the causal relations related to the issue on the agenda
# 		print(agents.select_pinstrument)
# 		for cw_choice in range(len(secondary)):
# 			# Index explanation - pass all issues, then all causal relations related to the PC-Pr links, then reach the links related to the issue on the agenda
# 			if agents.belieftree[0][len_PC + len_ML + len_S + (len_PC * len_ML) + (agenda_as_issue - len_PC)*len_S + cw_choice][0] \
# 				* instruments[agents.select_pinstrument][cw_choice] != 0:
# 				cw_of_interest.append(len_PC + len_ML + len_S + (len_PC * len_ML) + (agenda_as_issue - len_PC)*len_S + cw_choice)

		
# 		# Looking for the relevant issues for the policy formulation
# 		# That is we choose the secondary issues that are impacted by the policy instrument
# 		# that the agent has selected.
# 		issue_of_interest = []
# 		for issue_choice in range(len(secondary)):
# 			if instruments[agents.select_pinstrument][issue_choice] != 0:
# 				issue_of_interest.append(len_PC + len_ML + issue_choice)

# 		# Assignment of the resources for the two main types of actions:
# 		agents.resources_actions_EInfluence = agents.resources_actions * 0.2


# 		############################################################################################################
# 		# 1. Blanket framing, grading of actions and implementation of the best actions until resources run out 
# 		# 100% of the resources (from actions)

# 		# This will need to be adjusted at a later point
# 		actionWeight = 1

# 		# Making sure that there are enough resources
# 		while agents.resources_actions > 0.001:
			
# 			####################################
# 			# Grading of all the possible actions

# 			total_agent_grades = []

# 			# For the causal relations
# 			for cw in cw_of_interest:
# 				cw_grade_list = []
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					# Going through all of the links
# 					for links in link_list:
# 						# Check that the list has an awareness level
# 						if links.aware != -1:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 								# Make sure to look at the right direction of the conflict level
# 								if links.agent1 == agents:
									
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										cw_grade = links.conflict_level[0][cw][0] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										cw_grade = links.conflict_level[0][cw][0] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										cw_grade = links.conflict_level[0][cw][0] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										cw_grade = links.conflict_level[0][cw][0] * links.aware * actionWeight * affiliation_weights[2]

# 									cw_grade_list.append(cw_grade)

# 								if links.agent2 == agents:
									
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										cw_grade = links.conflict_level[1][cw][0] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										cw_grade = links.conflict_level[1][cw][0] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										cw_grade = links.conflict_level[1][cw][0] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										cw_grade = links.conflict_level[1][cw][0] * links.aware * actionWeight * affiliation_weights[2]
									
# 									cw_grade_list.append(cw_grade)

# 						# If the link has a negative awareness, set the grade of the action to 0
# 						else:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 								cw_grade_list.append(0)

# 				total_agent_grades.append(sum(cw_grade_list))


# 			# For the state on the selected issue

# 			for issue_num in issue_of_interest:
# 				state_grade_list = []
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					for links in link_list:
# 						# Check that the list has an awareness level
# 						if links.aware != -1:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:

# 								# Make sure to look at the right direction of the conflict level
# 								if links.agent1 == agents:
								
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										state_grade = links.conflict_level[0][issue_num][0] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[0][issue_num][0] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[0][issue_num][0] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										state_grade = links.conflict_level[0][issue_num][0] * links.aware * actionWeight * affiliation_weights[2]

# 									state_grade_list.append(state_grade)

# 								if links.agent2 == agents:
								
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										state_grade = links.conflict_level[1][issue_num][0] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[1][issue_num][0] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[1][issue_num][0] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										state_grade = links.conflict_level[1][issue_num][0] * links.aware * actionWeight * affiliation_weights[2]
								
# 									state_grade_list.append(state_grade)

# 						# If the link has a negative awareness, set the grade of the action to 0
# 						else:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 								state_grade_list.append(0)

# 				total_agent_grades.append(sum(state_grade_list))

# 			# For the aim on the selected issue
# 			for issue_num in issue_of_interest:
# 				aim_grade_list = []
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					for links in link_list:
# 						# Check that the list has an awareness level
# 						if links.aware != -1:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:

# 								# Make sure to look at the right direction of the conflict level
# 								if links.agent1 == agents:

# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										aim_grade = links.conflict_level[0][issue_num][1] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[0][issue_num][1] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[0][issue_num][1] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										aim_grade = links.conflict_level[0][issue_num][1] * links.aware * actionWeight * affiliation_weights[2]

# 									aim_grade_list.append(aim_grade)

# 								if links.agent2 == agents:
								
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										aim_grade = links.conflict_level[1][issue_num][1] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[1][issue_num][1] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[1][issue_num][1] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										aim_grade = links.conflict_level[1][issue_num][1] * links.aware * actionWeight * affiliation_weights[2]
								
# 									aim_grade_list.append(aim_grade)

# 						# If the link has a negative awareness, set the grade of the action to 0
# 						else:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 								aim_grade_list.append(0)

# 				total_agent_grades.append(sum(aim_grade_list))

# 			# print(' ')
# 			# print('cw_of_interest ', len(cw_of_interest))
# 			# print('issue_of_interest ', len(issue_of_interest))
# 			# print('total_agent_grades ', len(total_agent_grades))

# 			####################################
# 			# Select of the best action

# 			best_action = total_agent_grades.index(max(total_agent_grades)) 

# 			# print('best_action ', best_action)

# 			####################################
# 			# Application of the action selected

# 			# Implementation of a causal relation blanket action
# 			if best_action < len(cw_of_interest):
# 				# print('Blanket framing action selected')
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					# Making sure that the agent does not count itself
# 					if agents != agent_inspected:

# 						# print(' ')
# 						# print('Before: ', agent_inspected.belieftree[0][cw_of_interest[best_action]][0])

# 						# Same affiliation
# 						if agents.affiliation == agent_inspected.affiliation:
# 							agent_inspected.belieftree[0][cw_of_interest[best_action]][0] += (agents.belieftree[0][cw_of_interest[best_action]][0] - agent_inspected.belieftree[0][cw_of_interest[best_action]][0]) * \
# 							agents.resources[0] * 0.1 / action_agent_number
						
# 						# Affiliation 1 and 2
# 						if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 							agent_inspected.belieftree[0][cw_of_interest[best_action]][0] += (agents.belieftree[0][cw_of_interest[best_action]][0] - agent_inspected.belieftree[0][cw_of_interest[best_action]][0]) * \
# 							agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number
						
# 						# Affiliation 1 and 3
# 						if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 							agent_inspected.belieftree[0][cw_of_interest[best_action]][0] += (agents.belieftree[0][cw_of_interest[best_action]][0] - agent_inspected.belieftree[0][cw_of_interest[best_action]][0]) * \
# 							agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
						
# 						# Affiliation 2 and 3
# 						if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 							agent_inspected.belieftree[0][cw_of_interest[best_action]][0] += (agents.belieftree[0][cw_of_interest[best_action]][0] - agent_inspected.belieftree[0][cw_of_interest[best_action]][0]) * \
# 							agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 						# print('After ', agent_inspected.belieftree[0][cw_of_interest[best_action]][0])

# 						# Checks and transfer of partial knowledge
# 						# 1-1 check
# 						agent_inspected.belieftree[0][cw_of_interest[best_action]][0] = self.one_minus_one_check(agent_inspected.belieftree[0][cw_of_interest[best_action]][0])
# 						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 						agents.belieftree[1 + agent_inspected.unique_id][cw_of_interest[best_action]][0] = agent_inspected.belieftree[0][cw_of_interest[best_action]][0] + (random.random()/2) - 0.25
# 						# 1-1 check
# 						agents.belieftree[1 + agent_inspected.unique_id][cw_of_interest[best_action]][0] = self.one_minus_one_check(agents.belieftree[1 + agent_inspected.unique_id][cw_of_interest[best_action]][0])
# 						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 						agent_inspected.belieftree[1 + agents.unique_id][cw_of_interest[best_action]][0] = agents.belieftree[0][cw_of_interest[best_action]][0] + (random.random()/2) - 0.25
# 						# 1-1 check
# 						agent_inspected.belieftree[1 + agents.unique_id][cw_of_interest[best_action]][0] =self.one_minus_one_check(agent_inspected.belieftree[1 + agents.unique_id][cw_of_interest[best_action]][0])

# 			# Implementation of a state influence blanket action
# 			if best_action >= len(cw_of_interest) and best_action < len(cw_of_interest) + len(issue_of_interest):
# 				# print('Blanket state action selected')
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					# Making sure that the agent does not count itself
# 					if agents != agent_inspected:

# 						# print(' ')
# 						# print('Before: ', agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0])

# 						# Same affiliation
# 						if agents.affiliation == agent_inspected.affiliation:
# 							agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0] += \
# 								(agents.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0] - agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0]) * \
# 								agents.resources[0] * 0.1 / action_agent_number
						
# 						# Affiliation 1 and 2
# 						if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 							agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0] += \
# 								(agents.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0] - agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0]) * \
# 								agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number
						
# 						# Affiliation 1 and 3
# 						if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 							agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0] += \
# 								(agents.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0] - agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0]) * \
# 								agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
						
# 						# Affiliation 2 and 3
# 						if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 							agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0] += \
# 								(agents.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0] - agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0]) * \
# 								agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 						# print('After: ', agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0])

# 						# Checks and transfer of partial knowledge
# 						# 1-1 check
# 						agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0] = self.one_minus_one_check(agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0])
# 						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 						agents.belieftree[1 + agent_inspected.unique_id][issue_of_interest[best_action - len(cw_of_interest)]][0] = \
# 							agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0] + (random.random()/2) - 0.25
# 						# 1-1 check
# 						agents.belieftree[1 + agent_inspected.unique_id][issue_of_interest[best_action - len(cw_of_interest)]][0] = \
# 							self.one_minus_one_check(agents.belieftree[1 + agent_inspected.unique_id][issue_of_interest[best_action - len(cw_of_interest)]][0])
# 						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 						agent_inspected.belieftree[1 + agents.unique_id][issue_of_interest[best_action - len(cw_of_interest)]][0] = \
# 							agents.belieftree[0][issue_of_interest[best_action - len(cw_of_interest)]][0] + (random.random()/2) - 0.25
# 						# 1-1 check
# 						agent_inspected.belieftree[1 + agents.unique_id][issue_of_interest[best_action - len(cw_of_interest)]][0] = \
# 							self.one_minus_one_check(agent_inspected.belieftree[1 + agents.unique_id][issue_of_interest[best_action - len(cw_of_interest)]][0])

# 			# Implementation of a state influence blanket action
# 			if best_action >= len(cw_of_interest) + len(issue_of_interest):
# 				# print('Blanket aim action selected')
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					# Making sure that the agent does not count itself
# 					if agents != agent_inspected:

# 						# print(' ')
# 						# print('Before: ', agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1])

# 						# Same affiliation
# 						if agents.affiliation == agent_inspected.affiliation:
# 							agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1] += \
# 								(agents.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1] - \
# 								agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1]) * \
# 								agents.resources[0] * 0.1 / action_agent_number
						
# 						# Affiliation 1 and 2
# 						if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 							agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1] += \
# 								(agents.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1] - \
# 								agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1]) * \
# 								agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number
						
# 						# Affiliation 1 and 3
# 						if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 							agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1] += \
# 								(agents.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1] - \
# 								agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1]) * \
# 							agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
						
# 						# Affiliation 2 and 3
# 						if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 							agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1] += \
# 								(agents.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1] - \
# 								agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1]) * \
# 								agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 						# print('After: ', agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1])

# 						# Checks and transfer of partial knowledge
# 						# 1-1 check
# 						agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1] = \
# 							self.one_minus_one_check(agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1])
# 						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 						agents.belieftree[1 + agent_inspected.unique_id][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1] = \
# 							agent_inspected.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1] + (random.random()/2) - 0.25
# 						# 1-1 check
# 						agents.belieftree[1 + agent_inspected.unique_id][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1] = \
# 							self.one_minus_one_check(agents.belieftree[1 + agent_inspected.unique_id][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1])
# 						# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 						agent_inspected.belieftree[1 + agents.unique_id][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1] = \
# 							agents.belieftree[0][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1] + (random.random()/2) - 0.25
# 						# 1-1 check
# 						agent_inspected.belieftree[1 + agents.unique_id][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1] = \
# 							self.one_minus_one_check(agent_inspected.belieftree[1 + agents.unique_id][issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)]][1])

# 			# Updating the resources after each action has been implemented
# 			agents.resources_actions -= agents.resources[0] * 0.1


# 		############################################################################################################
# 		# 2. Electorate influence, grading of actions and implementation of the best actions until resources run out 
# 		# 20% of the resources (from actions)

# 		# Making sure that there are enough resources
# 		while agents.resources_actions_EInfluence > 0.001:

# 			actions_EP_grades_EInfluence = []
# 			# FIRST - Calculation of the best option
# 			for issue_num in range(len(issue_of_interest)):
# 				actions_EP_grades_EInfluence_ind = []
# 				# Going through all agents that are electorate from the master_list
# 				agents_electorate = []
# 				for agents_run in master_list:
# 					if type(agents_run) == Electorate:
# 						agents_electorate.append(agents_run)

# 				for agents_el in agents_electorate:

# 					# Setting grade to 0 if the external party has no interest in the issue:
# 					if agents.belieftree[0][issue_of_interest[issue_num]][0] == 'No':
# 						issue_num_grade	 = 0 

# 					# Calculate a grade if the external party has an interest in the issue
# 					else:
# 						if agents.affiliation == agents_el.affiliation:
# 							issue_num_grade = abs((agents.belieftree[0][issue_of_interest[issue_num]][1] - agents_el.belieftree_electorate[issue_of_interest[issue_num]][1]) * \
# 								agents.resources[0] * 0.1 / electorate_number)

# 						# Affiliation 1 and 2
# 						if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
# 							issue_num_grade = abs((agents.belieftree[0][issue_of_interest[issue_num]][1] - agents_el.belieftree_electorate[issue_of_interest[issue_num]][1]) * \
# 								agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number * affiliation_weights[0])

# 						# Affiliation 1 and 3
# 						if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
# 							issue_num_grade = abs((agents.belieftree[0][issue_of_interest[issue_num]][1] - agents_el.belieftree_electorate[issue_of_interest[issue_num]][1]) * \
# 								agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number * affiliation_weights[1])

# 						# Affiliation 2 and 3
# 						if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
# 							issue_num_grade = abs((agents.belieftree[0][issue_of_interest[issue_num]][1] - agents_el.belieftree_electorate[issue_of_interest[issue_num]][1]) * \
# 								agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number )

# 						# Restoring the initial values

# 					actions_EP_grades_EInfluence_ind.append(issue_num_grade)

# 				actions_EP_grades_EInfluence.append(sum(actions_EP_grades_EInfluence_ind))

# 			best_EInfluence = actions_EP_grades_EInfluence.index(max(actions_EP_grades_EInfluence))
			
# 			# SECOND - Changing the aims of all the agents for the best choice
# 			for agents_el in agents_electorate:

# 				if agents.affiliation == agents_el.affiliation:
# 					agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1] += (agents.belieftree[0][issue_of_interest[best_EInfluence]][1] - agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1]) \
# 					* agents.resources[0] * 0.1 / electorate_number

# 				# Affiliation 1 and 2
# 				if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
# 					agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1] += (agents.belieftree[0][issue_of_interest[best_EInfluence]][1] - agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1]) \
# 					* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number

# 					# Affiliation 1 and 3
# 				if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
# 					agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1] += (agents.belieftree[0][issue_of_interest[best_EInfluence]][1] - agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1]) \
# 					* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number

# 				# Affiliation 2 and 3
# 				if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
# 					agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1] += (agents.belieftree[0][issue_of_interest[best_EInfluence]][1] - agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1]) \
# 					* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number

# 				# Check for max and min:
# 				agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1] = self.one_minus_one_check(agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1])

# 			agents.resources_actions_EInfluence -= agents.resources[0] * 0.1

# 	def external_parties_actions_as_3S(self, agents, agent_action_list, causalrelation_number, \
# 		affiliation_weights, deep_core, mid_level, secondary, electorate_number, action_agent_number, master_list, link_list, conflict_level_coef):

# 		"""
# 		The external parties actions function - three streams (agenda setting)
# 		===========================

# 		This function is used to perform the different active actions of the
# 		external parties during the agenda setting.

# 		It is split in two main parts:
# 		1. All active actions (blanket framing, blanket state influence and 
# 		blanket aim influence)
# 		2. Electorate influence - on the aims

# 		Note: This is the same function as the previous one, however it also 
# 		considers that the external parties can choose policies and hence adds
# 		code for the policy related actions.

# 		"""

# 		len_PC = len(deep_core)
# 		len_ML = len(mid_level)
# 		len_S = len(secondary)

# 		# Assignment of the resources for the two main types of actions:
# 		agents.resources_actions_EInfluence = agents.resources_actions * 0.2

# 		############################################################################################################
# 		# 1. Blanket framing, grading of actions and implementation of the best actions until resources run out 
# 		# 100% of the resources (from actions)

# 		# This will need to be adjusted at a later point
# 		actionWeight = 1

# 		cw_of_interest = []
# 		# We only consider the causal relations related to the problem on the agenda
# 		for cw_choice in range(len(deep_core)):
# 				cw_of_interest.append(len_PC + len_ML + len_S + (agents.select_problem_3S_as - len_PC) + cw_choice * len(mid_level))

# 		# If the team is advocating for a problem, the following tasks are completed
# 		if agents.select_issue_3S_as == 'problem':

# 			# Making sure that there are enough resources
# 			while agents.resources_actions > 0.001:

# 				####################################
# 				# Grading of all the possible actions

# 				total_agent_grades = []

# 				# For the causal relations
# 				for cw in cw_of_interest:
# 					cw_grade_list = []
# 					# Going through all active agents
# 					for agent_inspected in agent_action_list:
# 						# Going through all of the links
# 						for links in link_list:
# 							# Check that the list has an awareness level
# 							if links.aware != -1:
# 								# Check that only the link of interest is selected
# 								if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 									# Make sure to look at the right direction of the conflict level
# 									if links.agent1 == agents:
										
# 										# Grade calculation using the likelihood method
# 										# Same affiliation
# 										if links.agent1.affiliation == links.agent2.affiliation:
# 											cw_grade = links.conflict_level[0][cw][0] * links.aware * actionWeight

# 										# Affiliation 1-2
# 										if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 											cw_grade = links.conflict_level[0][cw][0] * links.aware * actionWeight * affiliation_weights[0]

# 										# Affiliation 1-3
# 										if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 											cw_grade = links.conflict_level[0][cw][0] * links.aware * actionWeight * affiliation_weights[1]

# 										# Affiliation 2-3
# 										if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 											cw_grade = links.conflict_level[0][cw][0] * links.aware * actionWeight * affiliation_weights[2]

# 										cw_grade_list.append(cw_grade)

# 									if links.agent2 == agents:
										
# 										# Grade calculation using the likelihood method
# 										# Same affiliation
# 										if links.agent1.affiliation == links.agent2.affiliation:
# 											cw_grade = links.conflict_level[1][cw][0] * links.aware * actionWeight

# 										# Affiliation 1-2
# 										if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 											cw_grade = links.conflict_level[1][cw][0] * links.aware * actionWeight * affiliation_weights[0]

# 										# Affiliation 1-3
# 										if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 											cw_grade = links.conflict_level[1][cw][0] * links.aware * actionWeight * affiliation_weights[1]

# 										# Affiliation 2-3
# 										if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 											cw_grade = links.conflict_level[1][cw][0] * links.aware * actionWeight * affiliation_weights[2]
										
# 										cw_grade_list.append(cw_grade)

# 							# If the link has a negative awareness, set the grade of the action to 0
# 							else:
# 								# Check that only the link of interest is selected
# 								if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 									cw_grade_list.append(0)

# 					total_agent_grades.append(sum(cw_grade_list))

# 				# For the state on the selected issue
# 				state_grade_list = []
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					for links in link_list:
# 						# Check that the list has an awareness level
# 						if links.aware != -1:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:

# 								# Make sure to look at the right direction of the conflict level
# 								if links.agent1 == agents:
								
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										state_grade = links.conflict_level[0][agents.select_problem_3S_as][0] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[0][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[0][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										state_grade = links.conflict_level[0][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[2]

# 									state_grade_list.append(state_grade)

# 								if links.agent2 == agents:
								
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										state_grade = links.conflict_level[1][agents.select_problem_3S_as][0] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[1][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[1][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										state_grade = links.conflict_level[1][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[2]
								
# 									state_grade_list.append(state_grade)

# 						# If the link has a negative awareness, set the grade of the action to 0
# 						else:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 								state_grade_list.append(0)

# 				total_agent_grades.append(sum(state_grade_list))

# 				# For the aim on the selected issue
# 				aim_grade_list = []
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					for links in link_list:
# 						# Check that the list has an awareness level
# 						if links.aware != -1:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:

# 								# Make sure to look at the right direction of the conflict level
# 								if links.agent1 == agents:

# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										aim_grade = links.conflict_level[0][agents.select_problem_3S_as][1] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[0][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[0][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										aim_grade = links.conflict_level[0][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[2]

# 									aim_grade_list.append(aim_grade)

# 								if links.agent2 == agents:
								
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										aim_grade = links.conflict_level[1][agents.select_problem_3S_as][1] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[1][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[1][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										aim_grade = links.conflict_level[1][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[2]
								
# 									aim_grade_list.append(aim_grade)

# 						# If the link has a negative awareness, set the grade of the action to 0
# 						else:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 								aim_grade_list.append(0)

# 				total_agent_grades.append(sum(aim_grade_list))

# 				####################################
# 				# Select of the best action

# 				best_action = total_agent_grades.index(max(total_agent_grades))

# 				####################################
# 				# Application of the action selected

# 				# Implementation of a causal relation blanket action
# 				if best_action < len(cw_of_interest):
# 					# Going through all active agents
# 					for agent_inspected in agent_action_list:
# 						# Making sure that the agent does not count itself
# 						if agents != agent_inspected:

# 							# print(' ')
# 							# print('Before: ', agent_inspected.belieftree[0][cw_of_interest[best_action]][0])

# 							# Same affiliation
# 							if agents.affiliation == agent_inspected.affiliation:
# 								agent_inspected.belieftree[0][cw_of_interest[best_action]][0] += (agents.belieftree[0][cw_of_interest[best_action]][0] - agent_inspected.belieftree[0][cw_of_interest[best_action]][0]) * \
# 									agents.resources[0] * 0.1 / action_agent_number
							
# 							# Affiliation 1 and 2
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][cw_of_interest[best_action]][0] += (agents.belieftree[0][cw_of_interest[best_action]][0] - agent_inspected.belieftree[0][cw_of_interest[best_action]][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number
							
# 							# Affiliation 1 and 3
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][cw_of_interest[best_action]][0] += (agents.belieftree[0][cw_of_interest[best_action]][0] - agent_inspected.belieftree[0][cw_of_interest[best_action]][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
							
# 							# Affiliation 2 and 3
# 							if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 								agent_inspected.belieftree[0][cw_of_interest[best_action]][0] += (agents.belieftree[0][cw_of_interest[best_action]][0] - agent_inspected.belieftree[0][cw_of_interest[best_action]][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 							# print('After ', agent_inspected.belieftree[0][cw_of_interest[best_action]][0])

# 							# Checks and transfer of partial knowledge
# 							# 1-1 check
# 							agent_inspected.belieftree[0][cw_of_interest[best_action]][0] = self.one_minus_one_check(agent_inspected.belieftree[0][cw_of_interest[best_action]][0])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 							agents.belieftree[1 + agent_inspected.unique_id][cw_of_interest[best_action]][0] = agent_inspected.belieftree[0][cw_of_interest[best_action]][0] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agents.belieftree[1 + agent_inspected.unique_id][cw_of_interest[best_action]][0] = self.one_minus_one_check(agents.belieftree[1 + agent_inspected.unique_id][cw_of_interest[best_action]][0])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 							agent_inspected.belieftree[1 + agents.unique_id][cw_of_interest[best_action]][0] = agents.belieftree[0][cw_of_interest[best_action]][0] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agent_inspected.belieftree[1 + agents.unique_id][cw_of_interest[best_action]][0] =self.one_minus_one_check(agent_inspected.belieftree[1 + agents.unique_id][cw_of_interest[best_action]][0])

# 				# Implementation of a state influence blanket action
# 				if best_action == len(cw_of_interest):
# 					# Going through all active agents
# 					for agent_inspected in agent_action_list:
# 						# Making sure that the agent does not count itself
# 						if agents != agent_inspected:

# 							# print(' ')
# 							# print('Before: ', agent_inspected.belieftree[0][agents.select_problem_3S_as][0])

# 							# Same affiliation
# 							if agents.affiliation == agent_inspected.affiliation:
# 								agent_inspected.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - agent_inspected.belieftree[0][agents.select_problem_3S_as][0]) * \
# 									agents.resources[0] * 0.1 / action_agent_number
							
# 							# Affiliation 1 and 2
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - agent_inspected.belieftree[0][agents.select_problem_3S_as][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number
							
# 							# Affiliation 1 and 3
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - agent_inspected.belieftree[0][agents.select_problem_3S_as][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
							
# 							# Affiliation 2 and 3
# 							if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - agent_inspected.belieftree[0][agents.select_problem_3S_as][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 							# print('After: ', agent_inspected.belieftree[0][agents.select_problem_3S_as][0])

# 							# Checks and transfer of partial knowledge
# 							# 1-1 check
# 							agent_inspected.belieftree[0][agents.select_problem_3S_as][0] = self.one_minus_one_check(agent_inspected.belieftree[0][agents.select_problem_3S_as][0])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 							agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_as][0] = agent_inspected.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_as][0] = self.one_minus_one_check(agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_as][0])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 							agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = self.one_minus_one_check(agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

# 				# Implementation of a state influence blanket action
# 				if best_action == len(cw_of_interest) + 1:
# 					# Going through all active agents
# 					for agent_inspected in agent_action_list:
# 						# Making sure that the agent does not count itself
# 						if agents != agent_inspected:

# 							# print(' ')
# 							# print('Before: ', agent_inspected.belieftree[0][agents.select_problem_3S_as][1])

# 							# Same affiliation
# 							if agents.affiliation == agent_inspected.affiliation:
# 								agent_inspected.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - agent_inspected.belieftree[0][agents.select_problem_3S_as][1]) * \
# 									agents.resources[0] * 0.1 / action_agent_number
							
# 							# Affiliation 1 and 2
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - agent_inspected.belieftree[0][agents.select_problem_3S_as][1]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number
							
# 							# Affiliation 1 and 3
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - agent_inspected.belieftree[0][agents.select_problem_3S_as][1]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
							
# 							# Affiliation 2 and 3
# 							if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - agent_inspected.belieftree[0][agents.select_problem_3S_as][1]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 							# print('After: ', agent_inspected.belieftree[0][agents.select_problem_3S_as][1])

# 							# Checks and transfer of partial knowledge
# 							# 1-1 check
# 							agent_inspected.belieftree[0][agents.select_problem_3S_as][1] = self.one_minus_one_check(agent_inspected.belieftree[0][agents.select_problem_3S_as][1])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 							agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_as][1] = agent_inspected.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_as][1] = self.one_minus_one_check(agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_as][1])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 							agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = self.one_minus_one_check(agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])

# 				# Updating the resources after each action has been implemented
# 				agents.resources_actions -= agents.resources[0] * 0.1

# 		# If the team is advocating for a policy, the following tasks are completed
# 		if agents.select_issue_3S_as == 'policy':

# 			# Check the total amount of impacts considered
# 			impact_number = len(agents.belieftree_policy[0][agents.select_policy_3S_as])

# 			# Making sure that there are enough resources
# 			while agents.resources_actions > 0.001:

# 				####################################
# 				# Grading of all the possible actions

# 				total_agent_grades = []

# 				# For the impacts
# 				for impact in range(impact_number):
# 					impact_grade_list = []
# 					# Going through all active agents
# 					for agent_inspected in agent_action_list:
# 						# Going through all of the links
# 						for links in link_list:
# 							# Check that the list has an awareness level
# 							if links.aware != -1:
# 								# Check that only the link of interest is selected
# 								if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:

# 									check_none = 0
# 									if agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] == None:
# 										agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] = 0
# 										check_none = 1

# 									belief_diff = abs(agents.belieftree_policy[0][agents.select_policy_3S_as][impact] - agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact])

# 									if check_none == 1:
# 										agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] = None

# 									if belief_diff <= 0.25:
# 										conflict_level_impact = conflict_level_coef[0]
# 									if belief_diff > 0.25 and belief_diff <= 1.75:
# 										conflict_level_impact = conflict_level_coef[2]
# 									if belief_diff > 1.75:
# 										conflict_level_impact = conflict_level_coef[1]

# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										impact_grade = conflict_level_impact * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[2]

# 									impact_grade_list.append(impact_grade)
										
# 							# If the link has a negative awareness, set the grade of the action to 0
# 							else:
# 								# Check that only the link of interest is selected
# 								if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 									impact_grade_list.append(0)

# 					total_agent_grades.append(sum(impact_grade_list))

# 				# For the state on the selected issue
# 				state_grade_list = []
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					for links in link_list:
# 						# Check that the list has an awareness level
# 						if links.aware != -1:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:

# 								# Make sure to look at the right direction of the conflict level
# 								if links.agent1 == agents:
								
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										state_grade = links.conflict_level[0][agents.select_problem_3S_as][0] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[0][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[0][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										state_grade = links.conflict_level[0][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[2]

# 									state_grade_list.append(state_grade)

# 								if links.agent2 == agents:
								
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										state_grade = links.conflict_level[1][agents.select_problem_3S_as][0] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[1][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[1][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										state_grade = links.conflict_level[1][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[2]
								
# 									state_grade_list.append(state_grade)

# 						# If the link has a negative awareness, set the grade of the action to 0
# 						else:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 								state_grade_list.append(0)

# 				total_agent_grades.append(sum(state_grade_list))

# 				# For the aim on the selected issue
# 				aim_grade_list = []
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					for links in link_list:
# 						# Check that the list has an awareness level
# 						if links.aware != -1:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:

# 								# Make sure to look at the right direction of the conflict level
# 								if links.agent1 == agents:

# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										aim_grade = links.conflict_level[0][agents.select_problem_3S_as][1] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[0][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[0][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										aim_grade = links.conflict_level[0][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[2]

# 									aim_grade_list.append(aim_grade)

# 								if links.agent2 == agents:
								
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										aim_grade = links.conflict_level[1][agents.select_problem_3S_as][1] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[1][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[1][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										aim_grade = links.conflict_level[1][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[2]
								
# 									aim_grade_list.append(aim_grade)

# 						# If the link has a negative awareness, set the grade of the action to 0
# 						else:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 								aim_grade_list.append(0)

# 				total_agent_grades.append(sum(aim_grade_list))

# 				####################################
# 				# Select of the best action

# 				best_action = total_agent_grades.index(max(total_agent_grades))

# 				####################################
# 				# Application of the action selected

# 				# Implementation of a causal relation blanket action
# 				if best_action < impact_number:
# 					# Going through all active agents
# 					for agent_inspected in agent_action_list:
# 						# Making sure that the agent does not count itself
# 						if agents != agent_inspected:

# 							# print(' ')
# 							# print('Before: ', agent_inspected.belieftree_policy[0][agents.select_policy_3S_as][best_action]])

# 							# Same affiliation
# 							if agents.affiliation == agent_inspected.affiliation:
# 								agent_inspected.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 									(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - agent_inspected.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 									agents.resources[0] * 0.1 / action_agent_number
							
# 							# Affiliation 1 and 2
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 									(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - agent_inspected.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number

							
# 							# Affiliation 1 and 3
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 									(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - agent_inspected.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
							
# 							# Affiliation 2 and 3
# 							if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 								agent_inspected.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 									(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - agent_inspected.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 							# print('After ', agent_inspected.belieftree_policy[0][agents.select_policy_3S_as][best_action])

# 							# Checks and transfer of partial knowledge
# 							# 1-1 check
# 							agent_inspected.belieftree_policy[0][agents.select_policy_3S_as][best_action] = self.one_minus_one_check(agent_inspected.belieftree_policy[0][agents.select_policy_3S_as][best_action])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 							agents.belieftree_policy[1 + agent_inspected.unique_id][agents.select_policy_3S_as][best_action] = agent_inspected.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agents.belieftree_policy[1 + agent_inspected.unique_id][agents.select_policy_3S_as][best_action] = \
# 								self.one_minus_one_check(agents.belieftree_policy[1 + agent_inspected.unique_id][agents.select_policy_3S_as][best_action])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 							agent_inspected.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = \
# 								agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agent_inspected.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = \
# 								self.one_minus_one_check(agent_inspected.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action])

# 				# Implementation of a state influence blanket action
# 				if best_action == impact_number:
# 					# Going through all active agents
# 					for agent_inspected in agent_action_list:
# 						# Making sure that the agent does not count itself
# 						if agents != agent_inspected:

# 							# print(' ')
# 							# print('Before: ', agent_inspected.belieftree[0][agents.select_problem_3S_as][0])

# 							# Same affiliation
# 							if agents.affiliation == agent_inspected.affiliation:
# 								agent_inspected.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - agent_inspected.belieftree[0][agents.select_problem_3S_as][0]) * \
# 									agents.resources[0] * 0.1 / action_agent_number
							
# 							# Affiliation 1 and 2
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - agent_inspected.belieftree[0][agents.select_problem_3S_as][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number
							
# 							# Affiliation 1 and 3
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - agent_inspected.belieftree[0][agents.select_problem_3S_as][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
							
# 							# Affiliation 2 and 3
# 							if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - agent_inspected.belieftree[0][agents.select_problem_3S_as][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 							# print('After: ', agent_inspected.belieftree[0][agents.select_problem_3S_as][0])

# 							# Checks and transfer of partial knowledge
# 							# 1-1 check
# 							agent_inspected.belieftree[0][agents.select_problem_3S_as][0] = self.one_minus_one_check(agent_inspected.belieftree[0][agents.select_problem_3S_as][0])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 							agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_as][0] = agent_inspected.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_as][0] = self.one_minus_one_check(agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_as][0])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 							agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = self.one_minus_one_check(agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

# 				# Implementation of a state influence blanket action
# 				if best_action == impact_number + 1:
# 					# Going through all active agents
# 					for agent_inspected in agent_action_list:
# 						# Making sure that the agent does not count itself
# 						if agents != agent_inspected:

# 							# print(' ')
# 							# print('Before: ', agent_inspected.belieftree[0][agents.select_problem_3S_as][1])

# 							# Same affiliation
# 							if agents.affiliation == agent_inspected.affiliation:
# 								agent_inspected.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - agent_inspected.belieftree[0][agents.select_problem_3S_as][1]) * \
# 									agents.resources[0] * 0.1 / action_agent_number
							
# 							# Affiliation 1 and 2
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - agent_inspected.belieftree[0][agents.select_problem_3S_as][1]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number
							
# 							# Affiliation 1 and 3
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - agent_inspected.belieftree[0][agents.select_problem_3S_as][1]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
							
# 							# Affiliation 2 and 3
# 							if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - agent_inspected.belieftree[0][agents.select_problem_3S_as][1]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 							# print('After: ', agent_inspected.belieftree[0][agents.select_problem_3S_as][1])

# 							# Checks and transfer of partial knowledge
# 							# 1-1 check
# 							agent_inspected.belieftree[0][agents.select_problem_3S_as][1] = self.one_minus_one_check(agent_inspected.belieftree[0][agents.select_problem_3S_as][1])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 							agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_as][1] = agent_inspected.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_as][1] = self.one_minus_one_check(agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_as][1])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 							agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = self.one_minus_one_check(agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])

# 				# Updating the resources after each action has been implemented
# 				agents.resources_actions -= agents.resources[0] * 0.1

# 		############################################################################################################
# 		# 2. Electorate influence, grading of actions and implementation of the best actions until resources run out 
# 		# 20% of the resources (from actions)
# 		while agents.resources_actions_EInfluence > 0.001:
# 			actions_EP_grades_EInfluence = []
# 			# FIRST - Calculation of the best option
# 			for issue_num in range(len_PC + len_ML):
# 				actions_EP_grades_EInfluence_ind = []
# 				# Going through all agents that are electorate from the master_list
# 				agents_electorate = []
# 				for agents_run in master_list:
# 					if type(agents) == Electorate:
# 						agents_electorate.append(agents_run)

# 				for agents_el in agents_electorate:

# 					# Setting grade to 0 if the external party has no interest in the issue:
# 					if agents.belieftree[0][issue_num][0] == 'No':
# 						issue_num_grade	 = 0 

# 					# Calculate a grade if the external party has an interest in the issue
# 					else:

# 						# Memorising the original belief values
# 						original_belief = [0,0,0]
# 						original_belief[0] = copy.copy(agents_el.belieftree_electorate[issue_num][0])
# 						original_belief[1] = copy.copy(agents_el.belieftree_electorate[issue_num][1])
# 						original_belief[2] = copy.copy(agents_el.belieftree_electorate[issue_num][2])

# 						if agents.affiliation == agents_el.affiliation:
# 							# Perfoming the action
# 							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
# 								* agents.resources[0] * 0.1 / electorate_number
# 							# Update of the preference
# 							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
# 							# Calculation of the new gradec
# 							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

# 						# Affiliation 1 and 2
# 						if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
# 							# Perfoming the action
# 							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
# 								* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number
# 							# Update of the preference
# 							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
# 							# Calculation of the new gradec
# 							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

# 						# Affiliation 1 and 3
# 						if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
# 							# Perfoming the action
# 							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
# 								* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number
# 							# Update of the preference
# 							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
# 							# Calculation of the new gradec
# 							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

# 						# Affiliation 2 and 3
# 						if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
# 							# Perfoming the action
# 							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
# 								* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number
# 							# Update of the preference
# 							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
# 							# Calculation of the new grade
# 							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

# 						# Restoring the initial values
# 						agents_el.belieftree_electorate[issue_num][0] = original_belief[0]
# 						agents_el.belieftree_electorate[issue_num][1] = original_belief[1]
# 						agents_el.belieftree_electorate[issue_num][2] = original_belief[2]


# 						# Re-updating the preference levels
# 						self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)

# 					actions_EP_grades_EInfluence_ind.append(issue_num_grade)

# 				actions_EP_grades_EInfluence.append(sum(actions_EP_grades_EInfluence_ind))

# 			# Choose the action that leads to the minimum amount of difference between the EP and the electorates
# 			best_EInfluence = actions_EP_grades_EInfluence.index(min(actions_EP_grades_EInfluence))
			
# 			# SECOND - Changing the aims of all the agents for the best choice
# 			for agents_el in agents_electorate:

# 				if agents.affiliation == agents_el.affiliation:
# 					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
# 					* agents.resources[0] * 0.1 / electorate_number

# 				# Affiliation 1 and 2
# 				if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
# 					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
# 					* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number

# 					# Affiliation 1 and 3
# 				if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
# 					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
# 					* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number

# 				# Affiliation 2 and 3
# 				if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
# 					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
# 					* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number

# 				# 1-1 check
# 				agents_el.belieftree_electorate[best_EInfluence][1] = \
# 					self.one_minus_one_check(agents_el.belieftree_electorate[best_EInfluence][1])

# 				# Re-updating the preference levels
# 				self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)

# 			agents.resources_actions_EInfluence -= agents.resources[0] * 0.1

# 	def external_parties_actions_pf_3S(self, agents, agent_action_list, causalrelation_number, \
# 		affiliation_weights, deep_core, mid_level, secondary, electorate_number, action_agent_number, master_list, agenda_prob_3S_as, link_list, conflict_level_coef):

# 		"""
# 		The external parties actions function - three streams (policy formulation)
# 		===========================

# 		This function is used to perform the different active actions of the
# 		external parties during the policy formulation.

# 		It is split in two main parts:
# 		1. All active actions (blanket framing, blanket state influence and 
# 		blanket aim influence)
# 		2. Electorate influence - on the aims

# 		Note: This is the same function as the previous one, however it also 
# 		considers that the external parties can choose policies and hence adds
# 		code for the policy related actions.

# 		Note2: This function is the same as the agenda setting function but adjusted
# 		for the change of selected issues.

# 		"""

# 		len_PC = len(deep_core)
# 		len_ML = len(mid_level)
# 		len_S = len(secondary)

# 		# Assignment of the resources for the two main types of actions:
# 		agents.resources_actions_EInfluence = agents.resources_actions * 0.2

# 		############################################################################################################
# 		# 1. Blanket framing, grading of actions and implementation of the best actions until resources run out 
# 		# 100% of the resources (from actions)

# 		# This will need to be adjusted at a later point
# 		actionWeight = 1

# 		# Selection of the cw of interest
# 		cw_of_interest = []
# 		# Select one by one the Pr
# 		j = agenda_prob_3S_as
# 		# for j in range(len_ML):
# 		# Selecting the causal relations starting from Pr
# 		for k in range(len_S):
# 			# Contingency for partial knowledge issues
# 			# print(len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML)
# 			if (agents.belieftree[0][len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML][0] < 0 and (agents.belieftree[0][j][1] - agents.belieftree[0][j][0]) < 0) \
# 			  or (agents.belieftree[0][len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML][0] > 0 and (agents.belieftree[0][j][1] - agents.belieftree[0][j][0]) > 0):
# 				cw_of_interest.append(len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML)
		

# 		# If the team is advocating for a problem, the following tasks are completed
# 		if agents.select_issue_3S_pf == 'problem':

# 			# Making sure that there are enough resources
# 			while agents.resources_actions > 0.001:

# 				####################################
# 				# Grading of all the possible actions

# 				total_agent_grades = []

# 				# For the causal relations
# 				for cw in cw_of_interest:
# 					cw_grade_list = []
# 					# Going through all active agents
# 					for agent_inspected in agent_action_list:
# 						# Going through all of the links
# 						for links in link_list:
# 							# Check that the list has an awareness level
# 							if links.aware != -1:
# 								# Check that only the link of interest is selected
# 								if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 									# Make sure to look at the right direction of the conflict level
# 									if links.agent1 == agents:
										
# 										# Grade calculation using the likelihood method
# 										# Same affiliation
# 										if links.agent1.affiliation == links.agent2.affiliation:
# 											cw_grade = links.conflict_level[0][cw][0] * links.aware * actionWeight

# 										# Affiliation 1-2
# 										if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 											cw_grade = links.conflict_level[0][cw][0] * links.aware * actionWeight * affiliation_weights[0]

# 										# Affiliation 1-3
# 										if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 											cw_grade = links.conflict_level[0][cw][0] * links.aware * actionWeight * affiliation_weights[1]

# 										# Affiliation 2-3
# 										if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 											cw_grade = links.conflict_level[0][cw][0] * links.aware * actionWeight * affiliation_weights[2]

# 										cw_grade_list.append(cw_grade)

# 									if links.agent2 == agents:
										
# 										# Grade calculation using the likelihood method
# 										# Same affiliation
# 										if links.agent1.affiliation == links.agent2.affiliation:
# 											cw_grade = links.conflict_level[1][cw][0] * links.aware * actionWeight

# 										# Affiliation 1-2
# 										if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 											cw_grade = links.conflict_level[1][cw][0] * links.aware * actionWeight * affiliation_weights[0]

# 										# Affiliation 1-3
# 										if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 											cw_grade = links.conflict_level[1][cw][0] * links.aware * actionWeight * affiliation_weights[1]

# 										# Affiliation 2-3
# 										if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 											cw_grade = links.conflict_level[1][cw][0] * links.aware * actionWeight * affiliation_weights[2]
										
# 										cw_grade_list.append(cw_grade)

# 							# If the link has a negative awareness, set the grade of the action to 0
# 							else:
# 								# Check that only the link of interest is selected
# 								if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 									cw_grade_list.append(0)

# 					total_agent_grades.append(sum(cw_grade_list))

# 				# For the state on the selected issue
# 				state_grade_list = []
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					for links in link_list:
# 						# Check that the list has an awareness level
# 						if links.aware != -1:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:

# 								# Make sure to look at the right direction of the conflict level
# 								if links.agent1 == agents:
								
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										state_grade = links.conflict_level[0][agents.select_problem_3S_pf][0] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[0][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[0][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										state_grade = links.conflict_level[0][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[2]

# 									state_grade_list.append(state_grade)

# 								if links.agent2 == agents:
								
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										state_grade = links.conflict_level[1][agents.select_problem_3S_pf][0] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[1][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[1][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										state_grade = links.conflict_level[1][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[2]
								
# 									state_grade_list.append(state_grade)

# 						# If the link has a negative awareness, set the grade of the action to 0
# 						else:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 								state_grade_list.append(0)

# 				total_agent_grades.append(sum(state_grade_list))

# 				# For the aim on the selected issue
# 				aim_grade_list = []
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					for links in link_list:
# 						# Check that the list has an awareness level
# 						if links.aware != -1:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:

# 								# Make sure to look at the right direction of the conflict level
# 								if links.agent1 == agents:

# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										aim_grade = links.conflict_level[0][agents.select_problem_3S_pf][1] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[0][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[0][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										aim_grade = links.conflict_level[0][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[2]

# 									aim_grade_list.append(aim_grade)

# 								if links.agent2 == agents:
								
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										aim_grade = links.conflict_level[1][agents.select_problem_3S_pf][1] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[1][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[1][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										aim_grade = links.conflict_level[1][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[2]
								
# 									aim_grade_list.append(aim_grade)

# 						# If the link has a negative awareness, set the grade of the action to 0
# 						else:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 								aim_grade_list.append(0)

# 				total_agent_grades.append(sum(aim_grade_list))

# 				####################################
# 				# Select of the best action

# 				best_action = total_agent_grades.index(max(total_agent_grades))

# 				####################################
# 				# Application of the action selected

# 				# Implementation of a causal relation blanket action
# 				if best_action < len(cw_of_interest):
# 					# Going through all active agents
# 					for agent_inspected in agent_action_list:
# 						# Making sure that the agent does not count itself
# 						if agents != agent_inspected:

# 							# print(' ')
# 							# print('Before: ', agent_inspected.belieftree[0][cw_of_interest[best_action]][0])

# 							# Same affiliation
# 							if agents.affiliation == agent_inspected.affiliation:
# 								agent_inspected.belieftree[0][cw_of_interest[best_action]][0] += (agents.belieftree[0][cw_of_interest[best_action]][0] - agent_inspected.belieftree[0][cw_of_interest[best_action]][0]) * \
# 									agents.resources[0] * 0.1 / action_agent_number
							
# 							# Affiliation 1 and 2
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][cw_of_interest[best_action]][0] += (agents.belieftree[0][cw_of_interest[best_action]][0] - agent_inspected.belieftree[0][cw_of_interest[best_action]][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number
							
# 							# Affiliation 1 and 3
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][cw_of_interest[best_action]][0] += (agents.belieftree[0][cw_of_interest[best_action]][0] - agent_inspected.belieftree[0][cw_of_interest[best_action]][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
							
# 							# Affiliation 2 and 3
# 							if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 								agent_inspected.belieftree[0][cw_of_interest[best_action]][0] += (agents.belieftree[0][cw_of_interest[best_action]][0] - agent_inspected.belieftree[0][cw_of_interest[best_action]][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 							# print('After ', agent_inspected.belieftree[0][cw_of_interest[best_action]][0])

# 							# Checks and transfer of partial knowledge
# 							# 1-1 check
# 							agent_inspected.belieftree[0][cw_of_interest[best_action]][0] = self.one_minus_one_check(agent_inspected.belieftree[0][cw_of_interest[best_action]][0])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 							agents.belieftree[1 + agent_inspected.unique_id][cw_of_interest[best_action]][0] = agent_inspected.belieftree[0][cw_of_interest[best_action]][0] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agents.belieftree[1 + agent_inspected.unique_id][cw_of_interest[best_action]][0] = self.one_minus_one_check(agents.belieftree[1 + agent_inspected.unique_id][cw_of_interest[best_action]][0])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 							agent_inspected.belieftree[1 + agents.unique_id][cw_of_interest[best_action]][0] = agents.belieftree[0][cw_of_interest[best_action]][0] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agent_inspected.belieftree[1 + agents.unique_id][cw_of_interest[best_action]][0] =self.one_minus_one_check(agent_inspected.belieftree[1 + agents.unique_id][cw_of_interest[best_action]][0])

# 				# Implementation of a state influence blanket action
# 				if best_action == len(cw_of_interest):
# 					# Going through all active agents
# 					for agent_inspected in agent_action_list:
# 						# Making sure that the agent does not count itself
# 						if agents != agent_inspected:

# 							# print(' ')
# 							# print('Before: ', agent_inspected.belieftree[0][agents.select_problem_3S_pf][0])

# 							# Same affiliation
# 							if agents.affiliation == agent_inspected.affiliation:
# 								agent_inspected.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - agent_inspected.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 									agents.resources[0] * 0.1 / action_agent_number
							
# 							# Affiliation 1 and 2
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - agent_inspected.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number
							
# 							# Affiliation 1 and 3
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - agent_inspected.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
							
# 							# Affiliation 2 and 3
# 							if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - agent_inspected.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 							# print('After: ', agent_inspected.belieftree[0][agents.select_problem_3S_pf][0])

# 							# Checks and transfer of partial knowledge
# 							# 1-1 check
# 							agent_inspected.belieftree[0][agents.select_problem_3S_pf][0] = self.one_minus_one_check(agent_inspected.belieftree[0][agents.select_problem_3S_pf][0])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 							agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_pf][0] = agent_inspected.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_pf][0] = self.one_minus_one_check(agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_pf][0])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 							agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = self.one_minus_one_check(agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

# 				# Implementation of a state influence blanket action
# 				if best_action == len(cw_of_interest) + 1:
# 					# Going through all active agents
# 					for agent_inspected in agent_action_list:
# 						# Making sure that the agent does not count itself
# 						if agents != agent_inspected:

# 							# print(' ')
# 							# print('Before: ', agent_inspected.belieftree[0][agents.select_problem_3S_pf][1])

# 							# Same affiliation
# 							if agents.affiliation == agent_inspected.affiliation:
# 								agent_inspected.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - agent_inspected.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 									agents.resources[0] * 0.1 / action_agent_number
							
# 							# Affiliation 1 and 2
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - agent_inspected.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number
							
# 							# Affiliation 1 and 3
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - agent_inspected.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
							
# 							# Affiliation 2 and 3
# 							if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - agent_inspected.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 							# print('After: ', agent_inspected.belieftree[0][agents.select_problem_3S_pf][1])

# 							# Checks and transfer of partial knowledge
# 							# 1-1 check
# 							agent_inspected.belieftree[0][agents.select_problem_3S_pf][1] = self.one_minus_one_check(agent_inspected.belieftree[0][agents.select_problem_3S_pf][1])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 							agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_pf][1] = agent_inspected.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_pf][1] = self.one_minus_one_check(agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_pf][1])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 							agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = self.one_minus_one_check(agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])

# 				# Updating the resources after each action has been implemented
# 				agents.resources_actions -= agents.resources[0] * 0.1

# 		# If the team is advocating for a policy, the following tasks are completed
# 		if agents.select_issue_3S_pf == 'policy':

# 			# Check the total amount of impacts considered
# 			impact_number = len(agents.belieftree_instrument[0][agents.select_policy_3S_pf])

# 			# Making sure that there are enough resources
# 			while agents.resources_actions > 0.001:

# 				####################################
# 				# Grading of all the possible actions

# 				total_agent_grades = []

# 				# For the impacts
# 				for impact in range(impact_number):
# 					impact_grade_list = []
# 					# Going through all active agents
# 					for agent_inspected in agent_action_list:
# 						# Going through all of the links
# 						for links in link_list:
# 							# Check that the list has an awareness level
# 							if links.aware != -1:
# 								# Check that only the link of interest is selected
# 								if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:

# 									check_none = 0
# 									if agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] == None:
# 										agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] = 0
# 										check_none = 1

# 									belief_diff = abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][impact] - agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact])

# 									if check_none == 1:
# 										agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] = None

# 									if belief_diff <= 0.25:
# 										conflict_level_impact = conflict_level_coef[0]
# 									if belief_diff > 0.25 and belief_diff <= 1.75:
# 										conflict_level_impact = conflict_level_coef[2]
# 									if belief_diff > 1.75:
# 										conflict_level_impact = conflict_level_coef[1]

# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										impact_grade = conflict_level_impact * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[2]

# 									impact_grade_list.append(impact_grade)
										
# 							# If the link has a negative awareness, set the grade of the action to 0
# 							else:
# 								# Check that only the link of interest is selected
# 								if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 									impact_grade_list.append(0)

# 					total_agent_grades.append(sum(impact_grade_list))

# 				# For the state on the selected issue
# 				state_grade_list = []
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					for links in link_list:
# 						# Check that the list has an awareness level
# 						if links.aware != -1:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:

# 								# Make sure to look at the right direction of the conflict level
# 								if links.agent1 == agents:
								
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										state_grade = links.conflict_level[0][agents.select_problem_3S_pf][0] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[0][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[0][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										state_grade = links.conflict_level[0][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[2]

# 									state_grade_list.append(state_grade)

# 								if links.agent2 == agents:
								
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										state_grade = links.conflict_level[1][agents.select_problem_3S_pf][0] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[1][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										state_grade = links.conflict_level[1][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										state_grade = links.conflict_level[1][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[2]
								
# 									state_grade_list.append(state_grade)

# 						# If the link has a negative awareness, set the grade of the action to 0
# 						else:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 								state_grade_list.append(0)

# 				total_agent_grades.append(sum(state_grade_list))

# 				# For the aim on the selected issue
# 				aim_grade_list = []
# 				# Going through all active agents
# 				for agent_inspected in agent_action_list:
# 					for links in link_list:
# 						# Check that the list has an awareness level
# 						if links.aware != -1:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:

# 								# Make sure to look at the right direction of the conflict level
# 								if links.agent1 == agents:

# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										aim_grade = links.conflict_level[0][agents.select_problem_3S_pf][1] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[0][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[0][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										aim_grade = links.conflict_level[0][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[2]

# 									aim_grade_list.append(aim_grade)

# 								if links.agent2 == agents:
								
# 									# Grade calculation using the likelihood method
# 									# Same affiliation
# 									if links.agent1.affiliation == links.agent2.affiliation:
# 										aim_grade = links.conflict_level[1][agents.select_problem_3S_pf][1] * links.aware * actionWeight

# 									# Affiliation 1-2
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[1][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[0]

# 									# Affiliation 1-3
# 									if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 										aim_grade = links.conflict_level[1][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[1]

# 									# Affiliation 2-3
# 									if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 										aim_grade = links.conflict_level[1][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[2]
								
# 									aim_grade_list.append(aim_grade)

# 						# If the link has a negative awareness, set the grade of the action to 0
# 						else:
# 							# Check that only the link of interest is selected
# 							if links.agent1 == agents and links.agent2 == agent_inspected or links.agent2 == agents and links.agent1 == agent_inspected:
# 								aim_grade_list.append(0)

# 				total_agent_grades.append(sum(aim_grade_list))

# 				####################################
# 				# Select of the best action

# 				best_action = total_agent_grades.index(max(total_agent_grades))

# 				####################################
# 				# Application of the action selected

# 				# Implementation of a causal relation blanket action
# 				if best_action < impact_number:
# 					# Going through all active agents
# 					for agent_inspected in agent_action_list:
# 						# Making sure that the agent does not count itself
# 						if agents != agent_inspected:

# 							# print(' ')
# 							# print('Before: ', agent_inspected.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]])

# 							# Same affiliation
# 							if agents.affiliation == agent_inspected.affiliation:
# 								agent_inspected.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 									(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - agent_inspected.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 									agents.resources[0] * 0.1 / action_agent_number
							
# 							# Affiliation 1 and 2
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 									(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - agent_inspected.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number

							
# 							# Affiliation 1 and 3
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 									(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - agent_inspected.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
							
# 							# Affiliation 2 and 3
# 							if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 								agent_inspected.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 									(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - agent_inspected.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 							# print('After ', agent_inspected.belieftree_instrument[0][agents.select_policy_3S_pf][best_action])

# 							# Checks and transfer of partial knowledge
# 							# 1-1 check
# 							agent_inspected.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] = self.one_minus_one_check(agent_inspected.belieftree_instrument[0][agents.select_policy_3S_pf][best_action])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 							agents.belieftree_instrument[1 + agent_inspected.unique_id][agents.select_policy_3S_pf][best_action] = agent_inspected.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agents.belieftree_instrument[1 + agent_inspected.unique_id][agents.select_policy_3S_pf][best_action] = \
# 								self.one_minus_one_check(agents.belieftree_instrument[1 + agent_inspected.unique_id][agents.select_policy_3S_pf][best_action])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 							agent_inspected.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = \
# 								agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agent_inspected.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = \
# 								self.one_minus_one_check(agent_inspected.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action])

# 				# Implementation of a state influence blanket action
# 				if best_action == impact_number:
# 					# Going through all active agents
# 					for agent_inspected in agent_action_list:
# 						# Making sure that the agent does not count itself
# 						if agents != agent_inspected:

# 							# print(' ')
# 							# print('Before: ', agent_inspected.belieftree[0][agents.select_problem_3S_pf][0])

# 							# Same affiliation
# 							if agents.affiliation == agent_inspected.affiliation:
# 								agent_inspected.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - agent_inspected.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 									agents.resources[0] * 0.1 / action_agent_number
							
# 							# Affiliation 1 and 2
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - agent_inspected.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number
							
# 							# Affiliation 1 and 3
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - agent_inspected.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
							
# 							# Affiliation 2 and 3
# 							if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - agent_inspected.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 							# print('After: ', agent_inspected.belieftree[0][agents.select_problem_3S_pf][0])

# 							# Checks and transfer of partial knowledge
# 							# 1-1 check
# 							agent_inspected.belieftree[0][agents.select_problem_3S_pf][0] = self.one_minus_one_check(agent_inspected.belieftree[0][agents.select_problem_3S_pf][0])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 							agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_pf][0] = agent_inspected.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_pf][0] = self.one_minus_one_check(agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_pf][0])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 							agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = self.one_minus_one_check(agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

# 				# Implementation of a state influence blanket action
# 				if best_action == impact_number + 1:
# 					# Going through all active agents
# 					for agent_inspected in agent_action_list:
# 						# Making sure that the agent does not count itself
# 						if agents != agent_inspected:

# 							# print(' ')
# 							# print('Before: ', agent_inspected.belieftree[0][agents.select_problem_3S_pf][1])

# 							# Same affiliation
# 							if agents.affiliation == agent_inspected.affiliation:
# 								agent_inspected.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - agent_inspected.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 									agents.resources[0] * 0.1 / action_agent_number
							
# 							# Affiliation 1 and 2
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 1) or (agents.affiliation == 1 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - agent_inspected.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[0] / action_agent_number
							
# 							# Affiliation 1 and 3
# 							if (agents.affiliation == 0 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 0):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - agent_inspected.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[1] / action_agent_number
							
# 							# Affiliation 2 and 3
# 							if (agents.affiliation == 1 and agent_inspected.affiliation == 2) or (agents.affiliation == 2 and agent_inspected.affiliation == 1):
# 								agent_inspected.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - agent_inspected.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 									agents.resources[0] * 0.1 * affiliation_weights[2] / action_agent_number

# 							# print('After: ', agent_inspected.belieftree[0][agents.select_problem_3S_pf][1])

# 							# Checks and transfer of partial knowledge
# 							# 1-1 check
# 							agent_inspected.belieftree[0][agents.select_problem_3S_pf][1] = self.one_minus_one_check(agent_inspected.belieftree[0][agents.select_problem_3S_pf][1])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acting agent)
# 							agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_pf][1] = agent_inspected.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_pf][1] = self.one_minus_one_check(agents.belieftree[1 + agent_inspected.unique_id][agents.select_problem_3S_pf][1])
# 							# Providing partial knowledge - Blanket framing - 0.5 range from real value: (Acted upon agent)
# 							agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
# 							# 1-1 check
# 							agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = self.one_minus_one_check(agent_inspected.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])

# 				# Updating the resources after each action has been implemented
# 				agents.resources_actions -= agents.resources[0] * 0.1

# 		############################################################################################################
# 		# 2. Electorate influence, grading of actions and implementation of the best actions until resources run out 
# 		# 20% of the resources (from actions)
# 		while agents.resources_actions_EInfluence > 0.001:
# 				actions_EP_grades_EInfluence = []
# 				# FIRST - Calculation of the best option
# 				for issue_num in range(len_PC + len_ML):
# 					actions_EP_grades_EInfluence_ind = []
# 					# Going through all agents that are electorate from the master_list
# 					agents_electorate = []
# 					for agents_run in master_list:
# 						if type(agents) == Electorate:
# 							agents_electorate.append(agents_run)

# 					for agents_el in agents_electorate:

# 						# Setting grade to 0 if the external party has no interest in the issue:
# 						if agents.belieftree[0][issue_num][0] == 'No':
# 							issue_num_grade	 = 0 

# 						# Calculate a grade if the external party has an interest in the issue
# 						else:

# 							# Memorising the original belief values
# 							original_belief = [0,0,0]
# 							original_belief[0] = copy.copy(agents_el.belieftree_electorate[issue_num][0])
# 							original_belief[1] = copy.copy(agents_el.belieftree_electorate[issue_num][1])
# 							original_belief[2] = copy.copy(agents_el.belieftree_electorate[issue_num][2])

# 							if agents.affiliation == agents_el.affiliation:
# 								# Perfoming the action
# 								agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
# 									* agents.resources[0] * 0.1 / electorate_number
# 								# Update of the preference
# 								self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
# 								# Calculation of the new gradec
# 								issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

# 							# Affiliation 1 and 2
# 							if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
# 								# Perfoming the action
# 								agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
# 									* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number
# 								# Update of the preference
# 								self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
# 								# Calculation of the new gradec
# 								issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

# 							# Affiliation 1 and 3
# 							if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
# 								# Perfoming the action
# 								agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
# 									* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number
# 								# Update of the preference
# 								self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
# 								# Calculation of the new gradec
# 								issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

# 							# Affiliation 2 and 3
# 							if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
# 								# Perfoming the action
# 								agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
# 									* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number
# 								# Update of the preference
# 								self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
# 								# Calculation of the new grade
# 								issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

# 							# Restoring the initial values
# 							agents_el.belieftree_electorate[issue_num][0] = original_belief[0]
# 							agents_el.belieftree_electorate[issue_num][1] = original_belief[1]
# 							agents_el.belieftree_electorate[issue_num][2] = original_belief[2]


# 							# Re-updating the preference levels
# 							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)

# 						actions_EP_grades_EInfluence_ind.append(issue_num_grade)

# 					actions_EP_grades_EInfluence.append(sum(actions_EP_grades_EInfluence_ind))

# 				# Choose the action that leads to the minimum amount of difference between the EP and the electorates
# 				best_EInfluence = actions_EP_grades_EInfluence.index(min(actions_EP_grades_EInfluence))
				
# 				# SECOND - Changing the aims of all the agents for the best choice
# 				for agents_el in agents_electorate:

# 					if agents.affiliation == agents_el.affiliation:
# 						agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
# 						* agents.resources[0] * 0.1 / electorate_number

# 					# Affiliation 1 and 2
# 					if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
# 						agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
# 						* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number

# 						# Affiliation 1 and 3
# 					if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
# 						agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
# 						* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number

# 					# Affiliation 2 and 3
# 					if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
# 						agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
# 						* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number

# 					# 1-1 check
# 					agents_el.belieftree_electorate[best_EInfluence][1] = \
# 						self.one_minus_one_check(agents_el.belieftree_electorate[best_EInfluence][1])

# 					# Re-updating the preference levels
# 					self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)

# 				agents.resources_actions_EInfluence -= agents.resources[0] * 0.1

# 	def preference_udapte_electorate(self, agent, len_PC, len_ML, len_S):

# 		"""
# 		Electorate preference update function
# 		===========================

# 		This function is used to calculate the preferences of the electorate
# 		agents. It is the similar to the function used to calculate the preferences
# 		of the other agents. The main difference is the non inclusion of the 
# 		causal relations (the electorate tree does not have any). Each preference
# 		is therefore calculated based on the state and aim for each level
# 		in the tree.

# 		The calculation of the deep core, policy core and secondary issues 
# 		preferences is performed.c

# 		"""

# 		#####
# 		# Preference calculation for the deep core issues
# 		Pr_denominator = 0
# 		for h in range(len_PC):
# 			Pr_denominator = Pr_denominator + abs(agent.belieftree_electorate[h][1] - agent.belieftree_electorate[h][0])
# 		for i in range(len_PC):
# 			# There are rare occasions where the denominator could be 0
# 			if Pr_denominator != 0:
# 				agent.belieftree_electorate[i][2] = abs(agent.belieftree_electorate[i][1] - agent.belieftree_electorate[i][0]) / Pr_denominator
# 			else:
# 				agent.belieftree_electorate[i][2] = 0

# 		#####
# 		# Preference calculation for the policy core issues
# 		PC_denominator = 0
# 		for h in range(len_ML):
# 			PC_denominator = PC_denominator + abs(agent.belieftree_electorate[len_PC + h][1] - agent.belieftree_electorate[len_PC + h][0])
# 		for i in range(len_ML):
# 			# There are rare occasions where the denominator could be 0
# 			if PC_denominator != 0:
# 				agent.belieftree_electorate[len_PC + i][2] = abs(agent.belieftree_electorate[len_PC + i][1] - agent.belieftree_electorate[len_PC + i][0]) / PC_denominator
# 			else:
# 				agent.belieftree_electorate[len_PC + i][2] = 0

# 		#####
# 		# Preference calculation for the secondary issues
# 		S_denominator = 0
# 		for h in range(len_S):
# 			S_denominator = S_denominator + abs(agent.belieftree_electorate[len_PC + len_ML + h][1] - agent.belieftree_electorate[len_PC + len_ML + h][0])
# 		for i in range(len_S):
# 			# There are rare occasions where the denominator could be 0
# 			if S_denominator != 0:
# 				agent.belieftree_electorate[len_PC + len_ML + i][2] = abs(agent.belieftree_electorate[len_PC + len_ML + i][1] - agent.belieftree_electorate[len_PC + len_ML + i][0]) / S_denominator
# 			else:
# 				agent.belieftree_electorate[len_PC + len_ML + i][2] = 0

# 	def one_minus_one_check(self, to_be_checked_parameter):

# 		"""
# 		One minus one check function
# 		===========================

# 		This function checks that a certain values does not got over one
# 		and does not go below one due to the randomisation.
		
# 		"""

# 		checked_parameter = 0
# 		if to_be_checked_parameter > 1:
# 			checked_parameter = 1
# 		elif to_be_checked_parameter < -1:
# 			checked_parameter = -1
# 		else:
# 			checked_parameter = to_be_checked_parameter
# 		return checked_parameter

# # Creation of the policy maker agents
# class Policymakers(Agent):

# 	def __init__(self, run_number, agent_id, unique_id, pos, network_strategy, affiliation, resources, belieftree, instrument_preferences, belieftree_policy, belieftree_instrument, select_as_issue, select_pinstrument, select_issue_3S_as, \
# 		select_problem_3S_as, select_policy_3S_as, select_issue_3S_pf, select_problem_3S_pf, select_policy_3S_pf, team_as, team_pf, coalition_as, coalition_pf):
# 		# super().__init__(unique_id, model)
# 		self.run_number = run_number
# 		self.agent_id = agent_id
# 		self.pos = pos
# 		self.network_strategy = network_strategy
# 		self.unique_id = unique_id
# 		# self.model = model
# 		self.affiliation = affiliation
# 		self.resources = resources
# 		self.belieftree = belieftree
# 		self.belieftree_policy = belieftree_policy
# 		self.belieftree_instrument = belieftree_instrument
# 		self.instrument_preferences = instrument_preferences
# 		self.select_as_issue = select_as_issue
# 		self.select_pinstrument = select_pinstrument
# 		self.select_issue_3S_as = select_issue_3S_as
# 		self.select_problem_3S_as = select_problem_3S_as
# 		self.select_policy_3S_as = select_policy_3S_as
# 		self.select_issue_3S_pf = select_issue_3S_pf
# 		self.select_problem_3S_pf = select_problem_3S_pf
# 		self.select_policy_3S_pf = select_policy_3S_pf
# 		self.team_as = team_as
# 		self.team_pf = team_pf
# 		self.coalition_as = coalition_as
# 		self.coalition_pf = coalition_pf

# 	# def __str__(self):
# 	# 	return 'POLICYMAKER - Affiliation: ' + str(self.affiliation) + ', Resources: ' + str(self.resources) + \
# 	# 	', Position: [' + str(self.pos[0]) + ',' + str(self.pos[1]) + '], ID: ' + str(self.unique_id) + \
# 	# 	', Problem selected: ' + str(self.select_problem) + ', Policy selected: ' + str(self.select_policy) + \
# 	# 	', Belief tree: ' + str(self.belieftree)

# 	def policymakers_states_update(self, agent, master_list, affiliation_weights):

# 		"""
# 		The policy makers states update function
# 		===========================

# 		This function uses the data from the external parties to update the states of 
# 		the policy makers.

# 		Note: Ultimately, this would need to include the external parties lack of interests
# 		for some of the states.

# 		"""

# 		#' Addition of more than 3 affiliation will lead to unreported errors!')
# 		if len(affiliation_weights) != 3:
# 			print('WARNING - THIS CODE DOESNT WORK FOR MORE OR LESS THAN 3 AFFILIATIONS')

# 		# Defining the external party list along with the truth agent relation
# 		externalparties_list = []
# 		for agents in master_list:
# 			if type(agents) == Truth:
# 				truthagent = agents
# 			if type(agents) == Externalparties:
# 				externalparties_list.append(agents)

# 		# going through the different external parties:
# 		belief_sum_ep = [0 for k in range(len(truthagent.belieftree_truth))]
# 		# print(belief_sum_ep)
# 		for i in range(len(truthagent.belieftree_truth)):
# 			# print('NEW ISSUE! NEW ISSUES!')
# 			# This is used because in some cases, the external parties will have no impact on the agent (None values in the states of the EP)
# 			actual_length_ep = 0
# 			for j in range(len(externalparties_list)):
# 				# This line is added in case the EP has None states
# 				if externalparties_list[j].belieftree[0][i][0] != 'No':
# 					actual_length_ep += 1
# 					# Currently, the state of the policy makers is initialised as being equal to their initial aim:
# 					if agent.belieftree[0][i][0] == None:
# 						# print('Triggered - changed to: ' + str(agent.belieftree[0][i][1]))
# 						agent.belieftree[0][i][0] = agent.belieftree[0][i][1]
# 					# If they have the same affiliation, add without weight
# 					if externalparties_list[j].affiliation == agent.affiliation:
# 						# print('AFFILIATIONS ARE EQUAL')
# 						# print('issue ' + str(i+1) + ': ' + str(externalparties_list[j].belieftree[0][i][0]) +  /
# 						# ' and affiliation: ' + str(externalparties_list[j].affiliation) + '  ' + str(externalparties_list[j].unique_id))
# 						# print('This is the sum: ' + str(belief_sum_ep[i]))
# 						belief_sum_ep[i] = belief_sum_ep[i] + (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0])
# 						# print('The sum is equal to: ' + str(belief_sum_ep))
# 						# print('The change in state belief is equal to: ' + str(belief_sum_ep[i] / len(externalparties_list)))
# 					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 1) or \
# 					   (externalparties_list[j].affiliation == 1 and agent.affiliation == 0):
# 						# print('AFFILIATION 1 AND 2')
# 						belief_sum_ep[i] = belief_sum_ep[i] + \
# 						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[0]
# 					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 2) or \
# 					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 0):
# 						# print('AFFILIATION 1 AND 3')
# 						belief_sum_ep[i] = belief_sum_ep[i] + \
# 						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[1]
# 					if (externalparties_list[j].affiliation == 1 and agent.affiliation == 2) or \
# 					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 1):
# 						# print('AFFILIATION 2 AND 3')
# 						belief_sum_ep[i] = belief_sum_ep[i] + \
# 						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[2]
# 			agent.belieftree[0][i][0] = agent.belieftree[0][i][0] + belief_sum_ep[i] / actual_length_ep
# 			# print('This is issue: ' + str(i+1) + ' and its new value is: ' + str(agent.belieftree[0][i][0]))
# 		# print(agent)

# 	# Simple print with ID
# 	def __str__(self):
# 		return 'Policy maker: ' + str(self.unique_id)

# 	def action_grade_calculator(self, links, issue, parameter, agents, actionWeight, affiliation_weights):

# 		if links.agent1 == agents:
# 			if links.agent1.affiliation == links.agent2.affiliation:
# 				grade = links.conflict_level[0][issue][parameter] * links.aware * actionWeight

# 			# Affiliation 1-2
# 			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 				(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 				grade = links.conflict_level[0][issue][parameter] * links.aware * actionWeight * affiliation_weights[0]

# 			# Affiliation 1-3
# 			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 				(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 				grade = links.conflict_level[0][issue][parameter] * links.aware * actionWeight * affiliation_weights[1]

# 			# Affiliation 2-3
# 			if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 				(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 				grade = links.conflict_level[0][issue][parameter] * links.aware * actionWeight * affiliation_weights[2]

# 		if links.agent2 == agents:
# 			# Grade calculation using the likelihood method
# 			# Same affiliation
# 			if links.agent1.affiliation == links.agent2.affiliation:
# 				grade = links.conflict_level[1][issue][parameter] * links.aware * actionWeight

# 			# Affiliation 1-2
# 			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 				(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 				grade = links.conflict_level[1][issue][parameter] * links.aware * actionWeight * affiliation_weights[0]

# 			# Affiliation 1-3
# 			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 				(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 				grade = links.conflict_level[1][issue][parameter] * links.aware * actionWeight * affiliation_weights[1]

# 			# Affiliation 2-3
# 			if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 				(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 				grade = links.conflict_level[1][issue][parameter] * links.aware * actionWeight * affiliation_weights[2]

# 		return grade

# 	def action_implementor(self, links, issue, parameter, agents, affiliation_weights, resources_weight_action, resources_potency):

# 		if links.agent1 == agents:
			
# 			# print('Before: ', links.agent2.belieftree[0][issue][parameter])

# 			# Same affiliation
# 			if links.agent1.affiliation == links.agent2.affiliation:
# 				links.agent2.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent2.belieftree[0][issue][parameter]) * \
# 					agents.resources[0] * resources_weight_action * resources_potency

# 			# Affiliation 1-2
# 			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 				links.agent2.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent2.belieftree[0][issue][parameter]) * \
# 					agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 			# Affiliation 1-3
# 			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 				links.agent2.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent2.belieftree[0][issue][parameter]) * \
# 					agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 			# Affiliation 2-3
# 			if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 				links.agent2.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent2.belieftree[0][issue][parameter]) * \
# 					agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 			# print('After: ', links.agent2.belieftree[0][issue][parameter])

# 			# Checks and transfer of partial knowledge
# 			# 1-1 check - new value
# 			links.agent2.belieftree[0][issue][parameter] = self.one_minus_one_check(links.agent2.belieftree[0][issue][parameter])
# 			# Partial knowledge 1 with 1-1 check
# 			agents.belieftree[1 + links.agent2.unique_id][issue][parameter] = links.agent2.belieftree[0][issue][parameter] + (random.random()/5) - 0.1
# 			agents.belieftree[1 + links.agent2.unique_id][issue][parameter] = self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][issue][parameter])
# 			# Partial knowledge 2 with 1-1 check
# 			links.agent2.belieftree[1 + agents.unique_id][issue][parameter] = agents.belieftree[0][issue][parameter] + (random.random()/5) - 0.1
# 			links.agent2.belieftree[1 + agents.unique_id][issue][parameter] = self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][issue][parameter])

# 			results = [links.agent2.belieftree[0][issue][parameter], agents.belieftree[1 + links.agent2.unique_id][issue][parameter], links.agent2.belieftree[1 + agents.unique_id][issue][parameter]]

# 		if links.agent2 == agents:

# 			# print('Before: ', links.agent1.belieftree[0][issue][parameter])
			
# 			# Same affiliation
# 			if links.agent1.affiliation == links.agent2.affiliation:
# 				links.agent1.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent1.belieftree[0][issue][parameter]) * \
# 					agents.resources[0] * resources_weight_action * resources_potency

# 			# Affiliation 1-2
# 			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 				links.agent1.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent1.belieftree[0][issue][parameter]) * \
# 					agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 			# Affiliation 1-3
# 			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 				links.agent1.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent1.belieftree[0][issue][parameter]) * \
# 					agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 			# Affiliation 2-3
# 			if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 				links.agent1.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent1.belieftree[0][issue][parameter]) * \
# 					agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 			# print('After: ', links.agent1.belieftree[0][issue][parameter])
			
# 			# Checks and transfer of partial knowledge
# 			# 1-1 check - new value
# 			links.agent1.belieftree[0][issue][parameter] = self.one_minus_one_check(links.agent1.belieftree[0][issue][parameter])
# 			# Partial knowledge 1 with 1-1 check
# 			agents.belieftree[1 + links.agent1.unique_id][issue][parameter] = links.agent1.belieftree[0][issue][parameter] + (random.random()/5) - 0.1
# 			agents.belieftree[1 + links.agent1.unique_id][issue][parameter] = self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][issue][parameter])
# 			# Partial knowledge 2 with 1-1 check
# 			links.agent1.belieftree[1 + agents.unique_id][issue][parameter] = agents.belieftree[0][issue][parameter] + (random.random()/5) - 0.1
# 			links.agent1.belieftree[1 + agents.unique_id][issue][parameter] = self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][issue][parameter])

# 			results = [links.agent1.belieftree[0][issue][parameter], agents.belieftree[1 + links.agent1.unique_id][issue][parameter], links.agent1.belieftree[1 + agents.unique_id][issue][parameter]]
		
# 		return results

# 	def pm_pe_actions_as(self, agents, link_list, deep_core, mid_level, secondary, resources_weight_action, resources_potency, affiliation_weights):

# 		"""
# 		The PEs and PMs actions function (agenda setting)
# 		===========================

# 		This function is used to perform the different active actions of the
# 		policy entrepreneurs and the policy makers during the agenda setting.

# 		The actions that can be performed are framing, influence on states and 
# 		influence on aims. All of the actions are first graded. Then the action
# 		that has the highest grade is selected. Finally, the action selected 
# 		is implemented.

# 		"""

# 		len_PC = len(deep_core)
# 		len_ML = len(mid_level)
# 		len_S = len(secondary)
# 		total_issue_number = len_PC + len_ML + len_S

# 		# Selection of the cw of interest
# 		cw_of_interest = []
# 		# We only consider the causal relations related to the problem on the agenda
# 		for cw_choice in range(len(deep_core)):
# 				cw_of_interest.append(len_PC + len_ML + len_S + (agents.select_as_issue - len_PC) + cw_choice * len(mid_level))

# 		# print(' ')
# 		# print('Causal relations of interest: ' + str(cw_of_interest))

# 		# Making sure there are enough resources
# 		while agents.resources_actions > 0.001:

# 			# Going through all the links in the model
# 			# print(agents)
# 			total_grade_list = []
# 			total_grade_list_links = []
# 			for links in link_list:

# 				# Making sure that the link is attached to the agent and has a aware higher than 0
# 				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
# 					total_grade_list_links.append(links)

# 					# Definition the action weight parameter
# 					if type(links.agent1) == Policymakers or type(links.agent2) == Policymakers:
# 						actionWeight = 1
# 					else:
# 						actionWeight = 0.95
					
# 					# 1. Grading all framing actions:
# 					# Checking through all possible framing - This is all based on partial knowledge!
# 					for cw in cw_of_interest:
# 						cw_grade = self.action_grade_calculator(links, cw, 0, agents, actionWeight, affiliation_weights)
# 						total_grade_list.append(cw_grade)	

# 					# 2. Grading all individual actions - Aim change
# 					aim_grade = self.action_grade_calculator(links, agents.select_as_issue, 1, agents, actionWeight, affiliation_weights)
# 					total_grade_list.append(aim_grade)

# 					# 3. Grading all individual actions - State change
# 					state_grade = self.action_grade_calculator(links, agents.select_as_issue, 0, agents, actionWeight, affiliation_weights)
# 					total_grade_list.append(state_grade)

# 			# print(' ')
# 			# print('Number of actions: ' + str(len(total_grade_list)))
# 			# print(total_grade_list)

# 			# 4. Choosing an action
# 			# Check if several actions have the same grade
# 			min_best_action = min(total_grade_list)
# 			count_min_list = []
# 			count = 0
# 			for item in total_grade_list:
# 				if item == min_best_action:
# 					count_min_list.append(count)
# 				count += 1
# 			# print('List of indexes: ' + str(count_min_list))
# 			# print(' ')

# 			# If there are several grades at the same level, then choose a random action from these grades:
# 			if len(count_min_list) > 1:
# 				best_action_index = random.choice(count_min_list)
# 				# print('Randomly chosen best action: ' + str(best_action_index))
# 			else:
# 				best_action_index = total_grade_list.index(min(total_grade_list))
# 				# print('Not randomly chosen: ' + str(best_action_index))
			
# 			# print(' ')
# 			# print('----- New check for best action ------')
# 			# print('Action value: ' + str(min(total_grade_list)))
# 			# print('Index of the best action: ' + str(best_action_index))
# 			# print('This is the grade of the action: ' + str(total_grade_list[best_action_index]))
# 			# Make sure that we do not take into account the 0 from the list to perform the following calculations
# 			# best_action_index += 1
# 			# print('The total amount of links considered: ' + str(len(total_grade_list_links)))
# 			# print('The number of actions per link considered: ' + str(len(cw_of_interest) + 2))
# 			# print('The total amount of actions considered: ' + str(len(total_grade_list)))
# 			# print('The link for the action is: ' + str(int(best_action_index/(len(cw_of_interest) + 2))))
# 			best_action = best_action_index - (len(cw_of_interest) + 2) * int(best_action_index/(len(cw_of_interest) + 2))
# 			# print('The impacted index is: ' + str(best_action))
# 			# print('The would be index without the +1: ' + str((best_action_index - (len(cw_of_interest) + 2) * int(best_action_index/(len(cw_of_interest) + 2))) - 1))
# 			# print('   ')

# 			# 5. Performing the actual action
# 			# Selecting the link:
# 			for links in link_list:

# 				if links == total_grade_list_links[int(best_action_index/(len(cw_of_interest) + 2))]:
# 					# print(links)

# 					# If the index is in the first part of the list, then the framing action is the best
# 					if best_action <= len(cw_of_interest) -1:					
# 						# print(' ')
# 						# print('Framing action - causal relation')
# 						# print('best_action: ' + str(best_action))
# 						# print('cw_of_interest: ' + str(cw_of_interest))
# 						# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

# 						# To simplify the notations
# 						best_action = cw_of_interest[best_action]

# 						# Update of the aware decay parameter
# 						links.aware_decay = 5

# 						implemented_action = self.action_implementor(links, best_action, 0, agents, affiliation_weights, resources_weight_action, resources_potency)

# 					# If the index is in the second part of the list, then the aim influence action is the best
# 					if best_action == len(cw_of_interest):
# 						# print('Implementing a aim influence action:')
# 						links.aware_decay = 5

# 						implemented_action = self.action_implementor(links, agents.select_as_issue, 1, agents, affiliation_weights, resources_weight_action, resources_potency)

# 					# If the index is in the first part of the list, then the state influence action is the best
# 					if best_action == len(cw_of_interest) + 1:
# 						# print('Implementing a state influence action:')
# 						links.aware_decay = 5
						
# 						implemented_action = self.action_implementor(links, agents.select_as_issue, 0, agents, affiliation_weights, resources_weight_action, resources_potency)

# 			# agents.resources_actions -= agents.resources
# 			agents.resources_actions -= agents.resources[0] * resources_weight_action

# 	def pm_pe_actions_pf(self, agents, link_list, deep_core, mid_level, secondary, causalrelation_number, agenda_as_issue, instruments, resources_weight_action, resources_potency, AS_theory, affiliation_weights):

# 		"""
# 		The PEs and PMs actions function (policy formulation)
# 		===========================

# 		This function is used to perform the different active actions of the
# 		policy entrepreneurs and the policy makers during the policy formulation.

# 		The actions that can be performed are framing, influence on states and 
# 		influence on aims. All of the actions are first graded. Then the action
# 		that has the highest grade is selected. Finally, the action selected 
# 		is implemented.

# 		"""

# 		len_PC = len(deep_core)
# 		len_ML = len(mid_level)
# 		len_S = len(secondary)
# 		total_issue_number = len_PC + len_ML + len_S

# 		# Here are the modifications related to the policy formulation
# 		# Looking for the relevant causal relations for the policy formulation
# 		of_interest = []
# 		cw_of_interest = []
# 		# We only consider the causal relations related to the problem on the agenda
# 		for cw_choice in range(len(secondary)):
# 			if agents.belieftree[0][len_PC + len_ML + len_S + (len_PC * len_ML) + (agenda_as_issue - len_PC)*len_S + cw_choice][0] \
# 				* instruments[agents.select_pinstrument][cw_choice] != 0:
# 				cw_of_interest.append(len_PC + len_ML + len_S + (len_PC * len_ML) + (agenda_as_issue - len_PC)*len_S + cw_choice)
# 		of_interest.append(cw_of_interest)

# 		# Looking for the relevant issues for the policy formulation
# 		issue_of_interest = []
# 		for issue_choice in range(len(secondary)):
# 			if instruments[agents.select_pinstrument][issue_choice] != 0:
# 				issue_of_interest.append(len_PC + len_ML + issue_choice)
# 		of_interest.append(issue_of_interest)

# 		# Making sure there are enough resources
# 		while agents.resources_actions > 0.001:
# 			# Going through all the links in the model
# 			# print(agents)
# 			total_grade_list = []
# 			total_grade_list_links = []
# 			for links in link_list:
				
# 				# Making sure that the link is attached to the agent and has a aware higher than 0
# 				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
# 					total_grade_list_links.append(links)
# 					# Definition the action weight parameter
# 					if type(links.agent1) == Policymakers or type(links.agent2) == Policymakers:
# 						actionWeight = 1
# 					else:
# 						actionWeight = 0.95

# 					# 1. Grading all framing actions:
# 					# Checking through all possible framing - This is all based on partial knowledge!
# 					for cw in cw_of_interest:

# 						# Checking which agent in the link is the original agent
# 						cw_grade = self.action_grade_calculator(links, cw, 0, agents, actionWeight, affiliation_weights)
# 						total_grade_list.append(cw_grade)

# 					# 2. Grading all individual actions - Aim change
# 					# Going though all possible choices of issue
# 					for issue_num in issue_of_interest:

# 						aim_grade = self.action_grade_calculator(links, issue_num, 1, agents, actionWeight, affiliation_weights)
# 						total_grade_list.append(aim_grade)

# 					# 3. Grading all individual actions - State change
# 					# Going though all possible choices of issue
# 					for issue_num in issue_of_interest:

# 						state_grade = self.action_grade_calculator(links, issue_num, 0, agents, actionWeight, affiliation_weights)
# 						total_grade_list.append(state_grade)

# 			# print(' ')
# 			# print(total_grade_list)

# 			# 4. Choosing an action
# 			best_action_index = total_grade_list.index(min(total_grade_list))

# 			# print(' ')
# 			# print('------ New action grade check -------')
# 			# print('Grade length: ' + str(len(total_grade_list)))
# 			# print('Best index: ' + str(best_action_index))
# 			# print('Number of links: ' + str(len(total_grade_list_links)))
# 			# print('Number of grades per link: ' + str(len(cw_of_interest) + 2 * len(issue_of_interest)))
# 			# print('Link for this action: ' + str(int(best_action_index / (len(cw_of_interest) + 2 * len(issue_of_interest) ) )))
			
# 			best_action = best_action_index - ((len(cw_of_interest) + 2 * len(issue_of_interest)) * int(best_action_index / (len(cw_of_interest) + 2 * len(issue_of_interest) ) ))
# 			# print('Best action selected: ' + str(best_action))

# 			best_action = len(cw_of_interest) + len(issue_of_interest) - 1

# 			for links in link_list:

# 				if links == total_grade_list_links[int(best_action_index / (len(cw_of_interest) + 2 * len(issue_of_interest) ) )]:
# 					# print(links)					

# 					# 5. Performing the actual action
# 					# If the index is in the first part of the list, then the framing action is the best
# 					if best_action <= len(cw_of_interest) - 1:

# 						# print(' ')
# 						# print('Framing action - causal relation')
# 						# print('best_action: ' + str(best_action))
# 						# print('of_interest[0]: ' + str(of_interest[0]))
# 						# print('of_interest[0][best_action]: ' + str(of_interest[0][best_action]))

# 						# Update of the aware decay parameter
# 						links.aware_decay = 5

# 						implemented_action = self.action_implementor(links, of_interest[0][best_action], 0, agents, affiliation_weights, resources_weight_action, resources_potency)

# 					# If the index is in the second part of the list, then the aim influence action on the problem is the best
# 					if best_action > len(cw_of_interest) - 1 and best_action < len(cw_of_interest) + len(issue_of_interest) - 1:

# 						# print(' ')
# 						# print('Aim influence action')
# 						# print('best_action: ' + str(best_action))
# 						# print('of_interest[1]: ' + str(of_interest[1]))
# 						# print('of_interest[1][best_action - len(cw_of_interest)]: ' + str(of_interest[1][best_action - len(cw_of_interest)]))
						
# 						# Update of the aware decay parameter
# 						links.aware_decay = 5

# 						implemented_action = self.action_implementor(links, of_interest[1][best_action - len(cw_of_interest)], 1, agents, affiliation_weights, resources_weight_action, resources_potency)

# 					# If the index is in the first part of the list, then the aim influence action on the policy is the best
# 					if best_action >= len(cw_of_interest) + len(issue_of_interest) - 1:

# 						# print(' ')
# 						# print('Aim influence action')
# 						# print('best_action: ' + str(best_action))
# 						# print('of_interest[1]: ' + str(of_interest[1]))
# 						# print('of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]: ' + str(of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]))

# 						# Update of the aware decay parameter
# 						links.aware_decay = 5

# 						implemented_action = self.action_implementor(links, of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)], 0, agents, affiliation_weights, resources_weight_action, resources_potency)

						
# 			# print('Resources left: ' + str(agents.resources_actions))
# 			agents.resources_actions -= agents.resources[0] * resources_weight_action

# 	def pm_pe_actions_as_3S(self, agents, link_list, deep_core, mid_level, secondary, resources_weight_action, resources_potency, affiliation_weights, conflict_level_coef):

# 		"""
# 		The PEs and PMs actions function - three streams (agenda setting)
# 		===========================

# 		This function is used to perform the different active actions of the
# 		policy entrepreneurs and the policy makers during the agenda setting.

# 		The actions that can be performed are framing, influence on states and 
# 		influence on aims. All of the actions are first graded. Then the action
# 		that has the highest grade is selected. Finally, the action selected 
# 		is implemented.

# 		Note: This function is the same as the one presented before for the backbone
# 		backbone+ and ACF. The main difference is the addition of actions related
# 		to the choice of a policy by the agents.

# 		"""

# 		len_PC = len(deep_core)
# 		len_ML = len(mid_level)
# 		len_S = len(secondary)
# 		total_issue_number = len_PC + len_ML + len_S

# 		# Selection of the cw of interest
# 		cw_of_interest = []
# 		# We only consider the causal relations related to the problem selected by the agent
# 		for cw_choice in range(len(deep_core)):
# 				cw_of_interest.append(len_PC + len_ML + len_S + (agents.select_problem_3S_as - len_PC) + cw_choice * len(mid_level))

# 		# Selection of the impact of interest
# 		impact_number = len(agents.belieftree_policy[0][agents.select_policy_3S_as])

# 		# print(' ')
# 		# print('Causal relations of interest: ' + str(cw_of_interest))

# 		# Making sure there are enough resources
# 		while agents.resources_actions > 0.001:

# 			# Going through all the links in the model
# 			# print(agents)
# 			total_grade_list = []
# 			total_grade_list_links = []
# 			for links in link_list:

# 				# Making sure that the link is attached to the agent and has a aware higher than 0
# 				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
# 					total_grade_list_links.append(links)

# 					# Definition the action weight parameter
# 					if type(links.agent1) == Policymakers or type(links.agent2) == Policymakers:
# 						actionWeight = 1
# 					else:
# 						actionWeight = 0.95
					
# 					# 1. Framing on causal relation and policy impacts

# 					# If the agent is advocating or a problem, the following tasks are performed
# 					if agents.select_issue_3S_as == 'problem':
# 						# 1.a. Grading all framing actions on causal relations:
# 						# Checking through all possible framing - This is all based on partial knowledge!
# 						for cw in range(len(cw_of_interest)):

# 							# Checking which agent in the link is the original agent
# 							if links.agent1 == agents:

# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									cw_grade = links.conflict_level[0][total_issue_number + cw][0] * links.aware * actionWeight
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									cw_grade = links.conflict_level[0][total_issue_number + cw][0] * links.aware * actionWeight * affiliation_weights[0]
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									cw_grade = links.conflict_level[0][total_issue_number + cw][0] * links.aware * actionWeight * affiliation_weights[1]
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									cw_grade = links.conflict_level[0][total_issue_number + cw][0] * links.aware * actionWeight * affiliation_weights[2]
# 									total_grade_list.append(cw_grade)					


# 								# # Check if no partial knowledge (initial value)
# 								# check_none = 0
# 								# if agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] == None:
# 								# 	agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = 0
# 								# 	check_none = 1
# 								# # Performing the action
# 								# cw_grade = (agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]) * \
# 								# 	agents.resources[0] * resources_weight_action * links.aware * resources_potency
# 								# # Adding the grade to the grade list
# 								# total_grade_list.append(cw_grade)
# 								# #  Reset to None after finding the grade
# 								# if check_none == 1:
# 								# 	agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = None

# 							# Checking which agent in the link is the original agent
# 							if links.agent2 == agents:
# 								#  Check if no partial knowledge (initial value)
# 								check_none = 0
# 								if agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] == None:
# 									agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = 0
# 									check_none = 1
# 								# Performing the action
# 								cw_grade = (agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0]) * \
# 									agents.resources[0] * resources_weight_action * links.aware * resources_potency
# 								# Adding the grade to the grade list
# 								total_grade_list.append(cw_grade)
# 								# Reset to None after finding the grade
# 								if check_none == 1:
# 									agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = None

# 					# If the agent is advocating or a policy, the following tasks are performed
# 					if agents.select_issue_3S_as == 'policy':
# 						# 1.b. Grading all framing actions on policy impacts:

# 						# Checking through all possible framing - This is all based on partial knowledge!
# 						for impact in range(impact_number):

# 							# Checking which agent in the link is the original agent
# 							if links.agent1 == agents:

# 								# Need to calculate the conflict level per impact (to avoid having to create a whole new conflict level array in the links for the policies)
# 								# Note that there is currently a need to check for None partial knowledge

# 								check_none = 0
# 								if agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] == None:
# 									agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] = 0
# 									check_none = 1
 
# 								belief_diff = abs(agents.belieftree_policy[0][agents.select_policy_3S_as][impact] - agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact])

# 								if check_none == 1:
# 									agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] = None

# 								if belief_diff <= 0.25:
# 									conflict_level_impact = conflict_level_coef[0]
# 								if belief_diff > 0.25 and belief_diff <= 1.75:
# 									conflict_level_impact = conflict_level_coef[2]
# 								if belief_diff > 1.75:
# 									conflict_level_impact = conflict_level_coef[1]

# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									impact_grade = conflict_level_impact * links.aware * actionWeight
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[0]
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[1]
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[2]
# 									total_grade_list.append(impact_grade)	

# 								# Check if no partial knowledge (initial value)
# 								# check_none = 0
# 								# if agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] == None:
# 								# 	agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] = 0
# 								# 	check_none = 1
# 								# # Performing the action
# 								# impact_grade = (agents.belieftree_policy[0][agents.select_policy_3S_as][impact] - agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact]) * \
# 								# 	agents.resources[0] * resources_weight_action * links.aware * resources_potency
# 								# # Adding the grade to the grade list
# 								# total_grade_list.append(impact_grade)
# 								# #  Reset to None after finding the grade
# 								# if check_none == 1:
# 								# 	agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] = None

# 							# Checking which agent in the link is the original agent
# 							if links.agent2 == agents:

# 								# Need to calculate the conflict level per impact (to avoid having to create a whole new conflict level array in the links for the policies)
# 								# Note that there is currently a need to check for None partial knowledge

# 								check_none = 0
# 								if agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] == None:
# 									agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] = 0
# 									check_none = 1
								
# 								belief_diff = abs(agents.belieftree_policy[0][agents.select_policy_3S_as][impact] - agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact])

# 								if check_none == 1:
# 									agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] = None

# 								if belief_diff <= 0.25:
# 									conflict_level_impact = conflict_level_coef[0]
# 								if belief_diff > 0.25 and belief_diff <= 1.75:
# 									conflict_level_impact = conflict_level_coef[2]
# 								if belief_diff > 1.75:
# 									conflict_level_impact = conflict_level_coef[1]

# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									impact_grade = conflict_level_impact * links.aware * actionWeight
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[0]
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[1]
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[2]
# 									total_grade_list.append(impact_grade)	


# 								# #  Check if no partial knowledge (initial value)
# 								# check_none = 0
# 								# if agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] == None:
# 								# 	agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] = 0
# 								# 	check_none = 1
# 								# impact_grade = (agents.belieftree_policy[0][agents.select_policy_3S_as][impact] - agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact]) * \
# 								# 	agents.resources[0] * resources_weight_action * links.aware * resources_potency
# 								# # Adding the grade to the grade list
# 								# total_grade_list.append(impact_grade)
# 								# # Reset to None after finding the grade
# 								# if check_none == 1:
# 								# 	agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] = None

# 					# 2. Grading all individual actions - Aim change
# 					if links.agent1 == agents:

# 						# Grade calculation using the likelihood method
# 						# Same affiliation
# 						if links.agent1.affiliation == links.agent2.affiliation:
# 							aim_grade_issue = links.conflict_level[0][agents.select_problem_3S_as][1] * links.aware * actionWeight
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 1-2
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 							(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 							aim_grade_issue = links.conflict_level[0][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[0]
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 1-3
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 							aim_grade_issue = links.conflict_level[0][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[1]
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 2-3
# 						if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 							aim_grade_issue = links.conflict_level[0][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[2]
# 							total_grade_list.append(aim_grade_issue)	

# 						# # Check if no partial knowledge (initial value)
# 						# check_none = 0
# 						# if agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] == None:
# 						# 	agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = 0
# 						# 	check_none = 1
# 						# # Performing the action
# 						# aim_grade_issue = (agents.belieftree[0][agents.select_problem_3S_as][1] - agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1]) * \
# 						# 	agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_problem_3S_as][1] * actionWeight * resources_potency
# 						# #  Reset to None after finding the grade
# 						# if check_none == 1:
# 						# 	agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = None
# 						# # Adding the grade to the grade list
# 						# total_grade_list.append(aim_grade_issue)

# 					if links.agent2 == agents:

# 						# Grade calculation using the likelihood method
# 						# Same affiliation
# 						if links.agent1.affiliation == links.agent2.affiliation:
# 							aim_grade_issue = links.conflict_level[1][agents.select_problem_3S_as][1] * links.aware * actionWeight
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 1-2
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 							(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 							aim_grade_issue = links.conflict_level[1][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[0]
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 1-3
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 							aim_grade_issue = links.conflict_level[1][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[1]
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 2-3
# 						if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 							aim_grade_issue = links.conflict_level[1][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[2]
# 							total_grade_list.append(aim_grade_issue)	

# 						# # Check if no partial knowledge (initial value)
# 						# check_none = 0
# 						# if agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] == None:
# 						# 	agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = 0
# 						# 	check_none = 1
# 						# # Performing the action
# 						# aim_grade_issue = (agents.belieftree[0][agents.select_problem_3S_as][1] - agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1]) * \
# 						# 	agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_problem_3S_as][1] * actionWeight * resources_potency
# 						# #  Reset to None after finding the grade
# 						# if check_none == 1:
# 						# 	agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = None
# 						# # Adding the grade to the grade list
# 						# total_grade_list.append(aim_grade_issue)

# 					# 3. Grading all individual actions - State change
# 					if links.agent1 == agents:

# 						# Grade calculation using the likelihood method
# 						# Same affiliation
# 						if links.agent1.affiliation == links.agent2.affiliation:
# 							state_grade_issue = links.conflict_level[0][agents.select_problem_3S_as][0] * links.aware * actionWeight
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 1-2
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 							(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 							state_grade_issue = links.conflict_level[0][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[0]
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 1-3
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 							state_grade_issue = links.conflict_level[0][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[1]
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 2-3
# 						if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 							state_grade_issue = links.conflict_level[0][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[2]
# 							total_grade_list.append(state_grade_issue)	


# 						# # Check if no partial knowledge (initial value)
# 						# check_none = 0
# 						# if agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] == None:
# 						# 	agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = 0
# 						# 	check_none = 1
# 						# # Performing the action
# 						# state_grade_issue = (agents.belieftree[0][agents.select_problem_3S_as][0] - agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0]) * \
# 						# 	agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_problem_3S_as][0] * actionWeight * resources_potency
# 						# #  Reset to None after finding the grade
# 						# if check_none == 1:
# 						# 	agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = None
# 						# # Adding the grade to the grade list
# 						# total_grade_list.append(state_grade_issue)

# 					if links.agent2 == agents:

# 						# Grade calculation using the likelihood method
# 						# Same affiliation
# 						if links.agent1.affiliation == links.agent2.affiliation:
# 							state_grade_issue = links.conflict_level[1][agents.select_problem_3S_as][0] * links.aware * actionWeight
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 1-2
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 							(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 							state_grade_issue = links.conflict_level[1][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[0]
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 1-3
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 							state_grade_issue = links.conflict_level[1][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[1]
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 2-3
# 						if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 							state_grade_issue = links.conflict_level[1][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[2]
# 							total_grade_list.append(state_grade_issue)


# 						# # Check if no partial knowledge (initial value)
# 						# check_none = 0
# 						# if agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] == None:
# 						# 	agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = 0
# 						# 	check_none = 1
# 						# # Performing the action
# 						# state_grade_issue = (agents.belieftree[0][agents.select_problem_3S_as][0] - agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0]) * \
# 						# 	agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_problem_3S_as][0] * actionWeight * resources_potency
# 						# #  Reset to None after finding the grade
# 						# if check_none == 1:
# 						# 	agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = None
# 						# # Adding the grade to the grade list
# 						# total_grade_list.append(state_grade_issue)
# 					# print(' ')

# 			# print(' ')
# 			# print('Number of actions: ' + str(len(total_grade_list)))
# 			# print(total_grade_list)

# 			# 4. Choosing an action

# 			# If the agent is advocating or a problem, the following tasks are performed
# 			if agents.select_issue_3S_as == 'problem':

# 				best_action_index = total_grade_list.index(max(total_grade_list))
# 				agent_best_action = int(best_action_index/(len(cw_of_interest) + 1 + 1))
# 				best_action = best_action_index - (agent_best_action)*(len(cw_of_interest) + 1 + 1)

# 				# print(' ')
# 				# print('----- Considering new action grading (problem) -----')
# 				# print('best_action_index: ' + str(best_action_index))
# 				# print('Number of actions per agent: ' + str(len(cw_of_interest) + 1 + 1))
# 				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
# 				# print('Action to be performed: ' + str(best_action))
# 				# print('Agent performing the action: ' + str(agent_best_action))

# 			# If the agent is advocating or a policy, the following tasks are performed
# 			if agents.select_issue_3S_as == 'policy':
				
# 				best_action_index = total_grade_list.index(max(total_grade_list))
# 				agent_best_action = int(best_action_index/(impact_number + 1 + 1))
# 				best_action = best_action_index - (agent_best_action)*(impact_number + 1 + 1)

# 				# print(' ')
# 				# print('----- Considering new action grading (policy) -----')
# 				# print('best_action_index: ' + str(best_action_index))
# 				# print('Number of actions per agent: ' + str(impact_number + 1 + 1))
# 				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
# 				# print('Action to be performed: ' + str(best_action))
# 				# print('Agent performing the action: ' + str(agent_best_action))


# 			# 5. Performing the actual action
# 			# Selecting the link:
# 			for links in link_list:

# 				# If the agent is advocating or a problem, the following tasks are performed
# 				if agents.select_issue_3S_as == 'problem':

# 					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
# 						# print(links)

# 						# Updating the aware decay parameter
# 						links.aware_decay = 5

# 						# If the index is in the first part of the list, then the framing action is the best
# 						if best_action <= len(cw_of_interest) - 1:
# 							# print(' ')
# 							# print('Performing a causal relation framing action')
# 							# print('best_action: ' + str(best_action))
# 							# print('cw_of_interest: ' + str(cw_of_interest))
# 							# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))
							
# 							# To simplify the notations
# 							best_action = cw_of_interest[best_action]

# 							if links.agent1 == agents:
								
# 								# print('Before: ' + str(links.agent2.belieftree[0][best_action][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][best_action][0]))

# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][best_action][0] = self.one_minus_one_check(links.agent2.belieftree[0][best_action][0])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][best_action][0] = links.agent2.belieftree[0][best_action][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][best_action][0] = self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][best_action][0])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][best_action][0] = self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][best_action][0])

# 								# print(' ')
# 								# print('Causal change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])
# 								# print(agents.belieftree[1 + links.agent2.unique_id][best_action][0])

# 							# Checking which agent in the link is the original agent
# 							if links.agent2 == agents:

# 								# print('Before: ' + str(links.agent1.belieftree[0][best_action][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]
# 								# print('After: ' + str(links.agent1.belieftree[0][best_action][0]))

# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][best_action][0] = self.one_minus_one_check(links.agent1.belieftree[0][best_action][0])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][best_action][0] = links.agent1.belieftree[0][best_action][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][best_action][0] = self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][best_action][0])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][best_action][0] = self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][best_action][0])

# 								# print(' ')
# 								# print('Causal change')
# 								# print(agents.belieftree[1 + links.agent1.unique_id])
# 								# print(agents.belieftree[1 + links.agent1.unique_id][best_action][0])

# 						# If the index is in the second part of the list, then the aim influence action is the best
# 						if best_action == len(cw_of_interest):
# 							# print(' ')
# 							# print('Performing a state change action')
# 							# print('best_action: ' + str(best_action))

# 							if links.agent1 == agents:
# 								# print('Before: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_as][1]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_as][1]))

# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][agents.select_problem_3S_as][1] = self.one_minus_one_check(links.agent2.belieftree[0][agents.select_problem_3S_as][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1]
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])

# 								# print(' ')
# 								# print('Aim change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])

# 							if links.agent2 == agents:

# 								# print('Before: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_as][1]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_as][1]))

# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][agents.select_problem_3S_as][1] = self.one_minus_one_check(links.agent1.belieftree[0][agents.select_problem_3S_as][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1]
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])


# 						# If the index is in the first part of the list, then the state influence action is the best
# 						if best_action == len(cw_of_interest) + 1:
# 							# print(' ')
# 							# print('Performing an aim change action')
# 							# print('best_action: ' + str(best_action))

# 							if links.agent1 == agents:

# 								# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))

# 								# Checks and transfer of partial knowledge
# 								links.agent2.belieftree[0][agents.select_problem_3S_as][0] = self.one_minus_one_check(links.agent2.belieftree[0][agents.select_problem_3S_as][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = links.agent2.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

# 								# print(' ')
# 								# print('State change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])

# 							if links.agent2 == agents:
# 								# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
# 								# 1-1 check
# 								links.agent1.belieftree[0][agents.select_problem_3S_as][0] = self.one_minus_one_check(links.agent1.belieftree[0][agents.select_problem_3S_as][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = links.agent1.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

# 								# print(' ')
# 								# print('State change')
# 								# print(agents.belieftree[1 + links.agent1.unique_id])

# 				# If the agent is advocating or a policy, the following tasks are performed
# 				if agents.select_issue_3S_as == 'policy':
					
# 					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
# 						# print(links)

# 						# Updating the aware decay parameter
# 						links.aware_decay = 5

# 						# If the index is in the first part of the list, then the framing action is the best
# 						if best_action <= impact_number - 1:
# 							# print(' ')
# 							# print('Performing a causal relation framing action')
# 							# print('best_action: ' + str(best_action))
# 							# print('impact_number: ' + str(impact_number))

# 							if links.agent1 == agents:
								
# 								# print('Before: ' + str(links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 										(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 										(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 										(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 										(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] = self.one_minus_one_check(links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
# 								agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][best_action] = links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][best_action] = \
# 									self.one_minus_one_check(agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][best_action])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = \
# 									self.one_minus_one_check(links.agent2.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action])

# 								# print(' ')
# 								# print('Causal change')
# 								# print(agents.belieftree_policy[1 + links.agent2.unique_id])
# 								# print(agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][best_action])

# 							# Checking which agent in the link is the original agent
# 							if links.agent2 == agents:

# 								# print('Before: ' + str(links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 										(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 										(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 										(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 										(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] = self.one_minus_one_check(links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
# 								agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][best_action] = links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][best_action] = \
# 									self.one_minus_one_check(agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][best_action])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = \
# 									self.one_minus_one_check(links.agent1.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action])

# 								# print(' ')
# 								# print('Causal change')
# 								# print(agents.belieftree_policy[1 + links.agent1.unique_id])
# 								# print(agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][best_action])

# 						# If the index is in the second part of the list, then the aim influence action is the best
# 						if best_action == impact_number:
# 							# print(' ')
# 							# print('Performing a state change action')
# 							# print('best_action: ' + str(best_action))

# 							if links.agent1 == agents:

# 								# print('Before: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_as][1]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_as][1]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][agents.select_problem_3S_as][1] = self.one_minus_one_check(links.agent2.belieftree[0][agents.select_problem_3S_as][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1]
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = \
# 									self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = \
# 									self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])

# 								# print(' ')
# 								# print('Aim change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])

# 							if links.agent2 == agents:

# 								# print('Before: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_as][1]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_as][1]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][agents.select_problem_3S_as][1] = self.one_minus_one_check(links.agent1.belieftree[0][agents.select_problem_3S_as][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1]
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = \
# 									self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = \
# 									self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])


# 						# If the index is in the first part of the list, then the state influence action is the best
# 						if best_action == impact_number + 1:
# 							# print(' ')
# 							# print('Performing an aim change action')
# 							# print('best_action: ' + str(best_action))

# 							if links.agent1 == agents:
# 								# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][agents.select_problem_3S_as][0] = self.one_minus_one_check(links.agent2.belieftree[0][agents.select_problem_3S_as][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = links.agent2.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = \
# 									self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = \
# 									self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

# 								# print(' ')
# 								# print('State change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])

# 							if links.agent2 == agents:

# 								# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][agents.select_problem_3S_as][0] = self.one_minus_one_check(links.agent1.belieftree[0][agents.select_problem_3S_as][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = links.agent1.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = \
# 									self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = \
# 									self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

# 								# print(' ')
# 								# print('State change')
# 								# print(agents.belieftree[1 + links.agent1.unique_id])


# 			# agents.resources_actions -= agents.resources
# 			agents.resources_actions -= agents.resources[0] * resources_weight_action

# 	def pm_pe_actions_pf_3S(self, agents, link_list, deep_core, mid_level, secondary, resources_weight_action, resources_potency, agenda_prob_3S_as, affiliation_weights, conflict_level_coef):

# 		"""
# 		The PEs and PMs actions function - three streams (policy formulation)
# 		===========================

# 		This function is used to perform the different active actions of the
# 		policy entrepreneurs and the policy makers during the policy formulation.

# 		The actions that can be performed are framing, influence on states and 
# 		influence on aims. All of the actions are first graded. Then the action
# 		that has the highest grade is selected. Finally, the action selected 
# 		is implemented.

# 		Note: This function is the same as the one presented before for the backbone
# 		backbone+ and ACF. The main difference is the addition of actions related
# 		to the choice of a policy by the agents.

# 		"""

# 		len_PC = len(deep_core)
# 		len_ML = len(mid_level)
# 		len_S = len(secondary)
# 		total_issue_number = len_PC + len_ML + len_S

# 		# Selection of the cw of interest
# 		cw_of_interest = []
# 		# Select one by one the Pr
# 		j = agenda_prob_3S_as
# 		# for j in range(len_ML):
# 		# Selecting the causal relations starting from Pr
# 		for k in range(len_S):
# 			# Contingency for partial knowledge issues
# 			# print(len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML)
# 			if (agents.belieftree[0][len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML][0] < 0 and (agents.belieftree[0][j][1] - agents.belieftree[0][j][0]) < 0) \
# 			  or (agents.belieftree[0][len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML][0] > 0 and (agents.belieftree[0][j][1] - agents.belieftree[0][j][0]) > 0):
# 				cw_of_interest.append(len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML)

# 		# Selection of the impact of interest
# 		impact_number = len(agents.belieftree_instrument[0][agents.select_policy_3S_pf])

# 		# print(' ')
# 		# print('Causal relations of interest: ' + str(cw_of_interest))

# 		# Making sure there are enough resources
# 		while agents.resources_actions > 0.001:

# 			# Going through all the links in the model
# 			# print(agents)
# 			total_grade_list = []
# 			total_grade_list_links = []
# 			for links in link_list:

# 				# Making sure that the link is attached to the agent and has a aware higher than 0
# 				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
# 					total_grade_list_links.append(links)

# 					# Definition the action weight parameter
# 					if type(links.agent1) == Policymakers or type(links.agent2) == Policymakers:
# 						actionWeight = 1
# 					else:
# 						actionWeight = 0.95
					
# 					# 1. Framing on causal relation and policy impacts

# 					# If the agent is advocating or a problem, the following tasks are performed
# 					if agents.select_issue_3S_pf == 'problem':
# 						# 1.a. Grading all framing actions on causal relations:
# 						# Checking through all possible framing - This is all based on partial knowledge!
# 						for cw in range(len(cw_of_interest)):

# 							# Checking which agent in the link is the original agent
# 							if links.agent1 == agents:

# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									cw_grade = links.conflict_level[0][cw_of_interest[cw]][0] * links.aware * actionWeight
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									cw_grade = links.conflict_level[0][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[0]
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									cw_grade = links.conflict_level[0][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[1]
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									cw_grade = links.conflict_level[0][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[2]
# 									total_grade_list.append(cw_grade)	


# 								# # Check if no partial knowledge (initial value)
# 								# check_none = 0
# 								# if agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] == None:
# 								# 	agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = 0
# 								# 	check_none = 1
# 								# # Performing the action
# 								# cw_grade = (agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]) * \
# 								# 	agents.resources[0] * resources_weight_action * links.aware * resources_potency
# 								# # Adding the grade to the grade list
# 								# total_grade_list.append(cw_grade)
# 								# #  Reset to None after finding the grade
# 								# if check_none == 1:
# 								# 	agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = None

# 							# Checking which agent in the link is the original agent
# 							if links.agent2 == agents:

# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									cw_grade = links.conflict_level[1][cw_of_interest[cw]][0] * links.aware * actionWeight
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									cw_grade = links.conflict_level[1][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[0]
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									cw_grade = links.conflict_level[1][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[1]
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									cw_grade = links.conflict_level[1][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[2]
# 									total_grade_list.append(cw_grade)	


# 								# #  Check if no partial knowledge (initial value)
# 								# check_none = 0
# 								# if agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] == None:
# 								# 	agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = 0
# 								# 	check_none = 1
# 								# # Performing the action
# 								# cw_grade = (agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0]) * \
# 								# 	agents.resources[0] * resources_weight_action * links.aware * resources_potency
# 								# # Adding the grade to the grade list
# 								# total_grade_list.append(cw_grade)
# 								# # Reset to None after finding the grade
# 								# if check_none == 1:
# 								# 	agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = None

# 					# If the agent is advocating or a policy, the following tasks are performed
# 					if agents.select_issue_3S_pf == 'policy':
# 						# 1.b. Grading all framing actions on policy impacts:
						
# 						# Checking through all possible framing - This is all based on partial knowledge!
# 						for impact in range(impact_number):

# 							# Checking which agent in the link is the original agent
# 							if links.agent1 == agents:

# 								# Need to calculate the conflict level per impact (to avoid having to create a whole new conflict level array in the links for the policies)
# 								# Note that there is currently a need to check for None partial knowledge

# 								check_none = 0
# 								if agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] == None:
# 									agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] = 0
# 									check_none = 1
 
# 								belief_diff = abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][impact] - agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact])

# 								if check_none == 1:
# 									agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] = None

# 								if belief_diff <= 0.25:
# 									conflict_level_impact = conflict_level_coef[0]
# 								if belief_diff > 0.25 and belief_diff <= 1.75:
# 									conflict_level_impact = conflict_level_coef[2]
# 								if belief_diff > 1.75:
# 									conflict_level_impact = conflict_level_coef[1]

# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									impact_grade = conflict_level_impact * links.aware * actionWeight
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[0]
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[1]
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[2]
# 									total_grade_list.append(impact_grade)	

# 								# # Check if no partial knowledge (initial value)
# 								# check_none = 0
# 								# if agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] == None:
# 								# 	agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] = 0
# 								# 	check_none = 1
# 								# # Performing the action
# 								# impact_grade = (agents.belieftree_instrument[0][agents.select_policy_3S_pf][impact] - agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact]) * \
# 								# 	agents.resources[0] * resources_weight_action * links.aware * resources_potency
# 								# # Adding the grade to the grade list
# 								# total_grade_list.append(impact_grade)
# 								# #  Reset to None after finding the grade
# 								# if check_none == 1:
# 								# 	agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] = None

# 							# Checking which agent in the link is the original agent
# 							if links.agent2 == agents:

# 								# Need to calculate the conflict level per impact (to avoid having to create a whole new conflict level array in the links for the policies)
# 								# Note that there is currently a need to check for None partial knowledge

# 								check_none = 0
# 								if agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] == None:
# 									agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] = 0
# 									check_none = 1
 
# 								belief_diff = abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][impact] - agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact])

# 								if check_none == 1:
# 									agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] = None

# 								if belief_diff <= 0.25:
# 									conflict_level_impact = conflict_level_coef[0]
# 								if belief_diff > 0.25 and belief_diff <= 1.75:
# 									conflict_level_impact = conflict_level_coef[2]
# 								if belief_diff > 1.75:
# 									conflict_level_impact = conflict_level_coef[1]

# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									impact_grade = conflict_level_impact * links.aware * actionWeight
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[0]
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[1]
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[2]
# 									total_grade_list.append(impact_grade)	


# 								# #  Check if no partial knowledge (initial value)
# 								# check_none = 0
# 								# if agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] == None:
# 								# 	agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] = 0
# 								# 	check_none = 1
# 								# impact_grade = (agents.belieftree_instrument[0][agents.select_policy_3S_pf][impact] - agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact]) * \
# 								# 	agents.resources[0] * resources_weight_action * links.aware * resources_potency
# 								# # Adding the grade to the grade list
# 								# total_grade_list.append(impact_grade)
# 								# # Reset to None after finding the grade
# 								# if check_none == 1:
# 								# 	agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] = None

# 					# 2. Grading all individual actions - Aim change
# 					if links.agent1 == agents:

# 						# Grade calculation using the likelihood method
# 						# Same affiliation
# 						if links.agent1.affiliation == links.agent2.affiliation:
# 							aim_grade_issue = links.conflict_level[0][agents.select_problem_3S_pf][1] * links.aware * actionWeight
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 1-2
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 							(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 							aim_grade_issue = links.conflict_level[0][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[0]
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 1-3
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 							aim_grade_issue = links.conflict_level[0][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[1]
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 2-3
# 						if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 							aim_grade_issue = links.conflict_level[0][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[2]
# 							total_grade_list.append(aim_grade_issue)	


# 						# # Check if no partial knowledge (initial value)
# 						# check_none = 0
# 						# if agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] == None:
# 						# 	agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = 0
# 						# 	check_none = 1
# 						# # Performing the action
# 						# aim_grade_issue = (agents.belieftree[0][agents.select_problem_3S_pf][1] - agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1]) * \
# 						# 	agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_problem_3S_pf][1] * actionWeight * resources_potency
# 						# #  Reset to None after finding the grade
# 						# if check_none == 1:
# 						# 	agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = None
# 						# # Adding the grade to the grade list
# 						# total_grade_list.append(aim_grade_issue)

# 					if links.agent2 == agents:

# 						# Grade calculation using the likelihood method
# 						# Same affiliation
# 						if links.agent1.affiliation == links.agent2.affiliation:
# 							aim_grade_issue = links.conflict_level[1][agents.select_problem_3S_pf][1] * links.aware * actionWeight
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 1-2
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 							(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 							aim_grade_issue = links.conflict_level[1][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[0]
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 1-3
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 							aim_grade_issue = links.conflict_level[1][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[1]
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 2-3
# 						if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 							aim_grade_issue = links.conflict_level[1][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[2]
# 							total_grade_list.append(aim_grade_issue)


# 						# # Check if no partial knowledge (initial value)
# 						# check_none = 0
# 						# if agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] == None:
# 						# 	agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = 0
# 						# 	check_none = 1
# 						# # Performing the action
# 						# aim_grade_issue = (agents.belieftree[0][agents.select_problem_3S_pf][1] - agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1]) * \
# 						# 	agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_problem_3S_pf][1] * actionWeight * resources_potency
# 						# #  Reset to None after finding the grade
# 						# if check_none == 1:
# 						# 	agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = None
# 						# # Adding the grade to the grade list
# 						# total_grade_list.append(aim_grade_issue)

# 					# 3. Grading all individual actions - State change
# 					if links.agent1 == agents:

# 						# Grade calculation using the likelihood method
# 						# Same affiliation
# 						if links.agent1.affiliation == links.agent2.affiliation:
# 							state_grade_issue = links.conflict_level[0][agents.select_problem_3S_pf][0] * links.aware * actionWeight
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 1-2
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 							(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 							state_grade_issue = links.conflict_level[0][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[0]
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 1-3
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 							state_grade_issue = links.conflict_level[0][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[1]
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 2-3
# 						if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 							state_grade_issue = links.conflict_level[0][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[2]
# 							total_grade_list.append(state_grade_issue)

# 						# # Check if no partial knowledge (initial value)
# 						# check_none = 0
# 						# if agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] == None:
# 						# 	agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = 0
# 						# 	check_none = 1
# 						# # Performing the action
# 						# state_grade_issue = (agents.belieftree[0][agents.select_problem_3S_pf][0] - agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0]) * \
# 						# 	agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_problem_3S_pf][0] * actionWeight * resources_potency
# 						# #  Reset to None after finding the grade
# 						# if check_none == 1:
# 						# 	agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = None
# 						# # Adding the grade to the grade list
# 						# total_grade_list.append(state_grade_issue)

# 					if links.agent2 == agents:

# 						# Grade calculation using the likelihood method
# 						# Same affiliation
# 						if links.agent1.affiliation == links.agent2.affiliation:
# 							state_grade_issue = links.conflict_level[1][agents.select_problem_3S_pf][0] * links.aware * actionWeight
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 1-2
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 							(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 							state_grade_issue = links.conflict_level[1][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[0]
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 1-3
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 							state_grade_issue = links.conflict_level[1][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[1]
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 2-3
# 						if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 							state_grade_issue = links.conflict_level[1][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[2]
# 							total_grade_list.append(state_grade_issue)


# 						# # Check if no partial knowledge (initial value)
# 						# check_none = 0
# 						# if agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] == None:
# 						# 	agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = 0
# 						# 	check_none = 1
# 						# # Performing the action
# 						# state_grade_issue = (agents.belieftree[0][agents.select_problem_3S_pf][0] - agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0]) * \
# 						# 	agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_problem_3S_pf][0] * actionWeight * resources_potency
# 						# #  Reset to None after finding the grade
# 						# if check_none == 1:
# 						# 	agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = None
# 						# # Adding the grade to the grade list
# 						# total_grade_list.append(state_grade_issue)

# 					# print(' ')


# 			# 4. Choosing an action

# 			# If the agent is advocating or a problem, the following tasks are performed
# 			if agents.select_issue_3S_as == 'problem':

# 				best_action_index = total_grade_list.index(max(total_grade_list))
# 				agent_best_action = int(best_action_index/(len(cw_of_interest) + 1 + 1))
# 				best_action = best_action_index - (agent_best_action)*(len(cw_of_interest) + 1 + 1)

# 				# print(' ')
# 				# print('----- Considering new action grading (problem) -----')
# 				# print('best_action_index: ' + str(best_action_index))
# 				# print('Number of actions per agent: ' + str(len(cw_of_interest) + 1 + 1))
# 				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
# 				# print('Action to be performed: ' + str(best_action))
# 				# print('Agent performing the action: ' + str(agent_best_action))

# 			# If the agent is advocating or a policy, the following tasks are performed
# 			if agents.select_issue_3S_as == 'policy':
				
# 				best_action_index = total_grade_list.index(max(total_grade_list))
# 				agent_best_action = int(best_action_index/(impact_number + 1 + 1))
# 				best_action = best_action_index - (agent_best_action)*(impact_number + 1 + 1)

# 				# print(' ')
# 				# print('----- Considering new action grading (policy) -----')
# 				# print('best_action_index: ' + str(best_action_index))
# 				# print('Number of actions per agent: ' + str(impact_number + 1 + 1))
# 				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
# 				# print('Action to be performed: ' + str(best_action))
# 				# print('Agent performing the action: ' + str(agent_best_action))

# 			# 5. Performing the actual action
# 			# Selecting the link:
# 			for links in link_list:

# 				# If the agent is advocating or a problem, the following tasks are performed
# 				if agents.select_issue_3S_pf == 'problem':

# 					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
# 						# print(links)

# 						# Updating the aware decay parameter
# 						links.aware_decay = 5

# 						# If the index is in the first part of the list, then the framing action is the best
# 						if best_action <= len(cw_of_interest) - 1:
# 							# print(' ')
# 							# print('Performing a causal relation framing action')
# 							# print('best_action: ' + str(best_action))
# 							# print('cw_of_interest: ' + str(cw_of_interest))
# 							# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))
							
# 							# To simplify the notations
# 							best_action = cw_of_interest[best_action]

# 							if links.agent1 == agents:
								
# 								# print('Before: ' + str(links.agent2.belieftree[0][best_action][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]
									
# 								# print('After: ' + str(links.agent2.belieftree[0][best_action][0]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][best_action][0] = self.one_minus_one_check(links.agent2.belieftree[0][best_action][0])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][best_action][0] = links.agent2.belieftree[0][best_action][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][best_action][0] = self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][best_action][0])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][best_action][0] = self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][best_action][0])

# 								# print(' ')
# 								# print('Causal change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])
# 								# print(agents.belieftree[1 + links.agent2.unique_id][best_action][0])

# 							# Checking which agent in the link is the original agent
# 							if links.agent2 == agents:
# 								# print('Before: ' + str(links.agent1.belieftree[0][best_action][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][best_action][0]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][best_action][0] = self.one_minus_one_check(links.agent1.belieftree[0][best_action][0])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][best_action][0] = links.agent1.belieftree[0][best_action][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][best_action][0] = self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][best_action][0])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][best_action][0] = self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][best_action][0])

# 								# print(' ')
# 								# print('Causal change')
# 								# print(agents.belieftree[1 + links.agent1.unique_id])
# 								# print(agents.belieftree[1 + links.agent1.unique_id][best_action][0])

# 						# If the index is in the second part of the list, then the aim influence action is the best
# 						if best_action == len(cw_of_interest):
# 							# print(' ')
# 							# print('Performing a state change action')
# 							# print('best_action: ' + str(best_action))

# 							if links.agent1 == agents:
# 								# print('Before: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_pf][1]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_pf][1]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][agents.select_problem_3S_pf][1] = self.one_minus_one_check(links.agent2.belieftree[0][agents.select_problem_3S_pf][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1]
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])

# 								# print(' ')
# 								# print('Aim change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])

# 							if links.agent2 == agents:
# 								# print('Before: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_pf][1]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_pf][1]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][agents.select_problem_3S_pf][1] = self.one_minus_one_check(links.agent1.belieftree[0][agents.select_problem_3S_pf][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1]
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])


# 						# If the index is in the first part of the list, then the state influence action is the best
# 						if best_action == len(cw_of_interest) + 1:
# 							# print(' ')
# 							# print('Performing an aim change action')
# 							# print('best_action: ' + str(best_action))

# 							if links.agent1 == agents:
# 								# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][agents.select_problem_3S_pf][0] = self.one_minus_one_check(links.agent2.belieftree[0][agents.select_problem_3S_pf][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = links.agent2.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

# 								# print(' ')
# 								# print('State change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])

# 							if links.agent2 == agents:
# 								# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][agents.select_problem_3S_pf][0] = self.one_minus_one_check(links.agent1.belieftree[0][agents.select_problem_3S_pf][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = links.agent1.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

# 								# print(' ')
# 								# print('State change')
# 								# print(agents.belieftree[1 + links.agent1.unique_id])

# 				# If the agent is advocating or a policy, the following tasks are performed
# 				if agents.select_issue_3S_pf == 'policy':
					
# 					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
# 						# print(links)

# 						# Updating the aware decay parameter
# 						links.aware_decay = 5

# 						# If the index is in the first part of the list, then the framing action is the best
# 						if best_action <= impact_number - 1:
# 							# print(' ')
# 							# print('Performing a causal relation framing action')
# 							# print('best_action: ' + str(best_action))
# 							# print('impact_number: ' + str(impact_number))

# 							if links.agent1 == agents:
								
# 								# print('Before: ' + str(links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 										(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 										(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 										(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 										(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] = self.one_minus_one_check(links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
# 								agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][best_action] = links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][best_action] = \
# 									self.one_minus_one_check(agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][best_action])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = \
# 									self.one_minus_one_check(links.agent2.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action])

# 								# print(' ')
# 								# print('Causal change')
# 								# print(agents.belieftree_instrument[1 + links.agent2.unique_id])
# 								# print(agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][best_action])

# 							# Checking which agent in the link is the original agent
# 							if links.agent2 == agents:

# 								# print('Before: ' + str(links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 										(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 										(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 										(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 										(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] = self.one_minus_one_check(links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
# 								agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][best_action] = links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][best_action] = \
# 									self.one_minus_one_check(agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][best_action])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = \
# 									self.one_minus_one_check(links.agent1.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action])

# 								# print(' ')
# 								# print('Causal change')
# 								# print(agents.belieftree_instrument[1 + links.agent1.unique_id])
# 								# print(agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][best_action])

# 						# If the index is in the second part of the list, then the aim influence action is the best
# 						if best_action == impact_number:
# 							# print(' ')
# 							# print('Performing a state change action')
# 							# print('best_action: ' + str(best_action))

# 							if links.agent1 == agents:
# 								# print('Before: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_pf][1]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_pf][1]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][agents.select_problem_3S_pf][1] = self.one_minus_one_check(links.agent2.belieftree[0][agents.select_problem_3S_pf][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1]
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = \
# 									self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = \
# 									self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])

# 								# print(' ')
# 								# print('Aim change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])

# 							if links.agent2 == agents:

# 								# print('Before: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_pf][1]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_pf][1]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][agents.select_problem_3S_pf][1] = self.one_minus_one_check(links.agent1.belieftree[0][agents.select_problem_3S_pf][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1]
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = \
# 									self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = \
# 									self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])


# 						# If the index is in the first part of the list, then the state influence action is the best
# 						if best_action == impact_number + 1:
# 							# print(' ')
# 							# print('Performing an aim change action')
# 							# print('best_action: ' + str(best_action))

# 							if links.agent1 == agents:
# 								# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][agents.select_problem_3S_pf][0] = self.one_minus_one_check(links.agent2.belieftree[0][agents.select_problem_3S_pf][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = links.agent2.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = \
# 									self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = \
# 									self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

# 								# print(' ')
# 								# print('State change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])

# 							if links.agent2 == agents:
# 								# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][agents.select_problem_3S_pf][0] = self.one_minus_one_check(links.agent1.belieftree[0][agents.select_problem_3S_pf][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = links.agent1.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = \
# 									self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = \
# 									self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

# 								# print(' ')
# 								# print('State change')
# 								# print(agents.belieftree[1 + links.agent1.unique_id])



# 			# agents.resources_actions -= agents.resources
# 			agents.resources_actions -= agents.resources[0] * resources_weight_action

# 	def preference_udapte_as_PC(self, agent, who, len_PC, len_ML, len_S):

# 		"""
# 		The preference update for policy cores function (agenda setting)
# 		===========================

# 		This function is used to update the policy core preferences. It is only used for the
# 		old way of calculating the grade actions.
	
# 		Note: This function will ultimately be removed once all grading actions have been
# 		modified.

# 		"""

# 		# Preference calculation for the policy core issues
# 		PC_denominator = 0
# 		# Select one by one the Pr
# 		for j in range(len_ML):
# 			PC_denominator = 0
# 			# Selecting the causal relations starting from Pr
# 			for k in range(len_PC):
# 				# Contingency for partial knowledge issues
# 				if agent.belieftree[who][k][1] == None or agent.belieftree[who][k][0] == None or agent.belieftree[who][len_PC+len_ML+len_S+j+(k*len_ML)][0] == None:
# 					PC_denominator = 0
# 				else:
# 					# Check if causal relation and gap are both positive of both negative
# 					if (agent.belieftree[who][len_PC+len_ML+len_S+j+(k*len_ML)][0] < 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) < 0) \
# 					  or (agent.belieftree[who][len_PC+len_ML+len_S+j+(k*len_ML)][0] > 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) > 0):
# 						PC_denominator = PC_denominator + abs(agent.belieftree[who][len_PC+len_ML+len_S+j+(k*len_ML)][0]*\
# 						  (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]))
# 					else:
# 						PC_denominator = PC_denominator	
# 		# Then adding the gap of the policy core:
# 		for i in range(len_ML):
# 			# Contingency for partial knowledge issues
# 			if agent.belieftree[who][len_PC + i][1] == None or agent.belieftree[who][len_PC + i][0] == None:
# 				PC_denominator = PC_denominator
# 			else:
# 				PC_denominator = PC_denominator + abs(agent.belieftree[who][len_PC + i][1] - agent.belieftree[who][len_PC + i][0])
		
# 		# Calculating the numerator and the preference of all policy core issues:
# 		# Select one by one the Pr
# 		for j in range(len_ML):
# 			PC_numerator = 0
# 			# Selecting the causal relations starting from Pr
# 			for k in range(len_PC):
# 				# Contingency for partial knowledge issues
# 				if agent.belieftree[who][k][1] == None or agent.belieftree[who][k][0] == None or agent.belieftree[who][len_PC+len_ML+len_S+j+(k*len_ML)][0] == None: 
# 					PC_numerator = 0
# 				else:
# 					# Check if causal relation and gap are both positive of both negative
# 					if (agent.belieftree[who][len_PC+len_ML+len_S+j+(k*len_ML)][0] < 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) < 0) \
# 					  or (agent.belieftree[who][len_PC+len_ML+len_S+j+(k*len_ML)][0] > 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) > 0):
# 						PC_numerator = PC_numerator + abs(agent.belieftree[who][len_PC+len_ML+len_S+j+(k*len_ML)][0]*\
# 						  (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]))
# 					else:
# 						PC_numerator = PC_numerator	
# 			# Contingency for partial knowledge issues
# 			if agent.belieftree[who][len_PC + j][1] == None or agent.belieftree[who][len_PC + j][0] == None:
# 				PC_numerator = 0
# 			else:
# 				# Then adding the gap of the policy core:
# 				PC_numerator = PC_numerator + abs(agent.belieftree[who][len_PC + j][1] - agent.belieftree[who][len_PC + j][0])
# 			if PC_denominator != 0:
# 				agent.belieftree[who][len_PC+j][2] = PC_numerator/PC_denominator 
# 			else:
# 				agent.belieftree[who][len_PC+j][2] = 0

# 	def preference_udapte_pf_PC(self, agent, who, len_PC, len_ML, len_S, agenda_prob_3S_as):

# 		"""
# 		The preference update for policy cores function (policy formulation)
# 		===========================

# 		This function is used to update the policy core preferences. It is only used for the
# 		old way of calculating the grade actions.
	
# 		Note: This function will ultimately be removed once all grading actions have been
# 		modified.

# 		"""

# 		k = agenda_prob_3S_as

# 		# Calculating the numerator and the preference of all policy core issues:
# 		# Select one by one the Pr
# 		S_denominator = 0
# 		for j in range(len_S):
# 			# print('Selection S' + str(j+1))
# 			# print('State of the S' + str(j+1) + ': ' + str(agent.belieftree[0][len_PC + j][0])) # the state printed
# 			# Selecting the causal relations starting from PC
# 			# print(' ')
# 			# print(len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC))
# 			# Contingency for partial knowledge issues
# 			if agent.belieftree[0][k][1] != None and agent.belieftree[0][k][0] != None and agent.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC)][0] != None:
# 				# print('Causal Relation S' + str(j+1) + ' - PC' + str(k+1) + ': ' + str(agent.belieftree[0][len_PC+len_ML+len_S+(j+(k*len_ML))][0]))
# 				# print('Gap of PC' + str(k+1) + ': ' + str(agent.belieftree[0][k][1] - agent.belieftree[0][k][0]))
# 				# Check if causal relation and gap are both positive of both negative
# 				if (agent.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC)][0] < 0 and (agent.belieftree[0][k][1] - agent.belieftree[0][k][0]) < 0) \
# 					or (agent.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC)][0] > 0 and (agent.belieftree[0][k][1] - agent.belieftree[0][k][0]) > 0):
# 					# print('Calculating')
# 					S_denominator = S_denominator + abs(agent.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC)][0] * \
# 						(agent.belieftree[0][k][1] - agent.belieftree[0][k][0]))
# 					# print('This is the PC numerator: ' + str(S_denominator))
# 				else:
# 					S_denominator = S_denominator
# 			else:
# 				S_denominator = 0
# 			# Contingency for partial knowledge issues
# 			if agent.belieftree[0][len_PC + len_ML + j][1] == None or agent.belieftree[0][len_PC + len_ML + j][0] == None:
# 				S_denominator = S_denominator
# 			else:
# 				# Then adding the gap of the policy core:
# 				# print('This is the gap for the S' + str(j+1) + ': ' + str(agent.belieftree[0][len_PC + len_ML + j][1] - agent.belieftree[0][len_PC + len_ML + j][0]))
# 				S_denominator = S_denominator + abs(agent.belieftree[0][len_PC + len_ML + j][1] - agent.belieftree[0][len_PC + len_ML + j][0])


# 		# Calculating the numerator and the preference of all policy core issues:
# 		# Select one by one the Pr
# 		for j in range(len_S):
# 			S_numerator = 0
# 			# Contingency for partial knowledge issues
# 			if agent.belieftree[0][k][1] != None and agent.belieftree[0][k][0] != None and agent.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC)][0] != None:
# 				# Check if causal relation and gap are both positive of both negative
# 				if (agent.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC)][0] < 0 and (agent.belieftree[0][k][1] - agent.belieftree[0][k][0]) < 0) \
# 					or (agent.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC)][0] > 0 and (agent.belieftree[0][k][1] - agent.belieftree[0][k][0]) > 0):
# 					# print('Calculating')
# 					S_numerator = S_numerator + abs(agent.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC)][0] * \
# 						(agent.belieftree[0][k][1] - agent.belieftree[0][k][0]))
# 					# print('This is the PC numerator: ' + str(S_numerator))
# 				else:
# 					S_numerator = S_numerator
# 			else:
# 				S_numerator = 0
# 			# Contingency for partial knowledge issues
# 			if agent.belieftree[0][len_PC + len_ML + j][1] == None or agent.belieftree[0][len_PC + len_ML + j][0] == None:
# 				S_numerator = 0
# 			else:
# 				# Then adding the gap of the policy core:
# 				S_numerator = S_numerator + abs(agent.belieftree[0][len_PC + len_ML + j][1] - agent.belieftree[0][len_PC + len_ML + j][0])
# 			if S_denominator != 0:
# 				agent.belieftree[who][len_PC + len_ML + j][2] = S_numerator/S_denominator 
# 			else:
# 				agent.belieftree[who][len_PC + len_ML + j][2] = 0

# 	def instrument_preference_update(self, agent, who, AS_theory, len_PC, len_ML, len_S, instruments):

# 		"""
# 		Instrument preference update function
# 		===========================

# 		This function is used to calculate the ranking of each of the instrument from 
# 		which the agents can choose from. This is done in two parts.

# 		1/ The first part consists of calculating the preference level for the different
# 		secondary issues (layer 3 in the belief tree). In this part, the preferences of
# 		the agents are updated similarly to the function where the preferences are calculated.
# 		The main difference is that this time, it is based on the agenda which means that
# 		only the secondary issues affecting the problem on the agenda are considered.

# 		2/ The second part consists of obtaining the grade for the policy instruments.
# 		This is calculated as shown in the formalisation with the equation given by:
# 		G = sum(impact * (Aim - State) * Preference_secondary)
# 		We make sure that the instruments impact are only taken into account if the
# 		impact is of the same sign as the gap between the state and the aim for the
# 		specific secondary issues. If this is not the case, the impact is not considered
# 		for that specific part of the instrument.

# 		Notes:
# 		1/ The secondary issues for which the agent is not interested (this applies to 
# 		the external parties only) are not taken into account in the calculation. They
# 		are marked as the 'No' values.

# 		This function will ultimately be removed when all of the grading actions will be
# 		modified.

# 		"""

# 		######################################################################################################
# 		# 1/ Calculation of the preference level for the secondary issues based on the problem on the agenda #
# 		######################################################################################################

# 		S_denominator = 0
# 		if AS_theory != 2:
# 			j = agent.select_as_issue
# 		if AS_theory == 2:
# 			j = agent.select_problem_3S_as
# 		for k in range(len_S):
# 			if agent.belieftree[who][j][1] != None and agent.belieftree[who][j][0] != None and agent.belieftree[who][len_PC + len_ML + len_S + (len_PC*len_ML) + (j - len_PC)*len_S + k][0] != None:
# 				if (agent.belieftree[who][len_PC + len_ML + len_S + (len_PC*len_ML) + (j - len_PC)*len_S + k][0] < 0 and (agent.belieftree[who][j][1] - agent.belieftree[who][j][0]) < 0) \
# 					or (agent.belieftree[who][len_PC + len_ML + len_S + (len_PC*len_ML) + (j - len_PC)*len_S + k][0] > 0 and (agent.belieftree[who][j][1] - agent.belieftree[who][j][0]) > 0):
# 					S_denominator = S_denominator + abs(agent.belieftree[who][len_PC + len_ML + len_S + (len_PC*len_ML) + (j - len_PC)*len_S + k][0]*\
# 					  (agent.belieftree[who][j][1] - agent.belieftree[who][j][0]))
# 				else:
# 					S_denominator = S_denominator
# 			else:
# 				S_denominator = S_denominator

# 		for i in range(len_S):
# 			if agent.belieftree[who][len_PC + len_ML + i][0] != 'No':
# 				if agent.belieftree[who][len_PC + len_ML + i][1] != None and agent.belieftree[who][len_PC + len_ML + i][0] != None:
# 					S_denominator = S_denominator + abs(agent.belieftree[who][len_PC + len_ML + i][1] - agent.belieftree[who][len_PC + len_ML + i][0])
# 				else:
# 					S_denominator = 0

# 		S_numerator = 0
		
# 		for j in range(len_S):
# 			S_numerator = 0
# 			if AS_theory != 2:
# 				k = agent.select_as_issue
# 			if AS_theory == 2:
# 				k = agent.select_problem_3S_as
# 			if agent.belieftree[who][k][1] != None and agent.belieftree[who][k][0] != None and agent.belieftree[who][len_PC + len_ML + len_S + (len_PC*len_ML) + (k - len_PC)*len_S + j][0] != None:
# 				if (agent.belieftree[who][len_PC + len_ML + len_S + (len_PC*len_ML) + (k - len_PC)*len_S + j][0] < 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) < 0) \
# 					or (agent.belieftree[who][len_PC + len_ML + len_S + (len_PC*len_ML) + (k - len_PC)*len_S + j][0] > 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) > 0):
# 					S_numerator = S_numerator + abs(agent.belieftree[who][len_PC + len_ML + len_S + (len_PC*len_ML) + (k - len_PC)*len_S + j][0]*\
# 						  (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]))
# 				else:
# 					S_numerator = S_numerator
# 			else:
# 				S_numerator = S_numerator
# 			if agent.belieftree[who][len_PC + len_ML + j][0] != 'No':
# 				if agent.belieftree[who][len_PC + len_ML + j][1] != None and agent.belieftree[who][len_PC + len_ML + j][0] != None:
# 					S_numerator = S_numerator + abs(agent.belieftree[who][len_PC + len_ML + j][1] - agent.belieftree[who][len_PC + len_ML + j][0])
# 				else:
# 					S_numerator = 0
# 			if S_denominator != 0:
# 				agent.belieftree[who][len_PC+len_ML+j][2] = S_numerator/S_denominator 
# 			else:
# 				agent.belieftree[who][len_PC+len_ML+j][2] = 0

# 		##################################################################################################
# 		# 2/ Calculation of the grade of each of the instruments based on impact on the secondary issues #
# 		##################################################################################################

# 		agent.instrument_preferences[who] = [0 for h in range(len(instruments))]
# 		for i in range(len(instruments)):
# 			for j in range(len_S):
# 				if agent.belieftree[who][len_PC + len_ML + j][0] != 'No':
# 					if agent.belieftree[who][len_PC + len_ML + j][1] != None and agent.belieftree[who][len_PC + len_ML + j][0] != None:
# 						if (instruments[i][j] > 0 and (agent.belieftree[who][len_PC + len_ML + j][1] - agent.belieftree[who][len_PC + len_ML + j][0]) > 0 ) \
# 							or (instruments[i][j] < 0 and (agent.belieftree[who][len_PC + len_ML + j][1] - agent.belieftree[who][len_PC + len_ML + j][0]) < 0 ):
# 							# print(' ')
# 							# print('agent.instrument_preferences[who][i]: ' + str(agent.instrument_preferences[who][i]))
# 							# print('instruments[i][j]: ' + str(instruments[i][j]))
# 							# print('agent.belieftree[' + str(who) + '][len_PC + len_ML + ' + str(j) + '][1]: ' + str(agent.belieftree[who][len_PC + len_ML + j][1]))
# 							# print('agent.belieftree[' + str(who) + '][len_PC + len_ML + ' + str(j) + '][0]: ' + str(agent.belieftree[who][len_PC + len_ML + j][0]))
# 							# print('agent.belieftree[' + str(who) + '][len_PC + len_ML + ' + str(j) + '][2]: ' + str(agent.belieftree[who][len_PC + len_ML + j][2]))
# 							agent.instrument_preferences[who][i] = agent.instrument_preferences[who][i] + \
# 								(instruments[i][j] * (agent.belieftree[who][len_PC + len_ML + j][1] - agent.belieftree[who][len_PC + len_ML + j][0]) * \
# 								(agent.belieftree[who][len_PC + len_ML + j][2]))
# 							# print('agent.instrument_preferences[who][i]: ' + str(agent.instrument_preferences[who][i]))
# 					else:
# 						agent.instrument_preferences[who][i] = 0

# 	def one_minus_one_check(self, to_be_checked_parameter):

# 		"""
# 		One minus one check function
# 		===========================

# 		This function checks that a certain values does not got over one
# 		and does not go below one due to the randomisation.
		
# 		"""

# 		checked_parameter = 0
# 		if to_be_checked_parameter > 1:
# 			checked_parameter = 1
# 		elif to_be_checked_parameter < -1:
# 			checked_parameter = -1
# 		else:
# 			checked_parameter = to_be_checked_parameter

# 		return checked_parameter

# # Creation of the policy entrepreneur agents
# class Policyentres(Agent):

# 	def __init__(self, run_number, agent_id, unique_id, pos, network_strategy, affiliation, resources, belieftree, instrument_preferences, belieftree_policy, belieftree_instrument, select_as_issue, select_pinstrument, select_issue_3S_as, \
# 		select_problem_3S_as, select_policy_3S_as, select_issue_3S_pf, select_problem_3S_pf, select_policy_3S_pf, team_as, team_pf, coalition_as, coalition_pf):
# 		# super().__init__(unique_id, model)
# 		self.run_number = run_number
# 		self.agent_id = agent_id
# 		self.unique_id = unique_id
# 		self.pos = pos
# 		self.network_strategy = network_strategy
# 		# self.model = model
# 		self.affiliation = affiliation
# 		self.resources = resources
# 		self.belieftree = belieftree
# 		self.belieftree_policy = belieftree_policy
# 		self.belieftree_instrument = belieftree_instrument
# 		self.instrument_preferences = instrument_preferences
# 		self.select_as_issue = select_as_issue
# 		self.select_pinstrument = select_pinstrument
# 		self.select_issue_3S_as = select_issue_3S_as
# 		self.select_problem_3S_as = select_problem_3S_as
# 		self.select_policy_3S_as = select_policy_3S_as
# 		self.select_issue_3S_pf = select_issue_3S_pf
# 		self.select_problem_3S_pf = select_problem_3S_pf
# 		self.select_policy_3S_pf = select_policy_3S_pf
# 		self.team_as = team_as
# 		self.team_pf = team_pf
# 		self.coalition_as = coalition_as
# 		self.coalition_pf = coalition_pf

# 	# def __str__(self):
# 	# 	return 'POLICYENTREPRENEUR - Affiliation: ' + str(self.affiliation) + ', Resources: ' + str(self.resources) + \
# 	# 	', Position: [' + str(self.pos[0]) + ',' + str(self.pos[1]) + '], ID: ' + str(self.unique_id) + \
# 	# 	', Problem selected: ' + str(self.select_problem) + ', Policy selected: ' + str(self.select_policy) + \
# 	# 	', Belief tree: ' + str(self.belieftree)

# 	# Simple print with ID
# 	def __str__(self):
# 		return 'Policy entrepreneur: ' + str(self.unique_id)

# 	def policyentres_states_update(self, agent, master_list, affiliation_weights):

# 		"""
# 		The policy entrepreneurs states update function
# 		===========================

# 		This function uses the data from the external parties to update the states of 
# 		the policy entrepreneurs.

# 		Note: Ultimately, this would need to include the external parties lack of interests
# 		for some of the states.

# 		"""

# 		#' Addition of more than 3 affiliation will lead to unreported errors!')
# 		if len(affiliation_weights) != 3:
# 			print('WARNING - THIS CODE DOESNT WORK FOR MORE OR LESS THAN 3 AFFILIATIONS')

# 		# Defining the external parties list and the truth agent
# 		externalparties_list = []
# 		for agents in master_list:
# 			if type(agents) == Truth:
# 				truthagent = agents
# 			if type(agents) == Externalparties:
# 				externalparties_list.append(agents)

# 		# going through the different external parties:
# 		belief_sum_ep = [0 for k in range(len(truthagent.belieftree_truth))]
# 		# print(belief_sum_ep)
# 		for i in range(len(truthagent.belieftree_truth)):
# 			# print('NEW ISSUE! NEW ISSUES!')
# 			# This is used because in some cases, the external parties will have no impact on the agent (None values in the states of the EP)
# 			actual_length_ep = 0
# 			for j in range(len(externalparties_list)):
# 				# This line is added in case the EP has None states
# 				if externalparties_list[j].belieftree[0][i][0] != 'No':
# 					actual_length_ep += 1
# 					# Currently, the state of the policy makers is initialised as being equal to their initial aim:
# 					if agent.belieftree[0][i][0] == None:
# 						# print('Triggered - changed to: ' + str(agent.belieftree[0][i][1]))
# 						agent.belieftree[0][i][0] = agent.belieftree[0][i][1]
# 					# If they have the same affiliation, add without weight
# 					if externalparties_list[j].affiliation == agent.affiliation:
# 						# print('AFFILIATIONS ARE EQUAL')
# 						# print('issue ' + str(i+1) + ': ' + str(externalparties_list[j].belieftree[0][i][0]) +  /
# 						# ' and affiliation: ' + str(externalparties_list[j].affiliation) + '  ' + str(externalparties_list[j].unique_id))
# 						# print('This is the sum: ' + str(belief_sum_ep[i]))
# 						belief_sum_ep[i] = belief_sum_ep[i] + (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0])
# 						# print('The sum is equal to: ' + str(belief_sum_ep))
# 						# print('The change in state belief is equal to: ' + str(belief_sum_ep[i] / len(externalparties_list)))
# 					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 1) or \
# 					   (externalparties_list[j].affiliation == 1 and agent.affiliation == 0):
# 						# print('AFFILIATION 1 AND 2')
# 						belief_sum_ep[i] = belief_sum_ep[i] + \
# 						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[0]
# 					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 2) or \
# 					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 0):
# 						# print('AFFILIATION 1 AND 3')
# 						belief_sum_ep[i] = belief_sum_ep[i] + \
# 						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[1]
# 					if (externalparties_list[j].affiliation == 1 and agent.affiliation == 2) or \
# 					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 1):
# 						# print('AFFILIATION 2 AND 3')
# 						belief_sum_ep[i] = belief_sum_ep[i] + \
# 						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[2]
# 			agent.belieftree[0][i][0] = agent.belieftree[0][i][0] + belief_sum_ep[i] / actual_length_ep
# 			# print('This is issue: ' + str(i+1) + ' and its new value is: ' + str(agent.belieftree[0][i][0]))
# 		# print(agent)

# 	def action_grade_calculator(self, links, issue, parameter, agents, actionWeight, affiliation_weights):

# 		if links.agent1 == agents:
# 			if links.agent1.affiliation == links.agent2.affiliation:
# 				grade = links.conflict_level[0][issue][parameter] * links.aware * actionWeight

# 			# Affiliation 1-2
# 			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 				(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 				grade = links.conflict_level[0][issue][parameter] * links.aware * actionWeight * affiliation_weights[0]

# 			# Affiliation 1-3
# 			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 				(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 				grade = links.conflict_level[0][issue][parameter] * links.aware * actionWeight * affiliation_weights[1]

# 			# Affiliation 2-3
# 			if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 				(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 				grade = links.conflict_level[0][issue][parameter] * links.aware * actionWeight * affiliation_weights[2]

# 		if links.agent2 == agents:
# 			# Grade calculation using the likelihood method
# 			# Same affiliation
# 			if links.agent1.affiliation == links.agent2.affiliation:
# 				grade = links.conflict_level[1][issue][parameter] * links.aware * actionWeight

# 			# Affiliation 1-2
# 			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 				(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 				grade = links.conflict_level[1][issue][parameter] * links.aware * actionWeight * affiliation_weights[0]

# 			# Affiliation 1-3
# 			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 				(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 				grade = links.conflict_level[1][issue][parameter] * links.aware * actionWeight * affiliation_weights[1]

# 			# Affiliation 2-3
# 			if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 				(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 				grade = links.conflict_level[1][issue][parameter] * links.aware * actionWeight * affiliation_weights[2]

# 		return grade

# 	def action_implementor(self, links, issue, parameter, agents, affiliation_weights, resources_weight_action, resources_potency):

# 		if links.agent1 == agents:
			
# 			# print('Before: ', links.agent2.belieftree[0][issue][parameter])

# 			# Same affiliation
# 			if links.agent1.affiliation == links.agent2.affiliation:
# 				links.agent2.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent2.belieftree[0][issue][parameter]) * \
# 					agents.resources[0] * resources_weight_action * resources_potency

# 			# Affiliation 1-2
# 			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 				links.agent2.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent2.belieftree[0][issue][parameter]) * \
# 					agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 			# Affiliation 1-3
# 			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 				links.agent2.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent2.belieftree[0][issue][parameter]) * \
# 					agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 			# Affiliation 2-3
# 			if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 				links.agent2.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent2.belieftree[0][issue][parameter]) * \
# 					agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 			# print('After: ', links.agent2.belieftree[0][issue][parameter])

# 			# Checks and transfer of partial knowledge
# 			# 1-1 check - new value
# 			links.agent2.belieftree[0][issue][parameter] = self.one_minus_one_check(links.agent2.belieftree[0][issue][parameter])
# 			# Partial knowledge 1 with 1-1 check
# 			agents.belieftree[1 + links.agent2.unique_id][issue][parameter] = links.agent2.belieftree[0][issue][parameter] + (random.random()/5) - 0.1
# 			agents.belieftree[1 + links.agent2.unique_id][issue][parameter] = self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][issue][parameter])
# 			# Partial knowledge 2 with 1-1 check
# 			links.agent2.belieftree[1 + agents.unique_id][issue][parameter] = agents.belieftree[0][issue][parameter] + (random.random()/5) - 0.1
# 			links.agent2.belieftree[1 + agents.unique_id][issue][parameter] = self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][issue][parameter])

# 			results = [links.agent2.belieftree[0][issue][parameter], agents.belieftree[1 + links.agent2.unique_id][issue][parameter], links.agent2.belieftree[1 + agents.unique_id][issue][parameter]]

# 		if links.agent2 == agents:

# 			# print('Before: ', links.agent1.belieftree[0][issue][parameter])
			
# 			# Same affiliation
# 			if links.agent1.affiliation == links.agent2.affiliation:
# 				links.agent1.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent1.belieftree[0][issue][parameter]) * \
# 					agents.resources[0] * resources_weight_action * resources_potency

# 			# Affiliation 1-2
# 			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 				links.agent1.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent1.belieftree[0][issue][parameter]) * \
# 					agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 			# Affiliation 1-3
# 			if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 				links.agent1.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent1.belieftree[0][issue][parameter]) * \
# 					agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 			# Affiliation 2-3
# 			if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 				links.agent1.belieftree[0][issue][parameter] += (agents.belieftree[0][issue][parameter] - links.agent1.belieftree[0][issue][parameter]) * \
# 					agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 			# print('After: ', links.agent1.belieftree[0][issue][parameter])
			
# 			# Checks and transfer of partial knowledge
# 			# 1-1 check - new value
# 			links.agent1.belieftree[0][issue][parameter] = self.one_minus_one_check(links.agent1.belieftree[0][issue][parameter])
# 			# Partial knowledge 1 with 1-1 check
# 			agents.belieftree[1 + links.agent1.unique_id][issue][parameter] = links.agent1.belieftree[0][issue][parameter] + (random.random()/5) - 0.1
# 			agents.belieftree[1 + links.agent1.unique_id][issue][parameter] = self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][issue][parameter])
# 			# Partial knowledge 2 with 1-1 check
# 			links.agent1.belieftree[1 + agents.unique_id][issue][parameter] = agents.belieftree[0][issue][parameter] + (random.random()/5) - 0.1
# 			links.agent1.belieftree[1 + agents.unique_id][issue][parameter] = self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][issue][parameter])

# 			results = [links.agent1.belieftree[0][issue][parameter], agents.belieftree[1 + links.agent1.unique_id][issue][parameter], links.agent1.belieftree[1 + agents.unique_id][issue][parameter]]
		
# 		return results

# 	def pm_pe_actions_as(self, agents, link_list, deep_core, mid_level, secondary, resources_weight_action, resources_potency, affiliation_weights):

# 		"""
# 		The PEs and PMs actions function (agenda setting)
# 		===========================

# 		This function is used to perform the different active actions of the
# 		policy entrepreneurs and the policy makers during the agenda setting.

# 		The actions that can be performed are framing, influence on states and 
# 		influence on aims. All of the actions are first graded. Then the action
# 		that has the highest grade is selected. Finally, the action selected 
# 		is implemented.

# 		"""

# 		len_PC = len(deep_core)
# 		len_ML = len(mid_level)
# 		len_S = len(secondary)
# 		total_issue_number = len_PC + len_ML + len_S

# 		# Selection of the cw of interest
# 		cw_of_interest = []
# 		# We only consider the causal relations related to the problem on the agenda
# 		for cw_choice in range(len(deep_core)):
# 				cw_of_interest.append(len_PC + len_ML + len_S + (agents.select_as_issue - len_PC) + cw_choice * len(mid_level))

# 		# print(' ')
# 		# print('Causal relations of interest: ' + str(cw_of_interest))

# 		# Making sure there are enough resources
# 		while agents.resources_actions > 0.001:

# 			# Going through all the links in the model
# 			# print(agents)
# 			total_grade_list = []
# 			total_grade_list_links = []
# 			for links in link_list:

# 				# Making sure that the link is attached to the agent and has a aware higher than 0
# 				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
# 					total_grade_list_links.append(links)

# 					# Definition the action weight parameter
# 					if type(links.agent1) == Policymakers or type(links.agent2) == Policymakers:
# 						actionWeight = 1
# 					else:
# 						actionWeight = 0.95
					
# 					# 1. Grading all framing actions:
# 					# Checking through all possible framing - This is all based on partial knowledge!
# 					for cw in cw_of_interest:
# 						cw_grade = self.action_grade_calculator(links, cw, 0, agents, actionWeight, affiliation_weights)
# 						total_grade_list.append(cw_grade)	

# 					# 2. Grading all individual actions - Aim change
# 					aim_grade = self.action_grade_calculator(links, agents.select_as_issue, 1, agents, actionWeight, affiliation_weights)
# 					total_grade_list.append(aim_grade)

# 					# 3. Grading all individual actions - State change
# 					state_grade = self.action_grade_calculator(links, agents.select_as_issue, 0, agents, actionWeight, affiliation_weights)
# 					total_grade_list.append(state_grade)

# 			# print(' ')
# 			# print('Number of actions: ' + str(len(total_grade_list)))
# 			# print(total_grade_list)

# 			# 4. Choosing an action
# 			# Check if several actions have the same grade
# 			min_best_action = min(total_grade_list)
# 			count_min_list = []
# 			count = 0
# 			for item in total_grade_list:
# 				if item == min_best_action:
# 					count_min_list.append(count)
# 				count += 1
# 			# print('List of indexes: ' + str(count_min_list))
# 			# print(' ')

# 			# If there are several grades at the same level, then choose a random action from these grades:
# 			if len(count_min_list) > 1:
# 				best_action_index = random.choice(count_min_list)
# 				# print('Randomly chosen best action: ' + str(best_action_index))
# 			else:
# 				best_action_index = total_grade_list.index(min(total_grade_list))
# 				# print('Not randomly chosen: ' + str(best_action_index))
			
# 			# print(' ')
# 			# print('----- New check for best action ------')
# 			# print('Action value: ' + str(min(total_grade_list)))
# 			# print('Index of the best action: ' + str(best_action_index))
# 			# print('This is the grade of the action: ' + str(total_grade_list[best_action_index]))
# 			# Make sure that we do not take into account the 0 from the list to perform the following calculations
# 			# best_action_index += 1
# 			# print('The total amount of links considered: ' + str(len(total_grade_list_links)))
# 			# print('The number of actions per link considered: ' + str(len(cw_of_interest) + 2))
# 			# print('The total amount of actions considered: ' + str(len(total_grade_list)))
# 			# print('The link for the action is: ' + str(int(best_action_index/(len(cw_of_interest) + 2))))
# 			best_action = best_action_index - (len(cw_of_interest) + 2) * int(best_action_index/(len(cw_of_interest) + 2))
# 			# print('The impacted index is: ' + str(best_action))
# 			# print('The would be index without the +1: ' + str((best_action_index - (len(cw_of_interest) + 2) * int(best_action_index/(len(cw_of_interest) + 2))) - 1))
# 			# print('   ')

# 			# 5. Performing the actual action
# 			# Selecting the link:
# 			for links in link_list:

# 				if links == total_grade_list_links[int(best_action_index/(len(cw_of_interest) + 2))]:
# 					# print(links)

# 					# If the index is in the first part of the list, then the framing action is the best
# 					if best_action <= len(cw_of_interest) -1:					
# 						# print(' ')
# 						# print('Framing action - causal relation')
# 						# print('best_action: ' + str(best_action))
# 						# print('cw_of_interest: ' + str(cw_of_interest))
# 						# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

# 						# To simplify the notations
# 						best_action = cw_of_interest[best_action]

# 						# Update of the aware decay parameter
# 						links.aware_decay = 5

# 						implemented_action = self.action_implementor(links, best_action, 0, agents, affiliation_weights, resources_weight_action, resources_potency)

# 					# If the index is in the second part of the list, then the aim influence action is the best
# 					if best_action == len(cw_of_interest):
# 						# print('Implementing a aim influence action:')
# 						links.aware_decay = 5

# 						implemented_action = self.action_implementor(links, agents.select_as_issue, 1, agents, affiliation_weights, resources_weight_action, resources_potency)

# 					# If the index is in the first part of the list, then the state influence action is the best
# 					if best_action == len(cw_of_interest) + 1:
# 						# print('Implementing a state influence action:')
# 						links.aware_decay = 5
						
# 						implemented_action = self.action_implementor(links, agents.select_as_issue, 0, agents, affiliation_weights, resources_weight_action, resources_potency)

# 			# agents.resources_actions -= agents.resources
# 			agents.resources_actions -= agents.resources[0] * resources_weight_action

# 	def pm_pe_actions_pf(self, agents, link_list, deep_core, mid_level, secondary, causalrelation_number, agenda_as_issue, instruments, resources_weight_action, resources_potency, AS_theory, affiliation_weights):

# 		"""
# 		The PEs and PMs actions function (policy formulation)
# 		===========================

# 		This function is used to perform the different active actions of the
# 		policy entrepreneurs and the policy makers during the policy formulation.

# 		The actions that can be performed are framing, influence on states and 
# 		influence on aims. All of the actions are first graded. Then the action
# 		that has the highest grade is selected. Finally, the action selected 
# 		is implemented.

# 		"""

# 		len_PC = len(deep_core)
# 		len_ML = len(mid_level)
# 		len_S = len(secondary)
# 		total_issue_number = len_PC + len_ML + len_S

# 		# Here are the modifications related to the policy formulation
# 		# Looking for the relevant causal relations for the policy formulation
# 		of_interest = []
# 		cw_of_interest = []
# 		# We only consider the causal relations related to the problem on the agenda
# 		for cw_choice in range(len(secondary)):
# 			if agents.belieftree[0][len_PC + len_ML + len_S + (len_PC * len_ML) + (agenda_as_issue - len_PC)*len_S + cw_choice][0] \
# 				* instruments[agents.select_pinstrument][cw_choice] != 0:
# 				cw_of_interest.append(len_PC + len_ML + len_S + (len_PC * len_ML) + (agenda_as_issue - len_PC)*len_S + cw_choice)
# 		of_interest.append(cw_of_interest)

# 		# Looking for the relevant issues for the policy formulation
# 		issue_of_interest = []
# 		for issue_choice in range(len(secondary)):
# 			if instruments[agents.select_pinstrument][issue_choice] != 0:
# 				issue_of_interest.append(len_PC + len_ML + issue_choice)
# 		of_interest.append(issue_of_interest)

# 		# Making sure there are enough resources
# 		while agents.resources_actions > 0.001:
# 			# Going through all the links in the model
# 			# print(agents)
# 			total_grade_list = []
# 			total_grade_list_links = []
# 			for links in link_list:
				
# 				# Making sure that the link is attached to the agent and has a aware higher than 0
# 				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
# 					total_grade_list_links.append(links)
# 					# Definition the action weight parameter
# 					if type(links.agent1) == Policymakers or type(links.agent2) == Policymakers:
# 						actionWeight = 1
# 					else:
# 						actionWeight = 0.95

# 					# 1. Grading all framing actions:
# 					# Checking through all possible framing - This is all based on partial knowledge!
# 					for cw in cw_of_interest:

# 						# Checking which agent in the link is the original agent
# 						cw_grade = self.action_grade_calculator(links, cw, 0, agents, actionWeight, affiliation_weights)
# 						total_grade_list.append(cw_grade)

# 					# 2. Grading all individual actions - Aim change
# 					# Going though all possible choices of issue
# 					for issue_num in issue_of_interest:

# 						aim_grade = self.action_grade_calculator(links, issue_num, 1, agents, actionWeight, affiliation_weights)
# 						total_grade_list.append(aim_grade)

# 					# 3. Grading all individual actions - State change
# 					# Going though all possible choices of issue
# 					for issue_num in issue_of_interest:

# 						state_grade = self.action_grade_calculator(links, issue_num, 0, agents, actionWeight, affiliation_weights)
# 						total_grade_list.append(state_grade)

# 			# print(' ')
# 			# print(total_grade_list)

# 			# 4. Choosing an action
# 			best_action_index = total_grade_list.index(min(total_grade_list))

# 			# print(' ')
# 			# print('------ New action grade check -------')
# 			# print('Grade length: ' + str(len(total_grade_list)))
# 			# print('Best index: ' + str(best_action_index))
# 			# print('Number of links: ' + str(len(total_grade_list_links)))
# 			# print('Number of grades per link: ' + str(len(cw_of_interest) + 2 * len(issue_of_interest)))
# 			# print('Link for this action: ' + str(int(best_action_index / (len(cw_of_interest) + 2 * len(issue_of_interest) ) )))
			
# 			best_action = best_action_index - ((len(cw_of_interest) + 2 * len(issue_of_interest)) * int(best_action_index / (len(cw_of_interest) + 2 * len(issue_of_interest) ) ))
# 			# print('Best action selected: ' + str(best_action))

# 			best_action = len(cw_of_interest) + len(issue_of_interest) - 1

# 			for links in link_list:

# 				if links == total_grade_list_links[int(best_action_index / (len(cw_of_interest) + 2 * len(issue_of_interest) ) )]:
# 					# print(links)					

# 					# 5. Performing the actual action
# 					# If the index is in the first part of the list, then the framing action is the best
# 					if best_action <= len(cw_of_interest) - 1:

# 						# print(' ')
# 						# print('Framing action - causal relation')
# 						# print('best_action: ' + str(best_action))
# 						# print('of_interest[0]: ' + str(of_interest[0]))
# 						# print('of_interest[0][best_action]: ' + str(of_interest[0][best_action]))

# 						# Update of the aware decay parameter
# 						links.aware_decay = 5

# 						implemented_action = self.action_implementor(links, of_interest[0][best_action], 0, agents, affiliation_weights, resources_weight_action, resources_potency)

# 					# If the index is in the second part of the list, then the aim influence action on the problem is the best
# 					if best_action > len(cw_of_interest) - 1 and best_action < len(cw_of_interest) + len(issue_of_interest) - 1:

# 						# print(' ')
# 						# print('Aim influence action')
# 						# print('best_action: ' + str(best_action))
# 						# print('of_interest[1]: ' + str(of_interest[1]))
# 						# print('of_interest[1][best_action - len(cw_of_interest)]: ' + str(of_interest[1][best_action - len(cw_of_interest)]))
						
# 						# Update of the aware decay parameter
# 						links.aware_decay = 5

# 						implemented_action = self.action_implementor(links, of_interest[1][best_action - len(cw_of_interest)], 1, agents, affiliation_weights, resources_weight_action, resources_potency)

# 					# If the index is in the first part of the list, then the aim influence action on the policy is the best
# 					if best_action >= len(cw_of_interest) + len(issue_of_interest) - 1:

# 						# print(' ')
# 						# print('Aim influence action')
# 						# print('best_action: ' + str(best_action))
# 						# print('of_interest[1]: ' + str(of_interest[1]))
# 						# print('of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]: ' + str(of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]))

# 						# Update of the aware decay parameter
# 						links.aware_decay = 5

# 						implemented_action = self.action_implementor(links, of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)], 0, agents, affiliation_weights, resources_weight_action, resources_potency)

						
# 			# print('Resources left: ' + str(agents.resources_actions))
# 			agents.resources_actions -= agents.resources[0] * resources_weight_action

# 	def pm_pe_actions_as_3S(self, agents, link_list, deep_core, mid_level, secondary, resources_weight_action, resources_potency, affiliation_weights, conflict_level_coef):

# 		"""
# 		The PEs and PMs actions function - three streams (agenda setting)
# 		===========================

# 		This function is used to perform the different active actions of the
# 		policy entrepreneurs and the policy makers during the agenda setting.

# 		The actions that can be performed are framing, influence on states and 
# 		influence on aims. All of the actions are first graded. Then the action
# 		that has the highest grade is selected. Finally, the action selected 
# 		is implemented.

# 		Note: This function is the same as the one presented before for the backbone
# 		backbone+ and ACF. The main difference is the addition of actions related
# 		to the choice of a policy by the agents.

# 		"""

# 		len_PC = len(deep_core)
# 		len_ML = len(mid_level)
# 		len_S = len(secondary)
# 		total_issue_number = len_PC + len_ML + len_S

# 		# Selection of the cw of interest
# 		cw_of_interest = []
# 		# We only consider the causal relations related to the problem selected by the agent
# 		for cw_choice in range(len(deep_core)):
# 				cw_of_interest.append(len_PC + len_ML + len_S + (agents.select_problem_3S_as - len_PC) + cw_choice * len(mid_level))

# 		# Selection of the impact of interest
# 		impact_number = len(agents.belieftree_policy[0][agents.select_policy_3S_as])

# 		# print(' ')
# 		# print('Causal relations of interest: ' + str(cw_of_interest))

# 		# Making sure there are enough resources
# 		while agents.resources_actions > 0.001:

# 			# Going through all the links in the model
# 			# print(agents)
# 			total_grade_list = []
# 			total_grade_list_links = []
# 			for links in link_list:

# 				# Making sure that the link is attached to the agent and has a aware higher than 0
# 				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
# 					total_grade_list_links.append(links)

# 					# Definition the action weight parameter
# 					if type(links.agent1) == Policymakers or type(links.agent2) == Policymakers:
# 						actionWeight = 1
# 					else:
# 						actionWeight = 0.95
					
# 					# 1. Framing on causal relation and policy impacts

# 					# If the agent is advocating or a problem, the following tasks are performed
# 					if agents.select_issue_3S_as == 'problem':
# 						# 1.a. Grading all framing actions on causal relations:
# 						# Checking through all possible framing - This is all based on partial knowledge!
# 						for cw in range(len(cw_of_interest)):

# 							# Checking which agent in the link is the original agent
# 							if links.agent1 == agents:

# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									cw_grade = links.conflict_level[0][total_issue_number + cw][0] * links.aware * actionWeight
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									cw_grade = links.conflict_level[0][total_issue_number + cw][0] * links.aware * actionWeight * affiliation_weights[0]
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									cw_grade = links.conflict_level[0][total_issue_number + cw][0] * links.aware * actionWeight * affiliation_weights[1]
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									cw_grade = links.conflict_level[0][total_issue_number + cw][0] * links.aware * actionWeight * affiliation_weights[2]
# 									total_grade_list.append(cw_grade)					


# 								# # Check if no partial knowledge (initial value)
# 								# check_none = 0
# 								# if agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] == None:
# 								# 	agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = 0
# 								# 	check_none = 1
# 								# # Performing the action
# 								# cw_grade = (agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]) * \
# 								# 	agents.resources[0] * resources_weight_action * links.aware * resources_potency
# 								# # Adding the grade to the grade list
# 								# total_grade_list.append(cw_grade)
# 								# #  Reset to None after finding the grade
# 								# if check_none == 1:
# 								# 	agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = None

# 							# Checking which agent in the link is the original agent
# 							if links.agent2 == agents:
# 								#  Check if no partial knowledge (initial value)
# 								check_none = 0
# 								if agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] == None:
# 									agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = 0
# 									check_none = 1
# 								# Performing the action
# 								cw_grade = (agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0]) * \
# 									agents.resources[0] * resources_weight_action * links.aware * resources_potency
# 								# Adding the grade to the grade list
# 								total_grade_list.append(cw_grade)
# 								# Reset to None after finding the grade
# 								if check_none == 1:
# 									agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = None

# 					# If the agent is advocating or a policy, the following tasks are performed
# 					if agents.select_issue_3S_as == 'policy':
# 						# 1.b. Grading all framing actions on policy impacts:

# 						# Checking through all possible framing - This is all based on partial knowledge!
# 						for impact in range(impact_number):

# 							# Checking which agent in the link is the original agent
# 							if links.agent1 == agents:

# 								# Need to calculate the conflict level per impact (to avoid having to create a whole new conflict level array in the links for the policies)
# 								# Note that there is currently a need to check for None partial knowledge

# 								check_none = 0
# 								if agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] == None:
# 									agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] = 0
# 									check_none = 1
 
# 								belief_diff = abs(agents.belieftree_policy[0][agents.select_policy_3S_as][impact] - agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact])

# 								if check_none == 1:
# 									agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] = None

# 								if belief_diff <= 0.25:
# 									conflict_level_impact = conflict_level_coef[0]
# 								if belief_diff > 0.25 and belief_diff <= 1.75:
# 									conflict_level_impact = conflict_level_coef[2]
# 								if belief_diff > 1.75:
# 									conflict_level_impact = conflict_level_coef[1]

# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									impact_grade = conflict_level_impact * links.aware * actionWeight
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[0]
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[1]
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[2]
# 									total_grade_list.append(impact_grade)	

# 								# Check if no partial knowledge (initial value)
# 								# check_none = 0
# 								# if agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] == None:
# 								# 	agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] = 0
# 								# 	check_none = 1
# 								# # Performing the action
# 								# impact_grade = (agents.belieftree_policy[0][agents.select_policy_3S_as][impact] - agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact]) * \
# 								# 	agents.resources[0] * resources_weight_action * links.aware * resources_potency
# 								# # Adding the grade to the grade list
# 								# total_grade_list.append(impact_grade)
# 								# #  Reset to None after finding the grade
# 								# if check_none == 1:
# 								# 	agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][impact] = None

# 							# Checking which agent in the link is the original agent
# 							if links.agent2 == agents:

# 								# Need to calculate the conflict level per impact (to avoid having to create a whole new conflict level array in the links for the policies)
# 								# Note that there is currently a need to check for None partial knowledge

# 								check_none = 0
# 								if agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] == None:
# 									agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] = 0
# 									check_none = 1
								
# 								belief_diff = abs(agents.belieftree_policy[0][agents.select_policy_3S_as][impact] - agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact])

# 								if check_none == 1:
# 									agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] = None

# 								if belief_diff <= 0.25:
# 									conflict_level_impact = conflict_level_coef[0]
# 								if belief_diff > 0.25 and belief_diff <= 1.75:
# 									conflict_level_impact = conflict_level_coef[2]
# 								if belief_diff > 1.75:
# 									conflict_level_impact = conflict_level_coef[1]

# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									impact_grade = conflict_level_impact * links.aware * actionWeight
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[0]
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[1]
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[2]
# 									total_grade_list.append(impact_grade)	


# 								# #  Check if no partial knowledge (initial value)
# 								# check_none = 0
# 								# if agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] == None:
# 								# 	agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] = 0
# 								# 	check_none = 1
# 								# impact_grade = (agents.belieftree_policy[0][agents.select_policy_3S_as][impact] - agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact]) * \
# 								# 	agents.resources[0] * resources_weight_action * links.aware * resources_potency
# 								# # Adding the grade to the grade list
# 								# total_grade_list.append(impact_grade)
# 								# # Reset to None after finding the grade
# 								# if check_none == 1:
# 								# 	agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][impact] = None

# 					# 2. Grading all individual actions - Aim change
# 					if links.agent1 == agents:

# 						# Grade calculation using the likelihood method
# 						# Same affiliation
# 						if links.agent1.affiliation == links.agent2.affiliation:
# 							aim_grade_issue = links.conflict_level[0][agents.select_problem_3S_as][1] * links.aware * actionWeight
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 1-2
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 							(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 							aim_grade_issue = links.conflict_level[0][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[0]
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 1-3
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 							aim_grade_issue = links.conflict_level[0][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[1]
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 2-3
# 						if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 							aim_grade_issue = links.conflict_level[0][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[2]
# 							total_grade_list.append(aim_grade_issue)	

# 						# # Check if no partial knowledge (initial value)
# 						# check_none = 0
# 						# if agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] == None:
# 						# 	agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = 0
# 						# 	check_none = 1
# 						# # Performing the action
# 						# aim_grade_issue = (agents.belieftree[0][agents.select_problem_3S_as][1] - agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1]) * \
# 						# 	agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_problem_3S_as][1] * actionWeight * resources_potency
# 						# #  Reset to None after finding the grade
# 						# if check_none == 1:
# 						# 	agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = None
# 						# # Adding the grade to the grade list
# 						# total_grade_list.append(aim_grade_issue)

# 					if links.agent2 == agents:

# 						# Grade calculation using the likelihood method
# 						# Same affiliation
# 						if links.agent1.affiliation == links.agent2.affiliation:
# 							aim_grade_issue = links.conflict_level[1][agents.select_problem_3S_as][1] * links.aware * actionWeight
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 1-2
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 							(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 							aim_grade_issue = links.conflict_level[1][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[0]
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 1-3
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 							aim_grade_issue = links.conflict_level[1][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[1]
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 2-3
# 						if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 							aim_grade_issue = links.conflict_level[1][agents.select_problem_3S_as][1] * links.aware * actionWeight * affiliation_weights[2]
# 							total_grade_list.append(aim_grade_issue)	

# 						# # Check if no partial knowledge (initial value)
# 						# check_none = 0
# 						# if agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] == None:
# 						# 	agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = 0
# 						# 	check_none = 1
# 						# # Performing the action
# 						# aim_grade_issue = (agents.belieftree[0][agents.select_problem_3S_as][1] - agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1]) * \
# 						# 	agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_problem_3S_as][1] * actionWeight * resources_potency
# 						# #  Reset to None after finding the grade
# 						# if check_none == 1:
# 						# 	agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = None
# 						# # Adding the grade to the grade list
# 						# total_grade_list.append(aim_grade_issue)

# 					# 3. Grading all individual actions - State change
# 					if links.agent1 == agents:

# 						# Grade calculation using the likelihood method
# 						# Same affiliation
# 						if links.agent1.affiliation == links.agent2.affiliation:
# 							state_grade_issue = links.conflict_level[0][agents.select_problem_3S_as][0] * links.aware * actionWeight
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 1-2
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 							(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 							state_grade_issue = links.conflict_level[0][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[0]
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 1-3
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 							state_grade_issue = links.conflict_level[0][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[1]
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 2-3
# 						if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 							state_grade_issue = links.conflict_level[0][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[2]
# 							total_grade_list.append(state_grade_issue)	


# 						# # Check if no partial knowledge (initial value)
# 						# check_none = 0
# 						# if agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] == None:
# 						# 	agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = 0
# 						# 	check_none = 1
# 						# # Performing the action
# 						# state_grade_issue = (agents.belieftree[0][agents.select_problem_3S_as][0] - agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0]) * \
# 						# 	agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_problem_3S_as][0] * actionWeight * resources_potency
# 						# #  Reset to None after finding the grade
# 						# if check_none == 1:
# 						# 	agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = None
# 						# # Adding the grade to the grade list
# 						# total_grade_list.append(state_grade_issue)

# 					if links.agent2 == agents:

# 						# Grade calculation using the likelihood method
# 						# Same affiliation
# 						if links.agent1.affiliation == links.agent2.affiliation:
# 							state_grade_issue = links.conflict_level[1][agents.select_problem_3S_as][0] * links.aware * actionWeight
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 1-2
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 							(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 							state_grade_issue = links.conflict_level[1][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[0]
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 1-3
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 							state_grade_issue = links.conflict_level[1][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[1]
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 2-3
# 						if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 							state_grade_issue = links.conflict_level[1][agents.select_problem_3S_as][0] * links.aware * actionWeight * affiliation_weights[2]
# 							total_grade_list.append(state_grade_issue)


# 						# # Check if no partial knowledge (initial value)
# 						# check_none = 0
# 						# if agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] == None:
# 						# 	agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = 0
# 						# 	check_none = 1
# 						# # Performing the action
# 						# state_grade_issue = (agents.belieftree[0][agents.select_problem_3S_as][0] - agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0]) * \
# 						# 	agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_problem_3S_as][0] * actionWeight * resources_potency
# 						# #  Reset to None after finding the grade
# 						# if check_none == 1:
# 						# 	agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = None
# 						# # Adding the grade to the grade list
# 						# total_grade_list.append(state_grade_issue)
# 					# print(' ')

# 			# print(' ')
# 			# print('Number of actions: ' + str(len(total_grade_list)))
# 			# print(total_grade_list)

# 			# 4. Choosing an action

# 			# If the agent is advocating or a problem, the following tasks are performed
# 			if agents.select_issue_3S_as == 'problem':

# 				best_action_index = total_grade_list.index(max(total_grade_list))
# 				agent_best_action = int(best_action_index/(len(cw_of_interest) + 1 + 1))
# 				best_action = best_action_index - (agent_best_action)*(len(cw_of_interest) + 1 + 1)

# 				# print(' ')
# 				# print('----- Considering new action grading (problem) -----')
# 				# print('best_action_index: ' + str(best_action_index))
# 				# print('Number of actions per agent: ' + str(len(cw_of_interest) + 1 + 1))
# 				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
# 				# print('Action to be performed: ' + str(best_action))
# 				# print('Agent performing the action: ' + str(agent_best_action))

# 			# If the agent is advocating or a policy, the following tasks are performed
# 			if agents.select_issue_3S_as == 'policy':
				
# 				best_action_index = total_grade_list.index(max(total_grade_list))
# 				agent_best_action = int(best_action_index/(impact_number + 1 + 1))
# 				best_action = best_action_index - (agent_best_action)*(impact_number + 1 + 1)

# 				# print(' ')
# 				# print('----- Considering new action grading (policy) -----')
# 				# print('best_action_index: ' + str(best_action_index))
# 				# print('Number of actions per agent: ' + str(impact_number + 1 + 1))
# 				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
# 				# print('Action to be performed: ' + str(best_action))
# 				# print('Agent performing the action: ' + str(agent_best_action))


# 			# 5. Performing the actual action
# 			# Selecting the link:
# 			for links in link_list:

# 				# If the agent is advocating or a problem, the following tasks are performed
# 				if agents.select_issue_3S_as == 'problem':

# 					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
# 						# print(links)

# 						# Updating the aware decay parameter
# 						links.aware_decay = 5

# 						# If the index is in the first part of the list, then the framing action is the best
# 						if best_action <= len(cw_of_interest) - 1:
# 							# print(' ')
# 							# print('Performing a causal relation framing action')
# 							# print('best_action: ' + str(best_action))
# 							# print('cw_of_interest: ' + str(cw_of_interest))
# 							# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))
							
# 							# To simplify the notations
# 							best_action = cw_of_interest[best_action]

# 							if links.agent1 == agents:
								
# 								# print('Before: ' + str(links.agent2.belieftree[0][best_action][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][best_action][0]))

# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][best_action][0] = self.one_minus_one_check(links.agent2.belieftree[0][best_action][0])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][best_action][0] = links.agent2.belieftree[0][best_action][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][best_action][0] = self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][best_action][0])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][best_action][0] = self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][best_action][0])

# 								# print(' ')
# 								# print('Causal change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])
# 								# print(agents.belieftree[1 + links.agent2.unique_id][best_action][0])

# 							# Checking which agent in the link is the original agent
# 							if links.agent2 == agents:

# 								# print('Before: ' + str(links.agent1.belieftree[0][best_action][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]
# 								# print('After: ' + str(links.agent1.belieftree[0][best_action][0]))

# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][best_action][0] = self.one_minus_one_check(links.agent1.belieftree[0][best_action][0])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][best_action][0] = links.agent1.belieftree[0][best_action][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][best_action][0] = self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][best_action][0])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][best_action][0] = self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][best_action][0])

# 								# print(' ')
# 								# print('Causal change')
# 								# print(agents.belieftree[1 + links.agent1.unique_id])
# 								# print(agents.belieftree[1 + links.agent1.unique_id][best_action][0])

# 						# If the index is in the second part of the list, then the aim influence action is the best
# 						if best_action == len(cw_of_interest):
# 							# print(' ')
# 							# print('Performing a state change action')
# 							# print('best_action: ' + str(best_action))

# 							if links.agent1 == agents:
# 								# print('Before: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_as][1]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_as][1]))

# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][agents.select_problem_3S_as][1] = self.one_minus_one_check(links.agent2.belieftree[0][agents.select_problem_3S_as][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1]
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])

# 								# print(' ')
# 								# print('Aim change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])

# 							if links.agent2 == agents:

# 								# print('Before: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_as][1]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_as][1]))

# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][agents.select_problem_3S_as][1] = self.one_minus_one_check(links.agent1.belieftree[0][agents.select_problem_3S_as][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1]
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])


# 						# If the index is in the first part of the list, then the state influence action is the best
# 						if best_action == len(cw_of_interest) + 1:
# 							# print(' ')
# 							# print('Performing an aim change action')
# 							# print('best_action: ' + str(best_action))

# 							if links.agent1 == agents:

# 								# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))

# 								# Checks and transfer of partial knowledge
# 								links.agent2.belieftree[0][agents.select_problem_3S_as][0] = self.one_minus_one_check(links.agent2.belieftree[0][agents.select_problem_3S_as][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = links.agent2.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

# 								# print(' ')
# 								# print('State change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])

# 							if links.agent2 == agents:
# 								# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
# 								# 1-1 check
# 								links.agent1.belieftree[0][agents.select_problem_3S_as][0] = self.one_minus_one_check(links.agent1.belieftree[0][agents.select_problem_3S_as][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = links.agent1.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

# 								# print(' ')
# 								# print('State change')
# 								# print(agents.belieftree[1 + links.agent1.unique_id])

# 				# If the agent is advocating or a policy, the following tasks are performed
# 				if agents.select_issue_3S_as == 'policy':
					
# 					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
# 						# print(links)

# 						# Updating the aware decay parameter
# 						links.aware_decay = 5

# 						# If the index is in the first part of the list, then the framing action is the best
# 						if best_action <= impact_number - 1:
# 							# print(' ')
# 							# print('Performing a causal relation framing action')
# 							# print('best_action: ' + str(best_action))
# 							# print('impact_number: ' + str(impact_number))

# 							if links.agent1 == agents:
								
# 								# print('Before: ' + str(links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 										(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 										(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 										(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 										(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] = self.one_minus_one_check(links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
# 								agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][best_action] = links.agent2.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][best_action] = \
# 									self.one_minus_one_check(agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][best_action])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = \
# 									self.one_minus_one_check(links.agent2.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action])

# 								# print(' ')
# 								# print('Causal change')
# 								# print(agents.belieftree_policy[1 + links.agent2.unique_id])
# 								# print(agents.belieftree_policy[1 + links.agent2.unique_id][agents.select_policy_3S_as][best_action])

# 							# Checking which agent in the link is the original agent
# 							if links.agent2 == agents:

# 								# print('Before: ' + str(links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 										(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 										(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 										(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] += \
# 										(agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] - links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] = self.one_minus_one_check(links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
# 								agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][best_action] = links.agent1.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][best_action] = \
# 									self.one_minus_one_check(agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][best_action])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = agents.belieftree_policy[0][agents.select_policy_3S_as][best_action] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action] = \
# 									self.one_minus_one_check(links.agent1.belieftree_policy[1 + agents.unique_id][agents.select_policy_3S_as][best_action])

# 								# print(' ')
# 								# print('Causal change')
# 								# print(agents.belieftree_policy[1 + links.agent1.unique_id])
# 								# print(agents.belieftree_policy[1 + links.agent1.unique_id][agents.select_policy_3S_as][best_action])

# 						# If the index is in the second part of the list, then the aim influence action is the best
# 						if best_action == impact_number:
# 							# print(' ')
# 							# print('Performing a state change action')
# 							# print('best_action: ' + str(best_action))

# 							if links.agent1 == agents:

# 								# print('Before: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_as][1]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent2.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_as][1]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][agents.select_problem_3S_as][1] = self.one_minus_one_check(links.agent2.belieftree[0][agents.select_problem_3S_as][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1]
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1] = \
# 									self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = \
# 									self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])

# 								# print(' ')
# 								# print('Aim change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])

# 							if links.agent2 == agents:

# 								# print('Before: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_as][1]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][1] += (agents.belieftree[0][agents.select_problem_3S_as][1] - links.agent1.belieftree[0][agents.select_problem_3S_as][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_as][1]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][agents.select_problem_3S_as][1] = self.one_minus_one_check(links.agent1.belieftree[0][agents.select_problem_3S_as][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1]
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1] = \
# 									self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1] = \
# 									self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][1])


# 						# If the index is in the first part of the list, then the state influence action is the best
# 						if best_action == impact_number + 1:
# 							# print(' ')
# 							# print('Performing an aim change action')
# 							# print('best_action: ' + str(best_action))

# 							if links.agent1 == agents:
# 								# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent2.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][agents.select_problem_3S_as][0] = self.one_minus_one_check(links.agent2.belieftree[0][agents.select_problem_3S_as][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = links.agent2.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0] = \
# 									self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_as][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = \
# 									self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

# 								# print(' ')
# 								# print('State change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])

# 							if links.agent2 == agents:

# 								# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][agents.select_problem_3S_as][0] += (agents.belieftree[0][agents.select_problem_3S_as][0] - links.agent1.belieftree[0][agents.select_problem_3S_as][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][agents.select_problem_3S_as][0] = self.one_minus_one_check(links.agent1.belieftree[0][agents.select_problem_3S_as][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = links.agent1.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0] = \
# 									self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_as][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0] = \
# 									self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_as][0])

# 								# print(' ')
# 								# print('State change')
# 								# print(agents.belieftree[1 + links.agent1.unique_id])


# 			# agents.resources_actions -= agents.resources
# 			agents.resources_actions -= agents.resources[0] * resources_weight_action

# 	def pm_pe_actions_pf_3S(self, agents, link_list, deep_core, mid_level, secondary, resources_weight_action, resources_potency, agenda_prob_3S_as, affiliation_weights, conflict_level_coef):

# 		"""
# 		The PEs and PMs actions function - three streams (policy formulation)
# 		===========================

# 		This function is used to perform the different active actions of the
# 		policy entrepreneurs and the policy makers during the policy formulation.

# 		The actions that can be performed are framing, influence on states and 
# 		influence on aims. All of the actions are first graded. Then the action
# 		that has the highest grade is selected. Finally, the action selected 
# 		is implemented.

# 		Note: This function is the same as the one presented before for the backbone
# 		backbone+ and ACF. The main difference is the addition of actions related
# 		to the choice of a policy by the agents.

# 		"""

# 		len_PC = len(deep_core)
# 		len_ML = len(mid_level)
# 		len_S = len(secondary)
# 		total_issue_number = len_PC + len_ML + len_S

# 		# Selection of the cw of interest
# 		cw_of_interest = []
# 		# Select one by one the Pr
# 		j = agenda_prob_3S_as
# 		# for j in range(len_ML):
# 		# Selecting the causal relations starting from Pr
# 		for k in range(len_S):
# 			# Contingency for partial knowledge issues
# 			# print(len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML)
# 			if (agents.belieftree[0][len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML][0] < 0 and (agents.belieftree[0][j][1] - agents.belieftree[0][j][0]) < 0) \
# 			  or (agents.belieftree[0][len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML][0] > 0 and (agents.belieftree[0][j][1] - agents.belieftree[0][j][0]) > 0):
# 				cw_of_interest.append(len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML)

# 		# Selection of the impact of interest
# 		impact_number = len(agents.belieftree_instrument[0][agents.select_policy_3S_pf])

# 		# print(' ')
# 		# print('Causal relations of interest: ' + str(cw_of_interest))

# 		# Making sure there are enough resources
# 		while agents.resources_actions > 0.001:

# 			# Going through all the links in the model
# 			# print(agents)
# 			total_grade_list = []
# 			total_grade_list_links = []
# 			for links in link_list:

# 				# Making sure that the link is attached to the agent and has a aware higher than 0
# 				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
# 					total_grade_list_links.append(links)

# 					# Definition the action weight parameter
# 					if type(links.agent1) == Policymakers or type(links.agent2) == Policymakers:
# 						actionWeight = 1
# 					else:
# 						actionWeight = 0.95
					
# 					# 1. Framing on causal relation and policy impacts

# 					# If the agent is advocating or a problem, the following tasks are performed
# 					if agents.select_issue_3S_pf == 'problem':
# 						# 1.a. Grading all framing actions on causal relations:
# 						# Checking through all possible framing - This is all based on partial knowledge!
# 						for cw in range(len(cw_of_interest)):

# 							# Checking which agent in the link is the original agent
# 							if links.agent1 == agents:

# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									cw_grade = links.conflict_level[0][cw_of_interest[cw]][0] * links.aware * actionWeight
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									cw_grade = links.conflict_level[0][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[0]
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									cw_grade = links.conflict_level[0][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[1]
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									cw_grade = links.conflict_level[0][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[2]
# 									total_grade_list.append(cw_grade)	


# 								# # Check if no partial knowledge (initial value)
# 								# check_none = 0
# 								# if agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] == None:
# 								# 	agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = 0
# 								# 	check_none = 1
# 								# # Performing the action
# 								# cw_grade = (agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0]) * \
# 								# 	agents.resources[0] * resources_weight_action * links.aware * resources_potency
# 								# # Adding the grade to the grade list
# 								# total_grade_list.append(cw_grade)
# 								# #  Reset to None after finding the grade
# 								# if check_none == 1:
# 								# 	agents.belieftree[1 + links.agent2.unique_id][cw_of_interest[cw]][0] = None

# 							# Checking which agent in the link is the original agent
# 							if links.agent2 == agents:

# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									cw_grade = links.conflict_level[1][cw_of_interest[cw]][0] * links.aware * actionWeight
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									cw_grade = links.conflict_level[1][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[0]
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									cw_grade = links.conflict_level[1][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[1]
# 									total_grade_list.append(cw_grade)

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									cw_grade = links.conflict_level[1][cw_of_interest[cw]][0] * links.aware * actionWeight * affiliation_weights[2]
# 									total_grade_list.append(cw_grade)	


# 								# #  Check if no partial knowledge (initial value)
# 								# check_none = 0
# 								# if agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] == None:
# 								# 	agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = 0
# 								# 	check_none = 1
# 								# # Performing the action
# 								# cw_grade = (agents.belieftree[0][cw_of_interest[cw]][0] - agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0]) * \
# 								# 	agents.resources[0] * resources_weight_action * links.aware * resources_potency
# 								# # Adding the grade to the grade list
# 								# total_grade_list.append(cw_grade)
# 								# # Reset to None after finding the grade
# 								# if check_none == 1:
# 								# 	agents.belieftree[1 + links.agent1.unique_id][cw_of_interest[cw]][0] = None

# 					# If the agent is advocating or a policy, the following tasks are performed
# 					if agents.select_issue_3S_pf == 'policy':
# 						# 1.b. Grading all framing actions on policy impacts:
						
# 						# Checking through all possible framing - This is all based on partial knowledge!
# 						for impact in range(impact_number):

# 							# Checking which agent in the link is the original agent
# 							if links.agent1 == agents:

# 								# Need to calculate the conflict level per impact (to avoid having to create a whole new conflict level array in the links for the policies)
# 								# Note that there is currently a need to check for None partial knowledge

# 								check_none = 0
# 								if agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] == None:
# 									agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] = 0
# 									check_none = 1
 
# 								belief_diff = abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][impact] - agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact])

# 								if check_none == 1:
# 									agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] = None

# 								if belief_diff <= 0.25:
# 									conflict_level_impact = conflict_level_coef[0]
# 								if belief_diff > 0.25 and belief_diff <= 1.75:
# 									conflict_level_impact = conflict_level_coef[2]
# 								if belief_diff > 1.75:
# 									conflict_level_impact = conflict_level_coef[1]

# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									impact_grade = conflict_level_impact * links.aware * actionWeight
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[0]
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[1]
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[2]
# 									total_grade_list.append(impact_grade)	

# 								# # Check if no partial knowledge (initial value)
# 								# check_none = 0
# 								# if agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] == None:
# 								# 	agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] = 0
# 								# 	check_none = 1
# 								# # Performing the action
# 								# impact_grade = (agents.belieftree_instrument[0][agents.select_policy_3S_pf][impact] - agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact]) * \
# 								# 	agents.resources[0] * resources_weight_action * links.aware * resources_potency
# 								# # Adding the grade to the grade list
# 								# total_grade_list.append(impact_grade)
# 								# #  Reset to None after finding the grade
# 								# if check_none == 1:
# 								# 	agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][impact] = None

# 							# Checking which agent in the link is the original agent
# 							if links.agent2 == agents:

# 								# Need to calculate the conflict level per impact (to avoid having to create a whole new conflict level array in the links for the policies)
# 								# Note that there is currently a need to check for None partial knowledge

# 								check_none = 0
# 								if agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] == None:
# 									agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] = 0
# 									check_none = 1
 
# 								belief_diff = abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][impact] - agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact])

# 								if check_none == 1:
# 									agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] = None

# 								if belief_diff <= 0.25:
# 									conflict_level_impact = conflict_level_coef[0]
# 								if belief_diff > 0.25 and belief_diff <= 1.75:
# 									conflict_level_impact = conflict_level_coef[2]
# 								if belief_diff > 1.75:
# 									conflict_level_impact = conflict_level_coef[1]

# 								# Grade calculation using the likelihood method
# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									impact_grade = conflict_level_impact * links.aware * actionWeight
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[0]
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[1]
# 									total_grade_list.append(impact_grade)

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[2]
# 									total_grade_list.append(impact_grade)	


# 								# #  Check if no partial knowledge (initial value)
# 								# check_none = 0
# 								# if agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] == None:
# 								# 	agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] = 0
# 								# 	check_none = 1
# 								# impact_grade = (agents.belieftree_instrument[0][agents.select_policy_3S_pf][impact] - agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact]) * \
# 								# 	agents.resources[0] * resources_weight_action * links.aware * resources_potency
# 								# # Adding the grade to the grade list
# 								# total_grade_list.append(impact_grade)
# 								# # Reset to None after finding the grade
# 								# if check_none == 1:
# 								# 	agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][impact] = None

# 					# 2. Grading all individual actions - Aim change
# 					if links.agent1 == agents:

# 						# Grade calculation using the likelihood method
# 						# Same affiliation
# 						if links.agent1.affiliation == links.agent2.affiliation:
# 							aim_grade_issue = links.conflict_level[0][agents.select_problem_3S_pf][1] * links.aware * actionWeight
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 1-2
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 							(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 							aim_grade_issue = links.conflict_level[0][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[0]
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 1-3
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 							aim_grade_issue = links.conflict_level[0][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[1]
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 2-3
# 						if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 							aim_grade_issue = links.conflict_level[0][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[2]
# 							total_grade_list.append(aim_grade_issue)	


# 						# # Check if no partial knowledge (initial value)
# 						# check_none = 0
# 						# if agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] == None:
# 						# 	agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = 0
# 						# 	check_none = 1
# 						# # Performing the action
# 						# aim_grade_issue = (agents.belieftree[0][agents.select_problem_3S_pf][1] - agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1]) * \
# 						# 	agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_problem_3S_pf][1] * actionWeight * resources_potency
# 						# #  Reset to None after finding the grade
# 						# if check_none == 1:
# 						# 	agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = None
# 						# # Adding the grade to the grade list
# 						# total_grade_list.append(aim_grade_issue)

# 					if links.agent2 == agents:

# 						# Grade calculation using the likelihood method
# 						# Same affiliation
# 						if links.agent1.affiliation == links.agent2.affiliation:
# 							aim_grade_issue = links.conflict_level[1][agents.select_problem_3S_pf][1] * links.aware * actionWeight
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 1-2
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 							(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 							aim_grade_issue = links.conflict_level[1][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[0]
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 1-3
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 							aim_grade_issue = links.conflict_level[1][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[1]
# 							total_grade_list.append(aim_grade_issue)

# 						# Affiliation 2-3
# 						if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 							aim_grade_issue = links.conflict_level[1][agents.select_problem_3S_pf][1] * links.aware * actionWeight * affiliation_weights[2]
# 							total_grade_list.append(aim_grade_issue)


# 						# # Check if no partial knowledge (initial value)
# 						# check_none = 0
# 						# if agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] == None:
# 						# 	agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = 0
# 						# 	check_none = 1
# 						# # Performing the action
# 						# aim_grade_issue = (agents.belieftree[0][agents.select_problem_3S_pf][1] - agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1]) * \
# 						# 	agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_problem_3S_pf][1] * actionWeight * resources_potency
# 						# #  Reset to None after finding the grade
# 						# if check_none == 1:
# 						# 	agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = None
# 						# # Adding the grade to the grade list
# 						# total_grade_list.append(aim_grade_issue)

# 					# 3. Grading all individual actions - State change
# 					if links.agent1 == agents:

# 						# Grade calculation using the likelihood method
# 						# Same affiliation
# 						if links.agent1.affiliation == links.agent2.affiliation:
# 							state_grade_issue = links.conflict_level[0][agents.select_problem_3S_pf][0] * links.aware * actionWeight
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 1-2
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 							(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 							state_grade_issue = links.conflict_level[0][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[0]
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 1-3
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 							state_grade_issue = links.conflict_level[0][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[1]
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 2-3
# 						if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 							state_grade_issue = links.conflict_level[0][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[2]
# 							total_grade_list.append(state_grade_issue)

# 						# # Check if no partial knowledge (initial value)
# 						# check_none = 0
# 						# if agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] == None:
# 						# 	agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = 0
# 						# 	check_none = 1
# 						# # Performing the action
# 						# state_grade_issue = (agents.belieftree[0][agents.select_problem_3S_pf][0] - agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0]) * \
# 						# 	agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[0][agents.select_problem_3S_pf][0] * actionWeight * resources_potency
# 						# #  Reset to None after finding the grade
# 						# if check_none == 1:
# 						# 	agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = None
# 						# # Adding the grade to the grade list
# 						# total_grade_list.append(state_grade_issue)

# 					if links.agent2 == agents:

# 						# Grade calculation using the likelihood method
# 						# Same affiliation
# 						if links.agent1.affiliation == links.agent2.affiliation:
# 							state_grade_issue = links.conflict_level[1][agents.select_problem_3S_pf][0] * links.aware * actionWeight
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 1-2
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 							(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 							state_grade_issue = links.conflict_level[1][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[0]
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 1-3
# 						if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 							state_grade_issue = links.conflict_level[1][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[1]
# 							total_grade_list.append(state_grade_issue)

# 						# Affiliation 2-3
# 						if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 							(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 							state_grade_issue = links.conflict_level[1][agents.select_problem_3S_pf][0] * links.aware * actionWeight * affiliation_weights[2]
# 							total_grade_list.append(state_grade_issue)


# 						# # Check if no partial knowledge (initial value)
# 						# check_none = 0
# 						# if agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] == None:
# 						# 	agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = 0
# 						# 	check_none = 1
# 						# # Performing the action
# 						# state_grade_issue = (agents.belieftree[0][agents.select_problem_3S_pf][0] - agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0]) * \
# 						# 	agents.resources[0] * resources_weight_action * links.aware * links.conflict_level[1][agents.select_problem_3S_pf][0] * actionWeight * resources_potency
# 						# #  Reset to None after finding the grade
# 						# if check_none == 1:
# 						# 	agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = None
# 						# # Adding the grade to the grade list
# 						# total_grade_list.append(state_grade_issue)

# 					# print(' ')


# 			# 4. Choosing an action

# 			# If the agent is advocating or a problem, the following tasks are performed
# 			if agents.select_issue_3S_as == 'problem':

# 				best_action_index = total_grade_list.index(max(total_grade_list))
# 				agent_best_action = int(best_action_index/(len(cw_of_interest) + 1 + 1))
# 				best_action = best_action_index - (agent_best_action)*(len(cw_of_interest) + 1 + 1)

# 				# print(' ')
# 				# print('----- Considering new action grading (problem) -----')
# 				# print('best_action_index: ' + str(best_action_index))
# 				# print('Number of actions per agent: ' + str(len(cw_of_interest) + 1 + 1))
# 				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
# 				# print('Action to be performed: ' + str(best_action))
# 				# print('Agent performing the action: ' + str(agent_best_action))

# 			# If the agent is advocating or a policy, the following tasks are performed
# 			if agents.select_issue_3S_as == 'policy':
				
# 				best_action_index = total_grade_list.index(max(total_grade_list))
# 				agent_best_action = int(best_action_index/(impact_number + 1 + 1))
# 				best_action = best_action_index - (agent_best_action)*(impact_number + 1 + 1)

# 				# print(' ')
# 				# print('----- Considering new action grading (policy) -----')
# 				# print('best_action_index: ' + str(best_action_index))
# 				# print('Number of actions per agent: ' + str(impact_number + 1 + 1))
# 				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
# 				# print('Action to be performed: ' + str(best_action))
# 				# print('Agent performing the action: ' + str(agent_best_action))

# 			# 5. Performing the actual action
# 			# Selecting the link:
# 			for links in link_list:

# 				# If the agent is advocating or a problem, the following tasks are performed
# 				if agents.select_issue_3S_pf == 'problem':

# 					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
# 						# print(links)

# 						# Updating the aware decay parameter
# 						links.aware_decay = 5

# 						# If the index is in the first part of the list, then the framing action is the best
# 						if best_action <= len(cw_of_interest) - 1:
# 							# print(' ')
# 							# print('Performing a causal relation framing action')
# 							# print('best_action: ' + str(best_action))
# 							# print('cw_of_interest: ' + str(cw_of_interest))
# 							# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))
							
# 							# To simplify the notations
# 							best_action = cw_of_interest[best_action]

# 							if links.agent1 == agents:
								
# 								# print('Before: ' + str(links.agent2.belieftree[0][best_action][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent2.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]
									
# 								# print('After: ' + str(links.agent2.belieftree[0][best_action][0]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][best_action][0] = self.one_minus_one_check(links.agent2.belieftree[0][best_action][0])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][best_action][0] = links.agent2.belieftree[0][best_action][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][best_action][0] = self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][best_action][0])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][best_action][0] = self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][best_action][0])

# 								# print(' ')
# 								# print('Causal change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])
# 								# print(agents.belieftree[1 + links.agent2.unique_id][best_action][0])

# 							# Checking which agent in the link is the original agent
# 							if links.agent2 == agents:
# 								# print('Before: ' + str(links.agent1.belieftree[0][best_action][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][best_action][0] += (agents.belieftree[0][best_action][0] - links.agent1.belieftree[0][best_action][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][best_action][0]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][best_action][0] = self.one_minus_one_check(links.agent1.belieftree[0][best_action][0])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][best_action][0] = links.agent1.belieftree[0][best_action][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][best_action][0] = self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][best_action][0])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][best_action][0] = agents.belieftree[0][best_action][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][best_action][0] = self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][best_action][0])

# 								# print(' ')
# 								# print('Causal change')
# 								# print(agents.belieftree[1 + links.agent1.unique_id])
# 								# print(agents.belieftree[1 + links.agent1.unique_id][best_action][0])

# 						# If the index is in the second part of the list, then the aim influence action is the best
# 						if best_action == len(cw_of_interest):
# 							# print(' ')
# 							# print('Performing a state change action')
# 							# print('best_action: ' + str(best_action))

# 							if links.agent1 == agents:
# 								# print('Before: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_pf][1]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_pf][1]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][agents.select_problem_3S_pf][1] = self.one_minus_one_check(links.agent2.belieftree[0][agents.select_problem_3S_pf][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1]
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])

# 								# print(' ')
# 								# print('Aim change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])

# 							if links.agent2 == agents:
# 								# print('Before: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_pf][1]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_pf][1]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][agents.select_problem_3S_pf][1] = self.one_minus_one_check(links.agent1.belieftree[0][agents.select_problem_3S_pf][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1]
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])


# 						# If the index is in the first part of the list, then the state influence action is the best
# 						if best_action == len(cw_of_interest) + 1:
# 							# print(' ')
# 							# print('Performing an aim change action')
# 							# print('best_action: ' + str(best_action))

# 							if links.agent1 == agents:
# 								# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][agents.select_problem_3S_pf][0] = self.one_minus_one_check(links.agent2.belieftree[0][agents.select_problem_3S_pf][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = links.agent2.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

# 								# print(' ')
# 								# print('State change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])

# 							if links.agent2 == agents:
# 								# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][agents.select_problem_3S_pf][0] = self.one_minus_one_check(links.agent1.belieftree[0][agents.select_problem_3S_pf][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = links.agent1.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

# 								# print(' ')
# 								# print('State change')
# 								# print(agents.belieftree[1 + links.agent1.unique_id])

# 				# If the agent is advocating or a policy, the following tasks are performed
# 				if agents.select_issue_3S_pf == 'policy':
					
# 					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
# 						# print(links)

# 						# Updating the aware decay parameter
# 						links.aware_decay = 5

# 						# If the index is in the first part of the list, then the framing action is the best
# 						if best_action <= impact_number - 1:
# 							# print(' ')
# 							# print('Performing a causal relation framing action')
# 							# print('best_action: ' + str(best_action))
# 							# print('impact_number: ' + str(impact_number))

# 							if links.agent1 == agents:
								
# 								# print('Before: ' + str(links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 										(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 										(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 										(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 										(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] = self.one_minus_one_check(links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
# 								agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][best_action] = links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][best_action] = \
# 									self.one_minus_one_check(agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][best_action])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = \
# 									self.one_minus_one_check(links.agent2.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action])

# 								# print(' ')
# 								# print('Causal change')
# 								# print(agents.belieftree_instrument[1 + links.agent2.unique_id])
# 								# print(agents.belieftree_instrument[1 + links.agent2.unique_id][agents.select_policy_3S_pf][best_action])

# 							# Checking which agent in the link is the original agent
# 							if links.agent2 == agents:

# 								# print('Before: ' + str(links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 										(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 										(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 										(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] += \
# 										(agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] - links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] = self.one_minus_one_check(links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acting agent)
# 								agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][best_action] = links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][best_action] = \
# 									self.one_minus_one_check(agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][best_action])
# 								# Providing partial knowledge - Framing - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = agents.belieftree_instrument[0][agents.select_policy_3S_pf][best_action] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action] = \
# 									self.one_minus_one_check(links.agent1.belieftree_instrument[1 + agents.unique_id][agents.select_policy_3S_pf][best_action])

# 								# print(' ')
# 								# print('Causal change')
# 								# print(agents.belieftree_instrument[1 + links.agent1.unique_id])
# 								# print(agents.belieftree_instrument[1 + links.agent1.unique_id][agents.select_policy_3S_pf][best_action])

# 						# If the index is in the second part of the list, then the aim influence action is the best
# 						if best_action == impact_number:
# 							# print(' ')
# 							# print('Performing a state change action')
# 							# print('best_action: ' + str(best_action))

# 							if links.agent1 == agents:
# 								# print('Before: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_pf][1]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent2.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][agents.select_problem_3S_pf][1]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][agents.select_problem_3S_pf][1] = self.one_minus_one_check(links.agent2.belieftree[0][agents.select_problem_3S_pf][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1]
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1] = \
# 									self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = \
# 									self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])

# 								# print(' ')
# 								# print('Aim change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])

# 							if links.agent2 == agents:

# 								# print('Before: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_pf][1]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][1] += (agents.belieftree[0][agents.select_problem_3S_pf][1] - links.agent1.belieftree[0][agents.select_problem_3S_pf][1]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][agents.select_problem_3S_pf][1]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][agents.select_problem_3S_pf][1] = self.one_minus_one_check(links.agent1.belieftree[0][agents.select_problem_3S_pf][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1]
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1] = \
# 									self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][1])
# 								# Providing partial knowledge - Aim problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1] = \
# 									self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][1])


# 						# If the index is in the first part of the list, then the state influence action is the best
# 						if best_action == impact_number + 1:
# 							# print(' ')
# 							# print('Performing an aim change action')
# 							# print('best_action: ' + str(best_action))

# 							if links.agent1 == agents:
# 								# print('Before: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent2.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent2.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent2.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent2.belieftree[0][agents.select_problem_3S_pf][0] = self.one_minus_one_check(links.agent2.belieftree[0][agents.select_problem_3S_pf][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = links.agent2.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0] = \
# 									self.one_minus_one_check(agents.belieftree[1 + links.agent2.unique_id][agents.select_problem_3S_pf][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = \
# 									self.one_minus_one_check(links.agent2.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

# 								# print(' ')
# 								# print('State change')
# 								# print(agents.belieftree[1 + links.agent2.unique_id])

# 							if links.agent2 == agents:
# 								# print('Before: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))

# 								# Same affiliation
# 								if links.agent1.affiliation == links.agent2.affiliation:
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency

# 								# Affiliation 1-2
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
# 									(links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[0]

# 								# Affiliation 1-3
# 								if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[1]

# 								# Affiliation 2-3
# 								if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
# 									(links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
# 									links.agent1.belieftree[0][agents.select_problem_3S_pf][0] += (agents.belieftree[0][agents.select_problem_3S_pf][0] - links.agent1.belieftree[0][agents.select_problem_3S_pf][0]) * \
# 										agents.resources[0] * resources_weight_action * resources_potency * affiliation_weights[2]

# 								# print('After: ' + str(links.agent1.belieftree[0][len(self.deep_core) + agents.select_problem][0]))
								
# 								# Checks and transfer of partial knowledge
# 								# 1-1 check
# 								links.agent1.belieftree[0][agents.select_problem_3S_pf][0] = self.one_minus_one_check(links.agent1.belieftree[0][agents.select_problem_3S_pf][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acting agent)
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = links.agent1.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0] = \
# 									self.one_minus_one_check(agents.belieftree[1 + links.agent1.unique_id][agents.select_problem_3S_pf][0])
# 								# Providing partial knowledge - State problem - 0.2 range from real value: (Acted upon agent)
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/5) - 0.1
# 								# 1-1 check
# 								links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0] = \
# 									self.one_minus_one_check(links.agent1.belieftree[1 + agents.unique_id][agents.select_problem_3S_pf][0])

# 								# print(' ')
# 								# print('State change')
# 								# print(agents.belieftree[1 + links.agent1.unique_id])



# 			# agents.resources_actions -= agents.resources
# 			agents.resources_actions -= agents.resources[0] * resources_weight_action

# 	def preference_udapte_as_PC(self, agent, who, len_PC, len_ML, len_S):

# 		"""
# 		The preference update for policy cores function (agenda setting)
# 		===========================

# 		This function is used to update the policy core preferences. It is only used for the
# 		old way of calculating the grade actions.
	
# 		Note: This function will ultimately be removed once all grading actions have been
# 		modified.

# 		"""

# 		# Preference calculation for the policy core issues
# 		PC_denominator = 0
# 		# Select one by one the Pr
# 		for j in range(len_ML):
# 			PC_denominator = 0
# 			# Selecting the causal relations starting from Pr
# 			for k in range(len_PC):
# 				# Contingency for partial knowledge issues
# 				if agent.belieftree[who][k][1] == None or agent.belieftree[who][k][0] == None or agent.belieftree[who][len_PC+len_ML+len_S+j+(k*len_ML)][0] == None:
# 					PC_denominator = 0
# 				else:
# 					# Check if causal relation and gap are both positive of both negative
# 					if (agent.belieftree[who][len_PC+len_ML+len_S+j+(k*len_ML)][0] < 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) < 0) \
# 					  or (agent.belieftree[who][len_PC+len_ML+len_S+j+(k*len_ML)][0] > 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) > 0):
# 						PC_denominator = PC_denominator + abs(agent.belieftree[who][len_PC+len_ML+len_S+j+(k*len_ML)][0]*\
# 						  (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]))
# 					else:
# 						PC_denominator = PC_denominator	
# 		# Then adding the gap of the policy core:
# 		for i in range(len_ML):
# 			# Contingency for partial knowledge issues
# 			if agent.belieftree[who][len_PC + i][1] == None or agent.belieftree[who][len_PC + i][0] == None:
# 				PC_denominator = PC_denominator
# 			else:
# 				PC_denominator = PC_denominator + abs(agent.belieftree[who][len_PC + i][1] - agent.belieftree[who][len_PC + i][0])
		
# 		# Calculating the numerator and the preference of all policy core issues:
# 		# Select one by one the Pr
# 		for j in range(len_ML):
# 			PC_numerator = 0
# 			# Selecting the causal relations starting from Pr
# 			for k in range(len_PC):
# 				# Contingency for partial knowledge issues
# 				if agent.belieftree[who][k][1] == None or agent.belieftree[who][k][0] == None or agent.belieftree[who][len_PC+len_ML+len_S+j+(k*len_ML)][0] == None: 
# 					PC_numerator = 0
# 				else:
# 					# Check if causal relation and gap are both positive of both negative
# 					if (agent.belieftree[who][len_PC+len_ML+len_S+j+(k*len_ML)][0] < 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) < 0) \
# 					  or (agent.belieftree[who][len_PC+len_ML+len_S+j+(k*len_ML)][0] > 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) > 0):
# 						PC_numerator = PC_numerator + abs(agent.belieftree[who][len_PC+len_ML+len_S+j+(k*len_ML)][0]*\
# 						  (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]))
# 					else:
# 						PC_numerator = PC_numerator	
# 			# Contingency for partial knowledge issues
# 			if agent.belieftree[who][len_PC + j][1] == None or agent.belieftree[who][len_PC + j][0] == None:
# 				PC_numerator = 0
# 			else:
# 				# Then adding the gap of the policy core:
# 				PC_numerator = PC_numerator + abs(agent.belieftree[who][len_PC + j][1] - agent.belieftree[who][len_PC + j][0])
# 			if PC_denominator != 0:
# 				agent.belieftree[who][len_PC+j][2] = PC_numerator/PC_denominator 
# 			else:
# 				agent.belieftree[who][len_PC+j][2] = 0

# 	def preference_udapte_pf_PC(self, agent, who, len_PC, len_ML, len_S, agenda_prob_3S_as):

# 		"""
# 		The preference update for policy cores function (policy formulation)
# 		===========================

# 		This function is used to update the policy core preferences. It is only used for the
# 		old way of calculating the grade actions.
	
# 		Note: This function will ultimately be removed once all grading actions have been
# 		modified.

# 		"""

# 		k = agenda_prob_3S_as

# 		# Calculating the numerator and the preference of all policy core issues:
# 		# Select one by one the Pr
# 		S_denominator = 0
# 		for j in range(len_S):
# 			# print('Selection S' + str(j+1))
# 			# print('State of the S' + str(j+1) + ': ' + str(agent.belieftree[0][len_PC + j][0])) # the state printed
# 			# Selecting the causal relations starting from PC
# 			# print(' ')
# 			# print(len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC))
# 			# Contingency for partial knowledge issues
# 			if agent.belieftree[0][k][1] != None and agent.belieftree[0][k][0] != None and agent.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC)][0] != None:
# 				# print('Causal Relation S' + str(j+1) + ' - PC' + str(k+1) + ': ' + str(agent.belieftree[0][len_PC+len_ML+len_S+(j+(k*len_ML))][0]))
# 				# print('Gap of PC' + str(k+1) + ': ' + str(agent.belieftree[0][k][1] - agent.belieftree[0][k][0]))
# 				# Check if causal relation and gap are both positive of both negative
# 				if (agent.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC)][0] < 0 and (agent.belieftree[0][k][1] - agent.belieftree[0][k][0]) < 0) \
# 					or (agent.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC)][0] > 0 and (agent.belieftree[0][k][1] - agent.belieftree[0][k][0]) > 0):
# 					# print('Calculating')
# 					S_denominator = S_denominator + abs(agent.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC)][0] * \
# 						(agent.belieftree[0][k][1] - agent.belieftree[0][k][0]))
# 					# print('This is the PC numerator: ' + str(S_denominator))
# 				else:
# 					S_denominator = S_denominator
# 			else:
# 				S_denominator = 0
# 			# Contingency for partial knowledge issues
# 			if agent.belieftree[0][len_PC + len_ML + j][1] == None or agent.belieftree[0][len_PC + len_ML + j][0] == None:
# 				S_denominator = S_denominator
# 			else:
# 				# Then adding the gap of the policy core:
# 				# print('This is the gap for the S' + str(j+1) + ': ' + str(agent.belieftree[0][len_PC + len_ML + j][1] - agent.belieftree[0][len_PC + len_ML + j][0]))
# 				S_denominator = S_denominator + abs(agent.belieftree[0][len_PC + len_ML + j][1] - agent.belieftree[0][len_PC + len_ML + j][0])


# 		# Calculating the numerator and the preference of all policy core issues:
# 		# Select one by one the Pr
# 		for j in range(len_S):
# 			S_numerator = 0
# 			# Contingency for partial knowledge issues
# 			if agent.belieftree[0][k][1] != None and agent.belieftree[0][k][0] != None and agent.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC)][0] != None:
# 				# Check if causal relation and gap are both positive of both negative
# 				if (agent.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC)][0] < 0 and (agent.belieftree[0][k][1] - agent.belieftree[0][k][0]) < 0) \
# 					or (agent.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC)][0] > 0 and (agent.belieftree[0][k][1] - agent.belieftree[0][k][0]) > 0):
# 					# print('Calculating')
# 					S_numerator = S_numerator + abs(agent.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + j*len_ML + (k-len_PC)][0] * \
# 						(agent.belieftree[0][k][1] - agent.belieftree[0][k][0]))
# 					# print('This is the PC numerator: ' + str(S_numerator))
# 				else:
# 					S_numerator = S_numerator
# 			else:
# 				S_numerator = 0
# 			# Contingency for partial knowledge issues
# 			if agent.belieftree[0][len_PC + len_ML + j][1] == None or agent.belieftree[0][len_PC + len_ML + j][0] == None:
# 				S_numerator = 0
# 			else:
# 				# Then adding the gap of the policy core:
# 				S_numerator = S_numerator + abs(agent.belieftree[0][len_PC + len_ML + j][1] - agent.belieftree[0][len_PC + len_ML + j][0])
# 			if S_denominator != 0:
# 				agent.belieftree[who][len_PC + len_ML + j][2] = S_numerator/S_denominator 
# 			else:
# 				agent.belieftree[who][len_PC + len_ML + j][2] = 0

# 	def instrument_preference_update(self, agent, who, AS_theory, len_PC, len_ML, len_S, instruments):

# 		"""
# 		Instrument preference update function
# 		===========================

# 		This function is used to calculate the ranking of each of the instrument from 
# 		which the agents can choose from. This is done in two parts.

# 		1/ The first part consists of calculating the preference level for the different
# 		secondary issues (layer 3 in the belief tree). In this part, the preferences of
# 		the agents are updated similarly to the function where the preferences are calculated.
# 		The main difference is that this time, it is based on the agenda which means that
# 		only the secondary issues affecting the problem on the agenda are considered.

# 		2/ The second part consists of obtaining the grade for the policy instruments.
# 		This is calculated as shown in the formalisation with the equation given by:
# 		G = sum(impact * (Aim - State) * Preference_secondary)
# 		We make sure that the instruments impact are only taken into account if the
# 		impact is of the same sign as the gap between the state and the aim for the
# 		specific secondary issues. If this is not the case, the impact is not considered
# 		for that specific part of the instrument.

# 		Notes:
# 		1/ The secondary issues for which the agent is not interested (this applies to 
# 		the external parties only) are not taken into account in the calculation. They
# 		are marked as the 'No' values.

# 		This function will ultimately be removed when all of the grading actions will be
# 		modified.

# 		"""

# 		######################################################################################################
# 		# 1/ Calculation of the preference level for the secondary issues based on the problem on the agenda #
# 		######################################################################################################

# 		S_denominator = 0
# 		if AS_theory != 2:
# 			j = agent.select_as_issue
# 		if AS_theory == 2:
# 			j = agent.select_problem_3S_as
# 		for k in range(len_S):
# 			if agent.belieftree[who][j][1] != None and agent.belieftree[who][j][0] != None and agent.belieftree[who][len_PC + len_ML + len_S + (len_PC*len_ML) + (j - len_PC)*len_S + k][0] != None:
# 				if (agent.belieftree[who][len_PC + len_ML + len_S + (len_PC*len_ML) + (j - len_PC)*len_S + k][0] < 0 and (agent.belieftree[who][j][1] - agent.belieftree[who][j][0]) < 0) \
# 					or (agent.belieftree[who][len_PC + len_ML + len_S + (len_PC*len_ML) + (j - len_PC)*len_S + k][0] > 0 and (agent.belieftree[who][j][1] - agent.belieftree[who][j][0]) > 0):
# 					S_denominator = S_denominator + abs(agent.belieftree[who][len_PC + len_ML + len_S + (len_PC*len_ML) + (j - len_PC)*len_S + k][0]*\
# 					  (agent.belieftree[who][j][1] - agent.belieftree[who][j][0]))
# 				else:
# 					S_denominator = S_denominator
# 			else:
# 				S_denominator = S_denominator

# 		for i in range(len_S):
# 			if agent.belieftree[who][len_PC + len_ML + i][0] != 'No':
# 				if agent.belieftree[who][len_PC + len_ML + i][1] != None and agent.belieftree[who][len_PC + len_ML + i][0] != None:
# 					S_denominator = S_denominator + abs(agent.belieftree[who][len_PC + len_ML + i][1] - agent.belieftree[who][len_PC + len_ML + i][0])
# 				else:
# 					S_denominator = 0

# 		S_numerator = 0
		
# 		for j in range(len_S):
# 			S_numerator = 0
# 			if AS_theory != 2:
# 				k = agent.select_as_issue
# 			if AS_theory == 2:
# 				k = agent.select_problem_3S_as
# 			if agent.belieftree[who][k][1] != None and agent.belieftree[who][k][0] != None and agent.belieftree[who][len_PC + len_ML + len_S + (len_PC*len_ML) + (k - len_PC)*len_S + j][0] != None:
# 				if (agent.belieftree[who][len_PC + len_ML + len_S + (len_PC*len_ML) + (k - len_PC)*len_S + j][0] < 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) < 0) \
# 					or (agent.belieftree[who][len_PC + len_ML + len_S + (len_PC*len_ML) + (k - len_PC)*len_S + j][0] > 0 and (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]) > 0):
# 					S_numerator = S_numerator + abs(agent.belieftree[who][len_PC + len_ML + len_S + (len_PC*len_ML) + (k - len_PC)*len_S + j][0]*\
# 						  (agent.belieftree[who][k][1] - agent.belieftree[who][k][0]))
# 				else:
# 					S_numerator = S_numerator
# 			else:
# 				S_numerator = S_numerator
# 			if agent.belieftree[who][len_PC + len_ML + j][0] != 'No':
# 				if agent.belieftree[who][len_PC + len_ML + j][1] != None and agent.belieftree[who][len_PC + len_ML + j][0] != None:
# 					S_numerator = S_numerator + abs(agent.belieftree[who][len_PC + len_ML + j][1] - agent.belieftree[who][len_PC + len_ML + j][0])
# 				else:
# 					S_numerator = 0
# 			if S_denominator != 0:
# 				agent.belieftree[who][len_PC+len_ML+j][2] = S_numerator/S_denominator 
# 			else:
# 				agent.belieftree[who][len_PC+len_ML+j][2] = 0

# 		##################################################################################################
# 		# 2/ Calculation of the grade of each of the instruments based on impact on the secondary issues #
# 		##################################################################################################

# 		agent.instrument_preferences[who] = [0 for h in range(len(instruments))]
# 		for i in range(len(instruments)):
# 			for j in range(len_S):
# 				if agent.belieftree[who][len_PC + len_ML + j][0] != 'No':
# 					if agent.belieftree[who][len_PC + len_ML + j][1] != None and agent.belieftree[who][len_PC + len_ML + j][0] != None:
# 						if (instruments[i][j] > 0 and (agent.belieftree[who][len_PC + len_ML + j][1] - agent.belieftree[who][len_PC + len_ML + j][0]) > 0 ) \
# 							or (instruments[i][j] < 0 and (agent.belieftree[who][len_PC + len_ML + j][1] - agent.belieftree[who][len_PC + len_ML + j][0]) < 0 ):
# 							# print(' ')
# 							# print('agent.instrument_preferences[who][i]: ' + str(agent.instrument_preferences[who][i]))
# 							# print('instruments[i][j]: ' + str(instruments[i][j]))
# 							# print('agent.belieftree[' + str(who) + '][len_PC + len_ML + ' + str(j) + '][1]: ' + str(agent.belieftree[who][len_PC + len_ML + j][1]))
# 							# print('agent.belieftree[' + str(who) + '][len_PC + len_ML + ' + str(j) + '][0]: ' + str(agent.belieftree[who][len_PC + len_ML + j][0]))
# 							# print('agent.belieftree[' + str(who) + '][len_PC + len_ML + ' + str(j) + '][2]: ' + str(agent.belieftree[who][len_PC + len_ML + j][2]))
# 							agent.instrument_preferences[who][i] = agent.instrument_preferences[who][i] + \
# 								(instruments[i][j] * (agent.belieftree[who][len_PC + len_ML + j][1] - agent.belieftree[who][len_PC + len_ML + j][0]) * \
# 								(agent.belieftree[who][len_PC + len_ML + j][2]))
# 							# print('agent.instrument_preferences[who][i]: ' + str(agent.instrument_preferences[who][i]))
# 					else:
# 						agent.instrument_preferences[who][i] = 0

# 	def one_minus_one_check(self, to_be_checked_parameter):

# 		"""
# 		One minus one check function
# 		===========================

# 		This function checks that a certain values does not got over one
# 		and does not go below one due to the randomisation.
		
# 		"""

# 		checked_parameter = 0
# 		if to_be_checked_parameter > 1:
# 			checked_parameter = 1
# 		elif to_be_checked_parameter < -1:
# 			checked_parameter = -1
# 		else:
# 			checked_parameter = to_be_checked_parameter
# 		return checked_parameter
