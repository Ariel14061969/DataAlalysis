# Import libraries
from libs_and_modules import *

# Import function files
from config_app_env import *
from manage_app_interface import *
from Intra_country_functions import *

# Configure the App and run it
set_st_bg('streamlit_countries_background.jpg')
config_st_page()
country_data, country_all_columns, country_numeric_columns, country_non_numeric_columns, country_columns_nan_percentage, import_type = st_ui_start()

#Test Printing - To be removed before release
#---------------For Removal------------------------------------------------------#
print(f'\ncountry_data is: {country_data.head()}\n')
print(f'\ncountry_all_columns is: {country_all_columns}\n')
print(f'\ncountry_numeric_columns is: {country_numeric_columns}\n')
print(f'\ncountry_non_numeric_columns is: {country_non_numeric_columns}\n')
print(f'\ncountry_columns_nan_percentage is: {country_columns_nan_percentage}\n')
print(f'\nimport_type is: {import_type}\n')
#--------------End of part for removal ------------------------------------------#

# To be integrated into the manage_app_interface - Temporarily here for inspection
get_country_id_data(country_data.loc[['Canada']],country_all_columns)
