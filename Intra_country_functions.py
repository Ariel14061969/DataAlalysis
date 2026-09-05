# ----------------------------------------------------------------------------------------#
#                           Intra Country functions                                       #
#-----------------------------------------------------------------------------------------#
# This file contains functions that are used to analyze the data of a single              #
# country from the file "country_with_data.csv"                                           #
#                                                                                         #
# List of functions included:                                                             #
# 1. Country ID - receives the data of a country as a row and prints it in an ID format   #
# 2. gdp per
#
#-----------------------------------------------------------------------------------------#

# Import libraries
from libs_and_modules import *

def get_country_id_data(country_row, country_all_columns):
    df_country = country_row
    country_id = dict()
    country_name = list(df_country.index)[0]
    country_id['Country_Name'] = country_name
    for key in country_all_columns:
        country_id[key] = df_country.loc[country_name][key]
    #return country_id
    formatted_data = ''
    #country_id_dict = get_country_id_data(country_row_local, country_all_columns)
    for key, value in country_id.items():
        if key == 'flag_url':
            continue
        else:
            formatted_data += f"{key}: {value}\n"

    # Create a narrower column for the text area
    #col1, col2 = st.columns([0.5, 2])  # Adjust column ratios for desired width
    col1, col2 = st.columns([1, 7])  # Adjust column ratios for desired width

    with col1:
        # Display the bold white header using markdown with HTML
        st.markdown("<h3 style='color:white;'><b>Country ID</b></h3>", unsafe_allow_html=True)
        # Display the text area with an empty label as the title is above it
        #st.text_area("", formatted_data, height=400)
        st.text_area("Country Details Label", formatted_data, height=400, label_visibility='hidden')




