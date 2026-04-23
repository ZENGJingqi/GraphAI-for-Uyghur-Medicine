# Data Folder Overview

This folder stores the core project data and model files.

## Main Files

- `full_prescription_graphs_with_labels.pt`  
  Full labeled graph corpus used for training and validation splitting.

- `gat_model.pth`  
  Pretrained GAT model weights used by the inference notebook.

- `Test_input.xlsx`  
  Bundled example prescription input for inference simulation.

- `prediction_graphs_from_input.pt`  
  Small example inference graph tensor generated from `Test_input.xlsx`.

## Label and Source Tables

- `UHF_Cluster_Dummies_Unique.csv`: original label source
- `UHF_Label_Matrix.csv`: normalized label table
- `UHF_UHP.tsv`: prescription-to-herb relation table
- `UHF_TCMT.tsv`: terminology mapping table
- `UHP_Encoder.tsv`: encoded herb feature table
- `UHP_Medicinal_properties_encode.tsv`: herb-to-property relation table
- `Uighur_herbal_formulas.tsv`: prescription metadata
- `Uighur_herbal_pieces.tsv`: herbal piece metadata

The repository keeps the necessary stored assets only. Generated prediction and evaluation result tables are not included.
