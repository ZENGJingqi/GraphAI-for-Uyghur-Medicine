# Data Directory Guide

This folder contains both source tables and generated artifacts used by the Uyghur medicine GAT workflow.

## Canonical Training Files

- `training_graphs_with_labels.pt`
  Canonical labeled graph tensor for training and validation

- `gat_model.pth`
  Previously trained GAT model weights

## Canonical Prediction Files

- `example_prescription_input.xlsx`
  Example Excel input for user-provided prescriptions

- `prescriptions_to_predict.pt`
  Unlabeled prediction graph tensor generated from the Excel input

- `prescription_prediction_outputs.tsv`
  Prediction probabilities and graph embeddings exported from the prediction script

- `prescription_attention_weights.tsv`
  Edge-level attention weights exported from the prediction script

## Source Tables

- `UHF_UHP.tsv`
  Full formula-to-herbal-piece relation table for the 480-formula corpus

- `UHF_TCMT.tsv`
  Formula-to-terminology mapping used in the original training context

- `UHP_Encoder.tsv`
  Herb-level encoded node features

- `UHP_Medicinal_properties_encode.tsv`
  Herb-to-medicinal-property edge table

- `Uighur_herbal_formulas.tsv`
  Formula metadata table

- `Uighur_herbal_pieces.tsv`
  Herbal piece metadata table

## Legacy Compatibility Files

- `all_graphs_to_be_predicted.pt`
  Legacy filename retained for the original notebooks; do not use this as the canonical training or prediction filename in new documentation

- `Test_input.xlsx`
  Legacy example input filename retained for the original notebook workflow

- `prediction_outputs.tsv`
- `attention_weights.tsv`
- `attention_averages.tsv`
- `calculated_attention_weights.tsv`
  Stored outputs from the earlier notebook-based workflow

## Usage Notes

- Use the scripts in `../scripts/` for the clearer Excel -> graph -> prediction pipeline
- Use `training_graphs_with_labels.pt` when referring to the labeled graph tensor for training / validation
- Use `prescriptions_to_predict.pt` when referring to the unlabeled graph tensor for inference
- The legacy files are still kept so the original notebooks remain understandable
