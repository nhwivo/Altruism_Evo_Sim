########################################################################################################
# DESCRIPTION
########################################################################################################

import copy
import os
from Population import *
from settings import *


class Simulation():
    ####################################################################################################
    # INITIALIZE SIMULATION  
    def __init__(self, start_pop, total_days, total_runs):
        self.start_pop = int(start_pop)
        self.total_days = int(total_days)
        self.total_runs = int(total_runs)
        
        self.initialize_populations()  # create starting population 
        
    def initialize_populations(self):
        self.initialize_indpop()  # initialize the group of individuals of interest
        self.initialize_foodpop()  # initialize population of food source
        # exceptions to populations (based on sim_mode):
        self.edit_mode()
        
    def initialize_indpop(self):
        self.og_individual_pop = IndividualPopulation(self.start_pop)  # population of individuals 
    
    def initialize_foodpop(self):
        # foodpop_startnum = self.calculate_foodstartnum()  # calculate number of starting food sources
        self.og_food_pop = FoodPopulation((self.start_pop+3))  # population of food sources 
        
    def calculate_foodstartnum(self):
        """Calculate the number of starting food sources needed."""
        INF_FOOD = config['INF_FOOD']  # obtain value from config file 
        if INF_FOOD:  # if simulation has inifite food
            # create number of food sources needed for population num specified plus 3 sources extra
            fs_num = int((self.start_pop/4)+3)   
            return fs_num  
        if not INF_FOOD:  # run when IND_FOOD = False --> food is finite 
            return FOOD_SOURCE_AVAIL  # specified value in settings.py
        
    def edit_mode(self):
        """Changes to simulations based on different modes."""
        sim_mode = config["SIM_MODE"]
        if sim_mode == 3:
            self.edit_m3()  # edit variables to be suitable for mode 3 of simulation
            
    def edit_m3(self):
        """
        Change genes of those with altruistic trait to match with mode of simulation.
        NOTE: might not need this 
            - doesnt matter what the altruistic marker is - condition is based on altrusitic gene
        """
        # make all altruistic individuals have altruistic marker: 
        for member in self.og_individual_pop:
            if member.genes['altruism'] == 1:
                member.genes['altruistic marker'] = 1
    #    
    ####################################################################################################
    
    
    
    ####################################################################################################
    # RUN THE SIMULATION
    def run_sim(self):
        for _ in range(self.total_runs):
            # use the same starting population in each run 
            self.food_pop = copy.deepcopy(self.og_food_pop)  # create a duplicate population object
            self.individual_pop = copy.deepcopy(self.og_individual_pop)  # create a duplicate population object
            self.record_init_pop_data()  # record starting population data
            
            # run the simulation
            self.run_run()  # simulate a single run
            self.record_run_data()  # record data for the run/repeat
            
        self.record_sim_data()  # record data of the whole simulation (all runs all days)
    
    def run_run(self):
        for _ in range(self.total_days):
            self.run_day()  # simulate a single day
        
    def run_day(self): 
        self.reset_day()  # reset the day (ex: reset food availability) 
        self.populations_action()  # all populations perform action 
        self.record_day_data()  # record data of the day 
    
    def reset_day(self):
        """Reset certain variables in the simulation"""
        ind_popnum = len(self.individual_pop.pop_mem_list)
        self.food_pop.reset_food_day(ind_popnum)  # reset the food source population 
    
    def populations_action(self):
        """Execute actions of members within each population"""
        self.individual_pop.population_actions(self.food_pop)  # individuals perform action
        self.food_pop.population_actions()  # food sources perform action
    #
    ####################################################################################################
    # RECORD SIMULATION DATA 
    def record_init_pop_data(self):
        """Record starting population number."""
        self.individual_pop.record_day_popnum()
        self.individual_pop.record_day_allelefreq()
        self.food_pop.record_day_popnum()
    
    def record_day_data(self):
        """Record data after simulating 1 day."""
        # Record day population data: 
        self.individual_pop.record_day_popnum()  # record population number of individuals 
        self.og_individual_pop.popnum_all_days = self.individual_pop.popnum_all_days  # copy data
        
        self.food_pop.record_day_popnum()  # record population number of food sources 
        self.og_food_pop.popnum_all_days = self.food_pop.popnum_all_days  # copy data
        
        # Record day allele frequency: 
        self.individual_pop.record_day_allelefreq()  # record allele freq 
        # copy data (because individual_pop resets) 
        self.og_individual_pop.allelefreq_alldays = self.individual_pop.allelefreq_alldays
        
    
    def record_run_data(self):
        """Record data of all days ran in 1 simulation repeat."""
        # record popnum of all days in the run 
        self.og_food_pop.record_run_popnum()  
        self.og_individual_pop.record_run_popnum()  
        
        # record allele freq of all days in the run 
        self.og_individual_pop.record_run_allelefreq()
    
    def record_sim_data(self):
        """"""
        self.og_individual_pop.cal_pop_growth()  # calculate population growth 
    #
    ####################################################################################################

    
    
    ####################################################################################################
    # SIMULATION COMPLETE - SAVE DATA INTO A FILE 
    def save_data(self):
        OUT_FNAME = config['OUT_FNAME']
        self.obtain_colnames()  # obtain column names 
        self.save_popnum_data(OUT_FNAME)  # save data of population number
        self.save_growthr_data()  # save data of growth rate 
        # self.save_allele_freq()
    
    def save_popnum_data(self, out_fname):
        out_fname_ind = "ind" + out_fname  # output file name for individual population data 
        out_fname_fs = "fsource" + out_fname# output file name for food source population data 
        out_flist = [out_fname_ind, out_fname_fs]  # list of output files to be created
               
        os.system("mkdir -p sim_output")  # create direcory for output file if none exists.
        
        self.save_allele_freq()  # save allele freq data 
        
        for fname in out_flist:
            if "ind" in fname:
                self.data_to_save = self.og_individual_pop.popnum_all_runs
            if "fsource" in fname:
                self.data_to_save = self.og_food_pop.popnum_all_runs
                
            self.write_colnames(fname)  # create headers/columns for the output files 
            # self.write_day0(fname)  # add data of the initial population
            self.write_data(fname)  # add population data to output files created above: 
    
    def save_growthr_data(self):
        """"""
        self.data_to_save = self.og_individual_pop.pop_growth_allruns
        self.write_colnames("ind_growth_rate.csv")
        self.write_data("ind_growth_rate.csv")
    
    def save_allele_freq(self):
        self.data_to_save = self.og_individual_pop.allelefreq_allruns
        self.write_colnames("allele_freq.csv")
        self.write_data("allele_freq.csv")
        
        
    def obtain_colnames(self):
        """Obtain column names/headers for the file"""
        self.headers = ["Day"]  # initialize list
        for run_num in range(self.total_runs):
            col_name = "Run" + str(run_num+1)
            self.headers.append(col_name)
        self.headers.append("Average")
        self.headers = ','.join(self.headers)
        
    def write_colnames(self, fname):
        """Write headers into a specified file."""
        command = "echo " + self.headers + " > sim_output/" + fname  # write columns into file 
        os.system(command)  # run the command to create file and add column names
        
    def write_data(self, fname): 
        """"""
        for day_num in range(self.total_days+1):
            data_string = str(day_num) + ", "  # add day number to row (start at 0)
            day_avg = 0
            for run in range(self.total_runs):
                run_data = self.data_to_save[run][day_num] # data for day_num of the run 
                day_avg += run_data
                data_string += str(run_data) + ", "
            
            day_avg = day_avg/self.total_runs  # calculate average for each day 
            command = "echo " + data_string + str(day_avg) + " >> sim_output/" + fname
            os.system(command)
            
    
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
    
    
######################################################################################################   
# TESTING 
class SimTest:
    def __init__(self):
        self.sim = Simulation(20, 30, 2)  # Initialize Simulation (20 ind, 30 days, 2 runs) 
        # My_Sim.run_sim(1)  # run the simulation mode 1
        # My_Sim.save_data(OUT_FNAME)
        
    def test_popaction(self):
        # obtain data: 
        self.sim.food_pop = copy.deepcopy(self.sim.og_food_pop)  # create a duplicate population object
        self.sim.individual_pop = copy.deepcopy(self.sim.og_individual_pop)  # create a duplicate population object
        self.report_action(True)  
        self.sim.populations_action()
        self.report_action(False)
        self.sim.populations_action()
        self.report_action(False)
        
    def report_action(self, before):
        str2add = "before the day: "
        if not before:
            str2add = "after the day: "
        
        print("Number of ind " + str2add + str(len(self.sim.individual_pop.pop_mem_list)))
        ind_stat = []  
        for ind in self.sim.individual_pop:
            ind_stat.append(ind.status)
            
        print("List of ind statuses: " + str(ind_stat))
        print("Number of food " + str2add + str(len(self.sim.food_pop.pop_mem_list)))
        print()
    
    
if __name__ == '__main__':
    simtest = SimTest()  
    simtest.test_popaction()
