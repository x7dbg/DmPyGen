# -*- coding: UTF-8 -*-
"""
示例1：基础使用 - 初始化大漠插件并执行简单操作

本示例展示：
    - 如何初始化 DmSoft 对象（免注册方式）
    - 获取插件版本号
    - 注册插件
    - 获取当前鼠标位置
"""

import sys
import os

# 将上级目录加入路径，以便导入 dmsoft
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dmsoft import DmSoft


def main():
    # ============================================================
    # 方式1：免注册调用（推荐，无需管理员权限注册 dll）
    # ============================================================
    # 请根据你的实际路径修改
    dm = DmSoft(
        dll_path=r"C:\path\to\dm.dll",
        reg_dll_path=r"C:\path\to\DmReg.dll"
    )

    # ============================================================
    # 方式2：已注册调用（需要先用 regsvr32 注册 dm.dll）
    # ============================================================
    # dm = DmSoft()

    # 获取插件版本号
    version = dm.Ver()
    print(f"大漠插件版本: {version}")

    # 注册插件（如果你有注册码的话）
    # ret = dm.Reg("你的注册码", "")
    # print(f"注册结果: {ret}")

    # 获取当前鼠标位置
    pos = dm.GetCursorPos()
    print(f"当前鼠标位置: {pos}")

    # 移动鼠标到屏幕中央（假设分辨率 1920x1080）
    screen_width = 1920
    screen_height = 1080
    center_x = screen_width // 2
    center_y = screen_height // 2

    ret = dm.MoveTo(center_x, center_y)
    print(f"移动鼠标到 ({center_x}, {center_y}): {'成功' if ret == 1 else '失败'}")

    # 获取移动后的鼠标位置
    pos = dm.GetCursorPos()
    print(f"移动后鼠标位置: {pos}")


if __name__ == "__main__":
    main()