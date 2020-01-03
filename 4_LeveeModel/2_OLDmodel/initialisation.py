import random
import copy

from mesa.space import MultiGrid
from schedule import RandomActivationByBreed
from tree_cell import TreeCell
from datacollection import DataCollector

from agent import Policymakers, Electorate, Externalparties, Truth, Policyentres
from network_creation import PolicyNetworkLinks

def initial_values(inputs_dict, experiment_input, run_number, agent_inputs, AS_theory, PF_theory):

	# Creating the canvas for the forest fire model
	inputs_dict["height"] = 100
	inputs_dict["width"] = 100

	####################################################################################################
	# INITIALISATION of the agents parameters
	####################################################################################################

	# Agents inputs
	affiliation_number = 3 # CURRENTLY THIS NUMBER CANNOT BE CHANGED OR THE CODE WONT WORK
	# affiliation_weights = [0.75, 0.85, 0.95]
	affiliation_weights = [experiment_input[1][run_number], experiment_input[2][run_number], experiment_input[3][run_number]]
	inputs_dict["affiliation_input"] =  [affiliation_number, affiliation_weights]
	
	policymaker_number = agent_inputs[0]
	policyentre_number = 3 * policymaker_number
	externalparties_number = agent_inputs[1]
	electorate_number = affiliation_number
	inputs_dict["total_agent_number"] =  [externalparties_number, policymaker_number, policyentre_number]

	####################################################################################################
	# INITIALISATION of the belief tree

	# Belief tree structure inputs
	inputs_dict["policy_core"] = ["PC1", "PC2"]
	len_PC = len(inputs_dict["policy_core"])
	inputs_dict["mid_level"] = ["ML1", "ML2", "ML3", "ML4"]
	len_ML = len(inputs_dict["mid_level"])
	inputs_dict["secondary"] = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"]
	len_S = len(inputs_dict["secondary"])

	# Inputs for the external parties state selection:
	issues_number = len_PC + len_ML + len_S
	# 1 means that the external party will collect the information, 0 not
	# The number of lists used will depend on the number of external parties used
	# IMPORTANT NOTE - THE CODE IS MADE IN SUCH A WAY THAT ONLY THE SECONDARY ISSUES CAN BE NOT CONSIDERED
	# TO ALSO NOT CONSIDER THE DEEP AND POLICY CORE, SIGNIFICANT CHANGES WILL BE NEEDED IN THE PREFERENCE CALCULATIONS
	no_interest_states = [[1] for i in range(externalparties_number)]
	no_interest_states_empty = [1 for i in range(issues_number)]
	for p in range(externalparties_number):
		no_interest_states[p] = no_interest_states_empty
	# no_interest_states[0] = [1, 1, 1, 1, 1, 0, 1, 1, 1, 0]
	# no_interest_states[1] = [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
	# no_interest_states[2] = [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
	# no_interest_states[3] = [1, 1, 1, 1, 1, 0, 1, 0, 1, 0]
	# no_interest_states[4] = [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
	# no_interest_states[5] = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
	# no_interest_states[6] = [1, 1, 1, 1, 1, 0, 1, 1, 1, 0]
	# no_interest_states[7] = [1, 1, 1, 1, 1, 1, 1, 0, 0, 1]
	# no_interest_states[8] = [1, 1, 1, 1, 1, 0, 0, 1, 0, 1]
	# no_interest_states[9] = [1, 1, 1, 1, 1, 0, 1, 0, 1, 0]
	# no_interest_states[10] = [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
	# no_interest_states[11] = [1, 1, 1, 1, 1, 1, 1, 0, 0, 1]
	inputs_dict["No_interest_states"] = no_interest_states

	####################################################################################################
	# INITIALISATION of the policies and policy instruments

	# NOTICES! - This needs to be changed for the 3S according to the new belief tree
	# Policies inputs (This is only used in the 3S model)
	policies_number = 10
	policies_start = [0 for i in range(len_ML)]
	policies = []
	for k in range(policies_number):
		policies.append(copy.copy(policies_start))
	# policy 1 - More forest size
	policies[0] = [0.5, 0, 0]
	# policy 2 - Less forest size
	policies[1] = [-0.5, 0, 0]
	# policy 3 - More tourism
	policies[2] = [0, 0.5, 0]
	# policy 4 - Less tourism
	policies[3] = [0, -0.5, 0]
	# policy 5 - More safety
	policies[4] = [0, 0, 0.5]
	# policy 6 - Less safety
	policies[5]= [0, 0, -0.5]
	inputs_dict["Policies"] = policies

	instruments = inputs_dict["Instruments"]

	####################################################################################################
	# INITIALISATION of the agents themselves

	# Team strategies
	# This has not yet been coded within the code present here. The different strategies are present in the 
	# formalisation in the report however.
	team_strategy = 1

	# Derived inputs:
	total_agent_number = externalparties_number + policymaker_number + policyentre_number
	# For the truth agents
	belieftree_truth = [None for i in range(issues_number)]
	# For the electorate
	belieftree_electorate = [None for i in range(issues_number)]
	# For all other agents
	causalrelation_number = len_PC*len_ML + len_ML*len_S
	belieftree = [[None] for i in range(len_PC + len_ML + len_S + causalrelation_number)]
	for i in range(len(belieftree)):
		# STATE - AIM - PREFERENCE for the issues and None - VALUE - NONE for the causal relations
		belieftree[i] = [[None, None, None] for i in range(len_PC + len_ML + len_S + causalrelation_number)]

	# Each of the active agent is assigned a unique ID
	unique_id = 0

	inputs_dict["Agents"] = []

	############################
	# Creation of the truth agent
	x = random.randrange(inputs_dict["width"])
	y = random.randrange(inputs_dict["height"])
	# print('Truth agent beliefs: ' + str(self.belieftree_truth))
	truthagent = Truth((x, y), belieftree_truth)
	# master_list.append(truthagent)
	inputs_dict["Agents"].append(truthagent)

	############################
	# Creation of the electorate

	# inputs_dict["representation"] = [0.2, 0.5, 0.3]

	inputs_dict["electorate_influence_coefficient"] = experiment_input[6][run_number]
	
	inputs_dict["representation"] = [experiment_input[4][run_number]/100, (1 - (experiment_input[4][run_number]/100))/2, (1 - (experiment_input[4][run_number]/100))/2]

	if sum(inputs_dict["representation"]) != 1 or len(inputs_dict["representation"]) != affiliation_number:
		print('WARNING! - There is a problem in the electorate representation calculation')

	for i in range(electorate_number):
		x = random.randrange(inputs_dict["width"])
		y = random.randrange(inputs_dict["height"])

		belieftree_electorate = [[None, 0, None] for p in range(issues_number)] # self.belieftree_electorate
		affiliation = i

		# Creating the initial values for the belief tree per affiliation - Self aims
		if affiliation == 0:

			# This is where the modeller inputs the values for the belief tree of the actors with affiliation 0
			belieftree_electorate_PC = [0.6, 0.7]
			belieftree_electorate_ML = [0.5, 0.5, 0.75, 0.75]
			belieftree_electorate_S = [0, 0, 0.75, -0.75, 0.5, 0.5, 0, 0]
			
		if affiliation == 1:

			# This is where the modeller inputs the values for the belief tree of the actors with affiliation 0
			belieftree_electorate_PC = [0.6, 0.7]
			belieftree_electorate_ML = [0.5, 0.5, 0.75, 0.75]
			belieftree_electorate_S = [0, 0, 0.75, -0.75, 0.5, 0.5, 0, 0]

		if affiliation == 2:

			# This is where the modeller inputs the values for the belief tree of the actors with affiliation 0
			belieftree_electorate_PC = [-0.2, 0.9]
			belieftree_electorate_ML = [-0.2, -0.2, 0.1, 0.1]
			belieftree_electorate_S = [0, 0, 0, 0, 0, 0, 0, 0.7, 0, 0]

		# Assembly
		belieftree_electorate_temp = belieftree_electorate_PC
		belieftree_electorate_temp.extend(belieftree_electorate_ML)
		belieftree_electorate_temp.extend(belieftree_electorate_S)

		# Replacing the main beliefs in the belief tree
		for ip in range(len_PC+len_ML+len_S):
				belieftree_electorate[ip][1] = belieftree_electorate_temp[i]

		# Randomises lightly the input value
		for j in range(len(belieftree_electorate)):
			belieftree_electorate[j][1] = round(belieftree_electorate[j][1] + (random.random()/10) - 0.05, 5)
			belieftree_electorate[j][1] = one_minus_one_check(belieftree_electorate[j][1])

		electorate = Electorate(run_number, (x, y), affiliation, belieftree_electorate, inputs_dict["representation"][i])
		# master_list.append(electorate)
		inputs_dict["Agents"].append(electorate)

	############################
	# Creation of the external parties

	# To get same affiliation each time:
	affiliation_list = []
	if externalparties_number == 6:
		affiliation_list = [0, 1, 2, 0, 1, 2]
	else:
		random.seed(1)
		for i in range(externalparties_number):
			affiliation_list.append(random.randrange(affiliation_number))
		random.seed()
	
	for i in range(externalparties_number):
		x = random.randrange(inputs_dict["width"])
		y = random.randrange(inputs_dict["height"])
		agent_id = i
		
		affiliation = affiliation_list[i]

		# Creation of the total belief tree (number of agents + 1)
		belieftree = [None]

		# Creation of the first part of the own belief tree containing the issues
		belieftree_empty_issues = [[None, 0, 0] for f in range(len_PC + len_ML + len_S)]
		belieftree_full = belieftree_empty_issues
		# Addition at the end of the own belief tree for the causal relation beliefs
		for p in range(causalrelation_number):
			belieftree_full.append([0])

		# Placement of the own belief tree in the total belief tree as the first spot.
		belieftree[0] = belieftree_full
		# Creation of the simplified agent tree for other agents (partial knowledge part)
		# Addition of the simplified agent tree after the first spot in the total belief tree
		for r in range(total_agent_number):
			belieftree_empty_agents = [[None, None, None] for p in range(len_PC + len_ML + len_S)]
			for l in range(causalrelation_number):
				belieftree_empty_agents.append([None])
			belieftree.append(belieftree_empty_agents)

		# Creation of the policy belief tree
		belieftree_policy_structure1 = [None for f in range(len_ML)]
		belieftree_policy = []
		for ij in range(total_agent_number + 1):
			belieftree_policy_structure2 = []
			for pk in range(len(policies)):
				belieftree_policy_structure2.append(copy.copy(belieftree_policy_structure1))
			belieftree_policy.append(copy.copy(belieftree_policy_structure2))

		# Creation of the instrument belief tree
		belieftree_instrument_structure1 = [None for f in range(len_S)]
		belieftree_instrument = []
		for ij in range(total_agent_number + 1):
			belieftree_instrument_structure2 = []
			for pk in range(len(instruments)):
				belieftree_instrument_structure2.append(copy.copy(belieftree_instrument_structure1))
			belieftree_instrument.append(copy.copy(belieftree_instrument_structure2))

		# The line below can be used in case one wants to run different set of profiles per experiment
		# if experiment_input[0][run_number] == 1:

		# Creation of the belieftrees
		belieftree, belieftree_policy, belieftree_instrument = belieftree_profiles(belieftree, belieftree_policy, belieftree_instrument, affiliation, len_PC, len_ML, len_S, causalrelation_number, policies, instruments)
		resources = [0, 0] # Initial resources, current resources
		# print('   ')
		# print('Original Belief Tree: ')
		# print(belieftree)
		if affiliation == 0:
			network_strategy = 2
		if affiliation == 1 or affiliation == 2:
			network_strategy = 1
		select_as_issue = None
		select_pinstrument = None
		select_issue_3S_as = None
		select_problem_3S_as = None
		select_policy_3S_as = None
		select_issue_3S_pf = None
		select_problem_3S_pf = None
		select_policy_3S_pf = None
		# The creation of the instrument preference array includes the presence of other agents (partial knowledge)
		instrument_preferences_base = [0 for h in range(len(instruments))]
		instrument_preferences = [instrument_preferences_base]
		for _ in range(total_agent_number):
			instrument_preferences.append(copy.copy(instrument_preferences_base))
		# team_strategy 0 is all agents, 1 is minimum amount of agents
		team = [None, None, team_strategy] # starting with no team (as and pf)
		coalition = [None, None]
		externalparty = Externalparties(run_number, agent_id, unique_id, (x, y), network_strategy, affiliation, resources, \
			belieftree, instrument_preferences, belieftree_policy, belieftree_instrument, select_as_issue, select_pinstrument, \
			select_issue_3S_as, select_problem_3S_as, select_policy_3S_as, select_issue_3S_pf, select_problem_3S_pf, select_policy_3S_pf, team, copy.copy(team), coalition, copy.copy(coalition))
		# print(externalparty.unique_id)
		unique_id += 1
		# print('These are the resources of this external party: ' + str(externalparty.resources))
		# master_list.append(externalparty)
		# agent_action_list.append(externalparty)
		inputs_dict["Agents"].append(externalparty)

	############################
	# Creation of the policy makers

	# To get same affiliation each time:
	affiliation_list = []
	if policymaker_number == 6:
		affiliation_list = [0, 1, 2, 0, 1, 2]
	else:
		random.seed(1)
		for i in range(policymaker_number):
			affiliation_list.append(random.randrange(affiliation_number))
		random.seed()
	
	for i in range(policymaker_number):
		agent_id = i
		x = random.randrange(inputs_dict["width"])
		y = random.randrange(inputs_dict["height"])
		affiliation = affiliation_list[i]

		# Belief tree:
		belieftree = [None]
		belieftree_empty_issues = [[0, 0, 0] for f in range(len_PC + len_ML + len_S)]
		belieftree_full = belieftree_empty_issues
		for p in range(causalrelation_number):
			belieftree_full.append([0])
		belieftree[0] = belieftree_full
		for r in range(total_agent_number):
			belieftree_empty_agents = [[None, None, None] for p in range(len_PC + len_ML + len_S)]
			for l in range(causalrelation_number):
				belieftree_empty_agents.append([None])
			belieftree.append(belieftree_empty_agents)

		# Creation of the policy belief tree
		belieftree_policy_structure1 = [None for f in range(len_ML)]
		belieftree_policy = []
		for ij in range(total_agent_number + 1):
			belieftree_policy_structure2 = []
			for pk in range(len(policies)):
				belieftree_policy_structure2.append(copy.copy(belieftree_policy_structure1))
			belieftree_policy.append(copy.copy(belieftree_policy_structure2))

		# Creation of the instrument belief tree
		belieftree_instrument_structure1 = [None for f in range(len_S)]
		belieftree_instrument = []
		for ij in range(total_agent_number + 1):
			belieftree_instrument_structure2 = []
			for pk in range(len(instruments)):
				belieftree_instrument_structure2.append(copy.copy(belieftree_instrument_structure1))
			belieftree_instrument.append(copy.copy(belieftree_instrument_structure2))
		# print('Instruments: ' + str(belieftree_instrument))

		# Creating the initial values for the belief tree per affiliation
		# Aims of the actor itself:
		# This is the case where the agents from:
		# affiliation 1 will have high aim beleif
		# affiliation 2 will have low aim beliefs (opposite)
		# affiliation 3 will have mild aim beleifs (random)
		# if experiment_input[0][run_number] == 1:

		# Creation of the belieftrees
		belieftree, belieftree_policy, belieftree_instrument = belieftree_profiles(belieftree, belieftree_policy, belieftree_instrument, affiliation, len_PC, len_ML, len_S, causalrelation_number, policies, instruments)

		# print(' ')
		# print(belieftree[0])
		if affiliation == 0:
			network_strategy = 2
		if affiliation == 1 or affiliation == 2:
			network_strategy = 1
		resources = [0, 0] # Initial resources, current resources
		select_as_issue = None
		select_pinstrument = None
		select_issue_3S_as = None
		select_problem_3S_as = None
		select_policy_3S_as = None
		select_issue_3S_pf = None
		select_problem_3S_pf = None
		select_policy_3S_pf = None
		# The creation of the instrument preference array includes the presence of other agents (partial knowledge)
		instrument_preferences_base = [0 for h in range(len(instruments))]
		instrument_preferences = [instrument_preferences_base]
		for _ in range(total_agent_number):
			instrument_preferences.append(copy.copy(instrument_preferences_base))
		# team_strategy 0 is all agents, 1 is minimum amount of agents
		team = [None, None, team_strategy] # starting with no team (as and pf)
		coalition = [None, None]
		policymaker = Policymakers(run_number, agent_id, unique_id, (x, y), network_strategy,  affiliation, resources, belieftree, \
		 instrument_preferences, belieftree_policy, belieftree_instrument ,select_as_issue, select_pinstrument, \
		 select_issue_3S_as, select_problem_3S_as, select_policy_3S_as, select_issue_3S_pf, select_problem_3S_pf, select_policy_3S_pf, team, copy.copy(team), coalition, copy.copy(coalition))
		unique_id += 1
		# master_list.append(policymaker)
		# agent_action_list.append(policymaker)
		inputs_dict["Agents"].append(policymaker)

	############################
	# Creation of the policy entrepreneurs

	# To get same affiliation each time:
	affiliation_list = []
	if policyentre_number == 18:
		affiliation_list = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]
	else:
		random.seed(1)
		for i in range(policyentre_number):
			affiliation_list.append(random.randrange(affiliation_number))
		random.seed()
	
	for i in range(policyentre_number):
		x = random.randrange(inputs_dict["width"])
		y = random.randrange(inputs_dict["height"])
		affiliation = affiliation_list[i]
		agent_id = i
		# Belief tree:
		belieftree = [None]
		belieftree_empty_issues = [[0, 0, 0] for f in range(len_PC + len_ML + len_S)]
		belieftree_full = belieftree_empty_issues
		for p in range(causalrelation_number):
			belieftree_full.append([0])
		belieftree[0] = belieftree_full
		for r in range(total_agent_number):
			belieftree_empty_agents = [[None, None, None] for p in range(len_PC + len_ML + len_S)]
			for l in range(causalrelation_number):
				belieftree_empty_agents.append([None])
			belieftree.append(belieftree_empty_agents)

		# Creation of the policy belief tree
		belieftree_policy_structure1 = [None for f in range(len_ML)]
		belieftree_policy = []
		for ij in range(total_agent_number + 1):
			belieftree_policy_structure2 = []
			for pk in range(len(policies)):
				belieftree_policy_structure2.append(copy.copy(belieftree_policy_structure1))
			belieftree_policy.append(copy.copy(belieftree_policy_structure2))

		# Creation of the instrument belief tree
		belieftree_instrument_structure1 = [None for f in range(len_S)]
		belieftree_instrument = []
		for ij in range(total_agent_number + 1):
			belieftree_instrument_structure2 = []
			for pk in range(len(instruments)):
				belieftree_instrument_structure2.append(copy.copy(belieftree_instrument_structure1))
			belieftree_instrument.append(copy.copy(belieftree_instrument_structure2))
		# print('Instruments: ' + str(belieftree_instrument))

		# Creating the initial values for the belief tree per affiliation
		# This is the case where the agents from:
		# affiliation 1 will have high aim beleif
		# affiliation 2 will have low aim beliefs (opposite)
		# affiliation 3 will have mild aim beleifs (random)

		# if experiment_input[0][run_number] == 1:
		
		# Creation of the belieftrees
		belieftree, belieftree_policy, belieftree_instrument = belieftree_profiles(belieftree, belieftree_policy, belieftree_instrument, affiliation, len_PC, len_ML, len_S, causalrelation_number, policies, instruments)

		resources = [0, 0] # Initial resources, current resources
		if affiliation == 0:
			network_strategy = 2
		if affiliation == 1 or affiliation == 2:
			network_strategy = 1
		select_as_issue = None
		select_pinstrument = None
		select_issue_3S_as = None
		select_problem_3S_as = None
		select_policy_3S_as = None
		select_issue_3S_pf = None
		select_problem_3S_pf = None
		select_policy_3S_pf = None
		# The creation of the instrument preference array includes the presence of other agents (partial knowledge)
		instrument_preferences_base = [0 for h in range(len(instruments))]
		instrument_preferences = [instrument_preferences_base]
		for _ in range( total_agent_number):
			instrument_preferences.append(copy.copy(instrument_preferences_base))
		# team_strategy 0 is all agents, 1 is minimum amount of agents
		team = [None, None, team_strategy] # starting with no team (as and pf)
		coalition = [None, None]
		policyentre = Policyentres(run_number, agent_id, unique_id, (x, y), network_strategy, affiliation, resources, belieftree, \
		 instrument_preferences, belieftree_policy, belieftree_instrument, select_as_issue, select_pinstrument, \
		 select_issue_3S_as, select_problem_3S_as, select_policy_3S_as, select_issue_3S_pf, select_problem_3S_pf, select_policy_3S_pf, team, copy.copy(team), coalition, copy.copy(coalition))
		# print('These are the resources of this policy entrepreneur: ' + str(policyentre.resources))
		unique_id += 1
		# master_list.append(policyentre)
		# agent_action_list.append(policyentre)
		inputs_dict["Agents"].append(policyentre)

	####################################################################################################
	# INITIALISATION of the backbone parameters
	####################################################################################################

	# Parameters for the agents arguments on the agenda for the 3S and B/B+
	agenda_as_issue = None
	agenda_instrument = None
	agenda_prob_3S = None
	agenda_poli_3S = None
	inputs_dict["Agenda_inputs"] = [agenda_as_issue, agenda_instrument, agenda_prob_3S, agenda_poli_3S]

	# Parameter related to the resource potency
	if experiment_input[7][run_number] != False:
		inputs_dict["resources_potency"] = experiment_input[7][run_number]
	else:
		inputs_dict["resources_potency"] = 1

	# Parameter related to the amount of resources used for each action performed
	if experiment_input[8][run_number] != False:
		inputs_dict["resources_weight_action"] = experiment_input[8][run_number]
	else:
		inputs_dict["resources_weight_action"] = 0.1

	# Parameter related to the coefficients used for the different conflict levels
	if experiment_input[10][run_number] != False and experiment_input[11][run_number] != False and experiment_input[12][run_number] != False:
		inputs_dict["conflict_level_coef"] = [experiment_input[10][run_number], experiment_input[11][run_number], experiment_input[12][run_number]]
	else:
		inputs_dict["conflict_level_coef"] = [0.75, 0.85, 0.95]

	####################################################################################################
	# INITIALISATION of the backbone+ parameters
	####################################################################################################

	# ############################
	# # Creation of the network
	# This is the actual creation of the network.
	random.seed(1)
	inputs_dict["Link_list"] = []
	agent_action_list = []
	for agents in inputs_dict["Agents"]:
		if type(agents) == Policymakers or type(agents) == Policyentres or type(agents) == Externalparties:
			# print(agents)
			agent_action_list.append(agents)

	# print('')

	if experiment_input[9][run_number] != False:
		inputs_dict["Trust_decay_coefficient"] = experiment_input[9][run_number]
	else:
		inputs_dict["Trust_decay_coefficient"] = 0.05


	conflict_level_1 = [[inputs_dict["conflict_level_coef"][1], inputs_dict["conflict_level_coef"][1]] for i in range(len_PC + len_ML + len_S + len_PC*len_ML + len_ML*len_S)]
	conflict_level_2 = [[inputs_dict["conflict_level_coef"][1], inputs_dict["conflict_level_coef"][1]] for i in range(len_PC + len_ML + len_S + len_PC*len_ML + len_ML*len_S)]
	conflict_level = [conflict_level_1, conflict_level_2]
	# print('*************')
	# print('This is the conflict level')
	# print(conflict_level)
	# print('*************')
	link_id = 0
	nw_test = 1
	for i in range(len(agent_action_list)):
		for j in range(len(agent_action_list) - nw_test):
			# print('(' + str(i) + ',' + str(j + nw_test) + ')')
			# Defining the aware level
			aware_check = random.random()
			if aware_check < 0.1 and (type(agent_action_list[i]) != Policymakers and type(agent_action_list[j + nw_test]) != Policymakers):
				aware = -1
			if aware_check < 0.5 and aware_check >= 0.1:
				aware = 0
			if aware_check >= 0.5:
				aware = random.random()

			policynetworklink = PolicyNetworkLinks(link_id, agent_action_list[i], agent_action_list[j + nw_test], aware, inputs_dict["Trust_decay_coefficient"], conflict_level)
			inputs_dict["Link_list"].append(policynetworklink)
			# link_list.append(policynetworklink)
			# print(policynetworklink)
			link_id += 1
		nw_test += 1
	# print(link_list)
	# print(len(self.link_list[PolicyNetworkLinks]))

	conflict_level_update(inputs_dict["Link_list"], len_PC, len_ML, len_S, inputs_dict["conflict_level_coef"])

	# print(' ')
	# print(inputs_dict)
	# print(' ')

	# Restore randomness
	random.seed()

	####################################################################################################
	# INITIALISATION of the three streams parameters
	####################################################################################################

	# Parameter related to the gap required within an agent's belief to create or join a team
	if experiment_input[13][run_number] != False:
		inputs_dict["team_gap_threshold"] = experiment_input[13][run_number]
	else:
		inputs_dict["team_gap_threshold"] = 0.8

	# Parameter related to the belief similarity that is required for the problem to join
	# or create a team
	if experiment_input[14][run_number] != False:
		inputs_dict["team_belief_problem_threshold"] = experiment_input[14][run_number]
	else:
		inputs_dict["team_belief_problem_threshold"] = 0.5

	# Parameter related to the belief similarity that is required for the policy to join
	# or create a team
	if experiment_input[15][run_number] != False:
		inputs_dict["team_belief_policy_threshold"] = experiment_input[15][run_number]
	else:
		inputs_dict["team_belief_policy_threshold"] = 0.5

	####################################################################################################
	# INITIALISATION of the ACF parameters
	####################################################################################################

	# Parameter related to the threshold to create a new coalition
	if experiment_input[16][run_number] != False:
		inputs_dict["coalition_threshold"] = experiment_input[16][run_number]
	else:
		inputs_dict["coalition_threshold"] = 0.35

	return inputs_dict

def belieftree_profiles(belieftree, belieftree_policy, belieftree_instrument, affiliation, len_PC, len_ML, len_S, causalrelation_number, policies, instruments):

	# Creating the initial values for the belief tree per affiliation - Self aims
	if affiliation == 0:

		# This is where the modeller inputs the values for the belief tree of the actors with affiliation 0
		input_belieftree_PC = [0.6, 0.7]
		input_belieftree_ML = [0.5, 0.5, 0.75, 0.75]
		input_belieftree_S = [0, 0, 0, 0, 0, 0, 0, 0.7, 0, 0]
		input_belieftree_CR_PC = [0, 0, 0.75, -0.75, 0.5, 0.5, 0, 0]
		input_belieftree_CR_ML1 = [-0.5, 0, 0, 0.4, 0, -0.4, 0.7, 0.3, 0.9, 0]
		input_belieftree_CR_ML2 = [-0.5, 0, 0, 0.4, 0, -0.4, 0.7, 0.3, 0.9, 0]
		input_belieftree_CR_ML3 = [-0.9, 0, 0.8, 0.4, 0.9, 0.5, 0, 0.5, 0.3, -0.4]
		input_belieftree_CR_ML4 = [0, -0.9, 0.4, 0.1, 0.9, -0.5, 0, 0.3, -0.2, -0.1]

		# Policies belief tree
		# NOTICE! - Needs changing for the new belieftree
		belieftree_policy[0][0] = [0, 0, 0, 0]
		belieftree_policy[0][1] = [0, 0, 0, 0]
		belieftree_policy[0][2] = [0, 0, 0, 0]
		belieftree_policy[0][3] = [0, 0, 0, 0]
		belieftree_policy[0][4] = [0, 0, 0, 0]
		belieftree_policy[0][5] = [0, 0, 0, 0]
		belieftree_policy[0][6] = [0, 0, 0, 0]
		belieftree_policy[0][7] = [0, 0, 0, 0]
		belieftree_policy[0][8] = [0, 0, 0, 0]
		belieftree_policy[0][9] = [0, 0, 0, 0]

		# Instruments belief tree
		# NOTICE! - These have not yet been initiated
		belieftree_instrument[0][0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][1] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][2] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][3] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][4] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][5] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][6] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][7] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][8] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][9] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][10] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][11] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][12] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][13] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][14] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][15] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	if affiliation == 1:
		
		# This is where the modeller inputs the values for the belief tree of the actors with affiliation 1
		input_belieftree_PC = [0.6, 0.7]
		input_belieftree_ML = [0.5, 0.5, 0.75, 0.75]
		input_belieftree_S = [0, 0, 0, 0, 0, 0, 0, 0.7, 0, 0]
		input_belieftree_CR_PC = [0, 0, 0.75, -0.75, 0.5, 0.5, 0, 0]
		input_belieftree_CR_ML1 = [-0.5, 0, 0, 0.4, 0, -0.4, 0.7, 0.3, 0.9, 0]
		input_belieftree_CR_ML2 = [-0.5, 0, 0, 0.4, 0, -0.4, 0.7, 0.3, 0.9, 0]
		input_belieftree_CR_ML3 = [-0.9, 0, 0.8, 0.4, 0.9, 0.5, 0, 0.5, 0.3, -0.4]
		input_belieftree_CR_ML4 = [0, -0.9, 0.4, 0.1, 0.9, -0.5, 0, 0.3, -0.2, -0.1]

		# Policies belief tree
		# NOTICE! - These have not yet been initiated
		belieftree_policy[0][0] = [0, 0, 0, 0]
		belieftree_policy[0][1] = [0, 0, 0, 0]
		belieftree_policy[0][2] = [0, 0, 0, 0]
		belieftree_policy[0][3] = [0, 0, 0, 0]
		belieftree_policy[0][4] = [0, 0, 0, 0]
		belieftree_policy[0][5] = [0, 0, 0, 0]
		belieftree_policy[0][6] = [0, 0, 0, 0]
		belieftree_policy[0][7] = [0, 0, 0, 0]
		belieftree_policy[0][8] = [0, 0, 0, 0]
		belieftree_policy[0][9] = [0, 0, 0, 0]

		# Instruments belief tree
		# NOTICE! - These have not yet been initiated
		belieftree_instrument[0][0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][1] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][2] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][3] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][4] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][5] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][6] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][7] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][8] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][9] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][10] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][11] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][12] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][13] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][14] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][15] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		
	if affiliation == 2:
		
		# This is where the modeller inputs the values for the belief tree of the actors with affiliation 2
		input_belieftree_PC = [-0.2, 0.9]
		input_belieftree_ML = [-0.2, -0.2, 0.1, 0.1]
		input_belieftree_S = [0, 0, 0, 0, 0, 0, 0, 0.7, 0, 0]
		input_belieftree_CR_PC = [0, 0, 0.75, -0.75, 0.5, 0.5, 0, 0]
		input_belieftree_CR_ML1 = [-0.5, 0, 0, 0.4, 0, -0.4, 0.7, 0.3, 0.9, 0]
		input_belieftree_CR_ML2 = [-0.5, 0, 0, 0.4, 0, -0.4, 0.7, 0.3, 0.9, 0]
		input_belieftree_CR_ML3 = [-0.9, 0, 0.8, 0.4, 0.9, 0.5, 0, 0.5, 0.3, -0.4]
		input_belieftree_CR_ML4 = [0, -0.9, 0.4, 0.1, 0.9, -0.5, 0, 0.3, -0.2, -0.1]

		# Policies belief tree
		# NOTICE! - These have not yet been initiated
		belieftree_policy[0][0] = [0, 0, 0, 0]
		belieftree_policy[0][1] = [0, 0, 0, 0]
		belieftree_policy[0][2] = [0, 0, 0, 0]
		belieftree_policy[0][3] = [0, 0, 0, 0]
		belieftree_policy[0][4] = [0, 0, 0, 0]
		belieftree_policy[0][5] = [0, 0, 0, 0]
		belieftree_policy[0][6] = [0, 0, 0, 0]
		belieftree_policy[0][7] = [0, 0, 0, 0]
		belieftree_policy[0][8] = [0, 0, 0, 0]
		belieftree_policy[0][9] = [0, 0, 0, 0]

		# Instruments belief tree
		# NOTICE! - These have not yet been initiated
		belieftree_instrument[0][0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][1] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][2] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][3] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][4] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][5] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][6] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][7] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][8] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][9] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][10] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][11] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][12] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][13] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][14] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		belieftree_instrument[0][15] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	# Assembly
	input_belieftree = input_belieftree_PC
	input_belieftree.extend(input_belieftree_ML)
	input_belieftree.extend(input_belieftree_S)
	input_belieftree.extend(input_belieftree_CR_PC)
	input_belieftree.extend(input_belieftree_CR_ML1)
	input_belieftree.extend(input_belieftree_CR_ML2)
	input_belieftree.extend(input_belieftree_CR_ML3)
	input_belieftree.extend(input_belieftree_CR_ML4)

	# Replacing the main beliefs in the belief tree
	for i in range(len_PC+len_ML+len_S+causalrelation_number):
		# For the issue
		if i < len_PC+len_ML+len_S:
			belieftree[0][i][1] = input_belieftree[i]
		# For the causal relations
		else:
			belieftree[0][i][0] = input_belieftree[i]

	# Randomising the belief tree
	for j in range(len_PC + len_ML + len_S):
		belieftree[0][j][1] = round(belieftree[0][j][1] + (random.random()/10) - 0.05, 5)
		belieftree[0][j][1] = one_minus_one_check(belieftree[0][j][1])
		# NOTICE THIS! - Below does not currently work as it is case based (3S)

	# Randomising the causal relations
	for q in range(causalrelation_number):
		belieftree[0][q + len_PC + len_ML + len_S][0] = round(belieftree[0][q + len_PC + len_ML + len_S][0] + (random.random()/10) - 0.05, 5)
		belieftree[0][q + len_PC + len_ML + len_S][0] = one_minus_one_check(belieftree[0][q + len_PC + len_ML + len_S][0])
	# Randomising the policy tree
	for q in range(len(policies)):
		for p in range(len_ML):
			belieftree_policy[0][q][p] = belieftree_policy[0][q][p] + (random.random()/10) - 0.05
			belieftree_policy[0][q][p] = one_minus_one_check(belieftree_policy[0][q][p])
	# Randomising the instrument tree
	for q in range(len(instruments)):
		for p in range(len_S):
			belieftree_instrument[0][q][p] = belieftree_instrument[0][q][p] + (random.random()/10) - 0.05
			belieftree_instrument[0][q][p] = one_minus_one_check(belieftree_instrument[0][q][p])

	return belieftree, belieftree_policy, belieftree_instrument

def one_minus_one_check(to_be_checked_parameter):

	checked_parameter = 0
	if to_be_checked_parameter > 1:
		checked_parameter = 1
	elif to_be_checked_parameter < -1:
		checked_parameter = -1
	else:
		checked_parameter = to_be_checked_parameter
	return checked_parameter

def add(self, agent):
	agent_class = type(agent)
	self.agent_action_dict[agent_class].append(agent)

def conflict_level_update(link_list, len_PC, len_ML, len_S, conflict_level_coef):

		"""
		The conflict level update function
		===========================

		The description here is currently missing.

		"""

		for links in link_list:
			# print(links)
			conflict_level_temp = copy.copy(links.conflict_level)
			for issues in range(len_PC + len_ML + len_S):
				# This is all based on partial knowledge
				# AGENT 1 - based on the partial knowledge he has of 
				# For the calculation of the state conflict level:

				# If one of the beliefs is known to be 'No' then assign 'No' to the conflict level
				if links.agent1.belieftree[1 + links.agent2.unique_id][issues][0] == 'No' or links.agent1.belieftree[0][issues][0] == 'No':
					links.conflict_level[0][issues][0] = 'No'
				# If there is no knowledge of the other agent's beliefs, the conflict level is set to 0.85 by default
				elif links.agent1.belieftree[1 + links.agent2.unique_id][issues][0] == None:
					links.conflict_level[0][issues][0] = conflict_level_coef[1]
				# If all beliefs are known, calculate the conflict level
				else:
					conflict_level_temp[0][issues][0] = abs(links.agent1.belieftree[0][issues][0] - links.agent1.belieftree[1 + links.agent2.unique_id][issues][0])
					if conflict_level_temp[0][issues][0] <= 0.25:
						links.conflict_level[0][issues][0] = conflict_level_coef[0]
					if conflict_level_temp[0][issues][0] > 0.25 and conflict_level_temp[0][issues][0] <= 1.75:
						links.conflict_level[0][issues][0] = conflict_level_coef[2]
					if conflict_level_temp[0][issues][0] > 1.75:
						links.conflict_level[0][issues][0] = conflict_level_coef[1]

				# For the calculation of the aim conflict level:
				if links.agent1.belieftree[1 + links.agent2.unique_id][issues][1] == 'No' or links.agent1.belieftree[0][issues][1] == 'No':
					links.conflict_level[0][issues][1] = 'No'
				elif links.agent1.belieftree[1 + links.agent2.unique_id][issues][1] == None:
					links.conflict_level[0][issues][1] = conflict_level_coef[1]
				else:
					conflict_level_temp[0][issues][1] = abs(links.agent1.belieftree[0][issues][1] - links.agent1.belieftree[1 + links.agent2.unique_id][issues][1])
					if conflict_level_temp[0][issues][1] <= 0.25:
						links.conflict_level[0][issues][1] = conflict_level_coef[0]
					if conflict_level_temp[0][issues][1] > 0.25 and conflict_level_temp[0][issues][1] <= 1.75:
						links.conflict_level[0][issues][1] = conflict_level_coef[2]
					if conflict_level_temp[0][issues][1] > 1.75:
						links.conflict_level[0][issues][1] = conflict_level_coef[1]
				
				# AGENT 2
				# For the calculation of the state conflict level:
				if links.agent2.belieftree[1 + links.agent1.unique_id][issues][0] == 'No' or links.agent2.belieftree[0][issues][0] == 'No':
					links.conflict_level[1][issues][0] = 'No'
				elif links.agent2.belieftree[1 + links.agent1.unique_id][issues][0] == None:
					links.conflict_level[1][issues][0] = conflict_level_coef[1]
				else:
					conflict_level_temp[1][issues][0] = abs(links.agent2.belieftree[0][issues][0] - links.agent2.belieftree[1 + links.agent1.unique_id][issues][0])
					if conflict_level_temp[1][issues][0] <= 0.25:
						links.conflict_level[1][issues][0] = conflict_level_coef[0]
					if conflict_level_temp[1][issues][0] > 0.25 and conflict_level_temp[1][issues][0] <= 1.75:
						links.conflict_level[1][issues][0] = conflict_level_coef[2]
					if conflict_level_temp[1][issues][0] > 1.75:
						links.conflict_level[1][issues][0] = conflict_level_coef[1]
				# For the calculation of the aim conflict level:
				if links.agent2.belieftree[1 + links.agent1.unique_id][issues][1] == 'No' or links.agent2.belieftree[0][issues][1] == 'No':
					links.conflict_level[1][issues][1] = 'No'
				elif links.agent2.belieftree[1 + links.agent1.unique_id][issues][1] == None:
					links.conflict_level[1][issues][1] = conflict_level_coef[1]
				else:
					conflict_level_temp[1][issues][1] = abs(links.agent2.belieftree[0][issues][1] - links.agent2.belieftree[1 + links.agent1.unique_id][issues][1])
					if conflict_level_temp[1][issues][1] <= 0.25:
						links.conflict_level[1][issues][1] = conflict_level_coef[0]
					if conflict_level_temp[1][issues][1] > 0.25 and conflict_level_temp[1][issues][1] <= 1.75:
						links.conflict_level[1][issues][1] = conflict_level_coef[2]
					if conflict_level_temp[1][issues][1] > 1.75:
						links.conflict_level[1][issues][1] = conflict_level_coef[1]
			# print(links.conflict_level)

			# For the causal relation part:
			for issues in range(len_PC*len_ML + len_ML*len_S):
				# This is all based on partial knowledge
				# AGENT 1 - based on the partial knowledge he has of 
				# For the calculation of the state conflict level:

				# If one of the beliefs is known to be 'No' then assign 'No' to the conflict level
				if links.agent1.belieftree[1 + links.agent2.unique_id][len_PC + len_ML + len_S + issues][0] == 'No' or links.agent1.belieftree[0][len_PC + len_ML + len_S + issues][0] == 'No':
					links.conflict_level[0][len_PC + len_ML + len_S + issues][0] = 'No'
				# If there is no knowledge of the other agent's beliefs, the conflict level is set to 0.85 by default
				elif links.agent1.belieftree[1 + links.agent2.unique_id][len_PC + len_ML + len_S + issues][0] == None:
					links.conflict_level[0][len_PC + len_ML + len_S + issues][0] = conflict_level_coef[1]
				# If all beliefs are known, calculate the conflict level
				else:
					conflict_level_temp[0][len_PC + len_ML + len_S + issues][0] = abs(links.agent1.belieftree[0][len_PC + len_ML + len_S + issues][0] - links.agent1.belieftree[1 + links.agent2.unique_id][len_PC + len_ML + len_S + issues][0])
					if conflict_level_temp[0][len_PC + len_ML + len_S + issues][0] <= 0.25:
						links.conflict_level[0][len_PC + len_ML + len_S + issues][0] = conflict_level_coef[0]
					if conflict_level_temp[0][len_PC + len_ML + len_S + issues][0] > 0.25 and conflict_level_temp[0][len_PC + len_ML + len_S + issues][0] <= 1.75:
						links.conflict_level[0][len_PC + len_ML + len_S + issues][0] = conflict_level_coef[2]
					if conflict_level_temp[0][len_PC + len_ML + len_S + issues][0] > 1.75:
						links.conflict_level[0][len_PC + len_ML + len_S + issues][0] = conflict_level_coef[1]
				
				# AGENT 2
				# For the calculation of the state conflict level:
				if links.agent2.belieftree[1 + links.agent1.unique_id][len_PC + len_ML + len_S + issues][0] == 'No' or links.agent2.belieftree[0][len_PC + len_ML + len_S + issues][0] == 'No':
					links.conflict_level[1][len_PC + len_ML + len_S + issues][0] = 'No'
				elif links.agent2.belieftree[1 + links.agent1.unique_id][len_PC + len_ML + len_S + issues][0] == None:
					links.conflict_level[1][len_PC + len_ML + len_S + issues][0] = conflict_level_coef[1]
				else:
					conflict_level_temp[1][len_PC + len_ML + len_S + issues][0] = abs(links.agent2.belieftree[0][len_PC + len_ML + len_S + issues][0] - links.agent2.belieftree[1 + links.agent1.unique_id][len_PC + len_ML + len_S + issues][0])
					if conflict_level_temp[1][len_PC + len_ML + len_S + issues][0] <= 0.25:
						links.conflict_level[1][len_PC + len_ML + len_S + issues][0] = conflict_level_coef[0]
					if conflict_level_temp[1][len_PC + len_ML + len_S + issues][0] > 0.25 and conflict_level_temp[1][len_PC + len_ML + len_S + issues][0] <= 1.75:
						links.conflict_level[1][len_PC + len_ML + len_S + issues][0] = conflict_level_coef[2]
					if conflict_level_temp[1][len_PC + len_ML + len_S + issues][0] > 1.75:
						links.conflict_level[1][len_PC + len_ML + len_S + issues][0] = conflict_level_coef[1]
