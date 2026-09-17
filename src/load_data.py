"""MovieLens data discovery, loading, and data-quality summaries.

The course dataset is intentionally not committed to this repository because
the full MovieLens-20M download is large.  The loader accepts either the
download directory itself or a parent directory containing ``ml-20m``.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Mapping

import pandas as pd


REQUIRED_FILES = ("ratings.csv", "movies.csv")
OPTIONAL_FILES = (
    "tags.csv",
    "links.csv",
    "genome-scores.csv",
    "genome-tags.csv",
)


def _candidate_directories(raw_path: Path) -> list[Path]:
    """Return plausible MovieLens directories in priority order."""

    candidates = [raw_path]
    if raw_path.name.lower() not in {"ml-20m", "movielens-20m"}:
        candidates.extend([raw_path / "ml-20m", raw_path / "MovieLens-20M"])
    return candidates


def resolve_data_dir(data_dir: str | os.PathLike[str] | None = None) -> Path:
    """Resolve a directory containing at least ``ratings.csv`` and ``movies.csv``.

    ``MOVIELENS_DATA_DIR`` can be used to keep notebooks independent of a
    machine-specific absolute path.  Relative paths are interpreted from the
    current working directory, which is the usual project root when running a
    notebook or script.
    """

    raw_value = data_dir or os.environ.get("MOVIELENS_DATA_DIR") or "data/ml-20m"
    raw_path = Path(raw_value).expanduser()
    if not raw_path.is_absolute():
        raw_path = Path.cwd() / raw_path

    for candidate in _candidate_directories(raw_path):
        if all((candidate / filename).is_file() for filename in REQUIRED_FILES):
            return candidate.resolve()

    expected = ", ".join(REQUIRED_FILES)
    raise FileNotFoundError(
        f"Could not find MovieLens data under {raw_path}. Expected at least: {expected}. "
        "Download MovieLens-20M and set MOVIELENS_DATA_DIR to its extracted folder."
    )


def load_movielens(
    data_dir: str | os.PathLike[str] | None = None,
    *,
    include_optional: bool = True,
) -> dict[str, pd.DataFrame]:
    """Load available MovieLens CSV files into a named dictionary.

    The two core files are required.  Optional files are loaded when present;
    this makes the baseline EDA usable even before tags/genome files are added.
    """

    resolved_dir = resolve_data_dir(data_dir)
    filenames = list(REQUIRED_FILES)
    if include_optional:
        filenames.extend(OPTIONAL_FILES)

    frames: dict[str, pd.DataFrame] = {}
    for filename in filenames:
        path = resolved_dir / filename
        if path.is_file():
            frames[path.stem] = pd.read_csv(path, low_memory=False)
    frames["_data_dir"] = resolved_dir  # type: ignore[assignment]
    return frames


def summarize_frames(frames: Mapping[str, pd.DataFrame]) -> pd.DataFrame:
    """Create the required file-level quality summary table."""

    rows: list[dict[str, object]] = []
    for name, frame in frames.items():
        if not isinstance(frame, pd.DataFrame):
            continue
        rows.append(
            {
                "file": f"{name}.csv",
                "n_rows": int(frame.shape[0]),
                "n_columns": int(frame.shape[1]),
                "missing_cells": int(frame.isna().sum().sum()),
                "duplicate_rows": int(frame.duplicated().sum()),
                "memory_mb": round(
                    frame.memory_usage(index=True, deep=True).sum() / (1024**2), 3
                ),
            }
        )
    return pd.DataFrame(
        rows,
        columns=[
            "file",
            "n_rows",
            "n_columns",
            "missing_cells",
            "duplicate_rows",
            "memory_mb",
        ],
    ).sort_values("file", ignore_index=True)

