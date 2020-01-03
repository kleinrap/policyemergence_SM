'''''
'''''

def policy_implementation(policy_selected, AT_value, OT_value, DT_value, FPT_value, ERC_value, RT_value, AdT_value, PH_value, RS_value, CT_value):

	'''''
	This function is used to implement the policy package chosen by the policy makers through the changing of the exogenous parameters from the technical model.
	'''''

	min_AT = 15
	max_AT = 25

	min_OT = 20
	max_OT = 40

	min_DT = 1.5
	max_DT = 4.5

	min_FPT = 0
	max_FPT = 1

	min_ERC = 1.5
	max_ERC = 7.5

	min_RT = 2.5
	max_RT = 5

	min_AdT = 15
	max_AdT = 45

	min_PH = 15
	max_PH = 100

	min_RS = 0.05
	max_RS = 0.4

	min_CT = 3
	max_CT = 7

	AT_value = policy_package_implementation_formula(policy_selected, 0, AT_value, min_AT, max_AT)
	OT_value = policy_package_implementation_formula(policy_selected, 1, OT_value, min_OT, max_OT)
	DT_value = policy_package_implementation_formula(policy_selected, 2, DT_value, min_DT, max_DT)
	FPT_value = policy_package_implementation_formula(policy_selected, 3, FPT_value, min_FPT, max_FPT)
	ERC_value = policy_package_implementation_formula(policy_selected, 4, ERC_value, min_ERC, max_ERC)
	RT_value = policy_package_implementation_formula(policy_selected, 5, RT_value, min_RT, max_RT)
	AdT_value = policy_package_implementation_formula(policy_selected, 6, AdT_value, min_AdT, max_AdT)
	PH_value = policy_package_implementation_formula(policy_selected, 7, PH_value, min_PH, max_PH)
	RS_value = policy_package_implementation_formula(policy_selected, 8, RS_value, min_RS, max_RS)
	CT_value = policy_package_implementation_formula(policy_selected, 9, CT_value, min_CT, max_CT)

	return AT_value, OT_value, DT_value, FPT_value, ERC_value, RT_value, AdT_value, PH_value, RS_value, CT_value

def policy_package_implementation_formula(policy_selected, issue, current_value, min_value, max_value):

	# Function used for the formula used to implemented the policy package instruments. The policy instrument acts on the difference with either the minimum or the maximum to avoid it overshooting over what is prescribed as being the minimum or the maximum.
	if policy_selected[issue] > 0:
		current_value += abs(max_value-current_value)*policy_selected[issue]
	else:
		current_value += abs(min_value-current_value)*policy_selected[issue]

	# Some additional checks ... because computational error will make it go over the max or below the min.
	if current_value > max_value:
		current_value = max_value
	if current_value < min_value:
		current_value = min_value

	return current_value
