# Data Directory Guide

This folder contains the stored project data, the English label matrix, and the sample prediction artifacts.

## Full-Corpus Files

- `all_graphs_to_be_predicted.pt`
  Legacy filename from the original workflow. This is the stored full-corpus graph tensor, not a small prediction-only set.

- `full_prescription_graphs_with_labels.pt`
  English-named full-corpus graph tensor aligned with the legacy `.pt` file.

- `gat_model.pth`
  Previously trained GAT model weights.

## Label Files

- `UHF_Cluster_Dummies_Unique.csv`
  Original cluster dummy file from the earlier workflow.

- `UHF_Label_Matrix.csv`
  English label matrix with columns `Class_1` to `Class_4` for all 480 prescriptions.

Notes:

- 474 prescriptions come directly from the legacy cluster dummy file.
- 6 prescriptions have no `UHF_TCMT.tsv` rows and are filled with zero labels.
- Those zero labels match the stored labels in the legacy full-corpus `.pt` file.

## Source Tables

- `UHF_UHP.tsv`
  Full formula-to-herbal-piece relation table.

- `UHF_TCMT.tsv`
  Formula-to-terminology mapping used in the original label-generation context.

- `UHP_Encoder.tsv`
  Herb-level encoded node features.

- `UHP_Medicinal_properties_encode.tsv`
  Herb-to-property edge table.

- `Uighur_herbal_formulas.tsv`
  Formula metadata table.

- `Uighur_herbal_pieces.tsv`
  Herbal piece metadata table.

## Sample Prediction Files

- `sample_prescription_input.xlsx`
  Small sample input table for simulation testing.

- `sample_prediction_graphs.pt`
  Unlabeled graph tensor built from the sample input Excel file.

- `sample_prediction_outputs.tsv`
  Prediction probabilities and graph embeddings from the sample simulation.

- `sample_attention_weights.tsv`
  Attention weights from the sample simulation.

## Legacy Output Files

- `prediction_outputs.tsv`
- `attention_weights.tsv`
- `attention_averages.tsv`
- `calculated_attention_weights.tsv`

These are stored outputs from the earlier notebook-based workflow and are kept for traceability.
