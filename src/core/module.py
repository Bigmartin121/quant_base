#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基础模块类，为所有模块提供通用功能
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ModuleBase:
    """基础模块类，所有功能模块的基类"""
    
    def __init__(self):
        self.logger = logger
        self.initialized = False
        self.config: Optional[Dict] = None
    
    def initialize(self, config: Dict = None) -> bool:
        """
        初始化模块
        
        参数：
            config: 模块配置
            
        返回值：
            bool: 如果初始化成功返回True，否则返回False
        """
        try:
            if self.initialized:
                self.logger.warning("模块已经初始化")
                return True
            
            self.config = config or {}
            self.initialized = True
            return True
        except Exception as e:
            self.logger.error(f"模块初始化失败：{str(e)}")
            return False
    
    def is_initialized(self) -> bool:
        """
        检查模块是否已初始化
        
        返回值：
            bool: 如果模块已初始化返回True，否则返回False
        """
        return self.initialized
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """
        获取配置项的值
        
        参数：
            key: 配置项的键
            default: 默认值
            
        返回值：
            Any: 配置项的值，如果不存在则返回默认值
        """
        if not self.config:
            return default
        return self.config.get(key, default)
