"""腾讯视频离线爬虫示例。

真实接口在当前环境不可用，因此这里提供可扩展的离线数据源和与线上
实现一致的 API，便于后续替换网络请求逻辑。
"""

from __future__ import annotations

import itertools
from typing import Iterable, List, MutableMapping

from video_crawler import OfflineRequestModule, StorageModule, VideoRecord


class TencentVideoCrawler:
    """生成示例数据，模拟“免费视频”多页抓取。"""

    _SAMPLE_ROWS: List[MutableMapping] = [
        {
            "title": "示例·科幻大片",  # 使用中文便于和 README 对齐
            "cover_url": "https://v.qq.com/sample/scifi.jpg",
            "desc": "演示自动分页、去重、存储等流程。",
            "owner": "腾讯视频",
            "play": 1023920,
            "danmaku": 5523,
            "publish_time": "2024-08-08",
            "video_id": "tv_demo_001",
        },
        {
            "title": "示例·热门综艺",
            "cover_url": "https://v.qq.com/sample/variety.jpg",
            "desc": "模拟从 HTML/JS 混合数据中解析元数据。",
            "owner": "企鹅出品",
            "play": 832111,
            "danmaku": 4211,
            "publish_time": "2024-05-19",
            "video_id": "tv_demo_002",
        },
    ]

    def __init__(self, output_format: str = "json", storage: StorageModule | None = None):
        self.output_format = output_format
        self.storage = storage or StorageModule()
        self.request = OfflineRequestModule({row["video_id"]: row for row in self._SAMPLE_ROWS})

    def crawl(self, pages: int = 1) -> List[MutableMapping]:
        """模拟分页抓取。

        每一页重复示例数据，并为 ``page`` 字段打标，方便验证分页逻辑。
        """

        records: List[MutableMapping] = []
        for page in range(1, max(1, pages) + 1):
            for row in self._SAMPLE_ROWS:
                record = VideoRecord(
                    platform="tencent",
                    title=row["title"],
                    video_id=row["video_id"],
                    cover_url=row["cover_url"],
                    desc=row["desc"],
                    owner=row["owner"],
                    play=row["play"],
                    danmaku=row["danmaku"],
                    publish_time=row["publish_time"],
                ).__dict__
                record["page"] = page
                records.append(record)
        return records

    def get_by_id(self, video_id: str) -> MutableMapping:
        payload = self.request.get(video_id)
        return VideoRecord(
            platform="tencent",
            title=payload["title"],
            video_id=payload["video_id"],
            cover_url=payload["cover_url"],
            desc=payload["desc"],
            owner=payload["owner"],
            play=payload["play"],
            danmaku=payload["danmaku"],
            publish_time=payload["publish_time"],
        ).__dict__

    def save(self, data: Iterable[MutableMapping], path: str):
        path = str(path)
        if self.output_format == "csv":
            return self.storage.save_csv(data, path)
        return self.storage.save_json(data, path)
