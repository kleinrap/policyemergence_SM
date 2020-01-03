'''''
'''''

def policy_package_initialisation(inputs_dict):

	'''''
	This function is used to initialise the policy instrument used for the strategic flood protection system dynamics model.

	1. Ageing time - endogenous (AT_state)
	2. Obscolescence time - endogenous (OT_state)
	3. Design time - endogenous (DT_state)
	4. Flood perception time - endogenous (FPT_state)
	5. Effects on renovation and construction - endogenous (ERC_state)
	6. Renovation time - endogenous (RT_state)
	7. Adjustment time - endogenous (AdT_state)
	8. Planning horizon - endogenous (PH_state)
	9. Renovation standard - endogenous (RS_state)
	10. Construction time - endogenous (CT_state)
	'''''

	# Instruments inputs
	intstruments_number = 16
	instruments = [0 for i in range(intstruments_number)]

	# EXPERTISE related instruments impacts: AT (1), OT (2), DT (3)
	# Small and larger increase in expertise level
	instruments[0] = [0.05, 0.05, -0.05, 0, 0, 0, 0, 0, 0, 0]
	instruments[1] = [0.10, 0.10, -0.10, 0, 0, 0, 0, 0, 0, 0]
	# Small and large decrease in expertise level
	instruments[2] = [-0.05, -0.05, 0.05, 0, 0, 0, 0, 0, 0, 0]
	instruments[3] = [-0.10, -0.10, 0.10, 0, 0, 0, 0, 0, 0, 0]

	# PUBLIC PERCEPTION related instruments impacts: FPT (4), ERC (5)
	# Small and large increase in public perception
	instruments[4] = [0, 0, 0, -0.05, 0.05, 0, 0, 0, 0, 0]
	instruments[5] = [0, 0, 0, -0.10, 0.10, 0, 0, 0, 0, 0]
	# Small and large decrease in public perception
	instruments[6] = [0, 0, 0, 0.05, -0.05, 0, 0, 0, 0, 0]
	instruments[7] = [0, 0, 0, 0.10, -0.10, 0, 0, 0, 0, 0]

	# RESOURCE ALLOCATION related instruments impacts: AT (1), OT (2), DT (3), RT (6), AdT (7)
	# Small and large increase in resource allocation
	instruments[8] = [0.05, 0.05, -0.05, 0, 0, -0.05, -0.05, 0, 0, 0]
	instruments[9] = [0.10, 0.10, -0.10, 0, 0, -0.10, -0.10, 0, 0, 0]
	# Small and large decrease in resource allocation
	instruments[10] = [-0.05, -0.05, 0.05, 0, 0, 0.05, 0.05, 0, 0, 0]
	instruments[11] = [-0.10, -0.10, 0.10, 0, 0, 0.10, 0.10, 0, 0, 0]

	# INVESTMENT LEVEL related instruments impacts: PH (8), RS (9), CT (10)
	# Small and large increase in investment level
	instruments[12] = [0, 0, 0, 0, 0, 0, 0, 0.05, 0.05, -0.05]
	instruments[13] = [0, 0, 0, 0, 0, 0, 0, 0.10, 0.10, -0.10]
	# Small and large decrease in investment level
	instruments[14] = [0, 0, 0, 0, 0, 0, 0, -0.05, -0.05, 0.05]
	instruments[15] = [0, 0, 0, 0, 0, 0, 0, -0.10, -0.10, 0.10]
	
	inputs_dict["Instruments"] = instruments

	return inputs_dict

