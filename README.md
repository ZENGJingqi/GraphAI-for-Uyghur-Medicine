# GraphAI for Uyghur Medicine

This repository documents the graph-based modeling workflow for Uyghur medicine prescriptions.

The repository keeps the original stored project artifacts and provides English Python entry points for the main steps.

![Project Overview](Figure/Graphic_abstract.png)

## What Is Stored in the Repository

The key stored full-corpus graph file is:

- `Data/full_prescription_graphs_with_labels.pt`

Despite the filename, this file is the full stored graph corpus for all available samples. Training and validation are created later by splitting this full corpus.

The repository also stores:

- `Data/gat_model.pth`
- `Data/UHF_Cluster_Dummies_Unique.csv`
- `Data/UHF_Label_Matrix.csv`
- the original source tables
- the original legacy notebooks
- English Python workflow files

## Minimal Repository Structure

```text
GraphAI-for-Uyghur-Medicine/
+-- Data/
|   +-- full_prescription_graphs_with_labels.pt
|   +-- gat_model.pth
|   +-- UHF_UHP.tsv
|   +-- UHF_TCMT.tsv
|   +-- UHF_Cluster_Dummies_Unique.csv
|   +-- UHF_Label_Matrix.csv
|   +-- UHP_Encoder.tsv
|   +-- UHP_Medicinal_properties_encode.tsv
|   `-- Test_input.xlsx
+-- Python/
|   +-- build_label_matrix.py
|   +-- build_full_corpus_graphs.py
|   +-- build_sample_prediction_graphs.py
|   +-- run_gat_prediction.py
|   +-- train_validate_gat.py
|   +-- graph_pipeline_utils.py
|   `-- legacy notebooks
+-- Figure/
`-- README.md
```

## English Python Workflow

### 1. Build the English label matrix

```powershell
python Python/build_label_matrix.py
```

This generates `Data/UHF_Label_Matrix.csv`.

Important detail:

- The original cluster dummy file has 474 labeled prescriptions.
- 6 prescriptions have no `UHF_TCMT.tsv` rows.
- In the normalized English label matrix, those 6 prescriptions are filled with zero labels.
- That zero-filled behavior matches the labels already stored inside `full_prescription_graphs_with_labels.pt`.

### 2. Rebuild the full graph corpus for verification

```powershell
python Python/build_full_corpus_graphs.py
```

This rebuilds a verification `.pt` file from the source tables and the English label matrix.

The script preserves the legacy `CPM_ID` order so the rebuilt tensor can be compared directly with the stored full-corpus `.pt` file.

### 3. Train or evaluate the GAT model

```powershell
python Python/train_validate_gat.py --mode evaluate-existing
```

or

```powershell
python Python/train_validate_gat.py --mode train
```

The default full-corpus input is `Data/full_prescription_graphs_with_labels.pt`.

### 4. Simulate prediction from an Excel input

```powershell
python Python/build_sample_prediction_graphs.py --input-excel Data/Test_input.xlsx
python Python/run_gat_prediction.py --graph-pt Data/prediction_graphs_from_input.pt
```

This path is for simulation or user-provided prediction input. The generated files are outputs of the workflow, not core stored repository assets.

## Legacy Notebook Material

The repository still keeps the original notebooks for traceability:

- `Python/1_Graph Embedding in UHF.ipynb`
- `Python/2_Prediction Using the GAT Model.ipynb`
- `Python/3_Quantitative of Compatibility Mechanisms Using the GAT Model.ipynb`
- `Python/Legacy_Training_Multilayer_GAT.ipynb`
- `Python/Legacy_Hyperparameter_Search_Multilayer_GAT.ipynb`

## Reference Files

- [Data/README.md](./Data/README.md)
- [Python/README.md](./Python/README.md)
- [PROJECT_SCOPE.md](./PROJECT_SCOPE.md)
- [REPRODUCIBILITY.md](./REPRODUCIBILITY.md)
- [WORKFLOW_LOGIC.md](./WORKFLOW_LOGIC.md)

## Citation

If you reference the repository before the article title is finalized, cite the repository as software / project material. See [CITATION.cff](./CITATION.cff).
