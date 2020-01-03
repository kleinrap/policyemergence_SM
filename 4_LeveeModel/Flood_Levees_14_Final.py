"""
Python model "Flood_Levees_14_Final.py"
Translated using PySD version 0.9.0
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

__pysd_version__ = "0.9.0"


@cache('step')
def size_of_flood():
    """
    Real Name: size of flood
    Original Eqn: flood height*pulse if flood
    Units: m/km
    Limits: (None, None)
    Type: component


    """
    return flood_height() * pulse_if_flood()


@cache('run')
def flood_height():
    """
    Real Name: flood height
    Original Eqn: 0
    Units: m/km
    Limits: (None, None)
    Type: constant


    """
    return 0


@cache('run')
def flood_perception_time():
    """
    Real Name: flood perception time
    Original Eqn: 0.5
    Units: Year
    Limits: (None, None)
    Type: constant

    roughly 6 months
    """
    return 0.5


@cache('step')
def current_safety_standard():
    """
    Real Name: Current Safety Standard
    Original Eqn: INTEG ( (Current Safety Standard*fractional difference)/planning horizon, 7)
    Units: m/km
    Limits: (None, None)
    Type: component


    """
    return integ_current_safety_standard()


@cache('step')
def perceived_current_safety():
    """
    Real Name: perceived current safety
    Original Eqn: INTEG ( informed opinion adjustment-loss of perceived safety by flooding, length safety)
    Units: Dmnl
    Limits: (None, None)
    Type: component


    """
    return integ_perceived_current_safety()


@cache('run')
def planning_horizon():
    """
    Real Name: planning horizon
    Original Eqn: 55
    Units: Year
    Limits: (None, None)
    Type: constant


    """
    return 55


@cache('step')
def fractional_difference():
    """
    Real Name: fractional difference
    Original Eqn: (design safety standard-Current Safety Standard)/Current Safety Standard
    Units: 1
    Limits: (None, None)
    Type: component


    """
    return (design_safety_standard() - current_safety_standard()) / current_safety_standard()


@cache('step')
def informed_opinion_adjustment():
    """
    Real Name: informed opinion adjustment
    Original Eqn: (official current safety-perceived current safety)/adjustment time
    Units: 1/Year
    Limits: (None, None)
    Type: component


    """
    return (official_current_safety() - perceived_current_safety()) / adjustment_time()


@cache('step')
def anticipated_flood_level():
    """
    Real Name: Anticipated Flood Level
    Original Eqn: INTEG ( Anticipated Flood Level*(fractional change in anticipated flood level+effect of size of flood\ ), Current Safety Standard*0.98)
    Units: m/km
    Limits: (None, None)
    Type: component


    """
    return integ_anticipated_flood_level()


@cache('step')
def pulse_if_flood():
    """
    Real Name: pulse if flood
    Original Eqn: PULSE TRAIN( 40 , 0.2 , 3 , 50 )
    Units: 1
    Limits: (None, None)
    Type: component

    PULSE IF gives a value of 1 for one week at year 30
    """
    return functions.pulse_train(40, 0.2, 3, 50)


@cache('step')
def loss_of_perceived_safety_by_flooding():
    """
    Real Name: loss of perceived safety by flooding
    Original Eqn: perceived current safety*flooding/flood perception time
    Units: 1/Year
    Limits: (None, None)
    Type: component


    """
    return perceived_current_safety() * flooding() / flood_perception_time()


@cache('step')
def designing_rate():
    """
    Real Name: designing rate
    Original Eqn: MAX((((discrepancy in levee length - Designed Levees + expected obsolesence)*effect on renovation and construction )/design time), 0)
    Units: km/Year
    Limits: (None, None)
    Type: component


    """
    return np.maximum(
        (((discrepancy_in_levee_length() - designed_levees() + expected_obsolesence()) *
          effect_on_renovation_and_construction()) / design_time()), 0)


@cache('step')
def effect_of_size_of_flood():
    """
    Real Name: effect of size of flood
    Original Eqn: (MAX(size of flood-Anticipated Flood Level,0))/(Anticipated Flood Level*design time)
    Units: 1/Year
    Limits: (None, None)
    Type: component


    """
    return (np.maximum(size_of_flood() - anticipated_flood_level(),
                       0)) / (anticipated_flood_level() * design_time())


@cache('step')
def renovating_rate():
    """
    Real Name: renovating rate
    Original Eqn: Old Levees * renovation standard* effect on renovation and construction/renovation time
    Units: km/Year
    Limits: (None, None)
    Type: component


    """
    return old_levees() * renovation_standard() * effect_on_renovation_and_construction(
    ) / renovation_time()


@cache('run')
def fractional_change_in_anticipated_flood_level():
    """
    Real Name: fractional change in anticipated flood level
    Original Eqn: 0.0035
    Units: 1/Year
    Limits: (None, None)
    Type: constant

    0.5 in 50 years
    """
    return 0.0035


@cache('step')
def design_safety_standard():
    """
    Real Name: design safety standard
    Original Eqn: Anticipated Flood Level*1.08
    Units: m/km
    Limits: (None, None)
    Type: component


    """
    return anticipated_flood_level() * 1.08


@cache('step')
def safety_ol():
    """
    Real Name: Safety OL
    Original Eqn: INTEG ( change in safety of standard levees-change in safety due to renovation-decrease in safety of old levees\ , 5)
    Units: m
    Limits: (None, None)
    Type: component


    """
    return integ_safety_ol()


@cache('step')
def effect_on_renovation_and_construction():
    """
    Real Name: effect on renovation and construction
    Original Eqn: WITH LOOKUP ( perceived current safety, ([(0,0)-(10,10)],(0,5),(0.25,3.5),(0.5,2),(0.75,1.2),(0.85,0.9),(1,0.7),(1.25,0.35)\ ,(1.5,0.2),(2,0.1),(4,0.1),(5,0.1) ))
    Units: Dmnl
    Limits: (None, None)
    Type: component


    """
    return functions.lookup(perceived_current_safety(),
                            [0, 0.25, 0.5, 0.75, 0.85, 1, 1.25, 1.5, 2, 4, 5],
                            [5, 3.5, 2, 1.2, 0.9, 0.7, 0.35, 0.2, 0.1, 0.1, 0.1])


@cache('step')
def desired_safety_of_existing_levees():
    """
    Real Name: desired safety of existing levees
    Original Eqn: length of levees*Current Safety Standard
    Units: m
    Limits: (None, None)
    Type: component


    """
    return length_of_levees() * current_safety_standard()


@cache('step')
def flooding():
    """
    Real Name: flooding
    Original Eqn: (MAX((1-length safety) , (IF THEN ELSE( size of flood > average safety of old levees\ , (1-official current safety) , 0))))*pulse if flood *100
    Units: 1
    Limits: (None, None)
    Type: component

    % flooded
    """
    return (np.maximum(
        (1 - length_safety()),
        (functions.if_then_else(size_of_flood() > average_safety_of_old_levees(),
                                (1 - official_current_safety()), 0)))) * pulse_if_flood() * 100


@cache('step')
def safety_owing_to_levee_quality():
    """
    Real Name: safety owing to levee quality
    Original Eqn: ((Old Levees*average safety of old levees) + (Standard Levees*average safety of standard levees\ ))/desired safety of existing levees
    Units: 1
    Limits: (None, None)
    Type: component


    """
    return ((old_levees() * average_safety_of_old_levees()) +
            (standard_levees() * average_safety_of_standard_levees())
            ) / desired_safety_of_existing_levees()


@cache('step')
def official_current_safety():
    """
    Real Name: official current safety
    Original Eqn: MIN(length safety,safety owing to levee quality)
    Units: 1
    Limits: (None, None)
    Type: component


    """
    return np.minimum(length_safety(), safety_owing_to_levee_quality())


@cache('step')
def length_safety():
    """
    Real Name: length safety
    Original Eqn: (desired current total safety - discrepancy in safety owing to levee length)/desired current total safety
    Units: Dmnl
    Limits: (None, None)
    Type: component

    Near to zero, very unsafe as very few levees. Near to 1, or 1, safe as 100% 
        surrounded by levees                Practically equivalent to ratio of length of levees/ minimum length of 
        levees
    """
    return (desired_current_total_safety() -
            discrepancy_in_safety_owing_to_levee_length()) / desired_current_total_safety()


@cache('step')
def change_in_safety_due_to_renovation():
    """
    Real Name: change in safety due to renovation
    Original Eqn: average safety of old levees*renovating rate
    Units: m/Year
    Limits: (None, None)
    Type: component


    """
    return average_safety_of_old_levees() * renovating_rate()


@cache('step')
def expected_obsolesence():
    """
    Real Name: expected obsolesence
    Original Eqn: obsolesence rate*construction time
    Units: km
    Limits: (None, None)
    Type: component


    """
    return obsolesence_rate() * construction_time()


@cache('step')
def additional_safety_from_renovating():
    """
    Real Name: additional safety from renovating
    Original Eqn: renovating rate*Current Safety Standard*1.05
    Units: m/Year
    Limits: (None, None)
    Type: component


    """
    return renovating_rate() * current_safety_standard() * 1.05


@cache('step')
def safety_sl():
    """
    Real Name: Safety SL
    Original Eqn: INTEG ( additional safety from constructing+additional safety from renovating-change in safety of standard levees\ , 7)
    Units: m
    Limits: (None, None)
    Type: component


    """
    return integ_safety_sl()


@cache('step')
def discrepancy_in_safety_owing_to_levee_length():
    """
    Real Name: discrepancy in safety owing to levee length
    Original Eqn: discrepancy in levee length*Current Safety Standard
    Units: m
    Limits: (None, None)
    Type: component


    """
    return discrepancy_in_levee_length() * current_safety_standard()


@cache('step')
def additional_safety_from_constructing():
    """
    Real Name: additional safety from constructing
    Original Eqn: constructing rate*design safety standard
    Units: m/Year
    Limits: (None, None)
    Type: component


    """
    return constructing_rate() * design_safety_standard()


@cache('step')
def decrease_in_safety_of_old_levees():
    """
    Real Name: decrease in safety of old levees
    Original Eqn: average safety of old levees *obsolesence rate
    Units: m/Year
    Limits: (None, None)
    Type: component


    """
    return average_safety_of_old_levees() * obsolesence_rate()


@cache('step')
def average_safety_of_old_levees():
    """
    Real Name: average safety of old levees
    Original Eqn: Safety OL/Old Levees
    Units: m/km
    Limits: (None, None)
    Type: component


    """
    return safety_ol() / old_levees()


@cache('step')
def average_safety_of_standard_levees():
    """
    Real Name: average safety of standard levees
    Original Eqn: Safety SL/Standard Levees
    Units: m/km
    Limits: (None, None)
    Type: component


    """
    return safety_sl() / standard_levees()


@cache('step')
def standard_levees():
    """
    Real Name: Standard Levees
    Original Eqn: INTEG ( constructing rate+renovating rate-aging rate, 1)
    Units: km
    Limits: (None, None)
    Type: component


    """
    return integ_standard_levees()


@cache('step')
def change_in_safety_of_standard_levees():
    """
    Real Name: change in safety of standard levees
    Original Eqn: average safety of standard levees * aging rate
    Units: m/Year
    Limits: (None, None)
    Type: component


    """
    return average_safety_of_standard_levees() * aging_rate()


@cache('step')
def constructing_rate():
    """
    Real Name: constructing rate
    Original Eqn: Designed Levees/construction time
    Units: km/Year
    Limits: (None, None)
    Type: component


    """
    return designed_levees() / construction_time()


@cache('run')
def design_time():
    """
    Real Name: design time
    Original Eqn: 2.5
    Units: Year
    Limits: (None, None)
    Type: constant


    """
    return 2.5


@cache('step')
def designed_levees():
    """
    Real Name: Designed Levees
    Original Eqn: INTEG ( designing rate-constructing rate, 1)
    Units: km
    Limits: (None, None)
    Type: component


    """
    return integ_designed_levees()


@cache('run')
def adjustment_time():
    """
    Real Name: adjustment time
    Original Eqn: 30
    Units: Year
    Limits: (None, None)
    Type: constant


    """
    return 30


@cache('step')
def discrepancy_in_levee_length():
    """
    Real Name: discrepancy in levee length
    Original Eqn: MAX(minimum length of levees-length of levees,0)
    Units: km
    Limits: (None, None)
    Type: component


    """
    return np.maximum(minimum_length_of_levees() - length_of_levees(), 0)


@cache('step')
def desired_current_total_safety():
    """
    Real Name: desired current total safety
    Original Eqn: minimum length of levees*Current Safety Standard
    Units: m
    Limits: (None, None)
    Type: component


    """
    return minimum_length_of_levees() * current_safety_standard()


@cache('step')
def old_levees():
    """
    Real Name: Old Levees
    Original Eqn: INTEG ( aging rate-obsolesence rate-renovating rate, 4500)
    Units: km
    Limits: (None, None)
    Type: component


    """
    return integ_old_levees()


@cache('run')
def renovation_standard():
    """
    Real Name: renovation standard
    Original Eqn: 0.2
    Units: Dmnl
    Limits: (None, None)
    Type: constant

    20 % of Old Levees are under renovation at any one time. It takes 
        'renovation time' to do this.
    """
    return 0.2


@cache('run')
def renovation_time():
    """
    Real Name: renovation time
    Original Eqn: 3.5
    Units: Year
    Limits: (None, None)
    Type: constant


    """
    return 3.5


@cache('step')
def aging_rate():
    """
    Real Name: aging rate
    Original Eqn: Standard Levees/aging time
    Units: km/Year
    Limits: (None, None)
    Type: component


    """
    return standard_levees() / aging_time()


@cache('run')
def aging_time():
    """
    Real Name: aging time
    Original Eqn: 20
    Units: Year
    Limits: (None, None)
    Type: constant


    """
    return 20


@cache('run')
def construction_time():
    """
    Real Name: construction time
    Original Eqn: 5
    Units: Year
    Limits: (None, None)
    Type: constant


    """
    return 5


@cache('step')
def length_of_levees():
    """
    Real Name: length of levees
    Original Eqn: Standard Levees + Old Levees
    Units: km
    Limits: (None, None)
    Type: component


    """
    return standard_levees() + old_levees()


@cache('run')
def minimum_length_of_levees():
    """
    Real Name: minimum length of levees
    Original Eqn: 12000
    Units: km
    Limits: (None, None)
    Type: constant


    """
    return 12000


@cache('run')
def obsolescence_time():
    """
    Real Name: obsolescence time
    Original Eqn: 25
    Units: Year
    Limits: (None, None)
    Type: constant


    """
    return 25


@cache('step')
def obsolesence_rate():
    """
    Real Name: obsolesence rate
    Original Eqn: Old Levees/obsolescence time
    Units: km/Year
    Limits: (None, None)
    Type: component


    """
    return old_levees() / obsolescence_time()


@cache('run')
def final_time():
    """
    Real Name: FINAL TIME
    Original Eqn: 20
    Units: Year
    Limits: (None, None)
    Type: constant

    The final time for the simulation.
    """
    return 20


@cache('run')
def initial_time():
    """
    Real Name: INITIAL TIME
    Original Eqn: 0
    Units: Year
    Limits: (None, None)
    Type: constant

    The initial time for the simulation.
    """
    return 0


@cache('step')
def saveper():
    """
    Real Name: SAVEPER
    Original Eqn: TIME STEP
    Units: Year
    Limits: (0.0, None)
    Type: component

    The frequency with which output is stored.
    """
    return time_step()


@cache('run')
def time_step():
    """
    Real Name: TIME STEP
    Original Eqn: 0.0078125
    Units: Year
    Limits: (0.0, None)
    Type: constant

    The time step for the simulation.
    """
    return 0.0078125


integ_current_safety_standard = functions.Integ(
    lambda: (current_safety_standard() * fractional_difference()) / planning_horizon(), lambda: 7)

integ_perceived_current_safety = functions.Integ(
    lambda: informed_opinion_adjustment() - loss_of_perceived_safety_by_flooding(), lambda:
    length_safety())

integ_anticipated_flood_level = functions.Integ(
    lambda: anticipated_flood_level() * (fractional_change_in_anticipated_flood_level(
    ) + effect_of_size_of_flood()), lambda: current_safety_standard() * 0.98)

integ_safety_ol = functions.Integ(
    lambda: change_in_safety_of_standard_levees() - change_in_safety_due_to_renovation() -
    decrease_in_safety_of_old_levees(), lambda: 5)

integ_safety_sl = functions.Integ(
    lambda: additional_safety_from_constructing() + additional_safety_from_renovating() -
    change_in_safety_of_standard_levees(), lambda: 7)

integ_standard_levees = functions.Integ(
    lambda: constructing_rate() + renovating_rate() - aging_rate(), lambda: 1)

integ_designed_levees = functions.Integ(lambda: designing_rate() - constructing_rate(), lambda: 1)

integ_old_levees = functions.Integ(lambda: aging_rate() - obsolesence_rate() - renovating_rate(),
                                   lambda: 4500)
