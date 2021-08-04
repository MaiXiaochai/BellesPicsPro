# -*- encoding: utf-8 -*-

"""
------------------------------------------
@File       : workers.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2021/8/4 22:05
------------------------------------------
    一些主要的功能
"""
from re import findall
from os.path import join as path_join, exists
from os import makedirs

from requests import get as r_get
from lxml import etree

from utils import cfg, log


class ParerError(Exception):
    pass


def albums_parser(url) -> list:
    """
        解析该页上的所有写真集地址，并返回所有写真集 url
    """
    resp = r_get(url)
    resp.encoding = "gb2312"
    code = resp.status_code

    if code != 200:
        raise ParerError("专辑列表访问出误")

    content = etree.HTML(resp.text)
    data = content.xpath('//div[@class="m-list ml1"]/ul/li/a/@href')

    return data


def pic_page_parer(url) -> list:
    """
        解析图片页面的图片地址，并返回列表
        单个元素内容为 (图片地址，网站名称，专辑序号，人物名称)
    """
    resp = r_get(url)
    resp.encoding = "gb2312"
    code = resp.status_code

    if code != 200:
        raise ParerError("专辑列表访问出误")

    content = etree.HTML(resp.text)
    data = content.xpath('//div[@class="content"]/img')

    result = []
    for no, i in enumerate(data, 1):
        url = str(i.xpath("@src")[0])
        title = str(i.xpath("@alt")[0])

        site = findall(r"\[(.*?)\]", title)[0]
        no = int(findall(r"NO\.(\d+)", title)[0])

        name_content = findall(r"NO\.\d+(.*)", title)[0]
        name = name_content.strip().split()[0]

        result.append((url, site, no, name))

    return result


def album_full_pics_parser(url):
    """
        给出写真集的第一页地址，返回全部写真集的图片信息
        单个元素内容为 (图片地址，网站名称，专辑序号，人物名称)
    """
    url_content = url.rsplit(".", 1)
    base_url = url_content[0] + "_{}." + url_content[-1]

    result = []

    for count in range(1, 50):
        curr_url = base_url.format(count) if count != 1 else url

        try:
            curr_data = pic_page_parer(curr_url)
            result.extend(curr_data)
        except Exception:
            break

    return result


def get_pic_content(url) -> bytes:
    """
        获取图片二进制数据
    """
    return r_get(url).content


def save_pics(pics: list):
    """
        保存一套专辑的图片
    """
    _, site, no_, name = pics[0]
    album_name = f"{site}--{no_}--{name}"
    base_dir = cfg.pics_dir
    curr_dir = path_join(base_dir, album_name)

    if not exists(curr_dir):
        makedirs(curr_dir)

    for count, item in enumerate(pics, 1):
        pic_path = path_join(curr_dir, f"{album_name}--{count}.jpg")
        url = item[0]

        if not exists(pic_path):
            pic_bytes = get_pic_content(url)
            with open(pic_path, "wb") as f:
                f.write(pic_bytes)

        log.info(f"NO.{count} | {pic_path}, saved.")


def demo():
    pic_url = "https://pic.ku137.net/piccc/2021/allimg/210802/02153338-1-1Q2.jpg"
    pic_data = get_pic_content(pic_url)
    print(pic_data)
    print(type(pic_data))


def main():
    test_url = "https://www.ku137.net/b/9/41983.html"
    data = album_full_pics_parser(test_url)
    for no, i in enumerate(data, 1):
        print(no, i)


if __name__ == '__main__':
    demo()
