# Version info: Bioconductor version 3.11 (BiocManager 1.30.10), R 4.0.1 (2020-06-06)
# Author iwasakishuto
# Date 2020-06-08

source("generic_utils.R")
qlibrary(Biobase)
qlibrary(GEOquery)
qlibrary(limma)

GSE2MArrayLM <- function(GSE=NULL, filename=NULL, GPL=NULL, destdir="~/.GEO",
                         colname="", ctrls=c(), cases=c(), all=TRUE){
  if (FALSE){
    paste("Create a MArrayLM from GSE names.",
          "@reference       : https://www.ncbi.nlm.nih.gov/geo/geo2r",
          "=========================================================",
          "@params GSE      : A character string representing a GSE object for download and parsing.",
          "@params filename : The filename of a previously downloaded GEO SOFT format file or its gzipped representation.",
          "@params GPL      : A character string representing a GPL object.",
          "@params destdir  : The destination directory for any downloads.",
          "@params ctrls    : A character vector which represent belonging to `control` samples.",
          "@params cases    : A character vector which represent belonging to `case` samples.",
          "@params colnames : A character string representing a column name where we can distinguish `cases` and `controls`.",
          "@params all      : A boolean whether you extract all columns or only important ones.")
  }
  if ((length(ctrls)==0 && length(cases)==0) || length(colname)==0){
    print(paste0("Please visit GEO2R (https://www.ncbi.nlm.nih.gov/geo/geo2r) to ",
                 "check how to distinguish 'cases' and 'controls', and define them ",
                 "using `ctrls`, `cases`, `colname` arguments."))
    return (NULL)
  } else {
    ctrls <- unlist(ctrls)
    cases <- unlist(cases)
  }
  if (dir.exists(destdir)==FALSE){
    dir.create(destdir, recursive=TRUE)
  }
  if (is.null(filename)) GSE<-GSE else GSE<-NULL
  # This function is the main user-level function in the GEOquery package.
  # It directs the download (if no filename is specified) and parsing of a GEO
  # SOFT format file into an R data structure specifically designed to make
  # access to each of the important parts of the GEO SOFT format easily accessible.
  gset <- getGEO(GEO=GSE, filename=filename, destdir=destdir, GSEMatrix=TRUE, AnnotGPL=TRUE)
  if (length(gset)>1 && is.null(GPL)==FALSE) idx<-grep(pattern=GPL, x=attr(gset, "names")) else idx<-1
  gset <- gset[[idx]]

  # Make syntactically valid names out of character vectors.
  # (make proper column names to match toptable.)
  fvarLabels(gset) <- make.names(fvarLabels(gset))

  # Extract `colname` columns (=`group_cols`).
  j <- 1
  colname <- tolower(colname)
  for (label in varLabels(gset)) {
      if (any(grep(pattern=colname, x=label))){ break }
      j <- j + 1
  }
  group_cols <- gset[[j]]
  # Extract "control" and "case" samples.
  sml <- c()
  for (i in 1:length(group_cols)) {
    group <- group_cols[i]
    sml[i] <- "X"
    for (ctrl in ctrls){
      if (any(grep(pattern=ctrl, x=group))){
        sml[i] <- "0"
      }
    }
    for (case in cases){
      if (any(grep(pattern=case, x=group))){
        sml[i] <- "1"
      }
    }
  }
  print(paste(sum(sml=="0"), "control samples."))
  print(paste(sum(sml=="1"), "case samples."))
  print(paste(sum(sml=="X"), "other samples."))
  # eliminate samples marked as "X"
  sel  <- which(sml != "X")
  sml  <- sml[sel]
  gset <- gset[ ,sel]

  # log2 transform
  ex <- exprs(gset)
  qx <- as.numeric(quantile(ex, c(0., 0.25, 0.5, 0.75, 0.99, 1.0), na.rm=T))
  LogC <- (qx[5] > 100) ||
          (qx[6]-qx[1] > 50 && qx[2] > 0) ||
          (qx[2] > 0 && qx[2] < 1 && qx[4] > 1 && qx[4] < 2)
  if (LogC) {
    ex[which(ex <= 0)] <- NaN
    exprs(gset) <- log2(ex)
  }

  # set up the data and proceed with analysis
  sml <- paste("G", sml, sep="") # set group names
  fl <- as.factor(sml)
  gset$description <- fl
  design <- model.matrix(~ description + 0, gset)
  colnames(design) <- levels(fl)
  fit <- lmFit(gset, design)
  cont.matrix <- makeContrasts(G1-G0, levels=design)
  fit2 <- contrasts.fit(fit, cont.matrix)
  fit2 <- eBayes(fit2, 0.01)
  tT <- topTable(fit2, adjust="fdr", sort.by="B", number=nrow(fit2))
  if (all==FALSE){
    important_cols <- c("ID","adj.P.Val","P.Value","t","B","logFC","Gene.symbol","Gene.title")
    extract_cols   <- character()
    for (col in important_cols){
      if (col %in% colnames(gset)){
        extract_cols <- c(extract_cols, col)
      }
    }
    tT <- subset(tT, select=extract_cols)
    print("Extract only the following columns.")
    print(paste(extract_cols, collapse=", "))
  }
  return (list(tT, ex))
}
