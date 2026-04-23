# GraphAI for Uyghur Medicine

This repository documents the current graph-based modeling workflow for Uyghur medicine prescriptions.

It preserves the original project artifacts and also provides an English Python pipeline that makes the training side and the sample-prediction side explicit.

![Project Overview](Figure/Graphic_abstract.png)

## What This Repository Now Says Clearly

There are two different data roles in this project:

1. Full-corpus graph data  
   This is the graph tensor for all available prescription samples.

2. Sample prediction data  
   This is a small simulation path used to show how a user can input several prescriptions, generate graphs, and obtain prediction outputs.

The original file `Data/all_graphs_to_be_predicted.pt` is not a small prediction-only set. It is the full stored graph corpus from the earlier workflow. To make that explicit in English, the repository now also includes:

- `Data/full_prescription_graphs_with_labels.pt`

This English-named file is aligned with the legacy full-corpus `.pt` file.

## Repository Structure

```text
GraphAI-for-Uyghur-Medicine/
+-- Data/
|   +-- all_graphs_to_be_predicted.pt
|   +-- full_prescription_graphs_with_labels.pt
|   +-- UHF_UHP.tsv
|   +-- UHF_TCMT.tsv
|   +-- UHF_Cluster_Dummies_Unique.csv
|   +-- UHF_Label_Matrix.csv
|   +-- UHP_Encoder.tsv
|   +-- UHP_Medicinal_properties_encode.tsv
|   +-- sample_prescription_input.xlsx
|   +-- sample_prediction_graphs.pt
|   +-- sample_prediction_outputs.tsv
|   +-- sample_attention_weights.tsv
|   `-- gat_model.pth
+-- Figure/
+-- Python/
|   +-- build_label_matrix.py
|   +-- build_full_corpus_graphs.py
|   +-- build_sample_prediction_graphs.py
|   +-- run_gat_prediction.py
|   +-- train_validate_gat.py
|   +-- graph_pipeline_utils.py
|   `-- legacy notebooks
+-- WORKFLOW_LOGIC.md
`-- README.md
```

Directory notes:

- [Data/README.md](./Data/README.md)
- [Python/README.md](./Python/README.md)
- [Figure/README.md](./Figure/README.md)
- [PROJECT_SCOPE.md](./PROJECT_SCOPE.md)
- [REPRODUCIBILITY.md](./REPRODUCIBILITY.md)
- [WORKFLOW_LOGIC.md](./WORKFLOW_LOGIC.md)

## English Python Pipeline

### A. Build the English label matrix

```powershell
python Python/build_label_matrix.py
```

This produces:

- `Data/UHF_Label_Matrix.csv`

The label matrix covers all 480 prescriptions. For 6 prescriptions without `UHF_TCMT.tsv` rows, the labels are filled with zeros. That behavior matches the stored labels in the legacy full-corpus `.pt` file.

### B. Build the full graph corpus

```powershell
python Python/build_full_corpus_graphs.py
```

This produces:

- `Data/full_prescription_graphs_with_labels.pt`

The script preserves the original `CPM_ID` order from the legacy full-corpus `.pt` file so the rebuilt English-named file stays aligned with the stored project version.

### C. Train or evaluate the GAT model

```powershell
python Python/train_validate_gat.py --mode evaluate-existing
```

or

```powershell
python Python/train_validate_gat.py --mode train
```

### D. Run a sample prediction simulation

```powershell
python Python/build_sample_prediction_graphs.py
python Python/run_gat_prediction.py
```

This produces:

- `Data/sample_prediction_graphs.pt`
- `Data/sample_prediction_outputs.tsv`
- `Data/sample_attention_weights.tsv`

## Legacy Notebook Material

The repository still keeps the original notebooks for traceability:

- `Python/1_Graph Embedding in UHF.ipynb`
- `Python/2_Prediction Using the GAT Model.ipynb`
- `Python/3_Quantitative of Compatibility Mechanisms Using the GAT Model.ipynb`
- `Python/Legacy_Training_Multilayer_GAT.ipynb`
- `Python/Legacy_Hyperparameter_Search_Multilayer_GAT.ipynb`

These are preserved as historical project materials. The repository-level Python workflow is now expressed through the English `.py` files.

## Current Scope

- The repository preserves the original stored full-corpus graph data
- The repository includes the previously trained GAT weights
- The repository now explains the label source explicitly
- The repository now includes an English sample-prediction path
- The repository does not try to present later upgraded experiments or a final paper package

## Citation

If you reference the repository before the article title is finalized, cite the repository as software / project material. See [CITATION.cff](./CITATION.cff).

## Contact

Jingqi Zeng  
Email: `zjingqi@163.com`
