from statistics import mean


def inter_country(country_data,MyCountry,compareTo='World'):

    import seaborn as sns
    import matplotlib.pyplot as plt

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

    DivideByPop = ['tourists','area','co2_emissions']
    for col in df.keys():
        if col not in exclude_col and isinstance(df.loc[MyCountry,col],float):
            df['rel']=df[col]
            lb = col
            if col in DivideByPop:
                df['rel']= df['rel']/df['population']
                lb = lb + ' per capita'


            fig, ax = plt.subplots(figsize=(8, 5))

            sns.histplot(df['rel'].dropna() , bins = 30,ax=ax)
            min_country = df['rel'].idxmin()
            max_country = df['rel'].idxmax()
            median_country = (df['rel'] - df['rel'].median()).abs().idxmin()
            countries_of_interest =[min_country,max_country,median_country]
            plt.xlabel(lb)
            if df.loc[MyCountry,'rel']:
                max_count = max([bar.get_height() for bar in ax.containers[0]])

                xval = df.loc[MyCountry,'rel']

                plt.vlines(x=xval, ymin=0, ymax=max_count, colors="red", linestyles="dashed", lw=2)
                plt.text(x=xval, y=max_count * 0.75, s=f" {MyCountry}", color="red", rotation=0, va='top')
                for countryOfInterest in countries_of_interest:
                    xval = df.loc[countryOfInterest, 'rel']
                    plt.vlines(x=xval, ymin=0, ymax=max_count, colors="green", linestyles="dashed", lw=1)
                    plt.text(x=xval, y=max_count , s=f" {countryOfInterest}",  color="green", rotation=45, va='top')
                figs.append(fig)

    return figs