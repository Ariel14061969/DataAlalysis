# Import libraries
from libs_and_modules import *

# ---------------------------------------------------------------------------------------------------------------------#
# Function: run_intra_region_analysis                                                                                  #
#                                                                                                                      #
# Goal:     A wrapper function that launches all intra region analysis functions one by one                            #                                                                                      #
#                                                                                                                      #
# Input:    1. df_region - A subset of the original dataset, containing all data for the selected region               #
#                                                                                                                      #
# Return:   None ( VOID )                                                                                              #
#----------------------------------------------------------------------------------------------------------------------#
def run_intra_region_analysis(df_region):
    region_name = df_region.region.iloc[0]
    country_list = list(df_region.index) # List of countries that are specified for the selected region
    # Open the Intra region analysis log file
    log_file = open('intra_region_functions_log.txt', 'a+')
    log_file.write(f'Log for region {region_name} opened at: {dt.datetime.now(zi.ZoneInfo("Asia/Jerusalem")).strftime("%Y-%m-%d %H:%M:%S")} Jerusalm time. '
                   f'UTC time is {dt.datetime.now(zi.ZoneInfo("UTC")).strftime("%Y-%m-%d %H:%M:%S")}\n')
    log_file.write(f'#--------------------------------------------------------------------------------------------------------------------------------------------#\n')
    log_file.write(f'\n There are {len(country_list)} countries in the dataset of this region:\n')
    for country in country_list:
        log_file.write(f'{country}\n')

    log_file.write(f'\n#-------------------------------------------------------------------------------------------#\n')

    # Call the analysis functions
    single_region_plots(df_region, region_name, log_file)
    log_file.close()
#----------------------------------End of Function run_intra_country_analysis------------------------------------------#

# ---------------------------------------------------------------------------------------------------------------------#
# Function: single_region_plots                                                                                        #
#                                                                                                                      #
# Goal:     Create various informative plots for the selected region                                                   #
#                                                                                                                      #
# Input:    1. df_region - A subset of the original dataset, containing all data for the selected region               #
#                                                                                                                      #
# Return:   None ( VOID )                                                                                              #
#----------------------------------------------------------------------------------------------------------------------#
def single_region_plots(df_region,region_name, log_file):

    # Add a column as complementary of the employment sectors to 100%
    df_region['employment_other'] = 100 - (df_region['employment_industry'] +
                                              df_region['employment_services'] +
                                              df_region['employment_agriculture'] )

    log_file.write(f'\n\nStarting single_region_plots function\n')
    log_file.write(f'#----------------------------#\n')


    #-------------------------Create histogram and box plot for GDP----------------------#
    col1, col2 = st.columns([1, 1])
    with col1:
        fig_gdp, ax_gdp = plt.pyplot.subplots(figsize=(8, 6))
        sns.histplot(data=df_region, x='gdp', bins=10, ax=ax_gdp, color='green', kde = True)
        ax_gdp.set_title(f'Distribution of GDP for {region_name}')
        ax_gdp.set_xlabel('GDP [Millions of $]')
        ax_gdp.set_ylabel('Number of Countries')
        plt.pyplot.tight_layout()
        st.pyplot(fig_gdp)

    with col2:
        fig_gdp_bp, ax_gdp_bp = plt.pyplot.subplots(figsize=(8, 6))
        sns.boxplot(data=df_region, x='region', y='gdp', ax=ax_gdp_bp, color='green')
        ax_gdp_bp.set_title(f'GDP for region {region_name}, a boxplot representation')
        ax_gdp_bp.set_xlabel('')
        ax_gdp_bp.set_ylabel('GDP [Millions of $]')
        plt.pyplot.tight_layout()
        st.pyplot(fig_gdp_bp)

    # ----------------------End of histogram and box plots for GDP --------------------------- #

    # -------------------Create histogram and box plot for GDP Per Capita----------------------#
    col3, col4 = st.columns([1, 1])
    with col3:
        fig_gdp_per_capita, ax_gdp_per_capita = plt.pyplot.subplots(figsize=(8, 6))
        sns.histplot(data=df_region, x='gdp_per_capita', bins=10, ax=ax_gdp_per_capita, color='royalblue', kde = True)
        ax_gdp_per_capita.set_title(f'Distribution of GDP Per Capita for {region_name}')
        ax_gdp_per_capita.set_xlabel('GDP Per Capita [$]')
        ax_gdp_per_capita.set_ylabel('Number of Countries')
        plt.pyplot.tight_layout()
        st.pyplot(fig_gdp_per_capita)

    with col4:
        fig_gdp_per_capita_bp, ax_gdp_per_capita_bp = plt.pyplot.subplots(figsize=(8, 6))
        sns.boxplot(data=df_region, x='region', y='gdp_per_capita', ax=ax_gdp_per_capita_bp, color='royalblue')
        ax_gdp_per_capita_bp.set_title(f'GDP Per Capita for region {region_name}, a boxplot representation')
        ax_gdp_per_capita_bp.set_xlabel('')
        ax_gdp_per_capita_bp.set_ylabel('GDP Per Capita [$]')
        plt.pyplot.tight_layout()
        st.pyplot(fig_gdp_per_capita_bp)

    # --------------------End of histogram and box plots for GDP Per Capita ----------------------------#

    # -----------Overlay plot for the distribution of gdp vs gdp_per_capita (existing plot)-------------#
    fig_gdp_gdp_capita, ax1 = plt.pyplot.subplots(figsize=(14, 7))  # Create a figure and a primary axes

    # Plot GDP on the first y-axis
    df_region_sorted_gdp = df_region.sort_values('gdp', ascending = False)
    sns.barplot(x=df_region_sorted_gdp.index, y='gdp', data=df_region_sorted_gdp, color='green', ax=ax1, label='GDP')
    ax1.set_xlabel('Country')
    ax1.set_ylabel('GDP [Millions of $]', color='green')
    ax1.tick_params(axis='y', labelcolor='green')
    ax1.set_xticks(range(len(df_region_sorted_gdp.index)))  # Explicitly set tick locations
    ax1.set_xticklabels(df_region_sorted_gdp.index, rotation=90, ha='right')

    # Create a second y-axis that shares the same x-axis
    ax2 = ax1.twinx()

    # Plot GDP per Capita on the second y-axis
    sns.lineplot(x=df_region_sorted_gdp.index, y='gdp_per_capita', data=df_region_sorted_gdp, color='royalblue', marker='o', ax=ax2,
                 label='GDP per Capita')
    ax2.set_ylabel('GDP per Capita [$]', color='royalblue')
    ax2.tick_params(axis='y', labelcolor='royalblue')

    # Add title and combined legends
    plt.pyplot.title(f'GDP vs. GDP per Capita for countries in {region_name} ')
    fig_gdp_gdp_capita.tight_layout()  # Adjust layout to prevent labels from overlapping

    # Combine legends from both axes
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    st.pyplot(fig_gdp_gdp_capita)

    # ---------------------End of overlay plot for gdp and gdp per capita----------------- #

    # --------------------Create histograms for GDP growth and pop growth------------------#
    col5, col6 = st.columns([1, 1])
    with col5:
        fig_gdp_growth, ax_gdp_growth = plt.pyplot.subplots(figsize=(8, 6))
        sns.histplot(data=df_region, x='gdp_growth', bins=10, ax=ax_gdp_growth, color='lightgreen', kde = True)
        ax_gdp_growth.set_title(f'Distribution of GDP Growth for {region_name}')
        ax_gdp_growth.set_xlabel('GDP Growth[%]')
        ax_gdp_growth.set_ylabel('Number of Countries')
        plt.pyplot.tight_layout()
        st.pyplot(fig_gdp_growth)

    with col6:
        fig_pop_growth, ax_pop_growth = plt.pyplot.subplots(figsize=(8, 6))
        sns.histplot(data=df_region, x='pop_growth', bins=10, ax=ax_pop_growth, color='lightgrey', kde = True)
        ax_pop_growth.set_title(f'Distribution of Population Growth for {region_name}')
        ax_pop_growth.set_xlabel('Population Growth[%]')
        ax_pop_growth.set_ylabel('Number of Countries')
        plt.pyplot.tight_layout()
        st.pyplot(fig_pop_growth)

    # ---------------End of histogram plots for GDP Growth and Population Growth Per Capita ---------------#

    # ----------------------------Create Box plot for gdp_growth and pop_growth--------------------------#
    # Prepare data for boxplot
    df_growth_unified = df_region[['gdp_growth', 'pop_growth']].melt(var_name='Growth_Type',
                                                                       value_name='Growth_Value')

    fig_growth_bp, ax_growth_bp = plt.pyplot.subplots(figsize=(14, 7))
    sns.boxplot(data=df_growth_unified, x='Growth_Type', y='Growth_Value', hue='Growth_Type',
                palette={'gdp_growth': 'lightgreen', 'pop_growth': 'lightgrey'}, ax=ax_growth_bp, legend=False)

    ax_growth_bp.set_title(f'GDP Growth and Population Growth for countries in {region_name}')
    ax_growth_bp.set_xlabel('Growth Type')
    ax_growth_bp.set_ylabel('Growth Rate [%]')
    ax_growth_bp.set_xticks([0, 1])  # Explicitly set tick locations
    ax_growth_bp.set_xticklabels(['GDP Growth', 'Population Growth'])  # Set custom x-axis labels
    plt.pyplot.tight_layout()
    st.pyplot(fig_growth_bp)
    # ----------------------------End of Boxplot for gdp_growth and pop_growth---------------------------#

    # ----------------------------Create histogram and box plot for Fertility----------------------------#
    col7, col8 = st.columns([1, 1])
    with col7:
        fig_fertility_rate, ax_fertility_rate = plt.pyplot.subplots(figsize=(8, 6))
        sns.histplot(data=df_region, x='fertility', bins=5, ax=ax_fertility_rate, color='gold', kde = True)
        ax_fertility_rate.set_title(f'Distribution of fertility rate for {region_name}')
        ax_fertility_rate.set_xlabel('Ferility rate [Average number of children per woman]')
        ax_fertility_rate.set_ylabel('Number of Countries')
        plt.pyplot.tight_layout()
        st.pyplot(fig_fertility_rate)

    with col8:
        fig_fertility_rate_bp, ax_fertility_rate_bp = plt.pyplot.subplots(figsize=(8, 6))
        sns.boxplot(data=df_region, x='region', y='fertility', ax=ax_fertility_rate_bp, color='gold')
        ax_fertility_rate_bp.set_title(f'Fertility for countries in {region_name}, a boxplot representation')
        ax_fertility_rate_bp.set_xlabel('')
        ax_fertility_rate_bp.set_ylabel('Fertility [Average number of children per woman]')
        plt.pyplot.tight_layout()
        st.pyplot(fig_fertility_rate_bp)

    # -----------------------------End of histogram and box plots for Fertility--------------------------#

    # --------------------------------Create Box plot for employment sectors-----------------------------#
    df_employment_unified = df_region[['employment_industry', 'employment_agriculture', 'employment_services',
                                          'employment_other']].melt(var_name='Employment_Sectors',value_name='Sector_Portion')

    fig_employment_bp, ax_employment_bp = plt.pyplot.subplots(figsize=(14, 7))
    sns.boxplot(data=df_employment_unified, x='Employment_Sectors', y='Sector_Portion', hue='Employment_Sectors',
                palette={'employment_industry': 'lightgrey', 'employment_agriculture': 'lightgreen',
                         'employment_services': 'magenta','employment_other': 'gold' }, ax=ax_employment_bp, legend=False)

    ax_employment_bp.set_title(f'Portion Of Employment Sectors for countries in {region_name}')
    ax_employment_bp.set_xlabel('Employment Sectors')
    ax_employment_bp.set_ylabel('Sector Portion [%]')
    ax_employment_bp.set_xticks([0, 1, 2, 3])  # Explicitly set tick locations
    ax_employment_bp.set_xticklabels(['employment_industry', 'employment_agriculture', 'employment_services','employment_other' ])  # Set custom x-axis labels
    plt.pyplot.tight_layout()
    st.pyplot(fig_employment_bp)

    # -------------------------------End of Box plot for employment sectors-----------------------------#


    # ----------------------------Create histogram and box plot for unemployment rate---------------------------------#
    col9, col10 = st.columns([1, 1])
    with col9:
        fig_unemployment, ax_unemployment = plt.pyplot.subplots(figsize=(8, 6))
        sns.histplot(data=df_region, x='unemployment', bins=10, ax=ax_unemployment, color='orange', kde = True)
        ax_unemployment.set_title(f'Distribution of unemployment rate for countries in {region_name}')
        ax_unemployment.set_xlabel('Unemployment Rate [%]')
        ax_unemployment.set_ylabel('Number of Countries')
        plt.pyplot.tight_layout()
        st.pyplot(fig_unemployment)

    with col10:
        fig_unemployment_bp, ax_unemployment_bp = plt.pyplot.subplots(figsize=(8, 6))
        sns.boxplot(data=df_region, x='region', y='unemployment', ax=ax_unemployment_bp, color='orange')
        ax_unemployment_bp.set_title(f'Unemployment rate for countries in {region_name}, a boxplot representation')
        ax_unemployment_bp.set_xlabel('')
        ax_unemployment_bp.set_ylabel('Unemployment Rate [%]')
        plt.pyplot.tight_layout()
        st.pyplot(fig_unemployment_bp)

    # ----------------------------End of histogram and box plot for unemployment---------------------------- #

    # ----------------------------Create histogram and box plot for sex ratio---------------------------------#
    col11, col12 = st.columns([1, 1])
    with col11:
        fig_sex_ratio, ax_sex_ratio = plt.pyplot.subplots(figsize=(8, 6))
        sns.histplot(data=df_region, x='sex_ratio', bins=10, ax=ax_sex_ratio, color='lightsalmon', kde = True)
        ax_sex_ratio.set_title(f'Distribution of sex ratio for countries in {region_name}')
        ax_sex_ratio.set_xlabel('sex ratio [males per 100 females]')
        ax_sex_ratio.set_ylabel('Number of Countries')
        plt.pyplot.tight_layout()
        st.pyplot(fig_sex_ratio)

    with col12:
        fig_sex_ratio_bp, ax_sex_ratio_bp = plt.pyplot.subplots(figsize=(8, 6))
        sns.boxplot(data=df_region, x='region', y='sex_ratio', ax=ax_sex_ratio_bp, color='lightsalmon')
        ax_sex_ratio_bp.set_title(f'Distribution of sex ratio for countries in {region_name}, a boxplot representation')
        ax_sex_ratio_bp.set_xlabel('')
        ax_sex_ratio_bp.set_ylabel('sex ratio [males per 100 females]')
        plt.pyplot.tight_layout()
        st.pyplot(fig_sex_ratio_bp)

    # ----------------------------End of histogram and box plot for sex ratio---------------------------- #

    # --------------------Create violin plots for school enrollment and life expectancy-------------------#
    col13, col14 = st.columns([1, 1])
    with col13:
    # Violin plot for school enrollment by gender
        enrollment_cols = [
            'primary_school_enrollment_female', 'primary_school_enrollment_male',
            'secondary_school_enrollment_female', 'secondary_school_enrollment_male',
            'post_secondary_enrollment_female', 'post_secondary_enrollment_male'
        ]
        df_school_enrollment_violin = df_region[enrollment_cols].copy()

    # Melt the DataFrame to long format for violin plot
        df_school_enrollment_unified_violin = df_school_enrollment_violin.melt(var_name='Enrollment_Gender', value_name='Enrollment_Value')

    # Extract 'Enrollment_Type' and 'Gender' from 'Enrollment_Gender'
        df_school_enrollment_unified_violin['Enrollment_Type'] = df_school_enrollment_unified_violin['Enrollment_Gender'].apply(
            lambda x: x.split(' female')[0].split(' male')[0].replace('_', ' '))
        df_school_enrollment_unified_violin['Gender'] = df_school_enrollment_unified_violin['Enrollment_Gender'].apply(
            lambda x: 'Female' if 'female' in x else 'Male')

    # Create the violin plot
        fig_enrollment, ax_enrollment = plt.pyplot.subplots(figsize=(8, 6))
        sns.violinplot(x='Enrollment_Type', y='Enrollment_Value', hue='Gender', data=df_school_enrollment_unified_violin, split=True,
                       ax=ax_enrollment, palette={'Female': 'magenta', 'Male': 'orange'})

        ax_enrollment.set_title(f'School Enrollment Distribution by Gender for countries in {region_name}')
        ax_enrollment.set_xlabel('')
        ax_enrollment.set_ylabel('Enrollment Rate [%]')
        ax_enrollment.legend(title='Gender')

    # Define custom labels
        custom_labels = [
            'primary_school',
            'secondary_school',
            'post_secondary'
        ]

    # Remove x-ticks
        ax_enrollment.set_xticks([])

    # Add a single custom label for 'primary school enrollment'
    # The x-position for the first category is 0.
        y_axes_offset = -0.01
        ax_enrollment.text(0.5, y_axes_offset, 'primary_school', ha='center', va='top',
                           transform=ax_enrollment.get_xaxis_transform())
        ax_enrollment.text(2.5, y_axes_offset, 'secondary_school', ha='center', va='top',
                           transform=ax_enrollment.get_xaxis_transform())
        ax_enrollment.text(4.5, y_axes_offset, 'post_secondary', ha='center', va='top',
                           transform=ax_enrollment.get_xaxis_transform())

    # Add vertical lines between categories
        num_categories = len(df_school_enrollment_unified_violin['Enrollment_Type'].unique())
        for i in range(num_categories - 1):
            ax_enrollment.axvline(x=i + 0.5, color='gray', linestyle='--', linewidth=0.8)

        plt.pyplot.tight_layout()
        st.pyplot(fig_enrollment)


    # Start Violin plot for life expectancy per gender
    with col14:
        life_expectancy_cols = ['life_expectancy_female', 'life_expectancy_male']
        df_life_expectancy = df_region[life_expectancy_cols].copy()

    # Melt the DataFrame to long format for violin plot
        df_life_expectancy_unified_violin = df_life_expectancy.melt(var_name='Life_Expectancy_Gender',
                                                                    value_name='Life_Expectancy_Value')

    # Create a 'Population' category for the x-axis
        df_life_expectancy_unified_violin['Category'] = 'Population'

    # Extract 'Gender' from 'Life_Expectancy_Gender'
        df_life_expectancy_unified_violin['Gender'] = df_life_expectancy_unified_violin['Life_Expectancy_Gender'].apply(
            lambda x: 'Female' if 'female' in x else 'Male')

    # Create the violin plot
        fig_life_expectancy, ax_life_expectancy = plt.pyplot.subplots(figsize=(8, 6))
        sns.violinplot(x='Category', y='Life_Expectancy_Value', hue='Gender', data=df_life_expectancy_unified_violin,
                       split=True, ax=ax_life_expectancy, palette={'Female': 'magenta', 'Male': 'orange'})

        ax_life_expectancy.set_title(f'Life Expectancy Distribution by Gender for countries in {region_name}')
        ax_life_expectancy.set_xlabel('')
        ax_life_expectancy.set_ylabel('Life Expectancy [Years]')
        ax_life_expectancy.legend(title='Gender')

        plt.pyplot.tight_layout()
        st.pyplot(fig_life_expectancy)
    # ----------------  End of Violin plots for school enrollment and life expectancy by gender-----------------------#

    # -----------------------------Create histogram and box plot for Infant Mortality---------------------------------#
    col19, col20 = st.columns([1, 1])
    with col19:
        fig_infant_mortality, ax_infant_mortality = plt.pyplot.subplots(figsize=(8, 6))
        sns.histplot(data=df_region, x='infant_mortality', bins=10, ax=ax_infant_mortality, color='red', kde = True)
        ax_infant_mortality.set_title(f'Distribution of infant mortality for countries in {region_name}')
        ax_infant_mortality.set_xlabel('Infant Mortality Rate [per 1000 live births]')
        ax_infant_mortality.set_ylabel('Number of Countries')
        plt.pyplot.tight_layout()
        st.pyplot(fig_infant_mortality)

    with col20:
        fig_infant_mortality_bp, ax_infant_mortality_bp = plt.pyplot.subplots(figsize=(8, 6))
        sns.boxplot(data=df_region, x='region', y='infant_mortality', ax=ax_infant_mortality_bp, color='red')
        ax_infant_mortality_bp.set_title(f'Distribution of infant mortality for countries in {region_name}, a boxplot representation')
        ax_infant_mortality_bp.set_xlabel('')
        ax_infant_mortality_bp.set_ylabel('Infant Mortality Rate [per 1000 live births]')
        plt.pyplot.tight_layout()
        st.pyplot(fig_infant_mortality_bp)

    # ----------------------------End of histogram and box plot for Infant Mortality----------------------- #

    # ----------------------------Create histogram and box plot for CO2 Emissions---------------------------#
    col21, col22 = st.columns([1, 1])
    with col21:
        fig_co2_emissions, ax_co2_emissions = plt.pyplot.subplots(figsize=(8, 6))
        sns.histplot(data=df_region, x='co2_emissions', bins=10, ax=ax_co2_emissions, color='cyan', kde = True)
        ax_co2_emissions.set_title(f'Distribution of co2 emissions for countries in {region_name}')
        ax_co2_emissions.set_xlabel('CO2 emissions [Millions of metric tons]')
        ax_co2_emissions.set_ylabel('Number of Countries')
        plt.pyplot.tight_layout()
        st.pyplot(fig_co2_emissions)

    with col22:
        fig_co2_emissions_bp, ax_co2_emissions_bp = plt.pyplot.subplots(figsize=(8, 6))
        sns.boxplot(data=df_region, x='region', y='co2_emissions', ax=ax_co2_emissions_bp, color='cyan')
        ax_co2_emissions_bp.set_title(f'Distribution of co2 emissions for countries in {region_name}, a boxplot representation')
        ax_co2_emissions_bp.set_xlabel('')
        ax_co2_emissions_bp.set_ylabel('CO2 emissions [Millions of metric tons]')
        plt.pyplot.tight_layout()
        st.pyplot(fig_co2_emissions_bp)

    # ----------------------------End of histogram and box plot for CO2 Emissions----------------------- #

    # ----------------------------Create histogram and box plot on Tourists-----------------------------#
    col23, col24 = st.columns([1, 1])
    with col23:
        fig_tourists, ax_tourists = plt.pyplot.subplots(figsize=(8, 6))
        sns.histplot(data=df_region, x='tourists', bins=10, ax=ax_tourists, color='salmon', kde = True)
        ax_tourists.set_title(f'Distribution data on number tourists for countries in {region_name}')
        ax_tourists.set_xlabel('Number of Tourists [In Thousands]')
        ax_tourists.set_ylabel('Number of Countries')
        plt.pyplot.tight_layout()
        st.pyplot(fig_tourists)

    with col24:
        fig_tourists_bp, ax_tourists_bp = plt.pyplot.subplots(figsize=(8, 6))
        sns.boxplot(data=df_region, x='region', y='tourists', ax=ax_tourists_bp, color='salmon')
        ax_tourists_bp.set_title(f'Distribution data on number tourists for countries in {region_name}, a boxplot representation')
        ax_tourists_bp.set_xlabel('')
        ax_tourists_bp.set_ylabel('Number of Tourists [In Thousands]')
        plt.pyplot.tight_layout()
        st.pyplot(fig_tourists_bp)

    # ----------------------------End of histogram and box plot on Tourists----------------------- #


    # --------------------------Create histogram and box plot on Homicide rate---------------------#
    col25, col26 = st.columns([1, 1])
    with col25:
        fig_homicide_rate, ax_homicide_rate = plt.pyplot.subplots(figsize=(8, 6))
        sns.histplot(data=df_region, x='homicide_rate', bins=10, ax=ax_homicide_rate, color='red', kde = True)
        ax_homicide_rate.set_title(f'Distribution of homicide rate for countries in {region_name}')
        ax_homicide_rate.set_xlabel('Homicide rate [%]')
        ax_homicide_rate.set_ylabel('Number of Countries')
        plt.pyplot.tight_layout()
        st.pyplot(fig_homicide_rate)

    with col26:
        fig_homicide_rate_bp, ax_homicide_rate_bp = plt.pyplot.subplots(figsize=(8, 6))
        sns.boxplot(data=df_region, x='region', y='homicide_rate', ax=ax_homicide_rate_bp, color='red')
        ax_homicide_rate_bp.set_title(f'Distribution of homicide rate for countries in {region_name}, a boxplot representation')
        ax_homicide_rate_bp.set_xlabel('')
        ax_homicide_rate_bp.set_ylabel('Homicide rate [%]')
        plt.pyplot.tight_layout()
        st.pyplot(fig_homicide_rate_bp)

    # ----------------------------End of histogram and box plot on Homicide rate----------------------- #


    # --------------------------Create histogram and box plot on refugees portion ---------------------#
    df_refugees_extended = df_region
    df_refugees_extended['refugees_portion'] = (df_refugees_extended.refugees/df_refugees_extended.population)*100
    col27, col28 = st.columns([1, 1])
    with col27:
        fig_refugees_portion, ax_refugees_portion = plt.pyplot.subplots(figsize=(8, 6))
        sns.histplot(data=df_refugees_extended, x='refugees_portion', bins=10, ax=ax_refugees_portion, color='purple', kde = True)
        ax_refugees_portion.set_title(f'Distribution of refugees portion from total population for countries in {region_name}')
        ax_refugees_portion.set_xlabel('refugees_portion [%]')
        ax_refugees_portion.set_ylabel('Number of Countries')
        plt.pyplot.tight_layout()
        st.pyplot(fig_refugees_portion)

    with col28:
        fig_refugees_portion_bp, ax_refugees_portion_bp = plt.pyplot.subplots(figsize=(8, 6))
        sns.boxplot(data=df_refugees_extended, x='region', y='refugees_portion', ax=ax_refugees_portion_bp, color='purple')
        ax_refugees_portion_bp.set_title(f'Distribution of refugees portion from total population for countries in {region_name}, a boxplot representation')
        ax_refugees_portion_bp.set_xlabel('')
        ax_refugees_portion_bp.set_ylabel('refugees_portion [%]')
        plt.pyplot.tight_layout()
        st.pyplot(fig_refugees_portion_bp)

    # ----------------------------End of histogram and box plot on refugees portion----------------------- #
    log_file.write(f'\nsingle_region_plots function concluded\n')
    log_file.write(f'#-----------------------------------------------------------------------#\n')
