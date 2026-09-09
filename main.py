# Import libraries
from libs_and_modules import *

# Import function files
from config_app_env import *
from manage_app_interface import *
from Intra_country_functions import *
from Intra_continent_functions import *
from Intra_region_functions import *
from Inter_Country import *
from Inter_Continent import *
from Inter_Region import *
from Correlation_Matrix import *
from Units_Txt import *

# Default values for configurable parameters
row_dropna_threshold_factor = 0.9 # The relation between the number of non empty cells to the total number of cells in a row
plt.pyplot.rcParams['figure.max_open_warning'] = 30  # Set the limit for warnings on max number of figures ( Default is 20 )

# Clean up log files from previous runs
log_file_list = ['country_data_anlyze_and_process_log.txt',
                 'intra_country_functions_log.txt',
                 'intra_continent_functions_log.txt']
for project_log_file in log_file_list:
    if os.path.exists(project_log_file):
        os.remove(project_log_file)


# Configure the Streamlit environment of MyCountry App and run it
set_st_bg('streamlit_countries_background.jpg')
config_st_page()
country_data, country_column_data, country_columns_nan_percentage, country_geo_data = st_ui_start(row_dropna_threshold_factor)
analysis_type, target_entity = st_user_select_analysis(country_geo_data['countries'],country_geo_data['continents'], country_geo_data['regions'] )

# This prints  the variables explanations on the screen
char_exp = units_txt()
st.dataframe(char_exp)

# Run the analysis based on the user's selection
if analysis_type == 'intra_country':
    country_row = country_data[country_data.index == target_entity]
    run_intra_country_analysis(country_row, country_column_data['all'] )

if analysis_type == 'intra_continent':
    df_sorted_continent = country_data[country_data.Continent == target_entity]
    run_intra_continent_analysis(df_sorted_continent)

if analysis_type == 'intra_region':
    df_sorted_region = country_data[country_data.region == target_entity]
    run_intra_region_analysis(df_sorted_region)

# each of the inter... functions return figures handles to be displayed in streamlit.
# inside the functions, we do not call streamlit graphics!
if analysis_type == 'inter_country':
    figs = inter_country(country_data, target_entity, compareTo='World')
    for fig in figs:
        st.pyplot(fig)

if analysis_type == 'inter_continent':
    figs= inter_continent(country_data)
    for fig in figs:
        st.pyplot(fig)

if analysis_type == 'inter_region':
    figs= inter_region(country_data)
    for fig in figs:
        st.pyplot(fig)

if analysis_type == 'inter_continent':
    fig,matrix= correlation_matrix(country_data)
    figs = plot_interesting_correlations(country_data, matrix, 0.8)
    for fig in figs:
        st.pyplot(fig)
