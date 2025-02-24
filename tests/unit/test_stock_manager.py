#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
股票数据管理模块的单元测试
"""

import unittest
import os
import json
import pandas as pd
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.features.stock_manager import StockDataManager

class TestStockDataManager(unittest.TestCase):
    """测试股票数据管理类"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.manager = StockDataManager()
        
        # 创建测试用的股票数据
        self.test_data = pd.DataFrame({
            'open': [10.0, 11.0],
            'close': [11.0, 12.0],
            'high': [12.0, 13.0],
            'low': [9.0, 10.0],
            'volume': [1000, 2000]
        }, index=pd.date_range('2025-02-25', periods=2))
    
    def tearDown(self):
        """测试后的清理工作"""
        # 删除测试过程中创建的文件
        for file in os.listdir('.'):
            if file.endswith('.json') and '行情_' in file:
                os.remove(file)
    
    @patch('src.features.stock_manager.get_price')
    @patch('src.features.stock_fetcher.StockDataFetcher.get_stock_name')
    def test_get_and_save_stock_data(self, mock_get_name, mock_get_price):
        """测试获取并保存股票数据"""
        # 模拟数据获取
        mock_get_price.return_value = self.test_data
        mock_get_name.return_value = '测试股票'
        
        # 测试正常情况
        success, filename = self.manager.get_and_save_stock_data('300718', '1d', 2)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(filename))
        
        # 验证保存的数据
        with open(filename, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        
        self.assertEqual(saved_data['stock_code'], '300718')
        self.assertEqual(saved_data['stock_name'], '测试股票')
        self.assertEqual(saved_data['frequency'], '1d')
        self.assertEqual(saved_data['data_count'], 2)
        
        # 测试数据格式
        first_date = list(saved_data['data'].keys())[0]
        first_record = saved_data['data'][first_date]
        self.assertEqual(first_record['open'], 10.0)
        self.assertEqual(first_record['close'], 11.0)
        self.assertEqual(first_record['high'], 12.0)
        self.assertEqual(first_record['low'], 9.0)
        self.assertEqual(first_record['volume'], 1000.0)
    
    @patch('src.features.stock_manager.get_price')
    def test_error_handling(self, mock_get_price):
        """测试错误处理"""
        # 测试获取数据失败
        mock_get_price.return_value = None
        success, error_msg = self.manager.get_and_save_stock_data('300718')
        self.assertFalse(success)
        self.assertEqual(error_msg, "No data retrieved")
        
        # 测试数据为空
        mock_get_price.return_value = pd.DataFrame()
        success, error_msg = self.manager.get_and_save_stock_data('300718')
        self.assertFalse(success)
        self.assertEqual(error_msg, "No data retrieved")
        
        # 测试异常情况
        mock_get_price.side_effect = Exception('测试错误')
        success, error_msg = self.manager.get_and_save_stock_data('300718')
        self.assertFalse(success)
        self.assertIn('Failed to get or save data', error_msg)

if __name__ == '__main__':
    unittest.main()
