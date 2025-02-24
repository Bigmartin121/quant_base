#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试运行器，用于运行所有单元测试
"""

import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_all_tests():
    """运行所有单元测试"""
    # 自动发现并加载所有测试用例
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'unit')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # 运行测试并生成报告
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
