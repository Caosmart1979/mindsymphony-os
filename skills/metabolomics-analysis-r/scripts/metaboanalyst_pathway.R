# MetaboAnalystR pathway analysis template

if (!requireNamespace('devtools', quietly = TRUE)) install.packages('devtools')
if (!requireNamespace('MetaboAnalystR', quietly = TRUE)) {
  devtools::install_github('xia-lab/MetaboAnalystR', build = TRUE, build_vignettes = TRUE, build_manual = TRUE)
}

library(MetaboAnalystR)

# TODO: set input file and organism
# mSet <- InitDataObjects('conc', 'pathora', FALSE)
# mSet <- Read.TextData(mSet, 'path/to/peak_table.csv', 'rowu', 'disc')
# mSet <- SanityCheckData(mSet)
# mSet <- SetMetabolomeFilter(mSet, FALSE)
# mSet <- CrossReferencing(mSet, 'kegg')
# mSet <- CreateMappingResultTable(mSet)
# mSet <- SetKEGG.PathLib(mSet, 'hsa')
# mSet <- CalculateOraScore(mSet)
