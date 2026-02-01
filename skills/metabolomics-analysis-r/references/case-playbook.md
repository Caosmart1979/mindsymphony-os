# Case Playbook: Mixed GC/NMR Metabolomics (SBS Vitamin Case)

This playbook captures practical steps that repeatedly prevented failures.

## 1) Data inputs

- NMR feature table with metabolite name + chemical shift.
- GC peak table with AlignID-based features.
- GC alignment metadata:
  - `resultlist.csv` contains AlignID -> Name (and often CAS).
  - Use this to map GC feature IDs to compound names.

## 2) Metadata harmonization

- Normalize sample IDs to the same format (strip A/X prefixes).
- Translate group/timepoint labels into English early.
- Keep a single metadata table per platform.

## 3) Pathway mapping workflow

1. Build `feature_pathway_mapping.csv` with columns:
   - `feature`, `data_type`, `metabolite_name`, `pathway`, `kegg_id`, `hmdb_id`
2. NMR:
   - Parse `metabolite_name` from `feature` (e.g., "Alanine @1.46").
   - KEGG lookup by name (clean special characters first).
3. GC:
   - Join `feature` (AlignID) to `resultlist.csv` Name column.
   - KEGG lookup by name.
4. If no mapped pathways:
   - Use limma or top-N enrichment as exploratory fallback.

## 4) Statistical hygiene

- Keep `log2fc_status` to avoid forced log2 on non-positive values.
- Report both univariate and limma when designs are multi-factor.

## 5) Advantage metrics (clinical interpretation)

Use at least two of:
- **Perturbation index**: median/mean abs log2fc per group/timepoint.
- **Distance to Normal**: PCA distance to normal centroid.
- **Clinical recovery score**: z-score of biomarkers vs control (SOD up, MDA/IL6/TNF/CRP down).

Interpretation rule:
- A single timepoint advantage is **time-dependent**, not global superiority.

## 6) Deliverables

- `*_perturbation_index.csv`
- `*_distance_to_normal.csv`
- `part2_recovery_score.csv`
- `*_pathway_enrichment*.csv`
