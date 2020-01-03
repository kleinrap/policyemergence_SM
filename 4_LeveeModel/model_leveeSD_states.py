import random
import copy
import pysd

'''
Secondary beliefs (S)
S1. Standard levee safety - endogenous (SLS_state)
S2. Old levee safety - endogenous (OLS_state)
S3. Standard levees - endogenous (SL_state)
S4. Old levees - endogenous (OL_state)

Policy core beliefs (PC)
PC1. Investment priority - calculated as OL_state/SL_state (IP_state)
PC2. Safety - calculated as half perceived safety and hald technical safety (Sa_state)
'''



'''
Designed Levees
Standard Levees
Old Levees
Current Safety Standard
Safety SL
Safety OL
Anticipated Flood Level
perceived current safety
'''

def saving_stocks(model_technical):

	stocks = dict()
	stocks["DL"] = model_technical.components.designed_levees()
	stocks["SL"] = model_technical.components.standard_levees()
	stocks["OL"] = model_technical.components.old_levees()
	stocks["CSS"] = model_technical.components.current_safety_standard()
	stocks["SSL"] = model_technical.components.safety_sl()
	stocks["SOL"] = model_technical.components.safety_ol()
	stocks["AFL"] = model_technical.components.anticipated_flood_level()
	stocks["PCS"] = model_technical.components.perceived_current_safety()

	return stocks

def states_calculation(model_technical):

	'''''
	This function is used to calculate the states into a 0,1 interval from the states obtained in the technical model.
	'''''

	# S1 - Standard levy safety
	min_SLS = 0
	max_SLS = 80000
	SLS_state = model_technical.components.safety_sl()
	S1 = (SLS_state - min_SLS) / (max_SLS-min_SLS)

	# S2 - Old levee safety
	min_OLS = 0
	max_OLS = 80000
	OLS_state = model_technical.components.safety_ol()
	S2 = (OLS_state - min_OLS) / (max_OLS-min_OLS)

	# S3 - Standard levee length
	min_SL = 0
	max_SL = 12000
	SL_state = model_technical.components.standard_levees()
	S3 = (SL_state - min_SL) / (max_SL-min_SL)

	# S4 - Old levee length
	min_OL = 0
	max_OL = 12000
	OL_state = model_technical.components.old_levees()
	S4 = (OL_state - min_OL) / (max_OL-min_OL)

	# PC1 - Investment priority
	min_IP = 0
	max_IP  = 15
	IP_state = model_technical.components.old_levees()/model_technical.components.standard_levees()
	PC1 = (IP_state - min_IP) / (max_IP-min_IP)
	# Check considering the low level required for max_IP
	if PC1 < 0 or PC1 > 1:
		print('There is a problem for the calculation of the IP_state.')

	# PC2 - Safety
	min_Sa = 0
	max_Sa = 1
	Sa_state = (model_technical.components.perceived_current_safety()+model_technical.components.official_current_safety())/2
	PC2 = (Sa_state - min_Sa) / (max_Sa-min_Sa)

	KPIs = [0, PC1, PC2, S1, S2, S3, S4]

	return KPIs