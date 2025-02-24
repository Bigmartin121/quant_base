#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
基础控制器类，提供通用的控制器功能
"""

import logging
from typing import Dict, Any, Optional
from ..core.module import ModuleBase

logger = logging.getLogger(__name__)

class BaseController:
    """基础控制器类，用于所有控制器的基类"""
    
    def __init__(self):
        self.logger = logger
        self.modules: Dict[str, ModuleBase] = {}
    
    def register_module(self, name: str, module: ModuleBase) -> bool:
        """
        注册新模块
        
        参数：
            name: 模块名称
            module: 模块实例
            
        返回值：
            bool: 如果注册成功返回True，否则返回False
        """
        try:
            if name in self.modules:
                self.logger.warning(f"模块 {name} 已经注册")
                return False
            
            self.modules[name] = module
            return True
        except Exception as e:
            self.logger.error(f"模块注册错误：{str(e)}")
            return False
    
    def get_module(self, name: str) -> Optional[ModuleBase]:
        """
        通过名称获取已注册的模块
        
        参数：
            name: 模块名称
            
        返回值：
            Optional[ModuleBase]: 如果找到则返回模块实例，否则返回None
        """
        return self.modules.get(name)
    
    def initialize_modules(self, config: Optional[Dict] = None) -> bool:
        """
        初始化所有已注册的模块
        
        参数：
            config: 模块配置
            
        返回值：
            bool: 如果所有模块都初始化成功返回True，否则返回False
        """
        try:
            for name, module in self.modules.items():
                module_config = config.get(name) if config else None
                if not module.initialize(module_config):
                    self.logger.error(f"初始化模块失败：{name}")
                    return False
            return True
        except Exception as e:
            self.logger.error(f"模块初始化错误：{str(e)}")
            return False
