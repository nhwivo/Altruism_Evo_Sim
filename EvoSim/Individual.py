######################################################################################################
# DESCRIPTION
######################################################################################################
import random
from settings import *
from Population import *


class Individual(): 
    def __init__(self, age, start, parent_gene=None):
        """
        Initializes the Individual object. 
        
        Parameters: 
            age (int): age of the individual.
            start (boolean): T if individual is from the starting population - genetic makeup
                would be randomized; compared to F if the individual is an offspring - genes
                would be inherited from parents.
        """
        self.age = age
        self.gender = random.randint(0,1)  # random gender - male=0, female=1
        self.status = 1  # life status - alive=1, dead=0
        self.max_age = config['MAX_AGE']  # maximum age of the individual 
        self.days_since_repro = 0  # days since individual last reproduced 
        self.parent_genes = parent_gene  # genetic makeup of the parent 
        self.genes = {}  # dictionary of genes with values that will be assigned. 
        
        
        
        if start:  # individual is from starting population:
            self.obtain_available_genes()  # retrieve list of available genes from config file
            
        if not start:  # individual not from starting population - is offspring:
            self.inherit_genes()
        
    def obtain_available_genes(self):
        """Retrieve the list of genes an Individual can have."""
        self.avail_gene_dict = {}  # dictionary of available genes {'g1':1, 'g2:0}
        range_genes = config['GENE_LIST_RANGE']  # 0 in avail_gene_dict
        bool_genes = config['GENE_LIST_BOOL']  # 1 in avail_gene_dict
        
        for rgene in range_genes:
            self.avail_gene_dict[rgene] = 'range'
        
        for bgene in bool_genes:
            self.avail_gene_dict[bgene] = 'bool'
        
        self.randomize_starting_genes()  # randomize values for genes obtained above
    
    def randomize_starting_genes(self):
        """
        Randomize the conditions for each genes in the starting population.
        Note: sum of assigned values are lesser than ALLOTTED_GENE_VALUE from conifig, but 
        not guaranteed to add up to it. 
        """
        self.shuffle_avail_gene_dict()  # randomize the order of the available gene list
        gene_value = config['ALLOTTED_GENE_VALUE']  # number of gene "points" an individual can have 
        
        # obtain boolean genes, assign value randomly 
        for key in self.avail_gene_dict:
            if self.avail_gene_dict[key] == 'bool':
                self.genes[key] = random.randint(0,1)
                gene_value -= self.genes[key]  # subtract "point" used from total
        
        # obtain range genes and assign random values up to the remaining "points"
        for key in self.avail_gene_dict:
            if self.avail_gene_dict[key] == 'range':
                # make sure that random value is not greater than remaining points
                rand_val = random.randint(0,10)
                while rand_val > gene_value:
                    rand_val = random.randint(0,10)
                self.genes[key] = rand_val
        
    def shuffle_avail_gene_dict(self):
        """"""
        avail_g_list = list(self.avail_gene_dict.items())  # turn dict into list
        random.shuffle(avail_g_list)  # shuffle list 
        self.avail_gene_dict = dict(avail_g_list)  # convert list back into dict 
        
    def inherit_genes(self):
        self.mutate_parent_genes()  # introduce random mutation into genome
        self.genetic_makeup = None  # assign mutated parent's gene as individual's gene 
    
    def mutate_parent_genes(self):
        pass
        
        
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
        pass

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
                self.population_list.append(Individual(age=0, start=False, parent_gene=self.genetic_makeup)) 
                self.days_since_repro = 0  # reset days since last reproduce 
            self.days_since_repro += 1  # increment days since last reproduce
    
    def aging(self):
        """All individuals age by 1 per day. If individual is older than max_age, it is removed 
        from the population."""
        self.age += 1 
        if self.age > self.max_age:
            self.status = 0  # individual dies at max age 



            
######################################################################################################       
# TESTING 
class IndTest:
    def __init__(self):
        self.ind = Individual(10, True)  # create individual age 10
    
    def test_ind_init(self):
        """Test the __init__ function of Individual class."""
        ind = self.ind
        ind_char = [ind.age, ind.gender, ind.status, ind.max_age, ind.days_since_repro]
        print("Output: " +str(ind_char))
        print("Should be: [10, <random int from 0:1>, 1, " + str(config['MAX_AGE']) + ", 0]")
        print()
    
    def test_obtain_available_genes(self):
        """Test the obtain_available_genes() method."""
        print("Items in: " + str(config['GENE_LIST_RANGE']) + " should have 'range' as values")
        print("Items in: " + str(config['GENE_LIST_BOOL']) + " should 'bool' as values")
        print(self.ind.avail_gene_dict)
        print()
        print("gene list and values after randomization: " + str(self.ind.genes))
    
    def test_daily_action(self):
        """Test perform_daily_action() method of Individual class."""
        ind_pop = IndividualPopulation(5)  # create individual population of 5 individuals 
        food_pop = FoodPopulation(5)  # create food population of 5 food sources
        pass
    
            
if __name__ == '__main__':
    ind_test = IndTest()
    ind_test.test_ind_init()
    ind_test.test_obtain_available_genes()
    ind_test.test_daily_action()