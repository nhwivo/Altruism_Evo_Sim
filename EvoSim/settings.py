# Individual Settings: 
INNIT_AGE_RANGE = [10,40]  # age range of individuals in the starting population (range used to randomize age)
MAX_AGE = 55  # age at which individual is removed from population 
FERTILE_AGE_RANGE = [20,40]  #age range at which individuals can reproduce
REPRODUCE_RECOVER = 2  # number of days before individual can reproduce again 


# Food Source Settings: 
FOOD_UNIT = 4  # number of food unit per Food Source (1 unit = 1 individual) 
INF_FOOD = True  # T: simulation has inifite food sources for individuals; F: finite food
FOOD_SOURCE_AVAIL = 100  # number of food source, each producing FOOD_UNIT amount 
PREDATOR_RISK = 0.03  # probability of a predator in the food source; ex: 0.02 = 1 in 50
