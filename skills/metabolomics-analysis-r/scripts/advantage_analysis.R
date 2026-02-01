# Advantage analysis: quantify recovery/perturbation vs control and normal

suppressPackageStartupMessages({
  library(dplyr)
  library(tidyr)
  library(ggplot2)
})

calc_advantage_metrics <- function(output_dir) {
  # ---- helpers ----
  read_matrix <- function(path) {
    df <- read.csv(path, check.names = FALSE)
    rownames(df) <- df$feature
    df$feature <- NULL
    as.matrix(df)
  }

  read_meta <- function(path) {
    read.csv(path, stringsAsFactors = FALSE)
  }

  make_metadata <- function(meta_df) {
    meta_df <- meta_df |>
      mutate(sample_name = as.character(sample_name)) |>
      filter(!is.na(sample_name)) |>
      mutate(
        group = case_when(
          str_detect(sample_name, "^生理盐水") ~ "PN+saline",
          str_detect(sample_name, "^维生素") ~ "PN+Vit A/C/E (high dose)",
          str_detect(sample_name, "^低剂量") ~ "PN+fat-sol Vit 3.05 ml/kg + water-sol Vit 5 ml/kg (low dose)",
          str_detect(sample_name, "^高剂量") ~ "PN+fat-sol Vit 6.1 ml/kg + water-sol Vit 10 ml/kg (high dose)",
          str_detect(sample_name, "^正常组") ~ "Normal",
          str_detect(sample_name, "模型组术后10-12h") ~ "Model post-op 10-12h",
          TRUE ~ NA_character_
        ),
        timepoint = case_when(
          str_detect(sample_name, "3d") ~ "3d",
          str_detect(sample_name, "5d") ~ "5d",
          str_detect(sample_name, "16d") ~ "16d",
          str_detect(sample_name, "术后10-12h") ~ "post-op 10-12h",
          str_detect(sample_name, "术前") ~ "pre-op",
          str_detect(sample_name, "^正常组") ~ "baseline",
          TRUE ~ NA_character_
        )
      )
    meta_df
  }

  align_meta_matrix <- function(meta, mat) {
    meta <- make_metadata(meta)
    meta <- meta |>
      mutate(sample_id = gsub("^[AX]", "", experiment_id)) |>
      filter(sample_id %in% colnames(mat))
    mat <- mat[, meta$sample_id, drop = FALSE]
    list(meta = meta, mat = mat)
  }

  # ---- 1) Global perturbation index from univariate log2fc ----
  calc_perturbation_from_univariate <- function(path, prefix) {
    df <- read.csv(path)
    df <- df |> filter(log2fc_status == "ok")
    agg <- df |>
      group_by(group, timepoint) |>
      summarise(
        median_abs_log2fc = median(abs(log2fc), na.rm = TRUE),
        mean_abs_log2fc = mean(abs(log2fc), na.rm = TRUE),
        n_features = n(),
        .groups = "drop"
      )
    write.csv(agg, file.path(output_dir, paste0(prefix, "_perturbation_index.csv")), row.names = FALSE)
  }

  calc_perturbation_from_univariate(file.path(output_dir, "nmr_univariate.csv"), "nmr")
  calc_perturbation_from_univariate(file.path(output_dir, "gc_univariate.csv"), "gc")

  # ---- 2) Distance to Normal centroid in PCA space ----
  calc_distance_to_normal <- function(matrix_path, meta_path, prefix) {
    mat <- read_matrix(matrix_path)
    meta <- read_meta(meta_path)
    aligned <- align_meta_matrix(meta, mat)
    meta <- aligned$meta
    mat <- aligned$mat

    m <- t(scale(t(mat)))
    pca <- prcomp(t(m), scale. = FALSE)
    scores <- as.data.frame(pca$x[, 1:2])
    scores$sample_id <- rownames(scores)
    scores <- scores |>
      left_join(meta |> mutate(sample_id = gsub("^[AX]", "", experiment_id)),
                by = "sample_id")

    normal <- scores |> filter(group == "Normal")
    if (nrow(normal) == 0) {
      warning("No Normal group for ", prefix, "; skipping distance.")
      return(invisible(NULL))
    }
    centroid <- colMeans(normal[, c("PC1", "PC2")], na.rm = TRUE)

    scores$dist_to_normal <- sqrt((scores$PC1 - centroid[1])^2 + (scores$PC2 - centroid[2])^2)

    dist_sum <- scores |>
      group_by(group, timepoint) |>
      summarise(
        mean_dist_to_normal = mean(dist_to_normal, na.rm = TRUE),
        median_dist_to_normal = median(dist_to_normal, na.rm = TRUE),
        n = n(),
        .groups = "drop"
      )

    write.csv(dist_sum, file.path(output_dir, paste0(prefix, "_distance_to_normal.csv")), row.names = FALSE)
  }

  calc_distance_to_normal(file.path(output_dir, "nmr_matrix_pqn.csv"),
                          file.path(output_dir, "metadata_nmr.csv"),
                          "nmr")
  calc_distance_to_normal(file.path(output_dir, "gc_matrix_pqn.csv"),
                          file.path(output_dir, "metadata_gc.csv"),
                          "gc")

  # ---- 3) Part2 recovery score (clinical biomarkers) ----
  calc_part2_recovery <- function() {
    part2 <- read.csv(file.path(output_dir, "part2_calculated.csv"), stringsAsFactors = FALSE)
    direction <- data.frame(
      analyte = c("SOD_serum","SOD_liver","MDA_serum","8-isoprostane_urine",
                  "IL6_serum","TNF_serum","CRP_serum"),
      sign = c(1,1,-1,-1,-1,-1,-1)
    )
    part2 <- part2 |> left_join(direction, by = "analyte") |> filter(!is.na(sign))

    part2 <- part2 |>
      group_by(analyte, timepoint) |>
      mutate(
        ref_mean = mean(value[group == "PN+saline"], na.rm = TRUE),
        ref_sd = sd(value[group == "PN+saline"], na.rm = TRUE),
        z = (value - ref_mean) / ref_sd
      ) |>
      ungroup()

    part2$z[!is.finite(part2$z)] <- 0
    part2$recovery_score = part2$z * part2$sign

    score_sum <- part2 |>
      group_by(group, timepoint) |>
      summarise(
        mean_recovery_score = mean(recovery_score, na.rm = TRUE),
        median_recovery_score = median(recovery_score, na.rm = TRUE),
        n = n(),
        .groups = "drop"
      )

    write.csv(score_sum, file.path(output_dir, "part2_recovery_score.csv"), row.names = FALSE)
  }

  calc_part2_recovery()

  # ---- Summary outputs ----
  combine_advantage_summary <- function() {
    nmr_pert <- read.csv(file.path(output_dir, "nmr_perturbation_index.csv"))
    gc_pert <- read.csv(file.path(output_dir, "gc_perturbation_index.csv"))
    nmr_dist <- read.csv(file.path(output_dir, "nmr_distance_to_normal.csv"))
    gc_dist <- read.csv(file.path(output_dir, "gc_distance_to_normal.csv"))
    part2 <- read.csv(file.path(output_dir, "part2_recovery_score.csv"))

    nmr_pert$data_type <- "nmr"
    gc_pert$data_type <- "gc"
    nmr_dist$data_type <- "nmr"
    gc_dist$data_type <- "gc"

    write.csv(bind_rows(nmr_pert, gc_pert),
              file.path(output_dir, "metabolomics_perturbation_summary.csv"),
              row.names = FALSE)
    write.csv(bind_rows(nmr_dist, gc_dist),
              file.path(output_dir, "metabolomics_distance_summary.csv"),
              row.names = FALSE)
    write.csv(part2, file.path(output_dir, "part2_recovery_score.csv"), row.names = FALSE)
  }

  combine_advantage_summary()
}

# Usage:
# calc_advantage_metrics("D:/曹祥龙/动物-维生素-代谢组学/analysis/output")
