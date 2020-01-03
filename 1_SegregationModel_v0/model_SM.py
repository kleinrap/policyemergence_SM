from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
import numpy as np
import copy

from collections import defaultdict

from model_SM_agents_initialisation import init_active_agents, init_electorate_agents, init_truth_agent
from model_SM_agents import ActiveAgent, ElectorateAgent, TruthAgent
from model_module_interface import policy_instrument_input, issue_tree_input

# Data collector function

def get_agents_attributes(model):
	
	agent_attributes = []
	for agent in model.schedule.agent_buffer(shuffled=False):
		if isinstance(agent, ActiveAgent):
			_unique_id = agent.unique_id
			# agent_attributes.append([_unique_id, agent.agent_type, agent.affiliation, agent.selected_PC, agent.selected_S, agent.selected_PI, agent.issuetree[_unique_id], agent.policytree[_unique_id]])

			selected_PC = copy.deepcopy(agent.selected_PC)
			selected_S = copy.deepcopy(agent.selected_S)
			selected_PI = copy.deepcopy(agent.selected_PI)
			issuetree = copy.deepcopy(agent.issuetree[_unique_id])

			agent_attributes.append(
				[_unique_id, agent.agent_type, agent.affiliation, selected_PC, selected_S, selected_PI, issuetree])

	return agent_attributes


def get_electorate_attributes(model):
	agent_attributes = []
	for agent in model.schedule.agent_buffer(shuffled=False):
		if isinstance(agent, ElectorateAgent):
			_unique_id = agent.unique_id
			# agent_attributes.append([_unique_id, agent.agent_type, agent.affiliation, agent.selected_PC, agent.selected_S, agent.selected_PI, agent.issuetree[_unique_id], agent.policytree[_unique_id]])

			representativeness = copy.deepcopy(agent.representativeness)
			issuetree = copy.deepcopy(agent.issuetree_elec)

			agent_attributes.append([agent.affiliation, representativeness, issuetree])

	return agent_attributes


def get_problem_policy_chosen(model):

	return [model.agenda_PC, model.policy_implemented_number]

class PolicyEmergenceSM(Model):

	'''
	Simplest Model for the policy emergence model.
	'''

	def __init__(self, SM_inputs, height=20, width=20):

		self.height = height
		self.width = width

		self.SM_inputs = SM_inputs

		self.stepCount = 0
		self.agenda_PC = None
		self.policy_implemented = None
		self.policy_implemented_number = None
		self.policy_formulation_run = False  # True if an agenda is found

		self.w_el_influence = 0.05  # electorate influence weight

		self.schedule = RandomActivation(self)
		self.grid = SingleGrid(height, width, torus=True)

		# creation of the datacollector vector
		self.datacollector = DataCollector(
			# Model-level variables
			model_reporters =  {
				"step": "stepCount",
				"AS_PF": get_problem_policy_chosen,
				"agent_attributes": get_agents_attributes,
				"electorate_attributes": get_electorate_attributes},
			# Agent-level variables
			agent_reporters = {
				"x": lambda a: a.pos[0],
				"y": lambda a: a.pos[1],
				"Agent type": lambda a:type(a), 
				"Issuetree": lambda a: getattr(a, 'issuetree', [None])[a.unique_id if isinstance(a, ActiveAgent) else 0]}
			)

		# "x": lambda a: a.pos[0], "y": lambda a: a.pos[1]
		# "z": lambda a:a.issuetree

		# belief tree properties
		self.len_S, self.len_PC, self.len_DC, self.len_CR = issue_tree_input(self)
		# print(self.len_S, self.len_PC, self.len_DC, self.len_CR)

		# issue tree properties
		self.policy_instruments, self.len_ins, self.PF_indices = policy_instrument_input(self, self.len_PC)

		# Set up active agents
		init_active_agents(self, self.len_S, self.len_PC, self.len_DC, self.len_CR, self.len_PC, self.len_ins, self.SM_inputs)

		# Set up passive agents
		init_electorate_agents(self, self.len_S, self.len_PC, self.len_DC, self.SM_inputs)

		# Set up truth agent
		init_truth_agent(self, self.len_S, self.len_PC, self.len_DC, self.len_ins)
		# the issue tree will need to be updated at a later stage witht he values from the system/policy context

		# print("Schedule has : ", len(self.schedule.agents), " agents.")
		# print(self.schedule.agents)
		# print(" ")

		# for agent in self.schedule.agent_buffer(shuffled=False):
		# 	print(' ')
		# 	print(agent)
		# 	print(type(agent))
		# 	if isinstance(agent, ActiveAgent):
		# 		print(agent.unique_id, " ", agent.pos, " ", agent.agent_type, " ", agent.resources, " ", agent.affiliation, " ", agent.issuetree[agent.unique_id], " ", agent.policytree[agent.unique_id][0])
		# 	if isinstance(agent, ElectorateAgent):
		# 		print(agent.unique_id, " ", agent.pos, " ", agent.affiliation, " ", agent.issuetree)
		# 	if isinstance(agent, TruthAgent):
		# 		print(agent.pos, " ", agent.issuetree)

		self.running = True
		self.numberOfAgents = self.schedule.get_agent_count()
		self.datacollector.collect(self)

	def step(self, KPIs):
		print(" ")
		print("Step +1 - Policy emergence model")
		print("Step count: ", self.stepCount)

		'''
		Main steps of the Simplest Model for policy emergence:
		0. Module interface - Input
			Obtention of the beliefs from the system/policy context
			!! This is to be implemented at a later stage
		1. Agenda setting step
		2. Policy formulation step
		3. Module interface - Output
			Implementation of the policy instrument selected
		'''

		# saving the attributes
		self.KPIs = KPIs

		# 0.
		self.module_interface_input(self.KPIs)
		# electorate influence actions
		self.electorate_influence(self.w_el_influence)

		# for agent in self.schedule.agent_buffer(shuffled=False):
		# 	if isinstance(agent, ActiveAgent) and agent.agent_type == 'policymaker':
		# 		print(' ')
		# 		for issue in range(7):
		# 			print(agent.unique_id, agent.issuetree[agent.unique_id][issue][1])

		# 1.
		self.agenda_setting()

		# 2.
		if self.policy_formulation_run:
			self.policy_formulation()
		else:
			self.policy_implemented = self.policy_instruments[-1]

		# 3.
		# self.module_interface_output()

		# end of step actions:
		# iterate the steps counter
		self.stepCount += 1

		# collect data
		self.datacollector.collect(self)

		print("step ends")
		print(" ")

		# print(self.datacollector.get_agent_vars_dataframe())
		# print(self.datacollector.get_model_vars_dataframe())

		return self.policy_implemented

	def module_interface_input(self, KPIs):

		'''
		The module interface input step consists of actions related to the module interface and the policy emergence model
		'''

		# selection of the Truth agent policy tree and issue tree
		for agent in self.schedule.agent_buffer(shuffled=True):
			if isinstance(agent, TruthAgent):
				truth_policytree = agent.policytree_truth
				for issue in range(self.len_DC+self.len_PC+self.len_S):
					agent.issuetree_truth[issue] = KPIs[issue]
				truth_issuetree = agent.issuetree_truth

		# Transferring policy impact to active agents
		for agent in self.schedule.agent_buffer(shuffled=True):
			if isinstance(agent, ActiveAgent):
				# # replacing the policy family likelihoods
				# for PFj in range(self.len_PC):
				# 	for PFij in range(self.len_PC):
				# 		agent.policytree[agent.unique_id][PFj][PFij] = truth_policytree[PFj][PFij]

				# replacing the policy instruments impacts
				for insj in range(self.len_ins):
					agent.policytree[agent.unique_id][self.len_PC+insj][0:self.len_S] = truth_policytree[self.len_PC+insj]

				# replacing the issue beliefs from the KPIs
				for issue in range(self.len_DC+self.len_PC+self.len_S):
					agent.issuetree[agent.unique_id][issue][0] = truth_issuetree[issue]
				self.preference_update(agent, agent.unique_id)

	def agenda_setting(self):

		'''
		[C1 approach]
		The agenda setting step is the first step in the policy process conceptualised in this model. The steps are given as follows:
		1. Active agents policy core issue selection
		2. Agenda selection
		'''

		# 1. & 2.
		for agent in self.schedule.agent_buffer(shuffled=False):
			if isinstance(agent, ActiveAgent):  # considering only active agents
				agent.selection_PC()
				# print("PC and PF selected for  agent", agent.unique_id, ": ", agent.selected_PC, agent.selected_PF)

		# 2.
		# All active agents considered
		selected_PC_list = []
		number_ActiveAgents = 0
		for agent in self.schedule.agent_buffer(shuffled=False):
			if isinstance(agent, ActiveAgent):  # considering only policy makers
				selected_PC_list.append(agent.selected_PC)
				number_ActiveAgents += 1

		# finding the most common policy core issue and its frequency
		d = defaultdict(int)
		for i in selected_PC_list:
			d[i] += 1
		result = max(d.items(), key=lambda x: x[1])
		agenda_PC_temp = result[0]
		agenda_PC_temp_frequency = result[1]

		# checking for majority
		if agenda_PC_temp_frequency > int(number_ActiveAgents/2):
			self.agenda_PC = agenda_PC_temp
			self.policy_formulation_run = True
			print("The agenda consists of PC", self.agenda_PC, ".")
		else:
			self.policy_formulation_run = False
			print("No agenda was formed, moving to the next step.")

		# for purposes of not changing the entire code - the policy family selected is set at 0 so all policy instruments are always considered in the rest of the model
		self.agenda_PF = 0

	def policy_formulation(self):

		'''
		The policy formulation step is the second step in the policy process conceptualised in this model. The steps are given as follows:
		1. Policy makers individual policy instrument selection
		2. Policy instrument selection for the entire model

		NOTE: THIS CODE DOESNT CONSIDER MAJORITY WHEN MORE THAN THREE POLICY MAKERS ARE INCLUDED, IT CONSIDERS THE MAXIMUM. THIS NEEDS TO BE ADAPTED TO CONSIDER 50% OR MORE!
		'''

		print("Policy formulation starts")

		# todo [PF] -maybe later- missing selection of specific policy instruments
		'''
		Selec the instruments based on the impacts that they have on the policy core problem on the agenda through the secondary problems
		Overall, this means only choose instruments that impact a secondary problem that helps bridge the gap goal beliefs of the agenda problem
		'''

		# 1.
		selected_PI_list = []
		number_PMs = 0
		for agent in self.schedule.agent_buffer(shuffled=False):
			if isinstance(agent, ActiveAgent) and agent.agent_type == 'policymaker':  # considering only policy makers

				# individual agent policy instrument selection
				agent.selection_PI()

				# appending the policy instruments selected to a list for all PMs
				selected_PI_list.append(agent.selected_PI)
				number_PMs += 1


		# finding the most common secondary issue and its frequency
		d = defaultdict(int)
		for i in selected_PI_list:
			d[i] += 1
		result = max(d.items(), key=lambda x: x[1])
		self.policy_implemented_number = result[0]
		policy_implemented_number_frequency = result[1]

		# check for the majority and implemented if satisfied
		if policy_implemented_number_frequency > int(number_PMs/2):
			print("The policy instrument selected is policy instrument ", self.policy_implemented_number, ".")
			self.policy_implemented = self.policy_instruments[self.policy_implemented_number]
		else:
			print("No consensus on a policy instrument.")
			self.policy_implemented = self.policy_instruments[-1] # selecting last policy instrument which is the no instrument policy instrument

	def module_interface_output(self):

		print("Module interface output not introduced yet")

	def preference_update(self, agent, who):

		self.preference_update_DC(agent, who)

		self.preference_update_PC(agent, who)

		self.preference_update_S(agent, who)

	def preference_update_DC(self, agent, who):

		"""
		The preference update function (DC)
		===========================

		This function is used to update the preferences of the deep core issues of agents in their
		respective belief trees.

		agent - this is the owner of the belief tree
		who - this is the part of the belieftree that is considered - agent.unique_id should be used for this - this is done to also include partial knowledge preference calculation

		"""	

		len_DC = self.len_DC
		len_PC = self.len_PC
		len_S = self.len_S

		#####
		# 1.5.1. Preference calculation for the deep core issues

		# 1.5.1.1. Calculation of the denominator
		PC_denominator = 0
		for h in range(len_DC):
			if agent.issuetree[who][h][1] == None or agent.issuetree[who][h][0] == None:
				PC_denominator = 0
			else:
				PC_denominator = PC_denominator + abs(agent.issuetree[who][h][1] - agent.issuetree[who][h][0])
		# print('The denominator is given by: ' + str(PC_denominator))

		# 1.5.1.2. Selection of the numerator and calculation of the preference
		for i in range(len_DC):
			# There are rare occasions where the denominator could be 0
			if PC_denominator != 0:
				agent.issuetree[who][i][2] = abs(agent.issuetree[who][i][1] - agent.issuetree[who][i][0]) / PC_denominator
			else:
				agent.issuetree[who][i][2] = 0

	def preference_update_PC(self, agent, who):

		"""
		The preference update function (PC)
		===========================

		This function is used to update the preferences of the policy core issues of agents in their
		respective belief trees.

		agent - this is the owner of the belief tree
		who - this is the part of the belieftree that is considered - agent.unique_id should be used for this - this is done to also include partial knowledge preference calculation

		"""	

		len_DC = self.len_DC
		len_PC = self.len_PC
		len_S = self.len_S

		#####	
		# 1.5.2 Preference calculation for the policy core issues
		PC_denominator = 0
		# 1.5.2.1. Calculation of the denominator
		for j in range(len_PC):
			# print('Selection PC' + str(j+1))
			# print('State of the PC' + str(j+1) + ': ' + str(agent.issuetree[0][len_DC + j][0])) # the state printed
			# Selecting the causal relations starting from PC
			for k in range(len_DC):
				# Contingency for partial knowledge issues
				if agent.issuetree[who][k][1] == None or agent.issuetree[who][k][0] == None or agent.issuetree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] == None:
					PC_denominator += 0
				else:
					# print('Causal Relation PC' + str(j+1) + ' - PC' + str(k+1) + ': ' + str(agent.issuetree[0][len_DC+len_PC+len_S+j+(k*len_PC)][1]))
					# print('Gap of PC' + str(k+1) + ': ' + str((agent.issuetree[0][k][1] - agent.issuetree[0][k][0])))
					# Check if causal relation and gap are both positive of both negative
					# print('agent.issuetree[' + str(who) + '][' + str(len_DC+len_PC+len_S+j+(k*len_PC)) + '][0]: ' + str(agent.issuetree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0]))
					if (agent.issuetree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] < 0 and (agent.issuetree[who][k][1] - agent.issuetree[who][k][0]) < 0) or (agent.issuetree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] > 0 and (agent.issuetree[who][k][1] - agent.issuetree[who][k][0]) > 0):
						PC_denominator = PC_denominator + abs(agent.issuetree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0]*(agent.issuetree[who][k][1] - agent.issuetree[who][k][0]))
						# print('This is the PC numerator: ' + str(PC_denominator))
					else:
						PC_denominator = PC_denominator	

		# 1.5.2.2. Addition of the gaps of the associated mid-level issues
		for i in range(len_PC):
			# Contingency for partial knowledge issues
			if agent.issuetree[who][len_DC + i][1] == None or agent.issuetree[who][len_DC + i][0] == None:
				PC_denominator = PC_denominator
			else:
				# print('This is the gap for the PC' + str(i+1) + ': ' + str(agent.issuetree[0][len_DC + i][1] - agent.issuetree[0][len_DC + i][0]))
				PC_denominator += abs(agent.issuetree[who][len_DC + i][1] - agent.issuetree[who][len_DC + i][0])
		# print('This is the S denominator: ' + str(PC_denominator))
		
		# 1.5.2.3 Calculation the numerator and the preference
		# Select one by one the PC
		for j in range(len_PC):

			# 1.5.2.3.1. Calculation of the right side of the numerator
			PC_numerator = 0
			# print('Selection PC' + str(j+1))
			# print('State of the PC' + str(j+1) + ': ' + str(agent.issuetree[0][len_DC + j][0])) # the state printed
			# Selecting the causal relations starting from DC
			for k in range(len_DC):
				# Contingency for partial knowledge issues
				if agent.issuetree[who][k][1] == None or agent.issuetree[who][k][0] == None or agent.issuetree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] == None:
					PC_numerator += 0
				else:
					# print('Causal Relation PC' + str(j+1) + ' - DC' + str(k+1) + ': ' + str(agent.issuetree[0][len_DC+len_PC+len_S+j+(k*len_PC)][1]))
					# print('Gap of DC' + str(k+1) + ': ' + str((agent.issuetree[0][k][1] - agent.issuetree[0][k][0])))
					# Check if causal relation and gap are both positive of both negative
					if (agent.issuetree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] < 0 and (agent.issuetree[who][k][1] - agent.issuetree[who][k][0]) < 0) or (agent.issuetree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0] > 0 and (agent.issuetree[who][k][1] - agent.issuetree[who][k][0]) > 0):
						PC_numerator = PC_numerator + abs(agent.issuetree[who][len_DC+len_PC+len_S+j+(k*len_PC)][0]*(agent.issuetree[who][k][1] - agent.issuetree[who][k][0]))
						# print('This is the PC numerator: ' + str(PC_numerator))
					else:
						PC_numerator = PC_numerator	

			# 1.5.2.3.2. Addition of the gap to the numerator
			# Contingency for partial knowledge issues
			if agent.issuetree[who][len_DC + j][1] == None or agent.issuetree[who][len_DC + j][0] == None:
				PC_numerator += 0
			else:
				# print('This is the gap for the PC' + str(j+1) + ': ' + str(agent.issuetree[0][len_DC + j][1] - agent.issuetree[0][len_DC + j][0]))
				PC_numerator += abs(agent.issuetree[who][len_DC + j][1] - agent.issuetree[who][len_DC + j][0])
			# print('The numerator is equal to: ' + str(PC_numerator))
			# print('The denominator is equal to: ' + str(PC_denominator))

			# 1.5.2.3.3. Calculation of the preference
			if PC_denominator != 0:
				agent.issuetree[who][len_DC+j][2] = round(PC_numerator/PC_denominator,3) 
			# print('The new preference of the policy core PC' + str(j+1) + ' is: ' + str(agent.issuetree[0][len_DC+j][2]))
			else:
				agent.issuetree[who][len_DC+j][2] = 0

	def preference_update_S(self, agent, who):

		"""
		The preference update function (S)
		===========================

		This function is used to update the preferences of secondary issues the agents in their
		respective belief trees.

		agent - this is the owner of the belief tree
		who - this is the part of the belieftree that is considered - agent.unique_id should be used for this - this is done to also include partial knowledge preference calculation

		"""	

		len_DC = self.len_DC
		len_PC = self.len_PC
		len_S = self.len_S

		#####	
		# 1.5.3 Preference calculation for the secondary issues
		S_denominator = 0
		# 1.5.2.1. Calculation of the denominator
		for j in range(len_S):
			# print('Selection S' + str(j+1))
			# print('State of the S' + str(j+1) + ': ' + str(agent.issuetree[0][len_DC + len_PC + j][0])) # the state printed
			# Selecting the causal relations starting from S
			for k in range(len_PC):
				# Contingency for partial knowledge issues
				if agent.issuetree[who][len_DC + k][1] == None or agent.issuetree[who][len_DC + k][0] == None or agent.issuetree[who][len_DC+len_PC+len_S+len_DC*len_PC+j+(k*len_S)][0] == None:
					S_denominator += 0
				else:
					# print('Causal Relation S' + str(j+1) + ' - PC' + str(k+1) + ': ' + str(agent.issuetree[who][len_DC+len_PC+len_S+len_DC*len_PC+j+(k*len_S)][0]))
					# print('Gap of PC' + str(k+1) + ': ' + str((agent.issuetree[who][len_DC+k][1] - agent.issuetree[who][len_DC+k][0])))
					# Check if causal relation and gap are both positive of both negative
					# print('agent.issuetree[' + str(who) + '][' + str(len_DC+len_PC+len_S+len_DC*len_PC+j+(k*len_S)) + '][0]: ' + str(agent.issuetree[who][len_DC+len_PC+len_S+len_DC*len_PC+j+(k*len_S)][0]))
					if (agent.issuetree[who][len_DC+len_PC+len_S+len_DC*len_PC+j+(k*len_S)][0] < 0 and (agent.issuetree[who][len_DC+k][1] - agent.issuetree[who][len_DC+k][0]) < 0) or (agent.issuetree[who][len_DC+len_PC+len_S+len_DC*len_PC+j+(k*len_S)][0] > 0 and (agent.issuetree[who][len_DC+k][1] - agent.issuetree[who][len_DC+k][0]) > 0):
						S_denominator += abs(agent.issuetree[who][len_DC+len_PC+len_S+len_DC*len_PC+j+(k*len_S)][0]*(agent.issuetree[who][len_DC+k][1] - agent.issuetree[who][len_DC+k][0]))
						# print('This is the PC numerator: ' + str(S_denominator))
					else:
						S_denominator = S_denominator	

		# 1.5.2.2. Addition of the gaps of the associated secondary issues
		for j in range(len_S):
			# Contingency for partial knowledge issues
			if agent.issuetree[who][len_DC+len_PC+j][1] == None or agent.issuetree[who][len_DC+len_PC+j][0] == None:
				S_denominator = S_denominator
			else:
				# print('This is the gap for the PC' + str(i+1) + ': ' + str(agent.issuetree[0][len_DC + len_PC + i][1] - agent.issuetree[0][len_DC + len_PC + i][0]))
				S_denominator += abs(agent.issuetree[who][len_DC+len_PC+j][1] - agent.issuetree[who][len_DC+len_PC+j][0])
		# print('This is the PC denominator: ' + str(S_denominator))
		
		# 1.5.2.3 Calculation the numerator and the preference
		# Select one by one the S
		for j in range(len_S):

			# 1.5.2.3.1. Calculation of the right side of the numerator
			S_numerator = 0
			# print('Selection S' + str(j+1))
			# print('State of the S' + str(j+1) + ': ' + str(agent.issuetree[who][len_DC + len_PC + j][0])) # the state printed
			# Selecting the causal relations starting from PC
			for k in range(len_PC):
				# Contingency for partial knowledge issues
				if agent.issuetree[who][len_DC + k][1] == None or agent.issuetree[who][len_DC + k][0] == None or agent.issuetree[who][len_DC+len_PC+len_S+len_DC*len_PC+j+(k*len_S)][0] == None:
					S_numerator = 0
				else:
					# print('Causal Relation S' + str(j+1) + ' - PC' + str(k+1) + ': ' + str(agent.issuetree[who][len_DC+len_PC+len_S+len_DC*len_PC+j+(k*len_S)][0]))
					# print('Gap of PC' + str(k+1) + ': ' + str((agent.issuetree[who][len_DC + k][1] - agent.issuetree[who][len_DC + k][0])))
					# Check if causal relation and gap are both positive of both negative
					if (agent.issuetree[who][len_DC+len_PC+len_S+len_DC*len_PC+j+(k*len_S)][0] < 0 and (agent.issuetree[who][len_DC+k][1] - agent.issuetree[who][len_DC+k][0]) < 0) or (agent.issuetree[who][len_DC+len_PC+len_S+len_DC*len_PC+j+(k*len_S)][0] > 0 and (agent.issuetree[who][len_DC+k][1] - agent.issuetree[who][len_DC+k][0]) > 0):
						S_numerator += abs(agent.issuetree[who][len_DC+len_PC+len_S+len_DC*len_PC+j+(k*len_S)][0]*(agent.issuetree[who][len_DC+k][1] - agent.issuetree[who][len_DC+k][0]))
						# print('This is the PC numerator: ' + str(S_numerator))
					else:
						S_numerator = S_numerator

			# 1.5.2.3.2. Addition of the gap to the numerator
			# Contingency for partial knowledge issues
			if agent.issuetree[who][len_DC+len_PC+j][1] == None or agent.issuetree[who][len_DC+len_PC+j][0] == None:
				S_numerator += 0
			else:
				# print('This is the gap for the PC' + str(j+1) + ': ' + str(agent.issuetree[who][len_DC+len_PC+j][1] - agent.issuetree[who][len_DC+len_PC+j][0]))
				S_numerator += abs(agent.issuetree[who][len_DC+len_PC+j][1] - agent.issuetree[who][len_DC+len_PC+j][0])
			# print('The numerator is equal to: ' + str(S_numerator))
			# print('The denominator is equal to: ' + str(S_denominator))

			# 1.5.2.3.3. Calculation of the preference
			if S_denominator != 0:
				agent.issuetree[who][len_DC+len_PC+j][2] = round(S_numerator/S_denominator,3) 
			# print('The new preference of the policy core PC' + str(j+1) + ' is: ' + str(agent.issuetree[0][len_DC+j][2]))
			else:
				agent.issuetree[who][len_DC+len_PC+j][2] = 0

	def electorate_influence(self, w_el_influence):

		'''
		This function calls the influence actions in the electorate agent class

		'''

		for agent in self.schedule.agent_buffer(shuffled=True):
			if isinstance(agent, ElectorateAgent):
				agent.electorate_influence(w_el_influence)