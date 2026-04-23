import argparse
from pathlib import Path

import pandas as pd
import torch
import torch.nn as nn
from torch_geometric.data import Batch
from torch_geometric.nn import GATConv, global_mean_pool


class GATModel(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim, num_heads, dropout_rate=0.4, dosage_weight=1.0):
        super().__init__()
        self.dosage_weight = dosage_weight
        self.layer1 = GATConv(in_dim, hidden_dim, heads=num_heads, dropout=dropout_rate)
        self.layer2 = GATConv(hidden_dim * num_heads, hidden_dim, heads=num_heads, dropout=dropout_rate)
        self.layer3 = GATConv(hidden_dim * num_heads, hidden_dim, heads=num_heads, dropout=dropout_rate)
        self.layer4 = GATConv(hidden_dim * num_heads, hidden_dim, heads=1, dropout=dropout_rate)
        self.fc = nn.Linear(hidden_dim, out_dim)
        self._initialize_weights()

    def _initialize_weights(self):
        for layer in [self.layer1, self.layer2, self.layer3, self.layer4]:
            nn.init.xavier_uniform_(layer.lin.weight)
            if layer.lin.bias is not None:
                nn.init.zeros_(layer.lin.bias)

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch
        x = x.clone()
        x[:, 90] = torch.clamp(x[:, 90] * self.dosage_weight, min=0, max=10)

        h, attn_weights_1 = self.layer1(x, edge_index, return_attention_weights=True)
        h = torch.relu(h)
        h, attn_weights_2 = self.layer2(h, edge_index, return_attention_weights=True)
        h = torch.relu(h)
        h, attn_weights_3 = self.layer3(h, edge_index, return_attention_weights=True)
        h = torch.relu(h)
        h, attn_weights_4 = self.layer4(h, edge_index, return_attention_weights=True)

        hg = global_mean_pool(h, batch)
        out = self.fc(hg)
        return out, hg, (attn_weights_1, attn_weights_2, attn_weights_3, attn_weights_4)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run GAT prediction on a PT file of prescription graphs."
    )
    parser.add_argument(
        "--graph-pt",
        default="Data/prescriptions_to_predict.pt",
        help="PT file containing prediction graphs.",
    )
    parser.add_argument(
        "--model-path",
        default="Data/gat_model.pth",
        help="Path to the trained GAT model state dict.",
    )
    parser.add_argument(
        "--prediction-output",
        default="Data/prescription_prediction_outputs.tsv",
        help="Output TSV for graph-level prediction probabilities and embeddings.",
    )
    parser.add_argument(
        "--attention-output",
        default="Data/prescription_attention_weights.tsv",
        help="Output TSV for edge-level attention weights.",
    )
    parser.add_argument("--start-index", type=int, default=0, help="Start graph index.")
    parser.add_argument(
        "--end-index",
        type=int,
        default=None,
        help="End graph index (inclusive). Defaults to the last graph.",
    )
    return parser.parse_args()


def format_value(val):
    return round(float(val), 4)


def as_single_graph_batch(graph):
    if getattr(graph, "batch", None) is None:
        return Batch.from_data_list([graph])
    return graph


def export_predictions(model, graphs, prediction_output_path, attention_output_path, start_index, end_index):
    output_results = []
    attention_results = []

    for graph in graphs[start_index : end_index + 1]:
        batch_graph = as_single_graph_batch(graph)
        out, hg, attn_weights = model(batch_graph)
        out_probs = torch.sigmoid(out).detach().cpu().numpy()

        output_results.append(
            {
                "cpm_id": graph.cpm_id,
                **{f"Class_{j + 1}": format_value(val) for j, val in enumerate(out_probs.flatten())},
                **{f"hg_{j + 1}": format_value(val) for j, val in enumerate(hg.detach().cpu().numpy().flatten())},
            }
        )

        node_names = graph.node_names
        edge_dict = {}

        for layer_idx, (edge_index, attn_weight) in enumerate(attn_weights, start=1):
            edge_index_np = edge_index.detach().cpu().numpy().T
            attn_weight_np = attn_weight.detach().cpu().numpy()

            for edge, attention_values in zip(edge_index_np, attn_weight_np):
                source_idx, target_idx = edge
                source_name = node_names[int(source_idx)]
                target_name = node_names[int(target_idx)]
                edge_key = (source_name, target_name)

                if edge_key not in edge_dict:
                    edge_dict[edge_key] = {
                        "cpm_id": graph.cpm_id,
                        "Source": source_name,
                        "Target": target_name,
                    }

                for head_idx, attention_value in enumerate(attention_values, start=1):
                    edge_dict[edge_key][f"attn_weights_{layer_idx}_head_{head_idx}"] = format_value(
                        attention_value
                    )

        attention_results.extend(edge_dict.values())

    prediction_output_path.parent.mkdir(parents=True, exist_ok=True)
    attention_output_path.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(output_results).to_csv(prediction_output_path, sep="\t", index=False)
    pd.DataFrame(attention_results).to_csv(attention_output_path, sep="\t", index=False)

    print(f"Prediction outputs written to {prediction_output_path}")
    print(f"Attention weights written to {attention_output_path}")


def main():
    args = parse_args()
    graph_pt = Path(args.graph_pt)
    model_path = Path(args.model_path)
    prediction_output_path = Path(args.prediction_output)
    attention_output_path = Path(args.attention_output)

    graphs = torch.load(graph_pt, weights_only=False)
    end_index = len(graphs) - 1 if args.end_index is None else min(args.end_index, len(graphs) - 1)

    model = GATModel(in_dim=91, hidden_dim=64, out_dim=4, num_heads=2, dropout_rate=0.4, dosage_weight=1.0)
    state_dict = torch.load(model_path, weights_only=False)
    model.load_state_dict(state_dict)
    model.eval()

    export_predictions(model, graphs, prediction_output_path, attention_output_path, args.start_index, end_index)


if __name__ == "__main__":
    main()
