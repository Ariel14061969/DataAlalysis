# Import libraries
from libs_and_modules import *

# Import function files
from config_app_env import *
from manage_app_interface import *
from Intra_country_functions import *
from Inter_Country import inter_country
from Inter_Continent import inter_continent
from Inter_Region import inter_region
from Correlation_Matrix import *

# Default values for configurable parameters
row_dropna_threshold_factor = 0.9 # The relation between the number of non empty cells to the total number of cells in a row

# Clean up log files from previous runs
log_file_list = ['country_data_anlyze_and_process_log.txt', 'intra_country_functions_log.txt']
for project_log_file in log_file_list:
    if os.path.exists(project_log_file):
        os.remove(project_log_file)


# Configure the Streamlit environment of MyCountry App and run it
set_st_bg('streamlit_countries_background.jpg')
config_st_page()
country_data, country_column_data, country_columns_nan_percentage, country_geo_data = st_ui_start(row_dropna_threshold_factor)
analysis_type, target_entity = st_user_select_analysis(country_geo_data['countries'],country_geo_data['continents'], country_geo_data['regions'] )

# Run the analysis based on the user's selection
if analysis_type == 'intra_country':
    country_row = country_data[country_data.index == target_entity]
    run_intra_country_analysis(country_row, country_column_data['all'] )

if analysis_type == 'inter_country':
    figs = inter_country(country_data, target_entity, compareTo='World')
    for fig in figs:
        st.pyplot(fig)

if analysis_type == 'inter_continent':
    figs= inter_continent(country_data)
    for fig in figs:
        st.pyplot(fig)

if analysis_type == 'inter_continent':
    figs= inter_region(country_data)
    for fig in figs:
        st.pyplot(fig)

if analysis_type == 'inter_continent':
    fig,matrix= correlation_matrix(country_data)
    figs = plot_interesting_correlations(country_data, matrix, 0.8)
    for fig in figs:
        st.pyplot(fig)

