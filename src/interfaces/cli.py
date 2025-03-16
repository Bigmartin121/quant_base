#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
股票数据操作的命令行界面
"""

import logging
import sys
import io
from typing import Optional
from src.controllers.data_controller import DataController

logger = logging.getLogger(__name__)

class StockDataCLI:
    """股票数据操作的命令行界面类"""
    
    def __init__(self):
        self.controller = DataController()
        self.frequencies = ['1d', '1m', '5m', '15m', '30m', '60m']
    
    def setup(self):
        """设置命令行界面环境"""
        # 设置输入/输出编码
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
        
        # 初始化控制器
        if not self.controller.initialize():
            logger.error("初始化数据控制器失败")
            sys.exit(1)
    
    def run(self):
        """运行交互式界面"""
        self.setup()
        
        while True:
            try:
                # 步骤1：交互式搜索
                keyword = input("\n输入公司名称关键词（输入q退出）：")
                if keyword.lower() == 'q':
                    break
                
                matches = self.controller.search_stock(keyword)
                if not matches:
                    logger.info("未找到匹配的股票")
                    continue
                
                print("\n搜索结果：")
                for idx, stock in enumerate(matches, 1):
                    print(f"{idx}. 代码：{stock['code']}，名称：{stock['name']}")
                
                # 步骤2：选择股票
                choice = self._get_valid_input("\n选择股票编号（输入q重新搜索）：",
                                            1, len(matches))
                if choice is None:
                    continue
                
                selected_stock = matches[choice - 1]
                
                # 步骤3：选择频率
                print("\n可用的数据频率：")
                for idx, freq in enumerate(self.frequencies, 1):
                    print(f"{idx}. {freq}")
                
                freq_idx = self._get_valid_input("\n选择频率编号：",
                                               1, len(self.frequencies))
                if freq_idx is None:
                    continue
                
                frequency = self.frequencies[freq_idx - 1]
                
                # 获取并保存数据
                print(f"\n正在获取 {selected_stock['name']} 的{frequency}数据...")
                success, result = self.controller.get_stock_data(
                    selected_stock['code'],
                    frequency=frequency,
                    count=5
                )
                
                if success:
                    logger.info(f"数据已保存到：{result}")
                else:
                    logger.error(f"获取数据失败：{result}")
                
            except EOFError:
                break
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"意外错误：{str(e)}")
    
    def _get_valid_input(self, prompt: str, min_val: int, max_val: int) -> Optional[int]:
        """
        获取有效的用户输入
        
        参数：
            prompt: 输入提示
            min_val: 最小有效值
            max_val: 最大有效值
            
        返回值：
            Optional[int]: 用户输入的数字，如果输入无效则返回None
        """
        while True:
            try:
                value = input(prompt)
                if value.lower() == 'q':
                    return None
            
                num = int(value)
                if min_val <= num <= max_val:
                    return num
                print(f"请输入 {min_val} 到 {max_val} 之间的数字")
            except ValueError:
                print("请输入有效的数字")
