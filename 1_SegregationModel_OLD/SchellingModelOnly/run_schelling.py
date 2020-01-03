from model_schelling import Schelling
import matplotlib.pyplot as plt
import numpy as np

model_run = Schelling(20, 20, 0.75, 0.4)

for i in range(100):
	if model_run.happy != model_run.schedule.get_agent_count():
		print("Step: ", i)
		model_run.step()

dataPlot = model_run.datacollector.get_model_vars_dataframe()

print(dataPlot)
dataPlot.plot("step", "evenness")
dataPlot.plot("step", "happy")

# dataPlot.plot()
plt.show()