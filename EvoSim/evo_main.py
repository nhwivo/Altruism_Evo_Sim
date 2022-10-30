############################################################
# DESCRIPTION
############################################################

import argparse
import os
from Simulation import *

# COMMAND LINE ARGUMENTS:
parser = argparse.ArgumentParser()
# required parameters/inputs:
parser.add_argument("startPop", help="")
parser.add_argument("totalDays", help="")
# optional parameters/inputs:
parser.add_argument("-a","--aa", help="") 
parser.add_argument("-b","--bb", help="") 
args = parser.parse_args()

# PARAMETERS FOR THE SIMULATION: 
sim_mode = 1
run_num = 1

# PROCESSING OPTIONAL ARGUMENTS 

# RUNNING THE SIMULATION 
if __name__ == '__main__':
    My_Sim = Simulation(args.startPop, args.totalDays, run_num)  # Initialize Simulation 
    My_Sim.run_sim(sim_mode)  # run the simulation 
    My_Sim.save_data()