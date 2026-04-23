import argparse
from pathlib import Path

import networkx as nx
import pandas as pd
import torch
from torch_geometric.utils import from_networkx


REQUIRED_INPUT_COLUMNS = {"CPM_ID", "CHP_ID", "Dosage_ratio"}
VIRTUAL_NODES = [
    "Dry therapeutic",
    "Moist therapeutic",
    "Cold therapeutic",
    "Hot therapeutic",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build PyG graphs for prescription prediction from an Excel input table."
    )
    parser.add_argument(
        "--input-excel",
        default="Data/example_prescription_input.xlsx",
        help="Excel file containing CPM_ID, CHP_ID, Dosage_ratio.",
    )
    parser.add_argument(
        "--encoder-tsv",
        default="Data/UHP_Encoder.tsv",
        help="TSV file containing herb-level encoded node features.",
    )
    parser.add_argument(
        "--properties-tsv",
        default="Data/UHP_Medicinal_properties_encode.tsv",
        help="TSV file containing medicinal property edges.",
    )
    parser.add_argument(
        "--output-pt",
        default="Data/prescriptions_to_predict.pt",
        help="Output PT file for unlabeled prediction graphs.",
    )
    return parser.parse_args()


def validate_input_table(data: pd.DataFrame) -> None:
    missing = REQUIRED_INPUT_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Missing required input columns: {sorted(missing)}")


def calculate_weighted_features(G, connected_nodes, virtual_node_name, feature_template):
    weighted_features = [0.0] * len(feature_template)
    total_weight = 0.0

    for node in connected_nodes:
        node_features = G.nodes[node]["feature"]
        edge_data = G.get_edge_data(node, virtual_node_name)
        for edge_key in edge_data:
            edge_attr = edge_data[edge_key]["attr"]
            for value in edge_attr:
                weighted_features = [wf + feature * value for wf, feature in zip(weighted_features, node_features)]
                total_weight += value

    return weighted_features, total_weight


def update_virtual_node_features(G, feature_template):
    for virtual_node_name in VIRTUAL_NODES:
        connected_nodes = [node for node in G.neighbors(virtual_node_name) if G.nodes[node]["type"] == "Actual"]
        if not connected_nodes:
            continue

        initial_features = G.nodes[virtual_node_name]["feature"]
        weighted_features, total_weight = calculate_weighted_features(
            G, connected_nodes, virtual_node_name, feature_template
        )
        if total_weight == 0:
            continue

        updated_features = [value / total_weight for value in weighted_features]
        G.nodes[virtual_node_name]["feature"] = [
            (updated + initial) / 2 for updated, initial in zip(updated_features, initial_features)
        ]


def calculate_initial_edge_attributes(G):
    initial_edge_attrs = []
    for virtual_node_name in VIRTUAL_NODES:
        for node in G.neighbors(virtual_node_name):
            if G.nodes[node]["type"] != "Actual":
                continue
            edge_data = G.get_edge_data(node, virtual_node_name)
            for edge_key in edge_data:
                initial_edge_attrs.append(edge_data[edge_key]["attr"])

    if not initial_edge_attrs:
        return [0.0]

    return [sum(values) / len(initial_edge_attrs) for values in zip(*initial_edge_attrs)]


def convert_to_pyg_graph(G: nx.MultiDiGraph):
    pyg_graph = from_networkx(G)
    pyg_graph.x = torch.tensor([G.nodes[node]["feature"] for node in G.nodes], dtype=torch.float)
    pyg_graph.edge_attr = torch.tensor([G.edges[edge]["attr"] for edge in G.edges], dtype=torch.float)
    pyg_graph.node_types = [G.nodes[node]["type"] for node in G.nodes]
    return pyg_graph


def build_single_graph(cpm_id, input_data, properties_data, encoder_data):
    cpm_data = input_data[input_data["CPM_ID"] == cpm_id].copy()
    chp_ids = cpm_data["CHP_ID"].unique()
    chp_encoder = encoder_data[encoder_data["CHP_ID"].isin(chp_ids)].copy()

    if chp_encoder.empty:
        raise ValueError(f"No encoder rows found for CPM_ID={cpm_id}")

    G = nx.MultiGraph()
    feature_template = None

    for _, row in chp_encoder.iterrows():
        chp_id = row["CHP_ID"]
        chp_attr = row.iloc[1:].tolist()
        dosage_ratio = cpm_data.loc[cpm_data["CHP_ID"] == chp_id, "Dosage_ratio"]
        dosage_ratio = pd.to_numeric(dosage_ratio, errors="coerce").fillna(0).iloc[0]
        chp_attr.append(dosage_ratio)
        feature_template = chp_attr.copy()
        G.add_node(chp_id, feature=chp_attr, type="Actual", name=chp_id)

    if feature_template is None:
        raise ValueError(f"Failed to create features for CPM_ID={cpm_id}")

    for virtual_node_name in VIRTUAL_NODES:
        G.add_node(
            virtual_node_name,
            feature=feature_template.copy(),
            type="Virtual",
            name=virtual_node_name,
        )

    chp_properties = properties_data[properties_data["CHP_ID"].isin(chp_ids)].copy()
    if not chp_properties.empty:
        chp_properties["Level"] = chp_properties["Level"].astype(float)

    for chp_id in chp_ids:
        chp_rows = chp_properties[chp_properties["CHP_ID"] == chp_id]
        if chp_rows.empty:
            default_level = [0.0]
            G.add_edge(chp_id, "Cold therapeutic", attr=default_level)
            G.add_edge(chp_id, "Hot therapeutic", attr=default_level)
            continue

        for _, row in chp_rows.iterrows():
            G.add_edge(chp_id, row["Medicinal_properties"], attr=[float(row["Level"])])

    update_virtual_node_features(G, feature_template)
    initial_edge_attrs = calculate_initial_edge_attributes(G)

    for i, source in enumerate(VIRTUAL_NODES):
        for j, target in enumerate(VIRTUAL_NODES):
            if i >= j:
                continue
            if {source, target} in (
                {"Dry therapeutic", "Moist therapeutic"},
                {"Cold therapeutic", "Hot therapeutic"},
            ):
                continue
            G.add_edge(source, target, attr=initial_edge_attrs)

    directed_graph = G.to_directed()
    for source, target, key, edge_data in directed_graph.edges(keys=True, data=True):
        if "attr" in edge_data:
            directed_graph.edges[target, source, key]["attr"] = edge_data["attr"]

    pyg_graph = convert_to_pyg_graph(directed_graph)
    pyg_graph.node_names = [directed_graph.nodes[node]["name"] for node in directed_graph.nodes]
    pyg_graph.cpm_id = cpm_id
    return pyg_graph


def main():
    args = parse_args()

    input_excel = Path(args.input_excel)
    encoder_tsv = Path(args.encoder_tsv)
    properties_tsv = Path(args.properties_tsv)
    output_pt = Path(args.output_pt)

    input_data = pd.read_excel(input_excel)
    validate_input_table(input_data)

    encoder_data = pd.read_csv(encoder_tsv, sep="\t")
    encoder_data.iloc[:, 1:] = encoder_data.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")
    properties_data = pd.read_csv(properties_tsv, sep="\t")

    graphs = []
    for cpm_id in input_data["CPM_ID"].drop_duplicates():
        graph = build_single_graph(cpm_id, input_data, properties_data, encoder_data)
        graphs.append(graph)

    output_pt.parent.mkdir(parents=True, exist_ok=True)
    torch.save(graphs, output_pt)

    print(f"Saved {len(graphs)} unlabeled prediction graphs to {output_pt}")
    print("CPM_IDs:", [graph.cpm_id for graph in graphs])


if __name__ == "__main__":
    main()
