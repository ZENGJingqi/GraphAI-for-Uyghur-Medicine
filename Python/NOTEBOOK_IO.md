# Legacy Notebook IO Map

This file documents the legacy notebook flow.

## `1_Graph Embedding in UHF.ipynb`

- Input: `../Data/Test_input.xlsx`
- Output: `../Data/all_graphs_to_be_predicted.pt`

Important note:
- In the repository-level explanation, `all_graphs_to_be_predicted.pt` is treated as the stored full-corpus graph tensor.
- The notebook name and output filename are preserved as historical artifacts.

## `2_Prediction Using the GAT Model.ipynb`

- Input: `../Data/all_graphs_to_be_predicted.pt`
- Input: `../Data/gat_model.pth`
- Output: `../Data/prediction_outputs.tsv`
- Output: `../Data/attention_weights.tsv`

## `3_Quantitative of Compatibility Mechanisms Using the GAT Model.ipynb`

- Input: `../Data/attention_weights.tsv`
- Input: `../Data/Uighur_herbal_pieces.tsv`
- Output: `../Data/attention_averages.tsv`
- Output: `../Data/calculated_attention_weights.tsv`
- Output: `../Figure/*_Attention_Heatmap.pdf`

## English Python Replacements

- `build_label_matrix.py`
- `build_full_corpus_graphs.py`
- `build_sample_prediction_graphs.py`
- `run_gat_prediction.py`
- `train_validate_gat.py`
