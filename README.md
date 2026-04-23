# GraphAI for Uyghur Medicine

This repository documents the current graph-based modeling workflow for Uyghur medicine prescriptions.

It preserves the original notebooks, the previously trained GAT model, the stored training graph tensor, and a clearer prediction pipeline for user-provided prescription input.

It does not aim to present the later paper-upgrade experiments or any newly retrained version.

![Project Overview](Figure/Graphic_abstract.png)

## Project Overview

- Graph construction from structured Uyghur medicine prescription tables
- GAT-based prescription-level prediction
- Multi-layer attention tracing for compatibility interpretation
- Heatmap-based visualization of propagated herbal influence

## Key Clarification

This repository contains two different graph use cases:

1. Training / validation graphs  
   Canonical file: `Data/training_graphs_with_labels.pt`

2. Prediction graphs generated from user input  
   Canonical file: `Data/prescriptions_to_predict.pt`

The old filename `Data/all_graphs_to_be_predicted.pt` is retained only as a legacy compatibility artifact for the original notebooks. It should not be used as the canonical name when describing the project in methods or documentation.

For the detailed logic split, see [WORKFLOW_LOGIC.md](./WORKFLOW_LOGIC.md).

## Repository Structure

```text
GraphAI-for-Uyghur-Medicine/
+-- Data/
|   +-- example_prescription_input.xlsx
|   +-- prescriptions_to_predict.pt
|   +-- training_graphs_with_labels.pt
|   +-- gat_model.pth
|   +-- prescription_prediction_outputs.tsv
|   +-- prescription_attention_weights.tsv
|   +-- UHF_UHP.tsv
|   +-- UHF_TCMT.tsv
|   +-- UHP_Encoder.tsv
|   +-- UHP_Medicinal_properties_encode.tsv
|   `-- ...
+-- Figure/
+-- Python/
+-- scripts/
+-- WORKFLOW_LOGIC.md
`-- README.md
```

Directory notes:

- [Data/README.md](./Data/README.md)
- [Python/README.md](./Python/README.md)
- [Figure/README.md](./Figure/README.md)
- [PROJECT_SCOPE.md](./PROJECT_SCOPE.md)
- [REPRODUCIBILITY.md](./REPRODUCIBILITY.md)
- [WORKFLOW_LOGIC.md](./WORKFLOW_LOGIC.md)

## Recommended Prediction Workflow

1. Prepare an Excel table with columns:
   - `CPM_ID`
   - `CHP_ID`
   - `Dosage_ratio`

2. Build prediction graphs:

```powershell
python scripts/generate_prediction_graphs.py --input-excel Data/example_prescription_input.xlsx --output-pt Data/prescriptions_to_predict.pt
```

3. Run GAT prediction:

```powershell
python scripts/run_gat_prediction.py --graph-pt Data/prescriptions_to_predict.pt --model-path Data/gat_model.pth --prediction-output Data/prescription_prediction_outputs.tsv --attention-output Data/prescription_attention_weights.tsv
```

4. Read results:
   - `Data/prescription_prediction_outputs.tsv`
   - `Data/prescription_attention_weights.tsv`

## Legacy Notebook Workflow

The original notebooks are preserved in `Python/`.

- `1_Graph Embedding in UHF.ipynb`
  Builds prediction-style graphs from `Test_input.xlsx`

- `2_Prediction Using the GAT Model.ipynb`
  Loads graphs and exports probabilities plus raw attention values

- `3_Quantitative of Compatibility Mechanisms Using the GAT Model.ipynb`
  Aggregates attention into compatibility scores and heatmaps

The original training-related notebooks are also retained in `Python/` as historical project materials.

## Current Repository Scope

- `Data/training_graphs_with_labels.pt` is the canonical labeled tensor for the stored training/validation workflow
- `Data/gat_model.pth` is the previously trained model artifact
- `Data/example_prescription_input.xlsx` is an example user input table
- `Data/prescriptions_to_predict.pt` is the canonical unlabeled tensor for prediction
- `Data/prescription_prediction_outputs.tsv` and `Data/prescription_attention_weights.tsv` are generated from the example prediction path
- Existing legacy outputs are still preserved from the earlier stored workflow

## Environment

Two dependency files are included:

- `requirements.txt`
  Full local environment snapshot including notebook tooling

- `requirements-minimal.txt`
  Minimal dependency set for running the graph and prediction scripts

Recommended runtime:

- Python 3.10+
- PyTorch 2.7.x
- Torch Geometric 2.6.x

Example setup:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-minimal.txt
```

## Citation

If you reference the repository before the article title is finalized, cite the repository as software / project material. See [CITATION.cff](./CITATION.cff).

## Contact

Jingqi Zeng  
Email: `zjingqi@163.com`
