import argparse
from pathlib import Path

import pandas as pd
import torch

from graph_pipeline_utils import GATModel, as_single_graph_batch, format_value, get_repo_root


def parse_args():
    repo_root = get_repo_root()
    parser = argparse.ArgumentParser(
        description="Run GAT prediction on sample or user-provided graph tensors."
    )
    parser.add_argument(
        "--graph-pt",
        default=str(repo_root / "Data" / "prediction_graphs_from_input.pt"),
        help="PT file containing prediction graphs.",
    )
    parser.add_argument(
        "--model-path",
        default=str(repo_root / "Data" / "gat_model.pth"),
        help="Path to the trained GAT model weights.",
    )
    parser.add_argument(
        "--prediction-output",
        default=str(repo_root / "Data" / "prediction_outputs_from_input.tsv"),
        help="Output TSV for prediction probabilities and graph embeddings.",
    )
    parser.add_argument(
        "--attention-output",
        default=str(repo_root / "Data" / "attention_weights_from_input.tsv"),
        help="Output TSV for edge-level attention weights.",
    )
    parser.add_argument("--start-index", type=int, default=0, help="Start graph index.")
    parser.add_argument("--end-index", type=int, default=None, help="End graph index inclusive.")
    return parser.parse_args()


def main():
    args = parse_args()
    graphs = torch.load(args.graph_pt, weights_only=False)
    end_index = len(graphs) - 1 if args.end_index is None else min(args.end_index, len(graphs) - 1)

    model = GATModel()
    state_dict = torch.load(args.model_path, weights_only=False)
    model.load_state_dict(state_dict)
    model.eval()

    prediction_rows = []
    attention_rows = []

    for graph in graphs[args.start_index : end_index + 1]:
        batch_graph = as_single_graph_batch(graph)
        out, hg, attn_weights = model(batch_graph)
        out_probs = torch.sigmoid(out).detach().cpu().numpy()

        prediction_rows.append(
            {
                "cpm_id": graph.cpm_id,
                **{f"Class_{j + 1}": format_value(value) for j, value in enumerate(out_probs.flatten())},
                **{f"hg_{j + 1}": format_value(value) for j, value in enumerate(hg.detach().cpu().numpy().flatten())},
            }
        )

        edge_dict = {}
        node_names = graph.node_names

        for layer_index, (edge_index, attention_weight) in enumerate(attn_weights, start=1):
            edge_index_np = edge_index.detach().cpu().numpy().T
            attention_np = attention_weight.detach().cpu().numpy()

            for edge, attention_values in zip(edge_index_np, attention_np):
                source_index, target_index = edge
                source_name = node_names[int(source_index)]
                target_name = node_names[int(target_index)]
                edge_key = (source_name, target_name)

                if edge_key not in edge_dict:
                    edge_dict[edge_key] = {
                        "cpm_id": graph.cpm_id,
                        "Source": source_name,
                        "Target": target_name,
                    }

                for head_index, attention_value in enumerate(attention_values, start=1):
                    edge_dict[edge_key][f"attn_weights_{layer_index}_head_{head_index}"] = format_value(
                        attention_value
                    )

        attention_rows.extend(edge_dict.values())

    prediction_output_path = Path(args.prediction_output)
    attention_output_path = Path(args.attention_output)
    prediction_output_path.parent.mkdir(parents=True, exist_ok=True)
    attention_output_path.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(prediction_rows).to_csv(prediction_output_path, sep="\t", index=False)
    pd.DataFrame(attention_rows).to_csv(attention_output_path, sep="\t", index=False)

    print(f"Prediction outputs written to {prediction_output_path}")
    print(f"Attention weights written to {attention_output_path}")


if __name__ == "__main__":
    main()
