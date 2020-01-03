'''
This is a file that describes the policy tree:

1. The exogenous parameters - that can be affected by the policy instruments are:
	a. Vision - of the agents for determining their happiness
	b. Movement - quota for the number of agents that can move each tick
	c. Last movement - threshold determining the interval between ticks within which agents can move
	d. Type 0 preference - defines the preference of type 0 agents
	e. Type 1 preference - defines the preference of type 1 agents

2. Maxs and mins - help define the range within which the exogenous parameters can be changed:
	a. Vision: max = 15; min = 1
	b. Movement: max = 100%; min = 5%
	c. Last movement: max = 50; min = 0
	d. Type 0 pref.: max = 100; min = 0
	e. Type 1 pref.: max = 100; min = 0

3. Policy instrument potential - definition based on the previously defined exogenous parameters
	a. Vision: +/- 1 with min and max in mind
	b. Movement: +/- 5% with min and max in mind
	c. Last movement: +/-1 with min and max in mind
	d. T0P: +/- 5% with min and max in mind
	e. T1P: +/- 5% with min and max in mind

4. Policy instrument - exact policy instrument considered per policy family
	a. Policy family 1 - Movement:
		1. Vision: -1
		2. Vision: +1 
		3. Movement: -5% 
		4. Movement: +5% 
		5. Last movement: -1
		6. Last movement: +1 
	b. Policy family 2 - Happiness:
		7. Vision: - 1
		8. Vision: + 1
		9. T0P: - 5% 
		10. T0P: + 5% 
		11. T1P: - 5% 
		12. T1P: + 5% 

5. Impact of policy instrument - Calculation of the impacts
	The calculation of the impacts of the policy instruments on the beliefs of the agents (or at least the truth agent beliefs) can only be calculated through the simulation of the segregation model with a certain set of agents (benchmark model). Such simulation would have to be done for a number of tick equal to the number of tick the segregation model is run between times the policy emergence model ticks.
'''