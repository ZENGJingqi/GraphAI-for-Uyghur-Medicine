import argparse
from pathlib import Path

import pandas as pd
import torch

from graph_pipeline_utils import (
    build_single_graph,
    get_repo_root,
    load_encoder_data,
    load_property_data,
)


def parse_args():
    repo_root = get_repo_root()
    parser = argparse.ArgumentParser(
        description="Build the full labeled graph corpus for all prescriptions."
    )
    parser.add_argument(
        "--relation-tsv",
        default=str(repo_root / "Data" / "UHF_UHP.tsv"),
        help="Full prescription-to-herb relation table.",
    )
    parser.add_argument(
        "--label-csv",
        default=str(repo_root / "Data" / "UHF_Label_Matrix.csv"),
        help="English label matrix with Class_1..Class_4.",
    )
    parser.add_argument(
        "--encoder-tsv",
        default=str(repo_root / "Data" / "UHP_Encoder.tsv"),
        help="Herb-level encoded node features.",
    )
    parser.add_argument(
        "--properties-tsv",
        default=str(repo_root / "Data" / "UHP_Medicinal_properties_encode.tsv"),
        help="Herb-to-property edge table.",
    )
    parser.add_argument(
        "--output-pt",
        default=str(repo_root / "Data" / "rebuilt_full_corpus_graphs_with_labels.pt"),
        help="Output PT file for a rebuilt full labeled corpus used for verification.",
    )
    parser.add_argument(
        "--legacy-order-pt",
        default=str(repo_root / "Data" / "full_prescription_graphs_with_labels.pt"),
        help="Stored PT file used only to preserve the original stored CPM_ID order.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    relation_df = pd.read_csv(args.relation_tsv, sep="\t")
    label_df = pd.read_csv(args.label_csv)
    encoder_data = load_encoder_data(Path(args.encoder_tsv))
    property_data = load_property_data(Path(args.properties_tsv))

    graphs = []
    legacy_order_path = Path(args.legacy_order_pt)
    if legacy_order_path.exists():
        legacy_graphs = torch.load(legacy_order_path, weights_only=False)
        ordered_cpm_ids = [graph.cpm_id for graph in legacy_graphs]
    else:
        ordered_cpm_ids = relation_df["CPM_ID"].drop_duplicates().tolist()

    for cpm_id in ordered_cpm_ids:
        graph = build_single_graph(cpm_id, relation_df, property_data, encoder_data, label_df)
        graphs.append(graph)

    output_path = Path(args.output_pt)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(graphs, output_path)

    print(f"Saved {len(graphs)} full-corpus graphs to {output_path}")
    print(f"First CPM_ID: {graphs[0].cpm_id}")
    print(f"Label dimension: {graphs[0].y.shape[0]}")


if __name__ == "__main__":
    main()
