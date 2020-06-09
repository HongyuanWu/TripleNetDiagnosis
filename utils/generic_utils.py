def saveNameList(lst, path, remove_nan=True, add_num=True):
    if remove_nan:
        lst = [str(e)+"\n" for e in lst if str(e) != "nan"]
    else:
        lst = [str(e)+"\n" for e in lst]
    if add_num:
        num_data = len(lst)
        *fn, ext = path.split(".")
        path = ".".join(fn) + f".{num_data}data." + ext
    with open(path, mode="w") as f:
        f.writelines(lst)
