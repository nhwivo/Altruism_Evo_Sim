############################################################
# DESCRIPTION
############################################################

import argparse
import os
from Simulation import *
from settings import * 

# COMMAND LINE ARGUMENTS:
parser = argparse.ArgumentParser()
# required parameters/inputs:
parser.add_argument("startPop", help="")
parser.add_argument("totalDays", help="")
# optional parameters/inputs:
parser.add_argument("-a","--aa", help="") 
parser.add_argument("-b","--bb", help="") 
args = parser.parse_args()

# OBTAIN PARAMETERS FOR THE SIMULATION: 
RUN_NUM = config['RUN_NUM']
SIM_MODE = config['SIM_MODE']
OUT_FNAME = config['OUT_FNAME']


# RUNNING THE SIMULATION 
if __name__ == '__main__':
    My_Sim = Simulation(args.startPop, args.totalDays, RUN_NUM)  # Initialize Simulation 
    My_Sim.run_sim(SIM_MODE)  # run the simulation 
    My_Sim.save_data(OUT_FNAME)
    
    
    
    
    
#     print("All data below are from the end of the simulation.") 
#     print("")
#     print("Number of individuals: " + str(len(My_Sim.individual_pop.pop_mem_list)))
#     # print("List of individuals: " + str(My_Sim.individual_pop.pop_mem_list))
    
#     ind_stat = []  # status of individuals (alive/dead)
#     ind_age = []  # age of individuals 
#     for ind in My_Sim.individual_pop.pop_mem_list:
#         status, age = ind.status, ind.age
#         ind_stat.append(status)
#         ind_age.append(age)
        
#     print("Status of individuals - should be 1: " + str(ind_stat))
#     print("Age of individuals: " + str(ind_age))
#     print("")
#     print("Individual population number for all days and all runs: ")
#     print(My_Sim.individual_pop.popnum_all_runs)
#     print("")
    
#     print("Number of food sources: " + str(len(My_Sim.food_pop.pop_mem_list)))
#     # print("List of food sources: " + str(My_Sim.food_pop.pop_mem_list))
#     pred_presence, food_units = [], []
#     for fsource in My_Sim.food_pop.pop_mem_list:
#         presence = fsource.predator_presence
#         food_unit = fsource.food_unit
#         pred_presence.append(presence)
#         food_units.append(food_unit)
        
#     print("Predator presence in food source:  " + str(pred_presence))
#     print("Food unit - should be " + str(FOOD_UNIT) + ": " + str(food_units))
#     print("")
#     print("Food source population number for all days and all runs: ")
#     print(My_Sim.food_pop.popnum_all_runs)