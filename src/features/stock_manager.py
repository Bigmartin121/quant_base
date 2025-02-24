#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
股票数据管理模块，用于管理股票数据的获取和存储
"""

import os
import logging
from typing import Dict, Any, Tuple
import pandas as pd
from datetime import datetime
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
        self.stock_dir = os.path.join(self.data_dir, "stocks")
    
    def initialize(self, config: Dict = None) -> bool:
        """
        初始化数据管理器
        
        参数：
            config: 配置字典
            
        返回值：
            bool: 如果初始化成功返回True，否则返回False
        """
        try:
            # 创建所需的目录
            for directory in [self.data_dir, self.cache_dir, self.stock_dir]:
                if not os.path.exists(directory):
                    os.makedirs(directory)
            return True
        except Exception as e:
            logger.error(f"初始化数据管理器失败：{str(e)}")
            return False
    
    def _serialize_dataframe(self, df: pd.DataFrame) -> Dict:
        """
        将DataFrame序列化为可JSON化的字典
        
        参数：
            df: pandas DataFrame对象
            
        返回值：
            Dict: 可JSON化的字典
        """
        if df is None or df.empty:
            return {}
        
        # 将时间戳转换为字符串
        df_copy = df.copy()
        if not df_copy.empty and df_copy.index.dtype.kind == 'M':  # 检查是否为时间戳类型
            df_copy.index = df_copy.index.strftime('%Y-%m-%d %H:%M:%S')
        
        # 转换为字典并确保所有值都是JSON可序列化的
        data_dict = {
            'index': df_copy.index.tolist(),
            'columns': df_copy.columns.tolist(),
            'data': df_copy.values.tolist()
        }
        return data_dict
    
    def _deserialize_dataframe(self, data_dict: Dict) -> pd.DataFrame:
        """
        将字典反序列化为DataFrame
        
        参数：
            data_dict: 序列化的数据字典
            
        返回值：
            pd.DataFrame: 反序列化后的DataFrame
        """
        if not data_dict or not all(k in data_dict for k in ['index', 'columns', 'data']):
            return pd.DataFrame()
        
        try:
            df = pd.DataFrame(
                data=data_dict['data'],
                index=pd.to_datetime(data_dict['index']),
                columns=data_dict['columns']
            )
            return df
        except Exception as e:
            logger.error(f"反序列化DataFrame失败：{str(e)}")
            return pd.DataFrame()
    
    def _get_stock_file_path(self, code: str, frequency: str) -> str:
        """
        获取股票数据文件的保存路径
        
        参数：
            code: 股票代码
            frequency: 数据频率
            
        返回值：
            str: 文件保存路径
        """
        # 创建基于日期的目录结构
        date_str = datetime.now().strftime('%Y%m%d')
        stock_date_dir = os.path.join(self.stock_dir, date_str)
        if not os.path.exists(stock_date_dir):
            os.makedirs(stock_date_dir)
        
        # 生成文件名
        filename = f"{code}_{frequency}_{date_str}.json"
        return os.path.join(stock_date_dir, filename)
    
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
            if data is None or data.empty:
                return False, "未获取到数据"
            
            # 序列化数据
            data_dict = self._serialize_dataframe(data)
            if not data_dict:
                return False, "数据序列化失败"
            
            # 保存到缓存
            cache_file = os.path.join(self.cache_dir, f"{code}_{frequency}.json")
            if not save_to_json(cache_file, data_dict):
                logger.warning(f"保存数据到缓存失败：{cache_file}")
            
            # 保存到数据文件夹
            stock_file = self._get_stock_file_path(code, frequency)
            if not save_to_json(stock_file, data_dict):
                return False, f"保存数据失败：{stock_file}"
            
            return True, stock_file  # 返回保存的文件路径
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
                return self._deserialize_dataframe(data_dict)
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"加载缓存数据失败：{str(e)}")
            return pd.DataFrame()
