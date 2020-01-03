from model_PE_agents import TruthAgent
import copy
import pathos.multiprocessing as mp

from model_leveeSD_policies import policy_implementation
from model_leveeSD_states import states_calculation
import pysd
import numpy as np
import matplotlib.pyplot as plt


def model_simulation(inputs):

	'''
	This function is used to simulate the model for the evaluation of the policies. It outputs the indicators of the
	simulation that has been run.

	NOTE - THE INSTRUMENT IS ASSESSED ONLY ONE YEAR AHEAD
	'''

	policy_chosen = inputs[0] # policy chosen
	policy_eval_tick = inputs[1]
	run_time_till_now = inputs[2]
	time_step_SD = inputs[3]
	model_levee_PI = inputs[4]
	stocks = inputs[5]
	exo_values = inputs[6]

	exo_values = policy_implementation(policy_chosen, exo_values) # exo_values for policy

	# initialising
	model_levee_PI.run(params={'aging time':exo_values['AT_value'],
							   'obsolescence time':exo_values['OT_value'],
							   'design time':exo_values['DT_value'],
							   'flood perception time':exo_values['FPT_value'],
							   'renovation time':exo_values['RT_value'],
							   'adjustment time':exo_values['AdT_value'],
							   'planning horizon':exo_values['PH_value'],
							   'renovation standard':exo_values['RS_value'],
							   'construction time':exo_values['CT_value']},
					   # initial_condition='current',
					   initial_condition=(1 + run_time_till_now,
										  {'Designed Levees':stocks['DL'],
										   'Standard Levees':stocks['SL'],
										   'Old Levees':stocks['OL'],
										   'Current Safety Standard':stocks['CSS'],
										   'Safety SL':stocks['SSL'],
										   'Safety OL':stocks['SOL'],
										   'Anticipated Flood Level':stocks['AFL'],
										   'perceived current safety':stocks['PCS']}),
					   return_timestamps=np.linspace(1 + run_time_till_now,
													 1 + run_time_till_now + 1,
													 1 // time_step_SD))

	for n in range(policy_eval_tick):
		model_levee_PI.run(params={'aging time': exo_values['AT_value'],
								   'obsolescence time': exo_values['OT_value'],
								   'design time': exo_values['DT_value'],
								   'flood perception time': exo_values['FPT_value'],
								   'renovation time': exo_values['RT_value'],
								   'adjustment time': exo_values['AdT_value'],
								   'planning horizon': exo_values['PH_value'],
								   'renovation standard': exo_values['RS_value'],
								   'construction time': exo_values['CT_value']},
						   # initial_condition='current',
						   initial_condition='current',
						   return_timestamps=np.linspace(1 + run_time_till_now + n,
														 1 + run_time_till_now + n + 1,
														 1 // time_step_SD))

	KPIs = states_calculation(model_levee_PI) # mapping the states

	return KPIs

def policy_impact_evaluation(model_run_PE, KPIs_init, policy_eval_tick, run_time_till_now,
							 time_step_SD, stocks, exo_values):

	'''
	This function is used to estimate the impact of the policy instruments on the policy context. This is done by
	separately simulating every policy instruments and comparing the results with the initial states of the policy
	context. This is what is then used to inform the agents on the impact of the policies.
	The simulations for the different policies are parallelised for computational efficiency.
	'''

	len_DC = model_run_PE.len_DC; len_PC = model_run_PE.len_PC; len_S = model_run_PE.len_S
	policy_ins = model_run_PE.policy_instruments

	# creating the input vector for the parallelised simulation
	inputs = []
	for j in range(len(policy_ins)):
		intermediate = []
		intermediate.append(policy_ins[j])
		intermediate.append(policy_eval_tick)
		intermediate.append(run_time_till_now)
		intermediate.append(time_step_SD)
		intermediate.append(pysd.load('Flood_Levees_14_Final.py'))
		intermediate.append(stocks)
		intermediate.append(exo_values)
		inputs.append(intermediate)

	# running the parallel simulation
	pool = mp.Pool(8)
	results = pool.map(lambda a: model_simulation(a), inputs)
	pool.close()

	'''
	OLD NON-PARALLELISED CODE
	# initialisation of the vector that will store the KPIs of the mock simulation for each policy instrument
	issues = [0 for l in range(len_S + len_PC + len_DC)]
	for q in range(len_S + len_PC + len_DC):
		issues[q] = [0 for l in range(len(policy_ins))]

	# simulating all policy instruments for n ticks to obtain KPIs at the final state
	for j in range(len(policy_ins)):
		# copy of the model in its current state
		model_run_context_PI_test = copy.deepcopy(model_run_context)

		# run the simulation with policy introduced and collect data
		policy = policy_ins[j]  # set policy vector for one step
		for k in range(interval_tick):
			KPIs = model_run_context_PI_test.step(policy)
			policy = [None for f in range(len(policy_ins[j]))] 
				# reset policy vector after it has been implemented once

		# mapping the outcomes to a [0,1] interval
		IssueE = issue_mapping(KPIs)

		# store the final state of the belief (last simulation)
		for p in range(len_S + len_PC + len_DC):
			issues[p][j] = IssueE[p]
	'''

	# for i in range(len(results)):
	# 	print(' ')
	# 	print('policy:', policy_ins[i], 'results:', results[i])

	# looking at one policy instrument after the other
	impact_policy = [[0 for l in range(len_S + len_PC)] for r in range(len(policy_ins))]
	for j in range(len(policy_ins)):

		for q in range(len_PC + len_S): # calculating the percentage change from no policy to a policy
			new_KPI = results[j][len_DC + q]
			old_KPI = KPIs_init[len_DC + q]
			if old_KPI != 0:
				impact_policy_temp = (new_KPI - old_KPI)/old_KPI
				impact_policy[j][q] = round(impact_policy_temp, 3)
			if old_KPI == 0 and new_KPI == 0:
				impact_policy[j][q] = 0
			if old_KPI == 0 and new_KPI != 0:
				impact_policy[j][q] = 1

		for agent in model_run_PE.schedule.agent_buffer(shuffled=True): # updating the truth agent
			if isinstance(agent, TruthAgent):
				agent.policytree_truth[len_PC + j] = impact_policy[j][len_PC:len_PC + len_S]

	# # considering the policy families
	# # policy family 1 (instruments: 0, 1, 2, 3, 8, 9, 10)
	# # policy family 2 (instruments: 4, 5, 6, 7, 8, 9, 10)
	# likelihood_PF1 = [0 for f in range(len_PC)]
	# len_PF1 = 7
	# likelihood_PF2 = [0 for f in range(len_PC)]
	# len_PF2 = 7
	# # average the absolute value of their impact per
	# for j in range(len(policy_ins)):
	# 	# selecting only policy instruments related to policy family 1
	# 	if j == 0 or j == 1 or j == 2 or j == 3 or j == 8 or j == 9 or j == 10:
	# 		likelihood_PF1[0] += impact_policy[j][len_S] / len_PF1
	# 		likelihood_PF1[1] += impact_policy[j][len_S + 1] / len_PF1
	# 	# selecting only policy instruments related to policy family 2
	# 	if j == 4 or j == 5 or j == 6 or j == 7 or j == 8 or j == 9 or j == 10:
	# 		likelihood_PF2[0] += impact_policy[j][len_S] / len_PF2
	# 		likelihood_PF2[1] += impact_policy[j][len_S+1] / len_PF2
	#
	# # rounding values
	# likelihood_PF1[0] = round(likelihood_PF1[0], 3)
	# likelihood_PF1[1] = round(likelihood_PF1[1], 3)
	# likelihood_PF2[0] = round(likelihood_PF2[0], 3)
	# likelihood_PF2[1] = round(likelihood_PF2[1], 3)
	#
	# for agent in model_run_PE.schedule.agent_buffer(shuffled=True):
	# 	if isinstance(agent, TruthAgent):
	# 		# updating the policy tree of the truth agent
	# 		agent.policytree_truth[0] = likelihood_PF1
	# 		agent.policytree_truth[1] = likelihood_PF2
