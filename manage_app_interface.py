# Import libraries
from libs_and_modules import *

# Import Functions
from import_country_data import import_country_data

# -------------------------------------------------------------------------#
# Function: validate_data_source_select                                    #
#                                                                          #
# Goal:     Validate the user selection of data source. While input is     #
#           not a valid value, it clears the input and waits for a valid   #
#           value.                                                         #
#                                                                          #
# Input:    None                                                           #
#                                                                          #
# Return:   None ( VOID )                                                  #
#--------------------------------------------------------------------------#
def validate_data_source_select():
    current_input = st.session_state.data_source_select_input
    if ((current_input.lower() != 'y') & (current_input.lower() != 'n')):
        st.error(f"'{current_input}' is not a valid selection, please select either 'y' or 'n'. Clearing input.")
        st.session_state.data_source_select_input = ""  # If validation fails, clear the input by setting its session_state value to an empty string
#----------------------------------------End of Function validate_data_source_select----------------------------------------------------------------#


# -------------------------------------------------------------------------------------------#
# Function: st_ui_start                                                                      #
#                                                                                            #
# Goals:    1. Ask for user name and selecion of data source ( imported / existing )         #
#                                                                                            #
#           2. Validate the user selection of data source, using function                    #
#              "validate_data_source_select"                                                 #
#                                                                                            #
#           3. Based on a valid user selection of the data source, it runs                   #
#              the proper analysis and returns the clean dataframe to the                    #
#              process that invoked it.                                                      #
#                                                                                            #
#                                                                                            #
# Input:    Threshold parameter indicating the number of non empty cells relative to the     #
#           total number of cells in a row. Used as threshold in the of dropna function      #
#                                                                                            #
#                                                                                            #
# Return:   1. A clean dataframe for further data analysis                                   #
#              ( empty cells may still exist on some columns, see item 5 below )             #
#                                                                                            #
#           2. A Dictionary that includes:                                                   #
#              * List of all columns ( after index replaced to country name )                #
#              * List of all numeric columns                                                 #
#              * List of all non-numeric columns                                             #
#                                                                                            #
#           3. A dictionary that holds each of the numeric column names                      #
#              as key and the percentage of empty cells in each column                       #
#                                                                                            #
#           4. A dictionary that holds the geographic data in the post processed dataset:    #
#              * Names of all countries                                                      #
#              * Names of all continents                                                     #
#              * Names of all regions                                                        #
#--------------------------------------------------------------------------------------------#
def st_ui_start(row_dropna_threshold_factor = 0.9):
    st.markdown(
        "<h3 style='text-align: left; color: white; font-weight: bold;'>MyCountry - The World In Your Hands</h2>",
        unsafe_allow_html=True)

    name = st.text_input('Enter your name, please:', '', autocomplete='off')
    if not name:
        st.stop()

    st.write(
        f"<span style='color: white; font-weight: bold;'>Hello, <span style='color: white; font-weight: bold;'>{name}, welcome to MyCountry</span>!",
        unsafe_allow_html=True)

    if 'data_source_select_input' not in st.session_state:
        st.session_state.data_source_select_input = ""

    Import_data = st.text_input(
        "Re-import data ? (y = re-import / n = use existing): ",
        key='data_source_select_input',
        on_change=validate_data_source_select,
        autocomplete = 'off'
    )

    if not Import_data:
        st.stop()

    if (Import_data.lower() == 'y'):
        out_filename = 'country_with_data.csv'
        st.write(f"<span style='color: white; font-weight: bold;'>Creating new database, please wait...</span>",
                 unsafe_allow_html=True)
        try:
            import_country_data(out_filename)
            country_data_orig = pd.read_csv('country_with_data.csv')
            st.write(f"<span style='color: white; font-weight: bold;'>Finished loading and reading new data</span>",
                     unsafe_allow_html=True)

        except Exception as e:
            st.write(f"<span style='color: white; font-weight: bold;'>Failed to load new data:{e}</span>",
                     unsafe_allow_html=True)
            quit()

        country_data_pre_process = country_data_orig.copy()
        country_data, country_column_data, country_columns_nan_percentage, country_geo_data  = process_new_data(country_data_pre_process, 'new', row_dropna_threshold_factor)
        return country_data, country_column_data, country_columns_nan_percentage, country_geo_data

    else:
        try:
            country_data_orig = pd.read_csv('country_with_data.csv')
            st.write(
            f"<span style='color: white; font-weight: bold;'>Finished loading and reading current data</span>", unsafe_allow_html=True)

        except Exception as e:
            st.write(f"<span style='color: white; font-weight: bold;'>Failed to load current data:{e}</span>",
                    unsafe_allow_html=True)
            quit()

        country_data_pre_process = country_data_orig.copy()
        country_data, country_column_data, country_columns_nan_percentage, country_geo_data  = process_new_data(country_data_pre_process, 'current', row_dropna_threshold_factor)
        return country_data, country_column_data, country_columns_nan_percentage, country_geo_data
#-----------------------------------------------------End of Function validate_data_source_select---------------------------------------------------------------------#

# ---------------------------------------------------------------------------------------------------#
# Function: process_new_data                                                                         #
#                                                                                                    #
# Goal:     1. Analyze and clean the the Data                                                        #
#              * Remove duplicates, if any, based on the Country column                              #
#              * Set the country name as index of the DataFrame                                      #
#              * Identify empty cells on each row and remove rows in which                           #
#                the number of empty cells exceeds a pre-defined threshold (Default is 10%)          #
#                                                                                                    #
#           2. Identify percentage of NaNs in each numerical columns                                 #
#                                                                                                    #
#           3. Extract the named of countries, continents and regions in the dataset                 #
#                                                                                                    #
#                                                                                                    #
# Input:    1. New DataFrame created from either a new API or from existing csv file                 #
#              originally generated during a previous read of data from an API                       #
#                                                                                                    #
#           2. A string that specifies the desired source of data                                    #
#              * 'new' - DataFrame source is a new dataset, read from an API during this run         #
#              * 'current' - Data source is an existing local csv                                    #
#                                                                                                    #
#           3. A Threshold parameter indicating the allowed number of non empty cells relative to    #
#              the total number of cells in a row. Used to claculate the threshold in the            #
#              dropna function                                                                       #
#                                                                                                    #
# Return:   1. Cleaned DataFrame                                                                     #
#                                                                                                    #
#           2. A Dictionary that includes:                                                           #
#              * List of all columns ( after index replaced to country name )                        #
#              * List of all numeric columns                                                         #
#              * List of all non-numeric columns                                                     #
#                                                                                                    #
#           3. A dictionary that holds each of the numeric column names                              #
#              as key and the percentage of empty cells in each column                               #
#                                                                                                    #
#           4. A dictionary that holds the geographic data in the post processed dataset:            #
#              * Names of all countries                                                              #
#              * Names of all continents                                                             #
#              * Names of all regions                                                                #
#----------------------------------------------------------------------------------------------------#
def process_new_data(datain, data_import_type, row_dropna_threshold_factor = 0.9):
    # Open a log file for debug and review
    with open('country_data_anlyze_and_process_log.txt', 'w') as log_file:
        log_file.write(f'Log opened at: {dt.datetime.now(zi.ZoneInfo("Asia/Jerusalem")).strftime("%Y-%m-%d %H:%M:%S")}\n')
        if (data_import_type == 'new'):
            log_file.write(f'Run on new data imported during this run\n')
        else:
            log_file.write(f'Run on data imported from existing csv file created in the past\n')
        log_file.write(f'Starting Analysis and Processing...\n')

    # ---------------------- Remove Duplicates on the 'Country' Column----------------------------#
        length_orig = len(datain)
        datain.drop_duplicates(subset='Country', keep='first', inplace=True)
        length_post_duplicates_removal = len(datain)
        delta_length = length_orig - length_post_duplicates_removal
        log_file.write(f"\n#------Handling Duplicates on the 'Country' column----#\n")
        log_file.write(f'Original length of dataset was {length_orig}\n')
        log_file.write(f'Length of dataset after removal of duplicates is {length_post_duplicates_removal}\n')
        log_file.write(f"Total of {delta_length} duplicates were identified and removed on the 'Country' column")
        log_file.write(f'\n#-----------------------------------------------------------------------------------#\n')
    # ------------------------------End of Duplicate removal----------------------------------------#

    # ------------------------Change index to Country before starting the analysis----------------#
        datain.set_index('Country', inplace=True)
    # -----------------------------------End of Index replacement-----------------------------------#

    # -----------------------Examine the Dataset and handle empty cells-------------------------#
        # Assign all countries and columns in the original dataset to lists
        country_list_pre_drop = list(datain.index)
        country_column_list = list(datain.columns)

        # Split the column list to a list of columns with numeric values and a list of columns with non-numeric values
        possible_numeric_dtype_vals = ['float32', 'float64', 'int64', 'int32', 'unit32', 'int16', 'uint16', 'int8', 'uint8']
        numeric_column_list = list(datain.dtypes[datain.dtypes.astype(str).isin(possible_numeric_dtype_vals)].index)
        non_numeric_column_list = [column_name for column_name in country_column_list if column_name not in numeric_column_list]
        log_file.write(f"\n#------Splitting the column list to numeric and non-numeric---------------#\n")
        log_file.write(f'\nThere are {len(numeric_column_list)} numeric columns in the dataset\n')
        log_file.write(f'There are {len(non_numeric_column_list)} non-numeric columns in the dataset\n')

        log_file.write(f'\n#-------List of numeric columns ---------#\n')
        for num_column_name in numeric_column_list:
            log_file.write(f'{num_column_name}\n')

        log_file.write(f'\n#-------List of non-numeric columns ---------#\n')
        for non_num_column_name in non_numeric_column_list:
            log_file.write(f'{non_num_column_name}\n')
        log_file.write(f'#-----------------------------------------------------------------------#\n')

        # Define the max allowed empty cells in a row and remove all rows beyond that number
        row_na_removal_threshold = row_dropna_threshold_factor  # Min required percentage of non-empty cells in a row
        datain.dropna(subset=numeric_column_list,thresh=math.ceil((len(numeric_column_list) * row_na_removal_threshold)),inplace=True)

        # Identify which countries remained and which were removed from the original dataset
        country_list_post_drop = list(datain.index)
        removed_countries = [country for country in country_list_pre_drop if country not in country_list_post_drop]

        # Check how many rows were removed and report in the log
        length_post_NA_rows_removal = len(datain)
        delta_length_post_NA_removal = length_post_duplicates_removal - length_post_NA_rows_removal
        log_file.write(f"\n#------Report the number of removed rows (countries) ----------------------#\n")
        log_file.write(f'Original length of dataset before removal of NA rows was {length_post_duplicates_removal}\n')
        log_file.write(f'Length of dataset after removal of NA rows is {length_post_NA_rows_removal}\n')
        log_file.write(f"Total of {delta_length_post_NA_removal} rows with more than {int(math.ceil((1 - row_na_removal_threshold) * 100))}% empty cells on the numerical columns of the dataset were identified and removed from the dataset ")

        log_file.write(f'\nThe following countries were removed from the original list following the drop of rows described above:\n')
        for country in removed_countries:
            log_file.write(f'{country}\n')
        log_file.write(f'\n#-----------------------------------------------------------------------#\n')

        # Identify the percentage of empty cells in each numeric columns and create a dictionaly to hold the data
        country_columns_nan_percentage = dict()
        for column_name in numeric_column_list:
            country_columns_nan_percentage[column_name] = round((1 - float(datain[column_name].count() / len(datain))) * 100, 1)

        log_file.write(f'\n#-------List of nan_percentage per column ---------#\n')
        for key in country_columns_nan_percentage:
            log_file.write(f'{key}: {country_columns_nan_percentage[key]}\n')
        log_file.write(f'#----------------------------------------------------:\n')

        # Identify the number and names of continents in the dataset
        continents_list = list(datain.Continent.unique())
        num_of_continents = datain.Continent.nunique()

        # Identify the number and names of regions in the dataset
        regions_list = list(datain.region.unique())
        num_of_regions = datain.region.nunique()

        # Summarize the geographical information (countries, continents, regions ) for the user
        log_file.write(f"\n\n#------Summary of geographical data in the processed dataset----------------------#\n")
        log_file.write(f'\nTotal of {len(country_list_post_drop)} are included in the set:\n')
        for country in country_list_post_drop:
            log_file.write(f'{country}\n')
        log_file.write(f'#----------\n')

        log_file.write(f'\n\nTotal of {num_of_continents} continents are included in the set:\n')
        for continent in continents_list:
            log_file.write(f'{continent}\n')
        log_file.write(f'#----------\n')

        log_file.write(f'\n\nTotal of {num_of_regions} regions are included in the set:\n')
        for region in regions_list:
            log_file.write(f'{region}\n')
        log_file.write(f'#-----------------------------------------------------\n')

        # Consolidate the column data into a single dictionary
        country_column_data = dict()
        country_column_data['all'] = country_column_list
        country_column_data['numeric'] = numeric_column_list
        country_column_data['non_numeric'] = non_numeric_column_list

        # Consolidate the geographical data into a single dictionary
        country_geo_data = dict()
        country_geo_data['countries'] = country_list_post_drop
        country_geo_data['continents'] = continents_list
        country_geo_data['regions'] = regions_list

    # Create a copy of the datain before return - no further processing will be done on the processed DataFrame inplace
    country_data_post_process = datain.copy()
    return country_data_post_process, country_column_data, country_columns_nan_percentage, country_geo_data

#-----------------------------------------End of Function process_new_data-------------------------------------------------#


# -------------------------------------------------------------------------#
# Function: st_user_select_analysis                                        #
#                                                                          #
# Goal:     Create the user selection manual in streamlit ,receive the     #
#           selected value and send it back to the main function.          #
#                                                                          #
# Input:    1.List of countries                                            #
#           2.List of continents                                           #
#           3.List of regions                                              #
#                                                                          #
# Return:   1.Selected analysis type ( one of the below options):          #
#             * intra_country                                              #
#             * inter_country                                              #
#             * intra_continent                                            #
#             * inter_continent                                            #
#             * intra_region                                               #
#             * inter_region                                               #
#                                                                          #
#          2.Selected country / continent / region to be analyzed          #
#--------------------------------------------------------------------------#
def st_user_select_analysis(country_list, continents_list, regions_list):
    analysis_options = [ '','intra_country', 'inter_country',
                        'intra_continent', 'inter_continent',
                        'intra_region', 'inter_region']

    # Add empty space as the first value of each list such that user has to select
    country_list_modified = [''] + country_list
    continents_list_modified = [''] + continents_list
    regions_list_modified = [''] + regions_list

    col_label, col_select, col_empty = st.columns([1, 1, 8])
    with col_label:
        st.markdown("<h3 style='color:white;'><b>Analysis Type</b></h3>", unsafe_allow_html=True)
    with col_select:
        selected_analysis = st.selectbox('Analysis Type', analysis_options, label_visibility='hidden', key='analysis_type')
    if not selected_analysis:
        st.stop()


    if (selected_analysis == 'intra_country') | (selected_analysis == 'inter_country'):
        col_label, col_select, col_empty = st.columns([1, 1, 8])
        with col_label:
            st.markdown("<h3 style='color:white;'><b>Countries</b></h3>", unsafe_allow_html=True)
        with col_select:
            selected_country = st.selectbox('Countries', country_list_modified, label_visibility='hidden', key='country_select')
            if not selected_country:
                st.stop()
        return selected_analysis, selected_country

    elif (selected_analysis == 'intra_continent') | (selected_analysis == 'inter_continent'):
        col_label, col_select, col_empty = st.columns([1, 1, 8])
        with col_label:
            st.markdown("<h3 style='color:white;'><b>Continents</b></h3>", unsafe_allow_html=True)
        with col_select:
            selected_continent = st.selectbox('Continents', continents_list_modified, label_visibility='hidden', key='continent_select')
            if not selected_continent:
                st.stop()
        return selected_analysis, selected_continent

    else:
        col_label, col_select, col_empty = st.columns([1, 1, 8])
        with col_label:
            st.markdown("<h3 style='color:white;'><b>Regions</b></h3>", unsafe_allow_html=True)
        with col_select:
            selected_region = st.selectbox('Regions', regions_list_modified, label_visibility='hidden', key='region_select')
            if not selected_region:
                st.stop()
        return selected_analysis, selected_region
#----------------------------------------End of Function st_user_select_analysis -------------------------------------------------------#