"""Offline-friendly B站爬虫示例。

由于运行环境无法直接访问外网，这个实现通过预置的数据集来模拟 B 站
接口返回的数据结构，并暴露出与真实爬虫一致的 API，方便后续替换为真
实的网络请求逻辑。
"""

from __future__ import annotations

import datetime as _dt
import re
from typing import Dict, Iterable, List, MutableMapping, Sequence

from video_crawler import OfflineRequestModule, StorageModule, VideoRecord


class BilibiliCrawler:
    """采集 B 站视频元数据的简易版本。

    - ``get_video_info``：根据 BV 号返回视频详情
    - ``search``：在离线样本中按关键字搜索
    - ``save``：将数据写入 JSON / CSV
    """

    _SAMPLE_DATA: Dict[str, MutableMapping] = {
        "BV1xx411c7mD": {
            "title": "离线环境示例：如何构建可靠的爬虫",  # 保留中文示例标题
            "owner": "demo_up",
            "desc": "演示在无法联网的环境下如何构建可替换的爬虫骨架。",
            "pic": "https://i0.hdslb.com/bfs/archive/demo.jpg",
            "stat": {"view": 390231, "danmaku": 10293},
            "pubdate": "2024-11-19",
        },
        "BV19b411c7Py": {
            "title": "多线程爬虫优化实战",
            "owner": "dev_log",
            "desc": "记录多线程队列、限速和重试策略的最佳实践。",
            "pic": "https://i0.hdslb.com/bfs/archive/demo2.jpg",
            "stat": {"view": 120003, "danmaku": 6311},
            "pubdate": "2024-10-02",
        },
    }

    def __init__(self, storage: StorageModule | None = None):
        self.storage = storage or StorageModule()
        self.request = OfflineRequestModule(self._SAMPLE_DATA)

    def get_video_info(self, bvid: str) -> MutableMapping:
        """返回与 README 示例兼容的元数据字典。"""

        payload = self.request.get(bvid)
        return self._to_record(bvid, payload)

    def search(self, keyword: str, limit: int = 5) -> List[MutableMapping]:
        """在离线样本中模糊匹配标题/简介。"""

        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        results: List[MutableMapping] = []
        for bvid, payload in self._SAMPLE_DATA.items():
            if pattern.search(payload["title"]) or pattern.search(payload["desc"]):
                results.append(self._to_record(bvid, payload))
            if len(results) >= limit:
                break
        return results

    def save_json(self, data: Iterable[MutableMapping], path: str):
        return self.storage.save_json(data, path)

    def save_csv(self, data: Iterable[MutableMapping], path: str):
        return self.storage.save_csv(data, path)

    def _to_record(self, bvid: str, payload: MutableMapping) -> MutableMapping:
        record = VideoRecord(
            platform="bilibili",
            title=payload["title"],
            video_id=bvid,
            cover_url=payload["pic"],
            desc=payload["desc"],
            owner=payload["owner"],
            play=int(payload.get("stat", {}).get("view", 0)),
            danmaku=int(payload.get("stat", {}).get("danmaku", 0)),
            publish_time=payload.get(
                "pubdate", _dt.date.today().isoformat()
            ),
        )
        return record.__dict__
