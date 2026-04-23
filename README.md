# GraphAI for Uyghur Medicine

Author: Zeng Jingqi  
Contact: zjingqi@163.com  
Project update: April 2026

GraphAI for Uyghur Medicine is a graph-based workflow for modeling and interpreting compatibility mechanisms in Uyghur medicine prescriptions.

This repository keeps the current project assets for graph construction, pretrained inference, mechanism interpretation, and reproducible model training. Its organization follows the same general design used in `GraphAI-for-TCM`, while remaining separate from a finalized paper release.

![Project Overview](Figure/Graphic_abstract.png)

## Overview

The repository contains two different kinds of graph data:

1. `Data/full_prescription_graphs_with_labels.pt`  
   This is the full labeled graph corpus for all available samples. It is the dataset used for training and validation splitting.

2. `Data/prediction_graphs_from_input.pt`  
   This is a small example inference graph tensor generated from `Data/Test_input.xlsx`. It is only used to demonstrate the prediction workflow.

The repository also keeps:

- `Data/gat_model.pth`: pretrained GAT model weights
- the original source tables in `Data/`
- the notebook workflow in `Python/`
- the project overview image in `Figure/`

Generated prediction tables and temporary evaluation outputs are not stored in the repository.

## Repository Structure

```text
GraphAI-for-Uyghur-Medicine/
+-- Data/
|   +-- full_prescription_graphs_with_labels.pt
|   +-- gat_model.pth
|   +-- Test_input.xlsx
|   +-- prediction_graphs_from_input.pt
|   +-- UHF_Cluster_Dummies_Unique.csv
|   +-- UHF_Label_Matrix.csv
|   `-- source tables
+-- Figure/
+-- Python/
|   +-- 1_Graph Embedding in Uyghur Formulae.ipynb
|   +-- 2_Prediction Using the GAT Model.ipynb
|   +-- 3_Quantitative Evaluation of Compatibility Mechanisms Using the GAT Model.ipynb
|   +-- Graph Attention Network.ipynb
|   +-- Hyperparameter Search for GAT.ipynb
|   `-- README.md
`-- requirements.txt
```

## Quick Start

Create an environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

Launch Jupyter from the repository root:

```powershell
jupyter notebook
```

## Recommended Notebook Order

For most users, the public workflow is:

1. `Python/1_Graph Embedding in Uyghur Formulae.ipynb`
2. `Python/2_Prediction Using the GAT Model.ipynb`
3. `Python/3_Quantitative Evaluation of Compatibility Mechanisms Using the GAT Model.ipynb`

The training notebook is:

- `Python/Graph Attention Network.ipynb`

The hyperparameter notebook is:

- `Python/Hyperparameter Search for GAT.ipynb`

## Notes

- `full_prescription_graphs_with_labels.pt` is the full training corpus, not a temporary prediction file.
- `prediction_graphs_from_input.pt` is only a small bundled inference example.
- The repository currently explains the project and its workflow; it is not a paper-results archive.

## Folder Guides

- [Data/README.md](./Data/README.md)
- [Python/README.md](./Python/README.md)
