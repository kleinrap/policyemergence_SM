import csv
import pandas as pd

test = pd.read_csv('input_beliefProfiles', sep=',')

print(test)
print(test.iloc[0].tolist())