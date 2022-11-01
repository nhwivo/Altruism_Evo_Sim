############################################################
# DESCRIPTION
############################################################
import random
from settings import *


class Individual(): 
    def __init__(self, age):
        """
        Initializes the Individual object. 
        
        Parameters: 
            age (int): age of the individual.
        """
        self.age = age
        self.gender = random.randint(0,1)  # random gender - male=0, female=1
        self.status = 1  # life status - alive=1, dead=0
        self.max_age = config['MAX_AGE']  # maximum age of the individual 
        self.days_since_repro = 0  # days since individual last reproduced 
        
    def perform_daily_action(self, pop, food):
        """
        Actions that an individual perfom each day in the simulation. 
        
        Parameters:
            pop (Population object): population that the individual is in. 
            food (Population object): population of FoodSource objects 
        """
        self.population = pop  # Population object that this individual is in 
        self.population_list = pop.pop_mem_list  # list of Individual objects in Population object
        self.food = food  # Population object that contains FoodSource objects 
        # self.get_food()
        self.reproduce()
        self.aging()
        
        # remove individuals that are dead from the population:
        if self.status == 0:
            self.population.remove_member(self)
    
    def get_food(self):
        """Individual goes out to get food. If individual runs into predator, it dies."""
        self.food_source = False  # source of food being consumed 
        self.consume_food()  # find tree with food 
        self.check_predator()  # see if tree has predator 
        
        
    def consume_food(self):
        """
        Description 
        """
        while self.food_source == False: # search until FoodSource object with food unit is found
            food_avail_list=list(set(self.food.pop_mem_list).difference(self.food.no_food_unit_list))
            # pick random from list of sources with food
            food_source = random.choice(food_avail_list)  
            if food_source.food_unit > 0:  # random source has food:
                self.food_source = food_source
                food_avail = True  # break the loop 
                
            if food_source.food_unit <= 0:  # source does not have food:
                # add source to list of objects without food 
                self.food.no_food_unit_list.append(food_source)
        
        self.food_source.food_unit -= 1  # consume food from source

    def check_predator(self):
        """
        Description 
        """
        if self.food_source.predator_presence == True:
            self.status = 0  # dies when food source has predator 
    
    def reproduce(self):
        """Certain individuals are capable of producing more individuals."""
        begin = config['FERTILE_AGE_RANGE'][0]
        end = config['FERTILE_AGE_RANGE'][1]
        REPRODUCE_RECOVER = config['REPRODUCE_RECOVER']
        if self.age > begin and self.age < end:  # check for age 
            if self.gender ==1 and self.status ==1 and self.days_since_repro > REPRODUCE_RECOVER:
                # add newborn individual into population
                self.population_list.append(Individual(0)) 
                self.days_since_repro = 0  # reset days since last reproduce 
            self.days_since_repro += 1  # increment days since last reproduce
    
    def aging(self):
        """All individuals age by 1 per day. If individual is older than max_age, it is removed 
        from the population."""
        self.age += 1 
        if self.age > self.max_age:
            self.status = 0  # individual dies at max age 
            
            
# TESTING 
if __name__ == '__main__':
    pass