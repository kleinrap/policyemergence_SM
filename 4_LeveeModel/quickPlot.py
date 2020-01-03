import matplotlib.pyplot as plt
import pandas as pd


data_read = pd.read_csv('O_L1_model_Sce1_Exp0_Run7.csv', sep=',')

plt.figure()
plt.title('Levees')
plt.plot(data_read['Designed Levees'])
plt.plot(data_read['Old Levees'])
plt.plot(data_read['Standard Levees'])
plt.legend()

plt.figure()
plt.title('planning horizon')
plt.plot(data_read['planning horizon'])
plt.plot(data_read['renovation standard'])
plt.plot(data_read['construction time'])
plt.legend()

plt.figure()
plt.title('safety')
plt.plot(data_read['Safety OL'])
plt.plot(data_read['Safety SL'])
plt.legend()

plt.figure()
plt.plot(data_read['perceived current safety'])

plt.figure()
plt.plot(data_read['flooding'])

plt.legend()
plt.show()