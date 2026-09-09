def units_txt():
    import pandas as pd
    df = pd.DataFrame(columns=['var', 'explain'])
    df.loc[0, 'var'] = 'gdp per capita'
    df.loc[0, 'explain'] = 'Gross Domestic Product ($/person)'
    df.loc[1, 'var'] = 'gdp growth'
    df.loc[1, 'explain'] = 'GDP growth rate is measured as a percentage (%) change'
    df.loc[2, 'var'] = 'sex ratio'
    df.loc[ 2, 'explain'] = ('the proportion of males to females in a population, '
                         'expressed as the number of males for every 100 females')
    df.loc[3, 'var'] = 'unemployment'
    df.loc[3, 'explain'] = 'The percentage of unemployed people (%)'
    df.loc[4, 'var'] = 'homicide rate'
    df.loc[4, 'explain'] = 'number of homicide per 100,000 population per year'
    df.loc[5, 'var'] = 'urban population'
    df.loc[5, 'explain'] = 'Percentage(%) of people living in urban areas'
    df.loc[6, 'var'] = 'urban population growth'
    df.loc[6, 'explain'] = 'Annual percentage growth of people living in urban areas'
    df.loc[7, 'var'] = 'employment agriculture'
    df.loc[7, 'explain'] = 'Percentage (%) of a nation''s active workforce engaged in Agriculture,'
    df.loc[8, 'var'] = 'employment industry'
    df.loc[8, 'explain'] = 'Percentage (%) of a nation''s active workforce engaged in Industry'
    df.loc[9, 'var'] = 'employment services'
    df.loc[9, 'explain'] = 'Percentage (%) of a nation''s active workforce engaged in Services'
    df.loc[10, 'var'] = 'pop growth'
    df.loc[10, 'explain'] = 'Annual population percentage(%) change'
    df.loc[11, 'var'] = 'infant mortality'
    df.loc[11, 'explain'] = 'the number of resident infant deaths under one year of age per 1000 live births'
    df.loc[12, 'var'] = 'fertility'
    df.loc[12, 'explain'] = 'Average number of live births per woman over her lifetime'
    df.loc[13, 'var'] = 'pop density'
    df.loc[13, 'explain'] = 'Persons per square Km (person/Km^2)'
    df.loc[14, 'var'] = 'life expectancy female'
    df.loc[14, 'explain'] = 'average female life expectancy in years'
    df.loc[15, 'var'] = 'life expectancy male'
    df.loc[15, 'explain'] = 'average male life expectancy in years'
    df.loc[16, 'var'] = 'primary school enrollment male'
    df.loc[16, 'explain'] = 'Percentage (%) of the official primary school-age male population'
    df.loc[17, 'var'] = 'primary school enrollment female'
    df.loc[17, 'explain'] = 'Percentage (%) of the official primary school-age female population'
    df.loc[18, 'var'] = 'secondary school enrollment male'
    df.loc[18, 'explain'] = 'Percentage (%) of the official secondary school-age male population'
    df.loc[19, 'var'] = 'secondary school enrollment female'
    df.loc[19, 'explain'] = 'Percentage (%) of the official secondary school-age female population'
    df.loc[20, 'var'] = 'refugees per capita'
    df.loc[20, 'explain'] = 'refugees per resident'
    df.loc[21, 'var'] = 'tourists per capita'
    df.loc[21, 'explain'] = 'tourists per resident'
    df.loc[22, 'var'] = 'internet users'
    df.loc[22, 'explain'] = 'Percentage(%) of internet users (ages 15-74)'
    df.loc[23, 'var'] = 'co2 emissions per capita'
    df.loc[23, 'explain'] = 'CO2 emissions per capita are measured in tonnes of carbon dioxide per person per year (tCO₂/capita/year)'
    df.loc[24, 'var'] = 'forested area'
    df.loc[24, 'explain'] = 'Percentage(%) of forested area out of total land area'
    df.loc[25, 'var'] = 'imports per capita'
    df.loc[25, 'explain'] = 'measured in $/person'
    df.loc[26, 'var'] = 'exports per capita'
    df.loc[26, 'explain'] = 'measured in $/person'

    country_columns = ['gdp',
                       'sex_ratio',
                       'surface_area',
                       'life_expectancy_male',
                       'unemployment',
                       'homicide_rate',
                       'urban_population_growth',
                       'secondary_school_enrollment_female',
                       'employment_agriculture',
                       'co2_emissions',
                       'forested_area',
                       'tourists',
                       'life_expectancy_female',
                       'post_secondary_enrollment_female',
                       'post_secondary_enrollment_male',
                       'primary_school_enrollment_female',
                       'infant_mortality',
                       'gdp_growth',
                       'population',
                       'urban_population',
                       'secondary_school_enrollment_male',
                       'pop_growth',
                       'region',
                       'pop_density',
                       'internet_users',
                       'gdp_per_capita',
                       'fertility',
                       'refugees',
                       'primary_school_enrollment_male',
                       'employment_industry',
                       'employment_services',
                       'imports',
                       'exports']
    return df
