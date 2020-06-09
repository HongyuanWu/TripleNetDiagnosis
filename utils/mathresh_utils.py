# coding: utf-8
import os
import re
import numpy as np
import pandas as pd

# set the `plotly.io.orca.config.executable` property to the full path of your orca executable.
# If you use `environment.yml` to create anaconda environment, this command automatically correct the path.
import plotly
conda_env_name = "triple-net-diagnosis"
result = re.findall(pattern=fr"\/.*\/versions\/{conda_env_name}\/", string=plotly.__path__[0])
if len(result)>0:
    plotly.io.orca.config.executable = os.path.join(result[0], "bin/orca")

import plotly.express as px

def volcanoplot(df, logFC=1.2, p_val=0.05, hover_data=[], title="", save_path=None):
    color_discrete_map={"up": "red", "down": "blue", "normal": "lightgray"}
    hover_data = [col for col in hover_data if col in df.columns]

    df.loc[:, "-log10(P.Value)"] = -np.log10(df["P.Value"].values)
    df.loc[:, "p_significance"]  = df["P.Value"] < p_val
    df.loc[:, "Significant"] = "normal"
    df.loc[df["p_significance"] & (df["logFC"] >  logFC), "Significant"] = "up"
    df.loc[df["p_significance"] & (df["logFC"] < -logFC), "Significant"] = "down"

    df = df.fillna("-")
    fig = px.scatter(df, x="logFC", y="-log10(P.Value)", color="Significant", color_discrete_map=color_discrete_map, hover_data=hover_data)
    fig.update_layout(title=title, font=dict(family="Monaco", size=18, color="#7f7f7f"))

    y_min = df["-log10(P.Value)"].min()
    y_max = df["-log10(P.Value)"].max()
    x_min = df["logFC"].min()
    x_max = df["logFC"].max()
    fig.add_shape(type="line", x0=-logFC, x1=-logFC, y0=y_min, y1=y_max, line=dict(color="black", width=2, dash="dot"))
    fig.add_shape(type="line", x0=logFC,  x1=logFC,  y0=y_min, y1=y_max, line=dict(color="black", width=2, dash="dot"))
    fig.add_shape(type="line", x0=x_min,  x1=x_max,  y0=-np.log10(p_val), y1=-np.log10(p_val), line=dict(color="black", width=2, dash="dot"))
    if save_path is not None:
        fig.write_image(save_path)
        print(f"volcano plot was saved at `{save_path}`")
    fig.show()

def MAthresholding(x, logFC=1.2, p_val=0.05, verbose=True, title="", plot_volcano=False, **volcanokwargs):
    """
    @params x            : input data. (str) path or (pd.DataFrame)
    @params logFC        : (float) threshold value.
    @params p_val        : (float) threshold value.
    @params verbose      : (bool)  Whether print information or not.
    @params plot_volcano : (bool)  Whethre plot volcanoplot or not.
    @params volcanokwargs
        - hover_data : (list) colnames for hover labels.
        - title      : (str)  title for figure.
        - save_path  : (str)  A string representing a local file path.
    """
    # Load original DataFrame.
    df = x if isinstance(x, pd.DataFrame) else pd.read_csv(str(x), sep="\t")
    before = len(df)
    # Drop NaN data.
    df = df.dropna(axis=0, how="any", subset=["logFC", "P.Value"])
    middle = len(df)
    if plot_volcano:
        volcanoplot(df=df, logFC=logFC, p_val=p_val, title=title, **volcanokwargs)
    # Thresholding
    df = df[(abs(df["logFC"])>logFC) & (df["P.Value"]<p_val)]
    after  = len(df)

    if verbose:
        print(f"{title} : {before} --[drop NaN]-> {middle} --[threshold]-> {after} ({after/before:>6.1%})")
    return df

def applyMAthresh2all(gen, colnames=[], logFC=1.2, p_val=0.05, verbose=True, plot_volcano=False, volcano_save_dir="."):
    """Apply `MAthresholding` to all data.
    @params colnames     :
    @params logFC        : (float) threshold value.
    @params p_val        : (float) threshold value.
    @params verbose      :
    @params plot_volcano : (bool) Whether plot or not.
    @return unique_list  :
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
        fn = str(path).split("/")[-1]
        volcano_fig_path = os.path.join(volcano_save_dir, fn + ".png")
        df = MAthresholding(x=path, logFC=logFC, p_val=p_val, verbose=verbose, title=fn, plot_volcano=True, hover_data=colnames, save_path=volcano_fig_path)
        feature_col = [col for col in colnames if col in df.columns][0]
        lst.extend(df[feature_col].values.tolist())
    before = len(lst)
    unique_list = list(set(lst))
    after = len(unique_list)
    print(f"unique data : {before} -> {after} ({after/before:>6.1%})")
    return unique_list
