# Python Directory Guide

This folder now contains English Python entry points for the repository workflow.

## Core English Python Files

- `graph_pipeline_utils.py`
  Shared graph-building and GAT-model utilities.

- `build_label_matrix.py`
  Builds the English 4-class label matrix for all prescriptions.

- `build_full_corpus_graphs.py`
  Builds the full labeled graph corpus.

- `build_sample_prediction_graphs.py`
  Builds sample prediction graphs from an Excel input file.

- `run_gat_prediction.py`
  Runs the stored GAT model on sample or user-provided prediction graphs.

- `train_validate_gat.py`
  Trains a new model or evaluates the stored model on the full corpus.

## Legacy Notebooks

- `1_Graph Embedding in UHF.ipynb`
- `2_Prediction Using the GAT Model.ipynb`
- `3_Quantitative of Compatibility Mechanisms Using the GAT Model.ipynb`
- `Legacy_Training_Multilayer_GAT.ipynb`
- `Legacy_Hyperparameter_Search_Multilayer_GAT.ipynb`

These notebooks are kept for historical traceability. The repository-level code path is now defined by the English `.py` files above.
