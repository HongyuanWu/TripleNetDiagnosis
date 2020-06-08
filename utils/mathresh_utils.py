# coding: utf-8
import pandas as pd

def MAthresholding(x, logFC=1.2, p_val=0.05, verbose=True):
    """
    @params x     : input data. (str) path or (pd.DataFrame)
    @params logFC : (float) threshold value.
    @params p_val : (float) threshold value.
    """
    if isinstance(x, pd.DataFrame):
        df = x
    else:
        df = pd.read_csv(str(x), sep="\t")

    before = len(df)
    df = df.dropna(axis=0, how="any", subset=["logFC", "P.Value"])
    middle = len(df)
    df = df[(abs(df["logFC"])>logFC) & (df["P.Value"]<p_val)]
    after  = len(df)

    if verbose: print(f"{before} --[drop NaN]-> {middle} --[threshold]-> {after} ({after/before:>6.1%})")
    return df

def applyMAthresh2all(gen, colnames=[], logFC=1.2, p_val=0.05, verbose=True):
    """Apply `MAthresholding` to all data.
    @params
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
        if verbose:
            print(str(path).split("/")[-1], end=" : ")
        df = MAthresholding(x=path, logFC=logFC, p_val=p_val, verbose=verbose)
        for col in colnames:
            if col in df.columns:
                data = df[col].values.tolist()
                lst.extend(data)
                break
    before = len(lst)
    unique_list = list(set(lst))
    after = len(unique_list)
    print(f"unique data : {before} -> {after} ({after/before:>6.1%})")
    return unique_list
