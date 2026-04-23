# Notebook Input / Output Map

This file summarizes the legacy notebook dependencies and clarifies where they differ from the newer script-based workflow.

## 1. `1_Graph Embedding in UHF.ipynb`

Purpose:
- Build prediction-style graphs from a user-style input table

Main inputs:
- `../Data/Test_input.xlsx`
- `../Data/UHP_Encoder.tsv`
- `../Data/UHP_Medicinal_properties_encode.tsv`

Main output:
- `../Data/all_graphs_to_be_predicted.pt`

Important note:
- This is a prediction-side graph builder
- It is not the canonical full-corpus training graph builder

## 2. `2_Prediction Using the GAT Model.ipynb`

Purpose:
- Load graph tensors, run the GAT model, and export predictions plus raw attention values

Main inputs:
- `../Data/all_graphs_to_be_predicted.pt`
- `../Data/gat_model.pth`

Main outputs:
- `../Data/prediction_outputs.tsv`
- `../Data/attention_weights.tsv`

## 3. `3_Quantitative of Compatibility Mechanisms Using the GAT Model.ipynb`

Purpose:
- Aggregate multi-layer attention and generate compatibility visualizations

Main inputs:
- `../Data/attention_weights.tsv`
- `../Data/Uighur_herbal_pieces.tsv`

Main outputs:
- `../Data/attention_averages.tsv`
- `../Data/calculated_attention_weights.tsv`
- `../Figure/*_Attention_Heatmap.pdf`

## Historical Training Notebooks

The retained Chinese notebooks use a different training-side assumption:

- labeled graphs already exist
- labels are read from graph attribute `y`
- graph filename is still the legacy `all_graphs_to_be_predicted.pt`

In the clearer repository terminology, that role is now represented by:

- `../Data/training_graphs_with_labels.pt`

## Recommended Canonical File Mapping

```text
Training / validation:
    training_graphs_with_labels.pt

Prediction from user Excel:
    example_prescription_input.xlsx
        -> scripts/generate_prediction_graphs.py
        -> prescriptions_to_predict.pt
        -> scripts/run_gat_prediction.py
        -> prescription_prediction_outputs.tsv
        -> prescription_attention_weights.tsv
```
