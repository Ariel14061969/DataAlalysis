def inter_region(country_data):
    import seaborn as sns
    import statistics as stt
    import matplotlib.pyplot as plt
    figs = []
    df = country_data

    exclude_col = ["gdp","rel","population","surface_area"]

    DivideByPop = ['tourists','area','co2_emissions']
    for col in df.keys():

        if col not in exclude_col and  isinstance(df.loc[df.index[0],col],float):
            grouped_df = df.groupby('region')[col].mean()
            fig, ax = plt.subplots(figsize=(8, 5))

            lb = col
            if col in DivideByPop:
                df['rel']= df[col]/df['population']
                lb = lb + ' per capita'


            sns.barplot(x=grouped_df, y=grouped_df.index, ax=ax)
            plt.xlabel(lb)
            figs.append(fig)
    return figs
