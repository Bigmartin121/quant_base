#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
股票数据管理模块，用于管理股票数据的获取和存储
"""

import os
import logging
from typing import Dict, Any, Tuple
import pandas as pd
from ..core.module import ModuleBase
from ..lib.Ashare import get_price
from ..utils.file_utils import save_to_json, load_from_json

logger = logging.getLogger(__name__)

class StockDataManager(ModuleBase):
    """股票数据管理类，用于处理股票数据的获取和存储"""
    
    def __init__(self):
        super().__init__()
        self.data_dir = "data"
        self.cache_dir = os.path.join(self.data_dir, "cache")
    
    def initialize(self, config: Dict = None) -> bool:
        """
        初始化数据管理器
        
        参数：
            config: 配置字典
            
        返回值：
            bool: 如果初始化成功返回True，否则返回False
        """
        try:
            if not os.path.exists(self.data_dir):
                os.makedirs(self.data_dir)
            if not os.path.exists(self.cache_dir):
                os.makedirs(self.cache_dir)
            return True
        except Exception as e:
            logger.error(f"初始化数据管理器失败：{str(e)}")
            return False
    
    def get_and_save_stock_data(self, code: str, frequency: str = '1d',
                               count: int = 5, end_date: str = '') -> Tuple[bool, Any]:
        """
        获取并保存股票数据
        
        参数：
            code: 股票代码
            frequency: 数据频率
            count: 数据点数量
            end_date: 结束日期
            
        返回值：
            Tuple[bool, Any]: (成功标志, 数据或错误信息)
        """
        try:
            # 获取股票数据
            data = get_price(code, frequency=frequency, count=count, end_date=end_date)
            if data is None:
                return False, "获取数据失败"
            
            # 保存数据到缓存
            cache_file = os.path.join(self.cache_dir, f"{code}_{frequency}.json")
            save_result = save_to_json(cache_file, data.to_dict())
            if not save_result:
                logger.warning(f"保存数据到缓存失败：{cache_file}")
            
            return True, data
        except Exception as e:
            error_msg = f"获取或保存股票数据失败：{str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def load_cached_data(self, code: str, frequency: str = '1d') -> pd.DataFrame:
        """
        从缓存加载股票数据
        
        参数：
            code: 股票代码
            frequency: 数据频率
            
        返回值：
            pd.DataFrame: 股票数据，如果加载失败则返回空DataFrame
        """
        try:
            cache_file = os.path.join(self.cache_dir, f"{code}_{frequency}.json")
            data_dict = load_from_json(cache_file)
            if data_dict:
                return pd.DataFrame.from_dict(data_dict)
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"加载缓存数据失败：{str(e)}")
            return pd.DataFrame()
