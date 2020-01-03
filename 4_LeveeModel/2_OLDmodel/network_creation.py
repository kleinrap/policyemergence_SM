from mesa import Agent

class PolicyNetworkLinks(Agent):

	def __init__(self, unique_id, agent1, agent2, aware, aware_decay, conflict_level):
		# super().__init__(unique_id, model)

		self.agent1 = agent1
		self.agent2 = agent2
		self.aware = aware
		self.aware_decay = aware_decay
		self.conflict_level = conflict_level
		self.unique_id = unique_id

	# def __str__(self):
	# 	return 'LINK - ' + str(self.unique_id) 

	def __str__(self):
		return 'LINK - ' + str(self.unique_id) + ' with agent1: ' + str(self.agent1) + ', and agent2: ' + str(self.agent2)


	# def __str__(self):
	# 	return 'LINK - ' + str(self.unique_id) + ' with agent1: ' + str(self.agent1) + ', and agent2: ' + str(self.agent2) + ', and aware: ' + str(self.aware)


	def awareness_level_selection(link_list, groups, outsider_agent):

		"""
		The awareness level selection function - three streams shadow network
		===========================

		This function is used to select the agent with the highest awareness level
		and his awareness level with the outsider agent.

		"""

		group_aware = 0
		agent_with_highest_awareness = 0 # uses for the partial knowledge later on

		for agent_check_aware in groups.members:
			for links_check in link_list:
				if outsider_agent == links_check.agent1 and agent_check_aware == links_check.agent2:
					if links_check.aware >= group_aware:
						group_aware = links_check.aware
						agent_with_highest_awareness = links_check.agent2
				if outsider_agent == links_check.agent2 and agent_check_aware == links_check.agent1:
					if links_check.aware >= group_aware:
						group_aware = links_check.aware
						agent_with_highest_awareness = links_check.agent1

		return group_aware, agent_with_highest_awareness


	def conflict_level_value_calculation(issue, conflict_level, conflict_level_coef, checked_value):
		"""
		The conflict level value calculation function - three streams shadow network
		===========================

		This function is standardised to find the value of the conflict level (one of three values specified as code input)

		"""

		if checked_value <= 0.25:
			conflict_level[issue] = conflict_level_coef[0]
		if checked_value > 0.25 and checked_value <= 1.75:
			conflict_level[issue] = conflict_level_coef[2]
		if checked_value > 1.75:
			conflict_level[issue] = conflict_level_coef[1]

		
		return conflict_level[issue]

	def conflict_level_calculation(groups, outsider_agent, conflict_level_coef, conflict_level_option, agent_with_highest_awareness, len_PC, len_ML, len_S):
		"""
		The conflict level calculation function - three streams shadow network
		===========================

		Lorem Ipsum

		"""

		# 0. Array initialisation
		# The conflict level is calculated based on the average of the beliefs of the whole group on the issue for state and aim
		# Set by default to the medium value 
		# (i.e.: [0.75, 0.75 , 0.75, ..., 0.75 ])
		# 	     [Aim , State, Causal relations]
		# First for the aim and the state of the selected issue and then appending all possible causal relations in the belief tree
		conflict_level = [conflict_level_coef[1], conflict_level_coef[1]]
		for p in range(len_PC*len_ML + len_ML*len_S):
			conflict_level.append(conflict_level_coef[1])

		# 1. Aim and state conflict level calculations (only for teams)
		if conflict_level_option == 0 or conflict_level_option == 1:
			state_cf_group_list = []
			aim_cf_group_list = []

			# Calculating the average belief (based on the actual, and not partial, knowledge)
			for agent_cf in groups.members:
				state_cf_group_list.append(agent_cf.belieftree[0][groups.issue][0])
				aim_cf_group_list.append(agent_cf.belieftree[0][groups.issue][1])
			state_cf_group = sum(state_cf_group_list)/len(state_cf_group_list)
			aim_cf_group = sum(aim_cf_group_list)/len(aim_cf_group_list)

			# If the first option has been selected (full knowledge):
			if conflict_level_option == 0:
				# The group as a whole does not have partial knowledge of the other agent's beliefs, therefore the actual belief of 
				# the outsider agent is considered
				state_cf_difference = abs(outsider_agent.belieftree[0][groups.issue][0] - state_cf_group)
				aim_cf_difference = abs(outsider_agent.belieftree[0][groups.issue][1] - aim_cf_group)

		# If the second option has been selected (partial knowledge):
		if conflict_level_option == 1:
			# It is considered that the partial knowledge of the agent with the highest awareness is the most accurate one. It is therefore selected
			# to calculate the difference for the conflict level.
			
			# None checks
			check_none0 = 0
			if agent_with_highest_awareness.belieftree[1 + outsider_agent.unique_id][groups.issue][0] == None:
				agent_with_highest_awareness.belieftree[1 + outsider_agent.unique_id][groups.issue][0] = 0
				check_none0 = 1
			check_none1 = 0
			if agent_with_highest_awareness.belieftree[1 + outsider_agent.unique_id][groups.issue][1] == None:
				agent_with_highest_awareness.belieftree[1 + outsider_agent.unique_id][groups.issue][1] = 0
				check_none1 = 1

			state_cf_difference = abs(agent_with_highest_awareness.belieftree[1 + outsider_agent.unique_id][groups.issue][0] - state_cf_group)
			aim_cf_difference = abs(agent_with_highest_awareness.belieftree[1 + outsider_agent.unique_id][groups.issue][1] - aim_cf_group)

			# None checks
			if check_none0 == 1:
				agent_with_highest_awareness.belieftree[1 + outsider_agent.unique_id][groups.issue][0] = None
			if check_none1 == 1:
				agent_with_highest_awareness.belieftree[1 + outsider_agent.unique_id][groups.issue][1] = None

		# For the coalitions:
		if conflict_level_option == 2:

			# None checks
			check_none0 = 0
			if groups.lead.belieftree[1 + outsider_agent.unique_id][groups.issue][0] == None:
				groups.lead.belieftree[1 + outsider_agent.unique_id][groups.issue][0] = 0
				check_none0 = 1
			check_none1 = 0
			if groups.lead.belieftree[1 + outsider_agent.unique_id][groups.issue][1] == None:
				groups.lead.belieftree[1 + outsider_agent.unique_id][groups.issue][1] = 0
				check_none1 = 1

			# This is entirely dependent on the coalition leader.
			state_cf_difference = abs(agent_with_highest_awareness.belieftree[1 + outsider_agent.unique_id][groups.issue][0] - groups.lead.belieftree[0][groups.issue][0])
			aim_cf_difference = abs(agent_with_highest_awareness.belieftree[1 + outsider_agent.unique_id][groups.issue][1] - groups.lead.belieftree[0][groups.issue][1])

			# None checks
			if check_none0 == 1:
				groups.lead.belieftree[1 + outsider_agent.unique_id][groups.issue][0] = None
			if check_none1 == 1:
				groups.lead.belieftree[1 + outsider_agent.unique_id][groups.issue][1] = None

		# Value of the conflict level
		conflict_level[0] = PolicyNetworkLinks.conflict_level_value_calculation(0, conflict_level, conflict_level_coef, state_cf_difference)
		conflict_level[1] = PolicyNetworkLinks.conflict_level_value_calculation(1, conflict_level, conflict_level_coef, aim_cf_difference)

		# 2. Causal relations conflict level calculations
		cw_average = []
		for p in range(len_PC*len_ML + len_ML*len_S):
			cw_list = []
			for agent_cf in groups.members:
				cw_list.append(agent_cf.belieftree[0][len_PC+len_ML+len_S+p][0])
			cw_average.append(sum(cw_list)/len(cw_list))

		for p in range(len_PC*len_ML + len_ML*len_S):
			if conflict_level_option == 0:
				cw_difference = abs(outsider_agent.belieftree[0][len_PC + len_ML + len_S + p][0] - cw_average[p])
			if conflict_level_option == 1:
				cw_difference = abs(agent_with_highest_awareness.belieftree[1 + outsider_agent.unique_id][len_PC + len_ML + len_S + p][0] - cw_average[p])
			if conflict_level_option == 2:
				cw_difference = abs(groups.lead.belieftree[1 + outsider_agent.unique_id][len_PC + len_ML + len_S + p][0] - groups.lead.belieftree[0][len_PC + len_ML + len_S + p][0])
			
			conflict_level[2+p] = PolicyNetworkLinks.conflict_level_value_calculation(2 + p, conflict_level, conflict_level_coef, cw_difference)

		return conflict_level













