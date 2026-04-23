# Notebook Guide

This repository is organized as a notebook-first workflow.

The notebooks here correspond to the original working version of the project and the existing stored model / output files kept in `../Data`.

## Execution Order

1. `1_Graph Embedding in UHF.ipynb`
   Builds graph objects from the structured Uyghur medicine input file and writes `../Data/all_graphs_to_be_predicted.pt`

2. `2_Prediction Using the GAT Model.ipynb`
   Loads graph tensors, defines and runs the GAT model, saves `../Data/gat_model.pth`, and exports:
   - `../Data/prediction_outputs.tsv`
   - `../Data/attention_weights.tsv`

3. `3_Quantitative of Compatibility Mechanisms Using the GAT Model.ipynb`
   Computes mean attention per layer, propagates multi-layer attention paths, and generates compatibility heatmaps

## Additional Notebooks

- `中药方剂-中医证候-多层注意力模型.ipynb`
  Original training notebook retained from the project workspace; it trains directly from `../Data/all_graphs_to_be_predicted.pt`

- `超参数优化-中药方剂-中医证候-多层注意力模型.ipynb`
  Original hyperparameter-search notebook retained from the project workspace; it uses the same committed graph tensor

- `Start_Jupyter.bat`
  Local helper launcher kept together with the original notebook workflow

## Scope Note

- This folder describes the original project workflow preserved in the repository.
- It is not intended to document the later extended experiment pipeline used during subsequent paper drafting.
- The repository already includes the training graph tensor file and trained model artifact used in this original workflow version.

## Important Assumptions

- Run notebooks from within the `Python/` folder
- The notebooks use relative paths such as `../Data`
- Output files are written back into `Data/` and `Figure/`

For a file-by-file dependency view, see [NOTEBOOK_IO.md](./NOTEBOOK_IO.md).
