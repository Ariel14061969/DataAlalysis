# Import libraries
from libs_and_modules import *

# ---------------------------------------------------------------------------------------------------------------------#
# Function: run_intra_country_analysis                                                                                 #
#                                                                                                                      #
# Goal:     A wrapper function that launches all inta country analysis functions one by one                            #                                                                                      #
#                                                                                                                      #
# Input:    1. country_row - The specific row of the target country from the analyzed dataset                          #
#           2. country_all_columns - A list of all the columns in the dataset (used as parameters of the analyzed row  #
#                                                                                                                      #
# Return:   None ( VOID )                                                                                              #
#----------------------------------------------------------------------------------------------------------------------#
def run_intra_country_analysis(country_row, country_all_columns):
    get_country_id_data(country_row, country_all_columns)
    single_counrty_plots(country_row)
#----------------------------------End of Function run_intra_country_analysis------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Function: get_country_id_data                                                                                        #
#                                                                                                                      #
# Goal:     Create a country "ID card" by showing relevant information from the dataset                                #
#                                                                                                                      #
# Input:    1. country_row - The specific row of the target country from the analyzed dataset                          #
#           2. country_all_columns - A list of all the columns in the dataset (used as parameters of the analyzed row  #
#                                                                                                                      #
# Return:   None ( VOID )                                                                                              #
#----------------------------------------------------------------------------------------------------------------------#
def get_country_id_data(country_row, country_all_columns):
    df_country = country_row
    country_id = dict()
    country_name = list(df_country.index)[0]
    country_id['Country_Name'] = country_name
    for key in country_all_columns:
        country_id[key] = df_country.loc[country_name][key]

    # Prepare the content of the country ID
    formatted_data = ''
    for key, value in country_id.items():
        if (key == 'flag_url'):
            continue
        elif (value is None):
            formatted_data += f"{key}: No Data\n"
        else:
            formatted_data += f"{key}: {value}\n"

    # Define the Text Box structure and text format
    col1, col2 = st.columns([2, 7])  # Adjust column ratios for desired width
    with col1:
        st.markdown("<h3 style='color:white;'><b>Country ID</b></h3>", unsafe_allow_html=True)
        st.text_area("Country Details Label", formatted_data, height=400, label_visibility='hidden')
#-------------------------------------End of Function get_country_id_data-----------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Function: single_country_plots                                                                                       #
#                                                                                                                      #
# Goal:     Create the following plots for the selected country:                                                       #
#           1. gdp growth vs. fertility ( bar plot )                                                                   #
#           2. Import vs. Export ( bar plot )                                                                          #
#           3. Employment breakdown ( pie chart )                                                                      #
#           4. School enrollment (primary, secondary and post secondary) - male vs females                             #
#           5. Life expectancy male vs. female                                                                         #
#                                                                                                                      #
#                                                                                                                      #
# Input:    1. country_row - The specific row of the target country from the analyzed dataset                          #
#                                                                                                                      #
# Return:   None ( VOID )                                                                                              #
#----------------------------------------------------------------------------------------------------------------------#
def single_counrty_plots(country_row):
    country_name = list(country_row.index)[0]

    # ---------------Plotting gdp_growth vs. fertility-----------------------#
    col1, col2 = st.columns([1, 1])

    with col1:
        plot_data_gdp_fert = country_row.loc[country_name][['gdp_growth', 'fertility']]
        # Create a bar plot for GDP Growth and Fertility
        fig_gdp_fert, ax_gdp_fert = plt.pyplot.subplots(figsize=(8, 5))
        plot_data_gdp_fert.plot(kind='bar', ax=ax_gdp_fert, color=['skyblue', 'lightcoral'])

        ax_gdp_fert.set_title('GDP Growth vs. Fertility')
        ax_gdp_fert.set_ylabel('Value in [%]')
        ax_gdp_fert.set_xlabel('Indicator')
        ax_gdp_fert.tick_params(axis='x', rotation=0)
        plt.pyplot.grid(axis='y', linestyle='--', alpha=0.7)
        plt.pyplot.tight_layout()
        st.pyplot(fig_gdp_fert)
    #------------------End of bar plot for gdp growth vs. fertility------------#

    # --------------------Plotting gdp growth vs. population growth---------------------------#
    with col2:
        plot_data_gdp_pop = country_row.loc[country_name][['gdp_growth', 'pop_growth']]
        fig_gdp_pop, ax_gdp_pop = plt.pyplot.subplots(figsize=(8, 5))
        plot_data_gdp_pop.plot(kind='bar', ax=ax_gdp_pop, color=['lightgreen', 'yellow'])

        ax_gdp_pop.set_title('GDP Growth vs. Population Growth')
        ax_gdp_pop.set_ylabel('Value in [%]')
        ax_gdp_pop.set_xlabel('Indicator')
        ax_gdp_pop.tick_params(axis='x', rotation=0)

        plt.pyplot.grid(axis='y', linestyle='--', alpha=0.7)
        plt.pyplot.tight_layout()
        st.pyplot(fig_gdp_pop)
    # ------------------End of bar plot for gdp growth vs. population growth-------------------#


    # ----------------Plotting Import vs. Export----------------#
    col3, col4 = st.columns([1, 1])

    with col3:
        plot_data_imports_exports = country_row.loc[country_name][['imports', 'exports']]
        # Create a bar plot for Imports and Exports
        fig_imports_exports, ax_imports_exports = plt.pyplot.subplots(figsize=(8, 5))
        plot_data_imports_exports.plot(kind='bar', ax=ax_imports_exports, color=['red', 'green'])

        ax_imports_exports.set_title('Imports vs. Exports')
        ax_imports_exports.set_ylabel('Value in Millions of $')
        ax_imports_exports.set_xlabel('Indicator')
        ax_imports_exports.tick_params(axis='x', rotation=0)

        plt.pyplot.grid(axis='y', linestyle='--', alpha=0.7)
        plt.pyplot.tight_layout()
        st.pyplot(fig_imports_exports)
    # ------------------End of bar plot for Import vs. Export-------------------#

    # ---------Plotting employment sectors breakdown in a pie chart -----------#
    with col4:
        # Pie chart for employment data
        employment_sectors = ['employment_agriculture', 'employment_industry', 'employment_services']
        employment_values = country_row[employment_sectors].values[0]
        sum_employment = employment_values.sum()

        # Calculate the 'Other' category
        other_employment = 100 - sum_employment if sum_employment < 100 else 0  # Assuming values are percentages

        pie_data = list(employment_values) + [other_employment]
        pie_labels = ['Agriculture', 'Industry', 'Services', 'Other']
        pie_colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']  # Different colors for sectors

        fig_employment_pie, ax_employment_pie = plt.pyplot.subplots(figsize=(8, 5))
        #ax_employment_pie.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', startangle=90, colors=pie_colors,
        #                      pctdistance=0.85)
        wedges, texts, autotexts = ax_employment_pie.pie(pie_data, labels=None, autopct='%1.1f%%', startangle=90,
                                                         colors=pie_colors, pctdistance=0.85)
        ax_employment_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax_employment_pie.set_title('Employment by Sector')

        # Create custom legend labels with values
        legend_labels = [f'{label}: {value:.1f}%' for label, value in zip(pie_labels, pie_data)]
        ax_employment_pie.legend(wedges, legend_labels, title="Sectors", loc="lower left", bbox_to_anchor=(-0.1, -0.2))

        plt.pyplot.tight_layout()
        st.pyplot(fig_employment_pie)
    # ------------------End of pie chart for employment sectors-------------------#


    # ---------------Plotting School Enrollment male vs. Female-----------------------#
    col5, col6 = st.columns([1, 1])

    with col5:
        # Bar plot for enrollment data
        enrollment_data_male = country_row[
            ['primary_school_enrollment_male', 'secondary_school_enrollment_male', 'post_secondary_enrollment_male']].T
        enrollment_data_female = country_row[['primary_school_enrollment_female', 'secondary_school_enrollment_female',
                                              'post_secondary_enrollment_female']].T

        # The user asked for 'post_secondary_enrollment_male'/'female' twice. Assuming they wanted to combine some or show them distinct.
        # For clarity, I will take the distinct values. If the user meant a specific aggregate or different metric, further clarification is needed.
        # Based on the available data, 'secondary_school_enrollment_male' and 'secondary_school_enrollment_female' might also be relevant, but user only specified 'primary' and 'post_secondary'.

        # Prepare data for plotting
        enrollment_df = pd.DataFrame({
            'Male': [country_row['primary_school_enrollment_male'].values[0],
                     country_row['secondary_school_enrollment_male'].values[0],
                     country_row['post_secondary_enrollment_male'].values[0]],
            'Female': [country_row['primary_school_enrollment_female'].values[0],
                       country_row['secondary_school_enrollment_female'].values[0],
                       country_row['post_secondary_enrollment_female'].values[0]
                       ]
        }, index=['Primary School', 'Secondary School', 'Post Secondary'])

        fig_enrollment, ax_enrollment = plt.pyplot.subplots(figsize=(8, 5))
        enrollment_df.plot(kind='bar', ax=ax_enrollment, color={'Male': 'steelblue', 'Female': 'palevioletred'})

        ax_enrollment.set_title('School Enrollment (Male vs. Female)')
        ax_enrollment.set_ylabel('Enrollment Rate (%)')
        ax_enrollment.set_xlabel('Education Level')
        ax_enrollment.tick_params(axis='x', rotation=45)
        plt.pyplot.grid(axis='y', linestyle='--', alpha=0.7)
        plt.pyplot.tight_layout()
        st.pyplot(fig_enrollment)
    #------------------End of bar plot for School Enrollment-------------------#

    # ---------------Plotting Life Expectancy male vs. female------------------#
    with col6:
        plot_data_life_expectancy = country_row.loc[country_name][['life_expectancy_male', 'life_expectancy_female']]
        fig_life_expectancy, ax_life_expectancy = plt.pyplot.subplots(figsize=(8, 5))
        plot_data_life_expectancy.plot(kind='bar', ax=ax_life_expectancy, color=['blue', 'gold'])

        ax_life_expectancy.set_title('Life Expectancy Male vs. Female')
        ax_life_expectancy.set_ylabel('Value in Years')
        ax_life_expectancy.set_xlabel('Indicator')
        ax_life_expectancy.tick_params(axis='x', rotation=0)

        plt.pyplot.grid(axis='y', linestyle='--', alpha=0.7)
        plt.pyplot.tight_layout()
        st.pyplot(fig_life_expectancy)
    # ------------------End of bar Life Expectancy-------------------#