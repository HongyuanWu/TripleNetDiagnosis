# Author iwasakishuto
# Date 2020-06-07

# Install `probelms`, `spec`, ...
library(readr)

print_save_log <- function(path){
  print(paste("Save at ", path, "", sep="'"))
}

print_var_length <- function(var, varname=deparse(substitute(var))) {
  print(paste("The number of", varname, ":", length(var), sep=" "))
}

fraction2float <- function(df, colname){
  floats <- c()
  fractions <- df[, colname]
  for (i in 1:nrow(df)){
    floats[i] <- eval(parse(text=fractions[i]))
  }
  df[, colname] <- floats
  return (df)
}