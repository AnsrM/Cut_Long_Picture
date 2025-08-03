#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
长图切割工具启动脚本
"""

import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from 长图切割 import main

    if __name__ == "__main__":
        print("正在启动长图切割工具...")
        main()

except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保已安装所需依赖: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"启动错误: {e}")
    sys.exit(1)
