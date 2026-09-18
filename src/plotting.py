"""Leader-owned plotting helpers.

Contributor notebooks should create their own analysis-specific figures.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_rating_distribution(counts: pd.DataFrame) -> plt.Figure:
    """Plot the dataset-level rating distribution owned by the leader."""

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(counts["rating"].astype(str), counts["count"], color="#35618d")
    ax.set_title("MovieLens rating distribution")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Number of ratings")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    return fig


def save_figure(fig: plt.Figure, path: str | Path, *, dpi: int = 150) -> Path:
    """Save a figure to a project-relative output path."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
    return output_path
