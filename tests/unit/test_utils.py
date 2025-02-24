#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
工具函数的单元测试
"""

import os
import unittest
import tempfile
import json
from src.utils.helpers import save_to_json, load_from_json, ensure_directory

class TestUtils(unittest.TestCase):
    """测试工具函数"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """测试后的清理工作"""
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)
    
    def test_save_and_load_json(self):
        """测试JSON文件的保存和加载"""
        test_file = os.path.join(self.temp_dir, "test.json")
        test_data = {"test": "data", "number": 42}
        
        # 测试保存
        self.assertTrue(save_to_json(test_file, test_data))
        self.assertTrue(os.path.exists(test_file))
        
        # 测试加载
        loaded_data = load_from_json(test_file)
        self.assertEqual(loaded_data, test_data)
        
        # 测试加载不存在的文件
        self.assertIsNone(load_from_json("nonexistent.json"))
    
    def test_ensure_directory(self):
        """测试目录创建功能"""
        test_dir = os.path.join(self.temp_dir, "test_dir")
        
        # 测试创建目录
        self.assertTrue(ensure_directory(test_dir))
        self.assertTrue(os.path.exists(test_dir))
        
        # 测试已存在的目录
        self.assertTrue(ensure_directory(test_dir))
        
        # 测试创建嵌套目录
        nested_dir = os.path.join(test_dir, "nested", "dir")
        self.assertTrue(ensure_directory(nested_dir))
        self.assertTrue(os.path.exists(nested_dir))

if __name__ == '__main__':
    unittest.main()
