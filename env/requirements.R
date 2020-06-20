# Version info: R 3.6.3, BiocVersion 3.1
# Author iwasakishuto
# Date 2020-06-20

packages <- c(
)

if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")

for(pkg in packages) if (!require(pkg, character.only = T)){
  BiocManager::install(pkg, update = F)
  require(pkg, character.only = T)
}