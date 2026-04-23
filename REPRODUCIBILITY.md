# Reproducibility Guide

This file summarizes the minimum set of files and steps required to reproduce the current repository version.

## Core Stored Artifacts

### Training / validation side

- `Data/training_graphs_with_labels.pt`
  Canonical labeled graph tensor for the stored training workflow

- `Data/gat_model.pth`
  Previously trained GAT model artifact

### Prediction side

- `Data/example_prescription_input.xlsx`
  Example prescription input file

- `Data/prescriptions_to_predict.pt`
  Graph tensor generated from the example Excel input

- `Data/prescription_prediction_outputs.tsv`
  Prediction output exported from the stored example prediction run

- `Data/prescription_attention_weights.tsv`
  Attention output exported from the stored example prediction run

## Reproduction Paths

There are three practical reproduction paths:

1. Artifact-based inspection  
   Use the committed `.pt`, `.pth`, and `.tsv` files directly.

2. Script-based prediction reproduction  
   Recreate the prediction path from Excel input:

   ```powershell
   python scripts/generate_prediction_graphs.py --input-excel Data/example_prescription_input.xlsx --output-pt Data/prescriptions_to_predict.pt
   python scripts/run_gat_prediction.py --graph-pt Data/prescriptions_to_predict.pt --model-path Data/gat_model.pth --prediction-output Data/prescription_prediction_outputs.tsv --attention-output Data/prescription_attention_weights.tsv
   ```

3. Legacy notebook rerun reproduction  
   Re-execute the notebooks in order from `Python/`:
   - `1_Graph Embedding in UHF.ipynb`
   - `2_Prediction Using the GAT Model.ipynb`
   - `3_Quantitative of Compatibility Mechanisms Using the GAT Model.ipynb`

## Expected Folder Assumptions

- Run notebooks from the `Python/` directory
- Keep `Data/` at exactly `../Data`
- Keep `Figure/` at exactly `../Figure` when generating visual outputs

## Important Scope Note

- `training_graphs_with_labels.pt` is the canonical labeled tensor for training / validation
- `prescriptions_to_predict.pt` is the canonical unlabeled tensor for inference
- `all_graphs_to_be_predicted.pt` is retained only as a legacy filename for compatibility with the original notebooks
- This guide applies to the current repository snapshot only
