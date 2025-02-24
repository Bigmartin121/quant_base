#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
股票数据管理模块的单元测试
"""

import os
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.features.stock_manager import StockDataManager

class TestStockDataManager(unittest.TestCase):
    """测试股票数据管理类"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.manager = StockDataManager()
        self.manager.initialize()
        
        # 创建测试数据
        dates = pd.date_range('2023-01-01', periods=5)
        self.test_data = pd.DataFrame({
            'open': [100.0] * 5,
            'close': [101.0] * 5,
            'high': [102.0] * 5,
            'low': [99.0] * 5,
            'volume': [1000000] * 5
        }, index=dates)
    
    def tearDown(self):
        """测试后的清理工作"""
        # 清理测试过程中创建的文件
        cache_file = os.path.join(self.manager.cache_dir, "300718_1d.json")
        if os.path.exists(cache_file):
            os.remove(cache_file)
    
    @patch('src.lib.Ashare.get_price')
    def test_get_and_save_stock_data(self, mock_get_price):
        """测试获取和保存股票数据"""
        # 模拟获取数据
        mock_get_price.return_value = self.test_data
        
        # 测试获取数据
        success, data = self.manager.get_and_save_stock_data('300718')
        self.assertTrue(success)
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(len(data), 5)
        
        # 验证数据已保存
        cache_file = os.path.join(self.manager.cache_dir, "300718_1d.json")
        self.assertTrue(os.path.exists(cache_file))
        
        # 测试加载缓存数据
        loaded_data = self.manager.load_cached_data('300718')
        self.assertIsInstance(loaded_data, pd.DataFrame)
        self.assertEqual(len(loaded_data), 5)
        
        # 验证数据内容
        pd.testing.assert_frame_equal(data, self.test_data)
        pd.testing.assert_frame_equal(loaded_data, self.test_data)
    
    @patch('src.lib.Ashare.get_price')
    def test_error_handling(self, mock_get_price):
        """测试错误处理"""
        # 模拟数据获取失败
        mock_get_price.return_value = None
        
        # 测试获取数据失败
        success, error_msg = self.manager.get_and_save_stock_data('300718')
        self.assertFalse(success)
        self.assertEqual(error_msg, "未获取到数据")
        
        # 测试加载不存在的缓存
        data = self.manager.load_cached_data('nonexistent')
        self.assertTrue(data.empty)
    
    def test_initialization(self):
        """测试初始化功能"""
        # 测试目录创建
        self.assertTrue(os.path.exists(self.manager.data_dir))
        self.assertTrue(os.path.exists(self.manager.cache_dir))
        
        # 测试重复初始化
        self.assertTrue(self.manager.initialize())

if __name__ == '__main__':
    unittest.main()
