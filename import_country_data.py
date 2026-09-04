# Import libraries
from libs_and_modules import *

def import_country_data(filename):
    with open(".streamlit/secrets.toml", "rb") as f:
        config = tomllib.load(f)
    # print(config['api_key'])

    country_data = pd.read_csv('countries.csv')
    country_data.set_index('Country', inplace=True)
    country_data['flag_url']= ""
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
                       'exports',
                       'capital']

    for col in country_columns:
        country_data[col] = None

    # get country flag and country data using api
    for country in country_data.index:
        print(country)
        country_ISO2 = country_data.loc[country,'ISO2']
        api_url_flag = 'https://api.api-ninjas.com/v1/countryflag?country={}'.format(country_ISO2)
        response = requests.get(api_url_flag, headers={'X-Api-Key': config['api_key']})
        if response.status_code == requests.codes.ok:
            res = response.json()
            if res:
                country_data.loc[country,'flag_url']= res['rectangle_image_url']
        else:
            print("Error:", response.status_code, response.text)

        api_url_country = 'https://api.api-ninjas.com/v1/country?name={}'.format(country)
        response = requests.get(api_url_country, headers={'X-Api-Key': config['api_key']})
        if response.status_code == requests.codes.ok:
            res = response.json()
            if res:
                for col in country_columns:
                    if col in res[0].keys():
                        country_data.loc[country,col]=res[0][col]


    country_data.to_csv(filename)  # Write the dataframe to a csv file

#---------End of Function "import_country_data"-----------#
