# -*- encoding: utf-8 -*-

"""
------------------------------------------
@File       : settings.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2021/6/6 22:55
------------------------------------------
"""
from os.path import dirname, join as path_join


class BaseConfig:
    # 该文件所在的目录的绝对路径
    base_dir = dirname(__file__)

    # ======================[ 数据库相关设置 ]======================
    # ORM格式的数据库地址
    # db_uri = f"sqlite:///{base_dir}/kuaidou.db"
    db_uri = f"mysql+pymysql://spider:Spider666123~@192.168.3.2/videos?charset=utf8"

    # 连接池大小
    pool_size = 15

    # 超过连接池的大小外最多创建的连接
    max_overflow = 10

    # 池中没有线程最多等待的时间，否则报错
    pool_timeout = -1

    # 多久后对线程池中的线程进行一次连接的回收(重置)
    pool_recycle = -1
    # ===========================[ end ]===========================

    # 日志配置
    log = {
        "log_dir": path_join(base_dir, "logs"),
        "filename": "belles_pics_pro.log"
    }

    # 图片文件保存位置
    pics_dir = path_join(base_dir, "pics")

    parser_delay = 5  # 解析线程的延迟时间，防止反爬虫, 单位:秒

    # 下载写真的套数
    download_number = 10000


cfg = BaseConfig
