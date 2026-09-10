# Import libraries
from libs_and_modules import *

def inter_continent(country_data):
    #Lior Sinay 10/09/26 - Put in comment,importing * from libs and modules
    #import seaborn as sns
    #import matplotlib.pyplot as plt
    #libs_and_modules
    figs = []
    df = country_data
    exclude_col = ["gdp","rel","population","surface_area"]

    DivideByPop = ['tourists','area','co2_emissions','imports','exports','refugees']
    ng=0
    for col in df.keys():

        if col not in exclude_col and  isinstance(df.loc[df.index[0],col],float):
            if ng % 4 == 0:
                #Lior Sinay 10/09/2026 - replaced plt with plt.pyplot
                #fig, axes = plt.subplots(2,2,figsize=(12, 6))
                fig, axes = plt.pyplot.subplots(2, 2, figsize=(12, 6))
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
            ax.legend(loc='lower left',fontsize=7,framealpha=0.3)
            if ng % 4 == 1:
                figs.append(fig)
            ng=ng+1
    return figs
