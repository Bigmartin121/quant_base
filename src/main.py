#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
量化交易系统主程序入口
"""

import os
import sys
import logging

# 将项目根目录添加到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.interfaces.cli import StockDataCLI

def setup_logging():
    """设置日志配置"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """主程序入口"""
    setup_logging()
    cli = StockDataCLI()
    cli.run()

if __name__ == '__main__':
    main()
