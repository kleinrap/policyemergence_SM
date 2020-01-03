from model_predation import WolfSheepPredation

repetitions_runs = 50

for rep_runs in range(repetitions_runs):

    model_wolfsheep = WolfSheepPredation() # intialisation of the model
    model_wolfsheep.run_model() # running the model

    # output of the data

    output = model_wolfsheep.datacollector.get_model_vars_dataframe()
    output.to_csv('O_Pre_alone_model_Run' + str(rep_runs) + '.csv')
