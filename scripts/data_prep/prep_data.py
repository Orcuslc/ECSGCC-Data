from get_date import *
from get_max_daily_load import *

data_path = 'E:\\Desktop\\data\\load.csv'
date_index_path = 'E:\\Chuan\\Documents\\GitHub\\ECSGCC-data\\DATA for Loads\\date-index.csv'
max_load_path = 'E:\\Chuan\\Documents\\GitHub\\ECSGCC-data\\DATA for Loads\\date-load.csv'
get_date(data_path, date_index_path)
get_max_load(data_path, date_index_path, max_load_path)