# Version info: R 4.0.1 (2020-06-06)
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

qlibrary <- function(package){
  # make your `library` function very quiet.
  suppressMessages(suppressWarnings(
    library(
      as.character(substitute(package)), 
      character.only = TRUE
    )
  ))
}

qrequire <- function(package){
  # make your `require` function very quiet.
  suppressMessages(suppressWarnings(
    require(
      as.character(substitute(package)),
      character.only = TRUE
    )
  ))
}
