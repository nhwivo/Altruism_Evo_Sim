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