# -*- coding: UTF-8 -*-
"""
示例3：窗口绑定 - 后台操作窗口

本示例展示：
    - 如何查找窗口（通过类名、标题、进程名）
    - 如何绑定窗口（后台模式）
    - 后台找图、后台点击
    - 解绑窗口

前置准备：
    1. 打开目标游戏或应用窗口
    2. 使用 Spy++ 或类似工具获取窗口类名/标题
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dmsoft import DmSoft


def find_window_demo(dm: DmSoft):
    """演示多种查找窗口的方式"""

    print("=== 查找窗口示例 ===\n")

    # 方式1：通过窗口类名和标题查找
    # 使用 Spy++ 查看窗口类名，常见的有：
    # - Notepad 的类名: "Notepad"
    # - 计算器: "ApplicationFrameWindow"
    hwnd = dm.FindWindow("Notepad", "")
    print(f"查找记事本窗口: hwnd={hwnd}")

    # 方式2：通过进程名查找窗口
    hwnd = dm.FindWindowByProcess("notepad.exe", "", "")
    print(f"通过进程名查找记事本: hwnd={hwnd}")

    # 方式3：获取当前活动窗口
    hwnd = dm.GetForegroundWindow()
    print(f"当前活动窗口: hwnd={hwnd}")

    # 获取窗口信息
    if hwnd:
        title = dm.GetWindowTitle(hwnd)
        class_name = dm.GetWindowClass(hwnd)
        rect = dm.GetWindowRect(hwnd)
        print(f"窗口标题: {title}")
        print(f"窗口类名: {class_name}")
        print(f"窗口矩形: {rect}")

    # 方式4：枚举所有窗口
    print("\n=== 枚举所有记事本窗口 ===")
    result = dm.EnumWindowByProcess("notepad.exe", "", "", 0)
    if result:
        hwnds = result.split(",")
        print(f"找到 {len(hwnds)} 个记事本窗口: {hwnds}")
    else:
        print("未找到记事本窗口")

    return hwnd


def bind_window_demo(dm: DmSoft, hwnd: int):
    """
    演示窗口绑定

    大漠绑定模式说明：
        display（显示模式）:
            "normal"  = 正常模式（推荐，最稳定）
            "gdi"     = gdi 后台模式（窗口可被遮挡）
            "gdi2"    = gdi2 后台模式
            "dx2"     = dx2 后台模式（部分游戏适用）
            "opengl"  = opengl 后台模式

        mouse（鼠标模式）:
            "normal"    = 正常模式
            "windows"   = windows 消息模式（后台）
            "windows3"  = windows3 消息模式

        keypad（键盘模式）:
            "normal"   = 正常模式
            "windows"  = windows 消息模式（后台）

        mode（绑定模式）:
            0 = 推荐模式
            1 = 高级模式
    """

    print("\n=== 绑定窗口示例 ===\n")

    # 绑定窗口（后台模式）
    # display="gdi": gdi 后台，窗口可被遮挡
    # mouse="windows": 后台鼠标消息
    # keypad="windows": 后台键盘消息
    # mode=0: 推荐模式
    ret = dm.BindWindow(hwnd, display="gdi", mouse="windows", keypad="windows", mode=0)

    if ret == 1:
        print(f"窗口绑定成功！hwnd={hwnd}")
    else:
        print(f"窗口绑定失败，错误码: {ret}")
        print("常见原因：")
        print("  - 窗口句柄无效")
        print("  - 没有管理员权限（某些模式需要）")
        print("  - 窗口已经绑定")
        return False

    # 获取绑定信息
    bind_info = dm.GetBindWindow()
    print(f"当前绑定窗口: {bind_info}")

    return True


def background_operations(dm: DmSoft):
    """演示后台操作"""

    print("\n=== 后台操作示例 ===\n")

    # 后台找图（绑定后，即使窗口被遮挡也能找到）
    pic_path = r"C:\path\to\your\button.bmp"

    result = dm.FindPic(
        x1=0, y1=0,
        x2=1920, y2=1080,
        pic_name=pic_path,
        delta_color="000000",
        sim=0.9,
        dir=0
    )

    print(f"后台找图结果: {result}")

    if result and result != "-1|-1|-1":
        parts = result.split("|")
        x, y = int(parts[0]), int(parts[1])

        # 后台点击（绑定后有效）
        dm.MoveTo(x, y)
        dm.LeftClick()
        print(f"后台点击 ({x}, {y})")

    # 后台按键
    dm.KeyPress(13)  # 回车键
    print("后台发送回车键")


def unbind_window(dm: DmSoft):
    """解绑窗口"""
    print("\n=== 解绑窗口 ===")
    ret = dm.UnBindWindow()
    print(f"解绑结果: {'成功' if ret == 1 else '失败'}")


def main():
    # 初始化大漠插件
    dm = DmSoft(
        dll_path=r"C:\path\to\dm.dll",
        reg_dll_path=r"C:\path\to\DmReg.dll"
    )

    print(f"插件版本: {dm.Ver()}")

    # 演示查找窗口
    hwnd = find_window_demo(dm)

    if hwnd == 0:
        print("\n未找到目标窗口，请先打开记事本或其他目标窗口")
        print("你可以修改代码中的类名/标题来匹配你的目标窗口")
        return

    # 演示绑定窗口
    if bind_window_demo(dm, hwnd):
        try:
            # 演示后台操作
            background_operations(dm)
        finally:
            # 确保解绑
            unbind_window(dm)

    # 演示窗口状态控制
    print("\n=== 窗口状态控制 ===")
    print("最小化窗口...")
    dm.SetWindowState(hwnd, 2)  # 最小化
    time.sleep(1)

    print("还原窗口...")
    dm.SetWindowState(hwnd, 4)  # 还原
    time.sleep(1)

    print("激活窗口...")
    dm.SetWindowState(hwnd, 1)  # 激活


if __name__ == "__main__":
    main()