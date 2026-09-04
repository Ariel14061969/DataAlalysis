# Import libraries
from libs_and_modules import *

# Import function files
from config_app_env import *
from manage_app_interface import *

# Configure the App and run it
set_st_bg('streamlit_countries_background.jpg')
config_st_page()
(country_data, import_type) = st_ui_start()

#Test Printing - To be removed later
print(f'\nimport_type is: {import_type}\n')
print(f'\ncountry_data is: {country_data.head()}\n')


