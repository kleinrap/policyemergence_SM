from model_schelling import Schelling
from model_SM import PolicyEmergenceSM
import matplotlib.pyplot as plt
import copy

from model_SM_policyImpact import policy_impact_evaluation
from model_module_interface import issue_mapping
from model_SM_agents import TruthAgent

'''
The current architecture is used for test purposes.
Ultimately, the two models should be initialised and then their for loops should be intertwined.
'''

# 1 - policy emergence alone
# 2 - segregation alone
# 3 - both
run_type = 3

if run_type == 1:
	# running the policy emergence Simplest Model
	model_run_SM = PolicyEmergenceSM(10,10)

	for i in range(5):
		model_run_SM.step()

if run_type == 2:
	# running the Schelling model:
	model_run_schelling = Schelling(20, 20, 0.75, 0.4)

	for i in range(25):
		if model_run_schelling.happy != model_run_schelling.schedule.get_agent_count():
			print("Step: ", i)
			model_run_schelling.step()

if run_type == 3:

	# running parameters
	run_tick = 2
	interval_tick = 5
	warmup_tick = 5

	# initialisation of both models
	model_run_SM = PolicyEmergenceSM(10,10)
	model_run_schelling = Schelling(20, 20, 0.75, 0.4)


	print("\n")
	print("************************")
	print("Start of the simulation:", "\n")
	for i in range(run_tick):

		print(" ")
		print("************************")
		print("Tick number: ", i)

		# warm up time
		# this is also used as a warmup time
		if i == 0:
			policy_chosen = [None for ite in range(len(model_run_SM.policy_instruments[0]))]
			for warmup_time in range(warmup_tick):
				IssueInit, type0agents, type1agents = model_run_schelling.step(policy_chosen)

		# policy impact evaluation
		policy_impact_evaluation(model_run_SM, model_run_schelling, IssueInit, interval_tick)

		# running the policy emergence model
		if i == 0:
			KPIs = issue_mapping(IssueInit, type0agents, type1agents)
		else:
			KPIs = issue_mapping(KPIs, type0agents, type1agents)
		policy_chosen = model_run_SM.step(KPIs)

		# run of the segregation model for n ticks
		for p in range(interval_tick):
			KPIs, type0agents, type1agents = model_run_schelling.step(policy_chosen)
			policy_chosen = [None for ite in range(len(model_run_SM.policy_instruments[0]))] # reset policy after it has been implemented once

	# printing the data obtained from the Schelling model
	dataPlot_Schelling = model_run_schelling.datacollector.get_model_vars_dataframe()
	print(dataPlot_Schelling)
	dataPlot_Schelling.plot("step", "evenness")
	dataPlot_Schelling.plot("step", ["happy", "happytype0", "happytype1"])
	dataPlot_Schelling.plot("step", ["movement", "movementtype0", "movementtype1"])

	dataPlot_SM = model_run_SM.datacollector.get_model_vars_dataframe()
	print(dataPlot_SM)

	plt.show()