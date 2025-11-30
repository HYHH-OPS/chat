"""Shared utilities for the offline video crawler examples.

The real crawler endpoints are blocked in this execution environment, so this
module focuses on reusable helpers (storage + synthetic fetchers) that the
platform-specific crawlers can share. Keeping the helpers in one place keeps the
example small while still mirroring a production-style layout.
"""

from __future__ import annotations

import csv
import datetime as _dt
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, List, MutableMapping


@dataclass
class VideoRecord:
    """Normalized record used by all crawlers.

    The fields align with the README examples. Additional keys can be appended
    when writing CSV/JSON because ``asdict`` is not required; a plain mapping is
    accepted by the storage helpers.
    """

    platform: str
    title: str
    video_id: str
    cover_url: str
    desc: str
    owner: str
    play: int
    danmaku: int
    publish_time: str
    crawl_time: str = field(default_factory=lambda: _dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))


class StorageModule:
    """Helper that writes crawler output to disk.

    The helpers accept any iterable of mappings (including ``VideoRecord``
    dataclasses converted via ``.__dict__``). They keep the interface minimal so
    it is easy to swap in a real persistence layer later on.
    """

    def save_json(self, data: Iterable[MutableMapping], path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload: List[MutableMapping] = list(data)
        with path.open("w", encoding="utf-8") as fp:
            json.dump(payload, fp, ensure_ascii=False, indent=2)
        return path

    def save_csv(self, data: Iterable[MutableMapping], path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        rows: List[MutableMapping] = list(data)
        if not rows:
            path.write_text("", encoding="utf-8")
            return path

        fieldnames = list({key for row in rows for key in row.keys()})
        with path.open("w", newline="", encoding="utf-8") as fp:
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return path


class OfflineRequestModule:
    """A deterministic request layer used in place of network calls.

    The execution environment blocks outbound HTTP requests, so the crawlers use
    this class to provide predictable mock responses. It can easily be replaced
    with a real HTTP client in production without changing the public crawler
    APIs.
    """

    def __init__(self, offline_payloads: MutableMapping[str, MutableMapping]):
        self.offline_payloads = offline_payloads

    def get(self, key: str) -> MutableMapping:
        if key not in self.offline_payloads:
            raise KeyError(f"No offline payload registered for key '{key}'")
        return self.offline_payloads[key]
