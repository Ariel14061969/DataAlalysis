# Import libraries
from libs_and_modules import *

# Import Functions
from import_country_data import import_country_data

# -------------------------------------------------------------------------#
# Function: validate_data_source_select                                    #
# Goal:     Validate the user selection of data source. While input is     #
#           not a valid value, it clears the input and waits for a valid   #
#           value.                                                         #
# Input:    None                                                           #
# Return:   None ( VOID )                                                  #
#--------------------------------------------------------------------------#
def validate_data_source_select():
    current_input = st.session_state.data_source_select_input
    if ((current_input.lower() != 'y') & (current_input.lower() != 'n')):
        st.error(f"'{current_input}' is not a valid selection, please select either 'y' or 'n'. Clearing input.")
        st.session_state.data_source_select_input = ""  # If validation fails, clear the input by setting its session_state value to an empty string

#-----------End of Function validate_data_source_select--------------------#


# -----------------------------------------------------------------------------#
# Function: st_ui_start                                                        #
#                                                                              #
# Goals:                                                                       #
# 1. Ask for user name and selecion of data source ( imported / existing )     #
# 2. Validate the user selection of data source, using function                #
#    "validate_data_source_select"                                             #
# 3. Based on a valid user selection of the data source, it runs               #
#    the proper analysis and returns the clean dataframe to the                #
#    process that invoked it.                                                  #
#                                                                              #
# Input:  None                                                                 #
#                                                                              #
# Return: 1. A clean dataframe for further data analysis                       #
#            ( empty cells may still exist on some columns, see item 5 below ) #
#         2. List of all columns ( after index replaced to country name )      #
#         3. List of all numeric columns                                       #
#         4. List of all non-numeric columns                                   #
#         5. A dictionary that holds each of the numeric column names          #
#            as key and the percentage of empty cells in each column           #
#------------------------------------------------------------------------------#
def st_ui_start():
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
        country_data = process_new_data(country_data_pre_process)
        return country_data, 'new'

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
        country_all_columns = list() # A list of all columns in the DataFrame
        country_numeric_columns = list() # A list of all columns in the DataFrame that hold numerical values
        country_non_numeric_columns = list() # A list of all columns in the DataFrame that hold non-numerical values
        country_columns_nan_percentage = dict() # A dictionary that holds each of the numeric column names as a key
                                                # and the percentage of empty cells in each column as the value of that key

        country_data, country_all_columns, country_numeric_columns, country_non_numeric_columns, country_columns_nan_percentage  = process_new_data(country_data_pre_process)
        return country_data, country_all_columns, country_numeric_columns, country_non_numeric_columns, country_columns_nan_percentage, 'current'

#-----------End of Function validate_data_source_select-----------#

# --------------------------------------------------------------------------#
# Function: process_new_data                                                #
# Goal:     Prepare and clean the DataFrame                                 #
#           1. Remove duplicates, if any, based on the Country column       #
#           2. Set the country name as index of the DataFrame               #
#           3. Identify empty cells on each row and remove rows in which    #
#              the number of empty cells exceeds a pre-defined threshold    #
#              ( Default is 10% )                                           #
#           4. Identify NaNs                                                #
#                                                                           #
# Input:    New DataFrame read from the API                                 #
#                                                                           #
# Return:   1. Cleaned DataFrame                                            #
#           2. List of all columns ( after index replaced to country name ) #
#           3. List of all numeric columns                                  #
#           4. List of all non-numeric columns                              #
#           5. A dictionary that holds each of the numeric column names     #
#              as key and the percentage of empty cells in each column      #
#---------------------------------------------------------------------------#
def process_new_data(datain):
    # Open a log file for debug and review
    with open('country_data_anlyze_and_process_log.txt', 'w') as log_file:
        log_file.write(f'Log opened at: {dt.datetime.now(zi.ZoneInfo("Asia/Jerusalem")).strftime("%Y-%m-%d %H:%M:%S")}\n')
        log_file.write(f'Starting Analysis and Processing...\n')

    # ---------------------- Removing Duplicates on the 'Country' Column----------------------------#
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

    # ------------------------Changing index to Country and analyzing------------------------------#
        datain.set_index('Country', inplace=True)
    # -----------------------------------End of Index replacement-----------------------------------#

    # -----------------------Profiling the Dataset and handling empty cells-------------------------#
        # Assigning all columns in the DataFrame to a list
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
        # Total numeric rows: 32
        row_na_removal_threshold = 0.9  # Min required percentage of non-empty cells in a row (checked over the numeric columns of the dataset )
        datain.dropna(subset=numeric_column_list,thresh=math.ceil((len(numeric_column_list) * row_na_removal_threshold)),inplace=True)

        # Check how many rows were removed and report in the log
        length_post_NA_rows_removal = len(datain)
        delta_length_post_NA_removal = length_post_duplicates_removal - length_post_NA_rows_removal
        log_file.write(f"\n#------Report how many rows (countries) were removed----------------------#\n")
        log_file.write(f'Original length of dataset before removal of NA rows was {length_post_duplicates_removal}\n')
        log_file.write(f'Length of dataset after removal of NA rows is {length_post_NA_rows_removal}\n')
        log_file.write(f"Total of {delta_length_post_NA_removal} rows with more than {int(math.ceil((1 - row_na_removal_threshold) * 100))}% empty cells on the numerical columns of the dataset were identified and removed from the dataset ")
        log_file.write(f'\n#-----------------------------------------------------------------------#\n')

        # Identify the percentage of empty cells in each numeric columns
        # Create a dictionaly and a single row DataFrame containing this information
        columns_nan_percentage = dict()
        for column_name in numeric_column_list:
            columns_nan_percentage[column_name] = round((1 - float(datain[column_name].count() / len(datain))) * 100, 1)


        log_file.write(f'\n#-------List of nan_percentage per column ---------#\n')
        for key in columns_nan_percentage:
            log_file.write(f'{key}: {columns_nan_percentage[key]}\n')

        log_file.write(f'#----------------------------------------------------:\n')

    # Create a copy of the datain before return - no further processing will be done on the processed DataFrame inplace
    country_data_post_process = datain.copy()
    return country_data_post_process, country_column_list, numeric_column_list, non_numeric_column_list, columns_nan_percentage

#-----------End of Function process_new_API_data--------------------#