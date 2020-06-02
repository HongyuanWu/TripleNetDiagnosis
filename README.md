# Triple (circRNA-miRNA-mRNA) Network Diagnosis

This is a replication of the paper ["A novel circRNA-miRNA-mRNA network identifies circ-YOD1 as a biomarker for coronary artery disease"](https://doi.org/10.1038/s41598-019-54603-2). The flowchart is shown in following:

![Figure.1 A flowchart of ceRNA network construction.](image/Figure.1.png)

## Materials

Seven CAD-related microarray datasets were downloaded from the Gene Expression Omnibus (GEO) database (https://www.ncbi.nlm.nih.gov/geo/). The details for each microarray are shown in Supplementary [Table 3](https://static-content.springer.com/esm/art%3A10.1038%2Fs41598-019-54603-2/MediaObjects/41598_2019_54603_MOESM2_ESM.pdf).

|Type|GEO accession|Supplementary file|extension|
|:-:|:-:|:-|:-|
|mRNAs| [GSE34918](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE34918)|[GSE34918_RAW.tar](https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE34918&format=file)|`.txt`|
|mRNAs| [GSE62646](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE62646)|[GSE62646_RAW.tar](https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE62646&format=file)|`.CEL`|
|mRNAs| [GSE60993](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE60993)|[GSE60993_RAW.tar](https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE60993&format=file)|`.bgx`|
|mRNAs| [GSE61144](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE61144)|[GSE61144_non_normalized.txt.gz](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE61nnn/GSE61144/suppl/GSE61144_non_normalized.txt.gz)|`.txt`|
|miRNAs|[GSE24548](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE24548)|[GSE24548_RAW.tar](https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE24548&format=file)|`.txt`|
|miRNAs|[GSE53211](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE53211)|[GSE53211_non-normalized_data.txt.gz](https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE53211&format=file&file=GSE53211%5Fnon%2Dnormalized%5Fdata%2Etxt%2Egz)|`.txt`|
|miRNAs|[GSE53675](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE53675)|[GSE53675_RAW.tar](https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE53675&format=file)|`.gpr`|
