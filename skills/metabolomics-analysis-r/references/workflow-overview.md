# Workflow Overview

## Track A: Untargeted LC/GC-MS
1. Raw data import (mzML/mzXML/CDF)
2. Peak detection and grouping (xcms)
3. RT correction and feature matrix
4. Annotation (CAMERA)
5. QC and normalization
6. Stats: PCA, PLS-DA/OPLS-DA, univariate tests
7. Pathway enrichment (MetaboAnalystR)

## Track B: Targeted Quant
1. Standards and calibration curve design
2. Sample quantification
3. QC: pooled QC, blanks, drift checks
4. Normalization and stats

## Track C: Hybrid
- Use untargeted discovery to select candidate features.
- Validate with targeted quant and calibration.

## Key decision points
- Data type: raw spectra vs quantified table
- Platform: LC-MS/GC-MS/NMR
- QC availability: pooled QC and blanks
- Targeted vs untargeted vs hybrid


## Optional: Multi-omics integration

- Combine metabolomics with transcriptomics/proteomics via pathway-level integration.
- Use Fisher or similar p-value combination to score pathways across omics layers.
