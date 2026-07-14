# -*- coding: UTF-8 -*-
"""
示例4：文字识别与找色

本示例展示：
    - 如何识别屏幕上的文字（OCR）
    - 如何查找指定颜色
    - 如何获取指定点的颜色
    - 如何设置字库

前置准备：
    1. 准备字库文件（.txt 格式）
    2. 了解大漠的字库格式和使用方法
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dmsoft import DmSoft


def ocr_demo(dm: DmSoft):
    """文字识别示例"""

    print("=== 文字识别示例 ===\n")

    # 方式1：直接识别屏幕区域（不需要字库，但准确度较低）
    result = dm.Ocr(
        x1=0, y1=0,
        x2=1920, y2=1080,
        color="ffffff-000000",  # 白字黑底
        sim=0.9
    )
    print(f"OCR 识别结果: {result}")

    # 方式2：使用字库识别（准确度高）
    # 先设置字库路径
    # dm.SetDict(0, r"C:\path\to\your\dict.txt")
    #
    # result = dm.OcrEx(
    #     x1=100, y1=100,
    #     x2=500, y2=200,
    #     color="ffffff-000000",
    #     sim=0.9
    # )
    # print(f"使用字库识别结果: {result}")

    # 方式3：查找字符串位置
    # result = dm.FindStr(
    #     x1=0, y1=0,
    #     x2=1920, y2=1080,
    #     string="开始游戏",
    #     color="ffffff-000000",
    #     sim=0.9
    # )
    # print(f"查找字符串结果: {result}")


def find_color_demo(dm: DmSoft):
    """找色示例"""

    print("\n=== 找色示例 ===\n")

    # 查找指定颜色
    # 查找纯红色 (FF0000)
    result = dm.FindColor(
        x1=0, y1=0,
        x2=1920, y2=1080,
        color="FF0000",
        sim=1.0,  # 完全匹配
        dir=0
    )
    print(f"查找红色结果: {result}")

    # 解析结果
    if result and result != "-1|-1":
        x, y = map(int, result.split("|"))
        print(f"找到红色！位置: ({x}, {y})")

        # 获取该点的颜色验证
        actual_color = dm.GetColor(x, y)
        print(f"该点实际颜色: {actual_color}")

    # 查找多种颜色（用 | 分隔）
    result = dm.FindColor(
        x1=0, y1=0,
        x2=1920, y2=1080,
        color="FF0000|00FF00|0000FF",  # 红、绿、蓝
        sim=0.9,
        dir=0
    )
    print(f"查找红绿蓝结果: {result}")


def get_color_demo(dm: DmSoft):
    """获取颜色示例"""

    print("\n=== 获取颜色示例 ===\n")

    # 获取指定点的颜色
    x, y = 100, 100
    color = dm.GetColor(x, y)
    print(f"点 ({x}, {y}) 的颜色: {color}")

    # 获取多个点的颜色
    points = [(100, 100), (200, 200), (300, 300)]
    for px, py in points:
        c = dm.GetColor(px, py)
        print(f"点 ({px}, {py}) 的颜色: {c}")

    # 获取颜色差值（用于偏色设置）
    # 比如要设置偏色 "000000-FFFFFF"，意思是所有颜色都匹配
    print("\n偏色说明:")
    print("  '000000-FFFFFF' = 匹配所有颜色")
    print("  'FFFFFF-000000' = 只匹配纯白色")
    print("  'FF0000-101010' = 匹配红色及其附近颜色")


def color_comparison_demo(dm: DmSoft):
    """颜色比较示例"""

    print("\n=== 颜色比较示例 ===\n")

    x, y = 500, 500

    # 比较指定点颜色
    ret = dm.CmpColor(x, y, "FF0000", 0.9)
    print(f"点 ({x}, {y}) 是否接近红色: {'是' if ret == 1 else '否'}")

    # 比较多个点颜色
    # 格式: x1,y1,color1|x2,y2,color2|...
    multi_points = "100,100,FF0000|200,200,00FF00|300,300,0000FF"
    ret = dm.CmpColorEx(multi_points, 0.9)
    print(f"多点颜色比较结果: {ret}")


def main():
    # 初始化大漠插件
    dm = DmSoft(
        dll_path=r"C:\path\to\dm.dll",
        reg_dll_path=r"C:\path\to\DmReg.dll"
    )

    print(f"插件版本: {dm.Ver()}")

    # 演示 OCR
    ocr_demo(dm)

    # 演示找色
    find_color_demo(dm)

    # 演示获取颜色
    get_color_demo(dm)

    # 演示颜色比较
    color_comparison_demo(dm)


if __name__ == "__main__":
    main()