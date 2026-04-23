import argparse
import random
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import accuracy_score, auc, confusion_matrix, f1_score, precision_recall_fscore_support, recall_score, roc_curve
from sklearn.model_selection import train_test_split
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch_geometric.loader import DataLoader

from graph_pipeline_utils import GATModel, get_repo_root


def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


class EarlyStopping:
    def __init__(self, patience=3, min_delta=0.001):
        self.patience = patience
        self.min_delta = min_delta
        self.best_loss = float("inf")
        self.counter = 0

    def check_early_stop(self, value):
        if self.best_loss - value > self.min_delta:
            self.best_loss = value
            self.counter = 0
        else:
            self.counter += 1
        return self.counter >= self.patience


def parse_args():
    repo_root = get_repo_root()
    parser = argparse.ArgumentParser(
        description="Train or evaluate the GAT model on the full labeled corpus."
    )
    parser.add_argument(
        "--graph-pt",
        default=str(repo_root / "Data" / "full_prescription_graphs_with_labels.pt"),
        help="PT file containing the full labeled corpus.",
    )
    parser.add_argument(
        "--mode",
        choices=["train", "evaluate-existing"],
        default="evaluate-existing",
        help="Train a new model or evaluate the existing stored model.",
    )
    parser.add_argument(
        "--model-path",
        default=str(repo_root / "Data" / "gat_model.pth"),
        help="Output path for training mode or input path for evaluate-existing mode.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(repo_root / "Data" / "english_training_outputs"),
        help="Directory for exported metrics.",
    )
    parser.add_argument("--epochs", type=int, default=30, help="Maximum number of epochs.")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size.")
    parser.add_argument("--learning-rate", type=float, default=0.0003, help="Learning rate.")
    parser.add_argument("--validation-size", type=float, default=0.33, help="Validation split ratio.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    return parser.parse_args()


def split_graphs(graphs, validation_size, seed):
    labels = np.array([graph.y.numpy() if isinstance(graph.y, torch.Tensor) else graph.y for graph in graphs])
    train_graphs, val_graphs, train_labels, val_labels = train_test_split(
        graphs, labels, test_size=validation_size, random_state=seed, shuffle=True
    )
    return train_graphs, val_graphs, torch.tensor(train_labels, dtype=torch.float), torch.tensor(val_labels, dtype=torch.float)


def attach_labels(graphs, labels):
    for graph, label in zip(graphs, labels):
        graph.y = label
    return graphs


def create_batches(graphs, labels, batch_size, shuffle):
    labeled_graphs = attach_labels(graphs, labels)
    return DataLoader(labeled_graphs, batch_size=batch_size, shuffle=shuffle)


def evaluate_loader(loader, model, loss_fn):
    model.eval()
    total_loss = 0.0
    all_outputs = []
    all_labels = []

    with torch.no_grad():
        for batch in loader:
            outputs, _, _ = model(batch)
            batch_labels = batch.y.view(outputs.shape)
            loss = loss_fn(outputs, batch_labels)
            total_loss += loss.item()
            all_outputs.append(outputs.cpu().numpy())
            all_labels.append(batch_labels.cpu().numpy())

    outputs = np.vstack(all_outputs)
    labels = np.vstack(all_labels)
    probabilities = torch.sigmoid(torch.tensor(outputs)).numpy()
    predictions = (probabilities > 0.5).astype(int)

    average_loss = total_loss / len(loader)
    micro_recall = recall_score(labels, predictions, average="micro")
    micro_f1 = f1_score(labels, predictions, average="micro")

    return average_loss, micro_recall, micro_f1, labels, probabilities


def compute_metrics_table(labels, probabilities):
    records = []
    for class_index in range(labels.shape[1]):
        binary_predictions = (probabilities[:, class_index] > 0.5).astype(int)
        precision, recall, f1, _ = precision_recall_fscore_support(
            labels[:, class_index], binary_predictions, average="binary", zero_division=0
        )
        accuracy = accuracy_score(labels[:, class_index], binary_predictions)
        tn, fp, fn, tp = confusion_matrix(labels[:, class_index], binary_predictions).ravel()
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
        fpr, tpr, _ = roc_curve(labels[:, class_index], probabilities[:, class_index])
        roc_auc = auc(fpr, tpr)

        records.append(
            {
                "Class": f"Class_{class_index + 1}",
                "Precision": precision,
                "Recall": recall,
                "F1 Score": f1,
                "AUC": roc_auc,
                "Accuracy": accuracy,
                "Specificity": specificity,
            }
        )

    metrics_df = pd.DataFrame(records)
    metrics_df.loc[len(metrics_df)] = {
        "Class": "Average",
        "Precision": metrics_df["Precision"].mean(),
        "Recall": metrics_df["Recall"].mean(),
        "F1 Score": metrics_df["F1 Score"].mean(),
        "AUC": metrics_df["AUC"].mean(),
        "Accuracy": metrics_df["Accuracy"].mean(),
        "Specificity": metrics_df["Specificity"].mean(),
    }
    return metrics_df


def export_metrics(output_dir: Path, prefix: str, labels, probabilities):
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_df = compute_metrics_table(labels, probabilities)
    metrics_df.to_csv(output_dir / f"{prefix}_metrics.csv", index=False)

    roc_rows = []
    for class_index in range(labels.shape[1]):
        for reference, predicted in zip(labels[:, class_index], probabilities[:, class_index]):
            roc_rows.append(
                {
                    "Class": f"Class_{class_index + 1}",
                    "Reference": reference,
                    "Predicted": predicted,
                }
            )
    pd.DataFrame(roc_rows).to_csv(output_dir / f"{prefix}_roc_data.csv", index=False)
    return metrics_df


def train_model(train_loader, val_loader, model, optimizer, scheduler, loss_fn, epochs):
    early_stopping = EarlyStopping(patience=3)

    for epoch in range(epochs):
        model.train()
        total_loss = 0.0

        for batch in train_loader:
            outputs, _, _ = model(batch)
            batch_labels = batch.y.view(outputs.shape)
            loss = loss_fn(outputs, batch_labels)

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            total_loss += loss.item()

        train_loss = total_loss / len(train_loader)
        val_loss, val_recall, val_f1, _, _ = evaluate_loader(val_loader, model, loss_fn)
        scheduler.step(val_loss)
        print(
            f"Epoch {epoch + 1}/{epochs} | train_loss={train_loss:.4f} | "
            f"val_loss={val_loss:.4f} | val_recall={val_recall:.4f} | val_f1={val_f1:.4f}"
        )

        if early_stopping.check_early_stop(val_loss):
            print(f"Early stopping at epoch {epoch + 1}")
            break


def main():
    args = parse_args()
    set_seed(args.seed)

    graphs = torch.load(args.graph_pt, weights_only=False)
    train_graphs, val_graphs, train_labels, val_labels = split_graphs(graphs, args.validation_size, args.seed)

    pos_counts = train_labels.sum(dim=0)
    neg_counts = train_labels.size(0) - pos_counts
    pos_weight = neg_counts / (pos_counts + 1e-6)
    loss_fn = nn.BCEWithLogitsLoss(pos_weight=pos_weight)

    model = GATModel()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.mode == "train":
        train_loader = create_batches(train_graphs, train_labels, args.batch_size, shuffle=True)
        val_loader = create_batches(val_graphs, val_labels, args.batch_size, shuffle=False)
        optimizer = optim.Adam(model.parameters(), lr=args.learning_rate, weight_decay=1e-4)
        scheduler = ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=1)
        train_model(train_loader, val_loader, model, optimizer, scheduler, loss_fn, args.epochs)
        torch.save(model.state_dict(), args.model_path)
        print(f"Saved trained model to {args.model_path}")
    else:
        state_dict = torch.load(args.model_path, weights_only=False)
        model.load_state_dict(state_dict)
        print(f"Loaded existing model from {args.model_path}")

    train_loader = create_batches(train_graphs, train_labels, args.batch_size, shuffle=False)
    val_loader = create_batches(val_graphs, val_labels, args.batch_size, shuffle=False)
    train_loss, train_recall, train_f1, train_truth, train_prob = evaluate_loader(train_loader, model, loss_fn)
    val_loss, val_recall, val_f1, val_truth, val_prob = evaluate_loader(val_loader, model, loss_fn)

    train_metrics = export_metrics(output_dir, "train", train_truth, train_prob)
    val_metrics = export_metrics(output_dir, "validation", val_truth, val_prob)

    print(
        f"Train summary | loss={train_loss:.4f} | recall={train_recall:.4f} | f1={train_f1:.4f}"
    )
    print(
        f"Validation summary | loss={val_loss:.4f} | recall={val_recall:.4f} | f1={val_f1:.4f}"
    )
    print(train_metrics.to_string(index=False))
    print(val_metrics.to_string(index=False))


if __name__ == "__main__":
    main()
