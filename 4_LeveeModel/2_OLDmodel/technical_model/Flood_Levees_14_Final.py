"""
Python model "Flood_Levees_14_Final.py"
Translated using PySD version 0.8.3
"""
from __future__ import division
import numpy as np
from pysd import utils
import xarray as xr

from pysd.py_backend.functions import cache
from pysd.py_backend import functions

_subscript_dict = {}

_namespace = {
    'TIME': 'time',
    'Time': 'time',
    'size of flood': 'size_of_flood',
    'flood height': 'flood_height',
    'flood perception time': 'flood_perception_time',
    'Current Safety Standard': 'current_safety_standard',
    'perceived current safety': 'perceived_current_safety',
    'planning horizon': 'planning_horizon',
    'fractional difference': 'fractional_difference',
    'informed opinion adjustment': 'informed_opinion_adjustment',
    'Anticipated Flood Level': 'anticipated_flood_level',
    'pulse if flood': 'pulse_if_flood',
    'loss of perceived safety by flooding': 'loss_of_perceived_safety_by_flooding',
    'designing rate': 'designing_rate',
    'effect of size of flood': 'effect_of_size_of_flood',
    'renovating rate': 'renovating_rate',
    'fractional change in anticipated flood level': 'fractional_change_in_anticipated_flood_level',
    'design safety standard': 'design_safety_standard',
    'Safety OL': 'safety_ol',
    'effect on renovation and construction': 'effect_on_renovation_and_construction',
    'desired safety of existing levees': 'desired_safety_of_existing_levees',
    'flooding': 'flooding',
    'safety owing to levee quality': 'safety_owing_to_levee_quality',
    'official current safety': 'official_current_safety',
    'length safety': 'length_safety',
    'change in safety due to renovation': 'change_in_safety_due_to_renovation',
    'expected obsolesence': 'expected_obsolesence',
    'additional safety from renovating': 'additional_safety_from_renovating',
    'Safety SL': 'safety_sl',
    'discrepancy in safety owing to levee length': 'discrepancy_in_safety_owing_to_levee_length',
    'additional safety from constructing': 'additional_safety_from_constructing',
    'decrease in safety of old levees': 'decrease_in_safety_of_old_levees',
    'average safety of old levees': 'average_safety_of_old_levees',
    'average safety of standard levees': 'average_safety_of_standard_levees',
    'Standard Levees': 'standard_levees',
    'change in safety of standard levees': 'change_in_safety_of_standard_levees',
    'constructing rate': 'constructing_rate',
    'design time': 'design_time',
    'Designed Levees': 'designed_levees',
    'adjustment time': 'adjustment_time',
    'discrepancy in levee length': 'discrepancy_in_levee_length',
    'desired current total safety': 'desired_current_total_safety',
    'Old Levees': 'old_levees',
    'renovation standard': 'renovation_standard',
    'renovation time': 'renovation_time',
    'aging rate': 'aging_rate',
    'aging time': 'aging_time',
    'construction time': 'construction_time',
    'length of levees': 'length_of_levees',
    'minimum length of levees': 'minimum_length_of_levees',
    'obsolescence time': 'obsolescence_time',
    'obsolesence rate': 'obsolesence_rate',
    'FINAL TIME': 'final_time',
    'INITIAL TIME': 'initial_time',
    'SAVEPER': 'saveper',
    'TIME STEP': 'time_step'
}

__pysd_version__ = "0.8.3"


@cache('step')
def size_of_flood():
    """
    size of flood

    m/km

    component


    """
    return flood_height() * pulse_if_flood()


@cache('run')
def flood_height():
    """
    flood height

    m/km

    constant


    """
    return 10


@cache('run')
def flood_perception_time():
    """
    flood perception time

    Year

    constant

    roughly 6 months
    """
    return 0.5


@cache('step')
def current_safety_standard():
    """
    Current Safety Standard

    m/km

    component


    """
    return integ_current_safety_standard()


@cache('step')
def perceived_current_safety():
    """
    perceived current safety

    Dmnl

    component


    """
    return integ_perceived_current_safety()


@cache('run')
def planning_horizon():
    """
    planning horizon

    Year

    constant


    """
    return 55


@cache('step')
def fractional_difference():
    """
    fractional difference

    1

    component


    """
    return (design_safety_standard() - current_safety_standard()) / current_safety_standard()


@cache('step')
def informed_opinion_adjustment():
    """
    informed opinion adjustment

    1/Year

    component


    """
    return (official_current_safety() - perceived_current_safety()) / adjustment_time()


@cache('step')
def anticipated_flood_level():
    """
    Anticipated Flood Level

    m/km

    component


    """
    return integ_anticipated_flood_level()


@cache('step')
def pulse_if_flood():
    """
    pulse if flood

    1

    component

    PULSE IF gives a value of 1 for one week at year 30
    """
    return functions.pulse(initial_time() + 7, 0.019231)


@cache('step')
def loss_of_perceived_safety_by_flooding():
    """
    loss of perceived safety by flooding

    1/Year

    component


    """
    return perceived_current_safety() * flooding() / flood_perception_time()


@cache('step')
def designing_rate():
    """
    designing rate

    km/Year

    component


    """
    return np.maximum(
        (((discrepancy_in_levee_length() - designed_levees() + expected_obsolesence()
           ) * effect_on_renovation_and_construction()) / design_time()), 0)


@cache('step')
def effect_of_size_of_flood():
    """
    effect of size of flood

    1/Year

    component


    """
    return (np.maximum(size_of_flood() - anticipated_flood_level(), 0)) / (
        anticipated_flood_level() * design_time())


@cache('step')
def renovating_rate():
    """
    renovating rate

    km/Year

    component


    """
    return old_levees() * renovation_standard() * effect_on_renovation_and_construction(
    ) / renovation_time()


@cache('run')
def fractional_change_in_anticipated_flood_level():
    """
    fractional change in anticipated flood level

    1/Year

    constant

    0.5 in 50 years
    """
    return 0.0035


@cache('step')
def design_safety_standard():
    """
    design safety standard

    m/km

    component


    """
    return anticipated_flood_level() * 1.08


@cache('step')
def safety_ol():
    """
    Safety OL

    m

    component


    """
    return integ_safety_ol()


@cache('step')
def effect_on_renovation_and_construction():
    """
    effect on renovation and construction

    Dmnl

    component


    """
    return functions.lookup(perceived_current_safety(),
                            [0, 0.25, 0.5, 0.75, 0.85, 1, 1.25, 1.5, 2, 4, 5],
                            [5, 3.5, 2, 1.2, 0.9, 0.7, 0.35, 0.2, 0.1, 0.1, 0.1])


@cache('step')
def desired_safety_of_existing_levees():
    """
    desired safety of existing levees

    m

    component


    """
    return length_of_levees() * current_safety_standard()


@cache('step')
def flooding():
    """
    flooding

    1

    component

    % flooded
    """
    return (np.maximum(
        (1 - length_safety()),
        (functions.if_then_else(size_of_flood() > average_safety_of_old_levees(),
                                (1 - official_current_safety()), 0)))) * pulse_if_flood() * 100


@cache('step')
def safety_owing_to_levee_quality():
    """
    safety owing to levee quality

    1

    component


    """
    return ((old_levees() * average_safety_of_old_levees()) +
            (standard_levees() * average_safety_of_standard_levees())
            ) / desired_safety_of_existing_levees()


@cache('step')
def official_current_safety():
    """
    official current safety

    1

    component


    """
    return np.minimum(length_safety(), safety_owing_to_levee_quality())


@cache('step')
def length_safety():
    """
    length safety

    Dmnl

    component

    Near to zero, very unsafe as very few levees. Near to 1, or 1, safe as 100% 
        surrounded by levees                Practically equivalent to ratio of length of levees/ minimum length of 
        levees
    """
    return (desired_current_total_safety() - discrepancy_in_safety_owing_to_levee_length()
            ) / desired_current_total_safety()


@cache('step')
def change_in_safety_due_to_renovation():
    """
    change in safety due to renovation

    m/Year

    component


    """
    return average_safety_of_old_levees() * renovating_rate()


@cache('step')
def expected_obsolesence():
    """
    expected obsolesence

    km

    component


    """
    return obsolesence_rate() * construction_time()


@cache('step')
def additional_safety_from_renovating():
    """
    additional safety from renovating

    m/Year

    component


    """
    return renovating_rate() * current_safety_standard() * 1.05


@cache('step')
def safety_sl():
    """
    Safety SL

    m

    component


    """
    return integ_safety_sl()


@cache('step')
def discrepancy_in_safety_owing_to_levee_length():
    """
    discrepancy in safety owing to levee length

    m

    component


    """
    return discrepancy_in_levee_length() * current_safety_standard()


@cache('step')
def additional_safety_from_constructing():
    """
    additional safety from constructing

    m/Year

    component


    """
    return constructing_rate() * design_safety_standard()


@cache('step')
def decrease_in_safety_of_old_levees():
    """
    decrease in safety of old levees

    m/Year

    component


    """
    return average_safety_of_old_levees() * obsolesence_rate()


@cache('step')
def average_safety_of_old_levees():
    """
    average safety of old levees

    m/km

    component


    """
    return safety_ol() / old_levees()


@cache('step')
def average_safety_of_standard_levees():
    """
    average safety of standard levees

    m/km

    component


    """
    return safety_sl() / standard_levees()


@cache('step')
def standard_levees():
    """
    Standard Levees

    km

    component


    """
    return integ_standard_levees()


@cache('step')
def change_in_safety_of_standard_levees():
    """
    change in safety of standard levees

    m/Year

    component


    """
    return average_safety_of_standard_levees() * aging_rate()


@cache('step')
def constructing_rate():
    """
    constructing rate

    km/Year

    component


    """
    return designed_levees() / construction_time()


@cache('run')
def design_time():
    """
    design time

    Year

    constant


    """
    return 2.5


@cache('step')
def designed_levees():
    """
    Designed Levees

    km

    component


    """
    return integ_designed_levees()


@cache('run')
def adjustment_time():
    """
    adjustment time

    Year

    constant


    """
    return 30


@cache('step')
def discrepancy_in_levee_length():
    """
    discrepancy in levee length

    km

    component


    """
    return np.maximum(minimum_length_of_levees() - length_of_levees(), 0)


@cache('step')
def desired_current_total_safety():
    """
    desired current total safety

    m

    component


    """
    return minimum_length_of_levees() * current_safety_standard()


@cache('step')
def old_levees():
    """
    Old Levees

    km

    component


    """
    return integ_old_levees()


@cache('run')
def renovation_standard():
    """
    renovation standard

    Dmnl

    constant

    20 % of Old Levees are under renovation at any one time. It takes 
        'renovation time' to do this.
    """
    return 0.2


@cache('run')
def renovation_time():
    """
    renovation time

    Year

    constant


    """
    return 3.5


@cache('step')
def aging_rate():
    """
    aging rate

    km/Year

    component


    """
    return standard_levees() / aging_time()


@cache('run')
def aging_time():
    """
    aging time

    Year

    constant


    """
    return 20


@cache('run')
def construction_time():
    """
    construction time

    Year

    constant


    """
    return 5


@cache('step')
def length_of_levees():
    """
    length of levees

    km

    component


    """
    return standard_levees() + old_levees()


@cache('run')
def minimum_length_of_levees():
    """
    minimum length of levees

    km

    constant


    """
    return 12000


@cache('run')
def obsolescence_time():
    """
    obsolescence time

    Year

    constant


    """
    return 25


@cache('step')
def obsolesence_rate():
    """
    obsolesence rate

    km/Year

    component


    """
    return old_levees() / obsolescence_time()


@cache('run')
def final_time():
    """
    FINAL TIME

    Year

    constant

    The final time for the simulation.
    """
    return 20


@cache('run')
def initial_time():
    """
    INITIAL TIME

    Year

    constant

    The initial time for the simulation.
    """
    return 0


@cache('step')
def saveper():
    """
    SAVEPER

    Year [0,?]

    component

    The frequency with which output is stored.
    """
    return time_step()


@cache('run')
def time_step():
    """
    TIME STEP

    Year [0,?]

    constant

    The time step for the simulation.
    """
    return 0.0078125


integ_current_safety_standard = functions.Integ(
    lambda: (current_safety_standard() * fractional_difference()) / planning_horizon(), lambda: 7)

integ_perceived_current_safety = functions.Integ(
    lambda: informed_opinion_adjustment() - loss_of_perceived_safety_by_flooding(),
    lambda: length_safety())


integ_anticipated_flood_level = functions.Integ(lambda: anticipated_flood_level()*(fractional_change_in_anticipated_flood_level()+effect_of_size_of_flood()), lambda: current_safety_standard()*0.98)


integ_safety_ol = functions.Integ(lambda: change_in_safety_of_standard_levees()-change_in_safety_due_to_renovation()-decrease_in_safety_of_old_levees(), lambda: 5)


integ_safety_sl = functions.Integ(lambda: additional_safety_from_constructing()+additional_safety_from_renovating()-change_in_safety_of_standard_levees(), lambda: 7)

integ_standard_levees = functions.Integ(
    lambda: constructing_rate() + renovating_rate() - aging_rate(), lambda: 1)

integ_designed_levees = functions.Integ(lambda: designing_rate() - constructing_rate(), lambda: 1)

integ_old_levees = functions.Integ(lambda: aging_rate() - obsolesence_rate() - renovating_rate(),
                                   lambda: 4500)
