############################################################
# DESCRIPTION
############################################################
import random
from Individual import *
from FoodSource import *
from settings import *


class Population():
    def __init__(self, starting_popnum):
        self.starting_popnum = starting_popnum  # number of starting member in the population 
        self.pop_mem_list = []  # list that contains each member of the population (objects)
        
        # Simulation data: 
        # list of population number each day for 1 run (ex: [day1_popnum, day2_popnum, day3_popnum, day4_popnum]
        self.popnum_all_days = []  
        # list of popnum_day for every run (ex: [[day1_popnum, day2_popnum],[day1_popnum, day2_popnum]]
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
        pass
    
    
    
    def execute_population_actions(self):
        """
        Make all individuals in the population perform specified actions. 
        """
        pass 
    
    
    
    def record_day_popnum(self):
        """Record population number for 1 day."""
        popnum = len(self.pop_mem_list)
        self.popnum_all_days.append(popnum)
    
    def record_run_popnum(self):
        # record list of popnum for all days simulated
        self.popnum_all_runs.append(self.popnum_all_days)
        
        # clear list to record popnum for next run
        self.popnum_all_days = []
    
    def record_sim_popnum(self):
        """
        Record population number of the entire simulation (population of all days among all runs). 
        """
        pass
    
    
    
    
    
    
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
  

        
# child class of Population class         
class IndividualPopulation(Population):
    def __init__(self, starting_popnum):
        super().__init__(starting_popnum)
        
        self.initialize_population()  # create starting population of individuals 
        
    def initialize_population(self):
        """Create starting population of a specified number of individuals with random ages."""
        for _ in range(self.starting_popnum):
            start = config['INNIT_AGE_RANGE'][0]
            end = config['INNIT_AGE_RANGE'][1]
            age = random.randint(start, end)
            self.individual = Individual(age)
            self.pop_mem_list.append(self.individual)
            
    def ind_population_actions(self, food):
        """Make every members in the population perform specified actions."""
        for member in self.pop_mem_list:
            member.perform_daily_action(self, food)
    
    
# child class of Population class             
class FoodPopulation(Population):
    def __init__(self, starting_popnum):
        """
        Initializes the population of individuals in the simulation. 
        
        Parameters:
            starting_popnum (int): number of individuals in the starting population.
        """
        super().__init__(starting_popnum)  # obtain attributes from parent class 
        self.no_food_unit_list = []  # list of FoodSource objects without food unit (food unit = 0)
        
        self.initialize_population()  # create starting population of food source 
        
    def initialize_population(self):
        """Create starting population of a specified number of individuals with random ages."""
        for _ in range(self.starting_popnum):
            self.individual = FoodSource()
            self.pop_mem_list.append(self.individual)
        
        self.assign_predators()  # assign predators to random food sources 
    
    
    
    def fs_population_actions(self):
        """Make every members in the population perform specified actions."""
        for member in self.pop_mem_list:
            member.perform_daily_action(self)
    
    
    
    def reset_food_day(self, ind_popnum):
        """
        Reset certain attributes of the food source population, such as adjusting number of food source, 
        re-setting the food_unit attribute, and re-assigning predators. 
        
        Parameters:
            ind_popnum (int): population number of individuals that consume food. 
        """
        self.ind_popnum = ind_popnum  # number of IND that needs food 
        self.edit_food_source_pop()  # make sure there is enough food for the IND population 
        self.assign_predators()  # re-assign predators - in case number of food sources increased. 
        for food in self.pop_mem_list:
            food.food_unit = food.og_food_unit  # reset the food unit 
            
        self.no_food_unit_list = []  # clear list of FoodSource objects without food unit 
    
    def edit_food_source_pop(self):
        """
        Change the population number of the food source depending on the population of individuals. 
        More individual = add food source; less individual = remove food source 
        """
        FOOD_UNIT = config['FOOD_UNIT']
        food_unit_avail = len(self.pop_mem_list)*FOOD_UNIT  # number of food unit currently 
        # create number of food sources needed for current ind population num plus 2 sources extra
        if food_unit_avail < self.ind_popnum:  # if there are less food units than ind
            needed_food_unit = self.ind_popnum - food_unit_avail  # number of food unit needed 
            food_source_to_add = int(needed_food_unit/FOOD_UNIT)+2  # number of food source to add 
            for _ in range(food_source_to_add):
                self.pop_mem_list.append(FoodSource()) 
                
        # remove food sources if population decreased: 
        if food_unit_avail > self.ind_popnum:
            excess_food_unit_num = food_unit_avail - self.ind_popnum  # number of food unit in excess
            num_food_source_to_remove = int(excess_food_unit_num/FOOD_UNIT)  # number of food sources to remove 
            for member in range(num_food_source_to_remove):  # remove specified number of member from population 
                self.remove_member(self.pop_mem_list[member])  
    
    def assign_predators(self):
        """Determine which food source has predators in them based on probability given by PREDATOR_RISK"""
        self.reset_predators()  # remove predators from all fsources 
        PREDATOR_RISK = config['PREDATOR_RISK']
        number_of_members = len(self.pop_mem_list)  # number of members in the food source population 
        number_of_predators = int(number_of_members/(1/PREDATOR_RISK))  # calculate number of predators to assign 
        if number_of_predators == 0:
            number_of_predators = 1  # for when num of members < 1/risk
            
        pred_members = []  # list of food sources that have a predator
        # loop to create random list of food sources to assign predators to 
        while len(pred_members) < number_of_predators:
            max_range = number_of_members - 1
            value = random.randint(0, max_range)
            if value not in pred_members:
                pred_members.append(value) 
                
        # actually assigning the predators:
        for member in pred_members:  # for food sources with position randomly chosen above
            self.pop_mem_list[member].predator_presence = True  # set tree to have predator
            
    def reset_predators(self):
        """Remove predators from all sources before re-assigning predators."""
        for food_source in self.pop_mem_list:
            food_source.predator_presence = False
            
    
    
# TESTING 
if __name__ == '__main__':
    pass