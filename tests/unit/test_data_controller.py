#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据控制器模块的单元测试
"""

import unittest
from unittest.mock import patch, MagicMock
from src.controllers.data_controller import DataController

class TestDataController(unittest.TestCase):
    """测试数据控制器类"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.controller = DataController()
    
    def test_initialization(self):
        """测试控制器初始化"""
        # 测试模块注册
        self.assertTrue(self.controller.initialize())
        self.assertIn('fetcher', self.controller.modules)
        self.assertIn('manager', self.controller.modules)
    
    @patch('src.features.stock_manager.StockDataManager.get_and_save_stock_data')
    def test_get_stock_data(self, mock_get_data):
        """测试获取股票数据"""
        # 测试成功情况
        mock_get_data.return_value = (True, 'test.json')
        success, result = self.controller.get_stock_data('300718', '1d', 5)
        self.assertTrue(success)
        self.assertEqual(result, 'test.json')
        
        # 测试失败情况
        mock_get_data.return_value = (False, '获取数据失败')
        success, result = self.controller.get_stock_data('300718', '1d', 5)
        self.assertFalse(success)
        self.assertEqual(result, '获取数据失败')
        
        # 测试异常情况
        mock_get_data.side_effect = Exception('测试错误')
        success, result = self.controller.get_stock_data('300718', '1d', 5)
        self.assertFalse(success)
        self.assertIn('Failed to get stock data', result)
    
    @patch('src.features.stock_fetcher.StockDataFetcher.fuzzy_match_stock')
    def test_search_stock(self, mock_search):
        """测试搜索股票"""
        # 测试正常搜索
        expected_results = [
            {'code': '300718', 'name': '测试股票'},
            {'code': '600000', 'name': '测试银行'}
        ]
        mock_search.return_value = expected_results
        results = self.controller.search_stock('测试')
        self.assertEqual(results, expected_results)
        
        # 测试无结果
        mock_search.return_value = []
        results = self.controller.search_stock('不存在')
        self.assertEqual(results, [])
        
        # 测试异常情况
        mock_search.side_effect = Exception('搜索错误')
        results = self.controller.search_stock('测试')
        self.assertEqual(results, [])

if __name__ == '__main__':
    unittest.main()
