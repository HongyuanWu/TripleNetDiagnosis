# coding: utf-8
import os
import re
import numpy as np
import pandas as pd
import seaborn as sns
from kerasy.utils import findLowerUpper

# set the `plotly.io.orca.config.executable` property to the full path of your orca executable.
# If you use `environment.yml` to create anaconda environment, this command automatically correct the path.
import plotly
conda_env_name = "triple-net-diagnosis"
result = re.findall(pattern=fr"\/.*\/versions\/{conda_env_name}\/", string=plotly.__path__[0])
if len(result)>0:
    plotly.io.orca.config.executable = os.path.join(result[0], "bin/orca")

import plotly.express as px

def volcanoplot(df, logFC=1.2, p_val=0.05, hover_data=[],
                FC_col="FC.Value", p_val_col="P.Value", logFC_col="logFC", log_p_val_col="-log10(P.Value)"):
    """ Volcano plot.
    @params df         : (pd.DataFrame) Input data. This
    @params logFC      : (float) threshold value.
    @params p_val      : (float) threshold value.
    @params hover_data : (list)  colnames for hover labels.
    """
    col_names = df.columns
    hover_data = [col for col in hover_data if col in col_names]
    # Add necessary data.
    if log_p_val_col not in col_names:
        df.loc[:, log_p_val_col] = -np.log10(df[p_val_col].values)
    if logFC_col not in col_names:
        df.loc[:, logFC_col] = np.log2(df[FC_col].values)
    # Add coloring labels.
    df.loc[:, "p_significance"]  = df[p_val_col] < p_val
    df.loc[:, "Significant"] = "normal"
    df.loc[df["p_significance"] & (df[logFC_col] >  logFC), "Significant"] = "up"
    df.loc[df["p_significance"] & (df[logFC_col] < -logFC), "Significant"] = "down"
    color_discrete_map={"up": "red", "down": "blue", "normal": "lightgray"}
    # Fill NaN & get data info.
    df  = df.fillna("-")
    (x_min,y_min),(x_max,y_max) = findLowerUpper(df[[logFC_col, log_p_val_col]].values, margin=0)
    # Plot.
    fig = px.scatter(df, x=logFC_col, y=log_p_val_col, color="Significant", color_discrete_map=color_discrete_map, hover_data=hover_data)
    fig.add_shape(type="line", y0=y_min, y1=y_max, x0=-logFC,           x1=-logFC,           line=dict(color="black", width=2, dash="dot"))
    fig.add_shape(type="line", y0=y_min, y1=y_max, x0=logFC,            x1=logFC,            line=dict(color="black", width=2, dash="dot"))
    fig.add_shape(type="line", x0=x_min, x1=x_max, y0=-np.log10(p_val), y1=-np.log10(p_val), line=dict(color="black", width=2, dash="dot"))
    return fig

def MAthresholding(x, logFC=1.2, p_val=0.05, verbose=True,
                   plot_volcano=False, hover_data=[], title="", save_path=None):
    """
    @params x            : (str/pd.DataFrame) Input data.
    @params logFC        : (float) threshold value.
    @params p_val        : (float) threshold value.
    @params verbose      : (bool)  Whether print information or not.
    @params plot_volcano : (bool)  Whethre plot volcanoplot or not.
    @params hover_data   : (list)  colnames for hover labels.
    @params title        : (str)   title for figure.
    @params save_path    : (str)   A string representing a local file path.
    """
    # Load original DataFrame.
    df = x if isinstance(x, pd.DataFrame) else pd.read_csv(str(x), sep="\t")
    before = len(df)
    # Drop NaN data.
    df = df.dropna(axis=0, how="any", subset=["logFC", "P.Value"])
    middle = len(df)
    if plot_volcano:
        fig = volcanoplot(df=df, logFC=logFC, p_val=p_val, hover_data=hover_data)
        fig.update_layout(title=title, font=dict(family="Monaco", size=18, color="#7f7f7f"))
        fig.show()
        # Save figure.
        if save_path is not None:
            fig.write_image(save_path)
            if verbose: print(f"volcano plot was saved at `{save_path}`")
    # Thresholding
    df = df[(abs(df["logFC"])>logFC) & (df["P.Value"]<p_val)]
    after  = len(df)
    # print result.
    if verbose:
        title = title + " : " if len(title)>0 else title
        print(f"{title}{before} --[drop NaN]-> {middle} --[threshold]-> {after} ({after/before:>6.1%})")
    return df

def applyMAthresh2all(gen, colnames=[], logFC=1.2, p_val=0.05, verbose=True,
                      plot_volcano=False, volcano_save_dir=".",
                      plot_clustermap=False, clustermap_save_dir=".",):
    """Apply `MAthresholding` to all data.
    @params colnames     : (list)  Column Names for features you want to extract.
    @params logFC        : (float) threshold value.
    @params p_val        : (float) threshold value.
    @params verbose      : (bool) Whether print info or not.
    @params plot_*       : (bool) Whether plot or not.
    @params *_save_dir   : (str)  Where you want to save *plot.
    """
    if verbose:
        print("Apply MicroArray thresholding to all data.")
        print(f"|logFC| > {logFC}")
        print(f"p_val < {p_val}")
        print("="*42)
    if isinstance(colnames, str):
        colnames = [colnames]
    lst = []
    for path in gen:
        if isinstance(path, tuple) and len(path)==2:
            path, eset_path = path
        fn = str(path).split("/")[-1]
        volcano_fig_path = os.path.join(volcano_save_dir, fn + ".png")
        df = MAthresholding(x=path, logFC=logFC, p_val=p_val, verbose=verbose, title=fn, plot_volcano=True, hover_data=colnames, save_path=volcano_fig_path)
        feature_col = [col for col in colnames if col in df.columns][0]
        extracted_ids = df[feature_col].values.tolist()
        lst.extend(extracted_ids)
        if plot_clustermap:
            df_eset = pd.read_csv(eset_path, sep="\t")
            col_colors = np.where(df["logFC"]>=0, "red", "blue")
            data = df_eset.loc[df.ID, :].fillna(0).T
            data.columns = extracted_ids
            fig = sns.clustermap(data=data, cmap="bwr", figsize=(18,6), col_colors=col_colors)
            clustermap_fig_path = os.path.join(clustermap_save_dir, fn + ".png")
            fig.savefig(clustermap_fig_path)
    before = len(lst)
    num_nan_data = len([e for e in lst if str(e)=="nan"])
    unique_list = list(set(lst))
    after = len(unique_list)
    print(f"Not annotated data : {num_nan_data} ({num_nan_data/before:>6.1%})")
    print(f"Unique data : {before} -> {after} ({after/before:>6.1%})")
    return unique_list
