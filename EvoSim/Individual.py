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
        self.parent_genes = parent_gene  # self.genes dictionary of the parent
        self.genes = {}  # dictionary of genes with values that will be assigned. 
        
        
        
        if start:  # individual is from starting population:
            self.obtain_available_genes()  # retrieve list of available genes from config file
            
        if not start:  # individual not from starting population - is offspring:
            self.inherit_genes()

    ####################################################################################################   
    # METHODS TO DETERMINE INDIVIDUAL'S GENES
    def obtain_available_genes(self):
        """Retrieve the list of genes an Individual can have."""
        self.avail_gene_dict = {}  # dictionary of available genes {'g1':1, 'g2:0}
        self.gene = {}
        
        for gene in config['GENE_LIST']:
            self.avail_gene_dict[gene] = 0
            self.genes[gene] = 0 
        
        self.randomize_starting_genes()  # randomize values for genes obtained above
    
    def randomize_starting_genes(self):
        """
        Randomize the conditions for each genes in the starting population.
        Note: sum of assigned values are lesser than ALLOTTED_GENE_VALUE from conifig, but 
        not guaranteed to add up to it. 
        """
        self.shuffle_avail_gene_dict()  # randomize the order of the available gene list
        gene_value = config['ALLOTTED_GENE_VALUE']  # number of gene "points" an individual can have 
        
        
        for gene in self.genes:
            if gene_value > 0:
                self.genes[gene] = 1
                gene_value -= self.genes[gene]  # subtract "point" used from total
        
    def shuffle_avail_gene_dict(self):
        """Shuffle the ordered dictionary of available genes to randomize values that are assgined to them."""
        avail_g_list = list(self.genes.items())  # turn dict into list
        random.shuffle(avail_g_list)  # shuffle list 
        self.genes = dict(avail_g_list)  # convert list back into dict 
        
    def inherit_genes(self):
        """Pass genetic information from parent to the Individual."""
        self.mutate_parent_genes()  # introduce random mutation into genome
        self.genes = self.parent_genes  # assign mutated parent's gene as individual's gene 
    
    def mutate_parent_genes(self):
        """Mutate parental genes before passing it onto the offspring."""
        # NOTE: no mutation for now
        mutation_rate = (config['MUTATION_RATE'])/100
    #
    ####################################################################################################   
        
        
        
    ####################################################################################################   
    # DETERMINE WHICH SET OF ACTIONS TO RUN (based on SIM_MODE)
    def init_actions(self, pop, foodpop):
        """
        Initializes variables that are common in actions across all modes. 
        
        Parameters:
            pop (Population object): population that the individual is in. 
            food (Population object): population of FoodSource objects 
        """
        self.population = pop  # Population object that this individual is in 
        self.population_list = pop.pop_mem_list  # list of Individual objects in Population object
        self.foodpop = foodpop  # Population object that contains FoodSource objects 
    ####################################################################################################   
    # ACTIONS COMMON IN ALL MODES
    def determine_food(self):
        """"""
        # determine which food to consume 
        food_num = random.randint(0,(len(self.foodpop.pop_mem_list)-1))
        self.food_source = self.foodpop.pop_mem_list[food_num]  # food to eat
        
    def reproduce(self):
        """Certain individuals are capable of producing more individuals."""
        begin = config['FERTILE_AGE_RANGE'][0]
        end = config['FERTILE_AGE_RANGE'][1]
        REPRODUCE_RECOVER = config['REPRODUCE_RECOVER']
        if self.age > begin and self.age < end:  # check for age 
            if self.gender ==1 and self.status ==1 and self.days_since_repro > REPRODUCE_RECOVER:
                # add newborn individual into population
                self.population_list.append(Individual(age=0, start=False, parent_gene=self.genes)) 
                self.days_since_repro = 0  # reset days since last reproduce 
            self.days_since_repro += 1  # increment days since last reproduce
            
    def aging(self):
        """All individuals age by 1 per day. If individual is older than max_age, it is removed 
        from the population."""
        self.age += 1 
        if self.age > self.max_age:
            self.status = 0  # individual dies at max age
            
    def check_predator(self):
        """"""
        if self.food_source.predator_presence == True:
            return True
    
    def determine_stat(self):
        """Remove individual from population if its status is 0."""
        if self.status == 0:
            self.population.remove_member(self)
    
    ####################################################################################################    
    # ACTIONS FOR SIM_MODE 1
    def mode1_actions(self):
        self.get_food_m1()  
        
    def get_food_m1(self):
        """Individual obtain food. If individual runs into predator, it dies."""
        # check if food has predator:
        self.check_predator_m1()  # see if tree has predator 

    def check_predator_m1(self):
        """Check if the randomly chosen food source has predator. Change status depending on presence of predator."""
        if self.food_source.predator_presence == True:
            self.status = 0  # dies when food source has predator 
            
    ####################################################################################################    
    # ACTIONS FOR SIM_MODE 2
    def mode2_actions(self):
        """"""
        self.get_food_m2()  
    
    def get_food_m2(self):
        """"""
        self.check_predator_m2()  # see if tree has predator 
    
    def check_predator_m2(self):
        """"""
        altruism_gene = self.genes['altruism']  # 1=altruistic, 0=not
        if altruism_gene:  # if individual is altrusitic
            # check if food has predator: 
            if self.check_predator():
                # make food not available for others
                self.foodpop.remove_member(self.food_source)
                # potentially die
    
    def mode3_actions(self):
        pass

    def mode4_actions(self):
        pass    
    
    
    
     



            
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
        print("Genes attribute: " + str(ind.genes))
    
    def test_obtain_available_genes(self):
        """Test the obtain_available_genes() method. NOTE: test is currently not needed - might need later."""
        ind_pop = IndividualPopulation(5)  # create individual population of 5 individuals 
        print("Values in list below should not be greater than " + str(config['ALLOTTED_GENE_VALUE']))
        value_list = []  # list of sum of gene points in each individual
        for ind in ind_pop:
            value = sum(ind.genes.values())
            value_list.append(value)
            
        print("Sum of gene points in each individual: " + str(value_list))
    
    def test_daily_action(self):
        """Test perform_daily_action() method of Individual class."""
        ind_pop = IndividualPopulation(5)  # create individual population of 5 individuals 
        food_pop = FoodPopulation(5)  # create food population of 5 food sources
        self.ind.perform_daily_action(ind_pop, food_pop)
    
            
if __name__ == '__main__':
    ind_test = IndTest()
    ind_test.test_ind_init()
    ind_test.test_daily_action()