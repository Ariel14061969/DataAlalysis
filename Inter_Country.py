# Lior Sinay 10/09/26 - placed in comment , importing * from libs and modules
#from statistics import mean

# Import libraries
from libs_and_modules import *

def inter_country(country_data,MyCountry,compareTo='World'):

    # Lior Sinay 10/09/26 - placed in comment , importing * from libs and modules
    #import seaborn as sns
    #import matplotlib.pyplot as plt

    figs=[]
    MyContinent = country_data.loc[MyCountry,'Continent']
    MyRegion = country_data.loc[MyCountry,'region']
    exclude_col = ["gdp","rel","population","surface_area"]



    if compareTo == 'World':
        df=country_data
    elif compareTo == 'Continent':
        df = country_data[country_data['Continent']==MyContinent]
    else: #compareTo == 'Region':
        df = country_data[country_data['region']==MyRegion]

    DivideByPop = ['tourists','area','co2_emissions','imports','exports','refugees']
    ng=0
    for col in df.keys():
        if col not in exclude_col and isinstance(df.loc[MyCountry,col],float):
            df['rel']=df[col]
            lb = col
            if col in DivideByPop:
                df['rel']= df['rel']/df['population']
                lb = lb + ' per capita'

            if ng % 4 == 0:
                # Lior Sinay 10/09/26 - replaced plt with plt.pyplot
                #fig, axes = plt.subplots(2,2,figsize=(12, 6))
                fig, axes = plt.pyplot.subplots(2, 2, figsize=(12, 6))
                axes = axes.flatten()
            ax = axes[ng % 4]

            sns.histplot(df['rel'].dropna() , bins = 30,ax=ax)
            min_country = df['rel'].idxmin()
            max_country = df['rel'].idxmax()
            median_country = (df['rel'] - df['rel'].median()).abs().idxmin()
            countries_of_interest =[min_country,max_country,median_country]
            ax.set_xlabel(lb)
            if df.loc[MyCountry,'rel']:
                max_count = max([bar.get_height() for bar in ax.containers[0]])

                xval = df.loc[MyCountry,'rel']

                ax.vlines(x=xval, ymin=0, ymax=max_count, colors="red", linestyles="dashed", lw=2)
                ax.text(x=xval, y=max_count * 0.75, s=f" {MyCountry}", color="red", rotation=0, va='top')
                for countryOfInterest in countries_of_interest:
                    xval = df.loc[countryOfInterest, 'rel']
                    ax.vlines(x=xval, ymin=0, ymax=max_count, colors="green", linestyles="dashed", lw=1)
                    ax.text(x=xval, y=max_count , s=f" {countryOfInterest}",  color="green", rotation=45, va='top')
            if ng % 4 ==  1:
                figs.append(fig)
            ng=ng+1

    return figs