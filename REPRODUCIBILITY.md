# Reproducibility Guide

This file summarizes the minimum required steps for reproducing the stored project workflow.

## Core Stored Artifacts

- `Data/full_prescription_graphs_with_labels.pt`
  Stored full-corpus graph tensor.

- `Data/gat_model.pth`
  Stored GAT model weights.

- `Data/UHF_Cluster_Dummies_Unique.csv`
  Original cluster dummy file.

- `Data/UHF_Label_Matrix.csv`
  English normalized label matrix.

## Reproduction Paths

### 1. Rebuild the English label matrix

```powershell
python Python/build_label_matrix.py
```

### 2. Rebuild the full graph corpus for verification

```powershell
python Python/build_full_corpus_graphs.py
```

### 3. Evaluate the stored model on the stored full corpus

```powershell
python Python/train_validate_gat.py --mode evaluate-existing
```

### 4. Simulate prediction from an Excel input

```powershell
python Python/build_sample_prediction_graphs.py --input-excel Data/Test_input.xlsx
python Python/run_gat_prediction.py --graph-pt Data/prediction_graphs_from_input.pt
```

## Important Clarification

- `full_prescription_graphs_with_labels.pt` is the stored full-corpus graph tensor.
- Training and validation are created by splitting this full corpus.
- The prediction-from-Excel path is a generated workflow path, not a separate stored corpus.
