---
name: metabolomics-analysis-r
description: "End-to-end metabolomics analysis in R for untargeted and targeted LC/GC-MS or NMR, covering preprocessing (xcms/CAMERA), QC/normalization, stats (PCA/PLS-DA), differential analysis, pathway enrichment (MetaboAnalystR), and reporting. Use when asked to analyze metabolomics or lipidomics datasets, prepare feature matrices, or design R-based metabolomics workflows."
---

# Metabolomics Analysis in R

## Scope

Support three tracks in R only:
- Untargeted preprocessing and stats (A)
- Targeted quant, QC, and calibration (B)
- Hybrid workflows combining both (C)

## Workflow

1. **Intake**
   - Confirm data type: raw spectra (mzML/mzXML/CDF), peak table, or quantified matrix.
   - Collect sample metadata (group, batch, injection order, QC flags).
   - Identify platform: LC-MS, GC-MS, or NMR.
   - Clarify targeted vs untargeted vs hybrid.

2. **Choose track**
   - Untargeted: `xcms` + `CAMERA` preprocessing, then stats.
   - Targeted: calibration + QC + quant table, then stats.
   - Hybrid: untargeted discovery + targeted validation.

3. **Preprocess (untargeted)**
   - Use `xcms` for peak picking, RT correction, grouping, and feature matrix.
   - Use `CAMERA` for peak annotation/adduct grouping.

4. **QC and normalization**
   - Apply pooled QC checks, RSD filters, blank subtraction.
   - Normalize (PQN/median/sum), log transform, scale (auto/pareto).

5. **Statistics and visualization**
   - PCA for structure and outliers.
   - PLS-DA/OPLS-DA with cross-validation.
   - Univariate tests with FDR and volcano/heatmap.

6. **Pathway and interpretation**
   - Use `MetaboAnalystR` for pathway enrichment.
   - Map IDs and handle unmatched metabolites.
   - For lipidomics, prefer LipidMAPS/SMPDB-style class or network mapping.

7. **Deliverables**
   - Feature matrix, QC report, differential metabolites table.
   - Figures: PCA, volcano, heatmap, pathway plots.

## Case-based improvements (SBS vitamin metabolomics)

Add these checkpoints when working on real-world GC/NMR datasets with mixed labels:

1. **Metadata harmonization**
   - Normalize group/timepoint labels early (English labels recommended).
   - Keep a dedicated mapping table for sample IDs (e.g., A### / X###).

2. **GC annotation path**
   - Use vendor alignment outputs (e.g., `resultlist.csv` with AlignID -> Name).
   - Map AlignID to GC feature IDs before pathway mapping.

3. **Pathway mapping**
   - Maintain `feature_pathway_mapping.csv` with `feature`, `pathway`, IDs.
   - If no pathway hits, fall back to limma-based or top-N enrichment.

4. **Significance hygiene**
   - Record `log2fc_status` to track non-positive means or missing values.
   - Avoid forcing log2fc when values are non-positive.

5. **Clinical advantage tests**
   - Add global perturbation index (median/mean abs log2fc).
   - Add distance-to-normal in PCA space.
   - Add biomarker recovery score from clinical panels (SOD/MDA/IL6/TNF/CRP).

See `references/case-playbook.md` for concise templates and checks.

## Bundled scripts

- `scripts/xcms_untargeted_pipeline.R`: template for raw LC/GC-MS processing.
- `scripts/targeted_qc_calibration.R`: template for targeted QC and calibration.
- `scripts/metaboanalyst_pathway.R`: template for pathway analysis in R.

## References

Read only what is needed:
- `references/workflow-overview.md`: end-to-end pipelines and decision points.
- `references/study-design.md`: sample size guidance, randomization, QA/QC checks.
- `references/qc-qa.md`: QC design, pooled QC, randomization, RSD guidance.
- `references/preprocessing.md`: xcms/CAMERA parameters and feature matrix steps.
- `references/normalization-scaling.md`: normalization, transforms, scaling, missingness.
- `references/statistics.md`: PCA/PLS-DA, univariate tests, visualization.
- `references/pathway.md`: MetaboAnalystR pathway workflow and ID mapping.
- `references/lipidomics.md`: lipidomics-specific pathway limits and databases.
- `references/targeted-quant.md`: calibration and targeted quant steps.
- `references/case-playbook.md`: applied lessons and QC guardrails for mixed GC/NMR.

## Quality checks

- Verify QC stability (RSD thresholds, RT drift, QC clustering).
- Validate supervised models (Q2, permutation, or CV metrics).
- Confirm sample size is adequate for supervised models.
- Record parameter settings for reproducibility.

## Related skills

- Use `metabolomics-workbench-database` for compound lookup or public study metadata.
