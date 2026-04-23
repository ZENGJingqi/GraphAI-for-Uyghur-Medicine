# Notebook Input / Output Map

This file summarizes the input files, generated outputs, and dependencies for the three core notebooks.

## 1. `1_Graph Embedding in UHF.ipynb`

Purpose:
- Build graph objects from the structured Uyghur medicine input table

Main inputs:
- `../Data/Test_input.xlsx`
- `../Data/UHP_Encoder.tsv`

Main output:
- `../Data/all_graphs_to_be_predicted.pt`

Notes:
- This notebook prepares the graph dataset used by the later notebooks
- Downstream notebooks depend on this output

## 2. `2_Prediction Using the GAT Model.ipynb`

Purpose:
- Load graph tensors, run the GAT model, and export predictions plus raw attention values

Main input:
- `../Data/all_graphs_to_be_predicted.pt`

Main outputs:
- `../Data/gat_model.pth`
- `../Data/prediction_outputs.tsv`
- `../Data/attention_weights.tsv`

Notes:
- This notebook defines the model and performs inference / export
- The third notebook depends on `attention_weights.tsv`

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

Notes:
- This notebook turns raw layer attention into propagated compatibility scores
- It also creates the figure-level interpretability output

## Dependency Chain

```text
Test_input.xlsx + UHP_Encoder.tsv
    -> 1_Graph Embedding in UHF.ipynb
    -> all_graphs_to_be_predicted.pt
    -> 2_Prediction Using the GAT Model.ipynb
    -> gat_model.pth + prediction_outputs.tsv + attention_weights.tsv
    -> 3_Quantitative of Compatibility Mechanisms Using the GAT Model.ipynb
    -> attention_averages.tsv + calculated_attention_weights.tsv + heatmaps
```

