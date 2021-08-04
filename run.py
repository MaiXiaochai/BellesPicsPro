# -*- encoding: utf-8 -*-

"""
------------------------------------------
@File       : run.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2021/8/4 22:06
------------------------------------------
    整体思路:
            1）先解析出单套写真的图片地址
            2）然后下载图片
"""
from concurrent.futures import ThreadPoolExecutor

from utils import log, cfg
from workers import albums_parser, album_full_pics_parser, save_pics


def downloader(url):
    """
        单个写真合集下载
    """
    data = album_full_pics_parser(url)
    save_pics(data)


def multi_pics():
    # 单个品类链接，这里用秀人网的链接做测试
    base_url = "https://www.ku137.net/b/9/list_9_{}.html"

    with ThreadPoolExecutor(cfg.pool_size) as pool:

        for no in range(1, 130):
            # 单个写真集列表页
            url = base_url.format(no)

            for albums_no, albums_url in enumerate(albums_parser(url), 1):
                # 单个写真集页面
                pic_data = album_full_pics_parser(albums_url)

                for pic_no, pic_item in enumerate(pic_data, 1):
                    # 图片首页
                    args = [*pic_item, pic_no]
                    pool.submit(downloader, args=args)

            log.info(f"albums list {1}, parsed.")


def multi_albums():
    # 单个品类链接，这里用秀人网的链接做测试
    base_url = "https://www.ku137.net/b/9/list_9_{}.html"

    with ThreadPoolExecutor(10) as pool:
        for no in range(1, 10):
            url = base_url.format(no)

            for albums_no, albums_url in enumerate(albums_parser(url), 1):
                print(albums_no, albums_url)
                pool.submit(downloader, albums_url)


def main():
    multi_albums()


if __name__ == '__main__':
    main()
