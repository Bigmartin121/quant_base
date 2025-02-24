#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据控制器的单元测试
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.controllers.data_controller import DataController

class TestDataController(unittest.TestCase):
    """测试数据控制器类"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.controller = DataController()
        self.controller.initialize()
        
        # 创建测试数据
        dates = pd.date_range('2023-01-01', periods=5)
        self.test_data = pd.DataFrame({
            'open': [100.0] * 5,
            'close': [101.0] * 5,
            'high': [102.0] * 5,
            'low': [99.0] * 5,
            'volume': [1000000] * 5
        }, index=dates)
    
    def test_initialization(self):
        """测试初始化功能"""
        # 重新初始化应该成功
        self.assertTrue(self.controller.initialize())
        
        # 验证模块注册
        self.assertIsNotNone(self.controller.get_module("fetcher"))
        self.assertIsNotNone(self.controller.get_module("manager"))
    
    @patch('src.features.stock_manager.StockDataManager.get_and_save_stock_data')
    def test_get_stock_data(self, mock_get_data):
        """测试获取股票数据"""
        # 模拟成功获取数据
        mock_get_data.return_value = (True, self.test_data)
        success, data = self.controller.get_stock_data('300718')
        self.assertTrue(success)
        self.assertIs(data, self.test_data)
        
        # 模拟获取数据失败
        mock_get_data.return_value = (False, "未获取到数据")
        success, error = self.controller.get_stock_data('300718')
        self.assertFalse(success)
        self.assertEqual(error, "未获取到数据")
    
    @patch('src.features.stock_fetcher.StockDataFetcher.fuzzy_match_stock')
    def test_search_stock(self, mock_search):
        """测试股票搜索功能"""
        # 模拟搜索结果
        test_stocks = [
            {'code': '300718', 'name': '长盛股份'},
            {'code': '600000', 'name': '浦发银行'}
        ]
        mock_search.return_value = test_stocks
        
        # 测试正常搜索
        result = self.controller.search_stock('长盛')
        self.assertEqual(result, test_stocks)
        
        # 测试搜索失败
        mock_search.side_effect = Exception("搜索失败")
        result = self.controller.search_stock('长盛')
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
