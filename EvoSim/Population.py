######################################################################################################
# DESCRIPTION
######################################################################################################

import copy
import random
from Individual import *
from FoodSource import *
from settings import *

######################################################################################################
# PARENT POPULATION CLASS
class Population():
    def __init__(self, starting_popnum):
        self.starting_popnum = starting_popnum  # number of starting member in the population 
        self.pop_mem_list = []  # list that contains each member of the population (objects)
        
        # Attributes to store population number data: 
        # list of population number each day for 1 run (ex: [day1_popnum, day2_popnum, day3_popnum])
        self.popnum_all_days = []  
        # list of popnum_day for every run (ex: [[day1_popnum, day2_popnum],[day1_popnum, day2_popnum]])
        self.popnum_all_runs = [] 
        
    
    def __iter__(self):
        """
        Make the Population object iterable - each member in the self.pop_ind_list are iterated.
        Returns the Iterator object.
        """
        return PopulationIterator(self)
    
    def __next__(self):
        pass
    
    def remove_member(self, member):
        """Remove specified member from the list of members."""
        self.pop_mem_list.remove(member)
    
    def add_individual(self):
        """"""
        pass
    
    ####################################################################################################    
    # RECORD POPULATION DATA  
    def record_day_popnum(self):
        """Record population number for 1 day."""
        popnum = len(self.pop_mem_list)
        self.popnum_all_days.append(popnum)
    
    def record_run_popnum(self):
        """Record population data for the run."""
        # record list of popnum for all days simulated
        self.popnum_all_runs.append(self.popnum_all_days)
        
        # clear list to record popnum for next run
        self.popnum_all_days = []
    
    def record_sim_popnum(self):
        """
        Record population number of the entire simulation (population of all days among all runs). 
        NOTE: might not need 
        """
        pass
    ####################################################################################################    
    # POPULATION DATA CALCULATIONS
    def cal_pop_growth(self):
        """
        Calculate population growth
            - Growth = 1: stable population, no growth 
            - Growth < 1: population decline 
            - Growth > 1: population increase 
        """
        self.pop_growth_allruns = [] # list of list of population growth 
        for run in self.popnum_all_runs:  # cycle through each list of popnum/run 
            # reset list: 
            self.pop_growth = []  # list of population growth over days for 1 run 
            prev_pop_num = run[0]  # obtain starting population 
            for day in range(len(run)): # for each day
                current_pnum = run[day]  # current population number 
                # calculate population growth
                if prev_pop_num <= 0:  # division with 0  
                    growth = 0
                else: 
                    growth = (current_pnum/prev_pop_num)
                prev_pop_num = current_pnum  
                self.pop_growth.append(growth)  # add calculated growth to list
            self.pop_growth_allruns.append(self.pop_growth)
    #
    ####################################################################################################    

    
    

class PopulationIterator:
    """Iterator class for Population class - iterates through each member object in the population"""
    def __init__(self, population):
        self._team = population  # member object reference 
        self._index = 0  # member variable to keep track of current index 
        
    def __next__(self):
        """Returns the next value from population object's list"""
        if self._index < (len(self._team.pop_mem_list)):
            result = self._team.pop_mem_list[self._index]
            self._index +=1
            return result
        
        # End of Iteration
        raise StopIteration
######################################################################################################















######################################################################################################        
# INDIVIDUAL POPULATION CLASS - CHILD CLASS OF POPULATION CLASS         
class IndividualPopulation(Population):
    def __init__(self, starting_popnum):
        super().__init__(starting_popnum)
        self.sim_mode = config["SIM_MODE"]  # obtain mode from config
        
        # Attributes to store population allele frequency data: 
        # list of allele freq each day for 1 run (ex: [day1_afreq, day2_afreq, day3_afreq]) 
        self.allelefreq_alldays = []
        # list of allele freq for every run (ex: [[day1_afreq, day2_afreq],[day1_afreq, day2_afreq]]
        self.allelefreq_allruns = [] 
        
        self.initialize_population()  # create starting population of individuals 
        
    def initialize_population(self):
        """Create starting population of a specified number of individuals with random ages."""
        for _ in range(self.starting_popnum):
            start = config['INNIT_AGE_RANGE'][0]
            end = config['INNIT_AGE_RANGE'][1]
            age = random.randint(start, end)
            self.individual = Individual(age, start=True)
            self.pop_mem_list.append(self.individual)
        
        # initialize dict to keep count of allele freq - count only those with 1 for allele value 
        self.afreq_dict = {'total':0}  # ex: {'altruism':2, 'altruistic marker':5}
        for gene in self.pop_mem_list[0].genes:
            self.afreq_dict[gene] = 0 
            
        # record initial allele freq
        for member in self.pop_mem_list:
            self.member = member
            self.count_allele()
        
        if self.sim_mode == 4: 
            self.init_m4()
            
    def init_m4(self):
        # dict of number of number of individual of each phenotype 
        self.four_pheno_count = {"AB":0,"Ab":0,"aB":0,"ab":0}   
        for member in self.popmemlist:
            self.member = member
            pheno = self.determine_pheno_m4()
            self.four_pheno_count[pheno] += 1
            
            
    def determine_pheno_m4(self):
        """
        Returns: a string indicating the following 
            - AB: altruistic and has beard 
            - Ab: altruistic and no beard 
            - aB: not altruistic and has beard 
            - ab: not altruistic and no beard  
        """
        gene = self.member.genes  
        if gene['altruism']:  # is altruistic 
            if gene['altruistic marker']:  # has marker 
                # altruistic + has beard = AB
                return 'AB'
            else:
                # altruistic + no beard = Ab
                return 'Ab'
        elif:  # not altruistic 
            if gene['altruistic marker']:  # has marker
                # not altruistic + has beard = aB
                return 'aB'
            else:
                # not altruistic + no beard = ab 
                return 'ab'
            
    
            
            
    ####################################################################################################    
    # ACTION OF ALL MEMBERS IN THE IND POPULATION FOR THE DAY    
    def population_actions(self, foodpop):
        """Make every members in the population perform specified actions."""
        self.food_pop = copy.deepcopy(foodpop)  # make copy so that original list does not get altered
        self.init_var()  # initializes variables 
        
        for member in self.pop_mem_list:
            self.member = member
            self.member.init_actions(self, self.food_pop)  # pass on variables needed in all modes
            self.run_mode()  # run specified mode
            self.member.determine_stat()  # remove individual if dead  
            
    def run_mode(self):
        """Determine mode of the simulation and execute actions of ind accordingly."""
        # actions executed regardeless of sim_mode:
        self.member.determine_food()  # individual picks out food randomly
        mode = self.sim_mode 
        
        if mode == 0:
            self.member.mode0_actions()
            
        if mode == 1:
            self.member.mode1_actions()
            
        if mode == 2:
            self.member.mode2_actions()
            
        if mode == 3:
            self.member.mode3_actions(self.foodwpred)
            
        if mode == 4:
            self.member.mode4_actions(self.foodwpred)
        
        # actions executed regardeless of sim_mode:
        self.member.reproduce()
        self.member.aging()
        self.count_allele()  # record allele freq
        
    def init_var(self):
        """"""
        self.foodwpred = []  # list of food with predators
        for gene in self.afreq_dict:
            self.afreq_dict[gene] = 0  # reset count 
        
    def count_allele(self):
        """Record count of each gene in gene list of Individual object."""
        for gene in self.member.genes:  # for each gene in the ind genes dict
            self.afreq_dict[gene] += self.member.genes[gene] 
        self.afreq_dict['total'] += 1
    #
    ####################################################################################################    
    # RECORD ALLLE FREQUENCY POPULATION DATA  
    def record_day_allelefreq(self):
        """Record allele frequency for 1 day."""
        mode = self.sim_mode  # obtain mode
        if mode == 2 or mode == 3: 
            self.record_day_allelefreq_alt()
            
        if mode == 4: 
            self.record_day_4phenotypes()
            
            
        self.allelefreq_alldays.append(self.day_allelefreq)
    
    def record_day_allelefreq_alt(self):
        """Only record 'altruism' gene. day_allelefreq variable reports proportion of population with alt gene."""
        altruism_num = self.afreq_dict['altruism']  # number of individuals with gene 
        total_num = self.afreq_dict['total']  # total number of individuals 
        if altruism_num:  # not 0 
            self.day_allelefreq = altruism_num/total_num
            
        else:  # 0 altruisctic ind (indivisible by 0) 
            self.day_allelefreq = 0
            
    def record_day_4phenotypes(self):
        """
        Record the 4 different possible phenotypes in mode 4.
            - AB: altruistic and has beard 
            - Ab: altruistic and no beard 
            - aB: not altruistic and has beard 
            - ab: not altruistic and no beard  
        """
        pass
    
    
    def record_run_allelefreq(self):
        """Record allele frequency for 1 run."""
        # record list of allele freq for all days simulated
        self.allelefreq_allruns.append(self.allelefreq_alldays)
        
        # clear list to record popnum for next run
        self.allelefreq_alldays = []
        
    def record_breeding_pop(self):
        """Record proportion/fraction of breeding population."""
        pass
    
    
        
        
######################################################################################################














######################################################################################################    
# FOOD POPULATION CLASS - CHILD CLASS OF POPULATION CLASS             
class FoodPopulation(Population):
    def __init__(self, starting_popnum):
        """
        Initializes the population of individuals in the simulation. 
        
        Parameters:
            starting_popnum (int): number of individuals in the starting population.
        """
        super().__init__(starting_popnum)  # obtain attributes from parent class 
        self.initialize_population()  # create starting population of food source 
        
    def initialize_population(self):
        """Create starting population of a specified number of individuals with random ages."""
        for _ in range(self.starting_popnum):
            self.individual = FoodSource()
            self.pop_mem_list.append(self.individual)
        
        self.assign_predators()  # assign predators to random food sources 
    
    
    ####################################################################################################    
    # ACTION OF ALL MEMBERS IN THE POPULATION FOR THE DAY    
    def population_actions(self):
        """Make every members in the population perform specified actions for the day."""
        for member in self.pop_mem_list:
            member.perform_daily_action(self)
    
    
    ####################################################################################################    
    # RESETTING ATTRIBUTES OF ALL MEMBERS IN THE POPULATION 
    def reset_food_day(self, ind_popnum):
        """
        Reset certain attributes of the food source population, such as re-assigning predators. 
        
        Parameters:
            ind_popnum (int): population number of individuals that consume food. 
        """
        self.ind_popnum = ind_popnum  # number of IND that needs food 
        self.edit_food_source_pop()  # make sure there is enough food for the IND population 
        self.assign_predators()  # re-assign predators - in case number of food sources increased. 
                
    def edit_food_source_pop(self):
        """
        Change the population number of the food source depending on the population of individuals. 
        More individual = add food source; less individual = remove food source 
        """
        food_unit_avail = len(self.pop_mem_list)  # number of food available currently 
        # create number of food sources needed for current ind population num + 1 extra
        if food_unit_avail < self.ind_popnum:  # if there are less food units than ind
            needed_food_unit = (self.ind_popnum - food_unit_avail) + 1  # number of food unit needed 
            for _ in range(needed_food_unit):
                self.pop_mem_list.append(FoodSource()) 
                
        # remove food sources if population decreased: 
        if food_unit_avail > self.ind_popnum:
            excess_food_unit_num = (food_unit_avail - self.ind_popnum) - 1  # number of food unit in excess
            if excess_food_unit_num > 0: 
                for member in range(excess_food_unit_num):  # remove specified number of member from population 
                    self.remove_member(self.pop_mem_list[member])  
    
    def assign_predators(self):
        """Determine which food source has predators in them based on probability given by PREDATOR_RISK"""
        self.reset_predators()  # remove predators from all fsources 
        PREDATOR_RISK = config['PREDATOR_RISK']
        number_of_members = len(self.pop_mem_list)  # number of members in the food source population 
        number_of_predators = int(number_of_members/(1/PREDATOR_RISK))  # calculate number of predators to assign 
        if number_of_predators == 0:
            number_of_predators = 1  # for when num of members < 1/risk
            
        random.shuffle(self.pop_mem_list)  #shuffle position of food 
        for pred in range(number_of_predators): 
            self.pop_mem_list[pred].predator_presence = True
        
        random.shuffle(self.pop_mem_list)  #shuffle position of food 
            
#         pred_members = []  # list of food sources that have a predator
#         # loop to create random list of food sources to assign predators to 
#         while len(pred_members) < number_of_predators:
#             max_range = number_of_members - 1
#             value = random.randint(0, max_range)
#             if value not in pred_members:
#                 pred_members.append(value) 
                
#         # actually assigning the predators:
#         for member in pred_members:  # for food sources with position randomly chosen above
#             self.pop_mem_list[member].predator_presence = True  # set tree to have predator
            
    def reset_predators(self):
        """Remove predators from all sources before re-assigning predators."""
        for food_source in self.pop_mem_list:
            food_source.predator_presence = False
######################################################################################################


    
    
    
    
    
    
    
    
    
    
    
    

######################################################################################################   
# TESTING 
class IndPopTest:
    def __init__(self):
        self.start_popnum = 10
        self.pop = IndividualPopulation(self.start_popnum)
        self.foodpop = FoodPopulation(self.start_popnum)
    
    def test_pop_init(self):
        print("Number of starting population: " + str(len(self.pop.pop_mem_list))
             + " - Should be " + str(self.start_popnum))
        
    def test_record_allelefreq(self):
        # perform population action - to obtain afreq data 
        self.pop.population_actions(self.foodpop)  
        print("allele freq data end of 1 day: ")
        print(self.pop.afreq_dict)
        
        # calculate data
        self.pop.record_day_allelefreq()
        print()
        print(self.pop.allelefreq_alldays)
        
    def test_four_pheno_count(self):
        print(self.pop.four_pheno_count)
    
class FoodPopTest:
    def __init__(self):
        self.start_popnum = 10
        self.pop = FoodPopulation(self.start_popnum)
    
    def test_pop_init(self):
        print("Number of starting population: " + str(len(self.pop.pop_mem_list))
             + " - Should be " + str(self.start_popnum))
        pred_pres_data = []  # predator in food population 
        for member in self.pop.pop_mem_list:
            pred_pres_data.append(member.predator_presence)
        print("Predator presence data: " + str(pred_pres_data))


if __name__ == '__main__':
    # test IndividualPopulation child class
    print("IndividualPopulation Class Tests:")
    ipop_test = IndPopTest()
    ipop_test.test_record_allelefreq()
    ipop_test.test_four_pheno_count() 
    print("")

    
    # test FoodPopulation child class
    print("FoodPopulation Class Tests:")
    fpop_test = FoodPopTest()
    fpop_test.test_pop_init()
    
    