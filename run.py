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
from re import findall

from workers import albums_parser, album_full_pics_parser, save_pics


def main():
    # 单个品类链接，这里用秀人网的链接做测试
    base_url = "https://www.ku137.net/b/9/list_9_{}.html"

    no = 1

    while True:
        url = base_url.format(no)

        for url in albums_parser(url):
            data = album_full_pics_parser(url)
            print(data)
            save_pics(data)

        if no == 1:
            break

        no += 1


def demo():
    titles = [
        "[秀人XIUREN] 2021.04.06 NO.3275 陈小喵",
        "[秀人XIUREN] 2021.04.07 NO.3279 周于希Sandy",
        "[秀人XIUREN] 2021.04.07 NO.3277 葛征 净高184cm",
        "[秀人XIUREN] 2021.04.06 NO.3272 梦心月",
        "[秀人XIUREN] 2020.07.30 NO.2387 白茹雪Abby"
    ]

    for title in titles:
        site = findall(r"\[(.*?)\]", title)[0]
        no = int(findall(r"NO\.(\d+)", title)[0])
        name_content = findall(r"NO\.\d+(.*)", title)[0]
        name = name_content.strip().split()[0]

        print(site)
        print(no)
        print(name)


if __name__ == '__main__':
    main()
    # demo()
