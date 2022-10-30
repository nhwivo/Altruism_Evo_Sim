############################################################
# DESCRIPTION
############################################################
from settings import *


class FoodSource(): 
    def __init__(self):
        self.og_food_unit = FOOD_UNIT  # base food unit that members reset to at end of day 
        self.food_unit = self.og_food_unit  # food unit that changes as the day progresses 
        self.predator_presence = False
        
    def perform_daily_action(self, pop_list):
        self.foodsource_list = pop_list  # list of all members in the population this foodsource is in 
    
    def assign_predators(self):
        pass
    
    def reset_food_unit(self):
        pass
    