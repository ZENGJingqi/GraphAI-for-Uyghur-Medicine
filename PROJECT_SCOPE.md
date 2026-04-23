# Project Scope

This file defines what the current repository version is intended to represent.

## What This Repository Includes

- The original notebook-based workflow for graph construction, GAT inference, and compatibility quantification
- A clearer script-based prediction path from Excel input to graph tensor to model output
- The structured data tables used by that workflow
- One previously generated model file: `Data/gat_model.pth`
- A canonical labeled training tensor: `Data/training_graphs_with_labels.pt`
- A canonical prediction tensor: `Data/prescriptions_to_predict.pt`
- Existing exported outputs from the earlier completed run:
  - `Data/prediction_outputs.tsv`
  - `Data/attention_weights.tsv`
  - `Data/attention_averages.tsv`
  - `Data/calculated_attention_weights.tsv`
- Example prediction outputs from the script-based path:
  - `Data/prescription_prediction_outputs.tsv`
  - `Data/prescription_attention_weights.tsv`
- Example figures generated from the original project version

## What This Repository Does Not Try to Be

- It is not the final paper repository
- It is not a benchmark-report repository
- It does not document later upgraded experiments or later retrained models
- It is not yet packaged as a command-line tool or installable Python package

## Current Purpose

The current purpose of the repository is to:

- introduce the project clearly
- preserve the original working version
- expose the notebook workflow and the clearer training/prediction file organization
- keep the previously completed model artifact and exported interpretability files available

## Recommended Interpretation

If you are reading this repository from GitHub:

- treat it as the current stable project snapshot
- use it to understand the workflow, files, and existing artifacts
- do not assume that every later paper-drafting experiment is included here
