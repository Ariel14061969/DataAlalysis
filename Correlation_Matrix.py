from matplotlib import pyplot as plt


def correlation_matrix(country_data):

    from matplotlib import pyplot as plt
    import seaborn as sns

    df=country_data
    DivideByPop = ['tourists', 'area', 'co2_emissions','imports','exports']
    exclude_col = ["gdp", "rel", "surface_area"]
    for col in df.keys():
        if col in DivideByPop:
                df[col]=df[col]/df['population']
        if col in exclude_col or not isinstance(df.loc[df.index[0],col],float):
            df.drop(columns=[col],inplace=True)
    matrix = abs(df.corr())
    fig, ax = plt.subplots()
    sns.heatmap(matrix,ax=ax)
    return fig,matrix

def plot_interesting_correlations(country_data, matrix, threshold = 0.8):

    figs =[]
    ng = 0
    n_subg =4
    for i, row in enumerate(matrix.index):
                    # Slice from the current row to the end using columns
                    for col in matrix.columns[i:]:
                        val = matrix.loc[row, col]
                        if val > threshold and col != row:
                            if ng % n_subg == 0:
                                fig, axes = plt.subplots(2, 2, figsize=[12, 5])
                                axes = axes.flatten()
                            axc = axes[ng % n_subg]
                            axc.scatter(country_data[row], country_data[col],s=5)
                            axc.set_xlabel(row,fontsize=7)
                            axc.set_ylabel(col,fontsize=7)
                            axc.tick_params(axis='both', labelsize=7)
                            if ng % n_subg == 1:
                                figs.append(fig)
                            ng = ng + 1
    return figs

