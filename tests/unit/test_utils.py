#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
工具函数的单元测试
"""

import unittest
import json
import os
import tempfile
from src.utils.helpers import load_json, save_json, format_stock_code

class TestHelpers(unittest.TestCase):
    """测试工具函数类"""
    
    def setUp(self):
        """测试前的准备工作"""
        # 创建临时目录用于测试文件操作
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'test.json')
        self.test_data = {'test': 'data', 'number': 123}
    
    def tearDown(self):
        """测试后的清理工作"""
        # 删除测试过程中创建的文件
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.test_dir)
    
    def test_save_and_load_json(self):
        """测试JSON文件的保存和加载功能"""
        # 测试保存JSON文件
        self.assertTrue(save_json(self.test_data, self.test_file))
        self.assertTrue(os.path.exists(self.test_file))
        
        # 测试加载JSON文件
        loaded_data = load_json(self.test_file)
        self.assertEqual(loaded_data, self.test_data)
        
        # 测试加载不存在的文件
        self.assertIsNone(load_json('nonexistent.json'))
    
    def test_format_stock_code(self):
        """测试股票代码格式化功能"""
        # 测试上交所代码
        self.assertEqual(format_stock_code('600000.XSHG'), 'sh600000')
        self.assertEqual(format_stock_code('sh600000'), 'sh600000')
        self.assertEqual(format_stock_code('600000'), 'sh600000')
        
        # 测试深交所代码
        self.assertEqual(format_stock_code('300718.XSHE'), 'sz300718')
        self.assertEqual(format_stock_code('sz300718'), 'sz300718')
        self.assertEqual(format_stock_code('300718'), 'sz300718')

if __name__ == '__main__':
    unittest.main()
