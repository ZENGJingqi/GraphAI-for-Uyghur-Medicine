# Python Directory Guide

This folder contains the necessary English Python workflow files.

## Core Python Files

- `graph_pipeline_utils.py`
  Shared graph-building and GAT utilities.

- `build_label_matrix.py`
  Builds the English label matrix for all prescriptions.

- `build_full_corpus_graphs.py`
  Rebuilds the full graph corpus for verification.

- `build_sample_prediction_graphs.py`
  Builds prediction graphs from an Excel input file.

- `run_gat_prediction.py`
  Runs the stored GAT model on prediction graphs.

- `train_validate_gat.py`
  Trains or evaluates the GAT model on the stored full corpus.

## Legacy Notebooks

- `1_Graph Embedding in UHF.ipynb`
- `2_Prediction Using the GAT Model.ipynb`
- `3_Quantitative of Compatibility Mechanisms Using the GAT Model.ipynb`
- `Legacy_Training_Multilayer_GAT.ipynb`
- `Legacy_Hyperparameter_Search_Multilayer_GAT.ipynb`

These notebooks are kept only for traceability.
