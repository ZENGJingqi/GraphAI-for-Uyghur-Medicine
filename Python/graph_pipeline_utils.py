from pathlib import Path
from typing import Iterable, Optional

import networkx as nx
import pandas as pd
import torch
import torch.nn as nn
from torch_geometric.data import Batch
from torch_geometric.nn import GATConv, global_mean_pool
from torch_geometric.utils import from_networkx


VIRTUAL_NODES = [
    "Dry therapeutic",
    "Moist therapeutic",
    "Cold therapeutic",
    "Hot therapeutic",
]


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def calculate_weighted_features(
    graph: nx.MultiGraph,
    connected_nodes: Iterable[str],
    virtual_node_name: str,
    feature_template,
):
    weighted_features = [0.0] * len(feature_template)
    total_weight = 0.0

    for node in connected_nodes:
        node_features = graph.nodes[node]["feature"]
        edge_data = graph.get_edge_data(node, virtual_node_name)
        for edge_key in edge_data:
            edge_attr = edge_data[edge_key]["attr"]
            for value in edge_attr:
                weighted_features = [wf + feature * value for wf, feature in zip(weighted_features, node_features)]
                total_weight += value

    return weighted_features, total_weight


def update_virtual_node_features(graph: nx.MultiGraph, feature_template):
    for virtual_node_name in VIRTUAL_NODES:
        connected_nodes = [
            node for node in graph.neighbors(virtual_node_name) if graph.nodes[node]["type"] == "Actual"
        ]
        if not connected_nodes:
            continue

        initial_features = graph.nodes[virtual_node_name]["feature"]
        weighted_features, total_weight = calculate_weighted_features(
            graph, connected_nodes, virtual_node_name, feature_template
        )
        if total_weight == 0:
            continue

        updated_features = [value / total_weight for value in weighted_features]
        graph.nodes[virtual_node_name]["feature"] = [
            (updated + initial) / 2 for updated, initial in zip(updated_features, initial_features)
        ]


def calculate_initial_edge_attributes(graph: nx.MultiGraph):
    initial_edge_attrs = []
    for virtual_node_name in VIRTUAL_NODES:
        for node in graph.neighbors(virtual_node_name):
            if graph.nodes[node]["type"] != "Actual":
                continue
            edge_data = graph.get_edge_data(node, virtual_node_name)
            for edge_key in edge_data:
                initial_edge_attrs.append(edge_data[edge_key]["attr"])

    if not initial_edge_attrs:
        return [0.0]

    return [sum(values) / len(initial_edge_attrs) for values in zip(*initial_edge_attrs)]


def convert_to_pyg_graph(graph: nx.MultiDiGraph):
    pyg_graph = from_networkx(graph)
    pyg_graph.x = torch.tensor([graph.nodes[node]["feature"] for node in graph.nodes], dtype=torch.float)
    pyg_graph.edge_attr = torch.tensor([graph.edges[edge]["attr"] for edge in graph.edges], dtype=torch.float)
    pyg_graph.node_types = [graph.nodes[node]["type"] for node in graph.nodes]
    return pyg_graph


def build_single_graph(cpm_id, relation_data, properties_data, encoder_data, label_df: Optional[pd.DataFrame] = None):
    cpm_data = relation_data[relation_data["CPM_ID"] == cpm_id].copy()
    chp_ids = cpm_data["CHP_ID"].unique()
    chp_encoder = encoder_data[encoder_data["CHP_ID"].isin(chp_ids)].copy()

    if chp_encoder.empty:
        raise ValueError(f"No encoder rows found for CPM_ID={cpm_id}")

    graph = nx.MultiGraph()
    feature_template = None

    for _, row in chp_encoder.iterrows():
        chp_id = row["CHP_ID"]
        chp_attr = row.iloc[1:].tolist()
        dosage_ratio = cpm_data.loc[cpm_data["CHP_ID"] == chp_id, "Dosage_ratio"]
        dosage_ratio = pd.to_numeric(dosage_ratio, errors="coerce").fillna(0).iloc[0]
        chp_attr.append(float(dosage_ratio))
        feature_template = chp_attr.copy()
        graph.add_node(chp_id, feature=chp_attr, type="Actual", name=chp_id)

    if feature_template is None:
        raise ValueError(f"Failed to create node features for CPM_ID={cpm_id}")

    for virtual_node_name in VIRTUAL_NODES:
        graph.add_node(
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
            graph.add_edge(chp_id, "Cold therapeutic", attr=default_level)
            graph.add_edge(chp_id, "Hot therapeutic", attr=default_level)
            continue

        for _, row in chp_rows.iterrows():
            graph.add_edge(chp_id, row["Medicinal_properties"], attr=[float(row["Level"])])

    update_virtual_node_features(graph, feature_template)
    initial_edge_attrs = calculate_initial_edge_attributes(graph)

    for i, source in enumerate(VIRTUAL_NODES):
        for j, target in enumerate(VIRTUAL_NODES):
            if i >= j:
                continue
            if {source, target} in (
                {"Dry therapeutic", "Moist therapeutic"},
                {"Cold therapeutic", "Hot therapeutic"},
            ):
                continue
            graph.add_edge(source, target, attr=initial_edge_attrs)

    directed_graph = graph.to_directed()
    for source, target, key, edge_data in directed_graph.edges(keys=True, data=True):
        if "attr" in edge_data:
            directed_graph.edges[target, source, key]["attr"] = edge_data["attr"]

    pyg_graph = convert_to_pyg_graph(directed_graph)
    pyg_graph.node_names = [directed_graph.nodes[node]["name"] for node in directed_graph.nodes]
    pyg_graph.cpm_id = cpm_id

    if label_df is not None:
        label_row = label_df.loc[label_df["CPM_ID"] == cpm_id]
        if label_row.empty:
            raise ValueError(f"No label row found for CPM_ID={cpm_id}")
        label_values = label_row[["Class_1", "Class_2", "Class_3", "Class_4"]].iloc[0].astype(float).tolist()
        pyg_graph.y = torch.tensor(label_values, dtype=torch.float)

    return pyg_graph


def load_encoder_data(encoder_tsv: Path):
    encoder_data = pd.read_csv(encoder_tsv, sep="\t")
    encoder_data.iloc[:, 1:] = encoder_data.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")
    return encoder_data


def load_property_data(properties_tsv: Path):
    return pd.read_csv(properties_tsv, sep="\t")


def format_value(value):
    return round(float(value), 4)


def as_single_graph_batch(graph):
    if getattr(graph, "batch", None) is None:
        return Batch.from_data_list([graph])
    return graph


class GATModel(nn.Module):
    def __init__(self, in_dim=91, hidden_dim=64, out_dim=4, num_heads=2, dropout_rate=0.4, dosage_weight=1.0):
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
