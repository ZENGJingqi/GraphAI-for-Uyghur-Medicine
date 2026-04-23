# Workflow Logic

This document clarifies the current codebase logic and separates training assets from prediction assets.

## 1. What the repository currently contains

There are two different graph-generation use cases in this project:

1. Training / validation graphs  
   These are the labeled graphs used to fit and validate the GAT model.

2. Prediction graphs  
   These are unlabeled graphs generated from a user-provided prescription table for inference.

The earlier repository mixed these two responsibilities under the single filename `all_graphs_to_be_predicted.pt`. That filename is not precise enough for a reproducible workflow, because the training notebooks require labeled graphs while the prediction workflow should use unlabeled graphs.

## 2. Current data roles

- `Data/UHF_UHP.tsv`
  Full formula-to-herbal-piece table for the 480-formula corpus.

- `Data/UHF_TCMT.tsv`
  Formula-to-terminology mapping used in the original training context.

- `Data/training_graphs_with_labels.pt`
  Canonical labeled graph tensor for training and validation.

- `Data/example_prescription_input.xlsx`
  Example Excel file showing the expected user input format for prediction.

- `Data/prescriptions_to_predict.pt`
  Canonical unlabeled graph tensor generated from the prediction Excel input.

- `Data/gat_model.pth`
  Previously trained GAT weights.

## 3. Code responsibilities

### A. Graph construction for prediction

Script:
- `scripts/generate_prediction_graphs.py`

Input:
- Excel table with columns `CPM_ID`, `CHP_ID`, `Dosage_ratio`
- `UHP_Encoder.tsv`
- `UHP_Medicinal_properties_encode.tsv`

Output:
- `prescriptions_to_predict.pt`

Logic:
- Build one graph per prescription (`CPM_ID`)
- Use herb encoder features as actual-node features
- Append dosage ratio as the last node feature
- Add four virtual medicinal-property nodes
- Connect herbs to virtual nodes using encoded medicinal properties
- Export an unlabeled PyTorch Geometric graph list

### B. Prediction

Script:
- `scripts/run_gat_prediction.py`

Input:
- `prescriptions_to_predict.pt`
- `gat_model.pth`

Outputs:
- graph-level probabilities
- graph embeddings
- edge-level attention weights

Logic:
- Load the stored GAT architecture
- Apply sigmoid to 4 output logits
- Export `Class_1` to `Class_4` probabilities
- Export graph embedding dimensions `hg_1 ...`
- Export attention weights layer by layer and head by head

### C. Compatibility quantification

Legacy notebook:
- `Python/3_Quantitative of Compatibility Mechanisms Using the GAT Model.ipynb`

Role:
- Aggregate raw attention values
- Produce propagated compatibility weights
- Save heatmaps as PDF

## 4. Important distinction

`Python/1_Graph Embedding in UHF.ipynb` is a prediction-style graph builder because it reads `Test_input.xlsx`.

It is not the canonical full-corpus training graph builder, even though the old repository state temporarily used the filename `all_graphs_to_be_predicted.pt` for the labeled 480-graph training tensor.

## 5. Recommended practical workflow

1. Prepare an Excel file with columns:
   - `CPM_ID`
   - `CHP_ID`
   - `Dosage_ratio`
2. Run `scripts/generate_prediction_graphs.py`
3. Run `scripts/run_gat_prediction.py`
4. Read:
   - `prescription_prediction_outputs.tsv`
   - `prescription_attention_weights.tsv`

## 6. Legacy compatibility note

The legacy filename `all_graphs_to_be_predicted.pt` is retained only for backward compatibility with the original notebooks.

For future development and paper-facing descriptions, the canonical distinction should be:

- `training_graphs_with_labels.pt`
- `prescriptions_to_predict.pt`
