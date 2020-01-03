import pysd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# The line below is only needed when the model needs to be imported into Python.
model_flood = pysd.read_vensim('Flood_Levees_14_Final.mdl')

## The following are the elevent parameters 

time_step_SD = 0.0078125

# Notes:
# To output specific data, use: return_columns=['',''] filling in with the parameter names
# To input specific data, use: params={'':, '':}
# To start at a different point or to start from a freeze of the model, use: initial_condition='current', return_timestamps=range(20,40)

# stocks = model_flood.run(return_columns=['safety owing to levee quality', 'perceived current safety'], params={'construction time':10, 'FINAL TIME':time_step_SD})

stocks = model_flood.run(return_columns=['safety owing to levee quality', 'perceived current safety'], params={'construction time':10, 'FINAL TIME':5})

stocks2 = model_flood.run(return_columns=['safety owing to levee quality', 'perceived current safety'], params={'TIME STEP':0.0078125}, initial_condition='current', return_timestamps=np.linspace(5,20, int((20-5)/0.0078125)))

# print(stocks)
stocks.plot()
plt.xlim((0,20))
plt.ylim((0,1))


print('printing the last row only: \n', stocks2.loc['safety owing to levee quality'])
stocks2.plot()
plt.xlim((0,20))
plt.ylim((0,1))

stocks3 = stocks.append(stocks2)
stocks3.plot()
# print(stocks3)
plt.xlim((0,20))
plt.ylim((0,2))

# plt.show()