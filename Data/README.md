# Data Directory Guide

This folder contains both source tables and generated artifacts used by the Uyghur medicine GAT workflow.

## Source Tables

- `Test_input.xlsx`
  Main structured input workbook used by the graph-construction notebook

- `Uighur_herbal_formulas.tsv`
  Formula-level structured table for Uyghur medicine prescriptions

- `Uighur_herbal_pieces.tsv`
  Herbal piece metadata table

- `UHF_UHP.tsv`
  Formula-to-herbal-piece relationship table used in graph construction

- `UHF_TCMT.tsv`
  Formula-to-terminology / therapeutic mapping table

- `UHP_Medicinal_properties_encode.tsv`
  Encoded medicinal-property table for herbal pieces

- `UHP_Encoder.tsv`
  Combined herbal feature table used during graph embedding

## Generated Artifacts

- `all_graphs_to_be_predicted.pt`
  Serialized graph dataset generated from the input tables

- `gat_model.pth`
  Saved model weights from the GAT notebook

- `prediction_outputs.tsv`
  Formula-level model predictions

- `attention_weights.tsv`
  Raw edge-level attention weights exported from all GAT layers

- `attention_averages.tsv`
  Layer-wise averaged attention values

- `calculated_attention_weights.tsv`
  Propagated compatibility scores aggregated across multiple attention layers

## Usage Notes

- The notebooks in `../Python/` expect this folder at exactly `../Data`
- Some files are intermediate outputs and may be overwritten during reruns
- Keep the source tables unchanged if exact reproduction of the current outputs is required

