import argparse
from pathlib import Path

import pandas as pd

from graph_pipeline_utils import get_repo_root


CLASS_NAME_MAP = {
    "Generate dryness and cold": "Class_1",
    "Generate dryness and heat": "Class_2",
    "Generate moisture and cold": "Class_3",
    "Generate moisture and heat": "Class_4",
}


def parse_args():
    repo_root = get_repo_root()
    parser = argparse.ArgumentParser(
        description="Build an English label matrix for all prescriptions in the full corpus."
    )
    parser.add_argument(
        "--relation-tsv",
        default=str(repo_root / "Data" / "UHF_UHP.tsv"),
        help="Full prescription-to-herb relation table.",
    )
    parser.add_argument(
        "--cluster-csv",
        default=str(repo_root / "Data" / "UHF_Cluster_Dummies_Unique.csv"),
        help="Original cluster dummy file from the legacy workflow.",
    )
    parser.add_argument(
        "--output-csv",
        default=str(repo_root / "Data" / "UHF_Label_Matrix.csv"),
        help="Output CSV with CPM_ID and Class_1..Class_4.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    relation_df = pd.read_csv(args.relation_tsv, sep="\t")
    cluster_df = pd.read_csv(args.cluster_csv)

    label_df = cluster_df.rename(columns=CLASS_NAME_MAP)
    label_df = label_df[["CPM_ID", "Class_1", "Class_2", "Class_3", "Class_4"]].copy()
    for column in ["Class_1", "Class_2", "Class_3", "Class_4"]:
        label_df[column] = label_df[column].astype(int)

    full_cpm_ids = relation_df["CPM_ID"].drop_duplicates().to_frame()
    full_label_df = full_cpm_ids.merge(label_df, on="CPM_ID", how="left")
    full_label_df[["Class_1", "Class_2", "Class_3", "Class_4"]] = full_label_df[
        ["Class_1", "Class_2", "Class_3", "Class_4"]
    ].fillna(0).astype(int)

    output_path = Path(args.output_csv)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    full_label_df.to_csv(output_path, index=False)

    missing_ids = full_label_df.loc[
        (full_label_df[["Class_1", "Class_2", "Class_3", "Class_4"]] == 0).all(axis=1), "CPM_ID"
    ]
    legacy_ids = set(cluster_df["CPM_ID"])
    missing_from_cluster = [cpm_id for cpm_id in missing_ids if cpm_id not in legacy_ids]

    print(f"Saved label matrix to {output_path}")
    print(f"Total prescriptions: {len(full_label_df)}")
    print(f"Rows originally missing from cluster file and filled with zeros: {len(missing_from_cluster)}")
    if missing_from_cluster:
        print("Filled CPM_IDs:", missing_from_cluster)


if __name__ == "__main__":
    main()
