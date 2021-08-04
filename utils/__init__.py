# -*- encoding: utf-8 -*-

"""
------------------------------------------
@File       : __init__.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2021/8/4 21:59
------------------------------------------
"""
from settings import cfg
from .logger import Logger

log = Logger(**cfg.log).log
