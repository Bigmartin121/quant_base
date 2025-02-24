#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
股票数据获取模块，用于获取股票信息
"""

import json
import logging
import requests
from typing import Dict, List
from ..core.module import ModuleBase

logger = logging.getLogger(__name__)

class StockDataFetcher(ModuleBase):
    """股票数据获取类，用于与外部API交互获取数据"""
    
    def __init__(self):
        super().__init__()
        self.frequency_map = {
            '1d': '日线',
            '1m': '1分钟线',
            '5m': '5分钟线',
            '15m': '15分钟线',
            '30m': '30分钟线',
            '60m': '60分钟线'
        }
    
    def get_stock_name(self, code: str) -> str:
        """
        根据股票代码获取股票名称
        
        参数：
            code: 股票代码（如'sz300718'或'300718.XSHE'）
            
        返回值：
            str: 股票名称
        """
        try:
            # 统一股票代码格式
            if '.XSHG' in code or '.XSHE' in code:
                market = 'sh' if '.XSHG' in code else 'sz'
                code = code.replace('.XSHG', '').replace('.XSHE', '')
                code = f"{market}{code}"
            elif not (code.startswith('sh') or code.startswith('sz')):
                code = f"sz{code}" if code.startswith('3') else f"sh{code}"
            
            # 尝试使用腾讯接口
            url = f'http://qt.gtimg.cn/q={code}'
            response = requests.get(url)
            if response.status_code == 200:
                text = response.text
                if text and '~' in text:
                    stock_name = text.split('~')[1]
                    return stock_name
            
            # 如果腾讯接口失败，尝试新浪接口
            code = code[2:]  # 移除 sh/sz 前缀
            url = f'http://hq.sinajs.cn/list={code}'
            response = requests.get(url)
            if response.status_code == 200:
                text = response.text
                if text and ',' in text:
                    stock_name = text.split('"')[1].split(',')[0]
                    return stock_name
            
            return "未知股票"
        except Exception as e:
            logger.error(f"获取股票名称失败：{str(e)}")
            return "未知股票"
    
    def fuzzy_match_stock(self, company_name: str) -> List[Dict[str, str]]:
        """
        模糊匹配公司名称，返回可能的股票列表
        
        参数：
            company_name: 公司名称关键词
            
        返回值：
            List[Dict[str, str]]: 包含匹配到的股票信息的列表
        """
        try:
            urls = [
                'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=3000&sort=symbol&asc=1&node=sz_a',
                'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=3000&sort=symbol&asc=1&node=sh_a'
            ]
            
            matched_stocks = []
            for url in urls:
                response = requests.get(url)
                if response.status_code == 200 and response.text:
                    try:
                        stocks = json.loads(response.text)
                        if isinstance(stocks, list):
                            for stock in stocks:
                                # 确保股票数据包含必要的字段
                                if isinstance(stock, dict) and 'name' in stock and 'symbol' in stock:
                                    if company_name.lower() in stock['name'].lower():
                                        matched_stocks.append({
                                            'code': stock['symbol'],
                                            'name': stock['name']
                                        })
                    except json.JSONDecodeError as e:
                        logger.error(f"解析JSON响应失败：{str(e)}")
                        continue
            
            return matched_stocks
        except Exception as e:
            logger.error(f"匹配股票失败：{str(e)}")
            return []
