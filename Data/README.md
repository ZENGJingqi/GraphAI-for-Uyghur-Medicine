# 📁 Data Directory

This folder contains all raw input files, intermediate outputs, and final processed results used in the project **"Quantifying compatibility mechanisms in Uyghur medicine with interpretable graph neural networks"**.

---

## 📂 File Descriptions

### 🔸 Input Files

| File Name                             | Description |
|--------------------------------------|-------------|
| `Test_input.xlsx`                    | Raw prescription-to-herb mapping table. Each row represents one herbal component (CHP) within a prescription (CPM). |
| `UHP_Encoder.tsv`                    | Numerical feature encoding for each CHP (Uyghur Herbal Piece), including physicochemical or semantic descriptors. |
| `UHP_Medicinal_properties_encode.tsv` | Encoded mapping between each CHP and its associated medicinal property (Dry, Moist, Cold, Hot), with strength levels. |
| `Uighur_herbalpieces.tsv`            | Metadata table describing individual CHP items, used for labeling and visualization. |
| `Uighur_herbal_formulas.tsv`         | Optional: Information about herbal prescription groups (CPM), names, sources, or classification. |
| `UHF_UHP.tsv` / `UHF_TCMT.tsv`       | Legacy or alternative mappings of prescriptions to herbal components or therapeutic classifications. |

---

### 🧠 Model and Graph Data

| File Name                         | Description |
|----------------------------------|-------------|
| `all_graphs_to_be_predicted.pt` | Serialized PyTorch Geometric graph list. Each graph represents a CPM and contains node features, edge attributes, node types, and CPM ID. |
| `gat_model.pth`                  | Trained Graph Attention Network (GAT) model with four GATConv layers and learned multi-head attention parameters. |

---

### 📈 Prediction and Attention Results

| File Name                         | Description |
|----------------------------------|-------------|
| `prediction_outputs.tsv`         | Model predictions per prescription (CPM), including: class probabilities (sigmoid) and graph-level embeddings. |
| `attention_weights.tsv`          | Raw attention weights from each GAT layer and head for every edge in every graph. |
| `attention_averages.tsv`         | Per-layer mean attention weights aggregated across all heads. Simplifies interpretation by reducing dimensionality. |
| `calculated_attention_weights.tsv` | Multi-layer propagated attention between node pairs, computed by tracing influence from source to target over 4 layers. Represents long-range compatibility impact. |

---

## 🔄 Data Flow Summary

```mermaid
graph TD
    A[Test_input.xlsx] --> B[Graph Construction]
    B --> C[all_graphs_to_be_predicted.pt]
    C --> D[GAT Model Prediction]
    D --> E[prediction_outputs.tsv]
    D --> F[attention_weights.tsv]
    F --> G[attention_averages.tsv]
    G --> H[calculated_attention_weights.tsv]

