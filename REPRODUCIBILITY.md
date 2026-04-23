# Reproducibility Guide

This file summarizes the minimum set of files and steps required to reproduce the current repository version.

## Core Reproducibility Artifacts

The following files are already included in the repository and are intended to support peer reproduction of the current stored workflow:

- `Data/all_graphs_to_be_predicted.pt`
  Serialized graph dataset used by the original notebook workflow

- `Data/gat_model.pth`
  Previously generated trained model artifact kept with this repository version

- `Data/prediction_outputs.tsv`
  Stored prediction output from the completed run

- `Data/attention_weights.tsv`
  Raw attention export from the completed run

- `Data/attention_averages.tsv`
  Layer-wise averaged attention values

- `Data/calculated_attention_weights.tsv`
  Final propagated compatibility scores

## Reproduction Paths

There are two reproduction paths for peers:

1. Artifact-based reproduction
   Use the stored `.pt`, `.pth`, and `.tsv` files directly to inspect the existing model artifact and downstream interpretability outputs.

2. Notebook rerun reproduction
   Re-execute the notebooks in order from `Python/`:
   - `1_Graph Embedding in UHF.ipynb`
   - `2_Prediction Using the GAT Model.ipynb`
   - `3_Quantitative of Compatibility Mechanisms Using the GAT Model.ipynb`

## Expected Folder Assumptions

- Run notebooks from the `Python/` directory
- Keep `Data/` at exactly `../Data`
- Keep `Figure/` at exactly `../Figure` when generating visual outputs

## Scope Note

This reproducibility guide applies to the current repository snapshot only.

- It refers to the original stored workflow
- It does not describe the later paper-upgrade experiments
- It does not claim to package every later draft-stage model variant

