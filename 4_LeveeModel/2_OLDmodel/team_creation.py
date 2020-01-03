import random
from network_creation import PolicyNetworkLinks
from functions_actions import ActionFunctions

class Team():

	def __init__(self, unique_id, lead, members, members_id, issue_type, issue, creation, resources):

		self.unique_id = unique_id
		self.lead = lead
		self.members = members
		self.members_id = members_id
		self.issue_type = issue_type
		self.issue = issue
		self.creation = creation
		self.resources = resources


	def __str__(self):
		return 'Team - ' + str(self.unique_id) + ' created at tick: ' + str(self.creation) + ' with issue: ' + str(self.issue)

	# def __str__(self):
	# 	return 'Team - ' + str(self.unique_id)

	def team_belief_actions_threeS_as(self, teams, causalrelation_number, deep_core, mid_level, secondary, agent_action_list, threeS_link_list_as, \
		threeS_link_list_as_total, threeS_link_id_as, link_list, affiliation_weights, conflict_level_coef, resources_weight_action, resources_potency, conflict_level_option):

		"""
		Team actions - three streams(agenda setting)
		===========================

		This function is used to perform the team actions. The team actions
		are the same as the individual agent actions as shown in the formalisation.
		For each team, inter- and intra- actions are graded by all possible agents.
		The action that has the highest grade is then selected for
		implementation.

		Depending on whether the team is focused on a policy or a problem, the
		actions will be slightly different.

		"""

		len_PC = len(deep_core)
		len_ML = len(mid_level)
		len_S = len(secondary)

		# print('The belief actions now have to be performed for each team!')
		# Make sure that the team actually axists:
		if len(teams.members) > 0:

			# 0. Asssigning the resources
			teams.resources[1] = teams.resources[0]

			# 1. Intra-team actions (actions performed on agents inside the team)

			# If the team is advocating for a problem, the following tasks are completed
			if teams.issue_type == 'problem':

				# As long as there are enough resources (50% of the total)
				while True:
					# a. First exchange of information on all causal relations and the policy issue of the team
					#  Exchange of knowledge on the policy (state and aim)
					
					self.knowledge_exchange_team(teams, teams.issue, 0)
					self.knowledge_exchange_team(teams, teams.issue, 1)
					# Exchange of knowledge on the causal relations

					cw_of_interest = []
					# We only consider the causal relations related to the problem on the agenda
					for cw_choice in range(len(deep_core)):
							cw_of_interest.append(len_PC + len_ML + len_S + len_PC + (teams.issue - len_PC) + cw_choice * len(mid_level))
					# print(' ')
					# print('cw_of_interest: ' + str(cw_of_interest))

					for cw in cw_of_interest:
						self.knowledge_exchange_team(teams, cw, 0)
					
					# b. Compiling all actions for each actor

					# We select one agent at a time
					total_agent_grades = []
					for agents_in_team in teams.members:
						#  We look at one causal relation at a time:
						# print(' ')
						# print(agents_in_team)	

						# CAUSAL RELATIONS GRADING
						for cw in cw_of_interest:
							cw_grade_list = []
							# We then go through all agents
							for agent_inspected in teams.members:
								# Take the list of links
								for links in link_list:
									# Check that only the link of interest is selected
									if (links.agent1 == agents_in_team and links.agent2 == agent_inspected) or (links.agent2 == agents_in_team and links.agent1 == agent_inspected) and links.aware > 0:

										cw_grade = ActionFunctions.action_grade_calculator(links, cw, 0, agents_in_team, affiliation_weights)
										cw_grade_list.append(cw_grade)

							total_agent_grades.append(sum(cw_grade_list))

						# STATES GRADING
						state_grade_list = []
						# We then go through all agents
						for agent_inspected in teams.members:
							# Take the list of links
							for links in link_list:
								# Check that only the link of interest is selected
								if (links.agent1 == agents_in_team and links.agent2 == agent_inspected) or (links.agent2 == agents_in_team and links.agent1 == agent_inspected) and links.aware > 0:

									state_grade = ActionFunctions.action_grade_calculator(links, teams.issue, 0, agents_in_team, affiliation_weights)
									state_grade_list.append(state_grade)

							# state_grade_list.append(state_grade)
						total_agent_grades.append(sum(state_grade_list))
						# print('State: ' + str(sum(state_grade_list)))
						
						# AIMS GRADING
						aim_grade_list = []
						# We then go through all agents
						for agent_inspected in teams.members:
							# Take the list of links
							for links in link_list:
								# Check that only the link of interest is selected
								if (links.agent1 == agents_in_team and links.agent2 == agent_inspected) or (links.agent2 == agents_in_team and links.agent1 == agent_inspected) and links.aware > 0:

									aim_grade = ActionFunctions.action_grade_calculator(links, teams.issue, 1, agents_in_team, affiliation_weights)
									aim_grade_list.append(aim_grade)

						total_agent_grades.append(sum(aim_grade_list))
						# print('Aim: ' + str(sum(aim_grade_list)))
					

					# c. Finding the best action
					# print('total_agent_grades ', len(total_agent_grades))
					best_action_index = total_agent_grades.index(max(total_agent_grades))
					agent_best_action = int(best_action_index/(len(cw_of_interest) + 1 + 1))
					best_action = best_action_index - (agent_best_action)*(len(cw_of_interest) + 1 + 1)

					# print(' ')
					# print('----- Considering new action grading -----')
					# print('best_action_index: ' + str(best_action_index))
					# print('Number of actions per agent: ' + str((len(cw_of_interest) + 1 + 1)))
					# print('Number of agents performing actions: ' + str(len(teams.members)))
					# print('Action to be performed: ' + str(best_action))
					# print('Agent performing the action: ' + str(agent_best_action))
					
					# d. Implementation the best action

					for agent_impacted in teams.members:
						# Selecting the link:
						for links in link_list:
							# Check that only the link of interest is selected
							if (links.agent1 == teams.members[agent_best_action] and links.agent2 == agent_impacted) or (links.agent2 == teams.members[agent_best_action] and links.agent1 == agent_impacted) and links.aware > 0:

								# Update of the aware decay parameter
								links.aware_decay = 5

								# The causal relation action is performed
								if best_action <= len(cw_of_interest) - 1:
									# print(' ')
									# print('Performing a causal relation framing action')
									# print('best_action: ' + str(best_action))
									# print('cw_of_interest: ' + str(cw_of_interest))
									# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

									implemented_action = ActionFunctions.action_implementor(links, cw_of_interest[best_action], 0, teams.members[agent_best_action], teams, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(teams.members))
										
								# The state change is performed
								if best_action == len(cw_of_interest):
									# print(' ')
									# print('Performing a state change action')
									# print('best_action: ' + str(best_action))

									implemented_action = ActionFunctions.action_implementor(links, teams.issue, 0, teams.members[agent_best_action], teams, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(teams.members))

								# The aim change is performed
								if best_action == len(cw_of_interest) + 1:
									# print(' ')
									# print('Performing an aim change action')
									# print('best_action: ' + str(best_action))

									implemented_action = ActionFunctions.action_implementor(links, teams.issue, 1, teams.members[agent_best_action], teams, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(teams.members))
				
					# Updating the resources of the team
					teams.resources[1] -= teams.resources[0]*0.1

					# Resources check
					if teams.resources[1] <= 0.5 * teams.resources[0]:
						# print('RAN OUT OF RESOURCES!')
						break

			# If the team is advocating for a problem, the following tasks are completed
			if teams.issue_type == 'policy':

				# As long as there are enough resources (50% of the total)
				while True:
					# a. First exchange of information on all causal relations and the policy issue of the team
					#  Exchange of knowledge on the policy (state and aim)

					impact_number = len(teams.lead.belieftree_policy[0][teams.issue])
					
					self.knowledge_exchange_team(teams, teams.issue, 0)
					self.knowledge_exchange_team(teams, teams.issue, 1)
					# Exchange of knowledge on the causal relations

					for impact in range(impact_number):
						self.knowledge_exchange_team_policy(teams, teams.issue, impact)
					
					# b. Compiling all actions for each actor

					# We select one agent at a time
					total_agent_grades = []
					for agents_in_team in teams.members:
						#  We look at one causal relation at a time:
						# print(' ')
						# print(agents_in_team)	
						for impact in range(impact_number):
							impact_grade_list = []
							# We then go through all agents
							for agent_inspected in teams.members:
								# Take the list of links
								for links in link_list:
									# Check that only the link of interest is selected
									if (links.agent1 == agents_in_team and links.agent2 == agent_inspected) or (links.agent2 == agents_in_team and links.agent1 == agent_inspected) and links.aware > 0:

										impact_grade = ActionFunctions.action_grade_calculator_3S_AS(links, impact, agents_in_team, affiliation_weights, conflict_level_coef)
										impact_grade_list.append(impact_grade)
								
							total_agent_grades.append(sum(impact_grade_list))

							# print('CR: ' + str(cw) + ' with grade: ' + str(sum(impact_grade_list)))

						# We look at the state for the policy
						state_grade_list = []
						# We then go through all agents
						for agent_inspected in teams.members:
							# Take the list of links
							for links in link_list:
								# Check that only the link of interest is selected
								if (links.agent1 == agents_in_team and links.agent2 == agent_inspected) or (links.agent2 == agents_in_team and links.agent1 == agent_inspected) and links.aware > 0:

									state_grade = ActionFunctions.action_grade_calculator(links, teams.issue, 0, agents_in_team, affiliation_weights)
									state_grade_list.append(state_grade)

						total_agent_grades.append(sum(state_grade_list))
						# print('State: ' + str(sum(state_grade_list)))
						
						# We look at the aim for the policy
						aim_grade_list = []
						# We then go through all agents
						for agent_inspected in teams.members:
							# Take the list of links
							for links in link_list:
								# Check that only the link of interest is selected
								if (links.agent1 == agents_in_team and links.agent2 == agent_inspected) or (links.agent2 == agents_in_team and links.agent1 == agent_inspected) and links.aware > 0:

									aim_grade = ActionFunctions.action_grade_calculator(links, teams.issue, 1, agents_in_team, affiliation_weights)
									aim_grade_list.append(aim_grade)

						total_agent_grades.append(sum(aim_grade_list))
						# print('Aim: ' + str(sum(aim_grade_list)))
					

					# c. Finding the best action
					best_action_index = total_agent_grades.index(max(total_agent_grades))
					agent_best_action = int(best_action_index/(impact_number + 1 + 1))
					best_action = best_action_index - (agent_best_action)*(impact_number + 1 + 1)

					# print(' ')
					# print('----- Considering new action grading -----')
					# print('best_action_index: ' + str(best_action_index))
					# print('Number of actions per agent: ' + str(impact_number + 1 + 1))
					# print('Number of agents performing actions: ' + str(len(teams.members)))
					# print('Action to be performed: ' + str(best_action))
					# print('Agent performing the action: ' + str(agent_best_action))

					# d. Implementation the best action

					for agent_impacted in teams.members:
						# Selecting the link:
						for links in link_list:
							# Check that only the link of interest is selected
							if (links.agent1 == teams.members[agent_best_action] and links.agent2 == agent_impacted) or (links.agent2 == teams.members[agent_best_action] and links.agent1 == agent_impacted) and links.aware > 0:

								# Update of the aware decay parameter
								links.aware_decay = 5

								# The causal relation action is performed
								if best_action <= impact_number - 1:
									# print(' ')
									# print('Performing a causal relation framing action')
									# print('best_action: ' + str(best_action))
									# print('cw_of_interest: ' + str(cw_of_interest))
									# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

									implemented_action = ActionFunctions.action_implementor_3S_AS(links, teams.issue, best_action, 0, teams.members[agent_best_action], teams, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(teams.members))
										
								# The state change is performed
								if best_action == impact_number:
									# print(' ')
									# print('Performing a state change action')
									# print('best_action: ' + str(best_action))

									implemented_action = ActionFunctions.action_implementor(links, teams.issue, 0, teams.members[agent_best_action], teams, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(teams.members))

								# The aim change is performed
								if best_action == impact_number + 1:
									# print(' ')
									# print('Performing an aim change action')
									# print('best_action: ' + str(best_action))

									implemented_action = ActionFunctions.action_implementor(links, teams.issue, 1, teams.members[agent_best_action], teams, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(teams.members))

					# Updating the resources of the team
					teams.resources[1] -= teams.resources[0]*0.1

					# Resources check
					if teams.resources[1] <= 0.5 * teams.resources[0]:
						# print('RAN OUT OF RESOURCES!')
						break

			# 2. Inter-team actions (actions performed on agents outside the team)

			# Creation of the list of agents to be considered:
			inter_agent_list = []
			for potential_agent in agent_action_list:
				if potential_agent not in teams.members:
					inter_agent_list.append(potential_agent)
			# print(' ')
			# print('# of agents not in the team: ' + str(len(inter_agent_list)))

			# Creation of the shadow network for this team
			# Check that the shadow network does not exist yet
			network_existence_check = False
			for links in threeS_link_list_as:
				# Teams can only be as agent1 in the links
				if links.agent1 == teams:
					network_existence_check = True
					# Stop checking the links if one has been found already (for comptutional efficiency)
					break

			# If the shadow network doesnt exist create it
			if network_existence_check == False:
				# print('We need to create a link network for this team!')
				for agent_network in inter_agent_list:
					# Do not take into account EP with no interest in that issue for the network
					if agent_network.belieftree[0][teams.issue][0] != 'No':
						# print(' ')
						# print('Added 1 - ' + str(agent_network))
						self.new_link_threeS_as(link_list, agent_network, teams, threeS_link_list_as, threeS_link_list_as_total, threeS_link_id_as, len_PC, len_ML, len_S, conflict_level_coef, conflict_level_option)

			# If the shadow network exists then update the aware, conflict level, aware_decay
			if network_existence_check == True:
				# Checking that no new members where added - in which case new links would have to be created
				list_agent2 = []
				# print(' ')
				for links in threeS_link_list_as:
					if links.agent1 == teams:
						# print('Agent 1: ' + str(links.agent1) + ', team ID: ' + str(teams) + ' and the ' + str(links))
						list_agent2.append(links.agent2)
				# print(' ')
				# print('The two numbers below should match:')
				# print('# of agents not in the team: ' + str(len(inter_agent_list)))	
				# print('After check, this is # of agents not in the team having a link with the team: ' + str(len(list_agent2)))

				# If there are more links than agents outside the team, remove links
				if len(list_agent2) > len(inter_agent_list):
					# Go through all agents members of the team
					for item in teams.members:
						# Go through the list of all links
						for links in threeS_link_list_as:
							# If the link between the team and the member of the team exists, add it for removal
							if links.agent1 == teams and links.agent2 == item:
								# Procede to remove the link from the list of links considered for the teams
								# print(' ')
								# print(str(links) + ' is being deleted.')
								threeS_link_list_as.remove(links)

				# If there are less links than there are agents outside the team, add links
				if len(list_agent2) < len(inter_agent_list):
					# Add new links
					# Finding the agents to be added
					link_to_be_added = []
					for item in list_agent2:
						if item not in inter_agent_list:
							# print('We need to add a new link!')
							link_to_be_added.append(item)
					# print('----------------------------------')
					# print('')
					# print('Link length to be added: ' + str(len(link_to_be_added)))
					for new_team_agent in link_to_be_added:
						# Do not take into account EP with no interest in that issue for the network
						if new_team_agent.belieftree[0][teams.issue][0] != 'No':
							# print(' ')
							# print('Added 2: ' + str(new_team_agent))
							self.new_link_threeS_as(link_list, new_team_agent, teams, threeS_link_list_as, threeS_link_list_as_total, threeS_link_id_as, len_PC, len_ML, len_S, conflict_level_coef, conflict_level_option)

				# For updates:
				# Go through all the links
				for links in threeS_link_list_as:
					# Select the links related to this team only
					if links.agent1 == teams:
						# Make sure to select an existing link
						if links.aware != -1:
							# Update of the awareness level
							team_aware, agent_with_highest_awareness = PolicyNetworkLinks.awareness_level_selection(link_list, teams, links.agent2)

							# Update of the conflict level
							conflict_level = PolicyNetworkLinks.conflict_level_calculation(teams, links.agent2, conflict_level_coef, conflict_level_option, agent_with_highest_awareness, len_PC, len_ML, len_S)

							# Placing the new conflict level in the link itself
							links.conflict_level = conflict_level

			# Performing the actions using the shadow network and the individual agents within the team

			# If the team is advocating for a problem, the following tasks are completed
			if teams.issue_type == 'problem':

				# As long as there are enough resources (50% of the total)
				while True:

					# print('Performing inter-team actions')

					cw_of_interest = []
					# We only consider the causal relations related to the problem on the agenda
					for cw_choice in range(len(deep_core)):
							cw_of_interest.append(len_PC + len_ML + len_S + len_PC + (teams.issue - len_PC) + cw_choice * len(mid_level))
					# print(' ')
					# print('cw_of_interest: ' + str(cw_of_interest))

					# Going through each of the agents that are part of the team
					total_agent_grades = []
					for agents_in_team in teams.members:
						# Going through all agents that are not part of the team
						link_count = 0
						for links in threeS_link_list_as:
							# Make sure to only select the links related to this team
							if teams == links.agent1 and links.aware > 0:
								link_count += 1
								# Setting the action weight
								# Removed for now for technical issues
								if type(links.agent2).__name__ == 'Policymakers':
										actionWeight = 1
								else:
									actionWeight = 0.95
								# Framing actions:
								for cw in range(len(cw_of_interest)):

									# Grade calculation using the likelihood method
									# Same affiliation
									if agents_in_team.affiliation == links.agent2.affiliation:
										cw_grade = links.conflict_level[2 + cw_of_interest[cw] - (len_PC + len_ML + len_S)] * links.aware * actionWeight
										total_agent_grades.append(cw_grade)

									# Affiliation 1-2
									if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 1) or \
										(agents_in_team.affiliation == 1 and links.agent2.affiliation == 0):
										cw_grade = links.conflict_level[2 + cw_of_interest[cw] - (len_PC + len_ML + len_S)] * links.aware * actionWeight * affiliation_weights[0]
										total_agent_grades.append(cw_grade)

									# Affiliation 1-3
									if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 2) or \
										(agents_in_team.affiliation == 2 and links.agent2.affiliation == 0):
										cw_grade = links.conflict_level[2 + cw_of_interest[cw] - (len_PC + len_ML + len_S)] * links.aware * actionWeight * affiliation_weights[1]
										total_agent_grades.append(cw_grade)

									# Affiliation 2-3
									if (agents_in_team.affiliation == 1 and links.agent2.affiliation == 2) or \
										(agents_in_team.affiliation == 2 and links.agent2.affiliation == 1):
										cw_grade = links.conflict_level[2 + cw_of_interest[cw] - (len_PC + len_ML + len_S)] * links.aware * actionWeight * affiliation_weights[2]
										total_agent_grades.append(cw_grade)	

									
								# State influence actions
								# Grade calculation using the likelihood method
								# Same affiliation
								if agents_in_team.affiliation == links.agent2.affiliation:
									state_grade = links.conflict_level[0] * links.aware * actionWeight
									total_agent_grades.append(state_grade)

								# Affiliation 1-2
								if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 1) or \
									(agents_in_team.affiliation == 1 and links.agent2.affiliation == 0):
									state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[0]
									total_agent_grades.append(state_grade)

								# Affiliation 1-3
								if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 2) or \
									(agents_in_team.affiliation == 2 and links.agent2.affiliation == 0):
									state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[1]
									total_agent_grades.append(state_grade)

								# Affiliation 2-3
								if (agents_in_team.affiliation == 1 and links.agent2.affiliation == 2) or \
									(agents_in_team.affiliation == 2 and links.agent2.affiliation == 1):
									state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[2]
									total_agent_grades.append(state_grade)	

								# Aim influence actions
								# Grade calculation using the likelihood method
								# Same affiliation
								if agents_in_team.affiliation == links.agent2.affiliation:
									aim_grade = links.conflict_level[1] * links.aware * actionWeight
									total_agent_grades.append(aim_grade)

								# Affiliation 1-2
								if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 1) or \
									(agents_in_team.affiliation == 1 and links.agent2.affiliation == 0):
									aim_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[0]
									total_agent_grades.append(aim_grade)

								# Affiliation 1-3
								if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 2) or \
									(agents_in_team.affiliation == 2 and links.agent2.affiliation == 0):
									aim_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[1]
									total_agent_grades.append(aim_grade)

								# Affiliation 2-3
								if (agents_in_team.affiliation == 1 and links.agent2.affiliation == 2) or \
									(agents_in_team.affiliation == 2 and links.agent2.affiliation == 1):
									aim_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[2]
									total_agent_grades.append(aim_grade)									

					if len(total_agent_grades) == 0:
						break

					# Choosing the best action
					best_action_index = total_agent_grades.index(max(total_agent_grades))
					best_action = best_action_index - int(best_action_index/(len(cw_of_interest) + 1 + 1))*(len(cw_of_interest) + 1 + 1)
					number_actions = int(best_action_index/(len(cw_of_interest) + 1 + 1))
					acting_agent = int(number_actions/link_count)
					acted_upon_agent = number_actions-acting_agent*link_count

					# print(' ')
					# print('----- Considering new action grading -----')
					# print('best_action_index: ' + str(best_action_index))
					# print('Number of actions per agent: ' + str(len(cw_of_interest) + 1 + 1))
					# print('Number of agents performing actions: ' + str(len(teams.members)))
					# print('Number of links considered per agent: ' + str(link_count))
					# print('Action to be performed: ' + str(best_action))
					# print('Agent performing the action: ' + str(acting_agent))
					# print('Agent on which the action is performed: ' + str(acted_upon_agent))
					
					# Actually performing the action:
					# Getting a list of the links related to this team
					list_links_teams = []
					for links in threeS_link_list_as:
							# Make sure to only select the links related to this team
							if teams == links.agent1 and links.aware > 0:
								list_links_teams.append(links)	

					# Implement framing action
					if best_action <= len(cw_of_interest) - 1:
						# print(' ')
						# print('Performing a causal relation framing action')
						# print('best_action: ' + str(best_action))
						# print('cw_of_interest: ' + str(cw_of_interest))
						# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

						# print('Before: ' + str(list_links_teams[acted_upon_agent].agent2.belieftree[0][len(deep_core) + len(mid_level) + len(secondary) + best_action - 1][0]))

						# Same affiliation
						if teams.members[acting_agent].affiliation == list_links_teams[acted_upon_agent].agent2.affiliation:
							list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] += \
								(teams.members[acting_agent].belieftree[0][cw_of_interest[best_action]][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0]) * \
								teams.resources[0] * 0.1

						# Affiliation 1-2
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 1) or \
							(teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] += \
								(teams.members[acting_agent].belieftree[0][cw_of_interest[best_action]][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0]) * \
								teams.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] += \
								(teams.members[acting_agent].belieftree[0][cw_of_interest[best_action]][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0]) * \
								teams.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 1):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] += \
								(teams.members[acting_agent].belieftree[0][cw_of_interest[best_action]][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0]) * \
								teams.resources[0] * 0.1 * affiliation_weights[2]	

						# print('After: ' + str(list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0]))
					
						# 1-1 check
						list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] = ActionFunctions.one_minus_one_check(list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer(teams.members[acting_agent], list_links_teams[acted_upon_agent].agent2, cw_of_interest[best_action], 0)

					# Implement state influence action
					if best_action == len(cw_of_interest):
						# print(' ')
						# print('Performing a state change action')
						# print('best_action: ' + str(best_action))

						# Same affiliation
						if teams.members[acting_agent].affiliation == list_links_teams[acted_upon_agent].agent2.affiliation:
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0]) * teams.resources[0] * 0.1

						# Affiliation 1-2
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 1) or \
							(teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0]) * teams.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0]) * teams.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 1):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0]) * teams.resources[0] * 0.1 * affiliation_weights[2]	
						
						# 1-1 check
						list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] = ActionFunctions.one_minus_one_check(list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer(teams.members[acting_agent], list_links_teams[acted_upon_agent].agent2, teams.issue, 0)

					# Implement aim influence action
					if best_action == len(cw_of_interest) + 1:
						# print(' ')
						# print('Performing an aim change action')
						# print('best_action: ' + str(best_action))

						# Same affiliation
						if teams.members[acting_agent].affiliation == list_links_teams[acted_upon_agent].agent2.affiliation:
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][1] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1]) * teams.resources[0] * 0.1

						# Affiliation 1-2
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 1) or \
							(teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][1] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1]) * teams.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][1] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1]) * teams.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 1):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][1] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1]) * teams.resources[0] * 0.1 * affiliation_weights[2]
				
						# 1-1 check
						list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] = ActionFunctions.one_minus_one_check(list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer(teams.members[acting_agent], list_links_teams[acted_upon_agent].agent2, teams.issue, 1)

					# Adjusting the awareness decay of the team members
					for links_to_change in link_list:
						for agents_in_team in teams.members:
							if links_to_change.agent1 == agents_in_team and links_to_change.agent2.unique_id == acted_upon_agent:
								links_to_change.aware_decay = 5
							if links_to_change.agent2 == agents_in_team and links_to_change.agent1.unique_id == acted_upon_agent:
								links_to_change.aware_decay = 5

					# Updating the resources of the team
					teams.resources[1] -= teams.resources[0]*0.1

					# Resources check
					if teams.resources[1] <= 0 * teams.resources[0]:
						break

			# If the team is advocating for a policy, the following tasks are completed

			if teams.issue_type == 'policy':

				impact_number = len(teams.lead.belieftree_policy[0][teams.issue])

				# Calculation of the average of the belief for each of the impacts
				impact_average = []
				for p in range(impact_number):
					per_agent_list = []
					for agent_cf in teams.members:
						per_agent_list.append(agent_cf.belieftree_policy[0][teams.issue][p])
					impact_average.append(sum(per_agent_list)/len(per_agent_list))

				# As long as there are enough resources (50% of the total)
				while True:

					# print('Performing inter-team actions')

					# Going through each of the agents that are part of the team
					total_agent_grades = []
					for agents_in_team in teams.members:
						# Going through all agents that are not part of the team
						link_count = 0
						for links in threeS_link_list_as:
							# Make sure to only select the links related to this team
							if teams == links.agent1 and links.aware > 0:
								link_count += 1
								# Setting the action weight
								# Removed for now for technical issues
								if type(links.agent2).__name__ == 'Policymakers':
										actionWeight = 1
								else:
									actionWeight = 0.95
								# Framing actions:
								for impact in range(impact_number):

									# impact_grade = ActionFunctions.action_grade_calculator_3S_AS(links, impact, agents_in_team, affiliation_weights, conflict_level_coef)
									# total_agent_grades.append(impact_grade)

									# Calculation of the conflict level per impact:
									belief_diff = abs(agents_in_team.belieftree_policy[0][teams.issue][impact] - impact_average[impact])

									if belief_diff <= 0.25:
										conflict_level_impact = conflict_level_coef[0]
									if belief_diff > 0.25 and belief_diff <= 1.75:
										conflict_level_impact = conflict_level_coef[2]
									if belief_diff > 1.75:
										conflict_level_impact = conflict_level_coef[1]

									# Grade calculation using the likelihood method
									# Same affiliation
									if agents_in_team.affiliation == links.agent2.affiliation:
										impact_grade = conflict_level_impact * links.aware * actionWeight
										total_agent_grades.append(impact_grade)

									# Affiliation 1-2
									if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 1) or \
										(agents_in_team.affiliation == 1 and links.agent2.affiliation == 0):
										impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[0]
										total_agent_grades.append(impact_grade)

									# Affiliation 1-3
									if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 2) or \
										(agents_in_team.affiliation == 2 and links.agent2.affiliation == 0):
										impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[1]
										total_agent_grades.append(impact_grade)

									# Affiliation 2-3
									if (agents_in_team.affiliation == 1 and links.agent2.affiliation == 2) or \
										(agents_in_team.affiliation == 2 and links.agent2.affiliation == 1):
										impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[2]
										total_agent_grades.append(impact_grade)	
									
								# State influence actions

								# state_grade = ActionFunctions.action_grade_calculator(links, teams.issue, 0, agents_in_team, affiliation_weights)
								# total_agent_grades.append(state_grade)

								# Grade calculation using the likelihood method
								# Same affiliation
								if agents_in_team.affiliation == links.agent2.affiliation:
									state_grade = links.conflict_level[0] * links.aware * actionWeight
									total_agent_grades.append(state_grade)

								# Affiliation 1-2
								if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 1) or \
									(agents_in_team.affiliation == 1 and links.agent2.affiliation == 0):
									state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[0]
									total_agent_grades.append(state_grade)

								# Affiliation 1-3
								if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 2) or \
									(agents_in_team.affiliation == 2 and links.agent2.affiliation == 0):
									state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[1]
									total_agent_grades.append(state_grade)

								# Affiliation 2-3
								if (agents_in_team.affiliation == 1 and links.agent2.affiliation == 2) or \
									(agents_in_team.affiliation == 2 and links.agent2.affiliation == 1):
									state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[2]
									total_agent_grades.append(state_grade)

								# Aim influence actions

								# aim_grade = ActionFunctions.action_grade_calculator(links, teams.issue, 1, agents_in_team, affiliation_weights)
								# total_agent_grades.append(aim_grade)

								# Grade calculation using the likelihood method
								# Same affiliation
								if agents_in_team.affiliation == links.agent2.affiliation:
									state_grade = links.conflict_level[1] * links.aware * actionWeight
									total_agent_grades.append(state_grade)

								# Affiliation 1-2
								if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 1) or \
									(agents_in_team.affiliation == 1 and links.agent2.affiliation == 0):
									state_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[0]
									total_agent_grades.append(state_grade)

								# Affiliation 1-3
								if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 2) or \
									(agents_in_team.affiliation == 2 and links.agent2.affiliation == 0):
									state_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[1]
									total_agent_grades.append(state_grade)

								# Affiliation 2-3
								if (agents_in_team.affiliation == 1 and links.agent2.affiliation == 2) or \
									(agents_in_team.affiliation == 2 and links.agent2.affiliation == 1):
									state_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[2]
									total_agent_grades.append(state_grade)							

					# Check that some actions were performed
					if len(total_agent_grades) == 0:
						break
					# Choosing the best action
					best_action_index = total_agent_grades.index(max(total_agent_grades))
					best_action = best_action_index - int(best_action_index/(impact_number + 1 + 1))*(impact_number + 1 + 1)
					number_actions = int(best_action_index/(impact_number + 1 + 1))
					acting_agent = int(number_actions/link_count)
					acted_upon_agent = number_actions-acting_agent*link_count

					# print(' ')
					# print('----- Considering new action grading -----')
					# print('best_action_index: ' + str(best_action_index))
					# print('Number of actions per agent: ' + str(impact_number + 1 + 1))
					# print('Number of agents performing actions: ' + str(len(teams.members)))
					# print('Number of links considered per agent: ' + str(link_count))
					# print('Action to be performed: ' + str(best_action))
					# print('Agent performing the action: ' + str(acting_agent))
					# print('Agent on which the action is performed: ' + str(acted_upon_agent))					

					# Actually performing the action:
					# Getting a list of the links related to this team
					list_links_teams = []
					for links in threeS_link_list_as:
							# Make sure to only select the links related to this team
							if teams == links.agent1 and links.aware > 0:
								list_links_teams.append(links)

					# Implement framing action
					if best_action <= impact_number - 1:
						# print(' ')
						# print('Performing a causal relation framing action')
						# print('best_action: ' + str(best_action))

						# print('Before: ' + str(list_links_teams[acted_upon_agent].agent2.belieftree[0][len(deep_core) + len(mid_level) + len(secondary) + best_action][0]))

						# Same affiliation
						if teams.members[acting_agent].affiliation == list_links_teams[acted_upon_agent].agent2.affiliation:
							list_links_teams[acted_upon_agent].agent2.belieftree_policy[0][teams.issue][best_action] += \
								(teams.members[acting_agent].belieftree_policy[0][teams.issue][best_action] - list_links_teams[acted_upon_agent].agent2.belieftree_policy[0][teams.issue][best_action]) * \
								teams.resources[0] * 0.1

						# Affiliation 1-2
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 1) or \
							(teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree_policy[0][teams.issue][best_action] += \
								(teams.members[acting_agent].belieftree_policy[0][teams.issue][best_action] - list_links_teams[acted_upon_agent].agent2.belieftree_policy[0][teams.issue][best_action]) * \
								teams.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree_policy[0][teams.issue][best_action] += \
								(teams.members[acting_agent].belieftree_policy[0][teams.issue][best_action] - list_links_teams[acted_upon_agent].agent2.belieftree_policy[0][teams.issue][best_action]) * \
								teams.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 1):
							list_links_teams[acted_upon_agent].agent2.belieftree_policy[0][teams.issue][best_action] += \
								(teams.members[acting_agent].belieftree_policy[0][teams.issue][best_action] - list_links_teams[acted_upon_agent].agent2.belieftree_policy[0][teams.issue][best_action]) * \
								teams.resources[0] * 0.1 * affiliation_weights[2]

						# print('After: ' + str(list_links_teams[acted_upon_agent].agent2.belieftree[0][len(deep_core) + len(mid_level) + len(secondary) + best_action][0]))
						
						# 1-1 check
						list_links_teams[acted_upon_agent].agent2.belieftree_policy[0][teams.issue][best_action] = ActionFunctions.one_minus_one_check(list_links_teams[acted_upon_agent].agent2.belieftree_policy[0][teams.issue][best_action])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer_policy(teams.members[acting_agent], list_links_teams[acted_upon_agent].agent2, teams.issue, best_action)

					# Implement state influence action
					if best_action == impact_number:
						# print(' ')
						# print('Performing a state change action')
						# print('best_action: ' + str(best_action))

						if teams.members[acting_agent].affiliation == list_links_teams[acted_upon_agent].agent2.affiliation:
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0]) * teams.resources[0] * 0.1

						# Affiliation 1-2
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 1) or \
							(teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0]) * teams.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0]) * teams.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 1):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0]) * teams.resources[0] * 0.1 * affiliation_weights[2]
						
						# 1-1 check
						list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] = ActionFunctions.one_minus_one_check(list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer(teams.members[acting_agent], list_links_teams[acted_upon_agent].agent2, teams.issue, 0)

					# Implement aim influence action
					if best_action == impact_number + 1:
						# print(' ')
						# print('Performing an aim change action')
						# print('best_action: ' + str(best_action))

						if teams.members[acting_agent].affiliation == list_links_teams[acted_upon_agent].agent2.affiliation:
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][1] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1]) * teams.resources[0] * 0.1

						# Affiliation 1-2
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 1) or \
							(teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][1] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1]) * teams.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							llist_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][1] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1]) * teams.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 1):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][1] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1]) * teams.resources[0] * 0.1 * affiliation_weights[2]
						
						# 1-1 check
						list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] = ActionFunctions.one_minus_one_check(list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer(teams.members[acting_agent], list_links_teams[acted_upon_agent].agent2, teams.issue, 1)

					# Adjusting the awareness decay of the team members
					for links_to_change in link_list:
						for agents_in_team in teams.members:
							if links_to_change.agent1 == agents_in_team and links_to_change.agent2.unique_id == acted_upon_agent:
								links_to_change.aware_decay = 5
							if links_to_change.agent2 == agents_in_team and links_to_change.agent1.unique_id == acted_upon_agent:
								links_to_change.aware_decay = 5

					# Updating the resources of the team
					teams.resources[1] -= teams.resources[0]*0.1

					# Resources check
					if teams.resources[1] <= 0 * teams.resources[0]:
						break

	def team_belief_actions_threeS_pf(self, teams, causalrelation_number, deep_core, mid_level, secondary, agent_action_list, threeS_link_list_pf, \
		threeS_link_list_pf_total, threeS_link_id_pf, link_list, affiliation_weights, agenda_prob_3S_as, conflict_level_coef, resources_weight_action, resources_potency, conflict_level_option):

		"""
		Team actions - three streams(policy formulation)
		===========================

		This function is used to perform the team actions. The team actions
		are the same as the individual agent actions as shown in the formalisation.
		For each team, inter- and intra- actions are graded by all possible agents.
		The action that has the highest grade is then selected for
		implementation.

		Depending on whether the team is focused on a policy or a problem, the
		actions will be slightly different.

		"""

		len_PC = len(deep_core)
		len_ML = len(mid_level)
		len_S = len(secondary)

		# print('The belief actions now have to be performed for each team!')
		# Make sure that the team actually axists:
		if len(teams.members) > 0:

			# 0. Asssigning the resources
			teams.resources[1] = teams.resources[0]

			# 1. Intra-team actions (actions performed on agents inside the team)

			# If the team is advocating for a problem, the following tasks are completed
			if teams.issue_type == 'problem':

				# As long as there are enough resources (50% of the total)
				while True:
					# a. First exchange of information on all causal relations and the policy issue of the team
					#  Exchange of knowledge on the policy (state and aim)
					
					self.knowledge_exchange_team(teams, teams.issue, 0)
					self.knowledge_exchange_team(teams, teams.issue, 1)
					# Exchange of knowledge on the causal relations

					cw_of_interest = []
					# We only consider the causal relations related to the problem on the agenda
					for cw_choice in range(len(secondary)):
						cw_of_interest.append(len_PC + len_ML + len_S + (len_PC * len_ML) + (agenda_prob_3S_as - len_PC)*len_S + cw_choice)
					# print(' ')
					# print('cw_of_interest: ' + str(cw_of_interest))

					for cw in range(causalrelation_number):
						self.knowledge_exchange_team(teams, len_PC + len_ML + len_S + cw, 0)
					
					# b. Compiling all actions for each actor

					# We select one agent at a time
					total_agent_grades = []
					for agents_in_team in teams.members:
						#  We look at one causal relation at a time:
						# print(' ')
						# print(agents_in_team)	
						for cw in cw_of_interest:
							cw_grade_list = []
							# We then go through all agents
							for agent_inspected in teams.members:
								# Take the list of links
								for links in link_list:
									# Check that only the link of interest is selected
									if (links.agent1 == agents_in_team and links.agent2 == agent_inspected) or (links.agent2 == agents_in_team and links.agent1 == agent_inspected) and links.aware > 0:

										cw_grade = ActionFunctions.action_grade_calculator(links, cw, 0, agents_in_team, affiliation_weights)
										cw_grade_list.append(cw_grade)
								
							total_agent_grades.append(sum(cw_grade_list))

							# print('CR: ' + str(cw) + ' with grade: ' + str(sum(cw_grade_list)))

						# We look at the state for the policy
						state_grade_list = []
						# We then go through all agents
						for agent_inspected in teams.members:
							# Take the list of links
							for links in link_list:
								# Check that only the link of interest is selected
								if (links.agent1 == agents_in_team and links.agent2 == agent_inspected) or (links.agent2 == agents_in_team and links.agent1 == agent_inspected) and links.aware > 0:

									state_grade = ActionFunctions.action_grade_calculator(links, teams.issue, 0, agents_in_team, affiliation_weights)
									state_grade_list.append(state_grade)

						total_agent_grades.append(sum(state_grade_list))
						# print('State: ' + str(sum(state_grade_list)))
						
						# We look at the aim for the policy
						aim_grade_list = []
						# We then go through all agents
						for agent_inspected in teams.members:
							# Take the list of links
							for links in link_list:
								# Check that only the link of interest is selected
								if (links.agent1 == agents_in_team and links.agent2 == agent_inspected) or (links.agent2 == agents_in_team and links.agent1 == agent_inspected) and links.aware > 0:

									aim_grade = ActionFunctions.action_grade_calculator(links, teams.issue, 1, agents_in_team, affiliation_weights)
									aim_grade_list.append(aim_grade)

						total_agent_grades.append(sum(aim_grade_list))
						# print('Aim: ' + str(sum(aim_grade_list)))
				
					# c. Finding the best action
					best_action_index = total_agent_grades.index(max(total_agent_grades))
					agent_best_action = int(best_action_index/(len(cw_of_interest) + 1 + 1))
					best_action = best_action_index - (agent_best_action)*(len(cw_of_interest) + 1 + 1)

					# print(' ')
					# print('----- Considering new action grading -----')
					# print('best_action_index: ' + str(best_action_index))
					# print('Number of actions per agent: ' + str((len(cw_of_interest) + 1 + 1)))
					# print('Number of agents performing actions: ' + str(len(teams.members)))
					# print('Action to be performed: ' + str(best_action))
					# print('Agent performing the action: ' + str(agent_best_action))

					# d. Implementation the best action

					# The causal relation action is performed
					for agent_impacted in teams.members:
						# Selecting the link:
						for links in link_list:
							# Check that only the link of interest is selected
							if (links.agent1 == teams.members[agent_best_action] and links.agent2 == agent_impacted) or (links.agent2 == teams.members[agent_best_action] and links.agent1 == agent_impacted) and links.aware > 0:

								# Update of the aware decay parameter
								links.aware_decay = 5

								# The causal relation action is performed
								if best_action <= len(cw_of_interest) - 1:
									# print(' ')
									# print('Performing a causal relation framing action')
									# print('best_action: ' + str(best_action))
									# print('cw_of_interest: ' + str(cw_of_interest))
									# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

									implemented_action = ActionFunctions.action_implementor(links, cw_of_interest[best_action], 0, teams.members[agent_best_action], teams, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(teams.members))
										
								# The state change is performed
								if best_action == len(cw_of_interest):
									# print(' ')
									# print('Performing a state change action')
									# print('best_action: ' + str(best_action))

									implemented_action = ActionFunctions.action_implementor(links, teams.issue, 0, teams.members[agent_best_action], teams, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(teams.members))

								# The aim change is performed
								if best_action == len(cw_of_interest) + 1:
									# print(' ')
									# print('Performing an aim change action')
									# print('best_action: ' + str(best_action))

									implemented_action = ActionFunctions.action_implementor(links, teams.issue, 1, teams.members[agent_best_action], teams, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(teams.members))
					
					# Updating the resources of the team
					teams.resources[1] -= teams.resources[0]*0.1

					# Resources check
					if teams.resources[1] <= 0.5 * teams.resources[0]:
						# print('RAN OUT OF RESOURCES!')
						break

			# If the team is advocating for a problem, the following tasks are completed
			if teams.issue_type == 'policy':

				impact_number = len(teams.lead.belieftree_instrument[0][teams.issue])

				# As long as there are enough resources (50% of the total)
				while True:
					# a. First exchange of information on all causal relations and the policy issue of the team
					#  Exchange of knowledge on the policy (state and aim)
					
					self.knowledge_exchange_team(teams, teams.issue, 0)
					self.knowledge_exchange_team(teams, teams.issue, 1)
					# Exchange of knowledge on the causal relations

					for impact in range(impact_number):
						self.knowledge_exchange_team_instrument(teams, teams.issue, impact)
					
					# b. Compiling all actions for each actor
					# We select one agent at a time
					total_agent_grades = []
					for agents_in_team in teams.members:
						#  We look at one causal relation at a time:
						# print(' ')
						# print(agents_in_team)	
						for impact in range(impact_number):
							impact_grade_list = []
							# We then go through all agents
							for agent_inspected in teams.members:
								# Take the list of links
								for links in link_list:
									# Check that only the link of interest is selected
									if (links.agent1 == agents_in_team and links.agent2 == agent_inspected) or (links.agent2 == agents_in_team and links.agent1 == agent_inspected) and links.aware > 0:
										# Make sure to look at the right direction of the conflict level

										impact_grade = ActionFunctions.action_grade_calculator_3S_PF(links, impact, agents_in_team, affiliation_weights, conflict_level_coef)
										impact_grade_list.append(impact_grade)
								
							total_agent_grades.append(sum(impact_grade_list))

						# STATES GRADING
						state_grade_list = []
						# We then go through all agents
						for agent_inspected in teams.members:
							# Take the list of links
							for links in link_list:

								# Check that only the link of interest is selected
								if (links.agent1 == agents_in_team and links.agent2 == agent_inspected) or (links.agent2 == agents_in_team and links.agent1 == agent_inspected) and links.aware > 0:

									state_grade = ActionFunctions.action_grade_calculator(links, teams.issue, 0, agents_in_team, affiliation_weights)
									state_grade_list.append(state_grade)

						total_agent_grades.append(sum(state_grade_list))
						
						# AIMS GRADING
						aim_grade_list = []
						# We then go through all agents
						for agent_inspected in teams.members:
							# Take the list of links
							for links in link_list:

								# Check that only the link of interest is selected
								if (links.agent1 == agents_in_team and links.agent2 == agent_inspected) or (links.agent2 == agents_in_team and links.agent1 == agent_inspected) and links.aware > 0:

									aim_grade = ActionFunctions.action_grade_calculator(links, teams.issue, 1, agents_in_team, affiliation_weights)
									aim_grade_list.append(aim_grade)
							
						total_agent_grades.append(sum(aim_grade_list))
						# print('Aim: ' + str(sum(aim_grade_list)))
					
					# c. Finding the best action
					best_action_index = total_agent_grades.index(max(total_agent_grades))
					agent_best_action = int(best_action_index/(impact_number + 1 + 1))
					best_action = best_action_index - (agent_best_action)*(impact_number + 1 + 1)

					# print(' ')
					# print('----- Considering new action grading -----')
					# print('best_action_index: ' + str(best_action_index))
					# print('Number of actions per agent: ' + str(impact_number + 1 + 1))
					# print('Number of agents performing actions: ' + str(len(teams.members)))
					# print('Action to be performed: ' + str(best_action))
					# print('Agent performing the action: ' + str(agent_best_action))

					# d. Implementation the best action

					for agent_impacted in teams.members:
						# Selecting the link:
						for links in link_list:
							# Check that only the link of interest is selected
							if (links.agent1 == teams.members[agent_best_action] and links.agent2 == agent_impacted) or (links.agent2 == teams.members[agent_best_action] and links.agent1 == agent_impacted) and links.aware > 0:

								# Update of the aware decay parameter
								links.aware_decay = 5

								# The causal relation action is performed
								if best_action <= impact_number - 1:
									# print(' ')
									# print('Performing a causal relation framing action')
									# print('best_action: ' + str(best_action))
									# print('cw_of_interest: ' + str(cw_of_interest))
									# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

									implemented_action = ActionFunctions.action_implementor_3S_PF(links, teams.issue, best_action, 0, teams.members[agent_best_action], teams, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(teams.members))
										
								# The state change is performed
								if best_action == impact_number:
									# print(' ')
									# print('Performing a state change action')
									# print('best_action: ' + str(best_action))

									implemented_action = ActionFunctions.action_implementor(links, teams.issue, 0, teams.members[agent_best_action], teams, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(teams.members))

								# The aim change is performed
								if best_action == impact_number + 1:
									# print(' ')
									# print('Performing an aim change action')
									# print('best_action: ' + str(best_action))

									implemented_action = ActionFunctions.action_implementor(links, teams.issue, 1, teams.members[agent_best_action], teams, \
										affiliation_weights, resources_weight_action, resources_potency, True, len(teams.members))
					
					# Updating the resources of the team
					teams.resources[1] -= teams.resources[0]*0.1

					# Resources check
					if teams.resources[1] <= 0.5 * teams.resources[0]:
						# print('RAN OUT OF RESOURCES!')
						break

			# 2. Inter-team actions (actions performed on agents outside the team)

			# Creation of the list of agents to be considered:
			inter_agent_list = []
			for potential_agent in agent_action_list:
				if potential_agent not in teams.members:
					inter_agent_list.append(potential_agent)
			# print(' ')
			# print('# of agents not in the team: ' + str(len(inter_agent_list)))

			# Creation of the shadow network for this team
			# Check that the shadow network does not exist yet
			network_existence_check = False
			for links in threeS_link_list_pf:
				# Teams can only be as agent1 in the links
				if links.agent1 == teams:
					network_existence_check = True
					# Stop checking the links if one has been found already (for comptutional efficiency)
					if network_existence_check == True:
						break

			# If the shadow network doesnt exist create it
			if network_existence_check == False:
				# print('We need to create a link network for this team!')
				for agent_network in inter_agent_list:
					# Do not take into account EP with no interest in that issue for the network
					if agent_network.belieftree[0][teams.issue][0] != 'No':
						# print(' ')
						# print('Added 1 - ' + str(agent_network))
						self.new_link_threeS_pf(link_list, agent_network, teams, threeS_link_list_pf, threeS_link_list_pf_total, threeS_link_id_pf, len_PC, len_ML, len_S, conflict_level_coef, conflict_level_option)

			# If the shadow network exists then update the aware, conflict level, aware_decay
			if network_existence_check == True:
				# Checking that no new members where added - in which case new links would have to be created
				list_agent2 = []
				# print(' ')
				for links in threeS_link_list_pf:
					if links.agent1 == teams:
						# print('Agent 1: ' + str(links.agent1) + ', team ID: ' + str(teams) + ' and the ' + str(links))
						list_agent2.append(links.agent2)
				# print(' ')
				# print('The two numbers below should match:')
				# print('# of agents not in the team: ' + str(len(inter_agent_list)))	
				# print('After check, this is # of agents not in the team having a link with the team: ' + str(len(list_agent2)))

				# If there are more links than agents outside the team, remove links
				if len(list_agent2) > len(inter_agent_list):
					# Go through all agents members of the team
					for item in teams.members:
						# Go through the list of all links
						for links in threeS_link_list_pf:
							# If the link between the team and the member of the team exists, add it for removal
							if links.agent1 == teams and links.agent2 == item:
								# Procede to remove the link from the list of links considered for the teams
								# print(' ')
								# print(str(links) + ' is being deleted.')
								threeS_link_list_pf.remove(links)

				# If there are less links than there are agents outside the team, add links
				if len(list_agent2) < len(inter_agent_list):
					# Add new links
					# Finding the agents to be added
					link_to_be_added = []
					for item in list_agent2:
						if item not in inter_agent_list:
							# print('We need to add a new link!')
							link_to_be_added.append(item)
					# print('----------------------------------')
					# print('')
					# print('Link length to be added: ' + str(len(link_to_be_added)))
					for new_team_agent in link_to_be_added:
						# Do not take into account EP with no interest in that issue for the network
						if new_team_agent.belieftree[0][teams.issue][0] != 'No':
							# print(' ')
							# print('Added 2: ' + str(new_team_agent))
							self.new_link_threeS_pf(link_list, new_team_agent, teams, threeS_link_list_pf, threeS_link_list_pf_total, threeS_link_id_pf, len_PC, len_ML, len_S, conflict_level_coef, conflict_level_option)

				# For updates:
				# Go through all the links
				for links in threeS_link_list_pf:
					# Select the links related to this team only
					if links.agent1 == teams:
						# Make sure to select an existing link
						if links.aware != -1:
							# Update of the awareness level
							team_aware, agent_with_highest_awareness = PolicyNetworkLinks.awareness_level_selection(link_list, teams, links.agent2)

							# Update of the conflict level
							conflict_level = PolicyNetworkLinks.conflict_level_calculation(teams, links.agent2, conflict_level_coef, conflict_level_option, agent_with_highest_awareness, len_PC, len_ML, len_S)

							# Placing the new conflict level in the link itself
							links.conflict_level = conflict_level

			# Performing the actions using the shadow network and the individual agents within the team

			# If the team is advocating for a problem, the following tasks are completed
			if teams.issue_type == 'problem':

				# As long as there are enough resources (50% of the total)
				while True:

					# print('Performing inter-team actions')

					cw_of_interest = []
					# We only consider the causal relations related to the problem on the agenda
					for cw_choice in range(len(secondary)):
						cw_of_interest.append(len_PC + len_ML + len_S + (len_PC * len_ML) + (agenda_prob_3S_as - len_PC)*len_S + cw_choice)
					# print(' ')
					# print('cw_of_interest: ' + str(cw_of_interest))

					# Going through each of the agents that are part of the team
					total_agent_grades = []
					for agents_in_team in teams.members:
						# Going through all agents that are not part of the team
						link_count = 0
						for links in threeS_link_list_pf:
							# Make sure to select an existing link
							if links.aware != -1:
								# Make sure to only select the links related to this team
								if teams == links.agent1:
									link_count += 1
									# Setting the action weight
									# Removed for now for technical issues
									if type(links.agent2).__name__ == 'Policymakers':
											actionWeight = 1
									else:
										actionWeight = 0.95
									# Framing actions:
									for cw in range(len(cw_of_interest)):

										# Grade calculation using the likelihood method
										# Same affiliation
										if agents_in_team.affiliation == links.agent2.affiliation:
											cw_grade = links.conflict_level[2 + cw_of_interest[cw] - (len_PC + len_ML + len_S)] * links.aware * actionWeight
											total_agent_grades.append(cw_grade)

										# Affiliation 1-2
										if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 1) or \
											(agents_in_team.affiliation == 1 and links.agent2.affiliation == 0):
											cw_grade = links.conflict_level[2 + cw_of_interest[cw] - (len_PC + len_ML + len_S)] * links.aware * actionWeight * affiliation_weights[0]
											total_agent_grades.append(cw_grade)

										# Affiliation 1-3
										if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 2) or \
											(agents_in_team.affiliation == 2 and links.agent2.affiliation == 0):
											cw_grade = links.conflict_level[2 + cw_of_interest[cw] - (len_PC + len_ML + len_S)] * links.aware * actionWeight * affiliation_weights[1]
											total_agent_grades.append(cw_grade)

										# Affiliation 2-3
										if (agents_in_team.affiliation == 1 and links.agent2.affiliation == 2) or \
											(agents_in_team.affiliation == 2 and links.agent2.affiliation == 1):
											cw_grade = links.conflict_level[2 + cw_of_interest[cw] - (len_PC + len_ML + len_S)] * links.aware * actionWeight * affiliation_weights[2]
											total_agent_grades.append(cw_grade)	
										
									# State influence actions
									# Grade calculation using the likelihood method
									# Same affiliation
									if agents_in_team.affiliation == links.agent2.affiliation:
										state_grade = links.conflict_level[0] * links.aware * actionWeight
										total_agent_grades.append(state_grade)

									# Affiliation 1-2
									if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 1) or \
										(agents_in_team.affiliation == 1 and links.agent2.affiliation == 0):
										state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[0]
										total_agent_grades.append(state_grade)

									# Affiliation 1-3
									if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 2) or \
										(agents_in_team.affiliation == 2 and links.agent2.affiliation == 0):
										state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[1]
										total_agent_grades.append(state_grade)

									# Affiliation 2-3
									if (agents_in_team.affiliation == 1 and links.agent2.affiliation == 2) or \
										(agents_in_team.affiliation == 2 and links.agent2.affiliation == 1):
										state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[2]
										total_agent_grades.append(state_grade)	
										
									# Aim influence actions
									# Grade calculation using the likelihood method
									# Same affiliation
									if agents_in_team.affiliation == links.agent2.affiliation:
										aim_grade = links.conflict_level[1] * links.aware * actionWeight
										total_agent_grades.append(aim_grade)

									# Affiliation 1-2
									if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 1) or \
										(agents_in_team.affiliation == 1 and links.agent2.affiliation == 0):
										aim_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[0]
										total_agent_grades.append(aim_grade)

									# Affiliation 1-3
									if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 2) or \
										(agents_in_team.affiliation == 2 and links.agent2.affiliation == 0):
										aim_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[1]
										total_agent_grades.append(aim_grade)

									# Affiliation 2-3
									if (agents_in_team.affiliation == 1 and links.agent2.affiliation == 2) or \
										(agents_in_team.affiliation == 2 and links.agent2.affiliation == 1):
										aim_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[2]
										total_agent_grades.append(aim_grade)									

					if len(total_agent_grades) == 0:
						break

					# Choosing the best action

					best_action_index = total_agent_grades.index(max(total_agent_grades))
					best_action = best_action_index - int(best_action_index/(len(cw_of_interest) + 1 + 1))*(len(cw_of_interest) + 1 + 1)
					number_actions = int(best_action_index/(len(cw_of_interest) + 1 + 1))
					acting_agent = int(number_actions/link_count)
					acted_upon_agent = number_actions-acting_agent*link_count

					# print(' ')
					# print('----- Considering new action grading -----')
					# print('best_action_index: ' + str(best_action_index))
					# print('Number of actions per agent: ' + str(len(cw_of_interest) + 1 + 1))
					# print('Number of agents performing actions: ' + str(len(teams.members)))
					# print('Number of links considered per agent: ' + str(link_count))
					# print('Action to be performed: ' + str(best_action))
					# print('Agent performing the action: ' + str(acting_agent))
					# print('Agent on which the action is performed: ' + str(acted_upon_agent))

					# Actually performing the action:
					# Getting a list of the links related to this team
					list_links_teams = []
					for links in threeS_link_list_pf:
							# Make sure to only select the links related to this team
							if teams == links.agent1:
								# Make sure to select an existing link
								if links.aware != -1:
									list_links_teams.append(links)

					# Implement framing action
					if best_action <= len(cw_of_interest) - 1:
						# print(' ')
						# print('Performing a causal relation framing action')
						# print('best_action: ' + str(best_action))
						# print('cw_of_interest: ' + str(cw_of_interest))
						# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

						# print('Before: ' + str(list_links_teams[acted_upon_agent].agent2.belieftree[0][len(deep_core) + len(mid_level) + len(secondary) + best_action - 1][0]))

						# Same affiliation
						if teams.members[acting_agent].affiliation == list_links_teams[acted_upon_agent].agent2.affiliation:
							list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] += \
								(teams.members[acting_agent].belieftree[0][cw_of_interest[best_action]][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0]) * \
								teams.resources[0] * 0.1

						# Affiliation 1-2
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 1) or \
							(teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] += \
								(teams.members[acting_agent].belieftree[0][cw_of_interest[best_action]][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0]) * \
								teams.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] += \
								(teams.members[acting_agent].belieftree[0][cw_of_interest[best_action]][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0]) * \
								teams.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 1):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] += \
								(teams.members[acting_agent].belieftree[0][cw_of_interest[best_action]][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0]) * \
								teams.resources[0] * 0.1 * affiliation_weights[2]

						# print('After: ' + str(list_links_teams[acted_upon_agent].agent2.belieftree[0][len(deep_core) + len(mid_level) + len(secondary) + best_action - 1][0]))
						
						# 1-1 check
						list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0] = ActionFunctions.one_minus_one_check(list_links_teams[acted_upon_agent].agent2.belieftree[0][cw_of_interest[best_action]][0])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer(teams.members[acting_agent], list_links_teams[acted_upon_agent].agent2, cw_of_interest[best_action], 0)

					# Implement state influence action
					if best_action == len(cw_of_interest):
						# print(' ')
						# print('Performing a state change action')
						# print('best_action: ' + str(best_action))

						# Same affiliation
						if teams.members[acting_agent].affiliation == list_links_teams[acted_upon_agent].agent2.affiliation:
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0]) * teams.resources[0] * 0.1

						# Affiliation 1-2
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 1) or \
							(teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0]) * teams.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0]) * teams.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 1):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0]) * teams.resources[0] * 0.1 * affiliation_weights[2]	
						
						# Checks and transfer of partial knowledge
						# 1-1 check
						list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] = ActionFunctions.one_minus_one_check(list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer(teams.members[acting_agent], list_links_teams[acted_upon_agent].agent2, teams.issue, 0)

					# Implement aim influence action
					if best_action == len(cw_of_interest) + 1:
						# print(' ')
						# print('Performing an aim change action')
						# print('best_action: ' + str(best_action))

						# Same affiliation
						if teams.members[acting_agent].affiliation == list_links_teams[acted_upon_agent].agent2.affiliation:
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][1] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1]) * teams.resources[0] * 0.1

						# Affiliation 1-2
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 1) or \
							(teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][1] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1]) * teams.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][1] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1]) * teams.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 1):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][1] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1]) * teams.resources[0] * 0.1 * affiliation_weights[2]
						
						# 1-1 check
						list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] = ActionFunctions.one_minus_one_check(list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer(teams.members[acting_agent], list_links_teams[acted_upon_agent].agent2, teams.issue, 1)

					# Adjusting the awareness decay of the team members
					for links_to_change in link_list:
						for agents_in_team in teams.members:
							if links_to_change.agent1 == agents_in_team and links_to_change.agent2.unique_id == acted_upon_agent:
								links_to_change.aware_decay = 5
							if links_to_change.agent2 == agents_in_team and links_to_change.agent1.unique_id == acted_upon_agent:
								links_to_change.aware_decay = 5

					# Updating the resources of the team
					teams.resources[1] -= teams.resources[0]*0.1

					# Resources check
					if teams.resources[1] <= 0 * teams.resources[0]:
						break

			# If the team is advocating for a policy, the following tasks are completed
			if teams.issue_type == 'policy':

				impact_number = len(teams.lead.belieftree_instrument[0][teams.issue])

				# Calculation of the average of the belief for each of the impacts
				impact_average = []
				for p in range(impact_number):
					per_agent_list = []
					for agent_cf in teams.members:
						per_agent_list.append(agent_cf.belieftree_instrument[0][teams.issue][p])
					impact_average.append(sum(per_agent_list)/len(per_agent_list))

				# As long as there are enough resources (50% of the total)
				while True:

					# print('Performing inter-team actions')

					impact_number = len(teams.lead.belieftree_instrument[0][teams.issue])

					# Going through each of the agents that are part of the team
					total_agent_grades = []
					for agents_in_team in teams.members:
						# Going through all agents that are not part of the team
						link_count = 0
						for links in threeS_link_list_pf:
							# Make sure to select an existing link
							if links.aware != -1:
								# Make sure to only select the links related to this team
								if teams == links.agent1:
									link_count += 1
									# Setting the action weight
									# Removed for now for technical issues
									if type(links.agent2).__name__ == 'Policymakers':
											actionWeight = 1
									else:
										actionWeight = 0.95
									# Framing actions:
									for impact in range(impact_number):

										# Calculation of the conflict level per impact:
										belief_diff = abs(agents_in_team.belieftree_instrument[0][teams.issue][impact] - impact_average[impact])

										if belief_diff <= 0.25:
											conflict_level_impact = conflict_level_coef[0]
										if belief_diff > 0.25 and belief_diff <= 1.75:
											conflict_level_impact = conflict_level_coef[2]
										if belief_diff > 1.75:
											conflict_level_impact = conflict_level_coef[1]

										# Grade calculation using the likelihood method
										# Same affiliation
										if agents_in_team.affiliation == links.agent2.affiliation:
											impact_grade = conflict_level_impact * links.aware * actionWeight
											total_agent_grades.append(impact_grade)

										# Affiliation 1-2
										if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 1) or \
											(agents_in_team.affiliation == 1 and links.agent2.affiliation == 0):
											impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[0]
											total_agent_grades.append(impact_grade)

										# Affiliation 1-3
										if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 2) or \
											(agents_in_team.affiliation == 2 and links.agent2.affiliation == 0):
											impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[1]
											total_agent_grades.append(impact_grade)

										# Affiliation 2-3
										if (agents_in_team.affiliation == 1 and links.agent2.affiliation == 2) or \
											(agents_in_team.affiliation == 2 and links.agent2.affiliation == 1):
											impact_grade = conflict_level_impact * links.aware * actionWeight * affiliation_weights[2]
											total_agent_grades.append(impact_grade)	

									# State influence actions
									# Grade calculation using the likelihood method
									# Same affiliation
									if agents_in_team.affiliation == links.agent2.affiliation:
										state_grade = links.conflict_level[0] * links.aware * actionWeight
										total_agent_grades.append(state_grade)

									# Affiliation 1-2
									if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 1) or \
										(agents_in_team.affiliation == 1 and links.agent2.affiliation == 0):
										state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[0]
										total_agent_grades.append(state_grade)

									# Affiliation 1-3
									if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 2) or \
										(agents_in_team.affiliation == 2 and links.agent2.affiliation == 0):
										state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[1]
										total_agent_grades.append(state_grade)

									# Affiliation 2-3
									if (agents_in_team.affiliation == 1 and links.agent2.affiliation == 2) or \
										(agents_in_team.affiliation == 2 and links.agent2.affiliation == 1):
										state_grade = links.conflict_level[0] * links.aware * actionWeight * affiliation_weights[2]
										total_agent_grades.append(state_grade)

									# Aim influence actions
									# Grade calculation using the likelihood method
									# Same affiliation
									if agents_in_team.affiliation == links.agent2.affiliation:
										state_grade = links.conflict_level[1] * links.aware * actionWeight
										total_agent_grades.append(state_grade)

									# Affiliation 1-2
									if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 1) or \
										(agents_in_team.affiliation == 1 and links.agent2.affiliation == 0):
										state_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[0]
										total_agent_grades.append(state_grade)

									# Affiliation 1-3
									if (agents_in_team.affiliation == 0 and links.agent2.affiliation == 2) or \
										(agents_in_team.affiliation == 2 and links.agent2.affiliation == 0):
										state_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[1]
										total_agent_grades.append(state_grade)

									# Affiliation 2-3
									if (agents_in_team.affiliation == 1 and links.agent2.affiliation == 2) or \
										(agents_in_team.affiliation == 2 and links.agent2.affiliation == 1):
										state_grade = links.conflict_level[1] * links.aware * actionWeight * affiliation_weights[2]
										total_agent_grades.append(state_grade)								


					if len(total_agent_grades) == 0:
						break
					# Choosing the best action

					best_action_index = total_agent_grades.index(max(total_agent_grades))
					best_action = best_action_index - int(best_action_index/(impact_number + 1 + 1))*(impact_number + 1 + 1)
					number_actions = int(best_action_index/(impact_number + 1 + 1))
					acting_agent = int(number_actions/link_count)
					acted_upon_agent = number_actions-acting_agent*link_count

					# print(' ')
					# print('----- Considering new action grading -----')
					# print('best_action_index: ' + str(best_action_index))
					# print('Number of actions per agent: ' + str(impact_number + 1 + 1))
					# print('Number of agents performing actions: ' + str(len(teams.members)))
					# print('Number of links considered per agent: ' + str(link_count))
					# print('Action to be performed: ' + str(best_action))
					# print('Agent performing the action: ' + str(acting_agent))
					# print('Agent on which the action is performed: ' + str(acted_upon_agent))		
					

					# Actually performing the action:
					# Getting a list of the links related to this team
					list_links_teams = []
					for links in threeS_link_list_pf:
							# Make sure to only select the links related to this team
							if teams == links.agent1:
								# Make sure to select an existing link
								if links.aware != -1:
									list_links_teams.append(links)

					# Implement framing action
					if best_action <= impact_number - 1:
						# print(' ')
						# print('Performing a causal relation framing action')
						# print('best_action: ' + str(best_action))

						# print('Before: ' + str(list_links_teams[acted_upon_agent].agent2.belieftree[0][len(deep_core) + len(mid_level) + len(secondary) + best_action][0]))

						# Same affiliation
						if teams.members[acting_agent].affiliation == list_links_teams[acted_upon_agent].agent2.affiliation:
							list_links_teams[acted_upon_agent].agent2.belieftree_instrument[0][teams.issue][best_action] +=	\
								(teams.members[acting_agent].belieftree_instrument[0][teams.issue][best_action] - list_links_teams[acted_upon_agent].agent2.belieftree_instrument[0][teams.issue][best_action]) * \
								teams.resources[0] * 0.1

						# Affiliation 1-2
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 1) or \
							(teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree_instrument[0][teams.issue][best_action] +=	\
								(teams.members[acting_agent].belieftree_instrument[0][teams.issue][best_action] - list_links_teams[acted_upon_agent].agent2.belieftree_instrument[0][teams.issue][best_action]) * \
								teams.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree_instrument[0][teams.issue][best_action] +=	\
								(teams.members[acting_agent].belieftree_instrument[0][teams.issue][best_action] - list_links_teams[acted_upon_agent].agent2.belieftree_instrument[0][teams.issue][best_action]) * \
								teams.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 1):
							list_links_teams[acted_upon_agent].agent2.belieftree_instrument[0][teams.issue][best_action] +=	\
								(teams.members[acting_agent].belieftree_instrument[0][teams.issue][best_action] - list_links_teams[acted_upon_agent].agent2.belieftree_instrument[0][teams.issue][best_action]) * \
								teams.resources[0] * 0.1 * affiliation_weights[2]

						# print('After: ' + str(list_links_teams[acted_upon_agent].agent2.belieftree[0][len(deep_core) + len(mid_level) + len(secondary) + best_action][0]))
						
						# 1-1 check
						list_links_teams[acted_upon_agent].agent2.belieftree_instrument[0][teams.issue][best_action] = ActionFunctions.one_minus_one_check(list_links_teams[acted_upon_agent].agent2.belieftree_instrument[0][teams.issue][best_action])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer_instrument(teams.members[acting_agent], list_links_teams[acted_upon_agent].agent2, teams.issue, best_action)

					# Implement state influence action
					if best_action == impact_number:
						# print(' ')
						# print('Performing a state change action')
						# print('best_action: ' + str(best_action))

						if teams.members[acting_agent].affiliation == list_links_teams[acted_upon_agent].agent2.affiliation:
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0]) * teams.resources[0] * 0.1

						# Affiliation 1-2
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 1) or \
							(teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0]) * teams.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0]) * teams.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 1):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][0] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0]) * teams.resources[0] * 0.1 * affiliation_weights[2]
						
						# 1-1 check
						list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0] = ActionFunctions.one_minus_one_check(list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][0])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer(teams.members[acting_agent], list_links_teams[acted_upon_agent].agent2, teams.issue, 0)

					# Implement aim influence action
					if best_action == impact_number + 1:
						# print(' ')
						# print('Performing a state change action')
						# print('best_action: ' + str(best_action))
						
						if teams.members[acting_agent].affiliation == list_links_teams[acted_upon_agent].agent2.affiliation:
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][1] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1]) * teams.resources[0] * 0.1

						# Affiliation 1-2
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 1) or \
							(teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][1] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1]) * teams.resources[0] * 0.1 * affiliation_weights[0]

						# Affiliation 1-3
						if (teams.members[acting_agent].affiliation == 0 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 0):
							llist_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][1] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1]) * teams.resources[0] * 0.1 * affiliation_weights[1]

						# Affiliation 2-3
						if (teams.members[acting_agent].affiliation == 1 and list_links_teams[acted_upon_agent].agent2.affiliation == 2) or \
							(teams.members[acting_agent].affiliation == 2 and list_links_teams[acted_upon_agent].agent2.affiliation == 1):
							list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] += \
								(teams.members[acting_agent].belieftree[0][teams.issue][1] - list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1]) * teams.resources[0] * 0.1 * affiliation_weights[2]
						
						# 1-1 check
						list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1] = ActionFunctions.one_minus_one_check(list_links_teams[acted_upon_agent].agent2.belieftree[0][teams.issue][1])

						# Checks and transfer of partial knowledge
						partial_knowledge = ActionFunctions.partial_knowledge_transfer(teams.members[acting_agent], list_links_teams[acted_upon_agent].agent2, teams.issue, 1)

					# Adjusting the awareness decay of the team members
					for links_to_change in link_list:
						for agents_in_team in teams.members:
							if links_to_change.agent1 == agents_in_team and links_to_change.agent2.unique_id == acted_upon_agent:
								links_to_change.aware_decay = 5
							if links_to_change.agent2 == agents_in_team and links_to_change.agent1.unique_id == acted_upon_agent:
								links_to_change.aware_decay = 5

					# Updating the resources of the team
					teams.resources[1] -= teams.resources[0]*0.1

					# Resources check
					if teams.resources[1] <= 0 * teams.resources[0]:
						break

	def new_link_threeS(self, conflict_level_coef, link_list, outsider_agent, teams, conflict_level_option, len_PC, len_ML, len_S):

		"""
		The new link function - three streams shadow network
		===========================

		This function is used to create new links for the team shadow
		networks. These links are obtained through looking at whichever
		member in the team has the highest awareness level for that agent.

		When creating a new link, the conflict level is also set along with the
		awareness decay. This is the agenda setting version of the function. 

		"""

		# 1. We look for the highest awareness level
		team_aware, agent_with_highest_awareness = PolicyNetworkLinks.awareness_level_selection(link_list, teams, outsider_agent)

		# 2. We calculate the conflict level
		# Note that the conflict level is only of interest for the issue advocated by the team (simplifying things)
		# All causal relations are considered as any might be called up during the belief influence actions

		# There are two ways to calculate the conflict level:
		#	0. Uses full knowledge for the calculation
		#	1. Uses the partial knowledge of the agent with the highest amount of awareness for the calculation

		conflict_level = PolicyNetworkLinks.conflict_level_calculation(teams, outsider_agent, conflict_level_coef, conflict_level_option, agent_with_highest_awareness, len_PC, len_ML, len_S)

		# 3. We set the aware decay
		aware_decay = 0

		return conflict_level, aware_decay, team_aware

	def new_link_threeS_as(self, link_list, outsider_agent, teams, threeS_link_list_as, threeS_link_list_as_total, threeS_link_id_as, len_PC, len_ML, len_S, conflict_level_coef, conflict_level_option):

		"""
		The new link function - three streams shadow network (agenda setting)
		===========================

		This function is used to create new links for the team shadow
		networks. These links are obtained through looking at whichever
		member in the team has the highest awareness level for that agent.

		When creating a new link, the conflict level is also set along with the
		awareness decay. This is the agenda setting version of the function. 

		"""

		# 1/2/3. Initial part of the new link creation (common to AS and PF)
		conflict_level, aware_decay, team_aware = self.new_link_threeS(conflict_level_coef, link_list, outsider_agent, teams, conflict_level_option, len_PC, len_ML, len_S)

		# 4. We create the link
		team_link = PolicyNetworkLinks(threeS_link_id_as[0], teams, outsider_agent, team_aware, aware_decay, conflict_level)
		threeS_link_list_as.append(team_link)
		threeS_link_list_as_total.append(team_link)
		threeS_link_id_as[0] += 1

	def new_link_threeS_pf(self, link_list, outsider_agent, teams, threeS_link_list_pf, threeS_link_list_pf_total, threeS_link_id_pf, len_PC, len_ML, len_S, conflict_level_coef, conflict_level_option):

		"""
		The new link function - three streams shadow network (policy formulation)
		===========================

		This function is used to create new links for the team shadow
		networks. These links are obtained through looking at whichever
		member in the team has the highest awareness level for that agent.

		When creating a new link, the conflict level is also set along with the
		awareness decay. This is the agenda setting version of the function. 

		"""

		# 1/2/3. Initial part of the new link creation (common to AS and PF)
		conflict_level, aware_decay, team_aware = self.new_link_threeS(conflict_level_coef, link_list, outsider_agent, teams, conflict_level_option, len_PC, len_ML, len_S)

		# 4. We create the link
		team_link = PolicyNetworkLinks(threeS_link_id_pf[0], teams, outsider_agent, team_aware, aware_decay, conflict_level)
		threeS_link_list_pf.append(team_link)
		threeS_link_list_pf_total.append(team_link)
		threeS_link_id_pf[0] += 1

	def knowledge_exchange_team(self, team, cw_knowledge, parameter):

		"""
		Knowledge exchange function - issues - teams
		===========================

		This function is used for the exchange of partial knowledge between agents
		within the same team. This only regards the issue that is selected by the team
		and is kept with a certain amount of randomness.
		
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

	def knowledge_exchange_team_policy(self, team, cw_knowledge, parameter):

		"""
		Knowledge exchange function - policies - teams
		===========================

		This function is used for the exchange of partial knowledge between agents
		within the same team. This only regards the policy that is selected by the team
		and is kept with a certain amount of randomness.
		
		"""

		# Exchange of partial knowledge between the agents in the team
		for agent_exchange1 in team.members:
			for agent_exchange2 in team.members:
				# Actual knowledge exchange with a randomness of 0.2
				# print('Before: ' + str(agent_exchange1.belieftree[1 + agent_exchange2.unique_id][team.issue][0]))
				agent_exchange1.belieftree_policy[1 + agent_exchange2.unique_id][cw_knowledge][parameter] = \
				  agent_exchange2.belieftree_policy[0][cw_knowledge][0] + (random.random()/5) - 0.1
				# print('After: ' + str(agent_exchange1.belieftree[1 + agent_exchange2.unique_id][team.issue][0]))
				# 1-1 check
				if agent_exchange1.belieftree_policy[1 + agent_exchange2.unique_id][cw_knowledge][parameter] > 1:
					agent_exchange1.belieftree_policy[1 + agent_exchange2.unique_id][cw_knowledge][parameter] = 1
				if agent_exchange1.belieftree_policy[1 + agent_exchange2.unique_id][cw_knowledge][parameter] < -1:
					agent_exchange1.belieftree_policy[1 + agent_exchange2.unique_id][cw_knowledge][parameter]  = -1

	def knowledge_exchange_team_instrument(self, team, cw_knowledge, parameter):

		"""
		Knowledge exchange function - instruments - teams
		===========================

		This function is used for the exchange of partial knowledge between agents
		within the same team. This only regards the instrument that is selected by the team
		and is kept with a certain amount of randomness.
		
		"""

		# Exchange of partial knowledge between the agents in the team
		for agent_exchange1 in team.members:
			for agent_exchange2 in team.members:
				# Actual knowledge exchange with a randomness of 0.2
				# print('Before: ' + str(agent_exchange1.belieftree[1 + agent_exchange2.unique_id][team.issue][0]))
				agent_exchange1.belieftree_instrument[1 + agent_exchange2.unique_id][cw_knowledge][parameter] = \
				  agent_exchange2.belieftree_instrument[0][cw_knowledge][0] + (random.random()/5) - 0.1
				# print('After: ' + str(agent_exchange1.belieftree[1 + agent_exchange2.unique_id][team.issue][0]))
				# 1-1 check
				if agent_exchange1.belieftree_instrument[1 + agent_exchange2.unique_id][cw_knowledge][parameter] > 1:
					agent_exchange1.belieftree_instrument[1 + agent_exchange2.unique_id][cw_knowledge][parameter] = 1
				if agent_exchange1.belieftree_instrument[1 + agent_exchange2.unique_id][cw_knowledge][parameter] < -1:
					agent_exchange1.belieftree_instrument[1 + agent_exchange2.unique_id][cw_knowledge][parameter]  = -1
