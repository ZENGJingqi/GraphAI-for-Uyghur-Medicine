# Python Folder Overview

The Python directory contains the notebook-based workflow for graph construction, pretrained inference, interpretation, and training experiments in GraphAI for Uyghur Medicine.

## Recommended Notebook Order

For most users, the intended sequence is:

1. `1_Graph Embedding in Uyghur Formulae.ipynb`  
   Reads the example input file and builds the graph tensor used for inference.

2. `2_Prediction Using the GAT Model.ipynb`  
   Loads the graph tensor and the pretrained GAT model to generate prediction outputs and attention outputs.

3. `3_Quantitative Evaluation of Compatibility Mechanisms Using the GAT Model.ipynb`  
   Uses the attention outputs to support compatibility interpretation and figure generation.

## Training Notebook

- `Graph Attention Network.ipynb`  
  Training and evaluation notebook based on the full labeled graph corpus.

## Hyperparameter Notebook

- `Hyperparameter Search for GAT.ipynb`  
  Hyperparameter search notebook for the GAT workflow.

## Practical Notes

- The workflow is notebook-driven.
- The stored full corpus is `../Data/full_prescription_graphs_with_labels.pt`.
- The bundled example inference input is `../Data/Test_input.xlsx`.
- The bundled example inference graph tensor is `../Data/prediction_graphs_from_input.pt`.
