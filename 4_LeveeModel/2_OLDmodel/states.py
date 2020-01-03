import random
import copy
import pysd

'''''
What are the states that are needed from the technical model?

Secondary beliefs (S)
7. Ageing time - endogenous (AT_state)
8. Obscolescence time - endogenous (OT_state)
9. Design time - endogenous (DT_state)
10. Flood perception time - endogenous (FPT_state)
11. Effects on renovation and construction - endogenous (ERC_state)
12. Renovation time - endogenous (RT_state)
13. Adjustment time - endogenous (AdT_state)
14. Planning horizon - endogenous (PH_state)
15. Renovation standard - endogenous (RS_state)
16. Construction time - endogenous (CT_state)

Mid-level beliefs (ML)
3. Standard levee safety - endogenous (SLS_state)
4. Old levee safety - endogenous (OLS_state)
5. Standard levees - endogenous (SL_state)
6. Old levees - endogenous (OL_state)

Policy core beliefs (PC)
1. Investment priority - calculated as OL_state/SL_state (IP_state)
2. Safety - calculated as half perceived safety and hald technical safety (Sa_state)
'''''

def states_definition(model_technical, states_technical):

	'''''
	This function is used to assign the values from the technical model to their respective dictionnary.
	'''''

	# Assigning the values to the right dictionnary parameters
	states_technical["AT_state"] = model_technical.components.aging_time()
	states_technical["OT_state"] = model_technical.components.obsolescence_time()
	states_technical["DT_state"] = model_technical.components.design_time()
	states_technical["FPT_state"] = model_technical.components.flood_perception_time()
	# CHANGE THIS! - The ERC is currently the actual state of the model while it was intended to take the first value of the lookup function
	states_technical["ERC_state"] = model_technical.components.effect_on_renovation_and_construction()
	states_technical["RT_state"] = model_technical.components.renovation_time()
	states_technical["AdT_state"] = model_technical.components.adjustment_time()
	states_technical["PH_state"] = model_technical.components.planning_horizon()
	states_technical["RS_state"] = model_technical.components.renovation_standard()
	states_technical["CT_state"] = model_technical.components.construction_time()
	states_technical["SLS_state"] = model_technical.components.safety_sl()
	states_technical["OLS_state"] = model_technical.components.safety_ol()
	states_technical["SL_state"] = model_technical.components.standard_levees()
	states_technical["OL_state"] = model_technical.components.old_levees()
	states_technical["IP_state"] = model_technical.components.old_levees()/model_technical.components.standard_levees()
	states_technical["Sa_state"] = (model_technical.components.perceived_current_safety()+model_technical.components.official_current_safety())/2

	return states_technical

def states_calculation(states_technical, emergence_states):

	'''''
	This function is used to calculate the states into a -1,1 interval from the states obtained in the technical model.
	'''''

	# Calculation of the ageing time
	min_AT = 15
	max_AT = 25
	emergence_states["AT_state"] = (((states_technical["AT_state"] - min_AT) / (max_AT-min_AT)) * 2) - 1

	# Calculation of the obsolescence time
	min_OT = 20
	max_OT = 40
	emergence_states["OT_state"] = (((states_technical["OT_state"] - min_OT) / (max_OT-min_OT)) * 2) - 1

	# Calculation of the design time
	min_DT = 1.5
	max_DT = 4.5
	emergence_states["DT_state"] = (((states_technical["DT_state"] - min_DT) / (max_DT-min_DT)) * 2) - 1

	# Calculation of the flood perception time
	min_FPT = 0
	max_FPT = 1
	emergence_states["FPT_state"] = (((states_technical["FPT_state"] - min_FPT) / (max_FPT-min_FPT)) * 2) - 1

	# Calculation of the effects on renovation and construction
	min_ERC = 1.5
	max_ERC = 7.5
	emergence_states["ERC_state"] = (((states_technical["ERC_state"] - min_ERC) / (max_ERC-min_ERC)) * 2) - 1

	# Calculation of the renovation time
	min_RT = 2.5
	max_RT = 5
	emergence_states["RT_state"] = (((states_technical["RT_state"] - min_RT) / (max_RT-min_RT)) * 2) - 1

	# Calculation of the adjustment time
	min_AdT = 15
	max_AdT = 45
	emergence_states["AdT_state"] = (((states_technical["AdT_state"] - min_AdT) / (max_AdT-min_AdT)) * 2) - 1

	# Calculation of the planning horizon
	min_PH = 15
	max_PH = 100
	emergence_states["PH_state"] = (((states_technical["PH_state"] - min_PH) / (max_PH-min_PH)) * 2) - 1

	# Calculation of the renovation standard
	min_RS = 0.05
	max_RS = 0.4
	emergence_states["RS_state"] = (((states_technical["RS_state"] - min_RS) / (max_RS-min_RS)) * 2) - 1

	# Calculation of the construction time
	min_CT = 3
	max_CT = 7
	emergence_states["CT_state"] = (((states_technical["CT_state"] - min_CT) / (max_CT-min_CT)) * 2) - 1

	# Calculation of the standard levy safety
	min_SLS = 0
	max_SLS = 80000
	emergence_states["SLS_state"] = (((states_technical["SLS_state"] - min_SLS) / (max_SLS-min_SLS)) * 2) - 1

	# Calculation of the old levee safety
	min_OLS = 0
	max_OLS = 80000
	emergence_states["OLS_state"] = (((states_technical["OLS_state"] - min_OLS) / (max_OLS-min_OLS)) * 2) - 1

	# Calculation of the standard levee length
	min_SL = 0
	max_SL = 12000
	emergence_states["SL_state"] = (((states_technical["SL_state"] - min_SL) / (max_SL-min_SL)) * 2) - 1

	# Calculation of the old levee length
	min_OL = 0
	max_OL = 12000
	emergence_states["OL_state"] = (((states_technical["OL_state"] - min_OL) / (max_OL-min_OL)) * 2) - 1

	# Calculation of the investment priority
	min_IP = 0
	max_IP  = 15
	emergence_states["IP_state"] = (((states_technical["IP_state"] - min_IP) / (max_IP-min_IP)) * 2) - 1
	# Check considering the low level required for max_IP
	if emergence_states["IP_state"] < -1 or emergence_states["IP_state"] > 1:
		print('There is a problem for the calculation of the IP_state.')

	# Calculation of the safety
	min_Sa = 0
	max_Sa = 1
	emergence_states["Sa_state"] = (((states_technical["Sa_state"] - min_Sa) / (max_Sa-min_Sa)) * 2) - 1

	return emergence_states