#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
辅助函数模块，提供通用的工具函数
"""

import os
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def save_to_json(file_path: str, data: Dict) -> bool:
    """
    将数据保存为JSON文件
    
    参数：
        file_path: 文件路径
        data: 要保存的数据
        
    返回值：
        bool: 如果保存成功返回True，否则返回False
    """
    try:
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        logger.error(f"保存JSON文件失败：{str(e)}")
        return False

def load_from_json(file_path: str) -> Optional[Dict]:
    """
    从JSON文件加载数据
    
    参数：
        file_path: 文件路径
        
    返回值：
        Optional[Dict]: 如果加载成功返回数据字典，否则返回None
    """
    try:
        if not os.path.exists(file_path):
            logger.warning(f"文件不存在：{file_path}")
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载JSON文件失败：{str(e)}")
        return None

def ensure_directory(directory: str) -> bool:
    """
    确保目录存在，如果不存在则创建
    
    参数：
        directory: 目录路径
        
    返回值：
        bool: 如果目录存在或创建成功返回True，否则返回False
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except Exception as e:
        logger.error(f"创建目录失败：{str(e)}")
        return False
