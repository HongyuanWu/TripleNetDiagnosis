# Version info: R 3.2.3, clusterProfiler3.0.4
# Author iwasakishuto
# Date 2020-06-12

source("generic_utils.R")
library(clusterProfiler)
library(DOSE)
library(GOplot)
library(BiocManager)

enrichGOdotplot <- function(gene, OrgDb, keyType="ENTREZID", pvalueCutoff=0.05,
                           pAdjustMethod="BH", universe, qvalueCutoff=0.2,
                           minGSSize=10, maxGSSize=500, readable=FALSE,
                           width=14, height=8, title="", filename=NULL){
  if (FALSE){
    paste("Create a enrichGO dotplot.",
          "@reference       : https://www.rdocumentation.org/packages/clusterProfiler/versions/3.0.4/topics/enrichGO",
          "=========================================================",
          "@params gene          : a vector of entrez gene id.",
          "@params OrgDb         : OrgDb",
          "@params keyType       : keytype of input gene",
          "@params pvalueCutoff  : Cutoff value of pvalue.",
          "@params pAdjustMethod : one of 'holm', 'hochberg', 'hommel', 'bonferroni', 'BH', 'BY', 'fdr', 'none'",
          "@params universe      : background genes",
          "@params qvalueCutoff  : qvalue cutoff",
          "@params minGSSize     : minimal size of genes annotated by Ontology term for testing.",
          "@params maxGSSize     : maximal size of genes annotated for testing",
          "@params readable      : whether mapping gene ID to gene Name")
  }
  options(repr.plot.width=width, repr.plot.height=height)
  df.all <- data.frame()
  subontologies <- c("MF", "BP", "CC")
  for (ont in subontologies){
    ego <- enrichGO(gene=gene, OrgDb=OrgDb, keyType=keyType, ont=ont,
                    pvalueCutoff=pvalueCutoff, pAdjustMethod=pAdjustMethod,
                    universe=universe, qvalueCutoff=qvalueCutoff,
                    minGSSize=minGSSize, maxGSSize=maxGSSize,
                    readable=readable, pool=pool)
    df.ego <- as.data.frame(ego)
    if (nrow(df.ego)>0){
      df.ego$SampleGroup <- ont
      df.all <- rbind(df.all, df.ego)
    }
  }
  df.all.nrow <- nrow(df.all)
  if (df.all.nrow>0){
    GeneRatio_float <- c()
    GeneRatio_str <- df.all$GeneRatio
    for (i in 1:df.all.nrow){
      GeneRatio_float[i] <- eval(parse(text=GeneRatio_str[i]))
    }
    df.all$GeneRatio <- GeneRatio_float
    df.all$negLog10_Qvalue <- -log10(df.all$qvalue)
    df.all$label <- paste(df.all$ID, df.all$Description)
    df.all$label <- factor(df.all$label, levels=df.all$label[order(df.all$SampleGroup, df.all$GeneRatio)])
    fig <- ggplot() +
    geom_point(data=df.all, mapping=aes(x=GeneRatio, y=label, shape=SampleGroup, color=negLog10_Qvalue, size=Count)) +
    ggtitle(label=title, subtitle=waiver()) +
    scale_colour_gradient(low="blue", high="red")
    if (is.null(NULL)==FALSE){
      ggsave(filename, width=width, height=height)
    }
    return (fig)
  }else{
    print("enrichGO returns nothing.")
  }
}

myggsave <- function(filename){
  ggsave(filename, width=14, height=8)
}

# geneSYMBOL2KEGGID <- function(gene_symbols){
#   library(RCurl)
#   options(RCurlOptions = list(cainfo = system.file("CurlSSL", "cacert.pem", package = "RCurl")))
#   if (FALSE){
#     paste("reference: https://gist.github.com/vsoch/11149451")
#   }
#   hsa = c()
#   for (i in 1:length(gene_symbols)) {
#     query = paste("http://rest.kegg.jp/find/hsa/", gene_symbols[i], sep="")
#     result = getURL(query)
#     hsa = c(hsa,strsplit(result,"\t")[[1]][1])
#   }
#   data <- data.frame(gene_symbols, hsa)
#
#   missing = data[-grep("hsa:", hsa),]
#   missing$hsa = rep("<NA>", dim(missing)[1])
#   missing$ko  = rep("<NA>", dim(missing)[1])
#   data = data[grep("hsa:",hsa),]
#
#   # Now look up KO ID
#   ko = c()
#   for (i in 1:length(data$gene_symbols)) {
#     query = paste("http://rest.kegg.jp/link/ko/",as.character(data$hsa[i]),sep="")
#     result = getURL(query)
#     ko = c(ko, as.character(gsub("\n","",strsplit(result,"\t")[[1]][2])))
#   }
#
#   # More squashing
#   ko = as.character(ko)
#   data = cbind(data,ko)
#
#   # Add missing back
#   data <- rbind(data,missing)
#   data <- data[order(data$a),]
#   return (data)
# }

geneSYMBOL2KEGGID <- function(gene_symbols){
  library(org.Hs.eg.db)
  if (FALSE){
    paste("To get get the KEGG IDs associated with a particular gene symbol you ",
          "must first convert the gene symbols from the org.Hs.eg.db package into ",
          "Entrez Gene IDs.There are two reasons for this.",
          "1. we never want to use gene symbols as primary identifiers because they are not unique.",
          "2. the org.Hs.eg.db package is Entrez Gene centric.",
          "So if you have an Entrez Gene ID, then you can get to every other ",
          "piece of information in the org.Hs.eg.db package database.")
  }
  # Get the Entrez gene IDs associated with those symbols
  EG_IDs = mget(gene_symbols, revmap(org.Hs.egSYMBOL),ifnotfound=NA)
  # Then get the KEGG IDs associated with those entrez genes.
  KEGG_IDs = mget(as.character(EG_IDs), org.Hs.egPATH,ifnotfound=NA)
  return (KEGG_IDs)
}
