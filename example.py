"""快速演示离线爬虫的用法。"""

from bilibili_crawler import BilibiliCrawler
from tencent_video_crawler import TencentVideoCrawler


if __name__ == "__main__":
    # B 站：按 BV 号读取
    bili = BilibiliCrawler()
    video = bili.get_video_info("BV1xx411c7mD")
    print("B 站示例:", video)

    # B 站：按关键词搜索
    print("搜索“爬虫”:", bili.search("爬虫"))

    # 腾讯视频：分页抓取示例
    tencent = TencentVideoCrawler(output_format="json")
    dataset = tencent.crawl(pages=2)
    print("腾讯视频示例共", len(dataset), "条")

    # 将结果写入本地
    tencent.save(dataset, "output/tencent_samples.json")
    bili.save_json([video], "output/bilibili_single.json")
    bili.save_csv(bili.search("爬虫"), "output/bilibili_search.csv")
    print("数据已写入 output/ 目录")
