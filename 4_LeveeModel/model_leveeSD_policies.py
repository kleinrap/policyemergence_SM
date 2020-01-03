'''''
'''''

def exo_value_def(exo_value):

	exo_value['AT_value'] = 20
	exo_value['OT_value'] = 25
	exo_value['DT_value'] = 2.5
	exo_value['FPT_value'] = 0.5
	exo_value['ERC_value'] = 0
	# todo - CHANGE THIS ERC_value! This needs to affect 
	# the values in the graph only - ERC changes is currently deactivated in the rest of the code
	exo_value['RT_value'] = 3.5
	exo_value['AdT_value'] = 30
	exo_value['PH_value'] = 55
	exo_value['RS_value'] = 0.2
	exo_value["CT_value"] = 5

	return exo_value

def policy_implementation(policy, exo_value):

	'''''
	This function is used to implement the policy package chosen by the policy makers through the changing of the exogenous parameters from the technical model.
	'''''

	min_AT = 15; max_AT = 25
	if policy[0] != None and min_AT < exo_value['AT_value'] + policy[0] < max_AT:
		exo_value['AT_value'] += policy[0]

	min_OT = 20; max_OT = 40
	if policy[1] != None and min_OT < exo_value['OT_value'] + policy[1] < max_OT:
		exo_value['OT_value'] += policy[1]

	min_DT = 1.5; max_DT = 4.5
	if policy[2] != None and min_DT < exo_value['DT_value'] + policy[2] < max_DT:
		exo_value['DT_value'] += policy[2]

	min_FPT = 0; max_FPT = 1
	if policy[3] != None and min_FPT < exo_value['FPT_value'] + policy[3] < max_FPT:
		exo_value['FPT_value'] += policy[3]

	min_ERC = 1.5; max_ERC = 7.5
	if policy[4] != None and min_ERC < exo_value['ERC_value'] + policy[4] < max_ERC:
		exo_value['ERC_value'] += policy[4]

	min_RT = 2.5; max_RT = 5
	if policy[5] != None and min_RT < exo_value['RT_value'] + policy[5] < max_RT:
		exo_value['RT_value'] += policy[5]

	min_AdT = 15; max_AdT = 45
	if policy[6] != None and min_AdT < exo_value['AdT_value'] + policy[6] < max_AdT:
		exo_value['AdT_value'] += policy[6]

	min_PH = 10; max_PH = 100
	if policy[7] != None and min_PH < exo_value['PH_value'] + policy[7] < max_PH:
		exo_value['PH_value'] += policy[7]

	min_RS = 0.05; max_RS = 0.4
	if policy[8] != None and min_RS < exo_value['RS_value'] + policy[8] < max_RS:
		exo_value['RS_value'] += policy[8]

	min_CT = 3; max_CT = 7
	if policy[9] != None and min_CT < exo_value['CT_value'] + policy[9] < max_CT:
		exo_value['CT_value'] += policy[9]


	# print('AT', exo_value['AT_value'], 'OT', exo_value['OT_value'], 'DT', exo_value['DT_value'],
	# 	  'FPT', exo_value['FPT_value'], 'ERC', exo_value['ERC_value'], 'RT', exo_value['RT_value'])

	# for i in range(len(policy)):
	# 	if policy[i] == None:
	# 		policy[i] = 0

	# exo_value['AT_value'] = formula(policy, 0, exo_value['AT_value'], min_AT, max_AT)
	# exo_value['OT_value'] = formula(policy, 1, exo_value['OT_value'], min_OT, max_OT)
	# exo_value['DT_value'] = formula(policy, 2, exo_value['DT_value'], min_DT, max_DT)
	# exo_value['FPT_value'] = formula(policy, 3, exo_value['FPT_value'], min_FPT, max_FPT)
	# exo_value['ERC_value'] = formula(policy, 4, exo_value['ERC_value'], min_ERC, max_ERC)
	# exo_value['RT_value'] = formula(policy, 5, exo_value['RT_value'], min_RT, max_RT)
	# exo_value['AdT_value'] = formula(policy, 6, exo_value['AdT_value'], min_AdT, max_AdT)
	# exo_value['PH_value'] = formula(policy, 7, exo_value['PH_value'], min_PH, max_PH)
	# exo_value['RS_value'] = formula(policy, 8, exo_value['RS_value'], min_RS, max_RS)
	# exo_value['CT_value'] = formula(policy, 9, exo_value['CT_value'], min_CT, max_CT)

	return exo_value

def formula(policy, factor, current_value, min_value, max_value):

	# Function used for the formula used to implemented the policy package instruments. The policy instrument acts on the difference with either the minimum or the maximum to avoid it overshooting over what is prescribed as being the minimum or the maximum.
	if policy[factor] != 0:
		current_value += abs(max_value-current_value)*policy[factor]
	else:
		current_value += abs(min_value-current_value)*policy[factor]

	# Some additional checks ... because computational error will make it go over the max or below the min.
	if current_value > max_value:
		current_value = max_value
	if current_value < min_value:
		current_value = min_value

	return current_value
