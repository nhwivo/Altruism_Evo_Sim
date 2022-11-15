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
parser.add_argument("startPop", help="Number of starting individuals in the population.")
parser.add_argument("totalDays", help="Number of days to run the Simulation.")
parser.add_argument("repeatNum", help="Number of times to run the Simulation.")
# optional parameters/inputs:  
parser.add_argument("-b","--bb", help="") 
args = parser.parse_args()

# OBTAIN PARAMETERS FOR THE SIMULATION: 
OUT_FNAME = config['OUT_FNAME']

# RUNNING THE SIMULATION 
if __name__ == '__main__':
    My_Sim = Simulation(args.startPop, args.totalDays, args.repeatNum)  # Initialize Simulation 
    My_Sim.run_sim()  # run the simulation 
    My_Sim.save_data(OUT_FNAME)