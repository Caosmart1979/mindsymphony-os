# Preprocessing (xcms/CAMERA)

## xcms core steps
- Peak detection: CentWaveParam (ppm, peakwidth, snthresh)
- RT correction: ObiwarpParam
- Grouping: PeakDensityParam (bw, minFraction)
- Feature matrix: featureValues()

## CAMERA annotation
- Group peaks by co-elution and adduct patterns.
- Use annotation to reduce redundancy before pathway mapping.
