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


REQUIRED_COLUMNS = {"CPM_ID", "CHP_ID", "Dosage_ratio"}


def parse_args():
    repo_root = get_repo_root()
    parser = argparse.ArgumentParser(
        description="Build unlabeled prediction graphs from a sample or user-provided Excel file."
    )
    parser.add_argument(
        "--input-excel",
        default=str(repo_root / "Data" / "sample_prescription_input.xlsx"),
        help="Excel file with CPM_ID, CHP_ID, Dosage_ratio.",
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
        default=str(repo_root / "Data" / "sample_prediction_graphs.pt"),
        help="Output PT file for sample prediction graphs.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_df = pd.read_excel(args.input_excel)
    missing_columns = REQUIRED_COLUMNS - set(input_df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    encoder_data = load_encoder_data(Path(args.encoder_tsv))
    property_data = load_property_data(Path(args.properties_tsv))

    graphs = []
    for cpm_id in input_df["CPM_ID"].drop_duplicates():
        graph = build_single_graph(cpm_id, input_df, property_data, encoder_data, label_df=None)
        graphs.append(graph)

    output_path = Path(args.output_pt)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(graphs, output_path)

    print(f"Saved {len(graphs)} sample prediction graphs to {output_path}")
    print("CPM_IDs:", [graph.cpm_id for graph in graphs])


if __name__ == "__main__":
    main()
