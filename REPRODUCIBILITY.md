# Reproducibility Guide

This file summarizes the minimum set of files and steps required to reproduce the current repository version.

## Core Stored Artifacts

### Full-corpus side

- `Data/all_graphs_to_be_predicted.pt`
  Legacy stored full-corpus graph tensor.

- `Data/full_prescription_graphs_with_labels.pt`
  English-named full-corpus graph tensor aligned with the legacy stored file.

- `Data/gat_model.pth`
  Previously trained GAT model weights.

### Label side

- `Data/UHF_Cluster_Dummies_Unique.csv`
  Original legacy cluster dummy file.

- `Data/UHF_Label_Matrix.csv`
  English label matrix for all 480 prescriptions.

### Sample prediction side

- `Data/sample_prescription_input.xlsx`
- `Data/sample_prediction_graphs.pt`
- `Data/sample_prediction_outputs.tsv`
- `Data/sample_attention_weights.tsv`

## Reproduction Paths

### 1. Full-corpus reconstruction

```powershell
python Python/build_label_matrix.py
python Python/build_full_corpus_graphs.py
```

### 2. Stored-model evaluation

```powershell
python Python/train_validate_gat.py --mode evaluate-existing
```

### 3. Sample prediction simulation

```powershell
python Python/build_sample_prediction_graphs.py
python Python/run_gat_prediction.py
```

## Important Clarification

- The earlier file `all_graphs_to_be_predicted.pt` is the full stored graph corpus.
- Training and validation are created later by splitting this full corpus.
- The sample prediction path is only a small simulation path for demonstrating the Excel -> graph -> prediction flow.
