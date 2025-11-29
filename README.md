# 🎬 腾讯视频 + B站双平台爬虫

本项目是一个 **支持腾讯视频免费爬取 + B站公开数据采集** 的双平台视频元数据采集爬虫框架，具有高稳定性、强抗封锁、可扩展性强等特点。

---

## 🚀 功能特性

### 🟦 1. 腾讯视频爬虫（Tencent Video Crawler）

* 自动识别“免费”视频
* 支持电影 / 电视剧 / 动漫 / 综艺多分类批量采集
* 自适应页面变化的多层解析器
* 支持从 HTML + JS 数据中双模式解析

### 🟥 2. B站爬虫（Bilibili Crawler）

支持采集：

* 视频标题
* 封面图片
* UP 主
* 播放量
* 弹幕数量
* 简介
* 发布时间
  （使用官方 API + 页面解析双模式，增强稳定性）

---

## ⚡ 核心能力升级

### 🧱 RequestModule（请求模块）

* 智能 UA 轮换
* 代理池权重系统（失败降权 / 成功加权）
* 健康检查系统
* 自动规避反爬机制
* 随机延迟 + 重试机制（指数退避）

### 🔍 ParserModule（解析模块）

* 多选择器自动 fallback
* 支持 JSON / JS 变量解析
* 自动识别视频 ID
* 针对腾讯/B站分别实现独立解析器

### 💾 StorageModule（存储模块）

* JSON/CSV 双格式
* 自动去重（基于 video_id）
* 增量爬取

### ⚙ TencentVideoCrawler（控制模块）

* 多线程并行采集
* 自动分页
* 增量爬取
* 自动合并历史数据

### 🎯 BilibiliCrawler（新增）

* 支持 BV 号解析
* 调用官方接口获取部分元数据
* 自动兼容 HTML 页面解析 fallback
* 与腾讯共享 RequestModule、StorageModule

---

## 📦 安装

```bash
pip install -r requirements.txt
```

---

## 🛠 使用示例

### ▶ 腾讯视频爬取

```python
from tencent_video_crawler import TencentVideoCrawler

crawler = TencentVideoCrawler(output_format="json")
videos = crawler.crawl(pages=2)

print("共爬取:", len(videos))
```

### ▶ B站爬取

```python
from bilibili_crawler import BilibiliCrawler

b = BilibiliCrawler()
video = b.get_video_info("BV1xx411c7mD")

print(video)
```

---

## 📁 输出示例（JSON）

```json
{
  "platform": "bilibili",
  "title": "B站视频标题",
  "bvid": "BVxxxx",
  "cover_url": "...",
  "desc": "...",
  "owner": "UP主昵称",
  "play": 390231,
  "danmaku": 10293,
  "publish_time": "2024-11-19",
  "crawl_time": "2025-02-10 20:33:21"
}
```

---

## 🧩 项目结构

```
📦 project
 ┣ 📜 tencent_video_crawler.py
 ┣ 📜 bilibili_crawler.py  ← 新增
 ┣ 📜 test_crawler.py
 ┣ 📜 config.json
 ┣ 📜 requirements.txt
 ┗ 📜 README.md
```

---

## 📝 更新日志

### v2.0（推荐升级）

* ✅ 支持 **B站完整视频解析**
* 🔥 RequestModule 加入高级反爬模型
* 🚀 腾讯视频解析器全面增强
* 🧠 多线程队列优化
* 📌 JSON/CSV 存储升级为可扩展字段系统
* 🛡 代理池变为「权重 + 健康系统」

---

## 🪪 License

MIT License

---

如需解析更多视频网站（如爱奇艺/优酷/抖音），可联系我扩展模块。
