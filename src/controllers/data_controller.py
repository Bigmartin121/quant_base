#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据控制器，用于管理股票数据操作
"""

import logging
from typing import Dict, Any, Tuple, Optional
from .base_controller import BaseController
from ..features.stock_fetcher import StockDataFetcher
from ..features.stock_manager import StockDataManager

logger = logging.getLogger(__name__)

class DataController(BaseController):
    """数据控制器类，用于管理股票数据操作"""
    
    def __init__(self):
        super().__init__()
        self.fetcher = StockDataFetcher()
        self.manager = StockDataManager()
    
    def initialize(self) -> bool:
        """
        初始化控制器及其组件
        
        返回值：
            bool: 如果初始化成功返回True，否则返回False
        """
        try:
            self.register_module("fetcher", self.fetcher)
            self.register_module("manager", self.manager)
            return self.initialize_modules()
        except Exception as e:
            self.logger.error(f"控制器初始化错误：{str(e)}")
            return False
    
    def get_stock_data(self, code: str, frequency: str = '1d',
                      count: int = 5, end_date: str = '') -> Tuple[bool, Any]:
        """
        使用数据管理器获取股票数据
        
        参数：
            code: 股票代码
            frequency: 数据频率
            count: 数据点数量
            end_date: 结束日期
            
        返回值：
            Tuple[bool, Any]: (成功标志, 数据或错误信息)
        """
        try:
            return self.manager.get_and_save_stock_data(
                code, frequency, count, end_date
            )
        except Exception as e:
            error_msg = f"获取股票数据失败：{str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def search_stock(self, keyword: str) -> list:
        """
        使用数据获取器搜索股票
        
        参数：
            keyword: 搜索关键词
            
        返回值：
            list: 匹配的股票列表
        """
        try:
            return self.fetcher.fuzzy_match_stock(keyword)
        except Exception as e:
            self.logger.error(f"股票搜索错误：{str(e)}")
            return []
