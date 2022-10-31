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
        self.max_age = MAX_AGE  # maximum age of the individual 
        self.days_since_repro = 0  # days since individual last reproduced 
        
    def perform_daily_action(self, pop):
        """
        Actions that an individual perfom each day in the simulation. 
        
        Parameters:
            pop (Population object): population that the individual is in. 
        """
        self.population = pop  # Population object that this individual is in 
        self.population_list = pop.pop_mem_list  # list of members in the population (Individual objects)
        self.get_food()
        self.reproduce()
        self.aging()
        
        # remove individuals that are dead from the population:
        if self.status == 0:
            self.population.remove_member(self)  # remove this individual from the list of members in population
    
    def get_food(self):
        """Individual goes out to get food. If individual runs into predator, it dies."""
        self.find_food()  # find tree with food 
        self.check_predator()  # see if tree has predator 
        self.eat_food()  # consume the food unit on the tree
        
    def find_food(self):
        pass
    
    def check_predator(self):
        pass
    
    def eat_food(self):
        pass
    
    def reproduce(self):
        """Certain individuals are capable of producing more individuals."""
        begin, end = FERTILE_AGE_RANGE[0], FERTILE_AGE_RANGE[1]
        recover = REPRODUCE_RECOVER
        if self.age > begin and self.age < end:  # check for age 
            if self.gender ==1 and self.status ==1 and self.days_since_repro > recover:  # other parameter check
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