def inter_continent(country_data):
    import seaborn as sns
    import matplotlib.pyplot as plt
    #libs_and_modules
    figs = []
    df = country_data
    exclude_col = ["gdp","rel","population","surface_area"]

    DivideByPop = ['tourists','area','co2_emissions']
    ng=0
    for col in df.keys():

        if col not in exclude_col and  isinstance(df.loc[df.index[0],col],float):
            if ng % 4 == 0:
                fig, axes = plt.subplots(2,2,figsize=(12, 6))
                axes = axes.flatten()
            ax = axes[ng % 4]
            lb = col
            if col in DivideByPop:
                df['rel']= df[col]/df['population']
                sns.barplot(data=df, x='rel',  hue='Continent',ax=ax)
                lb = lb + ' per capita'
                ax.set_xlabel(lb)
            else:
                sns.barplot(data=df, x=col,  hue='Continent',ax=ax)
            if ng % 4 == 1:
                figs.append(fig)
            ng=ng+1
    return figs
