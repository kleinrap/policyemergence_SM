import random
import copy
from team_creation import Team
from coalition_creation import Coalition
from functions_actions import ActionFunctions

class Agent:
	
	def __init__(self, unique_id, model):
		self.unique_id = unique_id
		self.model = model

	def step(self):

		pass

	def network_upkeep_as(self, agents, link_list, affiliation_weights, AS_theory):

		"""
		Network update function (agenda setting)
		===========================

		This function is used to perform the maintenance and upkeep actions for the
		networks during the agenda setting. Two strategies are considered for these
		actions.

		Strategy 1 - Largest network strategy:
		For this, the agents focus on maintenaing all links awareness level at a 
		low level while opening new links wherever possible.

		Strategy 2 - Focus network strategy:
		For this, the agents focus on maintenaing the awareness of the links at a
		high level.

		"""

		# print('This is the agent: ' + str(agents))

		if agents.network_strategy == 1:
			# if there are still resources left:
			# First step: Check agents with less than 0.3
			low_link_list = []
			low_link_list_aware = []
			low_link = True
			# Check if there are resources left or if there still low level links
			while agents.resources_network > 0.0001 and low_link == True:
				# print('Agent network resources: ' + str(agents.resources_network))
				for links in link_list:
					# finding all links related to this agent and with aware higher than 0 and lower than 0.3
					if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0 and links.aware < 0.3:
						# print('Links list: ' + str(links) + ' with their aware: ' + str(links.aware))
						low_link_list.append(links)
						low_link_list_aware.append(links.aware)
				# Make sure that the list is not 0
				if len(low_link_list) > 0:
					# print('Trust list: ' + str(low_link_list_aware))
					index_min_aware = low_link_list_aware.index(min(low_link_list_aware))
					# print('Chosen index: ' + str(index_min_aware))
					# print(low_link_list[index_min_aware].aware)
					# print('The link upgrade is link: ' + str(low_link_list[index_min_aware]) + ' with aware: ' + str(low_link_list[index_min_aware].aware))
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						low_link_list[index_min_aware].aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
				      (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						low_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						low_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						low_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					# print('        ')
					# print('        ')
					low_link_list = []
					low_link_list_aware = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					low_link = False
			# 
			# Second step: Make new links:
			new_link_list = []
			new_link = True
			while agents.resources_network > 0.0001 and new_link == True:
				# The list is shuffled such that it is not always the links with the smallest ID that are selected:
				shuffled_list_links = link_list
				random.shuffle(shuffled_list_links)
				for links in shuffled_list_links:
					if (links.agent1 == agents or links.agent2 == agents) and links.aware == 0:
						new_link_list.append(links)
				if len(new_link_list) > 0:
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						random.choice(new_link_list).aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
				      (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					new_link_list = []
				else:
						# print('Loop stops now because there is no more 0 aware links.')
					new_link = False

			# Third step: Raise aware of remaining links:
			normal_link_list = []
			normal_link = True
			while agents.resources_network > 0.0001 and normal_link == True:
				for links in link_list:
					if (links.agent1 == agents or links.agent2 == agents) and links.aware <= 1 and links.aware != -1:
						normal_link_list.append(links)
				if len(normal_link_list) > 0:
					normal_link_to_change = random.choice(normal_link_list)
					if links.agent1.affiliation == links.agent2.affiliation:
						normal_link_to_change.aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
				      (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						normal_link_to_change.aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						normal_link_to_change.aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						normal_link_to_change.aware += 0.04*agents.resources[0]*affiliation_weights[2]
					# Make sure that no link will have a aware level higher than 1
					if normal_link_to_change.aware > 1:
						normal_link_to_change.aware = 1
					agents.resources_network -= 0.04*agents.resources[0]
					normal_link_list = []
				else:
					# print('All loops are their highest level.')
					new_link = False
	
		if agents.network_strategy  == 2:

			# First step: Check agents with more than 0.7 and similar beliefs
			high_link_list = []
			high_link_list_aware = []
			high_link = True
			# Check if there are resources left or if there still high level links
			while agents.resources_network > 0.0001 and high_link == True:
				for links in link_list:
					# finding all links related to this agent and with lower than than 0.7 and with similar belief:
					# similar belief is defined as if one of the two agents has their selected problem with 0.2 of the other.
					if AS_theory != 2:
						if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0.7 and links.aware <= 1 and \
						(abs(links.agent1.belieftree[0][links.agent1.select_as_issue][1] - links.agent1.belieftree[0][links.agent2.select_as_issue][1]) < 0.2 or 
						  abs(links.agent2.belieftree[0][links.agent1.select_as_issue][1] - links.agent2.belieftree[0][links.agent2.select_as_issue][1]) < 0.2):
							high_link_list.append(links)
							high_link_list_aware.append(links.aware)	
					if AS_theory == 2:			
						if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0.7 and links.aware <= 1 and \
						(abs(links.agent1.belieftree[0][links.agent1.select_problem_3S_as][1] - links.agent1.belieftree[0][links.agent2.select_problem_3S_as][1]) < 0.2 or 
						  abs(links.agent2.belieftree[0][links.agent1.select_problem_3S_as][1] - links.agent2.belieftree[0][links.agent2.select_problem_3S_as][1]) < 0.2):
							high_link_list.append(links)
							high_link_list_aware.append(links.aware)
				# Make sure that the list is not 0
				if len(high_link_list) > 0:
					index_min_aware = high_link_list_aware.index(min(high_link_list_aware))
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						# print('Same affiliation')
						high_link_list[index_min_aware].aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
					  (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						# print('Affiliation 1 and 2')
						high_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
					# print(' Affiliation 1 and 3')
						high_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[1]
						# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						# print('Affiliation 2 and 3')
						high_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[2]
					# Check that it is smaller than 1
					if high_link_list[index_min_aware].aware > 1:
						high_link_list[index_min_aware].aware = 1
					agents.resources_network -= 0.04*agents.resources[0]
					# print(high_link_list[index_min_aware].aware)
					high_link_list = []
					high_link_list_aware = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					high_link = False

			# Second step: Check agents with that are 0 and similar beliefs
			new_link_list = []
			new_link = True
			# Check if there are resources left or if there still high level links
			while agents.resources_network > 0.0001 and new_link == True:
				# print('Agent network resources: ' + str(agents.resources_network))
				shuffled_list_links = link_list
				random.shuffle(shuffled_list_links)
				for links in shuffled_list_links:
					# finding all links related to this agent and with aware of 0 and with similar belief:
					# similar belief is defined as if one of the two agents has their selected problem with 0.2 of the other.
					if AS_theory != 2:
						if (links.agent1 == agents or links.agent2 == agents) and links.aware == 0 and \
						(abs(links.agent1.belieftree[0][links.agent1.select_as_issue][1] - links.agent1.belieftree[0][links.agent2.select_as_issue][1]) < 0.2 or 
						  abs(links.agent2.belieftree[0][links.agent1.select_as_issue][1] - links.agent2.belieftree[0][links.agent2.select_as_issue][1]) < 0.2):
							# print(str(links) + ' with their aware: ' + str(links.aware))
							new_link_list.append(links)
					if AS_theory == 2:
						if (links.agent1 == agents or links.agent2 == agents) and links.aware == 0 and \
						(abs(links.agent1.belieftree[0][links.agent1.select_problem_3S_as][1] - links.agent1.belieftree[0][links.agent2.select_problem_3S_as][1]) < 0.2 or 
						  abs(links.agent2.belieftree[0][links.agent1.select_problem_3S_as][1] - links.agent2.belieftree[0][links.agent2.select_problem_3S_as][1]) < 0.2):
							# print(str(links) + ' with their aware: ' + str(links.aware))
							new_link_list.append(links)
						
				# Make sure that the list is not 0
				if len(new_link_list) > 0:
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						# print('Same affiliation')
						random.choice(new_link_list).aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
					  (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						# print('Affiliation 1 and 2')
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						# print(' Affiliation 1 and 3')
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						# print('Affiliation 2 and 3')
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					new_link_list = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					new_link = False
				
			# Third step: Raise agents with low aware
			medium_link_list = []
			medium_link_list_aware = []
			medium_link = True
			# Check if there are resources left or if there still high level links
			while agents.resources_network > 0.0001 and medium_link == True:
				# print('Agent network resources: ' + str(agents.resources_network))
				for links in link_list:
					# finding all links related to this agent and with lower than than 0.7 and with similar belief:
					# similar belief is defined as if one of the two agents has their selected problem with 0.2 of the other.
					if (links.agent1 == agents or links.agent2 == agents) and links.aware < 0.7 and links.aware > 0:
						# print(str(links) + ' with their aware: ' + str(links.aware))
						medium_link_list.append(links)
						medium_link_list_aware.append(links.aware)
				# print(medium_link_list)
						
				# Make sure that the list is not 0
				if len(medium_link_list) > 0:
					index_min_aware = medium_link_list_aware.index(min(medium_link_list_aware))
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						# print('Same affiliation')
						medium_link_list[index_min_aware].aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
					  (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						# print('Affiliation 1 and 2')
						medium_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						# print(' Affiliation 1 and 3')
						medium_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						# print('Affiliation 2 and 3')
						medium_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					# print('Tadah! ' + str(medium_link_list[index_min_aware].aware))
					medium_link_list = []
					medium_link_list_aware = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					medium_link = False

			# Fourth step: Check agents with that are 0 and similar beliefs
			new2_link_list = []
			new2_link = True
			# Check if there are resources left or if there still high level links
			while agents.resources_network > 0.0001 and new2_link == True:
				# print('Agent network resources: ' + str(agents.resources_network))
				shuffled_list_links = link_list
				random.shuffle(shuffled_list_links)
				for links in shuffled_list_links:
					# finding all links related to this agent and with aware of 0:
					# similar belief is defined as if one of the two agents has their selected problem with 0.2 of the other.
					if (links.agent1 == agents or links.agent2 == agents) and links.aware == 0:
						# print(str(links) + ' with their aware: ' + str(links.aware))
						new2_link_list.append(links)
						
				# Make sure that the list is not 0
				if len(new2_link_list) > 0:
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						# print('Same affiliation')
						random.choice(new2_link_list).aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
					  (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						# print('Affiliation 1 and 2')
						random.choice(new2_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						# print(' Affiliation 1 and 3')
						random.choice(new2_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						# print('Affiliation 2 and 3')
						random.choice(new2_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					new2_link_list = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					new2_link = False

	def network_upkeep_pf(self, agents, link_list, affiliation_weights, agenda_as_issue, agenda_prob_3S_as, PF_theory):

		"""
		Network update function (policy formulation)
		===========================

		Note: This is the same function as the one for the agenda setting function
		but with modification for the policy formulation part. This means changes in
		the selection of the selected issues.

		This function is used to perform the maintenance and upkeep actions for the
		networks during the policy formulation. Two strategies are considered for
		these actions.

		Strategy 1 - Largest network strategy:
		For this, the agents focus on maintenaing all links awareness level at a 
		low level while opening new links wherever possible.

		Strategy 2 - Focus network strategy:
		For this, the agents focus on maintenaing the awareness of the links at a
		high level.

		"""

		# print('This is the agent: ' + str(agents))

		if agents.network_strategy  == 1:
			# if there are still resources left:
			# First step: Check agents with less than 0.3
			low_link_list = []
			low_link_list_aware = []
			low_link = True
			# Check if there are resources left or if there still low level links
			while agents.resources_network > 0.0001 and low_link == True:
				# print('Agent network resources: ' + str(agents.resources_network))
				for links in link_list:
					# finding all links related to this agent and with aware higher than 0 and lower than 0.3
					if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0 and links.aware < 0.3:
						# print('Links list: ' + str(links) + ' with their aware: ' + str(links.aware))
						low_link_list.append(links)
						low_link_list_aware.append(links.aware)
				# Make sure that the list is not 0
				if len(low_link_list) > 0:
					# print('Trust list: ' + str(low_link_list_aware))
					index_min_aware = low_link_list_aware.index(min(low_link_list_aware))
					# print('Chosen index: ' + str(index_min_aware))
					# print(low_link_list[index_min_aware].aware)
					# print('The link upgrade is link: ' + str(low_link_list[index_min_aware]) + ' with aware: ' + str(low_link_list[index_min_aware].aware))
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						low_link_list[index_min_aware].aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
				      (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						low_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						low_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						low_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					# print('        ')
					# print('        ')
					low_link_list = []
					low_link_list_aware = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					low_link = False
			# 
			# Second step: Make new links:
			new_link_list = []
			new_link = True
			while agents.resources_network > 0.0001 and new_link == True:
				# The list is shuffled such that it is not always the links with the smallest ID that are selected:
				shuffled_list_links = link_list
				random.shuffle(shuffled_list_links)
				for links in shuffled_list_links:
					if (links.agent1 == agents or links.agent2 == agents) and links.aware == 0:
						new_link_list.append(links)
				if len(new_link_list) > 0:
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						random.choice(new_link_list).aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
				      (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					new_link_list = []
				else:
						# print('Loop stops now because there is no more 0 aware links.')
					new_link = False

			# Third step: Raise aware of remaining links:
			normal_link_list = []
			normal_link = True
			while agents.resources_network > 0.0001 and normal_link == True:
				for links in link_list:
					if (links.agent1 == agents or links.agent2 == agents) and links.aware <= 1 and links.aware != -1:
						normal_link_list.append(links)
				if len(normal_link_list) > 0:
					normal_link_to_change = random.choice(normal_link_list)
					if links.agent1.affiliation == links.agent2.affiliation:
						normal_link_to_change.aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
				      (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						normal_link_to_change.aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						normal_link_to_change.aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						normal_link_to_change.aware += 0.04*agents.resources[0]*affiliation_weights[2]
					# Make sure that no link will have a aware level higher than 1
					if normal_link_to_change.aware > 1:
						normal_link_to_change.aware = 1
					agents.resources_network -= 0.04*agents.resources[0]
					normal_link_list = []
				else:
					# print('All loops are their highest level.')
					new_link = False
	
		if agents.network_strategy  == 2:

			if PF_theory != 2:
				same_belief_issue = agenda_as_issue

			if PF_theory == 2:
				same_belief_issue = agenda_prob_3S_as

			# First step: Check agents with more than 0.7 and similar beliefs
			high_link_list = []
			high_link_list_aware = []
			high_link = True
			# Check if there are resources left or if there still high level links
			while agents.resources_network > 0.0001 and high_link == True:
				for links in link_list:
					# finding all links related to this agent and with lower than than 0.7 and with similar belief:
					# similar belief is defined as if one of the two agents has their selected problem with 0.2 of the other.
					if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0.7 and links.aware <= 1 and \
					(abs(links.agent1.belieftree[0][same_belief_issue][1] - links.agent1.belieftree[0][same_belief_issue][1]) < 0.2 or 
					  abs(links.agent2.belieftree[0][same_belief_issue][1] - links.agent2.belieftree[0][same_belief_issue][1]) < 0.2):
						high_link_list.append(links)
						high_link_list_aware.append(links.aware)					
				# Make sure that the list is not 0
				if len(high_link_list) > 0:
					index_min_aware = high_link_list_aware.index(min(high_link_list_aware))
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						# print('Same affiliation')
						high_link_list[index_min_aware].aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
					  (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						# print('Affiliation 1 and 2')
						high_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
					# print(' Affiliation 1 and 3')
						high_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[1]
						# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						# print('Affiliation 2 and 3')
						high_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[2]
					# Check that it is smaller than 1
					if high_link_list[index_min_aware].aware > 1:
						high_link_list[index_min_aware].aware = 1
					agents.resources_network -= 0.04*agents.resources[0]
					# print(high_link_list[index_min_aware].aware)
					high_link_list = []
					high_link_list_aware = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					high_link = False

			# Second step: Check agents with that are 0 and similar beliefs
			new_link_list = []
			new_link = True
			# Check if there are resources left or if there still high level links
			while agents.resources_network > 0.0001 and new_link == True:
				# print('Agent network resources: ' + str(agents.resources_network))
				shuffled_list_links = link_list
				random.shuffle(shuffled_list_links)
				for links in shuffled_list_links:
					# finding all links related to this agent and with aware of 0 and with similar belief:
					# similar belief is defined as if one of the two agents has their selected problem with 0.2 of the other.
					if (links.agent1 == agents or links.agent2 == agents) and links.aware == 0 and \
					(abs(links.agent1.belieftree[0][same_belief_issue][1] - links.agent1.belieftree[0][same_belief_issue][1]) < 0.2 or 
					  abs(links.agent2.belieftree[0][same_belief_issue][1] - links.agent2.belieftree[0][same_belief_issue][1]) < 0.2):
						# print(str(links) + ' with their aware: ' + str(links.aware))
						new_link_list.append(links)
						
				# Make sure that the list is not 0
				if len(new_link_list) > 0:
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						# print('Same affiliation')
						random.choice(new_link_list).aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
					  (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						# print('Affiliation 1 and 2')
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						# print(' Affiliation 1 and 3')
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						# print('Affiliation 2 and 3')
						random.choice(new_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					new_link_list = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					new_link = False
				
			# Third step: Raise agents with low aware
			medium_link_list = []
			medium_link_list_aware = []
			medium_link = True
			# Check if there are resources left or if there still high level links
			while agents.resources_network > 0.0001 and medium_link == True:
				# print('Agent network resources: ' + str(agents.resources_network))
				for links in link_list:
					# finding all links related to this agent and with lower than than 0.7 and with similar belief:
					# similar belief is defined as if one of the two agents has their selected problem with 0.2 of the other.
					if (links.agent1 == agents or links.agent2 == agents) and links.aware < 0.7 and links.aware > 0:
						# print(str(links) + ' with their aware: ' + str(links.aware))
						medium_link_list.append(links)
						medium_link_list_aware.append(links.aware)
				# print(medium_link_list)
						
				# Make sure that the list is not 0
				if len(medium_link_list) > 0:
					index_min_aware = medium_link_list_aware.index(min(medium_link_list_aware))
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						# print('Same affiliation')
						medium_link_list[index_min_aware].aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
					  (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						# print('Affiliation 1 and 2')
						medium_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						# print(' Affiliation 1 and 3')
						medium_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						# print('Affiliation 2 and 3')
						medium_link_list[index_min_aware].aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					# print('Tadah! ' + str(medium_link_list[index_min_aware].aware))
					medium_link_list = []
					medium_link_list_aware = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					medium_link = False

			# Fourth step: Check agents with that are 0 and similar beliefs
			new2_link_list = []
			new2_link = True
			# Check if there are resources left or if there still high level links
			while agents.resources_network > 0.0001 and new2_link == True:
				# print('Agent network resources: ' + str(agents.resources_network))
				shuffled_list_links = link_list
				random.shuffle(shuffled_list_links)
				for links in shuffled_list_links:
					# finding all links related to this agent and with aware of 0:
					# similar belief is defined as if one of the two agents has their selected problem with 0.2 of the other.
					if (links.agent1 == agents or links.agent2 == agents) and links.aware == 0:
						# print(str(links) + ' with their aware: ' + str(links.aware))
						new2_link_list.append(links)
						
				# Make sure that the list is not 0
				if len(new2_link_list) > 0:
					# Calculating the change in aware depending on resources and affiliation weight
					# Same affiliation
					if links.agent1.affiliation == links.agent2.affiliation:
						# print('Same affiliation')
						random.choice(new2_link_list).aware += 0.04*agents.resources[0]
					# Affiliation 1 and 2
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 1) or \
					  (links.agent1.affiliation == 1 and links.agent2.affiliation == 0):
						# print('Affiliation 1 and 2')
						random.choice(new2_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[0]
					# Affiliation 1 and 3
					if (links.agent1.affiliation == 0 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 0):
						# print(' Affiliation 1 and 3')
						random.choice(new2_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[1]
					# Affiliation 2 and 3
					if (links.agent1.affiliation == 1 and links.agent2.affiliation == 2) or \
					  (links.agent1.affiliation == 2 and links.agent2.affiliation == 1):
						# print('Affiliation 2 and 3')
						random.choice(new2_link_list).aware += 0.04*agents.resources[0]*affiliation_weights[2]
					agents.resources_network -= 0.04*agents.resources[0]
					new2_link_list = []
				# if it is, stop the loop
				else:
					# print('Loop stops now because there is no more low aware.')
					new2_link = False

	def agent_team_threeS_as(self, agents, agent_action_list, team_list_as, team_list_as_total, link_list, team_number_as, tick_number, threeS_link_list_as, policy_core, \
		mid_level, secondary, team_gap_threshold, team_belief_problem_threshold, team_belief_policy_threshold):

		"""
		Agent-team actions - Three streams (agenda setting)
		===========================

		This function is used to perform all the agent-team actions during the
		agent setting. The actions are given in order as follows:
			a. Belonging level update
			b. Leave team check
			c. Disband team check
			d. Join team
			e. Start team

		The team considered within this step are teams that are only present in
		the agenda setting. The agents also only consider the issues they have
		selected for the agenda setting.

		"""

		len_PC = len(policy_core)
		len_ML = len(mid_level)
		len_S = len(secondary)

		# print(' ')
		# print(agents.select_issue_3S_as)
		# agents.select_issue_3S_as = 'policy'
		# print(agents.select_issue_3S_as)

		# Calculation needed for the choice of the causal relation
		prefered_Pr = []
		for policy_core_issues in range(len_PC):
			prefered_Pr.append(agents.belieftree[0][policy_core_issues][2])
		prefered_Pr = prefered_Pr.index(max(prefered_Pr))

		# a. Belonging level update (completed)
		if agents.team_as[0] != None:
			self.belonging_level_as(agents, len_PC, len_ML)

		# b. Leave team check (completed)
		if agents.team_as[0] != None:
			# If the belonging level is below 30%, we remove the agent from the team
			if agents.team_as[1] < 0.3:
				# If the agent is the lead agent, then the team is disbanded
				team = agents.team_as[0]
				if agents == agents.team_as[0].lead:
					# Disband function
					self.disband_team_as(agents, team, threeS_link_list_as, team_list_as)

				# Else only this agent is removed
				else:
					self.remove_agent_team_as(agents)
					# If the length of the team becomes too small, then the team has to be disbanded:
					if len(team.members) < 3:
						# Disband function
						self.disband_team_as(agents, team, threeS_link_list_as, team_list_as)

		# c. Disband team check (completed)		
		if agents.team_as[0] != None:
			# Several cases for which a team can be disbanded:
			# 1. Lead agent changes selected problem/policy
			# This is checked every five ticks
			if (tick_number - agents.team_as[0].creation) % 1 == 0 and tick_number >= 5:
				# 1. Lead agent has different issue than the team issue (checked every five ticks)
				# Check that the agent is the lead of this team
				if agents == agents.team_as[0].lead:
					# Check that the agent has different issue type (problem/policy) or different issue number
					if agents.select_problem_3S_as != agents.team_as[0].issue or agents.select_issue_3S_as != agents.team_as[0].issue_type:
						team = agents.team_as[0]
						# Disband function
						self.disband_team_as(agents, team, threeS_link_list_as, team_list_as)

				# 2. Checking if each agent meets the requirements and remove if not
				# Check that the agent has same issue type (problem/policy) and same issue number
				elif agents.select_problem_3S_as == agents.team_as[0].issue and agents.select_issue_3S_as == agents.team_as[0].issue_type:

					# If the team is advocating for a problem, perform the following actions:
					if agents.team_as[0].issue_type == 'problem':
						team = agents.team_as[0]
						agent_removed = 0
						for agent_members in team.members:
							# Opposite of the requirements for the creation of a team

							if abs(team.lead.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.team_as[0].issue - len_PC)][0] - \
								agent_members.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.team_as[0].issue - len_PC)][0]) >= team_belief_problem_threshold or \
								abs(agent_members.belieftree[0][agents.select_problem_3S_as][0] - agent_members.belieftree[0][agents.select_problem_3S_as][1]) < team_gap_threshold:
								# Disband the team if the leader doesnt meet the requirements anymore
								if agent_members == team.lead:
									self.disband_team_as(agents, team, threeS_link_list_as, team_list_as)
									break
								else:
									self.remove_agent_team_as(agent_members)
									agent_removed = 1
									print('AS - Pr - THIS AGENT HAS TO BE REMOVED: ' + str(agent_members) + ' from ' + str(team))
									if agents == agent_members:
										print('I AM THE AGENT, BREAK AFTER ME')
										break

					# If the team is advocating for a policy, perform the following actions:
					elif agents.team_as[0].issue_type == 'policy':
						team = agents.team_as[0]
						agent_removed = 0
						for agent_members in team.members:
							# Opposite of the requirements for the creation of a team
							if abs(team.lead.belieftree_policy[0][agents.team_as[0].issue][team.lead.select_problem_3S_as - len_PC] - \
								agent_members.belieftree_policy[0][agents.team_as[0].issue][team.lead.select_problem_3S_as - len_PC]) >= team_belief_policy_threshold or \
								abs(agent_members.belieftree[0][team.lead.select_problem_3S_as][0] - agent_members.belieftree[0][team.lead.select_problem_3S_as][1]) < team_gap_threshold:
								# Disband the team if the leader doesnt meet the requirements anymore
								if agent_members == team.lead:

									self.disband_team_as(agents, team, threeS_link_list_as, team_list_as)
									break
								else:
									# Remove the agent if it does not satisfy the requirements anymore
									self.remove_agent_team_as(agent_members)
									agent_removed = 1
									print('AS - Po - THIS AGENT HAS TO BE REMOVED: ' + str(agent_members) + ' from ' + str(team))
									if agents == agent_members:
										print('I AM THE AGENT, BREAK AFTER ME')
										break

					# Recalculate the belonging level of the agents left
					if agents.team_as[0] != None:
						if agent_removed == 1:
							for agent_members in team.members:
								self.belonging_level_as(agent_members, len_PC, len_ML)

								# If the belonging level is below 30%, the agents are removed (similar to a previous loop)
								if agent_members.team_as[1] < 0.3:
									# team = agents.team_as[0]
									if agent_members == agent_members.team_as[0].lead:
										self.disband_team_as(agent_members, team, threeS_link_list_as, team_list_as)
									else:
										self.remove_agent_team_as(agent_members)
										if len(team.members) < 3:
											self.disband_team_as(agent_members, team, threeS_link_list_as, team_list_as)

					# Check the length of the team after all agents have been checked - disband if too small
					if agents.team_as[0] != None:
						if len(team.members) < 3:
							self.disband_team_as(agents, team, threeS_link_list_as, team_list_as)

		# d. Join a team (completed)
		if agents.team_as[0] == None:

			while True:

				added_team_check = 0

				for join_team in team_list_as:

					# If the team is advocating for a problem, the following tasks are completed
					if join_team.issue_type == 'problem':

						# Check that the team is still active and has members:
						if len(join_team.members) > 0:

							# None check
							check_none = 0
							if agents.belieftree[1+join_team.lead.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (join_team.issue - len_PC)][0] == None:
								agents.belieftree[1+join_team.lead.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (join_team.issue - len_PC)][0] = 0
								check_none = 1

							# First we check that the agent meets both requirements (based on partial knowledge) (we assume that the agent knows who the leader is)
							if abs(agents.belieftree[0][join_team.lead.select_problem_3S_as][0] - agents.belieftree[0][join_team.lead.select_problem_3S_as][1]) >= team_gap_threshold and \
								abs(agents.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (join_team.issue - len_PC)][0] - \
							  	agents.belieftree[1+join_team.lead.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (join_team.issue - len_PC)][0]) < team_belief_problem_threshold:

								# Add the agent to the team
								join_team.members.append(agents)
								join_team.members_id.append(agents.unique_id)

								agents.team_as[0] = join_team
								# Share knowledge within the team
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(join_team, join_team.issue, 0)

								# Change belonging level
								self.belonging_level_as(agents, len_PC, len_ML)

								# Notify that the loop can be stopped as the agent has been added
								added_team_check = 1

							# None reset
							if check_none == 1:
								agents.belieftree[1+join_team.lead.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (join_team.issue - len_PC)][0] = None

							# update of the resources
							agents.resources[1] -= 0.02 * agents.resources[0]

							# Resources sufficiency check
							if agents.resources[1] < 0.5 * agents.resources[0]:
								break

							# If the agent has been added to a team, stop this entire procedure
							if added_team_check == 1:
								break

					# If the team is advocating for a policy, the following tasks are completed
					elif join_team.issue_type == 'policy':

						# Check that the team is still active and has members:
						if len(join_team.members) > 0:

							# None check
							check_none = 0

							# team.lead.belieftree_policy[0][agents.team_as[0].issue][team.lead.select_problem_3S_as - len_PC]

							if agents.belieftree_policy[1+join_team.lead.unique_id][join_team.issue][join_team.lead.select_problem_3S_as - len_PC] == None:
								agents.belieftree_policy[1+join_team.lead.unique_id][join_team.issue][join_team.lead.select_problem_3S_as - len_PC] = 0
								check_none = 1

							# First we check that the agent meets both requirements (based on partial knowledge) (we assume that the agent knows who the leader is)
							if abs(agents.belieftree[0][join_team.issue][0] - agents.belieftree[0][join_team.issue][1]) >= team_gap_threshold and \
								abs(agents.belieftree_policy[0][join_team.issue][join_team.lead.select_problem_3S_as - len_PC] - \
								agents.belieftree_policy[1+join_team.lead.unique_id][join_team.issue][join_team.lead.select_problem_3S_as - len_PC]) < team_belief_policy_threshold:
								print(' ')
								print('Checked - Join 1!')

								# Add the agent to the team
								join_team.members.append(agents)
								join_team.members_id.append(agents.unique_id)
								agents.team_as[0] = join_team
								# Share knowledge within the team
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(join_team, join_team.issue, 0)

								# Change belonging level
								self.belonging_level_as(agents, len_PC, len_ML)

								# Notify that the loop can be stopped as the agent has been added
								added_team_check = 1

							# None reset
							if check_none == 1:
								agents.belieftree_policy[1+join_team.lead.unique_id][join_team.issue][join_team.lead.select_problem_3S_as - len_PC] = None

							# update of the resources
							agents.resources[1] -= 0.02 * agents.resources[0]

							# Resources sufficiency check
							if agents.resources[1] < 0.5 * agents.resources[0]:
								break

							# If the agent has been added to a team, stop this entire procedure
							if added_team_check == 1:
								break

				break

		# e. Start a team (completed)
		if agents.team_as[0] == None:
			# First team creation method:
			# Avoided for now - requires memory

			# print('agents.select_issue_3S_as: ' + str(agents.select_issue_3S_as))
			# print('agents.team_as[2]: ' + str(agents.team_as[2]))

			# Second team creation method:
			# a. Method 0 - All agents that qualify are selected
			if agents.team_as[2] == 0:
				# print(' ')
				# print(' ')
				# print('Strategy 0')

				# If the agent is advocating or a problem, the following tasks are performed
				if agents.select_issue_3S_as == 'problem':

					# Check if the agent indeed has a gap:
					if abs(agents.belieftree[0][agents.select_problem_3S_as][0] - agents.belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold:

						team_list_potential_agent = []
						shuffled_list_links = link_list
						random.shuffle(shuffled_list_links)
						for links in shuffled_list_links:
							# Make sure that there is aware
							if links.aware > 0:
								# print(links)
								
								# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not None
								if links.agent1 == agents and links.agent2.team_as[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] != 'No':

									# Check if no partial knowledge (initial value)
									if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] == None:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = 0
									if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] == None:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = 0
									if agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] == None:
										agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = 0

									# Check for the gap and the similarity in states based on partial knowledge - if okay, add the agent to the list
									if abs(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] - agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
										abs(agents.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] - \
									  	agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0]) < team_belief_problem_threshold:
										# Add the agent to the list of potential candidates
										team_list_potential_agent.append(links.agent2)

									# Actual knowledge exchange with a randomness of 0.5
									# Knowledge gained by the lead agent:
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = links.agent2.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
									agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = \
										links.agent2.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] + (random.random()/2) - 0.25
									# 1-1 check
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = \
										ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0])
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = \
										ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1])
									agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = \
										ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0])

									# Knowledge gained by the secondary link agent:
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
									links.agent2.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = \
										agents.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] + (random.random()/2) - 0.25
									# 1-1 check
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = \
										ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0])
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = \
										ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1])
									links.agent2.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = \
										ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0])

									# Adjusting resources
									agents.resources[1] -= 0.02 * agents.resources[0]
									links.agent2.resources[1] -= 0.01 * links.agent2.resources[0]

								# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
								if links.agent2 == agents and links.agent1.team_as[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = 0
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = 0
										if agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] == None:
											agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = 0

										# Check for the gap and the similarity in states based on partial knowledge
										if abs(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] - agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
											abs(agents.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] - \
										  	agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0]) < team_belief_problem_threshold:
											
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent1)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = links.agent1.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = links.agent1.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = \
											links.agent1.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0])
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1])
										agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0])

										# Knowledge gained by the secondary link agent:
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = \
											agents.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0])
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1])
										links.agent1.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent1.resources[1] -= 0.01 * links.agent1.resources[0]

						# If the list has more than 2 agents, then we can check to create a team
						if len(team_list_potential_agent) > 1:
							team_list_actual_agent = []
							# Make a new list containing the agent that actually match the requirements
							for potential_agent in team_list_potential_agent:
								if agents.belieftree[0][agents.select_problem_3S_as][0] != 'No':
									if abs(agents.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] - \
										potential_agent.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0]) < team_belief_problem_threshold and \
										abs(potential_agent.belieftree[0][agents.select_problem_3S_as][0] - potential_agent.belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold:
								  		team_list_actual_agent.append(potential_agent)
								else:
									print('1. ALERT - THIS IS AN INTRUDER - A AGENT THAT SHOULDNT BE IN THIS TEAM IS IN THIS TEAM')

							# Check that the list is still more than two agents and if so create the team:
							if len(team_list_potential_agent) > 1:

								# Now we can create the team						
								members = team_list_potential_agent
								members.append(agents)
								team_resources = [0, 0]
								members_id = []
								for members_for_id in members:
									members_id.append(members_for_id.unique_id)
								team = Team(team_number_as[0], agents, members, members_id, agents.select_issue_3S_as, agents.select_problem_3S_as, tick_number, team_resources)
								print('TEAM CREATION 1! ')
								# Iteration of the team ID number for the overall team list
								team_number_as[0] += 1
								team_list_as.append(team)
								team_list_as_total.append(team)
								
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(team, team.issue, 0)

								# Calculation of the average issue belief for belonging calculation (based on partial knowledge) per agent:
								for agent_members1 in team.members:
									# Setting the partial knowledge for himself equal to his own belief:
									agent_members1.belieftree[1+agent_members1.unique_id][team.issue][0] = agent_members1.belieftree[0][team.issue][0]
									# Calculating the average belief according to partial knowledge
									issue_avg_belief = []
									for agent_members2 in team.members:
										if agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0] != 'No':
											issue_avg_belief.append(agent_members2.resources[0]*agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0])
										else:
											print('2. ALERT - THIS IS AN INTRUDER - A AGENT THAT SHOULDNT BE IN THIS TEAM IS IN THIS TEAM')
									issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
									# Setting the belonging level
									agent_members1.team_as[1] = 1 - abs(agent_members1.belieftree[0][team.issue][0] - issue_avg_belief)
									# Setting of the team object
									agent_members1.team_as[0] = team
								# Setting the team resources
								for agent_members in team.members:
									team.resources[0] += agent_members.team_as[1]
									team.resources[1] = team.resources[0]

				# If the agent is advocating or a policy, the following tasks are performed
				if agents.select_issue_3S_as == 'policy':

					# Check if the agent indeed has a gap:
					if abs(agents.belieftree[0][agents.select_problem_3S_as][0] - agents.belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold:

						team_list_potential_agent = []
						shuffled_list_links = link_list
						random.shuffle(shuffled_list_links)
						for links in shuffled_list_links:
							# Make sure that there is aware
							if links.aware > 0:
								# print(links)
								
								# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not None
								if links.agent1 == agents and links.agent2.team_as[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] != 'No':

									# Check if no partial knowledge (initial value)
									if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] == None:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = 0
									if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] == None:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = 0
									if agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] == None:
										agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = 0

									# Check for the gap and the similarity in states based on partial knowledge - if okay, add the agent to the list
									if abs(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] - agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
										abs(agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] - \
									  	agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC]) < team_belief_policy_threshold:
										# Add the agent to the list of potential candidates
										team_list_potential_agent.append(links.agent2)

									# Actual knowledge exchange with a randomness of 0.5
									# Knowledge gained by the lead agent:
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = links.agent2.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
									agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = \
										links.agent2.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] + (random.random()/2) - 0.25
									# 1-1 check
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = \
										ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0])
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = \
										ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1])
									agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = \
										ActionFunctions.one_minus_one_check(agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC])

									# Knowledge gained by the secondary link agent:
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
									links.agent2.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = \
										agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] + (random.random()/2) - 0.25
									# 1-1 check
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = \
										ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0])
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = \
										ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1])
									links.agent2.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = \
										ActionFunctions.one_minus_one_check(links.agent2.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC])

									# Adjusting resources
									agents.resources[1] -= 0.02 * agents.resources[0]
									links.agent2.resources[1] -= 0.01 * links.agent2.resources[0]

								# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
								if links.agent2 == agents and links.agent1.team_as[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] != 'No':

									# Check if no partial knowledge (initial value)
									if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] == None:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = 0
									if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] == None:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = 0
									if agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] == None:
										agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = 0

									# Check for the gap and the similarity in states based on partial knowledge
									if abs(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] - agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
										abs(agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] - \
									  	agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC]) < team_belief_policy_threshold:
										
										# Add the agent to the list of potential candidates
										team_list_potential_agent.append(links.agent1)

									# Actual knowledge exchange with a randomness of 0.5
									# Knowledge gained by the lead agent:
									agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = links.agent1.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
									agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = links.agent1.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
									agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = \
										links.agent1.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] + (random.random()/2) - 0.25
									# 1-1 check
									agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = \
										ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0])
									agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = \
										ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1])
									agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = \
										ActionFunctions.one_minus_one_check(agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC])

									# Knowledge gained by the secondary link agent:
									links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
									links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
									links.agent1.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = \
										agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] + (random.random()/2) - 0.25
									# 1-1 check
									links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = \
										ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0])
									links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = \
										ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1])
									links.agent1.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = \
										ActionFunctions.one_minus_one_check(links.agent1.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC])

									# Adjusting resources
									agents.resources[1] -= 0.02 * agents.resources[0]
									links.agent1.resources[1] -= 0.01 * links.agent1.resources[0]

						# If the list has more than 2 agents, then we can check to create a team
						if len(team_list_potential_agent) > 1:
							team_list_actual_agent = []
							# Make a new list containing the agent that actually match the requirements
							for potential_agent in team_list_potential_agent:
								if agents.belieftree[0][agents.select_problem_3S_as][0] != 'No':
									if abs(agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] - \
										potential_agent.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC]) < team_belief_policy_threshold and \
										abs(potential_agent.belieftree[0][agents.select_problem_3S_as][0] - potential_agent.belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold:
								  		team_list_actual_agent.append(potential_agent)
								else:
									print('1. ALERT - THIS IS AN INTRUDER - A AGENT THAT SHOULDNT BE IN THIS TEAM IS IN THIS TEAM')

							# Check that the list is still more than two agents and if so create the team:
							if len(team_list_potential_agent) > 1:

								# Now we can create the team						
								members = team_list_potential_agent
								members.append(agents)
								team_resources = [0, 0]
								members_id = []
								for members_for_id in members:
									members_id.append(members_for_id.unique_id)
								team = Team(team_number_as[0], agents, members, members_id, agents.select_issue_3S_as, agents.select_policy_3S_as, tick_number, team_resources)
								print('TEAM CREATION 2! ')
								# Iteration of the team ID number for the overall team list
								team_number_as[0] += 1
								team_list_as.append(team)
								team_list_as_total.append(team)
								
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(team, team.issue, 0)

								# Calculation of the average issue belief for belonging calculation (based on partial knowledge) per agent:
								for agent_members1 in team.members:
									# Setting the partial knowledge for himself equal to his own belief:
									agent_members1.belieftree[1+agent_members1.unique_id][team.issue][0] = agent_members1.belieftree[0][team.issue][0]
									# Calculating the average belief according to partial knowledge
									issue_avg_belief = []
									for agent_members2 in team.members:
										if agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0] != 'No':
											issue_avg_belief.append(agent_members2.resources[0]*agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0])
										else:
											print('2. ALERT - THIS IS AN INTRUDER - A AGENT THAT SHOULDNT BE IN THIS TEAM IS IN THIS TEAM')
									issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
									# Setting the belonging level
									agent_members1.team_as[1] = 1 - abs(agent_members1.belieftree[0][team.issue][0] - issue_avg_belief)
									# Setting of the team object
									agent_members1.team_as[0] = team
								# Setting the team resources
								for agent_members in team.members:
									team.resources[0] += agent_members.team_as[1]
									team.resources[1] = team.resources[0]

			# b. Method 1 - Only the first X agents are selected for the team
			if agents.team_as[2] == 1:
				# print(' ')
				# print(' ')
				# print('Strategy 1')

				# If the agent is advocating or a problem, the following tasks are performed
				if agents.select_issue_3S_as == 'problem':

					# Check if the agent indeed has a gap:
					if abs(agents.belieftree[0][agents.select_problem_3S_as][0] - agents.belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold:

						team_list_potential_agent = []
						
						# Go through all possible links for this agent:
						while True:
							shuffled_list_links = link_list
							random.shuffle(shuffled_list_links)
							for links in shuffled_list_links:

								# Make sure that there is aware
								if links.aware > 0:
									
									# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
									if links.agent1 == agents and links.agent2.team_as[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] == None:
											agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = 0
										if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] == None:
											agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = 0
										if agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] == None:
											agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = 0

										# Check for the gap and the similarity in states based on partial knowledge - if okay, add the agent to the list
										if abs(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] - agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
											abs(agents.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] - \
										  	agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0]) < team_belief_problem_threshold:
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent2)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = links.agent2.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = \
											links.agent2.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0])
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1])
										agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0])

										# Knowledge gained by the secondary link agent:
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										links.agent2.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = \
											agents.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = \
											ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0])
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = \
											ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1])
										links.agent2.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = \
											ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent2.resources[1] -= 0.01 * links.agent2.resources[0]

									# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
									if links.agent2 == agents and links.agent1.team_as[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = 0
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = 0
										if agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] == None:
											agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = 0

										# Check for the gap and the similarity in states based on partial knowledge 
										if abs(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] - agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
											abs(agents.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] - \
										  	agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0]) < team_belief_problem_threshold:
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent1)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = links.agent1.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = links.agent1.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = \
											links.agent1.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0])
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1])
										agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0])

										# Knowledge gained by the secondary link agent:
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = \
											agents.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0])
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1])
										links.agent1.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent1.resources[1] -= 0.01 * links.agent1.resources[0]

									# Stop the while loop when there are enough agents to be in the team
									if len(team_list_potential_agent) > 1:
										break
							break

						# If there are enough agents, we create a team with them
						if len(team_list_potential_agent) == 2:

							# We check that the actual beliefs are within 0.2
							if abs(agents.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] - \
								team_list_potential_agent[0].belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0]) < team_belief_problem_threshold and \
								abs(agents.belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0] - \
							  	team_list_potential_agent[1].belieftree[0][len_PC + len_ML + len_S + prefered_Pr*len_ML + (agents.select_problem_3S_as - len_PC)][0]) < team_belief_problem_threshold and \
								abs(team_list_potential_agent[0].belieftree[0][agents.select_problem_3S_as][0] - team_list_potential_agent[0].belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
								abs(team_list_potential_agent[1].belieftree[0][agents.select_problem_3S_as][0] - team_list_potential_agent[1].belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold:
								# Now we can create the team						
								members = team_list_potential_agent
								members.append(agents)
								team_resources = [0, 0]
								members_id = []
								for members_for_id in members:
									members_id.append(members_for_id.unique_id)
								team = Team(team_number_as[0], agents, members, members_id, agents.select_issue_3S_as, agents.select_problem_3S_as, tick_number, team_resources)
								print('TEAM CREATION 3!')
								# Iteration of the team ID number for the overall team list
								team_number_as[0] += 1
								team_list_as.append(team)
								team_list_as_total.append(team)
								
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(team, team.issue, 0)

								# Calculation of the average issue belief (based on partial knowledge) per agent:
								for agent_members1 in team.members:
									# Setting the partial knowledge for himself equal to his own belief:
									agent_members1.belieftree[1+agent_members1.unique_id][team.issue][0] = agent_members1.belieftree[0][team.issue][0]
									# Calculating the average belief according to partial knowledge
									issue_avg_belief = []
									for agent_members2 in team.members:
										issue_avg_belief.append(agent_members2.resources[0]*agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0])
									issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
									# Setting the belonging level
									agent_members1.team_as[1] = 1 - abs(agent_members1.belieftree[0][team.issue][0] - issue_avg_belief)
									# Setting of the team object
									agent_members1.team_as[0] = team
								# Setting the team resources
								for agent_members in team.members:
									team.resources[0] += agent_members.team_as[1]
									team.resources[1] = team.resources[0]

				# If the agent is advocating or a policy, the following tasks are performed
				if agents.select_issue_3S_as == 'policy':

					# Check if the agent indeed has a gap:
					if abs(agents.belieftree[0][agents.select_problem_3S_as][0] - agents.belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold:

						team_list_potential_agent = []
						
						# Go through all possible links for this agent:
						while True:
							shuffled_list_links = link_list
							random.shuffle(shuffled_list_links)
							for links in shuffled_list_links:

								# Make sure that there is aware
								if links.aware > 0:
									
									# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
									if links.agent1 == agents and links.agent2.team_as[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] == None:
											agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = 0
										if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] == None:
											agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = 0
										if agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] == None:
											agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = 0

										# Check for the gap and the similarity in states based on partial knowledge - if okay, add the agent to the list
										if abs(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] - agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
											abs(agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] - \
										  	agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC]) < team_belief_policy_threshold:
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent2)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = links.agent2.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = links.agent2.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = \
											links.agent2.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][0])
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_as][1])
										agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = \
											ActionFunctions.one_minus_one_check(agents.belieftree_policy[1+links.agent2.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC])

										# Knowledge gained by the secondary link agent:
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										links.agent2.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = \
											agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = \
											ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0])
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = \
											ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1])
										links.agent2.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = \
											ActionFunctions.one_minus_one_check(links.agent2.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent2.resources[1] -= 0.01 * links.agent2.resources[0]

									# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
									if links.agent2 == agents and links.agent1.team_as[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = 0
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = 0
										if agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] == None:
											agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = 0

										# Check for the gap and the similarity in states based on partial knowledge 
										if abs(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] - agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
											abs(agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] - \
										  	agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC]) < team_belief_policy_threshold:
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent1)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = links.agent1.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = links.agent1.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = \
											links.agent1.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][0])
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_as][1])
										agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = \
											ActionFunctions.one_minus_one_check(agents.belieftree_policy[1+links.agent1.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC])

										# Knowledge gained by the secondary link agent:
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = agents.belieftree[0][agents.select_problem_3S_as][0] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = agents.belieftree[0][agents.select_problem_3S_as][1] + (random.random()/2) - 0.25
										links.agent1.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = \
											agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][0])
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_as][1])
										links.agent1.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree_policy[1+agents.unique_id][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent1.resources[1] -= 0.01 * links.agent1.resources[0]

									# Stop the while loop when there are enough agents to be in the team
									if len(team_list_potential_agent) > 1:
										break
							break

						# If there are enough agents, we create a team with them
						if len(team_list_potential_agent) == 2:

							# We check that the actual beliefs are within 0.2
							if abs(agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] - \
								team_list_potential_agent[0].belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC]) < team_belief_policy_threshold and \
								abs(agents.belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC] - \
							  	team_list_potential_agent[1].belieftree_policy[0][agents.select_policy_3S_as][agents.select_problem_3S_as - len_PC]) < team_belief_policy_threshold and \
								abs(team_list_potential_agent[0].belieftree[0][agents.select_problem_3S_as][0] - team_list_potential_agent[0].belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold and \
								abs(team_list_potential_agent[1].belieftree[0][agents.select_problem_3S_as][0] - team_list_potential_agent[1].belieftree[0][agents.select_problem_3S_as][1]) >= team_gap_threshold:
								# Now we can create the team						
								members = team_list_potential_agent
								members.append(agents)
								team_resources = [0, 0]
								members_id = []
								for members_for_id in members:
									members_id.append(members_for_id.unique_id)
								team = Team(team_number_as[0], agents, members, members_id, agents.select_issue_3S_as, agents.select_policy_3S_as, tick_number, team_resources)
								print('TEAM CREATION 4!')
								# Iteration of the team ID number for the overall team list
								team_number_as[0] += 1
								team_list_as.append(team)
								team_list_as_total.append(team)
								
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(team, team.issue, 0)

								# Calculation of the average issue belief (based on partial knowledge) per agent:
								for agent_members1 in team.members:
									# Setting the partial knowledge for himself equal to his own belief:
									agent_members1.belieftree[1+agent_members1.unique_id][team.issue][0] = agent_members1.belieftree[0][team.issue][0]
									# Calculating the average belief according to partial knowledge
									issue_avg_belief = []
									for agent_members2 in team.members:
										issue_avg_belief.append(agent_members2.resources[0]*agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0])
									issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
									# Setting the belonging level
									agent_members1.team_as[1] = 1 - abs(agent_members1.belieftree[0][team.issue][0] - issue_avg_belief)
									# Setting of the team object
									agent_members1.team_as[0] = team
								# Setting the team resources
								for agent_members in team.members:
									team.resources[0] += agent_members.team_as[1]
									team.resources[1] = team.resources[0]

	def agent_team_threeS_pf(self, agents, agent_action_list, team_list_pf, team_list_pf_total, link_list, team_number_pf, tick_number, threeS_link_list_pf, policy_core, \
		mid_level, secondary, agenda_prob_3S_as, team_gap_threshold, team_belief_problem_threshold, team_belief_policy_threshold):

		"""
		Agent-team actions - Three streams (policy formulation)
		===========================

		Note: This is the same function as the one for the agenda setting function
		but with modification for the policy formulation part. This means changes in
		the agents' selected issues.

		This function is used to perform all the agent-team actions during the
		policy formulation. The actions are given in order as follows:
			a. Belonging level update
			b. Leave team check
			c. Disband team check
			d. Join team
			e. Start team

		The team considered within this step are teams that are only present in
		the policy formulation. The agents also only consider the issues they have
		selected for the policy formulation.
		
		"""

		len_PC = len(policy_core)
		len_ML = len(mid_level)
		len_S = len(secondary)

		# print(' ')
		# print('Test')
		# print('This would be the CR of interest')
		# # For the PF
		# print(len_PC + len_ML + len_S + len_PC*len_ML + agenda_prob_3S_as*len_ML + (agents.team_as[0].issue - len_PC - len_ML))

		# a. Belonging level update (completed)
		if agents.team_pf[0] != None:
			self.knowledge_exchange_team(agents.team_pf[0], agents.team_pf[0].issue, 0)
			self.belonging_level_pf(agents, len_PC, len_ML)

		# b. Leave team check (completed)
		if agents.team_pf[0] != None:
			# If the belonging level is below 30%, we remove the agent from the team
			if agents.team_pf[1] < 0.3:
				# If the agent is the lead agent, then the team is disbanded
				team = agents.team_pf[0]
				if agents == agents.team_pf[0].lead:
					# Disband function
					# print('Disband 1 triggered!')
					self.disband_team_pf(agents, team, threeS_link_list_pf, team_list_pf)

				# Else only this agent is removed
				else:
					self.remove_agent_team_pf(agents)
					# If the length of the team becomes too small, then the team has to be disbanded:
					if len(team.members) < 3:
						# Disband function
						# print('Disband 2 triggered!')
						self.disband_team_pf(agents, team, threeS_link_list_pf, team_list_pf)

		# c. Disband team check (completed)
		if agents.team_pf[0] != None:

			# Several cases for which a team can be disbanded:
			# 1. Lead agent changes selected policy
			# This is checked every five ticks
			if (tick_number - agents.team_pf[0].creation) % 5 == 0 and tick_number >= 5:
				# 1. Lead agent has different issue than the team issue (checked every five ticks)
				# Check that the agent is the lead of this team
				if agents == agents.team_pf[0].lead:
					# Check that the agent has different issue type (problem/policy) or different issue number
					if agents.select_problem_3S_pf != agents.team_pf[0].issue or agents.select_issue_3S_pf != agents.team_pf[0].issue_type:
						team = agents.team_pf[0]
						# Disband function
						# print('Disband 3 triggered!')
						self.disband_team_pf(agents, team, threeS_link_list_pf, team_list_pf)

				# 2. Checking if each agent meets the requirements and remove if not
				# Check that the agent has same issue type (problem/policy) and same issue number
				elif agents.select_problem_3S_pf == agents.team_pf[0].issue and agents.select_issue_3S_pf == agents.team_pf[0].issue_type:

					# If the team is advocating for a problem, perform the following actions:
					if agents.team_pf[0].issue_type == 'problem':
						team = agents.team_pf[0]
						agent_removed = 0

						for agent_members in team.members:
							# Opposite of the requirements for the creation of a team
							if abs(team.lead.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (team.issue - len_PC - len_ML)][0] - \
								agent_members.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (team.issue - len_PC - len_ML)][0]) >= team_belief_problem_threshold or \
								abs(agent_members.belieftree[0][agents.select_problem_3S_pf][0] - agent_members.belieftree[0][agents.select_problem_3S_pf][1]) < team_gap_threshold:
								# Disband the team if the leader doesnt meet the requirements anymore
								if agent_members == team.lead:
									self.disband_team_pf(agents, team, threeS_link_list_pf, team_list_pf)
									break
								else:
									self.remove_agent_team_pf(agent_members)
									agent_removed = 1
									if agents == agent_members:
										print('I AM THE AGENT, BREAK AFTER ME')
										break

					# If the team is advocating for a policy, perform the following actions:
					elif agents.team_pf[0].issue_type == 'policy':
						team = agents.team_pf[0]
						agent_removed = 0
						for agent_members in team.members:
							# Opposite of the requirements for the creation of a team
							if abs(team.lead.belieftree_instrument[0][agents.team_pf[0].issue][team.lead.select_problem_3S_pf - len_PC - len_ML] - \
								agent_members.belieftree_instrument[0][agents.team_pf[0].issue][team.lead.select_problem_3S_pf - len_PC - len_ML]) >= team_belief_policy_threshold or \
								abs(agent_members.belieftree[0][team.lead.select_problem_3S_pf][0] - agent_members.belieftree[0][team.lead.select_problem_3S_pf][1]) < team_gap_threshold:
								# Disband the team if the leader doesnt meet the requirements anymore
								if agent_members == team.lead:
									self.disband_team_pf(agents, team, threeS_link_list_pf, team_list_pf)
									break
								else:
									self.remove_agent_team_pf(agent_members)
									agent_removed = 1
									if agents == agent_members:
										print('I AM THE AGENT, BREAK AFTER ME')
										break


					# Recalculate the belonging level of the agents left
					if agents.team_pf[0] != None:
						if agent_removed == 1:
							for agent_members in team.members:
								self.belonging_level_pf(agent_members, len_PC, len_ML)

								# If the belonging level is below 30%, the agents are removed (similar to a previous loop)
								if agent_members.team_pf[1] < 0.3:
									# team = agents.team_pf[0]
									if agent_members == agent_members.team_pf[0].lead:
										# print('Disband 4 triggered!')
										self.disband_team_pf(agent_members, team, threeS_link_list_pf, team_list_pf)
									else:
										self.remove_agent_team_pf(agent_members)
										if len(team.members) < 3:
											# print('Disband 5 triggered!')
											self.disband_team_pf(agent_members, team, threeS_link_list_pf, team_list_pf)

					# Check the length of the team after all agents have been checked - disband if too small
					if agents.team_pf[0] != None:
						if len(agents.team_pf[0].members) < 3:
							# print('Disband 6 triggered!')
							self.disband_team_pf(agents, team, threeS_link_list_pf, team_list_pf)

		# d. Join a team (completed)
		if agents.team_pf[0] == None:

			while True:

				added_team_check = 0

				for join_team in team_list_pf:

					# If the team is advocating for a problem, the following tasks are completed
					if join_team.issue_type == 'problem':

						# Check that the team is still active and has members:
						if len(join_team.members) > 0:

							# None check
							check_none = 0
							if agents.belieftree[1+join_team.lead.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (join_team.issue - len_PC - len_ML)][0] == None:
								agents.belieftree[1+join_team.lead.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (join_team.issue - len_PC - len_ML)][0] = 0
								check_none = 1

							# First we check that the agent meets both requirements (based on partial knowledge) (we assume that the agent knows who the leader is)
							if abs(agents.belieftree[0][join_team.issue][0] - agents.belieftree[0][join_team.issue][1]) >= team_gap_threshold and \
								abs(agents.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (join_team.issue - len_PC - len_ML)][0] - \
									agents.belieftree[1+join_team.lead.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (join_team.issue - len_PC - len_ML)][0]) < team_belief_problem_threshold:

								# Add the agent to the team
								join_team.members.append(agents)
								join_team.members_id.append(agents.unique_id)
								agents.team_pf[0] = join_team
								# Share knowledge within the team
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(join_team, join_team.issue, 0)

								# Change belonging level
								self.belonging_level_pf(agents, len_PC, len_ML)

								# Notify that the loop can be stopped as the agent has been added
								added_team_check = 1

								# None reset
								if check_none == 1:
									agents.belieftree[1+join_team.lead.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (join_team.issue - len_PC - len_ML)][0] = None

							# update of the resources
							agents.resources[1] -= 0.02 * agents.resources[0]

							# Resources sufficiency check
							if agents.resources[1] < 0.5 * agents.resources[0]:
								break

							# If the agent has been added to a team, stop this entire procedure
							if added_team_check == 1:
								break

					# If the team is advocating for a policy, the following tasks are completed
					if join_team.issue_type == 'policy':

						# Check that the team is still active and has members:
						if len(join_team.members) > 0:

							# None check
							check_none = 0
							if agents.belieftree_instrument[1+join_team.lead.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] == None:
								agents.belieftree_instrument[1+join_team.lead.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = 0
								check_none = 1

							# First we check that the agent meets both requirements (based on partial knowledge) (we assume that the agent knows who the leader is)
							if abs(agents.belieftree[0][join_team.lead.select_problem_3S_pf][0] - agents.belieftree[0][join_team.lead.select_problem_3S_pf][1]) >= team_gap_threshold and \
								abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] - \
									agents.belieftree_instrument[1+join_team.lead.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML]) < team_belief_policy_threshold:

								# Add the agent to the team
								join_team.members.append(agents)
								join_team.members_id.append(agents.unique_id)
								agents.team_pf[0] = join_team
								# Share knowledge within the team
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(join_team, join_team.issue, 0)

								# Change belonging level
								self.belonging_level_pf(agents, len_PC, len_ML)

								# Notify that the loop can be stopped as the agent has been added
								added_team_check = 1

							# None reset
							if check_none == 1:
								agents.belieftree_instrument[1+join_team.lead.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = None

							# update of the resources
							agents.resources[1] -= 0.02 * agents.resources[0]

							# Resources sufficiency check
							if agents.resources[1] < 0.5 * agents.resources[0]:
								break

							# If the agent has been added to a team, stop this entire procedure
							if added_team_check == 1:
								break
				break

		# e. Start a team (completed)
		if agents.team_pf[0] == None:
			# First team creation method:
			# Avoided for now - requires memory

			# Second team creation method:
			# a. Method 0 - All agents that qualify are selected
			if agents.team_pf[2] == 0:
				# print(' ')
				# print(' ')
				# print('Strategy 0')

				# If the agent is advocating or a problem, the following tasks are performed
				if agents.select_issue_3S_pf == 'problem':

					# Check if the agent indeed has a gap:
					if abs(agents.belieftree[0][agents.select_problem_3S_pf][0] - agents.belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold:

						team_list_potential_agent = []

						shuffled_list_links = link_list
						random.shuffle(shuffled_list_links)
						for links in shuffled_list_links:
							# Make sure that there is aware
							if links.aware > 0:
								# print(links)
								
								# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not None
								if links.agent1 == agents and links.agent2.team_pf[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] != 'No':

									# Check if no partial knowledge (initial value)
									if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] == None:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = 0
									if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] == None:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = 0
									if agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] == None:
										agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = 0

									# Check for the gap and the similarity in states based on partial knowledge - if okay, add the agent to the list
									if abs(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] - agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
										abs(agents.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] - \
									  	agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0]) < team_belief_problem_threshold:
										# Add the agent to the list of potential candidates
										team_list_potential_agent.append(links.agent2)

									# Actual knowledge exchange with a randomness of 0.5
									# Knowledge gained by the lead agent:
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = links.agent2.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
									agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = \
										links.agent2.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] + (random.random()/2) - 0.25
									# 1-1 check
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = \
										ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0])
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = \
										ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1])
									agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = \
										ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0])

									# Knowledge gained by the secondary link agent:
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
									links.agent2.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = \
										agents.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] + (random.random()/2) - 0.25
									# 1-1 check
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = \
										ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0])
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = \
										ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1])
									links.agent2.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = \
										ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0])

									# Adjusting resources
									agents.resources[1] -= 0.02 * agents.resources[0]
									links.agent2.resources[1] -= 0.01 * links.agent2.resources[0]

								# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
								if links.agent2 == agents and links.agent1.team_pf[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = 0
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = 0
										if agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] == None:
											agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = 0

										# Check for the gap and the similarity in states based on partial knowledge
										if abs(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] - agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
											abs(agents.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] - \
										  	agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0]) < team_belief_problem_threshold:
											
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent1)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = links.agent1.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = links.agent1.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = \
											links.agent1.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0])
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1])
										agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0])

										# Knowledge gained by the secondary link agent:
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = \
											agents.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0])
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1])
										links.agent1.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent1.resources[1] -= 0.01 * links.agent1.resources[0]

						# If the list has more than 2 agents, then we can check to create a team
						if len(team_list_potential_agent) > 1:
							team_list_actual_agent = []
							# Make a new list containing the agent that actually match the requirements
							for potential_agent in team_list_potential_agent:
								if agents.belieftree[0][agents.select_problem_3S_pf][0] != 'No':
									if abs(agents.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] - \
										potential_agent.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0]) < team_belief_problem_threshold and \
								  		abs(potential_agent.belieftree[0][agents.select_problem_3S_pf][0] - potential_agent.belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold:
								  		team_list_actual_agent.append(potential_agent)
								else:
									print('1. ALERT - THIS IS AN INTRUDER - A AGENT THAT SHOULDNT BE IN THIS TEAM IS IN THIS TEAM')

							# Check that the list is still more than two agents and if so create the team:
							if len(team_list_potential_agent) > 1:

								# Now we can create the team						
								members = team_list_potential_agent
								members.append(agents)
								team_resources = [0, 0]
								members_id = []
								for members_for_id in members:
									members_id.append(members_for_id.unique_id)
								team = Team(team_number_pf[0], agents, members, members_id, agents.select_issue_3S_pf, agents.select_problem_3S_pf, tick_number, team_resources)
								print('TEAM CREATION 5! ')
								# Iteration of the team ID number for the overall team list
								team_number_pf[0] += 1
								team_list_pf.append(team)
								team_list_pf_total.append(team)
								
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(team, team.issue, 0)

								# Calculation of the average issue belief for belonging calculation (based on partial knowledge) per agent:
								for agent_members1 in team.members:
									# Setting the partial knowledge for himself equal to his own belief:
									agent_members1.belieftree[1+agent_members1.unique_id][team.issue][0] = agent_members1.belieftree[0][team.issue][0]
									# Calculating the average belief according to partial knowledge
									issue_avg_belief = []
									for agent_members2 in team.members:
										if agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0] != 'No':
											issue_avg_belief.append(agent_members2.resources[0]*agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0])
										else:
											print('2. ALERT - THIS IS AN INTRUDER - A AGENT THAT SHOULDNT BE IN THIS TEAM IS IN THIS TEAM')
									issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
									# Setting the belonging level
									agent_members1.team_pf[1] = 1 - abs(agent_members1.belieftree[0][team.issue][0] - issue_avg_belief)
									# Setting of the team object
									agent_members1.team_pf[0] = team
								# Setting the team resources
								for agent_members in team.members:
									team.resources[0] += agent_members.team_pf[1]
									team.resources[1] = team.resources[0]

				# If the agent is advocating or a policy, the following tasks are performed
				if agents.select_issue_3S_pf == 'policy':

					# Check if the agent indeed has a gap:
					if abs(agents.belieftree[0][agents.select_problem_3S_pf][0] - agents.belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold:

						team_list_potential_agent = []

						shuffled_list_links = link_list
						random.shuffle(shuffled_list_links)
						for links in shuffled_list_links:
							# Make sure that there is aware
							if links.aware > 0:
								# print(links)
								
								# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not None
								if links.agent1 == agents and links.agent2.team_pf[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] != 'No':

									# Check if no partial knowledge (initial value)
									if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] == None:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = 0
									if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] == None:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = 0
									if agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] == None:
										agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = 0

									# Check for the gap and the similarity in states based on partial knowledge - if okay, add the agent to the list
									if abs(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] - agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
										abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] - \
									  	agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML]) < team_belief_policy_threshold:
										# Add the agent to the list of potential candidates
										team_list_potential_agent.append(links.agent2)

									# Actual knowledge exchange with a randomness of 0.5
									# Knowledge gained by the lead agent:
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = links.agent2.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
									agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = \
										links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] + (random.random()/2) - 0.25
									# 1-1 check
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = \
										ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0])
									agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = \
										ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1])
									agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = \
										ActionFunctions.one_minus_one_check(agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML])

									# Knowledge gained by the secondary link agent:
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
									links.agent2.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = \
										agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] + (random.random()/2) - 0.25
									# 1-1 check
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = \
										ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0])
									links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = \
										ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1])
									links.agent2.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = \
										ActionFunctions.one_minus_one_check(links.agent2.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML])

									# Adjusting resources
									agents.resources[1] -= 0.02 * agents.resources[0]
									links.agent2.resources[1] -= 0.01 * links.agent2.resources[0]

								# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
								if links.agent2 == agents and links.agent1.team_pf[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = 0
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = 0
										if agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] == None:
											agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = 0

										# Check for the gap and the similarity in states based on partial knowledge
										if abs(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] - agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
											abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] - \
										  	agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML]) < team_belief_policy_threshold:
											
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent1)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = links.agent1.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = links.agent1.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = \
											links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0])
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1])
										agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = \
											ActionFunctions.one_minus_one_check(agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML])

										# Knowledge gained by the secondary link agent:
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										links.agent1.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = \
											agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0])
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1])
										links.agent1.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent1.resources[1] -= 0.01 * links.agent1.resources[0]

						# If the list has more than 2 agents, then we can check to create a team
						if len(team_list_potential_agent) > 1:
							team_list_actual_agent = []
							# Make a new list containing the agent that actually match the requirements
							for potential_agent in team_list_potential_agent:
								if agents.belieftree[0][agents.select_problem_3S_pf][0] != 'No':
									if abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] - \
										potential_agent.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML]) < team_belief_policy_threshold and \
								  		abs(potential_agent.belieftree[0][agents.select_problem_3S_pf][0] - potential_agent.belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold:
								  		team_list_actual_agent.append(potential_agent)
								else:
									print('1. ALERT - THIS IS AN INTRUDER - A AGENT THAT SHOULDNT BE IN THIS TEAM IS IN THIS TEAM')

							# Check that the list is still more than two agents and if so create the team:
							if len(team_list_potential_agent) > 1:

								# Now we can create the team						
								members = team_list_potential_agent
								members.append(agents)
								team_resources = [0, 0]
								members_id = []
								for members_for_id in members:
									members_id.append(members_for_id.unique_id)
								team = Team(team_number_pf[0], agents, members, members_id, agents.select_issue_3S_pf, agents.select_policy_3S_pf, tick_number, team_resources)
								print('TEAM CREATION 6! ')
								# Iteration of the team ID number for the overall team list
								team_number_pf[0] += 1
								team_list_pf.append(team)
								team_list_pf_total.append(team)
								
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(team, team.issue, 0)

								# Calculation of the average issue belief for belonging calculation (based on partial knowledge) per agent:
								for agent_members1 in team.members:
									# Setting the partial knowledge for himself equal to his own belief:
									agent_members1.belieftree[1+agent_members1.unique_id][team.issue][0] = agent_members1.belieftree[0][team.issue][0]
									# Calculating the average belief according to partial knowledge
									issue_avg_belief = []
									for agent_members2 in team.members:
										if agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0] != 'No':
											issue_avg_belief.append(agent_members2.resources[0]*agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0])
										else:
											print('2. ALERT - THIS IS AN INTRUDER - A AGENT THAT SHOULDNT BE IN THIS TEAM IS IN THIS TEAM')
									issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
									# Setting the belonging level
									agent_members1.team_pf[1] = 1 - abs(agent_members1.belieftree[0][team.issue][0] - issue_avg_belief)
									# Setting of the team object
									agent_members1.team_pf[0] = team
								# Setting the team resources
								for agent_members in team.members:
									team.resources[0] += agent_members.team_pf[1]
									team.resources[1] = team.resources[0]


			# b. Method 1 - Only the first X agents are selected for the team
			if agents.team_pf[2] == 1:
				# print(' ')
				# print(' ')
				# print('Strategy 1')

				# If the agent is advocating or a problem, the following tasks are performed
				if agents.select_issue_3S_pf == 'problem':

					# Check if the agent indeed has a gap:
					if abs(agents.belieftree[0][agents.select_problem_3S_pf][0] - agents.belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold:

						team_list_potential_agent = []
						
						# Go through all possible links for this agent:
						while True:
							shuffled_list_links = link_list
							random.shuffle(shuffled_list_links)
							for links in shuffled_list_links:

								# Make sure that there is aware
								if links.aware > 0:
									
									# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
									if links.agent1 == agents and links.agent2.team_pf[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] == None:
											agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = 0
										if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] == None:
											agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = 0
										if agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] == None:
											agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = 0

										# Check for the gap and the similarity in states based on partial knowledge - if okay, add the agent to the list
										if abs(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] - agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
											abs(agents.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] - \
											agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0]) < team_belief_problem_threshold:
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent2)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = links.agent2.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = \
											links.agent2.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0])
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1])
										agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0])

										# Knowledge gained by the secondary link agent:
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										links.agent2.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = \
											agents.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = \
											ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0])
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = \
											ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1])
										links.agent2.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = \
											ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent2.resources[1] -= 0.01 * links.agent2.resources[0]

									# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
									if links.agent2 == agents and links.agent1.team_pf[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = 0
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = 0
										if agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + ((agenda_prob_3S_as-len_PC)-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] == None:
											agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = 0

										# Check for the gap and the similarity in states based on partial knowledge 
										if abs(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] - agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
											abs(agents.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] - \
											agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0]) < team_belief_problem_threshold:
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent1)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = links.agent1.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = links.agent1.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = \
											links.agent1.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0])
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1])
										agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0])

										# Knowledge gained by the secondary link agent:
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = \
											agents.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0])
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1])
										links.agent1.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent1.resources[1] -= 0.01 * links.agent1.resources[0]

									# Stop the while loop when there are enough agents to be in the team
									if len(team_list_potential_agent) > 1:
										break
							break

						# If there are enough agents, we create a team with them
						if len(team_list_potential_agent) == 2:

							# We check that the actual beliefs are within 0.2
							if abs(agents.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] - \
								team_list_potential_agent[0].belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0]) < team_belief_problem_threshold and \
								abs(agents.belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0] - \
								team_list_potential_agent[1].belieftree[0][len_PC + len_ML + len_S + len_PC*len_ML + (agenda_prob_3S_as-len_PC)*len_ML + (agents.select_problem_3S_pf - len_PC - len_ML)][0]) < team_belief_problem_threshold and \
								abs(team_list_potential_agent[0].belieftree[0][agents.select_problem_3S_pf][0] - team_list_potential_agent[0].belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
								abs(team_list_potential_agent[1].belieftree[0][agents.select_problem_3S_pf][0] - team_list_potential_agent[1].belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold:
								# Now we can create the team						
								members = team_list_potential_agent
								members.append(agents)
								team_resources = [0, 0]
								members_id = []
								for members_for_id in members:
									members_id.append(members_for_id.unique_id)
								team = Team(team_number_pf[0], agents, members, members_id, agents.select_issue_3S_pf, agents.select_problem_3S_pf, tick_number, team_resources)
								print('TEAM CREATION 7! ')
								# Iteration of the team ID number for the overall team list
								team_number_pf[0] += 1
								team_list_pf.append(team)
								team_list_pf_total.append(team)
								
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(team, team.issue, 0)

								# Calculation of the average issue belief (based on partial knowledge) per agent:
								for agent_members1 in team.members:
									# Setting the partial knowledge for himself equal to his own belief:
									agent_members1.belieftree[1+agent_members1.unique_id][team.issue][0] = agent_members1.belieftree[0][team.issue][0]
									# Calculating the average belief according to partial knowledge
									issue_avg_belief = []
									for agent_members2 in team.members:
										issue_avg_belief.append(agent_members2.resources[0]*agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0])
									issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
									# Setting the belonging level
									agent_members1.team_pf[1] = 1 - abs(agent_members1.belieftree[0][team.issue][0] - issue_avg_belief)
									# Setting of the team object
									agent_members1.team_pf[0] = team

								# Setting the team resources
								for agent_members in team.members:
									team.resources[0] += agent_members.team_pf[1]
									team.resources[1] = team.resources[0]

				# If the agent is advocating or a policy, the following tasks are performed
				if agents.select_issue_3S_pf == 'policy':

					# Check if the agent indeed has a gap:
					if abs(agents.belieftree[0][agents.select_problem_3S_pf][0] - agents.belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold:

						team_list_potential_agent = []
						
						# Go through all possible links for this agent:
						while True:
							shuffled_list_links = link_list
							random.shuffle(shuffled_list_links)
							for links in shuffled_list_links:

								# Make sure that there is aware
								if links.aware > 0:
									
									# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
									if links.agent1 == agents and links.agent2.team_pf[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] == None:
											agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = 0
										if agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] == None:
											agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = 0
										if agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] == None:
											agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = 0

										# Check for the gap and the similarity in states based on partial knowledge - if okay, add the agent to the list
										if abs(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] - agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
											abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] - \
											agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML]) < team_belief_policy_threshold:
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent2)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = links.agent2.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = links.agent2.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = \
											links.agent2.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][0])
										agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent2.unique_id][agents.select_problem_3S_pf][1])
										agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = \
											ActionFunctions.one_minus_one_check(agents.belieftree_instrument[1+links.agent2.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML])

										# Knowledge gained by the secondary link agent:
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										links.agent2.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = \
											agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = \
											ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0])
										links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = \
											ActionFunctions.one_minus_one_check(links.agent2.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1])
										links.agent2.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = \
											ActionFunctions.one_minus_one_check(links.agent2.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent2.resources[1] -= 0.01 * links.agent2.resources[0]

									# Make sure it is not in a team already and enough resources for the searching agent and that it is known that the other agent's state is not Non
									if links.agent2 == agents and links.agent1.team_pf[0] == None and agents.resources[1] > 0.02 * agents.resources[0] and agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] != 'No':
										
										# Check if no partial knowledge (initial value)
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = 0
										if agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] == None:
											agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = 0
										if agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] == None:
											agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = 0

										# Check for the gap and the similarity in states based on partial knowledge 
										if abs(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] - agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
											abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] - \
											agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML]) < team_belief_policy_threshold:
											# Add the agent to the list of potential candidates
											team_list_potential_agent.append(links.agent1)

										# Actual knowledge exchange with a randomness of 0.5
										# Knowledge gained by the lead agent:
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = links.agent1.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = links.agent1.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = \
											links.agent1.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] + (random.random()/2) - 0.25
										# 1-1 check
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][0])
										agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1] = \
											ActionFunctions.one_minus_one_check(agents.belieftree[1+links.agent1.unique_id][agents.select_problem_3S_pf][1])
										agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = \
											ActionFunctions.one_minus_one_check(agents.belieftree_instrument[1+links.agent1.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML])

										# Knowledge gained by the secondary link agent:
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = agents.belieftree[0][agents.select_problem_3S_pf][0] + (random.random()/2) - 0.25
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = agents.belieftree[0][agents.select_problem_3S_pf][1] + (random.random()/2) - 0.25
										links.agent1.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = \
											agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] + (random.random()/2) - 0.25
										# 1-1 check
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][0])
										links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree[1+agents.unique_id][agents.select_problem_3S_pf][1])
										links.agent1.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] = \
											ActionFunctions.one_minus_one_check(links.agent1.belieftree_instrument[1+agents.unique_id][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML])

										# Adjusting resources
										agents.resources[1] -= 0.02 * agents.resources[0]
										links.agent1.resources[1] -= 0.01 * links.agent1.resources[0]

									# Stop the while loop when there are enough agents to be in the team
									if len(team_list_potential_agent) > 1:
										break
							break

						# If there are enough agents, we create a team with them
						if len(team_list_potential_agent) == 2:

							# We check that the actual beliefs are within 0.2
							if abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] - \
								team_list_potential_agent[0].belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML]) < team_belief_policy_threshold and \
								abs(agents.belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML] - \
								team_list_potential_agent[1].belieftree_instrument[0][agents.select_policy_3S_pf][agents.select_problem_3S_pf - len_PC - len_ML]) < team_belief_policy_threshold and \
								abs(team_list_potential_agent[0].belieftree[0][agents.select_problem_3S_pf][0] - team_list_potential_agent[0].belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold and \
								abs(team_list_potential_agent[1].belieftree[0][agents.select_problem_3S_pf][0] - team_list_potential_agent[1].belieftree[0][agents.select_problem_3S_pf][1]) >= team_gap_threshold:
								# Now we can create the team						
								members = team_list_potential_agent
								members.append(agents)
								team_resources = [0, 0]
								members_id = []
								for members_for_id in members:
									members_id.append(members_for_id.unique_id)
								team = Team(team_number_pf[0], agents, members, members_id, agents.select_issue_3S_pf, agents.select_problem_3S_pf, tick_number, team_resources)
								print('TEAM CREATION 8! ')
								# Iteration of the team ID number for the overall team list
								team_number_pf[0] += 1
								team_list_pf.append(team)
								team_list_pf_total.append(team)
								
								# Exchange of partial knowledge between the agents in the team
								self.knowledge_exchange_team(team, team.issue, 0)

								# Calculation of the average issue belief (based on partial knowledge) per agent:
								for agent_members1 in team.members:
									# Setting the partial knowledge for himself equal to his own belief:
									agent_members1.belieftree[1+agent_members1.unique_id][team.issue][0] = agent_members1.belieftree[0][team.issue][0]
									# Calculating the average belief according to partial knowledge
									issue_avg_belief = []
									for agent_members2 in team.members:
										issue_avg_belief.append(agent_members2.resources[0]*agent_members1.belieftree[1+agent_members2.unique_id][team.issue][0])
									issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
									# Setting the belonging level
									agent_members1.team_pf[1] = 1 - abs(agent_members1.belieftree[0][team.issue][0] - issue_avg_belief)
									# Setting of the team object
									agent_members1.team_pf[0] = team
								# Setting the team resources
								for agent_members in team.members:
									team.resources[0] += agent_members.team_pf[1]
									team.resources[1] = team.resources[0]

	def disband_team_as(self, agents, team, threeS_link_list_as, team_list_as):

		"""
		Disband team function (agenda setting)
		===========================

		This is the disband team function. It removes agents from a team, 
		remove the team from the list of active teams in the agenda setting,
		and makes sure that the agents that were in the team have their
		attributes updated to say that they are not in a team anymore.
		
		"""

		# Deleting the associated shadow network
		to_be_deleted_links = []
		# print(' ')
		# Select the link in question
		for links in threeS_link_list_as:
			if links.agent1 == team:
				to_be_deleted_links.append(links)

		for link in to_be_deleted_links:
			threeS_link_list_as.remove(link)

		# Checking all agents in the team
		for removed_agent in team.members:
			# Remove agent object from the agent
			removed_agent.team_as[0] = None
			# Remove the belonging value of the agent
			removed_agent.team_as[1] = None
		# Removing the members from the team list and the leader of the team
		# For purposes of testing, the issue is kept along with the other attributes
		team.members = []
		team.lead = None
		# Remove the team from the list of active teams
		team_list_as.remove(team)

	def disband_team_pf(self, agents, team, threeS_link_list_pf, team_list_pf):

		"""
		Disband team function (policy formulation)
		===========================

		This is the disband team function. It removes agents from a team, 
		remove the team from the list of active teams in the policy formulation,
		and makes sure that the agents that were in the team have their
		attributes updated to say that they are not in a team anymore.
		
		"""

		# Deleting the associated shadow network
		to_be_deleted_links = []
		# print(' ')
		# Select the link in question
		for links in threeS_link_list_pf:
			if links.agent1 == team:
				to_be_deleted_links.append(links)

		for link in to_be_deleted_links:
			threeS_link_list_pf.remove(link)

		# Checking all agents in the team
		for removed_agent in team.members:
			# Remove agent object from the agent
			removed_agent.team_pf[0] = None
			# Remove the belonging value of the agent
			removed_agent.team_pf[1] = None
		# Removing the members from the team list and the leader of the team
		# For purposes of testing, the issue is kept along with the other attributes
		team.members = []
		team.lead = None
		# Remove the team from the list of active teams
		team_list_pf.remove(team)

	def remove_agent_team_as(self, agents_removal):

		"""
		Remove agent from team function (agenda setting)
		===========================

		This function removes agent from a specified team while updating its
		attributes to reflect that the agent is not part of the team anymore.
		This is the agenda setting version of the function
		
		"""

		agents_removal.team_as[0].members_id.remove(agents_removal.unique_id)
		agents_removal.team_as[0].members.remove(agents_removal)
		# Remove object and belonging values
		agents_removal.team_as[0] = None
		agents_removal.team_as[1] = None

	def remove_agent_team_pf(self, agents_removal):

		"""
		Remove agent from team function (policy formulation)
		===========================

		This function removes agent from a specified team while updating its
		attributes to reflect that the agent is not part of the team anymore.
		This is the policy formulation version of the function
		
		"""

		agents_removal.team_pf[0].members_id.remove(agents_removal.unique_id)
		agents_removal.team_pf[0].members.remove(agents_removal)

		# Remove object and belonging values
		agents_removal.team_pf[0] = None
		agents_removal.team_pf[1] = None

	def belonging_level_as(self, agents, len_PC, len_ML):

		"""
		Belonging level calculation function (agenda setting)
		===========================

		This function is used to update the belonging level of the agents within
		a team. For this first the average of the beliefs is calculated. Then each 
		agent's belonging level is calculated based on the difference between
		their beliefs and the average. This is the agenda setting version.

		Note: This function seems to be incorrectly used in so far as it is used
		for both policy and problem teams while it should only be used for problems
		teams.
		
		"""

		issue_avg_belief = []
		# Setting the partial knowledge for himself equal to his own belief:
		agents.belieftree[1+agents.unique_id][agents.team_as[0].issue][0] = agents.belieftree[0][agents.team_as[0].issue][0]
		# Calculation of the average issue belief for belonging calculation (based on partial knowledge) per agent:
		for agent_members in agents.team_as[0].members:
			issue_avg_belief.append(agent_members.resources[0]*agents.belieftree[1+agent_members.unique_id][agents.team_as[0].issue][0])
		# if len(issue_avg_belief) != 0:
		issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
		# else:
		# 	issue_avg_belief = 0
		agents.team_as[1] = 1 - abs(agents.belieftree[0][agents.team_as[0].issue][0] - issue_avg_belief)

	def belonging_level_pf(self, agents, len_PC, len_ML):

		"""
		Belonging level calculation function (policy formulation)
		===========================

		This function is used to update the belonging level of the agents within
		a team. For this first the average of the beliefs is calculated. Then each 
		agent's belonging level is calculated based on the difference between
		their beliefs and the average. This is the policy formulation version.

		Note: This function seems to be incorrectly used in so far as it is used
		for both policy and problem teams while it should only be used for problems
		teams.
		
		"""

		issue_avg_belief = []
		# Setting the partial knowledge for himself equal to his own belief:
		agents.belieftree[1+agents.unique_id][agents.team_pf[0].issue][0] = agents.belieftree[0][agents.team_pf[0].issue][0]
		# Calculation of the average issue belief for belonging calculation (based on partial knowledge) per agent:
		for agent_members in agents.team_pf[0].members:
			issue_avg_belief.append(agent_members.resources[0]*agents.belieftree[1+agent_members.unique_id][agents.team_pf[0].issue][0])
		issue_avg_belief = sum(issue_avg_belief)/len(issue_avg_belief)
		agents.team_pf[1] = 1 - abs(agents.belieftree[0][agents.team_pf[0].issue][0] - issue_avg_belief)

	def knowledge_exchange_team(self, team, issue, parameter):

		"""
		Knowledge exchange function - teams
		===========================

		This function is used for the exchange of partial knowledge between agents
		within the same team. This only regards the issue that is selected by the team
		and is kept with a certain amount of randomness.

		Note: This function seems to be incorrectly used in so far as it is used
		for both policy and problem teams while it should only be used for problems
		teams.
		
		"""

		# Exchange of partial knowledge between the agents in the team
		for agent_exchange1 in team.members:
			for agent_exchange2 in team.members:
				# Actual knowledge exchange with a randomness of 0.2
				# print('Before: ' + str(agent_exchange1.belieftree[1 + agent_exchange2.unique_id][team.issue][0]))
				if agent_exchange2.belieftree[0][issue][0] != 'No':
					agent_exchange1.belieftree[1 + agent_exchange2.unique_id][issue][parameter] = \
					  agent_exchange2.belieftree[0][issue][0] + (random.random()/5) - 0.1
					# 1-1 check
					agent_exchange1.belieftree[1 + agent_exchange2.unique_id][issue][parameter] = \
						ActionFunctions.one_minus_one_check(agent_exchange1.belieftree[1 + agent_exchange2.unique_id][issue][parameter])

	def pm_pe_actions_as(self, agents, link_list, policy_core, mid_level, secondary, resources_weight_action, resources_potency, affiliation_weights):

		"""
		The PEs and PMs actions function (agenda setting)
		===========================

		This function is used to perform the different active actions of the
		policy entrepreneurs and the policy makers during the agenda setting.

		The actions that can be performed are framing, influence on states and 
		influence on aims. All of the actions are first graded. Then the action
		that has the highest grade is selected. Finally, the action selected 
		is implemented.

		"""

		len_PC = len(policy_core)
		len_ML = len(mid_level)
		len_S = len(secondary)
		total_issue_number = len_PC + len_ML + len_S

		# Selection of the cw of interest
		cw_of_interest = []
		# We only consider the causal relations related to the problem on the agenda
		for cw_choice in range(len(policy_core)):
				cw_of_interest.append(len_PC + len_ML + len_S + (agents.select_as_issue - len_PC) + cw_choice * len(mid_level))

		# print(' ')
		# print('Causal relations of interest: ' + str(cw_of_interest))

		# Making sure there are enough resources
		while agents.resources_actions > 0.001:

			# Going through all the links in the model
			# print(agents)
			total_grade_list = []
			total_grade_list_links = []
			for links in link_list:

				# Making sure that the link is attached to the agent and has a aware higher than 0
				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
					total_grade_list_links.append(links)
					
					# 1. Grading all framing actions:
					# Checking through all possible framing - This is all based on partial knowledge!
					for cw in cw_of_interest:
						cw_grade = ActionFunctions.action_grade_calculator(links, cw, 0, agents, affiliation_weights)
						total_grade_list.append(cw_grade)	

					# 2. Grading all individual actions - Aim change
					aim_grade = ActionFunctions.action_grade_calculator(links, agents.select_as_issue, 1, agents, affiliation_weights)
					total_grade_list.append(aim_grade)

					# 3. Grading all individual actions - State change
					state_grade = ActionFunctions.action_grade_calculator(links, agents.select_as_issue, 0, agents, affiliation_weights)
					total_grade_list.append(state_grade)

			# print(' ')
			# print('Number of actions: ' + str(len(total_grade_list)))
			# print(total_grade_list)

			# 4. Choosing an action
			# Check if several actions have the same grade
			min_best_action = min(total_grade_list)
			count_min_list = []
			count = 0
			for item in total_grade_list:
				if item == min_best_action:
					count_min_list.append(count)
				count += 1
			# print('List of indexes: ' + str(count_min_list))
			# print(' ')

			# If there are several grades at the same level, then choose a random action from these grades:
			if len(count_min_list) > 1:
				best_action_index = random.choice(count_min_list)
				# print('Randomly chosen best action: ' + str(best_action_index))
			else:
				best_action_index = total_grade_list.index(min(total_grade_list))
				# print('Not randomly chosen: ' + str(best_action_index))
			
			# print(' ')
			# print('----- New check for best action ------')
			# print('Action value: ' + str(min(total_grade_list)))
			# print('Index of the best action: ' + str(best_action_index))
			# print('This is the grade of the action: ' + str(total_grade_list[best_action_index]))
			# Make sure that we do not take into account the 0 from the list to perform the following calculations
			# best_action_index += 1
			# print('The total amount of links considered: ' + str(len(total_grade_list_links)))
			# print('The number of actions per link considered: ' + str(len(cw_of_interest) + 2))
			# print('The total amount of actions considered: ' + str(len(total_grade_list)))
			# print('The link for the action is: ' + str(int(best_action_index/(len(cw_of_interest) + 2))))
			best_action = best_action_index - (len(cw_of_interest) + 2) * int(best_action_index/(len(cw_of_interest) + 2))
			# print('The impacted index is: ' + str(best_action))
			# print('The would be index without the +1: ' + str((best_action_index - (len(cw_of_interest) + 2) * int(best_action_index/(len(cw_of_interest) + 2))) - 1))
			# print('   ')

			# 5. Performing the actual action
			# Selecting the link:
			for links in link_list:

				if links == total_grade_list_links[int(best_action_index/(len(cw_of_interest) + 2))]:
					# print(links)

					# Update of the aware decay parameter
					links.aware_decay = 5

					# If the index is in the first part of the list, then the framing action is the best
					if best_action <= len(cw_of_interest) -1:					
						# print(' ')
						# print('Framing action - causal relation')
						# print('best_action: ' + str(best_action))
						# print('cw_of_interest: ' + str(cw_of_interest))
						# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

						implemented_action = ActionFunctions.action_implementor(links, cw_of_interest[best_action], 0, agents, agents, affiliation_weights, resources_weight_action, resources_potency, False, 1)

					# If the index is in the second part of the list, then the aim influence action is the best
					if best_action == len(cw_of_interest):
						# print('Implementing a aim influence action:')

						implemented_action = ActionFunctions.action_implementor(links, agents.select_as_issue, 1, agents, agents,affiliation_weights, resources_weight_action, resources_potency, False, 1)

					# If the index is in the first part of the list, then the state influence action is the best
					if best_action == len(cw_of_interest) + 1:
						# print('Implementing a state influence action:')
						
						implemented_action = ActionFunctions.action_implementor(links, agents.select_as_issue, 0, agents, agents,affiliation_weights, resources_weight_action, resources_potency, False, 1)

			# agents.resources_actions -= agents.resources
			agents.resources_actions -= agents.resources[0] * resources_weight_action

	def pm_pe_actions_pf(self, agents, link_list, policy_core, mid_level, secondary, causalrelation_number, agenda_as_issue, instruments, resources_weight_action, resources_potency, AS_theory, affiliation_weights):

		"""
		The PEs and PMs actions function (policy formulation)
		===========================

		This function is used to perform the different active actions of the
		policy entrepreneurs and the policy makers during the policy formulation.

		The actions that can be performed are framing, influence on states and 
		influence on aims. All of the actions are first graded. Then the action
		that has the highest grade is selected. Finally, the action selected 
		is implemented.

		"""

		len_PC = len(policy_core)
		len_ML = len(mid_level)
		len_S = len(secondary)
		total_issue_number = len_PC + len_ML + len_S

		# Here are the modifications related to the policy formulation
		# Looking for the relevant causal relations for the policy formulation
		of_interest = []
		cw_of_interest = []
		# We only consider the causal relations related to the problem on the agenda
		for cw_choice in range(len(secondary)):
			if agents.belieftree[0][len_PC + len_ML + len_S + (len_PC * len_ML) + (agenda_as_issue - len_PC)*len_S + cw_choice][0] \
				* instruments[agents.select_pinstrument][cw_choice] != 0:
				cw_of_interest.append(len_PC + len_ML + len_S + (len_PC * len_ML) + (agenda_as_issue - len_PC)*len_S + cw_choice)
		of_interest.append(cw_of_interest)

		# Looking for the relevant issues for the policy formulation
		issue_of_interest = []
		for issue_choice in range(len(secondary)):
			if instruments[agents.select_pinstrument][issue_choice] != 0:
				issue_of_interest.append(len_PC + len_ML + issue_choice)
		of_interest.append(issue_of_interest)

		# Making sure there are enough resources
		while agents.resources_actions > 0.001:
			# Going through all the links in the model
			# print(agents)
			total_grade_list = []
			total_grade_list_links = []
			for links in link_list:
				
				# Making sure that the link is attached to the agent and has a aware higher than 0
				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
					total_grade_list_links.append(links)

					# 1. Grading all framing actions:
					# Checking through all possible framing - This is all based on partial knowledge!
					for cw in cw_of_interest:

						# Checking which agent in the link is the original agent
						cw_grade = ActionFunctions.action_grade_calculator(links, cw, 0, agents, affiliation_weights)
						total_grade_list.append(cw_grade)

					# 2. Grading all individual actions - Aim change
					# Going though all possible choices of issue
					for issue_num in issue_of_interest:

						aim_grade = ActionFunctions.action_grade_calculator(links, issue_num, 1, agents, affiliation_weights)
						total_grade_list.append(aim_grade)

					# 3. Grading all individual actions - State change
					# Going though all possible choices of issue
					for issue_num in issue_of_interest:

						state_grade = ActionFunctions.action_grade_calculator(links, issue_num, 0, agents, affiliation_weights)
						total_grade_list.append(state_grade)

			# print(' ')
			# print(total_grade_list)

			# 4. Choosing an action
			best_action_index = total_grade_list.index(min(total_grade_list))

			# print(' ')
			# print('------ New action grade check -------')
			# print('Grade length: ' + str(len(total_grade_list)))
			# print('Best index: ' + str(best_action_index))
			# print('Number of links: ' + str(len(total_grade_list_links)))
			# print('Number of grades per link: ' + str(len(cw_of_interest) + 2 * len(issue_of_interest)))
			# print('Link for this action: ' + str(int(best_action_index / (len(cw_of_interest) + 2 * len(issue_of_interest) ) )))
			
			best_action = best_action_index - ((len(cw_of_interest) + 2 * len(issue_of_interest)) * int(best_action_index / (len(cw_of_interest) + 2 * len(issue_of_interest) ) ))
			# print('Best action selected: ' + str(best_action))

			best_action = len(cw_of_interest) + len(issue_of_interest) - 1

			for links in link_list:

				# IS THIS CORRECT - SHOULDNT THE SAME CHECK AS BEFORE BE ALSO IMPLEMENTED!
				if links == total_grade_list_links[int(best_action_index / (len(cw_of_interest) + 2 * len(issue_of_interest) ) )]:


					# print(links)					

					# Update of the aware decay parameter
					links.aware_decay = 5

					# 5. Performing the actual action
					# If the index is in the first part of the list, then the framing action is the best
					if best_action <= len(cw_of_interest) - 1:

						# print(' ')
						# print('Framing action - causal relation')
						# print('best_action: ' + str(best_action))
						# print('of_interest[0]: ' + str(of_interest[0]))
						# print('of_interest[0][best_action]: ' + str(of_interest[0][best_action]))

						implemented_action = ActionFunctions.action_implementor(links, of_interest[0][best_action], 0, agents, agents,affiliation_weights, resources_weight_action, resources_potency, False, 1)

					# If the index is in the second part of the list, then the aim influence action on the problem is the best
					if best_action > len(cw_of_interest) - 1 and best_action < len(cw_of_interest) + len(issue_of_interest) - 1:

						# print(' ')
						# print('Aim influence action')
						# print('best_action: ' + str(best_action))
						# print('of_interest[1]: ' + str(of_interest[1]))
						# print('of_interest[1][best_action - len(cw_of_interest)]: ' + str(of_interest[1][best_action - len(cw_of_interest)]))

						implemented_action = ActionFunctions.action_implementor(links, of_interest[1][best_action - len(cw_of_interest)], 1, agents, agents, affiliation_weights, resources_weight_action, resources_potency, False, 1)

					# If the index is in the first part of the list, then the aim influence action on the policy is the best
					if best_action >= len(cw_of_interest) + len(issue_of_interest) - 1:

						# print(' ')
						# print('Aim influence action')
						# print('best_action: ' + str(best_action))
						# print('of_interest[1]: ' + str(of_interest[1]))
						# print('of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]: ' + str(of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)]))

						implemented_action = ActionFunctions.action_implementor(links, of_interest[1][best_action - len(cw_of_interest) - len(issue_of_interest)], 0, agents, agents, \
							affiliation_weights, resources_weight_action, resources_potency, False, 1)

						
			# print('Resources left: ' + str(agents.resources_actions))
			agents.resources_actions -= agents.resources[0] * resources_weight_action

	def pm_pe_actions_as_3S(self, agents, link_list, policy_core, mid_level, secondary, resources_weight_action, resources_potency, affiliation_weights, conflict_level_coef):

		"""
		The PEs and PMs actions function - three streams (agenda setting)
		===========================

		This function is used to perform the different active actions of the
		policy entrepreneurs and the policy makers during the agenda setting.

		The actions that can be performed are framing, influence on states and 
		influence on aims. All of the actions are first graded. Then the action
		that has the highest grade is selected. Finally, the action selected 
		is implemented.

		Note: This function is the same as the one presented before for the backbone
		backbone+ and ACF. The main difference is the addition of actions related
		to the choice of a policy by the agents.

		"""

		len_PC = len(policy_core)
		len_ML = len(mid_level)
		len_S = len(secondary)
		total_issue_number = len_PC + len_ML + len_S

		# Selection of the cw of interest
		cw_of_interest = []
		# We only consider the causal relations related to the problem selected by the agent
		for cw_choice in range(len(policy_core)):
				cw_of_interest.append(len_PC + len_ML + len_S + (agents.select_problem_3S_as - len_PC) + cw_choice * len(mid_level))

		# Selection of the impact of interest
		impact_number = len(agents.belieftree_policy[0][agents.select_policy_3S_as])

		# print(' ')
		# print('Causal relations of interest: ' + str(cw_of_interest))

		# Making sure there are enough resources
		while agents.resources_actions > 0.001:

			# Going through all the links in the model
			# print(agents)
			total_grade_list = []
			total_grade_list_links = []
			for links in link_list:

				# Making sure that the link is attached to the agent and has a aware higher than 0
				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
					total_grade_list_links.append(links)
					
					# 1. Framing on causal relation and policy impacts

					# If the agent is advocating or a problem, the following tasks are performed
					if agents.select_issue_3S_as == 'problem':
						# 1.a. Grading all framing actions on causal relations:
						# Checking through all possible framing - This is all based on partial knowledge!
						for cw in cw_of_interest:

							cw_grade = ActionFunctions.action_grade_calculator(links, cw, 0, agents, affiliation_weights)
							total_grade_list.append(cw_grade)	

					# If the agent is advocating or a policy, the following tasks are performed
					if agents.select_issue_3S_as == 'policy':
						# 1.b. Grading all framing actions on policy impacts:

						# Checking through all possible framing - This is all based on partial knowledge!
						for impact in range(impact_number):

							impact_grade = ActionFunctions.action_grade_calculator_3S_AS(links, impact, agents, affiliation_weights, conflict_level_coef)
							total_grade_list.append(impact_grade)

					# 2. Grading all individual actions - Aim change
					aim_grade = ActionFunctions.action_grade_calculator(links, agents.select_problem_3S_as, 1, agents, affiliation_weights)
					total_grade_list.append(aim_grade)

					# 3. Grading all individual actions - State change
					state_grade = ActionFunctions.action_grade_calculator(links, agents.select_problem_3S_as, 0, agents, affiliation_weights)
					total_grade_list.append(state_grade)

			# print(' ')
			# print('Number of actions: ' + str(len(total_grade_list)))
			# print(total_grade_list)

			# 4. Choosing an action

			# If the agent is advocating or a problem, the following tasks are performed
			if agents.select_issue_3S_as == 'problem':

				best_action_index = total_grade_list.index(max(total_grade_list))
				agent_best_action = int(best_action_index/(len(cw_of_interest) + 1 + 1))
				best_action = best_action_index - (agent_best_action)*(len(cw_of_interest) + 1 + 1)

				# print(' ')
				# print('----- Considering new action grading (problem) -----')
				# print('best_action_index: ' + str(best_action_index))
				# print('Number of actions per agent: ' + str(len(cw_of_interest) + 1 + 1))
				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
				# print('Action to be performed: ' + str(best_action))
				# print('Agent performing the action: ' + str(agent_best_action))

			# If the agent is advocating or a policy, the following tasks are performed
			if agents.select_issue_3S_as == 'policy':
				
				best_action_index = total_grade_list.index(max(total_grade_list))
				agent_best_action = int(best_action_index/(impact_number + 1 + 1))
				best_action = best_action_index - (agent_best_action)*(impact_number + 1 + 1)

				# print(' ')
				# print('----- Considering new action grading (policy) -----')
				# print('best_action_index: ' + str(best_action_index))
				# print('Number of actions per agent: ' + str(impact_number + 1 + 1))
				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
				# print('Action to be performed: ' + str(best_action))
				# print('Agent performing the action: ' + str(agent_best_action))


			# 5. Performing the actual action
			# Selecting the link:
			for links in link_list:

				# If the agent is advocating or a problem, the following tasks are performed
				if agents.select_issue_3S_as == 'problem':

					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
						# print(links)

						# Updating the aware decay parameter
						links.aware_decay = 5

						# If the index is in the first part of the list, then the framing action is the best
						if best_action <= len(cw_of_interest) - 1:
							# print(' ')
							# print('Performing a causal relation framing action')
							# print('best_action: ' + str(best_action))
							# print('cw_of_interest: ' + str(cw_of_interest))
							# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

							implemented_action = ActionFunctions.action_implementor(links, cw_of_interest[best_action], 0, agents, agents, affiliation_weights, resources_weight_action, resources_potency, False, 1)

						# If the index is in the second part of the list, then the aim influence action is the best
						if best_action == len(cw_of_interest):
							# print(' ')
							# print('Performing a state change action')
							# print('best_action: ' + str(best_action))

							implemented_action = ActionFunctions.action_implementor(links, agents.select_problem_3S_as, 1, agents, agents, affiliation_weights, resources_weight_action, resources_potency, False, 1)

						# If the index is in the first part of the list, then the state influence action is the best
						if best_action == len(cw_of_interest) + 1:
							# print(' ')
							# print('Performing an aim change action')
							# print('best_action: ' + str(best_action))

							implemented_action = ActionFunctions.action_implementor(links, agents.select_problem_3S_as, 0, agents, agents, affiliation_weights, resources_weight_action, resources_potency, False, 1)


				# If the agent is advocating or a policy, the following tasks are performed
				if agents.select_issue_3S_as == 'policy':
					
					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
						# print(links)

						# Updating the aware decay parameter
						links.aware_decay = 5

						# If the index is in the first part of the list, then the framing action is the best
						if best_action <= impact_number - 1:
							# print(' ')
							# print('Performing a causal relation framing action')
							# print('best_action: ' + str(best_action))
							# print('impact_number: ' + str(impact_number))

							implemented_action = ActionFunctions.action_implementor_3S_AS(links, agents.select_policy_3S_as, best_action, agents, affiliation_weights, agents, resources_weight_action, resources_potency, False, 1)

						# If the index is in the second part of the list, then the aim influence action is the best
						if best_action == impact_number:
							# print(' ')
							# print('Performing a state change action')
							# print('best_action: ' + str(best_action))

							implemented_action = ActionFunctions.action_implementor(links, agents.select_problem_3S_as, 1, agents, agents, affiliation_weights, resources_weight_action, resources_potency, False, 1)

						# If the index is in the first part of the list, then the state influence action is the best
						if best_action == impact_number + 1:
							# print(' ')
							# print('Performing an aim change action')
							# print('best_action: ' + str(best_action))

							implemented_action = ActionFunctions.action_implementor(links, agents.select_problem_3S_as, 0, agents, agents, affiliation_weights, resources_weight_action, resources_potency, False, 1)

			agents.resources_actions -= agents.resources[0] * resources_weight_action

	def pm_pe_actions_pf_3S(self, agents, link_list, policy_core, mid_level, secondary, resources_weight_action, resources_potency, agenda_prob_3S_as, affiliation_weights, conflict_level_coef):

		"""
		The PEs and PMs actions function - three streams (policy formulation)
		===========================

		This function is used to perform the different active actions of the
		policy entrepreneurs and the policy makers during the policy formulation.

		The actions that can be performed are framing, influence on states and 
		influence on aims. All of the actions are first graded. Then the action
		that has the highest grade is selected. Finally, the action selected 
		is implemented.

		Note: This function is the same as the one presented before for the backbone
		backbone+ and ACF. The main difference is the addition of actions related
		to the choice of a policy by the agents.

		"""

		len_PC = len(policy_core)
		len_ML = len(mid_level)
		len_S = len(secondary)
		total_issue_number = len_PC + len_ML + len_S

		# Selection of the cw of interest
		cw_of_interest = []
		# Select one by one the Pr
		j = agenda_prob_3S_as
		# for j in range(len_ML):
		# Selecting the causal relations starting from Pr
		for k in range(len_S):
			# Contingency for partial knowledge issues
			# print(len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML)
			if (agents.belieftree[0][len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML][0] < 0 and (agents.belieftree[0][j][1] - agents.belieftree[0][j][0]) < 0) \
			  or (agents.belieftree[0][len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML][0] > 0 and (agents.belieftree[0][j][1] - agents.belieftree[0][j][0]) > 0):
				cw_of_interest.append(len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML)

		# Selection of the impact of interest
		impact_number = len(agents.belieftree_instrument[0][agents.select_policy_3S_pf])

		# print(' ')
		# print('Causal relations of interest: ' + str(cw_of_interest))

		# Making sure there are enough resources
		while agents.resources_actions > 0.001:

			# Going through all the links in the model
			# print(agents)
			total_grade_list = []
			total_grade_list_links = []
			for links in link_list:

				# Making sure that the link is attached to the agent and has a aware higher than 0
				if (links.agent1 == agents or links.agent2 == agents) and links.aware > 0:
					total_grade_list_links.append(links)
					
					# 1. Framing on causal relation and policy impacts

					# If the agent is advocating or a problem, the following tasks are performed
					if agents.select_issue_3S_pf == 'problem':
						# 1.a. Grading all framing actions on causal relations:
						# Checking through all possible framing - This is all based on partial knowledge!
						for cw in cw_of_interest:

							cw_grade = ActionFunctions.action_grade_calculator(links, cw, 0, agents, affiliation_weights)
							total_grade_list.append(cw_grade)


					# If the agent is advocating or a policy, the following tasks are performed
					if agents.select_issue_3S_pf == 'policy':
						# 1.b. Grading all framing actions on policy impacts:
						
						# Checking through all possible framing - This is all based on partial knowledge!
						for impact in range(impact_number):

							impact_grade = ActionFunctions.action_grade_calculator_3S_PF(links, impact, agents, affiliation_weights, conflict_level_coef)
							total_grade_list.append(impact_grade)
							
					# 2. Grading all individual actions - Aim change
					aim_grade = ActionFunctions.action_grade_calculator(links, agents.select_problem_3S_pf, 1, agents, affiliation_weights)
					total_grade_list.append(aim_grade)

					# 3. Grading all individual actions - State change
					state_grade = ActionFunctions.action_grade_calculator(links, agents.select_problem_3S_pf, 0, agents, affiliation_weights)
					total_grade_list.append(state_grade)

			# 4. Choosing an action

			# If the agent is advocating or a problem, the following tasks are performed
			if agents.select_issue_3S_as == 'problem':

				best_action_index = total_grade_list.index(max(total_grade_list))
				agent_best_action = int(best_action_index/(len(cw_of_interest) + 1 + 1))
				best_action = best_action_index - (agent_best_action)*(len(cw_of_interest) + 1 + 1)

				# print(' ')
				# print('----- Considering new action grading (problem) -----')
				# print('best_action_index: ' + str(best_action_index))
				# print('Number of actions per agent: ' + str(len(cw_of_interest) + 1 + 1))
				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
				# print('Action to be performed: ' + str(best_action))
				# print('Agent performing the action: ' + str(agent_best_action))

			# If the agent is advocating or a policy, the following tasks are performed
			if agents.select_issue_3S_as == 'policy':
				
				best_action_index = total_grade_list.index(max(total_grade_list))
				agent_best_action = int(best_action_index/(impact_number + 1 + 1))
				best_action = best_action_index - (agent_best_action)*(impact_number + 1 + 1)

				# print(' ')
				# print('----- Considering new action grading (policy) -----')
				# print('best_action_index: ' + str(best_action_index))
				# print('Number of actions per agent: ' + str(impact_number + 1 + 1))
				# print('Total number of agents being influenced: ' + str(len(total_grade_list_links)))
				# print('Action to be performed: ' + str(best_action))
				# print('Agent performing the action: ' + str(agent_best_action))

			# 5. Performing the actual action
			# Selecting the link:
			for links in link_list:

				# If the agent is advocating or a problem, the following tasks are performed
				if agents.select_issue_3S_pf == 'problem':

					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):
						# print(links)

						# Updating the aware decay parameter
						links.aware_decay = 5

						# If the index is in the first part of the list, then the framing action is the best
						if best_action <= len(cw_of_interest) - 1:
							# print(' ')
							# print('Performing a causal relation framing action')
							# print('best_action: ' + str(best_action))
							# print('cw_of_interest: ' + str(cw_of_interest))
							# print('cw_of_interest[best_action]: ' + str(cw_of_interest[best_action]))

							implemented_action = ActionFunctions.action_implementor(links, cw_of_interest[best_action], 0, agents, agents, affiliation_weights, resources_weight_action, resources_potency, False, 1)

						# If the index is in the second part of the list, then the aim influence action is the best
						if best_action == len(cw_of_interest):
							# print(' ')
							# print('Performing a state change action')
							# print('best_action: ' + str(best_action))

							implemented_action = ActionFunctions.action_implementor(links, agents.select_problem_3S_pf, 1, agents, agents, affiliation_weights, resources_weight_action, resources_potency, False, 1)

						# If the index is in the first part of the list, then the state influence action is the best
						if best_action == len(cw_of_interest) + 1:
							# print(' ')
							# print('Performing an aim change action')
							# print('best_action: ' + str(best_action))

							implemented_action = ActionFunctions.action_implementor(links, agents.select_problem_3S_pf, 0, agents, agents, affiliation_weights, resources_weight_action, resources_potency, False, 1)

				# If the agent is advocating or a policy, the following tasks are performed
				if agents.select_issue_3S_pf == 'policy':
					
					if (links.agent1 == agents and links.agent2.unique_id == agent_best_action) or (links.agent1.unique_id == agent_best_action and links.agent2 == agents):

						# Updating the aware decay parameter
						links.aware_decay = 5

						# If the index is in the first part of the list, then the framing action is the best
						if best_action <= impact_number - 1:
							# print(' ')
							# print('Performing a causal relation framing action')
							# print('best_action: ' + str(best_action))
							# print('impact_number: ' + str(impact_number))

							implemented_action = ActionFunctions.action_implementor_3S_PF(links, agents.select_policy_3S_pf, best_action, agents, agents, affiliation_weights, resources_weight_action, resources_potency, False, 1)

						# If the index is in the second part of the list, then the aim influence action is the best
						if best_action == impact_number:
							# print(' ')
							# print('Performing a state change action')
							# print('best_action: ' + str(best_action))

							implemented_action = ActionFunctions.action_implementor(links, agents.select_problem_3S_pf, 1, agents, agents, affiliation_weights, resources_weight_action, resources_potency, False, 1)

						# If the index is in the first part of the list, then the state influence action is the best
						if best_action == impact_number + 1:
							# print(' ')
							# print('Performing an aim change action')
							# print('best_action: ' + str(best_action))

							implemented_action = ActionFunctions.action_implementor(links, agents.select_problem_3S_pf, 0, agents, agents, affiliation_weights, resources_weight_action, resources_potency, False, 1)

			# agents.resources_actions -= agents.resources
			agents.resources_actions -= agents.resources[0] * resources_weight_action


# Creation of the policy maker agents
class Policymakers(Agent):

	def __init__(self, run_number, agent_id, unique_id, pos, network_strategy, affiliation, resources, belieftree, instrument_preferences, belieftree_policy, belieftree_instrument, select_as_issue, select_pinstrument, select_issue_3S_as, \
		select_problem_3S_as, select_policy_3S_as, select_issue_3S_pf, select_problem_3S_pf, select_policy_3S_pf, team_as, team_pf, coalition_as, coalition_pf):
		# super().__init__(unique_id, model)
		self.run_number = run_number
		self.agent_id = agent_id
		self.pos = pos
		self.network_strategy = network_strategy
		self.unique_id = unique_id
		# self.model = model
		self.affiliation = affiliation
		self.resources = resources
		self.belieftree = belieftree
		self.belieftree_policy = belieftree_policy
		self.belieftree_instrument = belieftree_instrument
		self.instrument_preferences = instrument_preferences
		self.select_as_issue = select_as_issue
		self.select_pinstrument = select_pinstrument
		self.select_issue_3S_as = select_issue_3S_as
		self.select_problem_3S_as = select_problem_3S_as
		self.select_policy_3S_as = select_policy_3S_as
		self.select_issue_3S_pf = select_issue_3S_pf
		self.select_problem_3S_pf = select_problem_3S_pf
		self.select_policy_3S_pf = select_policy_3S_pf
		self.team_as = team_as
		self.team_pf = team_pf
		self.coalition_as = coalition_as
		self.coalition_pf = coalition_pf

	# def __str__(self):
	# 	return 'POLICYMAKER - Affiliation: ' + str(self.affiliation) + ', Resources: ' + str(self.resources) + \
	# 	', Position: [' + str(self.pos[0]) + ',' + str(self.pos[1]) + '], ID: ' + str(self.unique_id) + \
	# 	', Problem selected: ' + str(self.select_problem) + ', Policy selected: ' + str(self.select_policy) + \
	# 	', Belief tree: ' + str(self.belieftree)



	# Simple print with ID
	def __str__(self):
		return 'Policy maker: ' + str(self.unique_id)

	def policymakers_states_update(self, agent, master_list, affiliation_weights):

		"""
		The policy makers states update function
		===========================

		This function uses the data from the external parties to update the states of 
		the policy makers.

		Note: Ultimately, this would need to include the external parties lack of interests
		for some of the states.

		"""

		#' Addition of more than 3 affiliation will lead to unreported errors!')
		if len(affiliation_weights) != 3:
			print('WARNING - THIS CODE DOESNT WORK FOR MORE OR LESS THAN 3 AFFILIATIONS')

		# Defining the external party list along with the truth agent relation
		externalparties_list = []
		for agents in master_list:
			if type(agents) == Truth:
				truthagent = agents
			if type(agents) == Externalparties:
				externalparties_list.append(agents)

		# going through the different external parties:
		belief_sum_ep = [0 for k in range(len(truthagent.belieftree_truth))]
		# print(belief_sum_ep)
		for i in range(len(truthagent.belieftree_truth)):
			# print('NEW ISSUE! NEW ISSUES!')
			# This is used because in some cases, the external parties will have no impact on the agent (None values in the states of the EP)
			actual_length_ep = 0
			for j in range(len(externalparties_list)):
				# This line is added in case the EP has None states
				if externalparties_list[j].belieftree[0][i][0] != 'No':
					actual_length_ep += 1
					# Currently, the state of the policy makers is initialised as being equal to their initial aim:
					if agent.belieftree[0][i][0] == None:
						# print('Triggered - changed to: ' + str(agent.belieftree[0][i][1]))
						agent.belieftree[0][i][0] = agent.belieftree[0][i][1]
					# If they have the same affiliation, add without weight
					if externalparties_list[j].affiliation == agent.affiliation:
						# print('AFFILIATIONS ARE EQUAL')
						# print('issue ' + str(i+1) + ': ' + str(externalparties_list[j].belieftree[0][i][0]) +  /
						# ' and affiliation: ' + str(externalparties_list[j].affiliation) + '  ' + str(externalparties_list[j].unique_id))
						# print('This is the sum: ' + str(belief_sum_ep[i]))
						belief_sum_ep[i] = belief_sum_ep[i] + (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0])
						# print('The sum is equal to: ' + str(belief_sum_ep))
						# print('The change in state belief is equal to: ' + str(belief_sum_ep[i] / len(externalparties_list)))
					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 1) or \
					   (externalparties_list[j].affiliation == 1 and agent.affiliation == 0):
						# print('AFFILIATION 1 AND 2')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[0]
					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 2) or \
					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 0):
						# print('AFFILIATION 1 AND 3')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[1]
					if (externalparties_list[j].affiliation == 1 and agent.affiliation == 2) or \
					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 1):
						# print('AFFILIATION 2 AND 3')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[2]
			agent.belieftree[0][i][0] = agent.belieftree[0][i][0] + belief_sum_ep[i] / actual_length_ep
			# print('This is issue: ' + str(i+1) + ' and its new value is: ' + str(agent.belieftree[0][i][0]))
		# print(agent)

# Creation of the policy entrepreneur agents
class Policyentres(Agent):

	def __init__(self, run_number, agent_id, unique_id, pos, network_strategy, affiliation, resources, belieftree, instrument_preferences, belieftree_policy, belieftree_instrument, select_as_issue, select_pinstrument, select_issue_3S_as, \
		select_problem_3S_as, select_policy_3S_as, select_issue_3S_pf, select_problem_3S_pf, select_policy_3S_pf, team_as, team_pf, coalition_as, coalition_pf):
		# super().__init__(unique_id, model)
		self.run_number = run_number
		self.agent_id = agent_id
		self.unique_id = unique_id
		self.pos = pos
		self.network_strategy = network_strategy
		# self.model = model
		self.affiliation = affiliation
		self.resources = resources
		self.belieftree = belieftree
		self.belieftree_policy = belieftree_policy
		self.belieftree_instrument = belieftree_instrument
		self.instrument_preferences = instrument_preferences
		self.select_as_issue = select_as_issue
		self.select_pinstrument = select_pinstrument
		self.select_issue_3S_as = select_issue_3S_as
		self.select_problem_3S_as = select_problem_3S_as
		self.select_policy_3S_as = select_policy_3S_as
		self.select_issue_3S_pf = select_issue_3S_pf
		self.select_problem_3S_pf = select_problem_3S_pf
		self.select_policy_3S_pf = select_policy_3S_pf
		self.team_as = team_as
		self.team_pf = team_pf
		self.coalition_as = coalition_as
		self.coalition_pf = coalition_pf

	# def __str__(self):
	# 	return 'POLICYENTREPRENEUR - Affiliation: ' + str(self.affiliation) + ', Resources: ' + str(self.resources) + \
	# 	', Position: [' + str(self.pos[0]) + ',' + str(self.pos[1]) + '], ID: ' + str(self.unique_id) + \
	# 	', Problem selected: ' + str(self.select_problem) + ', Policy selected: ' + str(self.select_policy) + \
	# 	', Belief tree: ' + str(self.belieftree)

	# Simple print with ID
	def __str__(self):
		return 'Policy entrepreneur: ' + str(self.unique_id)

	def policyentres_states_update(self, agent, master_list, affiliation_weights):

		"""
		The policy entrepreneurs states update function
		===========================

		This function uses the data from the external parties to update the states of 
		the policy entrepreneurs.

		Note: Ultimately, this would need to include the external parties lack of interests
		for some of the states.

		"""

		#' Addition of more than 3 affiliation will lead to unreported errors!')
		if len(affiliation_weights) != 3:
			print('WARNING - THIS CODE DOESNT WORK FOR MORE OR LESS THAN 3 AFFILIATIONS')

		# Defining the external parties list and the truth agent
		externalparties_list = []
		for agents in master_list:
			if type(agents) == Truth:
				truthagent = agents
			if type(agents) == Externalparties:
				externalparties_list.append(agents)

		# going through the different external parties:
		belief_sum_ep = [0 for k in range(len(truthagent.belieftree_truth))]
		# print(belief_sum_ep)
		for i in range(len(truthagent.belieftree_truth)):
			# print('NEW ISSUE! NEW ISSUES!')
			# This is used because in some cases, the external parties will have no impact on the agent (None values in the states of the EP)
			actual_length_ep = 0
			for j in range(len(externalparties_list)):
				# This line is added in case the EP has None states
				if externalparties_list[j].belieftree[0][i][0] != 'No':
					actual_length_ep += 1
					# Currently, the state of the policy makers is initialised as being equal to their initial aim:
					if agent.belieftree[0][i][0] == None:
						# print('Triggered - changed to: ' + str(agent.belieftree[0][i][1]))
						agent.belieftree[0][i][0] = agent.belieftree[0][i][1]
					# If they have the same affiliation, add without weight
					if externalparties_list[j].affiliation == agent.affiliation:
						# print('AFFILIATIONS ARE EQUAL')
						# print('issue ' + str(i+1) + ': ' + str(externalparties_list[j].belieftree[0][i][0]) +  /
						# ' and affiliation: ' + str(externalparties_list[j].affiliation) + '  ' + str(externalparties_list[j].unique_id))
						# print('This is the sum: ' + str(belief_sum_ep[i]))
						belief_sum_ep[i] = belief_sum_ep[i] + (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0])
						# print('The sum is equal to: ' + str(belief_sum_ep))
						# print('The change in state belief is equal to: ' + str(belief_sum_ep[i] / len(externalparties_list)))
					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 1) or \
					   (externalparties_list[j].affiliation == 1 and agent.affiliation == 0):
						# print('AFFILIATION 1 AND 2')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[0]
					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 2) or \
					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 0):
						# print('AFFILIATION 1 AND 3')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[1]
					if (externalparties_list[j].affiliation == 1 and agent.affiliation == 2) or \
					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 1):
						# print('AFFILIATION 2 AND 3')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree[0][i][0]) * affiliation_weights[2]
			agent.belieftree[0][i][0] = agent.belieftree[0][i][0] + belief_sum_ep[i] / actual_length_ep
			# print('This is issue: ' + str(i+1) + ' and its new value is: ' + str(agent.belieftree[0][i][0]))
		# print(agent)

# Creation of the Truth agent
class Truth(Agent):

	def __init__(self, pos, belieftree_truth):
		# super().__init__(unique_id, model)
		self.pos = pos
		# self.model = model
		self.belieftree_truth = belieftree_truth

	def __str__(self):
		return 'Position: [' + str(self.pos[0]) + ',' + str(self.pos[1]) + '], Belief tree: ' + str(self.belieftree_truth)

# Creation of the electorate agents
class Electorate(Agent):

	def __init__(self, run_number, pos, affiliation, belieftree_electorate, representation):
		# super().__init__(unique_id, model)
		self.run_number = run_number
		self.pos = pos
		# self.model = model
		self.affiliation = affiliation
		self.belieftree_electorate = belieftree_electorate
		self.representation = representation

	def electorate_influence(self, agent, master_list, affiliation_number, electorate_influence_coefficient):

		"""
		Electorate influence function
		===========================

		This function calculates the influence of the electorates 
		on the policy makers. It is dependent on the affiliations
		of each of the agents. The electorate can only influence
		policy makers with whom they share their affiliations.

		"""

		self.master_list = master_list

		policymaker_list = []
		for agents in self.master_list:
			if type(agents) == Policymakers:
				policymaker_list.append(agents)

		policymaker_number = len(policymaker_list)
		# policymaker_list = self.master_list[Policymakers]
		# Looking through all affiliations
		for i in range(affiliation_number):
			# Selecting one affiliation
			if self.affiliation == i:
				# Selection of the policy maker:
				for j in range(policymaker_number):
					# checking of the affiliation match of the policy maker
					if policymaker_list[j].affiliation == i:
						# Now we can change the tree of the policy makers
						for k in range(len(self.belieftree_electorate)):
							# print('Before change: ' + str(policymaker_list[j].belieftree[0][k][1]))
							policymaker_list[j].belieftree[0][k][1] = policymaker_list[j].belieftree[0][k][1] + \
							  (self.belieftree_electorate[k][1] - policymaker_list[j].belieftree[0][k][1]) * electorate_influence_coefficient
							# Again the oneminusone check does not work here
							policymaker_list[j].belieftree[0][k][1] = \
								ActionFunctions.one_minus_one_check(policymaker_list[j].belieftree[0][k][1])
							# print('Afters change: ' + str(policymaker_list[j].belieftree[0][k][1]))
						# print(policymaker_list[j].pos)
				# print(self.belieftree_electorate)
				# print(self.affiliation)
				# print(self.pos)

	def one_minus_one_check(self, to_be_checked_parameter):

		"""
		One minus one check function
		===========================

		This function checks that a certain values does not got over one
		and does not go below one due to the randomisation.
		
		"""

		checked_parameter = 0
		if to_be_checked_parameter > 1:
			checked_parameter = 1
		elif to_be_checked_parameter < -1:
			checked_parameter = -1
		else:
			checked_parameter = to_be_checked_parameter
		return checked_parameter

	def electorate_states_update(self, agent, master_list, affiliation_weights):

		"""
		The electorate states update function
		===========================

		This function uses the agent, the master list and the affiliation weight
		to update the states of the electorate belief tree. This is done using the
		states of the external parties depending on their affiliation and is therefore
		impacted by the affiliation weights.

		It is also assumed that the initial belief of the electorate is equal
		to their aim in the first tick.

		"""

		#' Addition of more than 3 affiliation will lead to unreported errors!')
		if len(affiliation_weights) != 3:
			print('WARNING - THIS CODE DOESNT WORK FOR MORE OR LESS THAN 3 AFFILIATIONS')

		# Defining the external party list along with the truth agent relation
		externalparties_list = []
		for agents in master_list:
			if type(agents) == Truth:
				truthagent = agents
			if type(agents) == Externalparties:
				externalparties_list.append(agents)

		# Going through the different external parties:
		belief_sum_ep = [0 for k in range(len(truthagent.belieftree_truth))]
		for i in range(len(truthagent.belieftree_truth)):
			# This is used because in some cases, the external parties will have no impact on the agent (None values in the states of the EP)
			actual_length_ep = 0
			for j in range(len(externalparties_list)):
				# This line is added in case the EP has None states
				if externalparties_list[j].belieftree[i][0] != 'No':
					actual_length_ep += 1
					# Currently, the state of the policy makers is initialised as being equal to their initial aim:
					if agent.belieftree_electorate[i][0] == None:
						# print('Triggered - changed to: ' + str(agent.belieftree[0][i][1]))
						agent.belieftree_electorate[i][0] = agent.belieftree_electorate[i][1]
					# If they have the same affiliation, add without weight
					if externalparties_list[j].affiliation == agent.affiliation:
						# print('AFFILIATIONS ARE EQUAL')
						# print('issue ' + str(i+1) + ': ' + str(externalparties_list[j].belieftree[0][i][0]) +  /
						# ' and affiliation: ' + str(externalparties_list[j].affiliation) + '  ' + str(externalparties_list[j].unique_id))
						# print('This is the sum: ' + str(belief_sum_ep[i]))
						belief_sum_ep[i] = belief_sum_ep[i] + (externalparties_list[j].belieftree[0][i][0] - agent.belieftree_electorate[i][0])
						# print('The sum is equal to: ' + str(belief_sum_ep))
						# print('The change in state belief is equal to: ' + str(belief_sum_ep[i] / len(externalparties_list)))
					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 1) or \
					   (externalparties_list[j].affiliation == 1 and agent.affiliation == 0):
						# print('AFFILIATION 1 AND 2')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree_electorate[i][0]) * affiliation_weights[0]
					if (externalparties_list[j].affiliation == 0 and agent.affiliation == 2) or \
					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 0):
						# print('AFFILIATION 1 AND 3')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree_electorate[i][0]) * affiliation_weights[1]
					if (externalparties_list[j].affiliation == 1 and agent.affiliation == 2) or \
					   (externalparties_list[j].affiliation == 2 and agent.affiliation == 1):
						# print('AFFILIATION 2 AND 3')
						belief_sum_ep[i] = belief_sum_ep[i] + \
						   (externalparties_list[j].belieftree[0][i][0] - agent.belieftree_electorate[i][0]) * affiliation_weights[2]
			agent.belieftree_electorate[i][0] = agent.belieftree_electorate[i][0] + belief_sum_ep[i] / actual_length_ep

	# def __str__(self):
	# 	return 'Affiliation: ' + str(self.affiliation) + ', Position: [' + str(self.pos[0]) + \
	# 	',' + str(self.pos[1]) + '], Electorate belief tree: ' + str(self.belieftree_electorate)

# Creation of the external party agents
class Externalparties(Agent):

	def __init__(self, run_number, agent_id, unique_id, pos, network_strategy, affiliation, resources, belieftree, instrument_preferences, belieftree_policy, belieftree_instrument, select_as_issue, select_pinstrument, select_issue_3S_as, \
		select_problem_3S_as, select_policy_3S_as, select_issue_3S_pf, select_problem_3S_pf, select_policy_3S_pf, team_as, team_pf, coalition_as, coalition_pf):
		# super().__init__(unique_id, model)
		self.run_number = run_number
		self.agent_id = agent_id
		self.unique_id = unique_id
		self.pos = pos
		self.network_strategy = network_strategy
		self.affiliation = affiliation
		self.resources = resources
		self.belieftree = belieftree
		self.instrument_preferences = instrument_preferences
		self.belieftree_policy = belieftree_policy
		self.belieftree_instrument = belieftree_instrument
		self.select_as_issue = select_as_issue
		self.select_pinstrument = select_pinstrument
		self.select_issue_3S_as = select_issue_3S_as
		self.select_problem_3S_as = select_problem_3S_as
		self.select_policy_3S_as = select_policy_3S_as
		self.select_issue_3S_pf = select_issue_3S_pf
		self.select_problem_3S_pf = select_problem_3S_pf
		self.select_policy_3S_pf = select_policy_3S_pf
		self.team_as = team_as
		self.team_pf = team_pf
		self.coalition_as = coalition_as
		self.coalition_pf = coalition_pf

	def external_parties_states_update(self, agent, master_list, no_interest_states):

		"""
		The external parties states update function
		===========================

		This function uses the truth agent to update the states of the external parties
		belief tree.

		Note: Ultimately, this would need to include the external parties lack of interests
		for some of the states.

		"""

		for agents in master_list:
			if type(agents) == Truth:
				truthagent = agents

		# print('Before: '  + str(agent.belieftree[0]))
		for i in range(len(truthagent.belieftree_truth)):
			# print(no_interest_states[agent.agent_id][i])
			if no_interest_states[agent.agent_id][i] == 1:
				# print('Value i: ' + str(i) + ' is being changed')
				agent.belieftree[0][i][0] = truthagent.belieftree_truth[i]
			# print('HERE!')
			else:
				agent.belieftree[0][i][0] = 'No'

		# print('After: '  + str(agent.belieftree[0]))
		# print('State updated!')
	
	# def __str__(self):
	# 	return 'EXTERNAL PARTIES - ' + 'Affiliation: ' + str(self.affiliation) + ', Resources: ' + str(self.resources) + \
	# 	', Position: [' + str(self.pos[0]) + \
	# 	',' + str(self.pos[1]) + '], ID: ' + str(self.unique_id) + ', Problem selected + 1: ' + str(self.select_problem) + \
	# 	', Policy selected + 1: ' + str(self.select_policy) + ', Belief tree: ' + str(self.belieftree)

	# Simple print with ID
	def __str__(self):
		return 'External party: ' + str(self.unique_id)

	def external_parties_actions_as(self, agents, agent_action_list, causalrelation_number, \
		affiliation_weights, policy_core, mid_level, secondary, electorate_number, action_agent_number, master_list, link_list, resources_weight_action, resources_potency):

		"""
		The external parties actions function (agenda setting)
		===========================

		This function is used to perform the different active actions of the
		external parties during the agenda setting.

		It is split in two main parts:
		1. All active actions (blanket framing, blanket state influence and 
		blanket aim influence)
		2. Electorate influence - on the aims

		"""

		len_PC = len(policy_core)
		len_ML = len(mid_level)
		len_S = len(secondary)

		# Assignment of the resources for the two main types of actions:
		agents.resources_actions_EInfluence = agents.resources_actions * 0.2

		############################################################################################################
		# 1. Blanket framing, grading of actions and implementation of the best actions until resources run out 
		# 100% of the resources (from actions)

		# Selecting the relevant causal relations
		cw_of_interest = []
		for cw_choice in range(len(policy_core)):
				cw_of_interest.append(len_PC + len_ML + len_S + (agents.select_as_issue - len_PC) + cw_choice * len(mid_level))

		# Making sure that there are enough resources
		while agents.resources_actions > 0.001:

			####################################
			# Grading of all the possible actions

			total_agent_grades = []

			# For the causal relations
			for cw in cw_of_interest:
				cw_grade_list = []
				# Going through all active agents
				for agent_inspected in agent_action_list:
					# Going through all of the links
					for links in link_list:
						# Check that only the link of interest is selected
						if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:
							# Make sure to look at the right direction of the conflict level

							cw_grade = ActionFunctions.action_grade_calculator(links, cw, 0, agents, affiliation_weights)
							cw_grade_list.append(cw_grade)


				total_agent_grades.append(sum(cw_grade_list))

			# For the state on the selected issue
			state_grade_list = []
			# Going through all active agents
			for agent_inspected in agent_action_list:
				for links in link_list:
					# Check that only the link of interest is selected
					if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:

						state_grade = ActionFunctions.action_grade_calculator(links, agents.select_as_issue, 0, agents, affiliation_weights)
						state_grade_list.append(state_grade)

			total_agent_grades.append(sum(state_grade_list))

			# For the aim on the selected issue
			aim_grade_list = []
			# Going through all active agents
			for agent_inspected in agent_action_list:
				for links in link_list:
					# Check that only the link of interest is selected
					if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:

						aim_grade = ActionFunctions.action_grade_calculator(links, agents.select_as_issue, 1, agents, affiliation_weights)
						aim_grade_list.append(aim_grade)

			total_agent_grades.append(sum(aim_grade_list))

			####################################
			# Select of the best action

			best_action = total_agent_grades.index(max(total_agent_grades))

			####################################
			# Application of the action selected

			# Going through all active agents
			for agent_inspected in agent_action_list:
				# Going through all of the links
				for links in link_list:
					# Check that only the link of interest is selected
					if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:
						# Make sure to look at the right direction of the conflict levels

						# Update aware decay
						links.aware_decay = 5

						# Implementation of a causal relation blanket action
						if best_action < len(cw_of_interest):

							implemented_action = ActionFunctions.action_implementor(links, cw_of_interest[best_action], 0, agents, agents, affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

						# Implementation of a state influence blanket action
						if best_action == len(cw_of_interest):

							implemented_action = ActionFunctions.action_implementor(links, agents.select_as_issue, 0, agents, agents, affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

						# Implementation of a state influence blanket action
						if best_action == len(cw_of_interest) + 1:

							implemented_action = ActionFunctions.action_implementor(links, agents.select_as_issue, 1, agents, agents, affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

			# Updating the resources after each action has been implemented
			agents.resources_actions -= agents.resources[0] * 0.1

		############################################################################################################
		# 2. Electorate influence, grading of actions and implementation of the best actions until resources run out 
		# 20% of the resources (from actions)

		# Making sure that there are enough resources
		while agents.resources_actions_EInfluence > 0.001:

			actions_EP_grades_EInfluence = []
			# FIRST - Calculation of the best option
			for issue_num in range(len_PC + len_ML):
				actions_EP_grades_EInfluence_ind = []
				# Going through all agents that are electorate from the master_list
				agents_electorate = []
				for agents_run in master_list:
					if type(agents_run) == Electorate:
						agents_electorate.append(agents_run)

				for agents_el in agents_electorate:

					# Setting grade to 0 if the external party has no interest in the issue:
					if agents.belieftree[0][issue_num][0] == 'No':
						issue_num_grade	 = 0 

					# Calculate a grade if the external party has an interest in the issue
					else:
						# Memorising the original belief values
						original_belief = [0,0,0]
						original_belief[0] = copy.copy(agents_el.belieftree_electorate[issue_num][0])
						original_belief[1] = copy.copy(agents_el.belieftree_electorate[issue_num][1])
						original_belief[2] = copy.copy(agents_el.belieftree_electorate[issue_num][2])

						if agents.affiliation == agents_el.affiliation:
							# Perfoming the action
							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
								* agents.resources[0] * 0.1 / electorate_number
							# Update of the preference
							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
							# Calculation of the new gradec
							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

						# Affiliation 1 and 2
						if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
							# Perfoming the action
							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
								* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number
							# Update of the preference
							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
							# Calculation of the new gradec
							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

						# Affiliation 1 and 3
						if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
							# Perfoming the action
							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
								* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number
							# Update of the preference
							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
							# Calculation of the new gradec
							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

						# Affiliation 2 and 3
						if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
							# Perfoming the action
							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
								* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number
							# Update of the preference
							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
							# Calculation of the new grade
							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

						# Restoring the initial values
						agents_el.belieftree_electorate[issue_num][0] = original_belief[0]
						agents_el.belieftree_electorate[issue_num][1] = original_belief[1]
						agents_el.belieftree_electorate[issue_num][2] = original_belief[2]


						# Re-updating the preference levels
						self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)

					actions_EP_grades_EInfluence_ind.append(issue_num_grade)

				actions_EP_grades_EInfluence.append(sum(actions_EP_grades_EInfluence_ind))

			# Choose the action that leads to the minimum amount of difference between the EP and the electorates
			best_EInfluence = actions_EP_grades_EInfluence.index(min(actions_EP_grades_EInfluence))
			
			# SECOND - Changing the aims of all the agents for the best choice
			for agents_el in agents_electorate:


				if agents.affiliation == agents_el.affiliation:
					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
					* agents.resources[0] * 0.1 / electorate_number

				# Affiliation 1 and 2
				if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
						* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number

					# Affiliation 1 and 3
				if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
						* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number

				# Affiliation 2 and 3
				if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
						* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number

				# 1-1 check
				agents_el.belieftree_electorate[best_EInfluence][1] = ActionFunctions.one_minus_one_check(agents_el.belieftree_electorate[best_EInfluence][1])

				# Re-updating the preference levels
				self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)

			agents.resources_actions_EInfluence -= agents.resources[0] * 0.1
			# agents.resources_actions -= agents.resources[0] * 0.1

	def external_parties_actions_pf(self, agents, agent_action_list, causalrelation_number, \
		affiliation_weights, policy_core, mid_level, secondary, electorate_number, action_agent_number, agenda_as_issue, instruments, master_list, link_list, resources_weight_action, resources_potency):

		"""
		The external parties actions function (policy formulation)
		===========================

		This function is used to perform the different active actions of the
		external parties during the policy formulation.

		It is split in two main parts:
		1. All active actions (blanket framing, blanket state influence and 
		blanket aim influence)
		2. Electorate influence - on the aims

		Note: This function is the same as the agenda setting function but adjusted
		for the change of selected issues.

		"""

		len_PC = len(policy_core)
		len_ML = len(mid_level)
		len_S = len(secondary)

		# Here are the modifications related to the policy formulation
		# Looking for the relevant causal relations for the policy formulation
		cw_of_interest = []
		# We only consider the causal relations related to the issue on the agenda
		print(agents.select_pinstrument)
		for cw_choice in range(len(secondary)):
			# Index explanation - pass all issues, then all causal relations related to the PC-ML links, then reach the links related to the issue on the agenda
			if agents.belieftree[0][len_PC + len_ML + len_S + (len_PC * len_ML) + (agenda_as_issue - len_PC)*len_S + cw_choice][0] \
				* instruments[agents.select_pinstrument][cw_choice] != 0:
				cw_of_interest.append(len_PC + len_ML + len_S + (len_PC * len_ML) + (agenda_as_issue - len_PC)*len_S + cw_choice)

		
		# Looking for the relevant issues for the policy formulation
		# That is we choose the secondary issues that are impacted by the policy instrument
		# that the agent has selected.
		issue_of_interest = []
		for issue_choice in range(len(secondary)):
			if instruments[agents.select_pinstrument][issue_choice] != 0:
				issue_of_interest.append(len_PC + len_ML + issue_choice)

		# Assignment of the resources for the two main types of actions:
		agents.resources_actions_EInfluence = agents.resources_actions * 0.2


		############################################################################################################
		# 1. Blanket framing, grading of actions and implementation of the best actions until resources run out 
		# 100% of the resources (from actions)

		# Making sure that there are enough resources
		while agents.resources_actions > 0.001:
			
			####################################
			# Grading of all the possible actions

			total_agent_grades = []

			# For the causal relations
			for cw in cw_of_interest:
				cw_grade_list = []
				# Going through all active agents
				for agent_inspected in agent_action_list:
					# Going through all of the links
					for links in link_list:
						# Check that only the link of interest is selected
						if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:

							cw_grade = ActionFunctions.action_grade_calculator(links, cw, 0, agents, affiliation_weights)
							cw_grade_list.append(cw_grade)

				total_agent_grades.append(sum(cw_grade_list))


			# For the state on the selected issue

			for issue_num in issue_of_interest:
				state_grade_list = []
				# Going through all active agents
				for agent_inspected in agent_action_list:
					for links in link_list:
						# Check that only the link of interest is selected
						if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:

							state_grade = ActionFunctions.action_grade_calculator(links, issue_num, 0, agents, affiliation_weights)
							state_grade_list.append(state_grade)

				total_agent_grades.append(sum(state_grade_list))

			# For the aim on the selected issue
			for issue_num in issue_of_interest:
				aim_grade_list = []
				# Going through all active agents
				for agent_inspected in agent_action_list:
					for links in link_list:
						# Check that only the link of interest is selected
						if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:

							aim_grade = ActionFunctions.action_grade_calculator(links, issue_num, 1, agents, affiliation_weights)
							aim_grade_list.append(aim_grade)

				total_agent_grades.append(sum(aim_grade_list))

			# print(' ')
			# print('cw_of_interest ', len(cw_of_interest))
			# print('issue_of_interest ', len(issue_of_interest))
			# print('total_agent_grades ', len(total_agent_grades))

			####################################
			# Select of the best action

			best_action = total_agent_grades.index(max(total_agent_grades)) 

			# print('best_action ', best_action)

			####################################
			# Application of the action selected

			# Going through all active agents
			for agent_inspected in agent_action_list:
				# Going through all of the links
				for links in link_list:
					# Check that only the link of interest is selected
					if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:
						# Make sure to look at the right direction of the conflict levels

						links.aware_decay = 5

						# Implementation of a causal relation blanket action
						if best_action < len(cw_of_interest):
							# print('Blanket framing action selected')
				
							implemented_action = ActionFunctions.action_implementor(links, cw_of_interest[best_action], 0, agents, agents, affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

						# Implementation of a state influence blanket action
						if best_action >= len(cw_of_interest) and best_action < len(cw_of_interest) + len(issue_of_interest):
							# print('Blanket state action selected')

							implemented_action = ActionFunctions.action_implementor(links, issue_of_interest[best_action - len(cw_of_interest)], 0, agents, agents, \
								affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

						# Implementation of a state influence blanket action
						if best_action >= len(cw_of_interest) + len(issue_of_interest):
							# print('Blanket aim action selected')

							implemented_action = ActionFunctions.action_implementor(links, issue_of_interest[best_action - len(cw_of_interest) - len(issue_of_interest)], 1, \
								agents, agents, affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

			# Updating the resources after each action has been implemented
			agents.resources_actions -= agents.resources[0] * 0.1


		############################################################################################################
		# 2. Electorate influence, grading of actions and implementation of the best actions until resources run out 
		# 20% of the resources (from actions)

		# Making sure that there are enough resources
		while agents.resources_actions_EInfluence > 0.001:

			actions_EP_grades_EInfluence = []
			# FIRST - Calculation of the best option
			for issue_num in range(len(issue_of_interest)):
				actions_EP_grades_EInfluence_ind = []
				# Going through all agents that are electorate from the master_list
				agents_electorate = []
				for agents_run in master_list:
					if type(agents_run) == Electorate:
						agents_electorate.append(agents_run)

				for agents_el in agents_electorate:

					# Setting grade to 0 if the external party has no interest in the issue:
					if agents.belieftree[0][issue_of_interest[issue_num]][0] == 'No':
						issue_num_grade	 = 0 

					# Calculate a grade if the external party has an interest in the issue
					else:
						if agents.affiliation == agents_el.affiliation:
							issue_num_grade = abs((agents.belieftree[0][issue_of_interest[issue_num]][1] - agents_el.belieftree_electorate[issue_of_interest[issue_num]][1]) * \
								agents.resources[0] * 0.1 / electorate_number)

						# Affiliation 1 and 2
						if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
							issue_num_grade = abs((agents.belieftree[0][issue_of_interest[issue_num]][1] - agents_el.belieftree_electorate[issue_of_interest[issue_num]][1]) * \
								agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number * affiliation_weights[0])

						# Affiliation 1 and 3
						if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
							issue_num_grade = abs((agents.belieftree[0][issue_of_interest[issue_num]][1] - agents_el.belieftree_electorate[issue_of_interest[issue_num]][1]) * \
								agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number * affiliation_weights[1])

						# Affiliation 2 and 3
						if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
							issue_num_grade = abs((agents.belieftree[0][issue_of_interest[issue_num]][1] - agents_el.belieftree_electorate[issue_of_interest[issue_num]][1]) * \
								agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number )

						# Restoring the initial values

					actions_EP_grades_EInfluence_ind.append(issue_num_grade)

				actions_EP_grades_EInfluence.append(sum(actions_EP_grades_EInfluence_ind))

			best_EInfluence = actions_EP_grades_EInfluence.index(max(actions_EP_grades_EInfluence))
			
			# SECOND - Changing the aims of all the agents for the best choice
			for agents_el in agents_electorate:

				if agents.affiliation == agents_el.affiliation:
					agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1] += (agents.belieftree[0][issue_of_interest[best_EInfluence]][1] - agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1]) \
					* agents.resources[0] * 0.1 / electorate_number

				# Affiliation 1 and 2
				if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
					agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1] += (agents.belieftree[0][issue_of_interest[best_EInfluence]][1] - agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1]) \
					* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number

					# Affiliation 1 and 3
				if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
					agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1] += (agents.belieftree[0][issue_of_interest[best_EInfluence]][1] - agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1]) \
					* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number

				# Affiliation 2 and 3
				if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
					agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1] += (agents.belieftree[0][issue_of_interest[best_EInfluence]][1] - agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1]) \
					* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number

				# Check for max and min:
				agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1] = ActionFunctions.one_minus_one_check(agents_el.belieftree_electorate[issue_of_interest[best_EInfluence]][1])

			agents.resources_actions_EInfluence -= agents.resources[0] * 0.1

	def external_parties_actions_as_3S(self, agents, agent_action_list, causalrelation_number, \
		affiliation_weights, policy_core, mid_level, secondary, electorate_number, action_agent_number, master_list, link_list, conflict_level_coef, resources_weight_action, resources_potency):

		"""
		The external parties actions function - three streams (agenda setting)
		===========================

		This function is used to perform the different active actions of the
		external parties during the agenda setting.

		It is split in two main parts:
		1. All active actions (blanket framing, blanket state influence and 
		blanket aim influence)
		2. Electorate influence - on the aims

		Note: This is the same function as the previous one, however it also 
		considers that the external parties can choose policies and hence adds
		code for the policy related actions.

		"""

		len_PC = len(policy_core)
		len_ML = len(mid_level)
		len_S = len(secondary)

		# Assignment of the resources for the two main types of actions:
		agents.resources_actions_EInfluence = agents.resources_actions * 0.2

		############################################################################################################
		# 1. Blanket framing, grading of actions and implementation of the best actions until resources run out 
		# 100% of the resources (from actions)

		cw_of_interest = []
		# We only consider the causal relations related to the problem on the agenda
		for cw_choice in range(len(policy_core)):
				cw_of_interest.append(len_PC + len_ML + len_S + (agents.select_problem_3S_as - len_PC) + cw_choice * len(mid_level))

		# If the team is advocating for a problem, the following tasks are completed
		if agents.select_issue_3S_as == 'problem':

			# Making sure that there are enough resources
			while agents.resources_actions > 0.001:

				####################################
				# Grading of all the possible actions

				total_agent_grades = []

				# For the causal relations
				for cw in cw_of_interest:
					cw_grade_list = []
					# Going through all active agents
					for agent_inspected in agent_action_list:
						# Going through all of the links
						for links in link_list:
							# Check that only the link of interest is selected
							if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:
								# Make sure to look at the right direction of the conflict level

								cw_grade = ActionFunctions.action_grade_calculator(links, cw, 0, agents, affiliation_weights)
								cw_grade_list.append(cw_grade)

					total_agent_grades.append(sum(cw_grade_list))

				# For the state on the selected issue
				state_grade_list = []
				# Going through all active agents
				for agent_inspected in agent_action_list:
					for links in link_list:
						# Check that only the link of interest is selected
						if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:

							state_grade = ActionFunctions.action_grade_calculator(links, agents.select_problem_3S_as, 0, agents, affiliation_weights)
							state_grade_list.append(state_grade)

				total_agent_grades.append(sum(state_grade_list))

				# For the aim on the selected issue
				aim_grade_list = []
				# Going through all active agents
				for agent_inspected in agent_action_list:
					for links in link_list:
						# Check that only the link of interest is selected
						if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:

							aim_grade = ActionFunctions.action_grade_calculator(links, agents.select_problem_3S_as, 1, agents, affiliation_weights)
							aim_grade_list.append(aim_grade)

				total_agent_grades.append(sum(aim_grade_list))

				####################################
				# Select of the best action

				best_action = total_agent_grades.index(max(total_agent_grades))

				####################################
				# Application of the action selected

				# Going through all active agents
				for agent_inspected in agent_action_list:
					# Going through all of the links
					for links in link_list:
						# Check that only the link of interest is selected
						if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:
							# Make sure to look at the right direction of the conflict levels

							links.aware_decay = 5

							# Implementation of a causal relation blanket action
							if best_action < len(cw_of_interest):
					
								implemented_action = ActionFunctions.action_implementor(links, cw_of_interest[best_action], 0, agents, agents, affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

							# Implementation of a state influence blanket action
							if best_action == len(cw_of_interest):

								implemented_action = ActionFunctions.action_implementor(links, agents.select_problem_3S_as, 0, agents, agents, affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

							# Implementation of a state influence blanket action
							if best_action == len(cw_of_interest) + 1:

								implemented_action = ActionFunctions.action_implementor(links, agents.select_problem_3S_as, 1, agents, agents, affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

				# Updating the resources after each action has been implemented
				agents.resources_actions -= agents.resources[0] * 0.1

		# If the team is advocating for a policy, the following tasks are completed
		if agents.select_issue_3S_as == 'policy':

			# Check the total amount of impacts considered
			impact_number = len(agents.belieftree_policy[0][agents.select_policy_3S_as])

			# Making sure that there are enough resources
			while agents.resources_actions > 0.001:

				####################################
				# Grading of all the possible actions

				total_agent_grades = []

				# For the impacts
				for impact in range(impact_number):
					impact_grade_list = []
					# Going through all active agents
					for agent_inspected in agent_action_list:
						# Going through all of the links
						for links in link_list:
							# Check that only the link of interest is selected
							if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:

								impact_grade = ActionFunctions.action_grade_calculator_3S_AS(links, impact, agents, affiliation_weights, conflict_level_coef)
								total_grade_list.append(impact_grade)

					total_agent_grades.append(sum(impact_grade_list))

				# For the state on the selected issue
				state_grade_list = []
				# Going through all active agents
				for agent_inspected in agent_action_list:
					for links in link_list:
						# Check that only the link of interest is selected
						if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:

							state_grade = ActionFunctions.action_grade_calculator(links, agents.select_problem_3S_as, 0, agents, affiliation_weights)
							state_grade_list.append(state_grade)

				total_agent_grades.append(sum(state_grade_list))

				# For the aim on the selected issue
				aim_grade_list = []
				# Going through all active agents
				for agent_inspected in agent_action_list:
					for links in link_list:
						# Check that only the link of interest is selected
						if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:

							aim_grade = ActionFunctions.action_grade_calculator(links, agents.select_problem_3S_as, 1, agents, affiliation_weights)
							aim_grade_list.append(aim_grade)

				total_agent_grades.append(sum(aim_grade_list))

				####################################
				# Select of the best action

				best_action = total_agent_grades.index(max(total_agent_grades))

				####################################
				# Application of the action selected

				# Going through all active agents
				for agent_inspected in agent_action_list:
					# Going through all of the links
					for links in link_list:
						# Check that only the link of interest is selected
						if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:
							# Make sure to look at the right direction of the conflict levels

							links.aware_decay = 5

							# Implementation of a causal relation blanket action
							if best_action < impact_number:
					
								implemented_action = ActionFunctions.action_implementor_3S_AS(links, agents.select_policy_3S_as, best_action, agents, agents, affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

							# Implementation of a state influence blanket action
							if best_action == impact_number:

								implemented_action = ActionFunctions.action_implementor(links, agents.select_problem_3S_as, 0, agents, agents, affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

							# Implementation of a state influence blanket action
							if best_action == impact_number + 1:

								implemented_action = ActionFunctions.action_implementor(links, agents.select_problem_3S_as, 1, agents, agents, affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

				# Updating the resources after each action has been implemented
				agents.resources_actions -= agents.resources[0] * 0.1

		############################################################################################################
		# 2. Electorate influence, grading of actions and implementation of the best actions until resources run out 
		# 20% of the resources (from actions)
		while agents.resources_actions_EInfluence > 0.001:
			actions_EP_grades_EInfluence = []
			# FIRST - Calculation of the best option
			for issue_num in range(len_PC + len_ML):
				actions_EP_grades_EInfluence_ind = []
				# Going through all agents that are electorate from the master_list
				agents_electorate = []
				for agents_run in master_list:
					if type(agents) == Electorate:
						agents_electorate.append(agents_run)

				for agents_el in agents_electorate:

					# Setting grade to 0 if the external party has no interest in the issue:
					if agents.belieftree[0][issue_num][0] == 'No':
						issue_num_grade	 = 0 

					# Calculate a grade if the external party has an interest in the issue
					else:

						# Memorising the original belief values
						original_belief = [0,0,0]
						original_belief[0] = copy.copy(agents_el.belieftree_electorate[issue_num][0])
						original_belief[1] = copy.copy(agents_el.belieftree_electorate[issue_num][1])
						original_belief[2] = copy.copy(agents_el.belieftree_electorate[issue_num][2])

						if agents.affiliation == agents_el.affiliation:
							# Perfoming the action
							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
								* agents.resources[0] * 0.1 / electorate_number
							# Update of the preference
							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
							# Calculation of the new gradec
							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

						# Affiliation 1 and 2
						if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
							# Perfoming the action
							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
								* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number
							# Update of the preference
							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
							# Calculation of the new gradec
							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

						# Affiliation 1 and 3
						if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
							# Perfoming the action
							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
								* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number
							# Update of the preference
							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
							# Calculation of the new gradec
							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

						# Affiliation 2 and 3
						if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
							# Perfoming the action
							agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
								* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number
							# Update of the preference
							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
							# Calculation of the new grade
							issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

						# Restoring the initial values
						agents_el.belieftree_electorate[issue_num][0] = original_belief[0]
						agents_el.belieftree_electorate[issue_num][1] = original_belief[1]
						agents_el.belieftree_electorate[issue_num][2] = original_belief[2]


						# Re-updating the preference levels
						self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)

					actions_EP_grades_EInfluence_ind.append(issue_num_grade)

				actions_EP_grades_EInfluence.append(sum(actions_EP_grades_EInfluence_ind))

			# Choose the action that leads to the minimum amount of difference between the EP and the electorates
			best_EInfluence = actions_EP_grades_EInfluence.index(min(actions_EP_grades_EInfluence))
			
			# SECOND - Changing the aims of all the agents for the best choice
			for agents_el in agents_electorate:

				if agents.affiliation == agents_el.affiliation:
					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
					* agents.resources[0] * 0.1 / electorate_number

				# Affiliation 1 and 2
				if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
					* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number

					# Affiliation 1 and 3
				if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
					* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number

				# Affiliation 2 and 3
				if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
					agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
					* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number

				# 1-1 check
				agents_el.belieftree_electorate[best_EInfluence][1] = \
					ActionFunctions.one_minus_one_check(agents_el.belieftree_electorate[best_EInfluence][1])

				# Re-updating the preference levels
				self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)

			agents.resources_actions_EInfluence -= agents.resources[0] * 0.1

	def external_parties_actions_pf_3S(self, agents, agent_action_list, causalrelation_number, \
		affiliation_weights, policy_core, mid_level, secondary, electorate_number, action_agent_number, master_list, agenda_prob_3S_as, link_list, conflict_level_coef, resources_weight_action, resources_potency):

		"""
		The external parties actions function - three streams (policy formulation)
		===========================

		This function is used to perform the different active actions of the
		external parties during the policy formulation.

		It is split in two main parts:
		1. All active actions (blanket framing, blanket state influence and 
		blanket aim influence)
		2. Electorate influence - on the aims

		Note: This is the same function as the previous one, however it also 
		considers that the external parties can choose policies and hence adds
		code for the policy related actions.

		Note2: This function is the same as the agenda setting function but adjusted
		for the change of selected issues.

		"""

		len_PC = len(policy_core)
		len_ML = len(mid_level)
		len_S = len(secondary)

		# Assignment of the resources for the two main types of actions:
		agents.resources_actions_EInfluence = agents.resources_actions * 0.2

		############################################################################################################
		# 1. Blanket framing, grading of actions and implementation of the best actions until resources run out 
		# 100% of the resources (from actions)

		# Selection of the cw of interest
		cw_of_interest = []
		# Select one by one the Pr
		j = agenda_prob_3S_as
		# for j in range(len_ML):
		# Selecting the causal relations starting from Pr
		for k in range(len_S):
			# Contingency for partial knowledge issues
			# print(len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML)
			if (agents.belieftree[0][len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML][0] < 0 and (agents.belieftree[0][j][1] - agents.belieftree[0][j][0]) < 0) \
			  or (agents.belieftree[0][len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML][0] > 0 and (agents.belieftree[0][j][1] - agents.belieftree[0][j][0]) > 0):
				cw_of_interest.append(len_PC + len_ML + len_S + len_ML*len_PC + (j-len_PC) + k*len_ML)
		

		# If the team is advocating for a problem, the following tasks are completed
		if agents.select_issue_3S_pf == 'problem':

			# Making sure that there are enough resources
			while agents.resources_actions > 0.001:

				####################################
				# Grading of all the possible actions

				total_agent_grades = []

				# For the causal relations
				for cw in cw_of_interest:
					cw_grade_list = []
					# Going through all active agents
					for agent_inspected in agent_action_list:
						# Going through all of the links
						for links in link_list:
							# Check that only the link of interest is selected
							if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:

								cw_grade = ActionFunctions.action_grade_calculator(links, cw, 0, agents, affiliation_weights)
								cw_grade_list.append(cw_grade)

					total_agent_grades.append(sum(cw_grade_list))

				# For the state on the selected issue
				state_grade_list = []
				# Going through all active agents
				for agent_inspected in agent_action_list:
					for links in link_list:
						# Check that only the link of interest is selected
						if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:

							state_grade = ActionFunctions.action_grade_calculator(links, agents.select_problem_3S_pf, 0, agents, affiliation_weights)
							state_grade_list.append(state_grade)

				total_agent_grades.append(sum(state_grade_list))

				# For the aim on the selected issue
				aim_grade_list = []
				# Going through all active agents
				for agent_inspected in agent_action_list:
					for links in link_list:
						# Check that only the link of interest is selected
						if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:

							aim_grade = ActionFunctions.action_grade_calculator(links, agents.select_problem_3S_pf, 1, agents, affiliation_weights)
							aim_grade_list.append(aim_grade)

				total_agent_grades.append(sum(aim_grade_list))

				####################################
				# Select of the best action

				best_action = total_agent_grades.index(max(total_agent_grades))

				####################################
				# Application of the action selected

				# Going through all active agents
				for agent_inspected in agent_action_list:
					# Going through all of the links
					for links in link_list:
						# Check that only the link of interest is selected
						if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:

							links.aware_decay = 5

							# Implementation of a causal relation blanket action
							if best_action < len(cw_of_interest):
					
								implemented_action = ActionFunctions.action_implementor(links, cw_of_interest[best_action], 0, agents, agents, affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

							# Implementation of a state influence blanket action
							if best_action == len(cw_of_interest):

								implemented_action = ActionFunctions.action_implementor(links, agents.select_problem_3S_pf, 0, agents, agents, affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

							# Implementation of a state influence blanket action
							if best_action == len(cw_of_interest) + 1:
		
								implemented_action = ActionFunctions.action_implementor(links, agents.select_problem_3S_pf, 1, agents, agents, affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

				# Updating the resources after each action has been implemented
				agents.resources_actions -= agents.resources[0] * 0.1

		# If the team is advocating for a policy, the following tasks are completed
		if agents.select_issue_3S_pf == 'policy':

			# Check the total amount of impacts considered
			impact_number = len(agents.belieftree_instrument[0][agents.select_policy_3S_pf])

			# Making sure that there are enough resources
			while agents.resources_actions > 0.001:

				####################################
				# Grading of all the possible actions

				total_agent_grades = []

				# For the impacts
				for impact in range(impact_number):
					impact_grade_list = []
					# Going through all active agents
					for agent_inspected in agent_action_list:
						# Going through all of the links
						for links in link_list:
							# Check that only the link of interest is selected
							if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:

								impact_grade = ActionFunctions.action_grade_calculator_3S_PF(links, impact, agents, affiliation_weights, conflict_level_coef)
								impact_grade_list.append(impact_grade)

					total_agent_grades.append(sum(impact_grade_list))

				# For the state on the selected issue
				state_grade_list = []
				# Going through all active agents
				for agent_inspected in agent_action_list:
					for links in link_list:
						# Check that only the link of interest is selected
						if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:

							state_grade = ActionFunctions.action_grade_calculator(links, agents.select_problem_3S_pf, 0, agents, affiliation_weights)
							state_grade_list.append(state_grade)

				total_agent_grades.append(sum(state_grade_list))

				# For the aim on the selected issue
				aim_grade_list = []
				# Going through all active agents
				for agent_inspected in agent_action_list:
					for links in link_list:
						# Check that only the link of interest is selected
						if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:

							aim_grade = ActionFunctions.action_grade_calculator(links, agents.select_problem_3S_pf, 1, agents, affiliation_weights)
							aim_grade_list.append(aim_grade)

				total_agent_grades.append(sum(aim_grade_list))

				####################################
				# Select of the best action

				best_action = total_agent_grades.index(max(total_agent_grades))

				####################################
				# Application of the action selected

				# Going through all active agents
				for agent_inspected in agent_action_list:
					# Going through all of the links
					for links in link_list:
						# Check that only the link of interest is selected
						if (links.agent1 == agents and links.agent2 == agent_inspected) or (links.agent2 == agents and links.agent1 == agent_inspected) and links.aware > 0:
							# Make sure to look at the right direction of the conflict levels

							links.aware_decay = 5

							# Implementation of a causal relation blanket action
							if best_action < impact_number:
					
								implemented_action = ActionFunctions.action_implementor_3S_PF(links, agents.select_policy_3S_pf, best_action, agents, agents, affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

							# Implementation of a state influence blanket action
							if best_action == impact_number:

								implemented_action = ActionFunctions.action_implementor(links, agents.select_problem_3S_pf, 0, agents, agents, affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

							# Implementation of a state influence blanket action
							if best_action == impact_number + 1:

								implemented_action = ActionFunctions.action_implementor(links, agents.select_problem_3S_pf, 1, agents, agents, affiliation_weights, resources_weight_action, resources_potency, True, action_agent_number)

				# Updating the resources after each action has been implemented
				agents.resources_actions -= agents.resources[0] * 0.1

		############################################################################################################
		# 2. Electorate influence, grading of actions and implementation of the best actions until resources run out 
		# 20% of the resources (from actions)
		while agents.resources_actions_EInfluence > 0.001:
				actions_EP_grades_EInfluence = []
				# FIRST - Calculation of the best option
				for issue_num in range(len_PC + len_ML):
					actions_EP_grades_EInfluence_ind = []
					# Going through all agents that are electorate from the master_list
					agents_electorate = []
					for agents_run in master_list:
						if type(agents) == Electorate:
							agents_electorate.append(agents_run)

					for agents_el in agents_electorate:

						# Setting grade to 0 if the external party has no interest in the issue:
						if agents.belieftree[0][issue_num][0] == 'No':
							issue_num_grade	 = 0 

						# Calculate a grade if the external party has an interest in the issue
						else:

							# Memorising the original belief values
							original_belief = [0,0,0]
							original_belief[0] = copy.copy(agents_el.belieftree_electorate[issue_num][0])
							original_belief[1] = copy.copy(agents_el.belieftree_electorate[issue_num][1])
							original_belief[2] = copy.copy(agents_el.belieftree_electorate[issue_num][2])

							if agents.affiliation == agents_el.affiliation:
								# Perfoming the action
								agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
									* agents.resources[0] * 0.1 / electorate_number
								# Update of the preference
								self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
								# Calculation of the new gradec
								issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

							# Affiliation 1 and 2
							if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
								# Perfoming the action
								agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
									* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number
								# Update of the preference
								self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
								# Calculation of the new gradec
								issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

							# Affiliation 1 and 3
							if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
								# Perfoming the action
								agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
									* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number
								# Update of the preference
								self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
								# Calculation of the new gradec
								issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

							# Affiliation 2 and 3
							if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
								# Perfoming the action
								agents_el.belieftree_electorate[issue_num][1] += (agents.belieftree[0][issue_num][1] - agents_el.belieftree_electorate[issue_num][1]) \
									* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number
								# Update of the preference
								self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)
								# Calculation of the new grade
								issue_num_grade = abs(agents.belieftree[0][issue_num][2] - agents_el.belieftree_electorate[issue_num][2])

							# Restoring the initial values
							agents_el.belieftree_electorate[issue_num][0] = original_belief[0]
							agents_el.belieftree_electorate[issue_num][1] = original_belief[1]
							agents_el.belieftree_electorate[issue_num][2] = original_belief[2]


							# Re-updating the preference levels
							self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)

						actions_EP_grades_EInfluence_ind.append(issue_num_grade)

					actions_EP_grades_EInfluence.append(sum(actions_EP_grades_EInfluence_ind))

				# Choose the action that leads to the minimum amount of difference between the EP and the electorates
				best_EInfluence = actions_EP_grades_EInfluence.index(min(actions_EP_grades_EInfluence))
				
				# SECOND - Changing the aims of all the agents for the best choice
				for agents_el in agents_electorate:

					if agents.affiliation == agents_el.affiliation:
						agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
						* agents.resources[0] * 0.1 / electorate_number

					# Affiliation 1 and 2
					if (agents.affiliation == 0 and agents_el.affiliation == 1) or (agents.affiliation == 1 and agents_el.affiliation == 0):
						agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
						* agents.resources[0] * 0.1 * affiliation_weights[0] / electorate_number

						# Affiliation 1 and 3
					if (agents.affiliation == 0 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 0):
						agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
						* agents.resources[0] * 0.1 * affiliation_weights[1] / electorate_number

					# Affiliation 2 and 3
					if (agents.affiliation == 1 and agents_el.affiliation == 2) or (agents.affiliation == 2 and agents_el.affiliation == 1):
						agents_el.belieftree_electorate[best_EInfluence][1] += (agents.belieftree[0][best_EInfluence][1] - agents_el.belieftree_electorate[best_EInfluence][1]) \
						* agents.resources[0] * 0.1 * affiliation_weights[2] / electorate_number

					# 1-1 check
					agents_el.belieftree_electorate[best_EInfluence][1] = \
						ActionFunctions.one_minus_one_check(agents_el.belieftree_electorate[best_EInfluence][1])

					# Re-updating the preference levels
					self.preference_udapte_electorate(agents_el, len_PC, len_ML, len_S)

				agents.resources_actions_EInfluence -= agents.resources[0] * 0.1

	def preference_udapte_electorate(self, agent, len_PC, len_ML, len_S):

		"""
		Electorate preference update function
		===========================

		This function is used to calculate the preferences of the electorate
		agents. It is the similar to the function used to calculate the preferences
		of the other agents. The main difference is the non inclusion of the 
		causal relations (the electorate tree does not have any). Each preference
		is therefore calculated based on the state and aim for each level
		in the tree.

		The calculation of the policy core, mid-level and secondary issues 
		preferences is performed.c

		"""

		#####
		# Preference calculation for the policy core issues
		Pr_denominator = 0
		for h in range(len_PC):
			Pr_denominator = Pr_denominator + abs(agent.belieftree_electorate[h][1] - agent.belieftree_electorate[h][0])
		for i in range(len_PC):
			# There are rare occasions where the denominator could be 0
			if Pr_denominator != 0:
				agent.belieftree_electorate[i][2] = abs(agent.belieftree_electorate[i][1] - agent.belieftree_electorate[i][0]) / Pr_denominator
			else:
				agent.belieftree_electorate[i][2] = 0

		#####
		# Preference calculation for the mid level issues
		ML_denominator = 0
		for h in range(len_ML):
			ML_denominator = ML_denominator + abs(agent.belieftree_electorate[len_PC + h][1] - agent.belieftree_electorate[len_PC + h][0])
		for i in range(len_ML):
			# There are rare occasions where the denominator could be 0
			if ML_denominator != 0:
				agent.belieftree_electorate[len_PC + i][2] = abs(agent.belieftree_electorate[len_PC + i][1] - agent.belieftree_electorate[len_PC + i][0]) / ML_denominator
			else:
				agent.belieftree_electorate[len_PC + i][2] = 0

		#####
		# Preference calculation for the secondary issues
		S_denominator = 0
		for h in range(len_S):
			S_denominator = S_denominator + abs(agent.belieftree_electorate[len_PC + len_ML + h][1] - agent.belieftree_electorate[len_PC + len_ML + h][0])
		for i in range(len_S):
			# There are rare occasions where the denominator could be 0
			if S_denominator != 0:
				agent.belieftree_electorate[len_PC + len_ML + i][2] = abs(agent.belieftree_electorate[len_PC + len_ML + i][1] - agent.belieftree_electorate[len_PC + len_ML + i][0]) / S_denominator
			else:
				agent.belieftree_electorate[len_PC + len_ML + i][2] = 0
