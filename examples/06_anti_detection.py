# -*- coding: UTF-8 -*-
"""
示例6：防检测技巧

本示例展示：
    - 随机延时（Delays）
    - 随机移动（MoveToEx）
    - 模拟人工操作轨迹
    - 随机点击偏移
    - 其他防检测建议

注意：
    这些技巧可以降低被检测的概率，但不能保证100%防检测
    游戏反作弊系统在不断升级，请谨慎使用
"""

import sys
import os
import time
import random
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dmsoft import DmSoft


DLL_PATH = r"C:\path\to\dm.dll"
REG_DLL_PATH = r"C:\path\to\DmReg.dll"


def random_delay(dm: DmSoft, min_ms: int = 500, max_ms: int = 1500):
    """
    随机延时

    Args:
        dm: DmSoft 实例
        min_ms: 最小延时（毫秒）
        max_ms: 最大延时（毫秒）
    """
    dm.Delays(min_ms, max_ms)


def human_like_move(dm: DmSoft, target_x: int, target_y: int, duration: float = 1.0):
    """
    模拟人类移动轨迹（贝塞尔曲线）

    Args:
        dm: DmSoft 实例
        target_x: 目标X坐标
        target_y: 目标Y坐标
        duration: 移动持续时间（秒）
    """
    # 获取当前位置
    pos = dm.GetCursorPos()
    if not pos:
        start_x, start_y = 0, 0
    else:
        start_x, start_y = map(int, pos.split(","))

    # 生成控制点（模拟人类的弧形轨迹）
    # 控制点偏离直线，产生曲线效果
    offset_x = random.randint(-200, 200)
    offset_y = random.randint(-200, 200)
    control_x = (start_x + target_x) // 2 + offset_x
    control_y = (start_y + target_y) // 2 + offset_y

    # 贝塞尔曲线插值
    steps = int(duration * 60)  # 60fps

    for i in range(steps + 1):
        t = i / steps

        # 二次贝塞尔曲线公式
        # B(t) = (1-t)^2 * P0 + 2(1-t)t * P1 + t^2 * P2
        x = int((1 - t) ** 2 * start_x + 2 * (1 - t) * t * control_x + t ** 2 * target_x)
        y = int((1 - t) ** 2 * start_y + 2 * (1 - t) * t * control_y + t ** 2 * target_y)

        # 添加微小随机偏移，模拟手抖
        jitter_x = random.randint(-2, 2)
        jitter_y = random.randint(-2, 2)

        dm.MoveTo(x + jitter_x, y + jitter_y)

        # 每步延时，模拟人类移动速度
        # 开始和结束慢，中间快（模拟加速减速）
        speed_factor = 1.0 - abs(t - 0.5) * 1.5  # 中间快，两边慢
        step_delay = (duration / steps) * (0.5 + speed_factor)
        time.sleep(max(0.001, step_delay))

    # 最后精确移动到目标位置
    dm.MoveToEx(target_x, target_y, 5, 5)


def human_like_click(dm: DmSoft, x: int, y: int):
    """
    模拟人类点击行为

    Args:
        dm: DmSoft 实例
        x: 点击X坐标
        y: 点击Y坐标
    """
    # 1. 移动鼠标到目标附近（不直接对准）
    offset_x = random.randint(-30, 30)
    offset_y = random.randint(-30, 30)
    dm.MoveToEx(x + offset_x, y + offset_y, 20, 20)

    # 2. 短暂停顿（人类需要反应时间）
    random_delay(dm, 200, 500)

    # 3. 微调位置到目标
    dm.MoveToEx(x, y, 10, 10)
    random_delay(dm, 50, 150)

    # 4. 按下左键（人类按下有时间）
    dm.LeftDown()
    random_delay(dm, 50, 120)

    # 5. 弹起左键
    dm.LeftUp()

    # 6. 点击后停顿
    random_delay(dm, 300, 800)


def random_offset_click(dm: DmSoft, x: int, y: int, max_offset: int = 10):
    """
    在目标位置周围随机偏移点击

    Args:
        dm: DmSoft 实例
        x: 目标X坐标
        y: 目标Y坐标
        max_offset: 最大偏移量（像素）
    """
    offset_x = random.randint(-max_offset, max_offset)
    offset_y = random.randint(-max_offset, max_offset)

    click_x = x + offset_x
    click_y = y + offset_y

    print(f"目标: ({x}, {y}), 实际点击: ({click_x}, {click_y}), 偏移: ({offset_x}, {offset_y})")

    dm.MoveToEx(click_x, click_y, 5, 5)
    dm.Delays(100, 300)
    dm.LeftClick()


def random_scroll(dm: DmSoft, min_times: int = 1, max_times: int = 5):
    """
    随机滚轮滚动

    Args:
        dm: DmSoft 实例
        min_times: 最少滚动次数
        max_times: 最多滚动次数
    """
    times = random.randint(min_times, max_times)
    direction = random.choice(["up", "down"])

    print(f"随机滚动: {direction} {times} 次")

    for _ in range(times):
        if direction == "up":
            dm.WheelUp()
        else:
            dm.WheelDown()
        dm.Delays(200, 500)


def simulate_reading(dm: DmSoft, region: tuple, duration: float = 3.0):
    """
    模拟阅读行为（鼠标在区域内随机移动）

    Args:
        dm: DmSoft 实例
        region: (x1, y1, x2, y2) 阅读区域
        duration: 阅读持续时间（秒）
    """
    x1, y1, x2, y2 = region

    print(f"模拟阅读区域: {region}, 持续时间: {duration}秒")

    start_time = time.time()
    while time.time() - start_time < duration:
        # 在区域内随机移动
        target_x = random.randint(x1, x2)
        target_y = random.randint(y1, y2)

        # 使用人类轨迹移动
        human_like_move(dm, target_x, target_y, duration=0.3)

        # 停留一段时间（模拟阅读）
        dm.Delays(500, 1500)


def main():
    dm = DmSoft(dll_path=DLL_PATH, reg_dll_path=REG_DLL_PATH)

    print(f"插件版本: {dm.Ver()}")
    print("=" * 60)
    print("防检测技巧演示")
    print("=" * 60)

    # 示例1：随机延时
    print("\n=== 示例1：随机延时 ===")
    print("延时 500-1500ms...")
    random_delay(dm, 500, 1500)
    print("延时结束")

    # 示例2：模拟人类移动轨迹
    print("\n=== 示例2：人类轨迹移动 ===")
    print("移动鼠标到 (800, 600)，使用贝塞尔曲线...")
    human_like_move(dm, 800, 600, duration=1.5)
    print("移动完成")

    # 示例3：模拟人类点击
    print("\n=== 示例3：人类点击 ===")
    print("在 (800, 600) 模拟人类点击...")
    human_like_click(dm, 800, 600)
    print("点击完成")

    # 示例4：随机偏移点击
    print("\n=== 示例4：随机偏移点击 ===")
    random_offset_click(dm, 800, 600, max_offset=15)

    # 示例5：随机滚动
    print("\n=== 示例5：随机滚动 ===")
    random_scroll(dm, 2, 4)

    # 示例6：模拟阅读
    print("\n=== 示例6：模拟阅读 ===")
    simulate_reading(dm, (100, 100, 800, 600), duration=2.0)

    print("\n" + "=" * 60)
    print("防检测建议：")
    print("=" * 60)
    print("1. 随机延时：每次操作后添加随机延时")
    print("2. 随机偏移：点击位置不要每次都一样")
    print("3. 人类轨迹：使用曲线移动，不要直线瞬移")
    print("4. 模拟停顿：操作之间添加随机停顿")
    print("5. 变速操作：不要固定频率操作")
    print("6. 随机滚动：偶尔滚动页面")
    print("7. 窗口激活：操作前先激活窗口")
    print("8. 避免规律：不要固定时间间隔做相同操作")
    print("=" * 60)


if __name__ == "__main__":
    main()