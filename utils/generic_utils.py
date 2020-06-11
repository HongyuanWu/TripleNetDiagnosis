#coding: utf-8
import pandas as pd
from kerasy.utils import toBLUE

def removeNaN(lst):
    return [e for e in lst if str(e) != "nan"]

def add_linefeed(lst, linefeed="\n"):
    return list(map(lambda x:str(x)+linefeed, lst))

def saveNameList(lst, path, remove_nan=True, sort=True, add_num=True, verbose=True):
    if remove_nan:
        if verbose: print("remove NaN.")
        lst = removeNaN(lst)
    if sort:
        if verbose: print("Sorted.")
        lst = sorted(lst)
    lst = add_linefeed(lst, linefeed="\n")
    if add_num:
        num_data = len(lst)
        *fn, ext = path.split(".")
        path = ".".join(fn) + f".{num_data}data." + ext
    with open(path, mode="w") as f:
        f.writelines(lst)
    if verbose: print(f"Save NameList to {toBLUE(path)}")

def collectGeneSymbols(gen, colnames=[], drop_duplicate=True, remove_nan=True):
    symbols = []
    for path in gen:
        df = pd.read_csv(path, sep="\t")
        colname = [col for col in colnames if col in df.columns][0]
        symbol  = df[colname].values.tolist()
        symbols.extend(symbol)
    if drop_duplicate:
        symbols = list(set(symbols))
    if remove_nan:
        symbols = removeNaN(symbols)
    return symbols
