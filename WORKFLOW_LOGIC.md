# Workflow Logic

This repository now uses a simple logic.

## 1. Full-corpus data

The stored graph tensor is:

- `Data/full_prescription_graphs_with_labels.pt`

This file is the full sample corpus. It is not a small prediction-only tensor.

## 2. Label logic

The original label source is:

- `Data/UHF_Cluster_Dummies_Unique.csv`

The English normalized label file is:

- `Data/UHF_Label_Matrix.csv`

The normalized matrix has 480 prescriptions.

- 474 prescriptions come directly from the legacy cluster dummy file.
- 6 prescriptions have no `UHF_TCMT.tsv` rows and therefore receive zero labels.
- That zero-filled behavior matches the labels stored in the full-corpus `.pt` file.

## 3. Training and validation

Training and validation are created by splitting the full-corpus graph tensor.

English entry point:

- `Python/train_validate_gat.py`

## 4. Prediction simulation

Prediction simulation starts from an Excel input table such as:

- `Data/Test_input.xlsx`

English entry points:

- `Python/build_sample_prediction_graphs.py`
- `Python/run_gat_prediction.py`

These scripts generate prediction artifacts as outputs of the workflow.

## 5. Verification rebuild

If needed, the repository can rebuild a verification full-corpus tensor from source tables and the English label matrix:

- `Python/build_full_corpus_graphs.py`
