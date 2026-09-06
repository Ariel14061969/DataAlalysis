# Import libraries
from libs_and_modules import *

# Import function files
from config_app_env import *
from manage_app_interface import *
from Intra_country_functions import *

# Default values for configurable parameters
row_dropna_threshold_factor = 0.9 #relative amount of non empty cells from total cells in a row. Used in calculation of dropna threshold parameters

# Clean up log files from previous runs
log_file_paths = ['country_data_anlyze_and_process_log.txt']
for project_log_file in log_file_paths:
    if os.path.exists(project_log_file):
        os.remove(project_log_file)

# Configure the App and run it
set_st_bg('streamlit_countries_background.jpg')
config_st_page()
country_data, country_column_data, country_columns_nan_percentage, country_geo_data, import_type = st_ui_start(row_dropna_threshold_factor)

#Test Printing - To be removed before release
#---------------For Removal------------------------------------------------------#
print(f'\ncountry_data is: {country_data.head()}\n')
print(f'\ncountry_data column data keys are: {country_column_data.keys()}\n')
print(f'\ncountry_data all columns are: {country_column_data['all']}\n')
print(f'\ncountry_data numeric columns are: {country_column_data['numeric']}\n')
print(f'\ncountry_data non_numeric columns are: {country_column_data['non_numeric']}\n')
print(f'\ncountry_data columns_nan_percentage is: {country_columns_nan_percentage}\n')
print(f'\ncountry_data geo_data keys are: {country_geo_data.keys()}\n')
print(f'\ncountry_data countries are: {country_geo_data['countries']}\n')
print(f'\ncountry_data continents are: {country_geo_data['continents']}\n')
print(f'\ncountry_data regions is: {country_geo_data['regions']}\n')
print(f'\nimport_type is: {import_type}\n')
#--------------End of part for removal ------------------------------------------#

# To be integrated into the manage_app_interface - Temporarily here for inspection
get_country_id_data(country_data.loc[['Canada']],country_column_data['all'])
