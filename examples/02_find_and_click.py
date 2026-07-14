# -*- coding: UTF-8 -*-
"""
示例2：找图点击 - 在屏幕上查找图片并点击

本示例展示：
    - 如何查找窗口
    - 如何找图（FindPic）
    - 如何解析找图结果
    - 如何点击找到的位置
    - 使用防检测的 MoveToEx

前置准备：
    1. 准备一张游戏/应用中的截图，保存为 bmp 格式
    2. 将图片路径填入下面的 pic_name 变量
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dmsoft import DmSoft


def parse_find_result(result: str):
    """
    解析大漠找图/找色的返回结果

    Args:
        result: 大漠返回的字符串，格式如 "100,200,0" 或 "-1,-1,-1"

    Returns:
        (x, y, index) 元组，如果未找到返回 None
    """
    if not result or result == "-1|-1|-1":
        return None

    parts = result.split("|")
    if len(parts) >= 3:
        try:
            x = int(parts[0])
            y = int(parts[1])
            index = int(parts[2])
            return x, y, index
        except ValueError:
            return None
    return None


def find_and_click(dm: DmSoft, pic_name: str, sim: float = 0.9):
    """
    查找图片并点击

    Args:
        dm: DmSoft 实例
        pic_name: 图片路径
        sim: 相似度，0.0-1.0

    Returns:
        是否成功点击
    """
    # 全屏找图
    result = dm.FindPic(
        x1=0, y1=0,
        x2=1920, y2=1080,  # 根据你的屏幕分辨率调整
        pic_name=pic_name,
        delta_color="000000",  # 不偏色
        sim=sim,
        dir=0  # 从左到右，从上到下查找
    )

    print(f"找图结果: {result}")

    parsed = parse_find_result(result)
    if parsed is None:
        print("未找到图片")
        return False

    x, y, index = parsed
    print(f"找到图片！位置: ({x}, {y}), 图片索引: {index}")

    # 移动鼠标到目标位置（使用防检测的 MoveToEx）
    # 在目标点周围 20x20 的范围内随机移动，更不容易被检测
    move_result = dm.MoveToEx(x, y, 20, 20)
    print(f"移动结果: {move_result}")

    # 随机延时 100-300 毫秒，模拟人工操作
    dm.Delays(100, 300)

    # 左键单击
    dm.LeftClick()
    print("点击完成")

    return True


def find_all_and_click(dm: DmSoft, pic_name: str, sim: float = 0.9):
    """
    查找所有匹配的图片并依次点击

    Args:
        dm: DmSoft 实例
        pic_name: 图片路径（多个用 | 分隔）
        sim: 相似度
    """
    # 使用 FindPicEx 查找所有结果
    result = dm.FindPicEx(
        x1=0, y1=0,
        x2=1920, y2=1080,
        pic_name=pic_name,
        delta_color="000000",
        sim=sim,
        dir=0
    )

    print(f"找图结果: {result}")

    if not result:
        print("未找到任何图片")
        return

    # 解析多个结果，格式: x1,y1,index1|x2,y2,index2|...
    matches = result.split("|")
    for match in matches:
        parts = match.split(",")
        if len(parts) >= 3:
            try:
                x = int(parts[0])
                y = int(parts[1])
                index = int(parts[2])

                print(f"点击位置 ({x}, {y})，图片索引: {index}")

                # 移动并点击
                dm.MoveToEx(x, y, 10, 10)
                dm.Delays(200, 500)
                dm.LeftClick()
                dm.Delays(500, 1000)

            except ValueError:
                continue


def main():
    # 初始化大漠插件
    dm = DmSoft(
        dll_path=r"C:\path\to\dm.dll",
        reg_dll_path=r"C:\path\to\DmReg.dll"
    )

    print(f"插件版本: {dm.Ver()}")

    # ============================================================
    # 示例1：查找单张图片并点击
    # ============================================================
    pic_path = r"C:\path\to\your\button.bmp"  # 修改为你的图片路径

    print("\n=== 示例1：查找单张图片 ===")
    found = find_and_click(dm, pic_path, sim=0.9)

    if found:
        print("操作成功！")
    else:
        print("操作失败，未找到目标图片")

    # ============================================================
    # 示例2：查找多张图片（用 | 分隔）
    # ============================================================
    # pics = r"C:\pics\btn1.bmp|C:\pics\btn2.bmp"
    # print("\n=== 示例2：查找多张图片 ===")
    # find_and_click(dm, pics, sim=0.85)

    # ============================================================
    # 示例3：循环找图直到找到（带超时）
    # ============================================================
    print("\n=== 示例3：循环找图（带5秒超时）===")
    timeout = 5  # 秒
    start_time = time.time()

    while time.time() - start_time < timeout:
        result = dm.FindPic(0, 0, 1920, 1080, pic_path, "000000", 0.9, 0)
        parsed = parse_find_result(result)

        if parsed:
            x, y, _ = parsed
            print(f"找到图片！位置: ({x}, {y})")
            dm.MoveToEx(x, y, 20, 20)
            dm.LeftClick()
            break

        # 每 500ms 找一次
        time.sleep(0.5)
    else:
        print("超时，未找到图片")


if __name__ == "__main__":
    main()