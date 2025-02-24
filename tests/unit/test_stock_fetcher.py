#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
股票数据获取模块的单元测试
"""

import unittest
from unittest.mock import patch, MagicMock
from src.features.stock_fetcher import StockDataFetcher

class TestStockDataFetcher(unittest.TestCase):
    """测试股票数据获取类"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.fetcher = StockDataFetcher()
    
    def test_frequency_map(self):
        """测试频率映射字典"""
        expected_map = {
            '1d': '日线',
            '1m': '1分钟线',
            '5m': '5分钟线',
            '15m': '15分钟线',
            '30m': '30分钟线',
            '60m': '60分钟线'
        }
        self.assertEqual(self.fetcher.frequency_map, expected_map)
    
    @patch('requests.get')
    def test_get_stock_name_tencent(self, mock_get):
        """测试从腾讯接口获取股票名称"""
        # 模拟腾讯接口返回数据
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = 'v_sz300718="1~测试股票~..."'
        mock_get.return_value = mock_response
        
        # 测试不同格式的股票代码
        self.assertEqual(self.fetcher.get_stock_name('sz300718'), '测试股票')
        self.assertEqual(self.fetcher.get_stock_name('300718.XSHE'), '测试股票')
        self.assertEqual(self.fetcher.get_stock_name('300718'), '测试股票')
    
    @patch('requests.get')
    def test_get_stock_name_sina(self, mock_get):
        """测试从新浪接口获取股票名称"""
        # 模拟腾讯接口失败，新浪接口成功
        def mock_get_response(url):
            mock_response = MagicMock()
            mock_response.status_code = 200
            if 'qt.gtimg.cn' in url:
                mock_response.text = ''  # 腾讯接口返回空
            else:
                mock_response.text = 'var hq_str_sz300718="测试股票,..."'
            return mock_response
        
        mock_get.side_effect = mock_get_response
        self.assertEqual(self.fetcher.get_stock_name('sz300718'), '测试股票')
    
    @patch('requests.get')
    def test_fuzzy_match_stock(self, mock_get):
        """测试模糊匹配股票功能"""
        def mock_get_response(url):
            mock_response = MagicMock()
            mock_response.status_code = 200
            
            # 根据URL返回不同的数据
            if 'node=sz_a' in url:
                mock_response.text = '''[{
                    "symbol": "300718",
                    "code": "300718",
                    "name": "测试股票",
                    "trade": "0.00"
                }]'''
            else:  # sh_a
                mock_response.text = '''[{
                    "symbol": "600000",
                    "code": "600000",
                    "name": "测试银行",
                    "trade": "0.00"
                }]'''
            return mock_response
        
        mock_get.side_effect = mock_get_response
        
        # 测试模糊匹配
        matches = self.fetcher.fuzzy_match_stock('测试')
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0]['code'], '300718')
        self.assertEqual(matches[0]['name'], '测试股票')
        self.assertEqual(matches[1]['code'], '600000')
        self.assertEqual(matches[1]['name'], '测试银行')
        
        # 测试无匹配结果
        def mock_empty_response(url):
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = '[]'
            return mock_response
        
        mock_get.side_effect = mock_empty_response
        matches = self.fetcher.fuzzy_match_stock('不存在的公司')
        self.assertEqual(len(matches), 0)
    
    def test_error_handling(self):
        """测试错误处理"""
        # 测试网络请求失败的情况
        with patch('requests.get', side_effect=Exception('网络错误')):
            self.assertEqual(self.fetcher.get_stock_name('300718'), '未知股票')
            self.assertEqual(self.fetcher.fuzzy_match_stock('测试'), [])

if __name__ == '__main__':
    unittest.main()
