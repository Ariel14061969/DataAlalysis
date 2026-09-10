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
def run_intra_country_analysis(country_row, country_all_columns ):
    # Open the Intra country analysis log file
    log_file = open('intra_country_functions_log.txt', 'a+')
    log_file.write(f'Log opened at: {dt.datetime.now(zi.ZoneInfo("Asia/Jerusalem")).strftime("%Y-%m-%d %H:%M:%S")} Jerusalm time. '
                   f'UTC time is {dt.datetime.now(zi.ZoneInfo("UTC")).strftime("%Y-%m-%d %H:%M:%S")}\n')
    log_file.write(f'#------------------------------------------------------------------------------------------------------------#\n')

    # Call the analysis functions
    get_country_id_data(country_row, country_all_columns,log_file)
    single_counrty_plots(country_row,log_file)
    log_file.close()
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
def get_country_id_data(country_row, country_all_columns,log_file):
    log_file.write(f'\nStarting country ID function\n')
    log_file.write(f'#----------------------------#\n')
    df_country = country_row
    country_id = dict()
    country_name = list(df_country.index)[0]
    country_id['Country_Name'] = country_name
    for key in country_all_columns:
        country_id[key] = df_country.loc[country_name][key]

    empty_columns = list()
    # Prepare the content of the country ID
    formatted_data = ''
    for key, value in country_id.items():
        if (key == 'flag_url'):
            svg_data = requests.get(df_country.loc[country_name, 'flag_url']).content

            # Convert vector SVG data into a rasterized PNG byte stream
            png_data = svg.svg2png(bytestring=svg_data)
            img = Image.open(BytesIO(png_data))
            st.image(img)
            continue
        elif (pd.isna(value)):
            formatted_data += f"{key}: No Data\n"
            log_file.write(f'{key}: No Data\n')
            empty_columns.append(key)  # Record the empty cells that are not the flag_url
        else:
            formatted_data += f"{key}: {value}\n"
            log_file.write(f'{key}: {value}\n')

    # Define the Text Box structure and text format
    col1, col2 = st.columns([2, 7])  # Adjust column ratios for desired width
    with col1:
        st.markdown("<h3 style='color:white;'><b>Country ID</b></h3>", unsafe_allow_html=True)
        st.text_area("Country Details Label", formatted_data, height=400, label_visibility='hidden')

    # Print the cells with no data to the log file
    if empty_columns:
        log_file.write(f'\nThe following columns are empty and reported as "No Data" in the country ID:\n')
        log_file.write('[\n')
        for val in empty_columns:
            log_file.write(f'{val}\n')
        log_file.write(']')

    else:
        log_file.write(f'\nNo empty cells were found in the data for {country_name}.\n')

    log_file.write(f'\n\nCountry ID function concluded\n')
    log_file.write(f'#---------------------------------------------------------------#\n')

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
def single_counrty_plots(country_row,log_file):
    log_file.write(f'\n\nStarting single_country_plots function\n')
    log_file.write(f'#----------------------------#\n')

    country_name = list(country_row.index)[0]

    # Identify missing data for plot selection
    plots_column_allocation = {
        'imports_and_exports'            : None,
        'gdp_growth_vs_pop_growth'       : None,
        'urban_pop_growth_vs_pop_growth' : None,
        'employment_sectors'             : None,
        'school_enrollment'              : None,
        'life_expectancy'                : None
    }
    plot_columns_counter = 0
    max_possible_num_of_plots = len(plots_column_allocation.keys())

    # Extract the value of each relevant column
    imports_val = country_row.loc[country_name]['imports']
    exports_val = country_row.loc[country_name]['exports']
    gdp_growth_val = country_row.loc[country_name]['gdp_growth']
    pop_growth_val = country_row.loc[country_name]['pop_growth']
    urban_pop_growth_val = country_row.loc[country_name]['urban_population_growth']

    employment_val = [ country_row.loc[country_name]['employment_services'],
                       country_row.loc[country_name]['employment_industry'],
                       country_row.loc[country_name]['employment_agriculture']]

    school_enrollment_val = [ country_row.loc[country_name]['primary_school_enrollment_male'],
                              country_row.loc[country_name]['primary_school_enrollment_female'],
                              country_row.loc[country_name]['secondary_school_enrollment_male'],
                              country_row.loc[country_name]['secondary_school_enrollment_female'],
                              country_row.loc[country_name]['post_secondary_enrollment_male'],
                              country_row.loc[country_name]['post_secondary_enrollment_female'] ]

    life_expectancy_val = [country_row.loc[country_name]['life_expectancy_male'],
                           country_row.loc[country_name]['life_expectancy_female'] ]

    # Allocate columns for plots
    if ((not pd.isna(imports_val)) & (not pd.isna(exports_val))):
        plot_columns_counter += 1
        plots_column_allocation['imports_and_exports'] = 'col' + str(plot_columns_counter)

    if ((not pd.isna(gdp_growth_val)) & (not pd.isna(pop_growth_val))):
        plot_columns_counter += 1
        plots_column_allocation['gdp_growth_vs_pop_growth'] = 'col' + str(plot_columns_counter)

    if ((not pd.isna(pop_growth_val)) & (not pd.isna(urban_pop_growth_val))):
        plot_columns_counter += 1
        plots_column_allocation['urban_pop_growth_vs_pop_growth'] = 'col' + str(plot_columns_counter)

    if all(not pd.isna(val) for val in employment_val):
        plot_columns_counter += 1
        plots_column_allocation['employment_sectors'] = 'col' + str(plot_columns_counter)

    if all(not pd.isna(val) for val in school_enrollment_val):
        plot_columns_counter += 1
        plots_column_allocation['school_enrollment'] = 'col' + str(plot_columns_counter)

    if all(not pd.isna(val) for val in life_expectancy_val):
        plot_columns_counter += 1
        plots_column_allocation['life_expectancy'] = 'col' + str(plot_columns_counter)

    # Update log file - Cells with missing values
    num_of_empty_cells = max_possible_num_of_plots - plot_columns_counter
    if num_of_empty_cells > 0:
        log_file.write(f'\n\nThere are {num_of_empty_cells} cells in the plot list that have no data. Here are their names:\n')
        no_data_columns = country_row.columns[country_row.isnull().any()].tolist()
        if no_data_columns:
            for column_name in no_data_columns:
                log_file.write(f'column_name\n')

        log_file.write(f'\n\nThe following plots were not drawn since one or more of their values has no data:\n')
        for key,value in plots_column_allocation.items():
            if value is None:
                log_file.write(f'{key}\n')
    else:
        log_file.write(f'\nAll cells used for plots have data. All figures plotted\n')


    # ---------------Plotting Imports vs. Exports ( Trade Balance ) -----------------------#
    if plot_columns_counter >= 1:
        col1, col2 = st.columns([1, 1])

        if plots_column_allocation['imports_and_exports'] is not None:
            with col1:
                plot_data_imports_exports = country_row.loc[country_name][['imports', 'exports']]
                fig_imports_exports, ax_imports_exports = plt.pyplot.subplots(figsize=(8, 5))
                plot_data_imports_exports.plot(kind='bar', ax=ax_imports_exports, color=['red', 'green'])

                ax_imports_exports.set_title('Imports vs. Exports ( Trade Balance )')
                ax_imports_exports.set_ylabel('Value in Millions of $')
                ax_imports_exports.set_xlabel('Indicator')
                ax_imports_exports.tick_params(axis='x', rotation=0)

                plt.pyplot.grid(axis='y', linestyle='--', alpha=0.7)
                plt.pyplot.tight_layout()
                st.pyplot(fig_imports_exports)

    #------------------End of bar plot for Imports vs. Exports ----------------------------#

    # --------------------Plotting gdp growth vs. population growth---------------------------#
        if plots_column_allocation['gdp_growth_vs_pop_growth'] is not None:
            col_num = plots_column_allocation['gdp_growth_vs_pop_growth']
            if ((col_num == 'col1') | (plots_column_allocation['imports_and_exports'] is None)):
                with col1:
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

            else:
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


    # ----------------Plotting Urban population growth vs Total population growth----------------#
        col3, col4 = st.columns([1, 1])

        if plots_column_allocation['urban_pop_growth_vs_pop_growth'] is not None:
            with col3:
                plot_data_urban_pg_vs_total_pg = country_row.loc[country_name][['urban_population_growth', 'pop_growth']]
                fig_urban_pg_vs_total_pg, ax_urban_pg_vs_total_pg = plt.pyplot.subplots(figsize=(8, 5))
                plot_data_urban_pg_vs_total_pg.plot(kind='bar', ax=ax_urban_pg_vs_total_pg, color=['red', 'green'])

                ax_urban_pg_vs_total_pg.set_title('Urban Population Growth vs. Total Population Growth')
                ax_urban_pg_vs_total_pg.set_ylabel('Value in [%]')
                ax_urban_pg_vs_total_pg.set_xlabel('Indicator')
                ax_urban_pg_vs_total_pg.tick_params(axis='x', rotation=0)

                plt.pyplot.grid(axis='y', linestyle='--', alpha=0.7)
                plt.pyplot.tight_layout()
                st.pyplot(fig_urban_pg_vs_total_pg)
    # ------------------End of bar plot for Urban Population Growth vs Total Population Growth-------------------#

    # ---------Plotting employment sectors breakdown in a pie chart -----------#
        if plots_column_allocation['employment_sectors'] is not None:
            col_num = plots_column_allocation['employment_sectors']
            if (((col_num == 'col1') | (col_num == 'col2') | (col_num == 'col3')) & (plots_column_allocation['imports_and_exports'] is None)):
                with col3:
                    employment_sectors = ['employment_agriculture', 'employment_industry', 'employment_services']
                    employment_values = country_row[employment_sectors].values[0]
                    sum_employment = employment_values.sum()

                    # Calculate the 'Other' category
                    other_employment = 100 - sum_employment if sum_employment < 100 else 0  # Assuming values are percentages

                    pie_data = list(employment_values) + [other_employment]
                    pie_labels = ['Agriculture', 'Industry', 'Services', 'Other']
                    pie_colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']  # Different colors for sectors

                    fig_employment_pie, ax_employment_pie = plt.pyplot.subplots(figsize=(8, 5))
                    wedges, texts, autotexts = ax_employment_pie.pie(pie_data, labels=None, autopct='%1.1f%%',
                                                                     startangle=90,
                                                                     colors=pie_colors, pctdistance=0.85)
                    ax_employment_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                    ax_employment_pie.set_title('Employment by Sector')

                    # Create custom legend labels with values
                    legend_labels = [f'{label}: {value:.1f}%' for label, value in zip(pie_labels, pie_data)]
                    ax_employment_pie.legend(wedges, legend_labels, title="Sectors", loc="lower left",
                                             bbox_to_anchor=(-0.1, -0.2))

                    plt.pyplot.tight_layout()
                    st.pyplot(fig_employment_pie)
            else:
                with col4:
                    employment_sectors = ['employment_agriculture', 'employment_industry', 'employment_services']
                    employment_values = country_row[employment_sectors].values[0]
                    sum_employment = employment_values.sum()

                    # Calculate the 'Other' category
                    other_employment = 100 - sum_employment if sum_employment < 100 else 0  # Assuming values are percentages

                    pie_data = list(employment_values) + [other_employment]
                    pie_labels = ['Agriculture', 'Industry', 'Services', 'Other']
                    pie_colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']  # Different colors for sectors

                    fig_employment_pie, ax_employment_pie = plt.pyplot.subplots(figsize=(8, 5))
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

        if plots_column_allocation['school_enrollment'] is not None:
            with col5:

                enrollment_df = pd.DataFrame({
                    'Male': [country_row['primary_school_enrollment_male'].values[0],
                             country_row['secondary_school_enrollment_male'].values[0],
                             country_row['post_secondary_enrollment_male'].values[0]],
                    'Female': [country_row['primary_school_enrollment_female'].values[0],
                               country_row['secondary_school_enrollment_female'].values[0],
                               country_row['post_secondary_enrollment_female'].values[0]]
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
        if plots_column_allocation['life_expectancy'] is not None:
            col_num = plots_column_allocation['life_expectancy']
            if (((col_num == 'col1') | (col_num == 'col2') | (col_num == 'col3') | (col_num == 'col4') | (col_num == 'col5')) & (plots_column_allocation['school_enrollment'] is None)) :
                with col5:
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
            else:
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

    log_file.write(f'\nsingle_counrty_plots function concluded\n')
    log_file.write(f'#-----------------------------------------------------------------------#\n')
