############################################################
# DESCRIPTION
############################################################
from settings import *
from Population import *


class FoodSource(): 
    def __init__(self):
        self.og_food_unit = config['FOOD_UNIT']  # base food unit that members reset to at end of day 
        self.food_unit = self.og_food_unit  # food unit that changes as the day progresses 
        self.predator_presence = False
        
    def perform_daily_action(self, pop_list):
        """
        Actions that an individual perfom each day in the simulation. 
        
        Parameters:
            pop (Population object): population that the individual is in. 
        """
        self.foodsource_list = pop_list  # list of all members in the population this foodsource is in 
    
    def assign_predators(self):
        pass
    
    def reset_food_unit(self):
        pass
    
    
class FsourceTest:
    def __init__(self):
        self.pop = FoodPopulation(5)  # create population of 5 food sources 
        self.fsource = random.choice(self.pop.pop_mem_list)  # random member from population
    
    def test_fs_init(self):
        """Test the __init__ function of FoodSource class."""
        fsource = self.fsource
        fsource_char = [fsource.og_food_unit, fsource.food_unit, fsource.predator_presence]
        print("Output: " +str(fsource_char))
        print("Should be: [" + str(config['FOOD_UNIT']) + ", " + str(config['FOOD_UNIT']) + ", False]")
        
    def test_daily_action(self):
        """Test the perform_daily_action() method of FoodSource class."""
        self.fsource.perform_daily_action(self.pop)  # nothing in this method for now 
    
    
# TESTING 
if __name__ == '__main__':
    fsource_test = FsourceTest()
    fsource_test.test_fs_init()
    fsource_test.test_daily_action()