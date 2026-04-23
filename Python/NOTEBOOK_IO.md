# Legacy Notebook IO Map

This file documents the retained legacy notebook flow.

## `1_Graph Embedding in UHF.ipynb`

- Input: `../Data/Test_input.xlsx`
- Output: `../Data/prediction_graphs_from_input.pt`

## `2_Prediction Using the GAT Model.ipynb`

- Input: `../Data/prediction_graphs_from_input.pt`
- Input: `../Data/gat_model.pth`
- Output: generated prediction TSV files when executed

## `3_Quantitative of Compatibility Mechanisms Using the GAT Model.ipynb`

- Input: generated attention TSV files when executed
- Input: `../Data/Uighur_herbal_pieces.tsv`
- Output: generated compatibility TSV files when executed
- Output: `../Figure/*_Attention_Heatmap.pdf`

## English Python Entry Points

- `build_label_matrix.py`
- `build_full_corpus_graphs.py`
- `build_sample_prediction_graphs.py`
- `run_gat_prediction.py`
- `train_validate_gat.py`
