# 🧪 Python Scripts for Graph-Based Uyghur Medicine Modeling

This folder contains three Jupyter notebooks that implement the core workflow of the project **"Quantifying compatibility mechanisms in Uyghur medicine with interpretable graph neural networks"**.

Each notebook corresponds to a distinct stage in the pipeline: from graph construction to GNN-based prediction and final attention-driven analysis.

---

## 📂 Contents

### 1️⃣ `1_Graph Embedding in UHF.ipynb`
**Purpose:**  
Constructs graphs from Uyghur herbal prescription data (`UHF`) using medicinal properties and herb encodings. Each prescription is transformed into a graph where:
- Nodes represent herbal components (CHPs)
- Virtual nodes represent four therapeutic attributes (Dry, Moist, Cold, Hot)
- Node features include encoded medicinal properties and dosage ratios

**Output:**  
A PyTorch Geometric `.pt` file containing a list of graph objects:


---

### 2️⃣ `2_Prediction Using the GAT Model.ipynb`
**Purpose:**  
Loads a trained multi-layer Graph Attention Network (GAT) and performs prediction on the encoded graphs. For each graph (prescription), the model outputs:
- Class probabilities (after sigmoid activation)
- Graph-level embedding (`hg`)
- Multi-head attention weights from all four GAT layers

**Output:**  
- `prediction_outputs.tsv`: Probabilities and embeddings  
- `attention_weights.tsv`: Raw attention values per layer and head

---

### 3️⃣ `3_Quantitative of Compatibility Mechanisms Using the GAT Model.ipynb`
**Purpose:**  
Performs a quantitative interpretation of compatibility mechanisms between herbs:
- Computes attention propagation paths across 4 GAT layers
- Aggregates cumulative attention from source to target nodes
- Visualizes intra-prescription herbal influence via attention heatmaps

**Output:**  
- `calculated_attention_weights.tsv`: Final aggregated pairwise attention  
- Heatmap PDF files stored in `../Figure/`

---

## 📌 Dependencies

These notebooks require the following core packages:

- `torch`, `torch_geometric`
- `networkx`, `matplotlib`, `pandas`, `numpy`
- `tqdm`, `openpyxl` (for Excel I/O)




