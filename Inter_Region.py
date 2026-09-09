# Import libraries
from libs_and_modules import *

def inter_region(country_data):

    # Lior Sinay 10/09/26 - Put in comment. Reading * from libs and modules instead
    #import seaborn as sns
    #import statistics as stt
    #import matplotlib.pyplot as plt
    figs = []
    df = country_data

    exclude_col = ["gdp","rel","population","surface_area"]

    DivideByPop = ['tourists','area','co2_emissions','imports','exports','refugees']
    ng =0
    for col in df.keys():

        if col not in exclude_col and  isinstance(df.loc[df.index[0],col],float):
            grouped_df = df.groupby('region')[col].mean()
            if ng % 4 ==0:
                #Lior Sinay 10/09/26 - Replaced plt with plt.pyplot
                #fig, axes = plt.subplots(2,2,figsize=(12, 6))
                fig, axes = plt.pyplot.subplots(2, 2, figsize=(12, 6))
                axes = axes.flatten()
            ax = axes[ng % 4]
            lb = col
            if col in DivideByPop:
                df['rel']= df[col]/df['population']
                lb = lb + ' per capita'


            sns.barplot(x=grouped_df, y=grouped_df.index, ax=ax)

            max_val = max(bar.get_width() for bar in ax.patches)
            min_val = min(bar.get_width() for bar in ax.patches)
            # 3. Highlight the bar that matches the maximum width
            for bar in ax.patches:
                if bar.get_width() == max_val:
                    bar.set_facecolor('green')  # Highlight color
                if bar.get_width() == min_val:
                    bar.set_facecolor('red')  # Highlight color

            ax.set_xlabel(lb, fontsize=7)
            ax.set_ylabel("")
            ax.tick_params(axis='both', labelsize=7)
            if ng % 4 == 1:
                figs.append(fig)
            ng = ng+1
    return figs
