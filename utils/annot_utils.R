# Author iwasakishuto
# Date 2020-06-07

library(mogene20sttranscriptcluster.db)

addAnnot <- function(eset){
  my_frame <- data.frame(exprs(eset))
  Annot <- data.frame(
      ACCNUM=sapply(contents(mogene20sttranscriptclusterACCNUM),   paste, collapse=", "),
      SYMBOL=sapply(contents(mogene20sttranscriptclusterSYMBOL),   paste, collapse=", "),
      DESC  =sapply(contents(mogene20sttranscriptclusterGENENAME), paste, collapse=", "),
  )
  all <- merge(Annot, my_frame, by.x=0, by.y=0, all=T)
  return all
}
