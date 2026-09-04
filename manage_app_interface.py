# Import libraries
from libs_and_modules import *

# Import Functions
from import_country_data import import_country_data

# -------------------------------------------------------------------------#
# Function: validate_data_source_select                                    #
# Goal:     Validate the user selection of data source. While input is     #
#           not a valid valid value it clears the input and waits for a    #
#           valid value.                                                   #
# Input:    None                                                           #
# Return:   None ( VOID )                                                  #
#--------------------------------------------------------------------------#
def validate_data_source_select():
    current_input = st.session_state.data_source_select_input
    if ((current_input.lower() != 'y') & (current_input.lower() != 'n')):
        st.error(f"'{current_input}' is not a valid selection, please select either 'y' or 'n'. Clearing input.")
        st.session_state.data_source_select_input = ""  # If validation fails, clear the input by setting its session_state value to an empty string

#-----------End of Function validate_data_source_select--------------------#


# -------------------------------------------------------------------------#
# Function: st_ui_start                                                    #
#                                                                          #
# Goals:                                                                   #
# 1. Ask for user name and selecion of data source ( imported / existing ) #
# 2. Validate the user selection of data source, using function            #
#    "validate_data_source_select"                                         #
# 3. Based on a valid user selection of the data source, it runs           #
#    the proper analysis and returns the clean dataframe to the            #
#    process that invoked it.                                              #
#                                                                          #
# Input:  None                                                             #
# Return: A clean dataframe for further data analysis                      #
#--------------------------------------------------------------------------#
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
        country_data = process_new_data(country_data_pre_process)
        return country_data, 'current'

#-----------End of Function validate_data_source_select-----------#

# ------------------------------------------------------------------------#
# Function: process_new_API_data                                          #
# Goal:     Prepare and clean the DataFrame                               #
#           1. Remove duplicates, if any, based on the Country column     #
#           2. Set the country name as index of the DataFrame             #
#           3. Identify NaNs                                              #
#                                                                         #
# Input:    New DataFrame read from the API                               #
# Return:   Cleaned DataFrame                                             #
#-------------------------------------------------------------------------#
def process_new_data(datain):
    datain.drop_duplicates(subset='Country', keep='first', inplace=True)
    datain.set_index('Country', inplace=True)
    country_data_post_process = datain.copy()
    return country_data_post_process

#-----------End of Function process_new_API_data--------------------#