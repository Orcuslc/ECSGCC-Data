# Configurations

###############################
# For prep_attr.py
###############################
LOAD_SCALE = 10000
TEMP_SCALE = 29
DAYS_BACK = 6

DATA_PATH = '../data/simp_daily_data.csv'
ATTR_PATH = '../data/attr.txt'

WEEKDAYS = ['0 0 0 0 0 1',
			'0 0 0 0 1 0',
			'0 0 0 1 0 0',
			'0 0 1 0 0 0',
			'0 1 0 0 0 0',
			'1 0 0 0 0 0',
			'0 0 0 0 0 0']

HOLIDAYS = ['1', '0.21', '0']

################################
# For predict.py
################################

# Notice: Do not change values in this region!
C = 4
gamma = 2**-4

# Ordinary configurations
MODEL_PATH = 'data/model.txt'
