########################################################################################################
# DESCRIPTION
########################################################################################################
import yaml

with open("../config/config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    
# TESTING 
if __name__ == '__main__':
    pass