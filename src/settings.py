"""Shared paths and public-safe settings for the capstone project."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
SAMPLE_DATA_DIR = DATA_DIR / "sample"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUT_DIR = DATA_DIR / "output"


@dataclass(frozen=True)
class DatabaseSettings:
    host: str
    port: int
    user: str
    password: str
    name: str
    schema: str = "public"

    @property
    def configured(self) -> bool:
        return all([self.host, self.user, self.password, self.name])


def database_settings_from_env() -> DatabaseSettings:
    """Read optional database settings without requiring a secret CSV file."""

    return DatabaseSettings(
        host=os.getenv("WEB3_LEADS_DB_HOST", "").strip(),
        port=int(os.getenv("WEB3_LEADS_DB_PORT", "5432") or "5432"),
        user=os.getenv("WEB3_LEADS_DB_USER", "").strip(),
        password=os.getenv("WEB3_LEADS_DB_PASSWORD", "").strip(),
        name=os.getenv("WEB3_LEADS_DB_NAME", "").strip(),
        schema=os.getenv("WEB3_LEADS_DB_SCHEMA", "public").strip() or "public",
    )


def ensure_runtime_dirs() -> None:
    for path in (RAW_DATA_DIR, PROCESSED_DATA_DIR, OUTPUT_DIR):
        path.mkdir(parents=True, exist_ok=True)
