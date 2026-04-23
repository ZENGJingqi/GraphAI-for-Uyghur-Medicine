# Workflow Logic

This document clarifies the repository logic in plain terms.

## 1. Full-corpus graph data

The project already has a stored graph tensor for all available prescription samples:

- `Data/all_graphs_to_be_predicted.pt`

Despite the filename, this file is the full sample corpus, not a small prediction-only tensor.

To make that explicit in English, the repository also includes:

- `Data/full_prescription_graphs_with_labels.pt`

These two files represent the same full-corpus role.

## 2. Label source

The model predicts 4 classes:

- `Class_1`
- `Class_2`
- `Class_3`
- `Class_4`

The original label source is:

- `Data/UHF_Cluster_Dummies_Unique.csv`

The English normalized label file is:

- `Data/UHF_Label_Matrix.csv`

Important detail:

- The legacy cluster file has 474 labeled prescriptions.
- 6 prescriptions have no `UHF_TCMT.tsv` rows.
- Those 6 prescriptions are assigned zero labels in the normalized matrix.
- That zero-filled behavior matches the labels already stored in the legacy full-corpus `.pt` file.

## 3. Training and validation logic

The training side does not use a separate stored training-only `.pt` file.

Instead:

1. Start from the full-corpus graph tensor
2. Split it into train and validation subsets
3. Train or evaluate the GAT model

English entry point:

- `Python/train_validate_gat.py`

## 4. Sample prediction logic

The repository also contains a small simulation path:

1. Input several prescriptions in Excel format
2. Convert them into graphs
3. Run the stored model
4. Export probabilities and attention weights

Files:

- `Data/sample_prescription_input.xlsx`
- `Data/sample_prediction_graphs.pt`
- `Data/sample_prediction_outputs.tsv`
- `Data/sample_attention_weights.tsv`

English entry points:

- `Python/build_sample_prediction_graphs.py`
- `Python/run_gat_prediction.py`

## 5. Legacy notebooks

The repository still keeps the historical notebooks for traceability, but the repository-level code path is now expressed through English `.py` files.
