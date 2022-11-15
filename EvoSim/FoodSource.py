############################################################
# DESCRIPTION
############################################################
from settings import *
from Population import *


class FoodSource(): 
    def __init__(self):
        self.predator_presence = False  
        
        # remove these features for now - might add them back later
        # self.og_food_unit = config['FOOD_UNIT']  # base food unit that members reset to at end of day 
        # self.food_unit = self.og_food_unit  # food unit that changes as the day progresses 
        
    def perform_daily_action(self, pop_list):
        """
        Actions that an individual perfom each day in the simulation. 
        
        Parameters:
            pop (Population object): population that the individual is in. 
        """
        self.foodsource_list = pop_list  # list of all members in the population this foodsource is in 
    
    
class FsourceTest:
    def __init__(self):
        self.pop = FoodPopulation(5)  # create population of 5 food sources             
    
    def test_fs_init(self):
        """Test the __init__ function of FoodSource class."""
        pred_presence = []  # list of predator presence attribute of each member in pop
        for member in self.pop:
            pred_presence.append(member.predator_presence)
            
        print(pred_presence)
        
    def test_daily_action(self):
        """Test the perform_daily_action() method of FoodSource class."""
        pass
    
# TESTING 
if __name__ == '__main__':
    fsource_test = FsourceTest()
    fsource_test.test_fs_init()
    fsource_test.test_daily_action()