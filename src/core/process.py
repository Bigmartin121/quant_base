#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
进程管理模块，用于管理和监控系统进程
"""

import logging
import multiprocessing as mp
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ProcessManager:
    """进程管理类，用于管理系统进程"""
    
    def __init__(self):
        self.processes: Dict[str, mp.Process] = {}
        self.logger = logger
    
    def start_process(self, name: str, target: Any, args: tuple = ()) -> bool:
        """
        启动新进程
        
        参数：
            name: 进程名称
            target: 目标函数
            args: 函数参数
            
        返回值：
            bool: 如果进程启动成功返回True，否则返回False
        """
        try:
            if name in self.processes:
                self.logger.warning(f"进程 {name} 已经存在")
                return False
            
            process = mp.Process(target=target, args=args, name=name)
            process.start()
            self.processes[name] = process
            return True
        except Exception as e:
            self.logger.error(f"启动进程失败：{str(e)}")
            return False
    
    def stop_process(self, name: str) -> bool:
        """
        停止指定进程
        
        参数：
            name: 进程名称
            
        返回值：
            bool: 如果进程停止成功返回True，否则返回False
        """
        try:
            process = self.processes.get(name)
            if not process:
                self.logger.warning(f"进程 {name} 不存在")
                return False
            
            process.terminate()
            process.join()
            del self.processes[name]
            return True
        except Exception as e:
            self.logger.error(f"停止进程失败：{str(e)}")
            return False
