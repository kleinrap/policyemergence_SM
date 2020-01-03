'''
This file is a large input file for all the parameters and inputs related to the module interface that are used to
populate the policy emergence model.
This file is an example file that was created for the segregation model connection ... for any other policy context,
this file would need to be changed accordingly.
This would include the changes of the policy instruments and the changes of the structure of the belief system
'''


def belief_tree_input():
	'''
	This is the function that is used to create the structure of the belief tree.
	!Warning - Changes for every different policy context model
	'''

	# input of the issue tree
	len_S_names = ["SLS", "OLS", "SLL", "OLL"]  # secondary belief names
	len_PC_names = ["Investment", "Safety"]  # policy core belief names
	len_DC_names = ["none"]  # deep core belief names

	len_S = len(len_S_names); len_PC = len(len_PC_names); len_DC = len(len_DC_names)
	len_CR = len_DC * len_PC + len_PC * len_S

	return len_S, len_PC, len_DC, len_CR

def policy_instrument_input():

	'''
	This is the function that is used to insert the policy instruments into the model. This function can be changed
	for new policy instruments designed by the modeller
	!Warning - Changes for every different policy context model
	'''

	# below are model inputs that change for every model
	len_ins = 9  # number of policy instruments considers
	len_ins_names = [0 for f in range(len_ins)]
	len_ins_names[0] = "+AT+OT-DT"
	len_ins_names[1] = "-AT-OT+DT"
	len_ins_names[2] = "-FPT+ERC"
	len_ins_names[3] = "+FPT-ERC"
	len_ins_names[4] = "+AT+OT-DT-RT-AdT"
	len_ins_names[5] = "-AT-OT+DT+RT+AdT"
	len_ins_names[6] = "+PH+RS-CT"
	len_ins_names[7] = "-PH-RS+CT"
	len_ins_names[8] = "None"

	len_ins_1_names = len_ins_names[:] # additional numbers can be created for more policy families
	len_ins_exo_names = ["AT", "OT", "DT", "FPT", "ERC", "RT", "AdT", "PH", "RS", "CT"]  # exogenous parameter abbreviations

	# definition of the policy families
	PF_indices = [0] # only one family [0, 0] for two families for example
	PF_indices[0] = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # policy family 1
	# PF_indices[1] = [4, 5, 6, 7, 8, 9, 10]  # policy family 2

	# Introducing the policy instrument impact on the system
	policy_instruments = [0 for f in range(len_ins)]

	# %	1. Ageing time - endogenous (AT_state)
	# %	2. Obscolescence time - endogenous (OT_state)
	# %	3. Design time - endogenous (DT_state)
	# %	4. Flood perception time - endogenous (FPT_state)
	# %	5. Effects on renovation and construction - endogenous (ERC_state)
	# %	6. Renovation time - endogenous (RT_state)
	# %	7. Adjustment time - endogenous (AdT_state)
	# %	8. Planning horizon - endogenous (PH_state)
	# %	9. Renovation standard - endogenous (RS_state)
	# %	10. Construction time - endogenous (CT_state)

	# PERCENTAGE BASED INSTRUMENTS
	# # 						 AT	  , OT  , DT  , FPT , ERC , RT  , AdT , PH  , RS  , CT
	# policy_instruments[0] = [ 0.06, 0.06,-0.06, None, None, None, None, None, None, None]
	# policy_instruments[1] = [-0.06,-0.06, 0.06, None, None, None, None, None, None, None]
	# policy_instruments[2] = [ None, None, None,-0.06, 0.06, None, None, None, None, None]
	# policy_instruments[3] = [ None, None, None, 0.06,-0.06, None, None, None, None, None]
	# policy_instruments[4] = [ 0.06, 0.06,-0.06, None, None,-0.06,-0.06, None, None, None]
	# policy_instruments[5] = [-0.06,-0.06, 0.06, None, None, 0.06, 0.06, None, None, None]
	# policy_instruments[6] = [ None, None, None, None, None, None, None, 0.06, 0.06,-0.06]
	# policy_instruments[7] = [ None, None, None, None, None, None, None,-0.06,-0.06, 0.06]
	# # the no policy option is always presented to the agents as the last instrument
	# policy_instruments[8] = [ None, None, None, None, None, None, None, None, None, None]

	# MAGNITUDE BASED INSTRUMENTS
	# 						  AT  , OT  , DT  , FPT , ERC , RT  , AdT , PH  , RS  , CT
	policy_instruments[0] = [ 1	  , 2	,-0.25, None, None, None, None, None, None, None]
	policy_instruments[1] = [-1	  ,-2   , 0.25, None, None, None, None, None, None, None]
	policy_instruments[2] = [ None, None, None,-0.05, 0.5 , None, None, None, None, None]
	policy_instruments[3] = [ None, None, None, 0.05,-0.5 , None, None, None, None, None]
	policy_instruments[4] = [ 1	  , 2   ,-0.25, None, None,-0.5 ,-5   , None, None, None]
	policy_instruments[5] = [-1	  ,-2   , 0.25, None, None, 0.5 , 5   , None, None, None]
	policy_instruments[6] = [ None, None, None, None, None, None, None, 10  , 0.05,-0.5 ]
	policy_instruments[7] = [ None, None, None, None, None, None, None,-10  ,-0.05, 0.5 ]
	# the no policy option is always presented to the agents as the last instrument
	policy_instruments[8] = [ None, None, None, None, None, None, None, None, None, None]

	return policy_instruments, len_ins, PF_indices

# def issue_mapping(Issues, type0agents, type1agents):
#
# 	'''
# 	This function takes the KPIs and transforms them onto an interval of 0 to 1 for the agent beliefs
# 	and other applications within the model.
# 	'''
#
# 	# DC conversion - evenness
# 	DC1_min = 0  # miminum value of evenness (by definition)
# 	DC1_max = 1  # maximum value of evenness (by definition)
# 	DC1 = round(Issues[0]/(DC1_max - DC1_min), 3)
#
# 	# PC1 conversion - movement of all agents
# 	PC1_min = 0
# 	PC1_max = type0agents + type1agents
# 	PC1 = round(Issues[1]/(PC1_max - PC1_min), 3)
#
# 	# PC2 conversion - happiness of all agents
# 	PC2_min = 0
# 	PC2_max = type0agents + type1agents
# 	PC2 = round(Issues[2]/(PC2_max - PC2_min), 3)
#
# 	# secondary issues
# 	# S1 conversion - movement type 0 agents
# 	S1_min = 0
# 	S1_max = type0agents
# 	S1 = round(Issues[3]/(S1_max - S1_min), 3)
#
# 	# S2 conversion - movement type 1 agents
# 	S2_min = 0
# 	S2_max = type1agents
# 	S2 = round(Issues[4]/(S2_max - S2_min), 3)
#
# 	# S3 conversion - happiness type 0 agents
# 	S3_min = 0
# 	S3_max = type0agents
# 	S3 = round(Issues[5]/(S3_max - S3_min), 3)
#
# 	# S4 conversion - happiness type 1 agents
# 	S4_min = 0
# 	S4_max = type1agents
# 	S4 = round(Issues[6]/(S4_max - S4_min), 3)
#
# 	Issues = [DC1, PC1, PC2, S1, S2, S3, S4]
#
# 	return Issues