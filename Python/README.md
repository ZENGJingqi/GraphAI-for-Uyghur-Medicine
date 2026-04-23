# Notebook Guide

This folder preserves the original notebook workflow.

For a clearer production-style path, prefer the scripts in `../scripts/`.

## Main Notebook Roles

1. `1_Graph Embedding in UHF.ipynb`
   Builds prediction-style graphs from the legacy example input table

2. `2_Prediction Using the GAT Model.ipynb`
   Loads graphs, applies the GAT model, and exports predictions plus attention values

3. `3_Quantitative of Compatibility Mechanisms Using the GAT Model.ipynb`
   Aggregates attention and generates compatibility heatmaps

## Additional Historical Notebooks

- `中药方剂-中医证候-多层注意力模型.ipynb`
  Original training notebook retained from the project workspace

- `超参数优化-中药方剂-中医证候-多层注意力模型.ipynb`
  Original hyperparameter-search notebook retained from the project workspace

- `Start_Jupyter.bat`
  Local helper launcher retained with the original notebook workflow

## Scope Note

- These notebooks are preserved as historical project code
- They still use some legacy filenames such as `all_graphs_to_be_predicted.pt`
- For new documentation, use the canonical distinction described in `../WORKFLOW_LOGIC.md`

For a file-by-file dependency view, see [NOTEBOOK_IO.md](./NOTEBOOK_IO.md).
