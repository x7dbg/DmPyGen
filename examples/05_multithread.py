# -*- coding: UTF-8 -*-
"""
示例5：多线程使用

本示例展示：
    - 如何在多线程中使用大漠插件
    - 每个线程创建独立的 DmSoft 实例
    - 线程间协作完成任务

注意：
    - 每个线程必须创建自己的 DmSoft 实例
    - 不要跨线程共享 DmSoft 对象
    - DmSoft 内部已自动初始化 COM 组件
"""

import sys
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dmsoft import DmSoft


# 全局配置
DLL_PATH = r"C:\path\to\dm.dll"
REG_DLL_PATH = r"C:\path\to\DmReg.dll"


def worker_find_pic(task_id: int, pic_name: str, region: tuple):
    """
    工作线程：在指定区域找图

    Args:
        task_id: 任务ID
        pic_name: 图片名称
        region: (x1, y1, x2, y2) 查找区域

    Returns:
        查找结果
    """
    # 每个线程创建自己的 DmSoft 实例
    dm = DmSoft(dll_path=DLL_PATH, reg_dll_path=REG_DLL_PATH)

    x1, y1, x2, y2 = region

    print(f"[线程-{task_id}] 开始在区域 ({x1},{y1},{x2},{y2}) 查找 {pic_name}")

    result = dm.FindPic(x1, y1, x2, y2, pic_name, "000000", 0.9, 0)

    print(f"[线程-{task_id}] 查找结果: {result}")

    return {
        "task_id": task_id,
        "region": region,
        "result": result
    }


def worker_monitor_window(task_id: int, hwnd: int, interval: float = 1.0):
    """
    工作线程：监控窗口状态

    Args:
        task_id: 任务ID
        hwnd: 要监控的窗口句柄
        interval: 检查间隔（秒）
    """
    dm = DmSoft(dll_path=DLL_PATH, reg_dll_path=REG_DLL_PATH)

    print(f"[线程-{task_id}] 开始监控窗口 {hwnd}")

    for i in range(10):  # 监控10次
        # 获取窗口状态
        is_alive = dm.IsWindow(hwnd)
        rect = dm.GetWindowRect(hwnd) if is_alive else "窗口已关闭"
        title = dm.GetWindowTitle(hwnd) if is_alive else "N/A"

        print(f"[线程-{task_id}] 检查 #{i+1}: 存活={is_alive}, 标题={title}, 矩形={rect}")

        time.sleep(interval)

    print(f"[线程-{task_id}] 监控结束")


def simple_thread_example():
    """简单多线程示例"""

    print("=== 简单多线程示例 ===\n")

    def task(name: str, delay: float):
        """模拟任务"""
        dm = DmSoft(dll_path=DLL_PATH, reg_dll_path=REG_DLL_PATH)

        print(f"[{name}] 开始执行，插件版本: {dm.Ver()}")
        time.sleep(delay)

        # 获取鼠标位置
        pos = dm.GetCursorPos()
        print(f"[{name}] 当前鼠标位置: {pos}")

        print(f"[{name}] 执行完成")

    # 创建多个线程
    threads = []
    for i in range(3):
        t = threading.Thread(target=task, args=(f"线程-{i+1}", 1.0))
        threads.append(t)
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()

    print("\n所有线程执行完成")


def thread_pool_example():
    """线程池示例：并行查找多张图片"""

    print("\n=== 线程池并行找图示例 ===\n")

    # 定义查找任务
    # 将屏幕分成4个区域，每个线程查找一个区域
    screen_width = 1920
    screen_height = 1080
    half_w = screen_width // 2
    half_h = screen_height // 2

    tasks = [
        (1, r"C:\pics\target.bmp", (0, 0, half_w, half_h)),           # 左上
        (2, r"C:\pics\target.bmp", (half_w, 0, screen_width, half_h)), # 右上
        (3, r"C:\pics\target.bmp", (0, half_h, half_w, screen_height)), # 左下
        (4, r"C:\pics\target.bmp", (half_w, half_h, screen_width, screen_height)), # 右下
    ]

    # 使用线程池并行执行
    with ThreadPoolExecutor(max_workers=4) as executor:
        # 提交所有任务
        futures = [
            executor.submit(worker_find_pic, task_id, pic, region)
            for task_id, pic, region in tasks
        ]

        # 收集结果
        results = []
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
                print(f"任务 {result['task_id']} 完成: {result['result']}")
            except Exception as e:
                print(f"任务执行出错: {e}")

    # 分析结果
    print("\n=== 查找结果汇总 ===")
    for r in sorted(results, key=lambda x: x["task_id"]):
        print(f"区域 {r['task_id']}: {r['result']}")


def producer_consumer_example():
    """生产者-消费者模式示例"""

    print("\n=== 生产者-消费者模式示例 ===\n")

    import queue

    # 任务队列
    task_queue = queue.Queue()
    result_queue = queue.Queue()

    # 生产者：生成点击任务
    def producer():
        dm = DmSoft(dll_path=DLL_PATH, reg_dll_path=REG_DLL_PATH)

        # 模拟生成一些点击位置
        positions = [(100, 100), (200, 200), (300, 300), (400, 400)]

        for i, (x, y) in enumerate(positions):
            task = {"id": i, "x": x, "y": y}
            task_queue.put(task)
            print(f"[生产者] 生成任务: {task}")
            time.sleep(0.5)

        # 发送结束信号
        for _ in range(2):  # 2个消费者
            task_queue.put(None)

    # 消费者：执行点击
    def consumer(consumer_id: int):
        dm = DmSoft(dll_path=DLL_PATH, reg_dll_path=REG_DLL_PATH)

        while True:
            task = task_queue.get()
            if task is None:
                print(f"[消费者-{consumer_id}] 收到结束信号")
                break

            print(f"[消费者-{consumer_id}] 处理任务: {task}")

            # 执行点击
            dm.MoveToEx(task["x"], task["y"], 10, 10)
            dm.Delays(100, 300)
            dm.LeftClick()

            result_queue.put({"consumer_id": consumer_id, "task": task, "status": "完成"})

    # 启动生产者
    producer_thread = threading.Thread(target=producer)
    producer_thread.start()

    # 启动消费者
    consumer_threads = []
    for i in range(2):
        t = threading.Thread(target=consumer, args=(i+1,))
        consumer_threads.append(t)
        t.start()

    # 等待完成
    producer_thread.join()
    for t in consumer_threads:
        t.join()

    # 收集结果
    print("\n=== 执行结果 ===")
    while not result_queue.empty():
        print(result_queue.get())


def main():
    # 简单多线程示例
    simple_thread_example()

    # 线程池示例（需要实际图片路径才能运行）
    # thread_pool_example()

    # 生产者-消费者示例
    # producer_consumer_example()


if __name__ == "__main__":
    main()