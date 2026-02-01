# Untargeted LC/GC-MS preprocessing template

if (!requireNamespace('BiocManager', quietly = TRUE)) install.packages('BiocManager')
BiocManager::install(c('xcms', 'CAMERA'))
install.packages(c('ropls', 'ggplot2', 'pheatmap'))

library(xcms)
library(CAMERA)
library(ropls)
library(ggplot2)
library(pheatmap)

# TODO: set working directory and input files
setwd('path/to/data')
raw_files <- list.files(pattern = '.mzML|.mzXML|.CDF', recursive = TRUE)

# TODO: build sample metadata
sample_info <- data.frame(
  sample_name = sub('\..*', '', basename(raw_files)),
  sample_group = NA,
  injection_order = seq_along(raw_files)
)

# Peak detection
cwp <- CentWaveParam(ppm = 30, peakwidth = c(5, 60), snthresh = 10, prefilter = c(3, 1000))
xdata <- findChromPeaks(readMSData(raw_files, mode = 'onDisk'), param = cwp)

# RT correction and grouping
xdata_adj <- adjustRtime(xdata, param = ObiwarpParam())
xdata_grp <- groupChromPeaks(xdata_adj, param = PeakDensityParam(sampleGroups = sample_info$sample_group, bw = 30, minFraction = 0.5))

# Feature matrix
feature_matrix <- featureValues(xdata_grp, value = 'into')

# TODO: missing value imputation and normalization
