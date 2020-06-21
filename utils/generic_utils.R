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
