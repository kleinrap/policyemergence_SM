import random
import copy

from network_creation import PolicyNetworkLinks
from functions_actions import ActionFunctions

class Coalition():

	def __init__(self, unique_id, lead, members, members_id, issue, creation, resources):

		self.unique_id = unique_id
		self.lead = lead
		self.members = members
		self.members_id = members_id
		self.issue = issue
		self.creation = creation
		self.resources = resources


	def __str__(self):
		return 'Coalition - ' + str(self.unique_id) + ' created at tick: ' + str(self.creation) + ' and a total of: ' + str(len(self.members)) + ' members.'

	# def __str__(self):
	# 	return 'Coalition - ' + str(self.unique_id)

	def coalition_belief_actions_ACF_as(self, coalitions, causalrelation_number, deep_core, mid_level, secondary, agent_action_list, ACF_link_list_as, ACF_link_list_as_total, \
		ACF_link_id_as, link_list, affiliation_weights, conflict_level_coef, resources_weight_action, resources_potency):

		"""
		The coalition belief actions function (agenda setting)
		===========================

		This function is used to perform the actions of the coalitions
		in the agenda setting. The actions of the coalitions are the 
		same actions as the one of the individual agents. The main
		differences here are the amount of resources used and the fact
		that all actions are estimated and performed by the coalition
		leader based on the coalition leader's partial knowledge.

		"""

		len_PC = len(deep_core)
		len_ML = len(mid_level)
		len_S = len(secondary)

		# print(coalitions)

		# print('The belief actions now have to be performed for each team!')
		# Make sure that the coalition actually axists:
		if len(coalitions.members) > 0:

			# 0. Asssigning the resources
			coalitions.resources[1] = coalitions.resources[0]

			cw_of_interest = []
			# We only consider the causal relations related to the problem on the agenda
			for cw_choice in range(len(deep_core)):
					cw_of_interest.append(len_PC + len_ML + len_S + (coalitions.issue - len_PC) + cw_choice * len(mid_level))
			# print(' ')
			# print('cw_of_interest: ' + str(cw_of_interest))

			# 1. Intra-team actions (actions performed on agents inside the team)
			# This step is only performed if there is more than one team member in the coalition
			if len(coalitions.members) != 1 and len(cw_of_interest) > 0:

				# As long as there are enough resources (50% of the total)
				while True:
					# a. First exchange of information on all causal relations and the policy issue of the team
					#  Exchange of knowledge on the policy (state and aim)
					
					self.knowledge_exchange_coalition(coalitions, coalitions.issue, 0)
					self.knowledge_exchange_coalition(coalitions, coalitions.issue, 1)
					# Exchange of knowledge on the causal relations

					for cw in cw_of_interest:
						self.knowledge_exchange_coalition(coalitions, cw, 0)
					
					# b. Compiling all actions for each actor

					# This will need to be adjusted at a later point.
					actionWeight = 1

					#  We look at one causal relation at a time:
					# print(' ')
					# print(coalitions.lead)
					total_agent_grades = []
					for cw in cw_of_interest:
						cw_grade_list = []
						# We then go through all agents
						for agent_inspected in coalitions.members:
							# Take the list of links
							for links in link_list:
								# Check that only the link of interest is selected
								if (links.agent1 == coalitions.lead and links.agent2 == agent_inspected) or (links.agent2 == coalitions.lead and links.agent1 == agent_inspected) and links.aware > 0:

									cw_grade = ActionFunctions.action_grade_calculator(links, cw, 0, coalitions.lead, affiliation_weights)
									cw_grade_list.append(cw_grade)
							
						total_agent_grades.append(sum(cw_grade_list))

						# print('CR: ' + str(cw) + ' with grade: ' + str(sum(cw_grade_list)))

					# We look at the state for the policy
					state_grade_list = []
					# We then go through all agents
					for agent_inspected in coalitions.members:
						# Take the list of links
						for links in link_list:
							# Check that only the link of interest is selected
							if (links.agent1 == coalitions.lead and links.agent2 == agent_inspected) or (links.agent2 == coalitions.lead and links.agent1 == agent_inspected) and links.aware > 0:

								state_grade = ActionFunctions.action_grade_calculator(links, coalitions.issue, 0, coalitions.lead, affiliation_weights)
								state_grade_list.append(state_grade)

					total_agent_grades.append(sum(state_grade_list))
					# print('State: ' + str(sum(state_grade_list)))
					
					# We look at the aim for the policy
					aim_grade_list = []
					# We then go through all agents
					for agent_inspected in coalitions.members:
						# Take the list of links
						for links in link_list:
							# Check that only the link of interest is selected
							if (links.agent1 == coalitions.lead and links.agent2 == agent_inspected) or (links.agent2 == coalitions.lead and links.agent1 == agent_inspected) and links.aware > 0:

								aim_grade = ActionFunctions.action_grade_calculator(links, coalitions.issue, 0, coalitions.lead, affiliation_weights)
								aim_grade_list.append(aim_grade)

					total_agent_grades.append(sum(aim_grade_list))
					# print('Aim: ' + str(sum(aim_grade_list)))

					# c. Finding the best action
					best_action = total_agent_grades.index(max(total_agent_grades))

					# print(' ')
					# print('----- Considering new action grading -----')
					# print('Action to be performed: ' + str(best_action))


					# d. Implementation the best action

					# It is the agent that has the best action that performs the action
					for agent_impacted in coalitions.members:
						# Selecting the link:
						for links in link_list:
							# Check that only the link of interest is selected
							if (links.agent1 == coalitions.lead and links.agent2 == agent_inspected) or (links.agent2 == coalitions.lead and links.agent1 == agent_inspected) and links.aware > 0:

								# Update of the aware decay parameter
								links.aware_decay = 5

								# The causal relation action is performed
								if best_action <= len(cw_of_interest) - 1:
									# print(' ')
									# print('Performing a causal relation framing action')
									# print('best_action: ' + str(best_action))
									# print('cw_of_interest: ' + str(cw_of_interest))
									# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

									implemented_action = ActionFunctions.action_implementor(links, cw_of_interest[best_action], 0, coalitions.lead, coalitions, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(coalitions.members))

								# The state change is performed
								if best_action == len(cw_of_interest):
									# print(' ')
									# print('Performing a state change action')
									# print('best_action: ' + str(best_action))

									implemented_action = ActionFunctions.action_implementor(links, coalitions.issue, 0, coalitions.lead, coalitions, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(coalitions.members))

								# The aim change is performed
								if best_action == len(cw_of_interest) + 1:
									# print(' ')
									# print('Performing an aim change action')
									# print('best_action: ' + str(best_action))

									implemented_action = ActionFunctions.action_implementor(links, coalitions.issue, 1, coalitions.lead, coalitions, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(coalitions.members))
					
					# Updating the resources of the team
					coalitions.resources[1] -= coalitions.resources[0]*0.1

					# Resources check
					if coalitions.resources[1] <= 0.5 * coalitions.resources[0]:
						# print('RAN OUT OF RESOURCES!')
						break

			# 2. Inter-team actions (actions performed on agents outside the team)

			# Only perform this if not all agents are in the coalition
			if len(coalitions.members) < len(agent_action_list) and len(cw_of_interest) > 0:

				# Creation of the list of agents to be considered:
				inter_agent_list = []
				for potential_agent in agent_action_list:
					if potential_agent not in coalitions.members:
						inter_agent_list.append(potential_agent)
				# print(' ')
				# print('# of agents not in the team: ' + str(len(inter_agent_list)))

				# Creation of the shadow network for this coalition
				# print('We need to create a link network for this team!')
				for agent_network in inter_agent_list:
					# Do not take into account EP with no interest in that issue for the network
					if agent_network.belieftree[0][coalitions.issue][0] != 'No':
						# print(' ')
						# print('Added 1 - ' + str(agent_network))
						self.new_link_ACF_as(link_list, agent_network, coalitions, ACF_link_list_as, ACF_link_list_as_total, ACF_link_id_as, len_PC, len_ML, len_S, conflict_level_coef)

				# Performing the actions using the shadow network and the individual agents within the team

				# As long as there are enough resources (50% of the total)
				while True:

					# print('Performing inter-team actions')

					total_agent_grades = []
					# for agents_in_team in teams.members:
					# Going through all agents that are not part of the team
					link_count = 0
					for links in ACF_link_list_as:
						# Make sure to select an existing link
						if links.aware != -1:
							# Make sure to only select the links related to this team
							if coalitions == links.agent1:
								# print(links)
								link_count += 1
								# Setting the action weight
								# Removed for now for technical issues
								# if type(links.agent2) == Policymakers:
								# 		actionWeight = 1
								# else:
								# 	actionWeight = 0.95
								actionWeight = 1
								# Framing actions:
								for cw in range(len(cw_of_interest)):

									# Grade calculation using the likelihood method
									# Same affiliation
									if coalitions.lead.affiliation == links.agent2.affiliation:
										cw_grade = links.conflict_level[2 + cw_of_interest[cw] - (len_PC + len_ML + len_S)] * links.aware * actionWeight
										total_agent_grades.append(cw_grade)

									# Affiliation 1-2
									if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 1) or \
										(coalitions.lead.affiliation == 1 and links.agent2.affiliation == 0):
										cw_grade = links.conflict_level[2 + cw_of_interest[cw] - (len_PC + len_ML + len_S)] * links.aware * actionWeight * affiliation_weights[0]
										total_agent_grades.append(cw_grade)

									# Affiliation 1-3
									if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 2) or \
										(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 0):
										cw_grade = links.conflict_level[2 + cw_of_interest[cw] - (len_PC + len_ML + len_S)] * links.aware * actionWeight * affiliation_weights[1]
										total_agent_grades.append(cw_grade)

									# Affiliation 2-3
									if (coalitions.lead.affiliation == 1 and links.agent2.affiliation == 2) or \
										(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 1):
										cw_grade = links.conflict_level[2 + cw_of_interest[cw] - (len_PC + len_ML + len_S)] * links.aware * actionWeight * affiliation_weights[2]
										total_agent_grades.append(cw_grade)
									
								# State influence actions
								# Grade calculation using the likelihood method
								# Same affiliation
								if coalitions.lead.affiliation == links.agent2.affiliation:
									state_grade = links.conflict_level[0] * links.aware * actionWeight
									total_agent_grades.append(state_grade)

								# Affiliation 1-2
								if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 1) or \
									(coalitions.lead.affiliation == 1 and links.agent2.affiliation == 0):
									state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[0]
									total_agent_grades.append(state_grade)

								# Affiliation 1-3
								if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 2) or \
									(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 0):
									state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[1]
									total_agent_grades.append(state_grade)

								# Affiliation 2-3
								if (coalitions.lead.affiliation == 1 and links.agent2.affiliation == 2) or \
									(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 1):
									state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[2]
									total_agent_grades.append(state_grade)

								# Aim influence actions
								# Grade calculation using the likelihood method
								# Same affiliation
								if coalitions.lead.affiliation == links.agent2.affiliation:
									aim_grade = links.conflict_level[1] * links.aware * actionWeight
									total_agent_grades.append(aim_grade)

								# Affiliation 1-2
								if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 1) or \
									(coalitions.lead.affiliation == 1 and links.agent2.affiliation == 0):
									aim_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[0]
									total_agent_grades.append(aim_grade)

								# Affiliation 1-3
								if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 2) or \
									(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 0):
									aim_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[1]
									total_agent_grades.append(aim_grade)

								# Affiliation 2-3
								if (coalitions.lead.affiliation == 1 and links.agent2.affiliation == 2) or \
									(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 1):
									aim_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[2]
									total_agent_grades.append(aim_grade)

					# Choosing the best action
					best_action_index = total_agent_grades.index(max(total_agent_grades))
					best_action = best_action_index - int(best_action_index/(len(cw_of_interest) + 1 + 1))*(len(cw_of_interest) + 1 + 1)
					acted_upon_agent = int(best_action_index/(len(cw_of_interest) + 1 + 1))

					# print(' ')
					# print('----- Considering new action grading -----')
					# print('Original index: ' + str(best_action_index))
					# print('Number of actions that can be performed: ' + str(len(cw_of_interest) + 1 + 1))
					# print('Action to be performed: ' + str(best_action))
					# print('This is the agent on which the action is performed: ' + str(acted_upon_agent))

					# Actually performing the action:
					# Getting a list of the links related to this team
					list_links_coalitions = []
					for links in ACF_link_list_as:
							# Make sure to only select the links related to this team
							if coalitions == links.agent1:
								# Make sure to select an existing link
								if links.aware != -1:
									list_links_coalitions.append(links)

					# Implement framing action
					if best_action <= len(cw_of_interest) - 1:
						# print(' ')
						# print('Performing a causal relation framing action')
						# print('best_action: ' + str(best_action))
						# print('cw_of_interest: ' + str(cw_of_interest))
						# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

						# print('Before: ', list_links_coalitions[acted_upon_agent].agent2.belieftree[0][len(deep_core) + len(mid_level) + len(secondary) + best_action - 1][0])

						if coalitions.lead.affiliation == list_links_coalitions[acted_upon_agent].agent2.affiliation:
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] += \
								(coalitions.lead.belieftree[0][cw_of_interest[best_action]][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0]) * \
								coalitions.resources[0] * 0.1

						# Affiliation 1-2
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1) or \
							(coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] += \
								(coalitions.lead.belieftree[0][cw_of_interest[best_action]][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] += \
								(coalitions.lead.belieftree[0][cw_of_interest[best_action]][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] += \
								(coalitions.lead.belieftree[0][cw_of_interest[best_action]][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[2]

						# print('After: ', list_links_coalitions[acted_upon_agent].agent2.belieftree[0][len(deep_core) + len(mid_level) + len(secondary) + best_action - 1][0])
						
						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] = \
							ActionFunctions.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer(coalitions.lead, list_links_coalitions[acted_upon_agent].agent2, cw_of_interest[best_action], 0)

					# Implement state influence action
					if best_action == len(cw_of_interest):
						# print(' ')
						# print('Performing a state change action')
						# print('best_action: ' + str(best_action))

						if coalitions.lead.affiliation == list_links_coalitions[acted_upon_agent].agent2.affiliation:
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0] += \
								(coalitions.lead.belieftree[0][coalitions.issue][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0]) * \
								coalitions.resources[0] * 0.1

						# Affiliation 1-2
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1) or \
							(coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0] += \
								(coalitions.lead.belieftree[0][coalitions.issue][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0] += \
								(coalitions.lead.belieftree[0][coalitions.issue][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0] += \
								(coalitions.lead.belieftree[0][coalitions.issue][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[2]
						
						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0] = \
							ActionFunctions.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][0])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer(coalitions.lead, list_links_coalitions[acted_upon_agent].agent2, coalitions.issue, 0)

					# Implement aim influence action
					if best_action == len(cw_of_interest) + 1:
						# print(' ')
						# print('Performing an aim change action')
						# print('best_action: ' + str(best_action))


						if coalitions.lead.affiliation == list_links_coalitions[acted_upon_agent].agent2.affiliation:
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1] += \
								(coalitions.lead.belieftree[0][coalitions.issue][1] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1]) * \
								coalitions.resources[0] * 0.1

						# Affiliation 1-2
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1) or \
							(coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1] += \
								(coalitions.lead.belieftree[0][coalitions.issue][1] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1] += \
								(coalitions.lead.belieftree[0][coalitions.issue][1] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1] += \
								(coalitions.lead.belieftree[0][coalitions.issue][1] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[2]
						
						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1] = \
							ActionFunctions.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[0][coalitions.issue][1])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer(coalitions.lead, list_links_coalitions[acted_upon_agent].agent2, coalitions.issue, 1)

					# Adjusting the awareness decay of the coalition members
					for links_to_change in link_list:
						for agents_in_coalition in coalitions.members:
							if links_to_change.agent1 == agents_in_coalition and links_to_change.agent2.unique_id == acted_upon_agent:
								links_to_change.aware_decay = 5
							if links_to_change.agent2 == agents_in_coalition and links_to_change.agent1.unique_id == acted_upon_agent:
								links_to_change.aware_decay = 5

					# Updating the resources of the team
					coalitions.resources[1] -= coalitions.resources[0]*0.1

					# Resources check
					if coalitions.resources[1] <= 0 * coalitions.resources[0]:
						break
			
	def coalition_belief_actions_ACF_pf(self, coalitions, causalrelation_number, deep_core, mid_level, secondary, agent_action_list, ACF_link_list_pf, ACF_link_list_pf_total, \
		ACF_link_id_pf, link_list, affiliation_weights, agenda_as_issue, instruments, conflict_level_coef, resources_weight_action, resources_potency):

		"""
		The coalition belief actions function (policy formulation)
		===========================

		This function is used to perform the actions of the coalitions
		in the policy formulation. The actions of the coalitions are the 
		same actions as the one of the individual agents. The main
		differences here are the amount of resources used and the fact
		that all actions are estimated and performed by the coalition
		leader based on the coalition leader's partial knowledge.

		Note: This function is the same as the previous one but with 
		changes associated with the already selected agenda.

		"""

		len_PC = len(deep_core)
		len_ML = len(mid_level)
		len_S = len(secondary)

		# print(coalitions)

		# print('The belief actions now have to be performed for each team!')
		# Make sure that the coalition actually axists:
		if len(coalitions.members) > 0:

			# 0. Asssigning the resources
			coalitions.resources[1] = coalitions.resources[0]

			# Looking for the relevant causal relations for the policy formulation
			of_interest = []
			cw_of_interest = []
			# We only consider the causal relations related to the problem on the agenda
			for cw_choice in range(len(secondary)):
				if coalitions.lead.belieftree[0][len_PC + len_ML + len_S + (len_PC * len_ML) + (agenda_as_issue - len_PC)*len_S + cw_choice][0] \
					* instruments[coalitions.issue][cw_choice] != 0:
					cw_of_interest.append(len_PC + len_ML + len_S + (len_PC * len_ML) + (agenda_as_issue - len_PC)*len_S + cw_choice)
			of_interest.append(cw_of_interest)
			# Looking for the relevant issues for the policy formulation
			# That is we choose the secondary issues that are impacted by the policy instrument
			# that the agent has selected.
			issue_of_interest = []
			for issue_choice in range(len(secondary)):
				if instruments[coalitions.issue][issue_choice] != 0:
					issue_of_interest.append(len_PC + len_ML + issue_choice)
			of_interest.append(issue_of_interest)
			# print(' ')
			# print('of_interest: ' + str(of_interest))

			# 1. Intra-team actions (actions performed on agents inside the team)
			# This step is only performed if there is more than one team member in the coalition
			if len(coalitions.members) != 1 and len(cw_of_interest) > 0:

				# As long as there are enough resources (50% of the total)
				while True:
					# a. First exchange of information on all causal relations and the policy issue of the team
					#  Exchange of knowledge on the policy (state and aim)
					
					for issues in issue_of_interest:
						self.knowledge_exchange_coalition(coalitions, issues, 0)
						self.knowledge_exchange_coalition(coalitions, issues, 1)
					# Exchange of knowledge on the causal relations

					for cw in range(causalrelation_number):
						self.knowledge_exchange_coalition(coalitions, len_PC + len_ML + len_S + cw, 0)
					
					# b. Compiling all actions for each actor

					#  We look at one causal relation at a time:
					# print(' ')
					# print(coalitions.lead)
					total_agent_grades = []
					for cw in cw_of_interest:
						cw_grade_list = []
						# We then go through all agents
						for agent_inspected in coalitions.members:
							# Take the list of links
							for links in link_list:
								# Check that only the link of interest is selected
								if (links.agent1 == coalitions.lead and links.agent2 == agent_inspected) or (links.agent2 == coalitions.lead and links.agent1 == agent_inspected) and links.aware > 0:

									cw_grade = ActionFunctions.action_grade_calculator(links, cw, 0, coalitions.lead, affiliation_weights)
									cw_grade_list.append(cw_grade)
							
						total_agent_grades.append(sum(cw_grade_list))

						# print('CR: ' + str(cw) + ' with grade: ' + str(sum(cw_grade_list)))

					# We look at the state for the policy
					for issue_num in issue_of_interest:
						state_grade_list = []
						# We then go through all agents
						for agent_inspected in coalitions.members:
							# Take the list of links
							for links in link_list:
								# Check that only the link of interest is selected
								if (links.agent1 == coalitions.lead and links.agent2 == agent_inspected) or (links.agent2 == coalitions.lead and links.agent1 == agent_inspected) and links.aware > 0:

									state_grade = ActionFunctions.action_grade_calculator(links, issue_num, 0, coalitions.lead, affiliation_weights)
									state_grade_list.append(state_grade)

						total_agent_grades.append(sum(state_grade_list))

					# print('State: ' + str(sum(state_grade_list)))
					
					# We look at the aim for the policy
					aim_grade_list = []
					for issue_num in issue_of_interest:
						# We then go through all agents
						for agent_inspected in coalitions.members:
							# Take the list of links
							for links in link_list:
								# Check that only the link of interest is selected
								if (links.agent1 == coalitions.lead and links.agent2 == agent_inspected) or (links.agent2 == coalitions.lead and links.agent1 == agent_inspected) and links.aware > 0:

									aim_grade = ActionFunctions.action_grade_calculator(links, issue_num, 1, coalitions.lead, affiliation_weights)
									aim_grade_list.append(aim_grade)

						total_agent_grades.append(sum(aim_grade_list))

					# c. Finding the best action
					best_action_index = total_agent_grades.index(min(total_agent_grades))

					# print(' ')
					# print('----- Considering new action grading -----')
					# print('Action to be performed: ' + str(best_action_index))

					# d. Implementation the best action
					# It is the agent that has the best action that performs the action
					for agent_impacted in coalitions.members:

						# Selecting the link:
						for links in link_list:

							# Check that only the link of interest is selected
							if (links.agent1 == coalitions.lead and links.agent2 == agent_inspected) or (links.agent2 == coalitions.lead and links.agent1 == agent_inspected) and links.aware > 0:

								# Update of the aware decay parameter
								links.aware_decay = 5

								# The causal relation action is performed
								if best_action_index <= len(cw_of_interest) - 1:
									# print(' ')
									# print('Performing a causal relation framing action')
									# print('best_action: ' + str(best_action))
									# print('cw_of_interest: ' + str(cw_of_interest))
									# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

									implemented_action = ActionFunctions.action_implementor(links, of_interest[0][best_action_index], 0, coalitions.lead, coalitions, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(coalitions.members))

								# The state change is performed
								if best_action_index > len(cw_of_interest) - 1 and best_action_index < len(cw_of_interest) + len(issue_of_interest) - 1:
									# print(' ')
									# print('Performing a state change action')
									# print('best_action: ' + str(best_action))

									implemented_action = ActionFunctions.action_implementor(links, of_interest[1][best_action_index - len(cw_of_interest)], 0, coalitions.lead, coalitions, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(coalitions.members))

								# The aim change is performed
								if best_action_index >= len(cw_of_interest) + len(issue_of_interest) - 1:
									# print(' ')
									# print('Performing an aim change action')
									# print('best_action: ' + str(best_action))

									implemented_action = ActionFunctions.action_implementor(links, of_interest[1][best_action_index - len(cw_of_interest) - len(cw_of_interest)], 1, coalitions.lead, coalitions, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(coalitions.members))

					# Updating the resources of the team
					coalitions.resources[1] -= coalitions.resources[0]*0.1

					# Resources check
					if coalitions.resources[1] <= 0.5 * coalitions.resources[0]:
						# print('RAN OUT OF RESOURCES!')
						break

			# 2. Inter-team actions (actions performed on agents outside the team)

			# Only perform this if not all agents are in the coalition
			if len(coalitions.members) < len(agent_action_list) and len(cw_of_interest) > 0:

				# Creation of the list of agents to be considered:
				inter_agent_list = []
				for potential_agent in agent_action_list:
					if potential_agent not in coalitions.members:
						inter_agent_list.append(potential_agent)
				# print(' ')
				# print('# of agents not in the team: ' + str(len(inter_agent_list)))

				# Creation of the shadow network for this coalition
				# print('We need to create a link network for this team!')
				for agent_network in inter_agent_list:
					# Do not take into account EP with no interest in that issue for the network
					if agent_network.belieftree[0][coalitions.issue][0] != 'No':
						# print(' ')
						# print('Added 1 - ' + str(agent_network))
						self.new_link_ACF_pf(link_list, agent_network, coalitions, ACF_link_list_pf, ACF_link_list_pf_total, ACF_link_id_pf, len_PC, len_ML, len_S, conflict_level_coef)

				# Performing the actions using the shadow network and the individual agents within the team

				# As long as there are enough resources (50% of the total)
				while True:

					# print('Performing inter-team actions')

					total_agent_grades = []
					# for agents_in_team in teams.members:
					# Going through all agents that are not part of the team
					link_count = 0
					for links in ACF_link_list_pf:
						# Make sure to select an existing link
						if links.aware != -1:
							# Make sure to only select the links related to this team
							if coalitions == links.agent1:
								link_count += 1
								# Setting the action weight
								# Removed for now for technical issues
								# if type(links.agent2) == Policymakers:
								# 		actionWeight = 1
								# else:
								# 	actionWeight = 0.95
								actionWeight = 1
								# Framing actions:
								for cw in range(len(cw_of_interest)):

									# Grade calculation using the likelihood method
									# Same affiliation
									if coalitions.lead.affiliation == links.agent2.affiliation:
										cw_grade = links.conflict_level[len_S + cw_of_interest[cw] - (len_PC + len_ML + len_S)] * links.aware * actionWeight
										total_agent_grades.append(cw_grade)

									# Affiliation 1-2
									if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 1) or \
										(coalitions.lead.affiliation == 1 and links.agent2.affiliation == 0):
										cw_grade = links.conflict_level[len_S + cw_of_interest[cw] - (len_PC + len_ML + len_S)] * links.aware * actionWeight * affiliation_weights[0]
										total_agent_grades.append(cw_grade)

									# Affiliation 1-3
									if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 2) or \
										(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 0):
										cw_grade = links.conflict_level[len_S + cw_of_interest[cw] - (len_PC + len_ML + len_S)] * links.aware * actionWeight * affiliation_weights[1]
										total_agent_grades.append(cw_grade)

									# Affiliation 2-3
									if (coalitions.lead.affiliation == 1 and links.agent2.affiliation == 2) or \
										(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 1):
										cw_grade = links.conflict_level[len_S + cw_of_interest[cw] - (len_PC + len_ML + len_S)] * links.aware * actionWeight * affiliation_weights[2]
										total_agent_grades.append(cw_grade)
								
								# State influence actions
								for issue_num in range(len(issue_of_interest)):

									# Grade calculation using the likelihood method
									# Same affiliation
									if coalitions.lead.affiliation == links.agent2.affiliation:
										state_grade = links.conflict_level[issue_of_interest[issue_num] - (len_PC + len_ML)][0] * links.aware * actionWeight
										total_agent_grades.append(state_grade)

									# Affiliation 1-2
									if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 1) or \
										(coalitions.lead.affiliation == 1 and links.agent2.affiliation == 0):
										state_grade = links.conflict_level[issue_of_interest[issue_num] - (len_PC + len_ML)][0] * links.aware * actionWeight * affiliation_weights[0]
										total_agent_grades.append(state_grade)

									# Affiliation 1-3
									if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 2) or \
										(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 0):
										state_grade = links.conflict_level[issue_of_interest[issue_num] - (len_PC + len_ML)][0] * links.aware * actionWeight * affiliation_weights[1]
										total_agent_grades.append(state_grade)

									# Affiliation 2-3
									if (coalitions.lead.affiliation == 1 and links.agent2.affiliation == 2) or \
										(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 1):
										state_grade = links.conflict_level[issue_of_interest[issue_num] - (len_PC + len_ML)][0] * links.aware * actionWeight * affiliation_weights[2]
										total_agent_grades.append(state_grade)

								# Aim influence actions
								for issue_num in range(len(issue_of_interest)):

									# Grade calculation using the likelihood method
									# Same affiliation
									if coalitions.lead.affiliation == links.agent2.affiliation:
										aim_grade = links.conflict_level[issue_of_interest[issue_num] - (len_PC + len_ML)][1] * links.aware * actionWeight
										total_agent_grades.append(aim_grade)

									# Affiliation 1-2
									if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 1) or \
										(coalitions.lead.affiliation == 1 and links.agent2.affiliation == 0):
										aim_grade = links.conflict_level[issue_of_interest[issue_num] - (len_PC + len_ML)][1] * links.aware * actionWeight * affiliation_weights[0]
										total_agent_grades.append(aim_grade)

									# Affiliation 1-3
									if (coalitions.lead.affiliation == 0 and links.agent2.affiliation == 2) or \
										(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 0):
										aim_grade = links.conflict_level[issue_of_interest[issue_num] - (len_PC + len_ML)][1] * links.aware * actionWeight * affiliation_weights[1]
										total_agent_grades.append(aim_grade)

									# Affiliation 2-3
									if (coalitions.lead.affiliation == 1 and links.agent2.affiliation == 2) or \
										(coalitions.lead.affiliation == 2 and links.agent2.affiliation == 1):
										aim_grade = links.conflict_level[issue_of_interest[issue_num] - (len_PC + len_ML)][1] * links.aware * actionWeight * affiliation_weights[2]
										total_agent_grades.append(aim_grade)								

					# Choosing the best action
					best_action_index = total_agent_grades.index(max(total_agent_grades))
					best_action = best_action_index - int(best_action_index/(len(cw_of_interest) + 2*len(issue_of_interest)))*(len(cw_of_interest) + 2*len(issue_of_interest))
					acted_upon_agent = int(best_action_index/(len(cw_of_interest) + 2*len(issue_of_interest)))

					# print(' ')
					# print('----- Considering new action grading -----')
					# print('Original index: ' + str(best_action_index))
					# print('Number of actions that can be performed: ' + str(len(cw_of_interest) + + 2*len(issue_of_interest)))
					# print('Action to be performed: ' + str(best_action))
					# print('This is the agent on which the action is performed: ' + str(acted_upon_agent))

					# Actually performing the action:
					# Getting a list of the links related to this team
					list_links_coalitions = []
					for links in ACF_link_list_pf:
							# Make sure to only select the links related to this team
							if coalitions == links.agent1:
								# Make sure to select an existing link
								if links.aware != -1:
									list_links_coalitions.append(links)

					# Implement framing action
					if best_action <= len(cw_of_interest) - 1:
						# print(' ')
						# print('Performing a CR action')
						# print(of_interest[0])
						# print('best_action: ' + str(best_action))
						# print(of_interest[0][best_action])

						# print('Before: ' + str(list_links_coalitions[acted_upon_agent].agent2.belieftree[0][len(deep_core) + len(mid_level) + len(secondary) + best_action - 1][0]))

						# Same affiliation
						if coalitions.lead.affiliation == list_links_coalitions[acted_upon_agent].agent2.affiliation:
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0] += \
								(coalitions.lead.belieftree[0][of_interest[0][best_action]][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0]) * \
								coalitions.resources[0] * 0.1

						# Affiliation 1-2
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1) or \
							(coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0] += \
								(coalitions.lead.belieftree[0][of_interest[0][best_action]][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0] += \
								(coalitions.lead.belieftree[0][of_interest[0][best_action]][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0] += \
								(coalitions.lead.belieftree[0][of_interest[0][best_action]][0] - list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[2]

						# print('After: ' + str(list_links_coalitions[acted_upon_agent].agent2.belieftree[0][len(deep_core) + len(mid_level) + len(secondary) + best_action - 1][0]))
						
						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0] = \
							ActionFunctions.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[0][best_action]][0])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer(coalitions.lead, list_links_coalitions[acted_upon_agent].agent2, of_interest[0][best_action], 0)

					# Implement state influence action
					elif best_action > len(cw_of_interest) - 1 and best_action < len(cw_of_interest) + len(issue_of_interest) - 1:
						# print(' ')
						# print('Performing a state action')
						# print(of_interest[1])
						# print('best_action - len(cw_of_interest): ' + str(best_action - len(cw_of_interest)))
						# print(of_interest[1][best_action - len(cw_of_interest)])

						# Same affiliation
						if coalitions.lead.affiliation == list_links_coalitions[acted_upon_agent].agent2.affiliation:
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] += \
								(coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] - \
								list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0]) * \
								coalitions.resources[0] * 0.1

						# Affiliation 1-2
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1) or \
							(coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] += \
								(coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] - \
								list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] += \
								(coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] - \
								list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] += \
								(coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] - \
								list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[2]

						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0] = \
							ActionFunctions.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest)]][0])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer(coalitions.lead, list_links_coalitions[acted_upon_agent].agent2, of_interest[1][best_action - len(cw_of_interest)], 0)

					# Implement aim influence action
					elif best_action >= len(cw_of_interest) + len(issue_of_interest) - 1:
						# print(' ')
						# print('Performing an aim action')
						# print(of_interest[1])
						# print('best_action - len(cw_of_interest) - len(cw_of_interest): ' + str(best_action - len(cw_of_interest) - len(cw_of_interest)))
						# print(of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)])

						if coalitions.lead.affiliation == list_links_coalitions[acted_upon_agent].agent2.affiliation:
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] += \
								(coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] - \
								list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1]) * \
								coalitions.resources[0] * 0.1

						# Affiliation 1-2
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1) or \
							(coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] += \
								(coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] - \
								list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (coalitions.lead.affiliation == 0 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 0):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] += \
								(coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] - \
								list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (coalitions.lead.affiliation == 1 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 2) or \
							(coalitions.lead.affiliation == 2 and list_links_coalitions[acted_upon_agent].agent2.affiliation == 1):
							list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] += \
								(coalitions.lead.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] - \
								list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1]) * \
								coalitions.resources[0] * 0.1 * affiliation_weights[2]
						
						# 1-1 check
						list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1] = \
							ActionFunctions.one_minus_one_check(list_links_coalitions[acted_upon_agent].agent2.belieftree[0][of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)]][1])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer(coalitions.lead, list_links_coalitions[acted_upon_agent].agent2, of_interest[1][best_action - len(cw_of_interest) - len(cw_of_interest)], 2)

					# Adjusting the awareness decay of the coalition members
					for links_to_change in link_list:
						for agents_in_coalition in coalitions.members:
							if links_to_change.agent1 == agents_in_coalition and links_to_change.agent2.unique_id == acted_upon_agent:
								links_to_change.aware_decay = 5
							if links_to_change.agent2 == agents_in_coalition and links_to_change.agent1.unique_id == acted_upon_agent:
								links_to_change.aware_decay = 5

					# Updating the resources of the team
					coalitions.resources[1] -= coalitions.resources[0]*0.1

					# Resources check
					if coalitions.resources[1] <= 0 * coalitions.resources[0]:
						break
	
	def new_link_ACF_as(self, link_list, outsider_agent, coalitions, ACF_link_list_as, ACF_link_list_as_total, ACF_link_id_as, len_PC, len_ML, len_S, conflict_level_coef):

		"""
		The new link function - ACF shadow network (agenda setting)
		===========================

		This function is used to create new links for the coalitions shadow
		networks. These links are obtained through looking at whichever
		member in the coalition has the highest awareness level for that agent.

		When creating a new link, the conflict level is also set along with the
		awareness decay. This is the agenda setting version of the function. 

		"""

		# 1. We look for the highest awareness level
		coalition_aware, agent_with_highest_awareness = PolicyNetworkLinks.awareness_level_selection(link_list, coalitions, outsider_agent)

		# 2. We calculate the conflict level (options 2 is for coalitions)
		# Note that the conflict level is only of interest for the issue advocated by the team (simplifying things)
		# All causal relations are considered as any might be called up during the belief influence actions
		conflict_level_option = 2
		agent_with_highest_awareness = coalitions.lead

		conflict_level = PolicyNetworkLinks.conflict_level_calculation(coalitions, outsider_agent, conflict_level_coef, conflict_level_option, agent_with_highest_awareness, len_PC, len_ML, len_S)

		# 3. We set the aware decay
		aware_decay = 0

		# 4. We create the link
		coalition_link = PolicyNetworkLinks(ACF_link_id_as[0], coalitions, outsider_agent, coalition_aware, aware_decay, conflict_level)
		ACF_link_list_as.append(coalition_link)
		ACF_link_list_as_total.append(coalition_link)
		ACF_link_id_as[0] += 1

	def new_link_ACF_pf(self, link_list, outsider_agent, coalitions, ACF_link_list_pf, ACF_link_list_pf_total, ACF_link_id_pf, len_PC, len_ML, len_S, conflict_level_coef):

		"""
		The new link function - ACF shadow network (policy formulation)
		===========================

		This function is used to create new links for the coalitions shadow
		networks. These links are obtained through looking at whichever
		member in the coalition has the highest awareness level for that agent.

		When creating a new link, the conflict level is also set along with the
		awareness decay. This is the policy formulation version of the function. 

		"""

		# 1. We look for the highest awareness level
		coalition_aware, agent_with_highest_awareness = PolicyNetworkLinks.awareness_level_selection(link_list, coalitions, outsider_agent)

		# 2. We calculate the conflict level
		# Note that the conflict level is only of interest for the issue advocated by the coalition leader (simplifying things)
		# The conflict level is calculated based on the beliefs of the whole coalition leader on the issue for state and aim
		conflict_level = []
		conflict_level_init = [conflict_level_coef[1], conflict_level_coef[1]]
		for p in range(len_S):
			conflict_level.append(copy.copy(conflict_level_init))

		for p in range(len_PC*len_ML + len_ML*len_S):
			conflict_level.append(conflict_level_coef[1])

		# Looking at the state and aim to calculate the conflict level
		for p in range(len_S):
			check_none0 = 0
			if coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_PC + len_ML + p][0] == None:
				coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_PC + len_ML + p][0] = 0
				check_none0 = 1
			check_none1 = 0
			if coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_PC + len_ML + p][1] == None:
				coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_PC + len_ML + p][1] = 0
				check_none1 = 1
			state_cf_difference = abs(coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_PC + len_ML + p][0] - coalitions.lead.belieftree[0][len_PC + len_ML + p][0])
			aim_cf_difference = abs(coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_PC + len_ML + p][1] - coalitions.lead.belieftree[0][len_PC + len_ML + p][1])
			if check_none0 == 1:
				coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_PC + len_ML + p][0] = None
			if check_none1 == 1:
				coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_PC + len_ML + p][1] = None

			# State conflict level
			if state_cf_difference <= 0.25:
				conflict_level[p][0] = conflict_level_coef[0]
			if state_cf_difference > 0.25 and state_cf_difference <=1.75:
				conflict_level[p][0] = conflict_level_coef[2]
			if state_cf_difference > 1.75:
				conflict_level[p][0] = conflict_level_coef[1]
			
			# Aim conflict level
			if aim_cf_difference <= 0.25:
				conflict_level[p][1] = conflict_level_coef[0]
			if aim_cf_difference > 0.25 and aim_cf_difference <=1.75:
				conflict_level[p][1] = conflict_level_coef[2]
			if aim_cf_difference > 1.75:
				conflict_level[p][1] = conflict_level_coef[1]

		# Conflict level for the causal relations
		for p in range(len_PC*len_ML + len_ML*len_S):
			cw_difference = abs(coalitions.lead.belieftree[1 + outsider_agent.unique_id][len_PC + len_ML + len_S + p][0] - coalitions.lead.belieftree[0][len_PC + len_ML + len_S + p][0])
			if cw_difference <= 0.25:
				conflict_level[len_S + p] = conflict_level_coef[0]
			if cw_difference > 0.25 and cw_difference <=1.75:
				conflict_level[len_S + p] = conflict_level_coef[2]
			if cw_difference > 1.75:
				conflict_level[len_S + p] = conflict_level_coef[1]

		# 3. We set the aware decay
		aware_decay = 0

		# 4. We create the link
		coalition_link = PolicyNetworkLinks(ACF_link_id_pf[0], coalitions, outsider_agent, coalition_aware, aware_decay, conflict_level)
		ACF_link_list_pf.append(coalition_link)
		ACF_link_list_pf_total.append(coalition_link)
		ACF_link_id_pf[0] += 1

	def knowledge_exchange_coalition(self, team, cw_knowledge, parameter):

		"""
		Knowledge exchange function - coalitions
		===========================

		This function is used for the exchange of partial knowledge between agents
		within the same coalition. This only regards the issue that is selected by the
		coalition and is kept with a certain amount of randomness.
		
		"""

		# Exchange of partial knowledge between the agents in the team
		for agent_exchange1 in team.members:
			for agent_exchange2 in team.members:
				# Actual knowledge exchange with a randomness of 0.2
				# print('Before: ' + str(agent_exchange1.belieftree[1 + agent_exchange2.unique_id][team.issue][0]))
				agent_exchange1.belieftree[1 + agent_exchange2.unique_id][cw_knowledge][parameter] = \
				  agent_exchange2.belieftree[0][cw_knowledge][0] + (random.random()/5) - 0.1
				# print('After: ' + str(agent_exchange1.belieftree[1 + agent_exchange2.unique_id][team.issue][0]))
				# 1-1 check
				if agent_exchange1.belieftree[1 + agent_exchange2.unique_id][cw_knowledge][parameter] > 1:
					agent_exchange1.belieftree[1 + agent_exchange2.unique_id][cw_knowledge][parameter] = 1
				if agent_exchange1.belieftree[1 + agent_exchange2.unique_id][cw_knowledge][parameter] < -1:
					agent_exchange1.belieftree[1 + agent_exchange2.unique_id][cw_knowledge][parameter]  = -1
