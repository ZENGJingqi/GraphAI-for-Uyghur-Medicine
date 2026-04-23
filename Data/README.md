# Data Directory Guide

This folder contains both source tables and generated artifacts used by the Uyghur medicine GAT workflow.

The files in this folder belong to the earlier completed project version that is currently being preserved in the repository.

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
  Serialized graph dataset generated from the input tables and committed for reproduction of the stored workflow version

- `gat_model.pth`
  Saved model weights from the previously completed GAT notebook workflow and committed for repository-level reproduction

- `prediction_outputs.tsv`
  Formula-level model predictions from the existing stored run

- `attention_weights.tsv`
  Raw edge-level attention weights exported from the existing stored run

- `attention_averages.tsv`
  Layer-wise averaged attention values derived from the stored run

- `calculated_attention_weights.tsv`
  Propagated compatibility scores aggregated across multiple attention layers from the stored run

## Usage Notes

- The notebooks in `../Python/` expect this folder at exactly `../Data`
- Some files are intermediate outputs and may be overwritten during reruns
- Keep the source tables and stored artifacts unchanged if exact reproduction of the current repository version is required
- The current repository already includes the key `.pt` and `.pth` files required to reproduce the stored workflow version
