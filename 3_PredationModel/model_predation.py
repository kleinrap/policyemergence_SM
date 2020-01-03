'''
Wolf-Sheep Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
'''

import random

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from model_predation_agents import Sheep, Wolf, GrassPatch
from model_predation_schedule import RandomActivationByBreed

'''
For the policy process hybrid modelling

Belief tree:
- Deep core beliefs
    - None

- Policy core beliefs
    - Amount of sheep
    - Amount of wolves
    - Amount of fully grown grass
    
- Secondary beliefs
    - Reproduction rate sheep
    - Reproduction rate wolf
    - Grass regrowth time

Policy instruments:
- Change sheep reproduction rate (+/- 0.01)
- Change wolf reproduction rate (+/- 0.01)
- Change grass regrowth time (+/- 2)

'''

def get_sheep_count(model):
    count = model.schedule.get_breed_count(Sheep)
    return count

def get_wolf_count(model):
    count = model.schedule.get_breed_count(Wolf)
    return count

def get_grassPatch_fully_grown(model):
    count = 0
    for grass in model.schedule.agents_by_breed[GrassPatch]:
        if grass.fully_grown == True:
            count += 1
    return count

def get_sheep_repro(model):
    return model.sheep_reproduce

def get_wolf_repro(model):
    return model.wolf_reproduce

def get_grass_regrowth(model):
    return model.grass_regrowth_time

def get_sheep_change(model):
    return model.schedule.get_breed_count(Sheep) - model.sheep_pop_init

def get_wolf_change(model):
    return model.schedule.get_breed_count(Wolf) - model.wolf_pop_init

def get_grass_change(model):
    return get_grassPatch_fully_grown(model) - model.grass_pop_init

class WolfSheepPredation(Model):
    '''
    Wolf-Sheep Predation Model
    '''

    height = 50
    width = 50

    initial_sheep = 100
    initial_wolves = 50

    sheep_reproduce = 0.04
    wolf_reproduce = 0.05

    sheep_gain_from_food = 4
    wolf_gain_from_food = 30

    grass = True
    grass_regrowth_time = 35

    verbose = False  # Print-monitoring

    def __init__(self, height=50, width=50,
                 initial_sheep=100, initial_wolves=50,
                 sheep_reproduce=0.04, wolf_reproduce=0.05,
                 wolf_gain_from_food=30,
                 grass=True, grass_regrowth_time=30, sheep_gain_from_food=4):
        '''
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        '''

        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food

        self.stepCount = 0

        self.sheep_pop_init = 0
        self.wolf_pop_init = 0
        self.grass_pop_init = 0

        self.sheep_pop_change = 0
        self.wolf_pop_change = 0
        self.grass_pop_change = 0

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            model_reporters=
            {"Sheep": get_sheep_count,
             "Wolves": get_wolf_count,
             "Grass": get_grassPatch_fully_grown,
             "SheepChange": get_sheep_change,
             "WolfChange": get_wolf_change,
             "GrassChange": get_grass_change,
             "SheepRepro": get_sheep_repro,
             "WolfRepro": get_wolf_repro,
             "GrassRegrowth": get_grass_regrowth},
            agent_reporters=
            {"Wolves": lambda m: m.schedule.get_breed_count(Wolf),
             "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
             "GrassPatch": lambda m: m.schedule.get_breed_count(GrassPatch)})

        # Create sheep:
        for i in range(self.initial_sheep):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = random.randrange(2 * self.sheep_gain_from_food)
            sheep = Sheep((x, y), self, True, energy)
            self.grid.place_agent(sheep, (x, y))
            self.schedule.add(sheep)

        # Create wolves
        for i in range(self.initial_wolves):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = random.randrange(2 * self.wolf_gain_from_food)
            wolf = Wolf((x, y), self, True, energy)
            self.grid.place_agent(wolf, (x, y))
            self.schedule.add(wolf)

        # Create grass patches
        if self.grass:
            for agent, x, y in self.grid.coord_iter():

                fully_grown = random.choice([True, False])

                if fully_grown:
                    countdown = self.grass_regrowth_time
                else:
                    countdown = random.randrange(self.grass_regrowth_time)

                patch = GrassPatch((x, y), self, fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        self.running = True

    def policy_implementation(self, policy):

        # [SR] - Sheep reproduction
        if policy[0] != None and self.sheep_reproduce >= 0.01 and self.sheep_reproduce <= 0.49:
            self.sheep_reproduce += policy[0]

        # [WWR - Wolf reproduction
        if policy[1] != None and self.wolf_reproduce >= 0.01 and self.wolf_reproduce <= 0.49:
            self.wolf_reproduce += policy[1]

        # [GR] - Grass regrowth
        if policy[2] != None and self.grass_regrowth_time >= 2 and self.grass_regrowth_time <= 198:
            self.grass_regrowth_time += policy[2]

    def step(self, policy):

        self.policy_implementation(policy)

        if self.stepCount % 100 == 0:
            self.sheep_pop_init = self.schedule.get_breed_count(Sheep)
            self.wolf_pop_init = self.schedule.get_breed_count(Wolf)
            self.grass_pop_init = get_grassPatch_fully_grown(self)

        self.schedule.step()
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_breed_count(Wolf),
                   self.schedule.get_breed_count(Sheep),
                   get_grassPatch_fully_grown(self)])

        KPIs = self.KPI_calculation()
        self.stepCount += 1

        return KPIs

    def KPI_calculation(self):
        '''
        Calculation of the KPIs for the link to the policy process model
        :return:
        '''

        # sheep count
        sheep_max = 500
        sheep_min = 0
        if self.schedule.get_breed_count(Sheep) > sheep_max:
            PC1 = 1
        else:
            PC1 = round(self.schedule.get_breed_count(Sheep) / (sheep_max - sheep_min), 3)

        # wolf count
        wolf_max = 500
        wolf_min = 0
        if self.schedule.get_breed_count(Wolf) > wolf_max:
            PC2 = 1
        else:
            PC2 = round(self.schedule.get_breed_count(Wolf) / (wolf_max - wolf_min), 3)

        # grass count
        grass_max = self.height * self.width
        grass_min = 0
        PC3 = round(get_grassPatch_fully_grown(self) / (grass_max - grass_min), 3)

        # sheep pop. change
        SP_max = 100
        SP_min = -100
        SP_temp_max = abs(SP_min) + abs(SP_max)
        SP_temp_min = 0
        SP_change = self.schedule.get_breed_count(Sheep) - self.sheep_pop_init
        # print('SP_change', SP_change)
        if SP_change < SP_min:
            SP_change = SP_min
        if SP_change > SP_max:
            SP_change = SP_max
        S1 = round((SP_max + SP_change) / (SP_temp_max - SP_temp_min), 3)

        # wolf pop. change
        WP_max = 100
        WP_min = -100
        WP_temp_max = abs(WP_min) + abs(WP_max)
        WP_temp_min = 0
        WP_change = self.schedule.get_breed_count(Wolf) - self.wolf_pop_init
        # print('WP_change', WP_change)
        if WP_change < WP_min:
            WP_change = WP_min
        if WP_change > WP_max:
            WP_change = WP_max
        S2 = round((WP_max + WP_change) / (WP_temp_max - WP_temp_min), 3)

        # grass pop. change
        GR_max = 500
        GR_min = -500
        GR_temp_max = abs(GR_min) + abs(GR_max)
        GR_temp_min = 0
        GR_change = get_grassPatch_fully_grown(self) - self.grass_pop_init
        # print('GR_change', GR_change)
        if GR_change < GR_min:
            GR_change = GR_min
        if GR_change > GR_max:
            GR_change = GR_max
        S3 = round((GR_max + GR_change) / (GR_temp_max - GR_temp_min), 3)

        KPIs = [0, PC1, PC2, PC3, S1, S2, S3]

        return KPIs

    def run_model(self, step_count=1600):

        self.verbose = True

        if self.verbose:
            print('Initial number wolves: ',
                  self.schedule.get_breed_count(Wolf))
            print('Initial number sheep: ',
                  self.schedule.get_breed_count(Sheep))
            print('Initial number grass patches: ',
                  get_grassPatch_fully_grown(self))

        for i in range(step_count):
            policy = [None, None, None]
            self.step(policy)

        if self.verbose:
            print('')
            print('Final number wolves: ',
                  self.schedule.get_breed_count(Wolf))
            print('Final number sheep: ',
                  self.schedule.get_breed_count(Sheep))
            print('Initial number grass patches: ',
                  get_grassPatch_fully_grown(self))
