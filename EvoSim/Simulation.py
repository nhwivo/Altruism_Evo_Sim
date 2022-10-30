############################################################
# DESCRIPTION
############################################################

import copy
from Population import *
from settings import *


class Simulation():
    ####################################################################################################
    # INITIALIZING SIMULATION  
    def __init__(self, start_pop, total_days, total_runs):
        self.start_pop = int(start_pop)
        self.total_days = int(total_days)
        self.total_runs = int(total_runs)
        
        self.initialize_populations()  # create starting population 
        
    def initialize_populations(self):
        self.initialize_indpop()  # initialize the group of individuals of interest
        self.initialize_foodpop()  # initialize population of food source
        
    def initialize_indpop(self):
        self.og_individual_pop = IndividualPopulation(self.start_pop)  # population of individuals 
    
    def initialize_foodpop(self):
        foodpop_startnum = self.calculate_foodstartnum()  # calculate number of starting food sources
        self.og_food_pop = FoodPopulation(foodpop_startnum)  # population of food sources 
        
    def calculate_foodstartnum(self):
        """Calculate the number of starting food sources needed."""
        if INF_FOOD:  # if simulation has inifite food
            # create number of food sources needed for population num specified plus 3 sources extra
            fs_num = int((self.start_pop/4)+3)   
            return fs_num  
        if not INF_FOOD:  # run when IND_FOOD = False --> food is finite 
            return FOOD_SOURCE_AVAIL  # specified value in settings.py
    ####################################################################################################
    
    
    
    ####################################################################################################
    # RUNNING THE SIMULATION
    def run_sim(self, sim_mode):
        for _ in range(self.total_runs):
            # use the same starting population in each run 
            self.food_pop = copy.deepcopy(self.og_food_pop)  # create a duplicate population object
            self.individual_pop = copy.deepcopy(self.og_individual_pop)  # create a duplicate population object
            # run the simulation
            self.run_run()  # simulate specified number of runs/repeats 
            
        self.record_sim_data()  # record data of the whole simulation (all runs all days)
    
    def run_run(self):
        for _ in range(self.total_days):
            self.run_day()  # simulate the specified number of days 
        
        self.record_run_data()  # record data for the run/repeat
    
    
    
    
    def run_day(self): 
        self.reset_day()  # reset the day (ex: reset food availability) 
        self.populations_action()  # all populations perform action 
        self.record_day_data()  # record data of the day 
    
    def reset_day(self):
        """Reset certain variables in the simulation"""
        ind_popnum = len(self.individual_pop.pop_mem_list)
        self.food_pop.reset_food_day(ind_popnum)  # reset the food source population 
    
    def populations_action(self):
        self.individual_pop.execute_population_actions()  # individuals perform action
        self.food_pop.execute_population_actions()  # food sources perform action
    
    
    
    
    def record_day_data(self):
        """Record data after simulating 1 day."""
        self.individual_pop.record_day_popnum()  # record population number of individuals 
        self.food_pop.record_day_popnum()  # record population number of food sources 
    
    def record_run_data(self):
        """Record data of all days ran in 1 simulation repeat."""
        # record popnum of all days in the run 
        self.individual_pop.record_run_popnum()  
        self.food_pop.record_run_popnum()  
    
    def record_sim_data(self):
        pass
    ####################################################################################################

    
    
    ####################################################################################################
    # SIMULATION COMPLETE - SAVE DATA INTO A FILE 
    def save_data(self):
        pass
    ####################################################################################################

    
class SimulationMode1(Simulation):
    def __init__(self):
        pass

    
class SimulationMode2(Simulation):
    def __init__(self):
        pass

    
class SimulationMode3(Simulation):
    def __init__(self):
        pass