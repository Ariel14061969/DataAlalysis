def inter_continent(country_data):
    import seaborn as sns
    import statistics as stt
    import matplotlib.pyplot as plt
    #libs_and_modules
    figs = []
    df = country_data
    exclude_col = ["gdp","rel","population","surface_area"]

    DivideByPop = ['tourists','area','co2_emissions']
    for col in df.keys():

        if col not in exclude_col and  isinstance(df.loc[df.index[0],col],float):
            fig, ax = plt.subplots(figsize=(8, 5))

            lb = col
            if col in DivideByPop:
                df['rel']= df[col]/df['population']
                sns.barplot(data=df, x='rel',  hue='Continent',ax=ax)
                lb = lb + ' per capita'
                plt.xlabel(lb)
            else:
                sns.barplot(data=df, x=col,  hue='Continent')
            figs.append(fig)
    return figs
