# Quantifying Compatibility Mechanisms in Uyghur Medicine with Interpretable Graph Neural Networks

This repository contains the code, structured data, trained artifacts, and figures used to model compatibility mechanisms in Uyghur medicine prescriptions with Graph Attention Networks (GATs).

The workflow is notebook-first: prescriptions are encoded as graphs, a multi-layer GAT model performs prediction, and attention weights are traced to quantify compatibility relationships between herbal components.

![Graphical Abstract](Figure/Graphic_abstract.png)

## Overview

- Graph construction from structured Uyghur medicine prescription tables
- Graph Attention Network inference for prescription-level prediction
- Multi-layer attention tracing for interpretable compatibility quantification
- Heatmap-based visualization of propagated herbal influence

## Repository Structure

```text
GraphAI-for-Uyghur-Medicine/
+-- Data/
|   +-- Test_input.xlsx
|   +-- Uighur_herbal_formulas.tsv
|   +-- Uighur_herbal_pieces.tsv
|   +-- UHF_UHP.tsv
|   +-- UHF_TCMT.tsv
|   +-- UHP_Encoder.tsv
|   +-- all_graphs_to_be_predicted.pt
|   +-- gat_model.pth
|   +-- prediction_outputs.tsv
|   +-- attention_weights.tsv
|   +-- attention_averages.tsv
|   `-- calculated_attention_weights.tsv
+-- Figure/
+-- Python/
+-- requirements.txt
+-- requirements-minimal.txt
`-- README.md
```

Directory notes:

- [Data/README.md](./Data/README.md)
- [Python/README.md](./Python/README.md)

## Workflow

1. Run `Python/1_Graph Embedding in UHF.ipynb`
   This builds graph objects from the structured input table and writes `Data/all_graphs_to_be_predicted.pt`.

2. Run `Python/2_Prediction Using the GAT Model.ipynb`
   This loads graph tensors, applies the GAT model, and exports:
   - `Data/gat_model.pth`
   - `Data/prediction_outputs.tsv`
   - `Data/attention_weights.tsv`

3. Run `Python/3_Quantitative of Compatibility Mechanisms Using the GAT Model.ipynb`
   This computes averaged attention, propagates multi-layer attention paths, and writes:
   - `Data/attention_averages.tsv`
   - `Data/calculated_attention_weights.tsv`
   - heatmap PDFs in `Figure/`

## Environment

Two dependency files are included:

- `requirements.txt`
  Full local environment snapshot including Jupyter and notebook tooling

- `requirements-minimal.txt`
  Minimal dependency set for running the core notebooks

Recommended runtime:

- Python 3.10+
- PyTorch 2.7.x
- Torch Geometric 2.6.x
- CPU or GPU with matching PyTorch build

Example setup:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-minimal.txt
```

## Key Files

Inputs:

- `Data/Test_input.xlsx`
- `Data/Uighur_herbal_formulas.tsv`
- `Data/Uighur_herbal_pieces.tsv`
- `Data/UHF_UHP.tsv`
- `Data/UHF_TCMT.tsv`
- `Data/UHP_Encoder.tsv`

Generated artifacts:

- `Data/all_graphs_to_be_predicted.pt`
- `Data/gat_model.pth`
- `Data/prediction_outputs.tsv`
- `Data/attention_weights.tsv`
- `Data/attention_averages.tsv`
- `Data/calculated_attention_weights.tsv`

## Reproducibility Notes

- Execute notebooks from within the `Python/` directory
- Preserve the relative path from `Python/` to `../Data`
- The repository currently favors direct reproducibility over packaging; it is not yet organized as a CLI tool or Python package

## Citation

See [CITATION.cff](./CITATION.cff) for repository citation metadata.

## Contact

Jingqi Zeng  
Email: `zjingqi@163.com`

