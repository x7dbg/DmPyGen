# -*- coding: UTF-8 -*-
"""
DmPyGen - 大漠插件 Python 类生成器

一键生成大漠插件(dm.dll)的 Python 封装类，包含 200+ 个接口方法，
完整的类型注解和中文注释，让你写游戏自动化脚本时有完美的代码提示！

支持多种生成模式：
    1. 内置接口模式 ⭐推荐：使用预定义的大漠接口列表（参数完整，有中文注释）
    2. 动态反射模式：从 COM 对象动态提取方法（包含最新接口，但参数信息不全）
    3. 混合模式：内置接口 + 动态提取的额外方法（兼顾完整性和准确性）

使用方法：
    【方式1】交互式菜单（推荐）
        python dm_generator.py
        按提示选择生成方式即可

    【方式2】命令行直接生成
        # 仅使用内置接口（参数完整，有中文注释）
        python dm_generator.py -o dm_soft.py

        # 混合模式（内置 + 动态提取）
        python dm_generator.py --dll ./dm.dll --reg ./DmReg.dll --dynamic -o dm_soft.py

        # 动态模式（从 COM 提取所有方法）
        python dm_generator.py --dll ./dm.dll --reg ./DmReg.dll -o dm_soft.py

    【方式3】代码中调用
        from dm_generator import generate_class

        # 生成内置接口版本
        code = generate_class(DM_INTERFACE, "DmSoft")
        with open("dm_soft.py", "w", encoding="utf-8") as f:
            f.write(code)

生成后的使用示例：
    from dm_soft import DmSoft

    # 方式1：已注册调用（需先用 regsvr32 注册 dm.dll）
    dm = DmSoft()

    # 方式2：免注册调用（指定 dm.dll 和 DmReg.dll 路径）
    dm = DmSoft(dll_path=r"C:\path\to\dm.dll", reg_dll_path=r"C:\path\to\DmReg.dll")

    # 方式3：免注册调用（只指定 dm.dll，自动找同目录的 DmReg.dll）
    dm = DmSoft(dll_path=r"C:\path\to\dm.dll")

    # 注册插件
    ret = dm.Reg("你的注册码", "")

    # 找图（有完整代码提示！）
    result = dm.FindPic(0, 0, 1920, 1080, "test.bmp", "000000", 0.9, 0)

    # 防检测随机移动
    point = dm.MoveToEx(100, 100, 50, 50)

    # 随机延时
    dm.Delays(1000, 3000)

依赖：
    pip install pywin32

项目地址：https://github.com/x7dbg/DmPyGen
许可证：MIT License
"""

import os
import sys
import argparse
import ctypes
from typing import List, Tuple, Optional

# ========== 大漠插件完整接口定义 ==========
# 基于大漠插件文档整理，包含所有方法及其参数

DM_INTERFACE = [
    # ==================== 版本与注册 ====================
    ("Ver", [], "str", "获取大漠插件版本号", None),
    ("Reg", [
        ("reg_code", "str", "注册码，从大漠官网购买获得"),
        ("ver_info", "str", "版本附加信息，一般留空即可")
    ], "int", "注册大漠插件（标准注册，绑定机器码）",
     {1: "成功", 2: "余额不足", -1: "无法连接网络", -2: "进程没有以管理员方式运行"}),
    ("RegEx", [
        ("reg_code", "str", "注册码，从大漠官网购买获得"),
        ("ver_info", "str", "版本附加信息，一般留空即可"),
        ("ip", "str", "指定IP地址，用于多机注册")
    ], "int", "注册大漠插件（高级注册，可指定IP）",
     {1: "成功", 2: "余额不足", -1: "无法连接网络", -2: "进程没有以管理员方式运行"}),
    ("RegNoMac", [
        ("reg_code", "str", "注册码，从大漠官网购买获得"),
        ("ver_info", "str", "版本附加信息，一般留空即可")
    ], "int", "注册大漠插件（不绑定机器码）",
     {1: "成功", 2: "余额不足", -1: "无法连接网络", -2: "进程没有以管理员方式运行"}),
    ("RegExNoMac", [
        ("reg_code", "str", "注册码，从大漠官网购买获得"),
        ("ver_info", "str", "版本附加信息，一般留空即可"),
        ("ip", "str", "指定IP地址，用于多机注册")
    ], "int", "注册大漠插件（高级不绑定机器码）",
     {1: "成功", 2: "余额不足", -1: "无法连接网络", -2: "进程没有以管理员方式运行"}),
    ("SetExePath", [("path", "str", "可执行文件路径，用于设置插件工作目录")], "int", "设置可执行文件路径", {1: "成功", 0: "失败"}),
    ("GetID", [], "int", "获取当前对象ID", None),
    ("GetLastError", [], "int", "获取插件命令的最后错误(必须紧跟上一句函数调用)",
     {0: "无错误",
      -1: "使用了绑定里的收费功能，但是没注册，无法使用",
      -2: "使用模式0 2时出现，目标窗口有保护（常见于win7以上系统/安全软件拦截）",
      -3: "使用模式0 2时出现，目标窗口有保护或异常错误，尝试换绑定模式",
      -4: "使用模式101 103时出现，异常错误",
      -5: "使用模式101 103时出现，关闭目标窗口重新打开再绑定，或检查管理员权限",
      -6: "被安全软件拦截（360关闭即可，金山必须卸载）",
      -7: "使用模式101 103时出现，异常错误或安全软件问题，尝试卸载360",
      -8: "使用模式101 103时出现，目标进程有保护或插件版本过老，可尝试DmGuard的np2盾",
      -9: "使用模式101 103时出现，异常错误或安全软件问题，尝试卸载360",
      -10: "使用模式101 103时出现，目标进程有保护或插件版本过老",
      -11: "使用模式101 103时出现，目标进程有保护",
      -12: "使用模式101 103时出现，目标进程有保护",
      -13: "使用模式101 103时出现，目标进程有保护或上次绑定未解绑，尝试ForceUnBindWindow",
      -14: "系统缺少部分DLL（尝试安装d3d）或鼠标键盘使用了dx.api但无设备/图色被占用",
      -16: "使用了绑定模式0和101并指定了子窗口，换模式2或103，或使用父窗口/顶级窗口",
      -17: "模式101 103时出现，异常错误",
      -18: "句柄无效",
      -19: "使用模式0 11 101时出现，异常错误",
      -20: "使用模式101 103时出现，目标进程未解绑且子绑定达最大，尝试ForceUnBindWindow",
      -21: "任何模式时出现，目标进程已存在绑定，尝试ForceUnBindWindow或检查代码",
      -22: "使用模式0 2绑定64位窗口时，安全软件拦截插件释放的EXE",
      -23: "使用模式0 2绑定64位窗口时，安全软件拦截插件释放的DLL",
      -24: "使用模式0 2绑定64位窗口时，安全软件拦截插件运行释放的EXE",
      -25: "使用模式0 2绑定64位窗口时，安全软件拦截插件运行释放的EXE",
      -26: "使用模式0 2绑定64位窗口时，目标窗口有保护（常见于win7以上系统/安全软件拦截）",
      -27: "绑定64位窗口时使用了不支持的模式，只支持模式0 2 11 13 101 103",
      -28: "绑定32位窗口时使用了不支持的模式，只支持模式0 2 11 13 101 103",
      -37: "使用模式101 103时出现，目标进程有保护",
      -38: "使用大于2的绑定模式且使用dx.public.inject.c时，分配内存失败，可尝试memory系列盾",
      -39: "使用大于2的绑定模式且使用dx.public.inject.c时，异常错误",
      -40: "使用大于2的绑定模式且使用dx.public.inject.c时，写入内存失败，可尝试memory系列盾",
      -41: "使用大于2的绑定模式且使用dx.public.inject.c时，异常错误",
      -42: "绑定时创建映射内存失败，异常错误，检查是否有同对象同时绑定或句柄泄露",
      -43: "绑定时映射内存失败，异常错误，检查进程是否内存泄漏",
      -44: "无效的参数，传递了不支持的参数",
      -45: "绑定时创建互斥信号失败，异常错误，检查进程是否有句柄泄漏",
      -100: "调用读写内存函数后，发现无效的窗口句柄",
      -101: "读写内存函数失败",
      -200: "AsmCall失败",
      -202: "AsmCall平台兼容问题"}),
    ("GetMachineCode", [], "str", "获取机器码", None),
    ("GetMachineCodeNoMac", [], "str", "获取机器码（不包含MAC地址）", None),

    # ==================== 窗口操作 ====================
    ("FindWindow", [
        ("class_name", "str", "窗口类名，可用Spy++查看，为空字符串表示匹配所有"),
        ("title", "str", "窗口标题，为空字符串表示匹配所有")
    ], "int", "查找窗口",
     {0: "未找到", "其他": "窗口句柄"}),
    ("FindWindowEx", [
        ("parent", "int", "父窗口句柄，0表示桌面窗口"),
        ("class_name", "str", "窗口类名，可用Spy++查看"),
        ("title", "str", "窗口标题，为空字符串表示匹配所有")
    ], "int", "查找子窗口",
     {0: "未找到", "其他": "窗口句柄"}),
    ("FindWindowByProcess", [
        ("process_name", "str", "进程名，如：notepad.exe"),
        ("class_name", "str", "窗口类名，为空字符串表示匹配所有"),
        ("title", "str", "窗口标题，为空字符串表示匹配所有")
    ], "int", "通过进程名查找窗口",
     {0: "未找到", "其他": "窗口句柄"}),
    ("FindWindowByProcessId", [
        ("process_id", "int", "进程ID（PID）"),
        ("class_name", "str", "窗口类名，为空字符串表示匹配所有"),
        ("title", "str", "窗口标题，为空字符串表示匹配所有")
    ], "int", "通过进程ID查找窗口",
     {0: "未找到", "其他": "窗口句柄"}),
    ("GetWindow", [
        ("hwnd", "int", "窗口句柄"),
        ("flag", "int", "获取方式：0父窗口,1第一个子窗口,2前一个兄弟窗口,3后一个兄弟窗口")
    ], "int", "获取指定窗口",
     {0: "失败", "其他": "窗口句柄"}),
    ("GetWindowRect", [("hwnd", "int", "窗口句柄")], "str", "获取窗口矩形坐标",
     {"格式": "x1,y1,x2,y2"}),
    ("GetWindowTitle", [("hwnd", "int", "窗口句柄")], "str", "获取窗口标题",
     {"": "失败", "其他": "窗口标题"}),
    ("GetWindowClass", [("hwnd", "int", "窗口句柄")], "str", "获取窗口类名",
     {"": "失败", "其他": "窗口类名"}),
    ("GetForegroundWindow", [], "int", "获取前台窗口句柄",
     {0: "失败", "其他": "窗口句柄"}),
    ("GetForegroundFocus", [], "int", "获取焦点窗口句柄",
     {0: "失败", "其他": "窗口句柄"}),
    ("GetMousePointWindow", [], "int", "获取鼠标指向的窗口句柄",
     {0: "失败", "其他": "窗口句柄"}),
    ("GetPointWindow", [
        ("x", "int", "屏幕X坐标"),
        ("y", "int", "屏幕Y坐标")
    ], "int", "获取指定坐标点的窗口句柄",
     {0: "失败", "其他": "窗口句柄"}),
    ("GetSpecialWindow", [("flag", "int", "0=桌面窗口,1=任务栏窗口,2=开始按钮,3=托盘窗口")], "int", "获取特殊窗口句柄",
     {0: "桌面窗口", 1: "任务栏窗口", 2: "开始按钮", 3: "托盘窗口"}),
    ("GetWindowProcessId", [("hwnd", "int", "窗口句柄")], "int", "获取窗口所属进程ID",
     {0: "失败", "其他": "进程ID"}),
    ("GetWindowThreadId", [("hwnd", "int", "窗口句柄")], "int", "获取窗口所属线程ID",
     {0: "失败", "其他": "线程ID"}),
    ("MoveWindow", [
        ("hwnd", "int", "窗口句柄"),
        ("x", "int", "新的X坐标"),
        ("y", "int", "新的Y坐标")
    ], "int", "移动窗口",
     {0: "失败", 1: "成功"}),
    ("SetWindowState", [
        ("hwnd", "int", "窗口句柄"),
        ("flag", "int", "0=关闭,1=激活,2=最小化,3=最大化,4=还原,5=置顶,6=取消置顶,7=禁用,8=启用,9=隐藏,10=显示,11=闪烁标题,12=停止闪烁")
    ], "int", "设置窗口状态",
     {0: "关闭", 1: "激活", 2: "最小化", 3: "最大化", 4: "还原", 5: "置顶", 6: "取消置顶", 7: "禁用", 8: "启用", 9: "隐藏", 10: "显示", 11: "闪烁标题", 12: "停止闪烁"}),
    ("SetWindowSize", [
        ("hwnd", "int", "窗口句柄"),
        ("width", "int", "新的宽度"),
        ("height", "int", "新的高度")
    ], "int", "设置窗口大小",
     {0: "失败", 1: "成功"}),
    ("SetWindowText", [
        ("hwnd", "int", "窗口句柄"),
        ("title", "str", "新的窗口标题")
    ], "int", "设置窗口标题",
     {0: "失败", 1: "成功"}),
    ("SetWindowTransparent", [
        ("hwnd", "int", "窗口句柄"),
        ("trans", "int", "透明度值，0-255，0=完全透明，255=不透明")
    ], "int", "设置窗口透明度",
     {0: "失败", 1: "成功"}),
    ("EnumWindow", [
        ("parent", "int", "父窗口句柄，0表示枚举顶级窗口"),
        ("title", "str", "窗口标题，为空字符串表示匹配所有"),
        ("class_name", "str", "窗口类名，为空字符串表示匹配所有"),
        ("filter", "int", "过滤方式：0=不过滤,1=只枚举可见窗口,2=只枚举有标题的窗口")
    ], "str", "枚举窗口",
     {"": "未找到", "其他": "窗口句柄列表，格式: hwnd1,hwnd2,..."}),
    ("EnumWindowByProcess", [
        ("process_name", "str", "进程名，如：notepad.exe"),
        ("title", "str", "窗口标题，为空字符串表示匹配所有"),
        ("class_name", "str", "窗口类名，为空字符串表示匹配所有"),
        ("filter", "int", "过滤方式：0=不过滤,1=只枚举可见窗口,2=只枚举有标题的窗口")
    ], "str", "按进程名枚举窗口",
     {"": "未找到", "其他": "窗口句柄列表，格式: hwnd1,hwnd2,..."}),
    ("EnumWindowSuper", [
        ("spec1", "str", "第一个条件，格式：类名|标题|进程名|PID"),
        ("flag1", "int", "第一个条件匹配方式：0=完全匹配,1=模糊匹配"),
        ("type1", "int", "第一个条件类型：0=类名,1=标题,2=进程名,3=PID"),
        ("spec2", "str", "第二个条件，格式同上，为空字符串表示不使用"),
        ("flag2", "int", "第二个条件匹配方式"),
        ("type2", "int", "第二个条件类型"),
        ("sort", "int", "排序方式：0=不排序,1=按窗口Z序排序")
    ], "str", "超级枚举窗口",
     {"": "未找到", "其他": "窗口句柄列表"}),
    ("EnumProcess", [("name", "str", "进程名，如：notepad.exe，为空字符串表示枚举所有进程")], "str", "枚举进程",
     {"": "未找到", "其他": "进程ID列表，格式: pid1,pid2,..."}),
    ("GetProcessInfo", [("pid", "int", "进程ID")], "str", "获取进程信息",
     {"": "失败", "其他": "进程信息字符串"}),

    # ==================== 鼠标操作 ====================
    ("MoveTo", [
        ("x", "int", "屏幕X坐标"),
        ("y", "int", "屏幕Y坐标")
    ], "int", "移动鼠标到指定坐标",
     {0: "失败", 1: "成功"}),
    ("MoveToEx", [
        ("x", "int", "目标区域左上角X坐标"),
        ("y", "int", "目标区域左上角Y坐标"),
        ("w", "int", "目标区域宽度"),
        ("h", "int", "目标区域高度")
    ], "str", "移动到目的范围内的任意一点（防检测）",
     {"格式": "x,y", "示例": "101,102"}),
    ("MoveR", [
        ("rx", "int", "相对X偏移量，正数向右负数向左"),
        ("ry", "int", "相对Y偏移量，正数向下负数向上")
    ], "int", "相对移动鼠标",
     {0: "失败", 1: "成功"}),
    ("LeftClick", [], "int", "左键单击",
     {0: "失败", 1: "成功"}),
    ("LeftDoubleClick", [], "int", "左键双击",
     {0: "失败", 1: "成功"}),
    ("LeftDown", [], "int", "左键按下",
     {0: "失败", 1: "成功"}),
    ("LeftUp", [], "int", "左键弹起",
     {0: "失败", 1: "成功"}),
    ("RightClick", [], "int", "右键单击",
     {0: "失败", 1: "成功"}),
    ("RightDown", [], "int", "右键按下",
     {0: "失败", 1: "成功"}),
    ("RightUp", [], "int", "右键弹起",
     {0: "失败", 1: "成功"}),
    ("MiddleClick", [], "int", "中键单击",
     {0: "失败", 1: "成功"}),
    ("WheelDown", [], "int", "鼠标滚轮下滚",
     {0: "失败", 1: "成功"}),
    ("WheelUp", [], "int", "鼠标滚轮上滚",
     {0: "失败", 1: "成功"}),
    ("GetCursorPos", [], "str", "获取当前鼠标坐标",
     {"格式": "x,y"}),
    ("GetCursorShape", [], "str", "获取当前鼠标形状",
     {"": "失败", "其他": "鼠标形状字符串"}),
    ("GetCursorShapeEx", [("type", "int", "类型：0=当前形状,1=当前形状+位置")], "str", "获取当前鼠标形状（扩展）",
     {"": "失败", "其他": "鼠标形状字符串"}),

    # ==================== 键盘操作 ====================
    ("KeyPress", [("key_code", "int", "虚拟键码，如：13=回车,32=空格,65=A")], "int", "按键（虚拟键码）",
     {0: "失败", 1: "成功"}),
    ("KeyDown", [("key_code", "int", "虚拟键码，如：13=回车,32=空格,65=A")], "int", "按下按键",
     {0: "失败", 1: "成功"}),
    ("KeyUp", [("key_code", "int", "虚拟键码，如：13=回车,32=空格,65=A")], "int", "弹起按键",
     {0: "失败", 1: "成功"}),
    ("WaitKey", [
        ("key_code", "int", "等待的虚拟键码"),
        ("time_out", "int", "超时时间，单位毫秒，0表示无限等待")
    ], "int", "等待按键",
     {0: "超时", 1: "成功"}),
    ("SendString", [
        ("hwnd", "int", "目标窗口句柄"),
        ("input_str", "str", "要发送的字符串")
    ], "int", "向指定窗口发送字符串",
     {0: "失败", 1: "成功"}),
    ("SendStringIme", [("input_str", "str", "要发送的字符串，支持中文")], "int", "发送字符串（IME方式）",
     {0: "失败", 1: "成功"}),
    ("SendString2", [
        ("hwnd", "int", "目标窗口句柄"),
        ("input_str", "str", "要发送的字符串")
    ], "int", "向指定窗口发送字符串（方式2）",
     {0: "失败", 1: "成功"}),

    # ==================== 找图 ====================
    ("FindPic", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("pic_name", "str", "图片名，可以是多个图片用|分隔，如：test.bmp|test2.bmp|test3.bmp"),
        ("delta_color", "str", "颜色色偏，如：203040表示RGB色偏分别是20/30/40(16进制)。如果2位表示灰度找图，如：20"),
        ("sim", "float", "相似度，取值范围0.1-1.0"),
        ("dir", "int", "查找方向：0=从左到右从上到下,1=从左到右从下到上,2=从右到左从上到下,3=从右到左从下到上")
    ], "str", "查找指定区域内的图片(位图必须是24位色格式,支持透明色,当图像上下左右4个顶点颜色一样时该颜色作为透明色处理)。只返回第一个找到的XY坐标",
     {"-1|-1|-1": "未找到", "其他": "x|y|index 格式，如: 100,200,0（index为找到的图片序号，从0开始）"}),
    ("FindPicE", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("pic_name", "str", "图片名，多个用|分隔"),
        ("delta_color", "str", "偏色，如：000000-FFFFFF表示不偏色"),
        ("sim", "float", "相似度，0.0-1.0之间"),
        ("dir", "int", "查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上")
    ], "str", "找图（易语言格式）",
     {"-1|-1|-1": "未找到", "其他": "易语言数组格式"}),
    ("FindPicEx", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("pic_name", "str", "图片名，多个用|分隔"),
        ("delta_color", "str", "偏色，如：000000-FFFFFF表示不偏色"),
        ("sim", "float", "相似度，0.0-1.0之间"),
        ("dir", "int", "查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上")
    ], "str", "找图（返回所有结果）",
     {"": "未找到", "其他": "多组坐标，格式: x1,y1,index1|x2,y2,index2|..."}),
    ("FindPicExS", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("pic_name", "str", "图片名，多个用|分隔"),
        ("delta_color", "str", "偏色，如：000000-FFFFFF表示不偏色"),
        ("sim", "float", "相似度，0.0-1.0之间"),
        ("dir", "int", "查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上")
    ], "str", "找图（返回所有结果，字符串格式）",
     {"": "未找到", "其他": "字符串格式结果"}),
    ("FindPicMem", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("pic_info", "str", "图片数据，由LoadPic加载到内存后的数据"),
        ("delta_color", "str", "偏色，如：000000-FFFFFF表示不偏色"),
        ("sim", "float", "相似度，0.0-1.0之间"),
        ("dir", "int", "查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上")
    ], "str", "从内存中找图",
     {"-1|-1|-1": "未找到", "其他": "x|y|index 格式"}),
    ("FindPicMemE", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("pic_info", "str", "图片数据，由LoadPic加载到内存后的数据"),
        ("delta_color", "str", "偏色，如：000000-FFFFFF表示不偏色"),
        ("sim", "float", "相似度，0.0-1.0之间"),
        ("dir", "int", "查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上")
    ], "str", "从内存中找图（易语言格式）",
     {"-1|-1|-1": "未找到", "其他": "易语言数组格式"}),
    ("FindPicMemEx", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("pic_info", "str", "图片数据，由LoadPic加载到内存后的数据"),
        ("delta_color", "str", "偏色，如：000000-FFFFFF表示不偏色"),
        ("sim", "float", "相似度，0.0-1.0之间"),
        ("dir", "int", "查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上")
    ], "str", "从内存中找图（扩展）",
     {"": "未找到", "其他": "多组坐标"}),
    ("SetPicPwd", [("pwd", "str")], "int", "设置图片密码",
     {0: "失败", 1: "成功"}),

    # ==================== 找色 ====================
    ("FindColor", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("color", "str", "颜色值，格式：RRGGBB，如：FFFFFF"),
        ("sim", "float", "相似度，0.0-1.0之间"),
        ("dir", "int", "查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上")
    ], "str", "找色",
     {"-1|-1": "未找到", "其他": "x|y 格式，如: 100,200"}),
    ("FindColorE", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("color", "str", "颜色值，格式：RRGGBB"),
        ("sim", "float", "相似度，0.0-1.0之间"),
        ("dir", "int", "查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上")
    ], "str", "找色（易语言格式）",
     {"-1|-1": "未找到", "其他": "易语言数组格式"}),
    ("FindColorEx", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("color", "str", "颜色值，格式：RRGGBB"),
        ("sim", "float", "相似度，0.0-1.0之间"),
        ("dir", "int", "查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上")
    ], "str", "找色（返回所有结果）",
     {"": "未找到", "其他": "多组坐标，格式: x1,y1|x2,y2|..."}),
    ("FindMultiColor", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("first_color", "str", "主颜色，格式：RRGGBB"),
        ("offset_color", "str", "偏移颜色，格式：x1-y1-颜色1|x2-y2-颜色2|..."),
        ("sim", "float", "相似度，0.0-1.0之间"),
        ("dir", "int", "查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上")
    ], "str", "找多色",
     {"-1|-1": "未找到", "其他": "x|y 格式"}),
    ("FindMultiColorE", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("first_color", "str", "主颜色，格式：RRGGBB"),
        ("offset_color", "str", "偏移颜色，格式：x1-y1-颜色1|x2-y2-颜色2|..."),
        ("sim", "float", "相似度，0.0-1.0之间"),
        ("dir", "int", "查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上")
    ], "str", "找多色（易语言格式）",
     {"-1|-1": "未找到", "其他": "易语言数组格式"}),
    ("FindMultiColorEx", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("first_color", "str", "主颜色，格式：RRGGBB"),
        ("offset_color", "str", "偏移颜色，格式：x1-y1-颜色1|x2-y2-颜色2|..."),
        ("sim", "float", "相似度，0.0-1.0之间"),
        ("dir", "int", "查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上")
    ], "str", "找多色（扩展）",
     {"": "未找到", "其他": "多组坐标"}),
    ("GetColor", [
        ("x", "int", "屏幕X坐标"),
        ("y", "int", "屏幕Y坐标")
    ], "str", "获取指定点颜色",
     {"格式": "RRGGBB", "示例": "FFFFFF"}),
    ("GetColorBGR", [
        ("x", "int", "屏幕X坐标"),
        ("y", "int", "屏幕Y坐标")
    ], "str", "获取指定点BGR颜色",
     {"格式": "BBGGRR", "示例": "FFFFFF"}),
    ("GetAveRGB", [
        ("x1", "int", "区域左上角X坐标"),
        ("y1", "int", "区域左上角Y坐标"),
        ("x2", "int", "区域右下角X坐标"),
        ("y2", "int", "区域右下角Y坐标")
    ], "str", "获取区域平均颜色",
     {"格式": "RRGGBB"}),
    ("GetAveHSV", [
        ("x1", "int", "区域左上角X坐标"),
        ("y1", "int", "区域左上角Y坐标"),
        ("x2", "int", "区域右下角X坐标"),
        ("y2", "int", "区域右下角Y坐标")
    ], "str", "获取区域平均HSV",
     {"格式": "H.S.V"}),
    ("CmpColor", [
        ("x", "int", "屏幕X坐标"),
        ("y", "int", "屏幕Y坐标"),
        ("color", "str", "要比较的颜色，格式：RRGGBB"),
        ("sim", "float", "相似度，0.0-1.0之间")
    ], "int", "比较颜色",
     {0: "颜色不匹配", 1: "颜色匹配"}),
    ("RGB2BGR", [("rgb_color", "str", "RGB颜色值，格式：RRGGBB")], "str", "RGB颜色转BGR颜色",
     {"格式": "BBGGRR"}),
    ("BGR2RGB", [("bgr_color", "str", "BGR颜色值，格式：BBGGRR")], "str", "BGR颜色转RGB颜色",
     {"格式": "RRGGBB"}),

    # ==================== 文字识别 ====================
    ("Ocr", [
        ("x1", "int", "识别区域左上角X坐标"),
        ("y1", "int", "识别区域左上角Y坐标"),
        ("x2", "int", "识别区域右下角X坐标"),
        ("y2", "int", "识别区域右下角Y坐标"),
        ("color_format", "str", "颜色格式，如：FFFFFF-000000表示白底黑字"),
        ("sim", "float", "相似度，0.0-1.0之间")
    ], "str", "文字识别",
     {"": "识别失败或未找到文字", "其他": "识别出的文字内容"}),
    ("OcrEx", [
        ("x1", "int", "识别区域左上角X坐标"),
        ("y1", "int", "识别区域左上角Y坐标"),
        ("x2", "int", "识别区域右下角X坐标"),
        ("y2", "int", "识别区域右下角Y坐标"),
        ("color_format", "str", "颜色格式，如：FFFFFF-000000表示白底黑字"),
        ("sim", "float", "相似度，0.0-1.0之间")
    ], "str", "文字识别（返回详细坐标）",
     {"": "识别失败", "其他": "格式: 文字1|x1|y1|文字2|x2|y2|..."}),
    ("OcrInFile", [
        ("x1", "int", "识别区域左上角X坐标"),
        ("y1", "int", "识别区域左上角Y坐标"),
        ("x2", "int", "识别区域右下角X坐标"),
        ("y2", "int", "识别区域右下角Y坐标"),
        ("color_format", "str", "颜色格式，如：FFFFFF-000000表示白底黑字"),
        ("sim", "float", "相似度，0.0-1.0之间"),
        ("file_name", "str", "图片文件名，从该文件识别文字")
    ], "str", "从文件文字识别",
     {"": "识别失败", "其他": "识别出的文字内容"}),
    ("FindStr", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("string", "str", "要查找的字符串"),
        ("color_format", "str", "颜色格式，如：FFFFFF-000000表示白底黑字"),
        ("sim", "float", "相似度，0.0-1.0之间")
    ], "str", "找字",
     {"-1|-1": "未找到", "其他": "x|y 格式，如: 100,200"}),
    ("FindStrE", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("string", "str", "要查找的字符串"),
        ("color_format", "str", "颜色格式，如：FFFFFF-000000表示白底黑字"),
        ("sim", "float", "相似度，0.0-1.0之间")
    ], "str", "找字（易语言格式）",
     {"-1|-1": "未找到", "其他": "易语言数组格式"}),
    ("FindStrEx", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("string", "str", "要查找的字符串"),
        ("color_format", "str", "颜色格式，如：FFFFFF-000000表示白底黑字"),
        ("sim", "float", "相似度，0.0-1.0之间")
    ], "str", "找字（返回所有结果）",
     {"": "未找到", "其他": "多组坐标，格式: x1,y1|x2,y2|..."}),
    ("FindStrExS", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("string", "str", "要查找的字符串"),
        ("color_format", "str", "颜色格式，如：FFFFFF-000000表示白底黑字"),
        ("sim", "float", "相似度，0.0-1.0之间")
    ], "str", "找字（返回所有结果，字符串格式）",
     {"": "未找到", "其他": "字符串格式结果"}),
    ("FindStrFast", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("string", "str", "要查找的字符串"),
        ("color_format", "str", "颜色格式，如：FFFFFF-000000表示白底黑字"),
        ("sim", "float", "相似度，0.0-1.0之间")
    ], "str", "快速找字",
     {"-1|-1": "未找到", "其他": "x|y 格式"}),
    ("FindStrFastE", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("string", "str", "要查找的字符串"),
        ("color_format", "str", "颜色格式，如：FFFFFF-000000表示白底黑字"),
        ("sim", "float", "相似度，0.0-1.0之间")
    ], "str", "快速找字（易语言格式）",
     {"-1|-1": "未找到", "其他": "易语言数组格式"}),
    ("FindStrFastEx", [
        ("x1", "int", "查找区域左上角X坐标"),
        ("y1", "int", "查找区域左上角Y坐标"),
        ("x2", "int", "查找区域右下角X坐标"),
        ("y2", "int", "查找区域右下角Y坐标"),
        ("string", "str", "要查找的字符串"),
        ("color_format", "str", "颜色格式，如：FFFFFF-000000表示白底黑字"),
        ("sim", "float", "相似度，0.0-1.0之间")
    ], "str", "快速找字（扩展）",
     {"": "未找到", "其他": "多组坐标"}),
    ("SetDict", [
        ("index", "int", "字库索引，0-9之间"),
        ("file_name", "str", "字库文件路径，如：C:\\test\\test.txt")
    ], "int", "设置字库文件",
     {0: "失败", 1: "成功"}),
    ("UseDict", [("index", "int", "字库索引，0-9之间")], "int", "使用指定字库",
     {0: "失败", 1: "成功"}),
    ("GetNowDict", [], "int", "获取当前使用的字库索引",
     {"": "未设置字库", "其他": "字库索引"}),
    ("SetShowErrorMsg", [("show", "int", "0=不显示,1=显示")], "int", "设置是否显示错误信息",
     {0: "不显示", 1: "显示"}),
    ("SetShowMsg", [
        ("x", "int", "显示位置X坐标"),
        ("y", "int", "显示位置Y坐标"),
        ("color", "str", "文字颜色，格式：RRGGBB"),
        ("size", "int", "字体大小"),
        ("msg", "str", "要显示的信息内容")
    ], "int", "在屏幕上显示信息",
     {0: "失败", 1: "成功"}),

    # ==================== 窗口绑定 ====================
    ("BindWindow", [
        ("hwnd", "int", "指定的窗口句柄"),
        ("display", "str", "屏幕颜色获取方式: normal=正常(前台截屏), gdi=gdi后台(Win10截图失败尝试重开目标程序), gdi2=gdi2后台(兼容性强但慢), dx2=dx2后台(部分在屏幕外,Win10截图失败尝试重开), dx3=dx3后台(后台不刷新时尝试,比dx2慢), dx=dx模式(等同BindWindowEx的dx.graphic.2d|dx.graphic.3d)"),
        ("mouse", "str", "鼠标仿真模式: normal=正常(前台), windows=模拟Windows消息(同按键后台), windows2=模拟Windows消息锁定鼠标位置, windows3=支持多子窗口的后台, dx=dx后台(锁定鼠标输入,绑定后可能需要激活窗口), dx2=dx2后台(不锁定外部鼠标输入,绑定后可能需要激活窗口)"),
        ("keypad", "str", "键盘仿真模式: normal=正常(前台), windows=模拟Windows消息(同按键后台), dx=dx后台(绑定后可能需要激活窗口)"),
        ("mode", "int", "绑定模式: 0=推荐模式(通用且后台效果最好), 2=同模式0(模式0崩溃时尝试,主绑定线程必须保持), 101=超级绑定模式(隐藏dm.dll,推荐), 103=同模式101(模式101崩溃时尝试), 11=驱动模式(特殊窗口,不支持32位), 13=驱动模式(特殊窗口,不支持32位)")
    ], "int", "绑定指定的窗口,并指定屏幕颜色获取方式,鼠标仿真模式,键盘仿真模式以及模式设定",
     {0: "失败(可调用GetLastError查看具体错误码)", 1: "成功"}),
    ("BindWindowEx", [
        ("hwnd", "int", "指定的窗口句柄"),
        ("display", "str", "屏幕颜色获取方式(支持组合用|连接): normal=正常(前台截屏), gdi=gdi后台(Win10截图失败尝试重开目标程序), gdi2=gdi2后台(兼容性强但慢), dx2=dx2后台(部分在屏幕外,Win10截图失败尝试重开), dx3=dx3后台(后台不刷新时尝试,比dx2慢), dx.graphic.2d=2d窗口dx图色, dx.graphic.2d.2=增强模式(兼容性更好), dx.graphic.3d=3d窗口dx图色, dx.graphic.3d.8=dx8图色(64位进程无效), dx.graphic.opengl=opengl图色(速度可能较慢,截图可能上下反向,可配合dx.public.graphic.revert), dx.graphic.opengl.esv2=opengl_esv2图色, dx.graphic.3d.10plus=dx10/11/12图色"),
        ("mouse", "str", "鼠标仿真模式(支持组合用|连接): normal=正常(前台), windows=模拟Windows消息(同按键后台), windows3=支持多子窗口的后台, dx.mouse.position.lock.api=封锁API锁定鼠标位置, dx.mouse.position.lock.message=封锁消息锁定鼠标位置, dx.mouse.focus.input.api=封锁API锁定输入焦点, dx.mouse.focus.input.message=封锁消息锁定输入焦点, dx.mouse.clip.lock.api=封锁API锁定刷新区域(绑定前需窗口完全显示), dx.mouse.input.lock.api=封锁API锁定鼠标输入接口, dx.mouse.state.api=封锁API锁定鼠标状态, dx.mouse.state.message=封锁消息锁定鼠标状态, dx.mouse.api=封锁API模拟dx鼠标, dx.mouse.cursor=后台获取鼠标特征码, dx.mouse.raw.input=部分窗口需要, dx.mouse.input.lock.api2=防止前台鼠标移动, dx.mouse.input.lock.api3=防止前台鼠标移动, dx.mouse.raw.input.active=配合raw.input使用(绑定前需激活窗口,非必要不用)"),
        ("keypad", "str", "键盘仿真模式(支持组合用|连接): normal=正常(前台), windows=模拟Windows消息(同按键后台), dx.keypad.input.lock.api=封锁API锁定键盘输入接口, dx.keypad.state.api=封锁API锁定键盘状态, dx.keypad.api=封锁API模拟dx键盘, dx.keypad.raw.input=部分窗口需要, dx.keypad.raw.input.active=配合raw.input使用(绑定前需激活窗口,非必要不用)"),
        ("public_desc", "str", "公共属性(支持组合用|连接,可为空): dx.public.active.api=封锁API锁定窗口激活(部分窗口耗资源慎用), dx.public.active.message=封锁消息锁定激活(绑定前需窗口激活), dx.public.disable.window.position=锁定窗口位置(不可与fake.window.min共用), dx.public.disable.window.size=禁止改变大小(不可与fake.window.min共用), dx.public.disable.window.minmax=禁止最大最小化(会置顶,不可与fake.window.min共用), dx.public.fake.window.min=最小化仍可操作(单开建议,多开混乱,可能不刷新或黑屏), dx.public.hide.dll=隐藏dm.dll(可能不稳定), dx.public.active.api2=部分窗口遮挡需要, dx.public.input.ime=配合SendStringIme使用, dx.public.graphic.protect=保护dx图色不被检测(可能导致场景重载时失效), dx.public.disable.window.show=禁止窗口显示(配合fake.window.min), dx.public.anti.api=突破部分后台保护, dx.public.km.protect=保护dx键鼠不被检测(可能导致部分功能失效), dx.public.prevent.block=避免模式1/3/5/7/101/103卡死, dx.public.ori.proc=让不同界面键鼠控制效果一致(测试无问题再用), dx.public.down.cpu=配合DownCpu降低CPU(会让图色降CPU失效), dx.public.focus.message=强制键盘消息到焦点窗口(可能导致后台键盘失灵), dx.public.graphic.speed=牺牲性能提高DX图色速度(刷新慢时有用), dx.public.memory=突破防护使用内存接口(速度取决于刷新率), dx.public.inject.super=突破难以绑定的窗口(除0/2模式), dx.public.hack.speed=配合HackSpeed变速齿轮, dx.public.inject.c=突破难以绑定的窗口(除0/2模式), dx.public.graphic.revert=截图内容上下反向(仅opengl/esv2有效)"),
        ("mode", "int", "绑定模式: 0=推荐模式(通用且后台效果最好), 2=同模式0(模式0崩溃时尝试,主绑定线程必须保持), 101=超级绑定模式(隐藏dm.dll,推荐), 103=同模式101(模式101崩溃时尝试), 11=驱动模式(特殊窗口,不支持32位), 13=驱动模式(特殊窗口,不支持32位)")
    ], "int", "绑定指定的窗口,并指定屏幕颜色获取方式,鼠标仿真模式,键盘仿真模式以及公共属性(高级用户推荐)",
     {0: "失败(可调用GetLastError查看具体错误码)", 1: "成功"}),
    ("UnBindWindow", [], "int", "解绑窗口",
     {0: "失败", 1: "成功"}),
    ("GetBindWindow", [], "int", "获取当前绑定的窗口句柄",
     {0: "未绑定", "其他": "窗口句柄"}),
    ("IsBind", [], "int", "判断是否已绑定窗口",
     {0: "未绑定", 1: "已绑定"}),
    ("GetDisplayMode", [], "str", "获取显示器分辨率",
     {"格式": "width,height", "示例": "1920,1080"}),
    ("SetDisplayInput", [("mode", "str", "输入模式：dx.mouse.input.lock|dx.mouse.input.api|dx.keypad.input.lock")], "int", "设置显示输入模式",
     {0: "失败", 1: "成功"}),
    ("SetUAC", [("uac", "int", "0=关闭UAC,1=开启UAC")], "int", "设置UAC",
     {0: "失败", 1: "成功"}),
    ("EnableRealMouse", [
        ("enable", "int", "0=关闭,1=开启"),
        ("mousedelay", "int", "鼠标移动延迟，单位毫秒"),
        ("mousestep", "int", "鼠标移动步长")
    ], "int", "启用真实鼠标模拟",
     {0: "失败", 1: "成功"}),
    ("EnableRealKeypad", [("enable", "int", "0=关闭,1=开启")], "int", "启用真实键盘模拟",
     {0: "失败", 1: "成功"}),
    ("EnableKeypadMsg", [("enable", "int", "0=关闭,1=开启")], "int", "启用键盘消息",
     {0: "失败", 1: "成功"}),
    ("EnableMouseMsg", [("enable", "int")], "int", "启用鼠标消息",
     {0: "失败", 1: "成功"}),
    ("EnableKeypadPatch", [("enable", "int")], "int", "启用键盘补丁",
     {0: "失败", 1: "成功"}),
    ("EnableMouseAccuracy", [("enable", "int")], "int", "启用鼠标高精度模式",
     {0: "失败", 1: "成功"}),

    # ==================== 截图 ====================
    ("Capture", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"), ("file_name", "str")], "int", "截图保存为BMP",
     {0: "失败", 1: "成功"}),
    ("CapturePng", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"), ("file_name", "str")], "int", "截图保存为PNG",
     {0: "失败", 1: "成功"}),
    ("CaptureJpg", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"), ("file_name", "str"), ("quality", "int")], "int", "截图保存为JPG",
     {0: "失败", 1: "成功"}),
    ("CaptureGif", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"), ("file_name", "str"), ("delay", "int"), ("time", "int")], "int", "截图保存为GIF",
     {0: "失败", 1: "成功"}),
    ("GetScreenData", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int")], "int", "获取屏幕数据到内存",
     {0: "失败", "其他": "数据句柄"}),
    ("GetScreenDataBmp", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int")], "int", "获取屏幕数据（BMP格式）",
     {0: "失败", "其他": "数据句柄"}),
    ("FreeScreenData", [("handle", "int")], "int", "释放屏幕数据",
     {0: "失败", 1: "成功"}),
    ("SetScreen", [("width", "int"), ("height", "int"), ("depth", "int")], "int", "设置屏幕分辨率",
     {0: "失败", 1: "成功"}),

    # ==================== 内存操作 ====================
    ("ReadInt", [("hwnd", "int"), ("addr", "str")], "int", "读取内存整数",
     {"其他": "读取到的整数值"}),
    ("ReadFloat", [("hwnd", "int"), ("addr", "str")], "float", "读取内存浮点数",
     {"其他": "读取到的浮点数值"}),
    ("ReadDouble", [("hwnd", "int"), ("addr", "str")], "float", "读取内存双精度浮点数",
     {"其他": "读取到的双精度浮点数值"}),
    ("ReadString", [("hwnd", "int"), ("addr", "str"), ("type", "int"), ("length", "int")], "str", "读取内存字符串",
     {"": "失败", "其他": "读取到的字符串"}),
    ("WriteInt", [("hwnd", "int"), ("addr", "str"), ("value", "int")], "int", "写入内存整数",
     {0: "失败", 1: "成功"}),
    ("WriteFloat", [("hwnd", "int"), ("addr", "str"), ("value", "float")], "int", "写入内存浮点数",
     {0: "失败", 1: "成功"}),
    ("WriteDouble", [("hwnd", "int"), ("addr", "str"), ("value", "float")], "int", "写入内存双精度浮点数",
     {0: "失败", 1: "成功"}),
    ("WriteString", [("hwnd", "int"), ("addr", "str"), ("type", "int"), ("value", "str")], "int", "写入内存字符串",
     {0: "失败", 1: "成功"}),
    ("AsmCall", [("hwnd", "int"), ("asm", "str"), ("mode", "int")], "int", "执行汇编代码",
     {0: "失败", "其他": "返回值"}),
    ("AsmCallEx", [("hwnd", "int"), ("asm", "str"), ("mode", "int"), ("param", "str")], "int", "执行汇编代码（扩展）",
     {0: "失败", "其他": "返回值"}),
    ("GetModuleBaseAddr", [("pid", "int"), ("module_name", "str")], "int", "获取模块基址",
     {0: "失败", "其他": "模块基址"}),
    ("GetModuleBaseAddrEx", [("hwnd", "int"), ("module_name", "str")], "int", "获取模块基址（扩展）",
     {0: "失败", "其他": "模块基址"}),
    ("GetRemoteProcAddress", [("hwnd", "int"), ("base_addr", "int"), ("proc_name", "str")], "int", "获取远程进程函数地址",
     {0: "失败", "其他": "函数地址"}),
    ("SetMemoryHwndAsProcessId", [("enable", "int")], "int", "设置内存操作句柄为进程ID",
     {0: "失败", 1: "成功"}),
    ("SetMemoryFindResultToFile", [("file_name", "str")], "int", "设置内存查找结果保存到文件",
     {0: "失败", 1: "成功"}),

    # ==================== 设置与路径 ====================
    ("SetPath", [("path", "str")], "int", "设置全局路径", None),
    ("GetPath", [], "str", "获取全局路径",
     {"": "未设置", "其他": "当前全局路径"}),
    ("SetExitKey", [("exit_key", "int")], "int", "设置退出键",
     {0: "失败", 1: "成功"}),
    ("SetClientSize", [("hwnd", "int"), ("width", "int"), ("height", "int")], "int", "设置客户区大小",
     {0: "失败", 1: "成功"}),
    ("SetMouseDelay", [("type", "str"), ("delay", "int")], "int", "设置鼠标延时",
     {0: "失败", 1: "成功"}),
    ("SetKeypadDelay", [("type", "str"), ("delay", "int")], "int", "设置键盘延时",
     {0: "失败", 1: "成功"}),
    ("SetWordGap", [("word_gap", "int")], "int", "设置文字间隔",
     {0: "失败", 1: "成功"}),
    ("SetRowGapNoDict", [("row_gap", "int")], "int", "设置无字库行间隔",
     {0: "失败", 1: "成功"}),
    ("SetColGapNoDict", [("col_gap", "int")], "int", "设置无字库列间隔",
     {0: "失败", 1: "成功"}),

    # ==================== 剪贴板 ====================
    ("GetClipboard", [], "str", "获取剪贴板内容",
     {"": "剪贴板为空", "其他": "剪贴板内容"}),
    ("SetClipboard", [("data", "str")], "int", "设置剪贴板内容",
     {0: "失败", 1: "成功"}),

    # ==================== 进度条(Foobar) ====================
    ("FoobarCreate", [("x", "int"), ("y", "int"), ("w", "int"), ("h", "int"), ("name", "str"), ("dir", "int")], "int", "创建进度条窗口",
     {0: "失败", "其他": "进度条窗口句柄"}),
    ("FoobarClose", [("hwnd", "int")], "int", "关闭进度条窗口",
     {0: "失败", 1: "成功"}),
    ("FoobarClearText", [("hwnd", "int")], "int", "清除进度条文本",
     {0: "失败", 1: "成功"}),
    ("FoobarPrintText", [("hwnd", "int"), ("text", "str"), ("color", "str")], "int", "在进度条打印文本",
     {0: "失败", 1: "成功"}),
    ("FoobarSetFont", [("hwnd", "int"), ("font_name", "str"), ("size", "int"), ("flag", "int")], "int", "设置进度条字体",
     {0: "失败", 1: "成功"}),
    ("FoobarSetSave", [("hwnd", "int"), ("file_name", "str")], "int", "设置进度条保存文件",
     {0: "失败", 1: "成功"}),
    ("FoobarDrawLine", [("hwnd", "int"), ("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"), ("color", "str"), ("style", "int"), ("width", "int")], "int", "在进度条绘制线条",
     {0: "失败", 1: "成功"}),
    ("FoobarDrawText", [("hwnd", "int"), ("x", "int"), ("y", "int"), ("w", "int"), ("h", "int"), ("text", "str"), ("color", "str"), ("align", "int")], "int", "在进度条绘制文本",
     {0: "失败", 1: "成功"}),
    ("FoobarDrawPic", [("hwnd", "int"), ("x", "int"), ("y", "int"), ("pic_name", "str")], "int", "在进度条绘制图片",
     {0: "失败", 1: "成功"}),
    ("FoobarFillRect", [("hwnd", "int"), ("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"), ("color", "str")], "int", "在进度条填充矩形",
     {0: "失败", 1: "成功"}),
    ("FoobarTextLineDir", [("hwnd", "int"), ("dir", "int")], "int", "设置进度条文本方向",
     {0: "失败", 1: "成功"}),

    # ==================== 其他常用方法 ====================
    ("Delay", [("mis", "int")], "int", "延时（毫秒）",
     {0: "失败", 1: "成功"}),
    ("Delays", [("mis_min", "int"), ("mis_max", "int")], "int", "随机延时（最小毫秒, 最大毫秒）",
     {0: "失败", 1: "成功"}),
    ("LoadPic", [("pic_name", "str")], "int", "加载图片到内存",
     {0: "失败", 1: "成功"}),
    ("FreePic", [("pic_name", "str")], "int", "释放内存中的图片",
     {0: "失败", 1: "成功"}),
    ("GetNetTime", [], "str", "获取网络时间",
     {"": "失败", "其他": "网络时间字符串"}),
    ("GetNetTimeSafe", [], "str", "获取网络时间（安全模式）",
     {"": "失败", "其他": "网络时间字符串"}),
    ("CheckUAC", [], "int", "检查UAC状态",
     {0: "UAC已关闭", 1: "UAC已开启"}),
    ("SetParam64ToPointer", [("enable", "int")], "int", "设置64位参数转指针",
     {0: "失败", 1: "成功"}),
    ("EnumIniKey", [("section", "str"), ("file_name", "str")], "str", "枚举INI文件的键",
     {"": "失败", "其他": "键名列表"}),
    ("EnumIniKeyPwd", [("section", "str"), ("file_name", "str"), ("pwd", "str")], "str", "枚举加密的INI文件键",
     {"": "失败", "其他": "键名列表"}),
    ("ReadIni", [("section", "str"), ("key", "str"), ("file_name", "str")], "str", "读取INI文件",
     {"": "失败或不存在", "其他": "键值"}),
    ("ReadIniPwd", [("section", "str"), ("key", "str"), ("file_name", "str"), ("pwd", "str")], "str", "读取加密的INI文件",
     {"": "失败或不存在", "其他": "键值"}),
    ("WriteIni", [("section", "str"), ("key", "str"), ("value", "str"), ("file_name", "str")], "int", "写入INI文件",
     {0: "失败", 1: "成功"}),
    ("WriteIniPwd", [("section", "str"), ("key", "str"), ("value", "str"), ("file_name", "str"), ("pwd", "str")], "int", "写入加密的INI文件",
     {0: "失败", 1: "成功"}),
    ("DeleteIni", [("section", "str"), ("key", "str"), ("file_name", "str")], "int", "删除INI文件键值",
     {0: "失败", 1: "成功"}),
    ("DeleteIniPwd", [("section", "str"), ("key", "str"), ("file_name", "str"), ("pwd", "str")], "int", "删除加密的INI文件键值",
     {0: "失败", 1: "成功"}),
    ("DeleteFile", [("file_name", "str")], "int", "删除文件",
     {0: "失败", 1: "成功"}),
    ("MoveFile", [("src_file", "str"), ("dst_file", "str")], "int", "移动文件",
     {0: "失败", 1: "成功"}),
    ("CreateFolder", [("folder_name", "str")], "int", "创建文件夹",
     {0: "失败", 1: "成功"}),
    ("DeleteFolder", [("folder_name", "str")], "int", "删除文件夹",
     {0: "失败", 1: "成功"}),
    ("GetFileLength", [("file_name", "str")], "int", "获取文件大小",
     {-1: "失败", "其他": "文件大小（字节）"}),
    ("ReadFile", [("file_name", "str")], "str", "读取文件内容",
     {"": "失败", "其他": "文件内容"}),
    ("WriteFile", [("file_name", "str"), ("content", "str")], "int", "写入文件内容",
     {0: "失败", 1: "成功"}),
    ("AppendFile", [("file_name", "str"), ("content", "str")], "int", "追加文件内容",
     {0: "失败", 1: "成功"}),
    ("OpenFile", [("file_name", "str")], "int", "打开文件",
     {0: "失败", "其他": "文件句柄"}),
    ("CloseFile", [("handle", "int")], "int", "关闭文件",
     {0: "失败", 1: "成功"}),
    ("ReadFileData", [("handle", "int"), ("length", "int")], "str", "读取文件数据",
     {"": "失败", "其他": "读取的数据"}),
    ("WriteFileData", [("handle", "int"), ("data", "str")], "int", "写入文件数据",
     {0: "失败", 1: "成功"}),
    ("SeekFile", [("handle", "int"), ("offset", "int")], "int", "移动文件指针",
     {0: "失败", 1: "成功"}),
    ("GetFilePointer", [("handle", "int")], "int", "获取文件指针位置",
     {-1: "失败", "其他": "当前指针位置"}),
    ("FlushFile", [("handle", "int")], "int", "刷新文件缓冲区",
     {0: "失败", 1: "成功"}),
    ("Base64Encode", [("data", "str")], "str", "Base64编码",
     {"": "失败", "其他": "Base64编码字符串"}),
    ("Base64Decode", [("data", "str")], "str", "Base64解码",
     {"": "失败", "其他": "解码后的字符串"}),
    ("MD5", [("data", "str")], "str", "计算MD5",
     {"": "失败", "其他": "MD5哈希值"}),
    ("GetLocale", [], "int", "获取系统区域设置",
     {"其他": "区域设置ID"}),
    ("GetLocaleAlias", [("id", "int")], "str", "获取区域设置别名",
     {"": "失败", "其他": "区域别名"}),
    ("GetOsType", [], "int", "获取操作系统类型",
     {0: "失败", "其他": "操作系统类型码"}),
    ("GetTime", [], "int", "获取系统时间",
     {"其他": "时间戳"}),
    ("GetSystemInfo", [("type", "int")], "str", "获取系统信息",
     {"": "失败", "其他": "系统信息字符串"}),
    ("SelectDirectory", [], "str", "选择文件夹对话框",
     {"": "取消", "其他": "选择的文件夹路径"}),
    ("SelectFile", [], "str", "选择文件对话框",
     {"": "取消", "其他": "选择的文件路径"}),
    ("RunApp", [("app_path", "str"), ("cmd", "str")], "int", "运行程序",
     {0: "失败", "其他": "进程ID"}),
    ("StopApp", [("pid", "int")], "int", "停止程序",
     {0: "失败", 1: "成功"}),
    ("GetProcessState", [("pid", "int")], "int", "获取进程状态",
     {0: "不存在", 1: "运行中", 2: "挂起"}),
    ("GetCommandLine", [("pid", "int")], "str", "获取进程命令行",
     {"": "失败", "其他": "命令行字符串"}),
    ("GetParentFolder", [("folder", "str")], "str", "获取父文件夹路径",
     {"": "失败", "其他": "父文件夹路径"}),
    ("GetFolderPath", [("folder", "str")], "str", "获取文件夹路径",
     {"": "失败", "其他": "文件夹路径"}),
    ("GetDiskSerial", [], "str", "获取硬盘序列号",
     {"": "失败", "其他": "硬盘序列号"}),
    ("GetDiskModel", [], "str", "获取硬盘型号",
     {"": "失败", "其他": "硬盘型号"}),
    ("GetCpuSerial", [], "str", "获取CPU序列号",
     {"": "失败", "其他": "CPU序列号"}),
    ("GetCpuModel", [], "str", "获取CPU型号",
     {"": "失败", "其他": "CPU型号"}),
    ("GetMac", [], "str", "获取MAC地址",
     {"": "失败", "其他": "MAC地址"}),
    ("GetNetIPByName", [("name", "str")], "str", "通过网卡名获取IP",
     {"": "失败", "其他": "IP地址"}),
    ("GetNetIP", [], "str", "获取本机IP地址",
     {"": "失败", "其他": "IP地址"}),
    ("GetNetIPEx", [], "str", "获取本机IP地址（扩展）",
     {"": "失败", "其他": "IP地址"}),
    ("EnableSpeedDx", [("enable", "int")], "int", "启用SpeedDX模式",
     {0: "失败", 1: "成功"}),
    ("EnableFakeActive", [("enable", "int")], "int", "启用假激活模式",
     {0: "失败", 1: "成功"}),
    ("SendCommand", [("cmd", "str")], "str", "发送命令",
     {"": "失败", "其他": "命令返回结果"}),
    ("SendCommandEx", [("cmd", "str"), ("param", "str")], "str", "发送命令（扩展）",
     {"": "失败", "其他": "命令返回结果"}),
    ("GetResult", [("id", "int")], "str", "获取异步结果",
     {"": "失败或未完成", "其他": "结果字符串"}),
    ("FreeResult", [("id", "int")], "int", "释放异步结果",
     {0: "失败", 1: "成功"}),
]


def generate_class(methods: List[Tuple], class_name: str = "DmSoft") -> str:
    """
    生成 Python 类代码

    Args:
        methods: 方法列表，每个元素为 (方法名, 参数列表, 返回类型, 文档)
        class_name: 类名

    Returns:
        生成的 Python 代码
    """

    lines = [
        "# -*- coding: UTF-8 -*-",
        '"""',
        f"大漠插件 Python 封装类",
        "自动生成，包含所有接口方法",
        '"""',
        "",
        "import ctypes",
        "import pythoncom",
        "import win32com.client",
        "from typing import Optional, Tuple, Any, List, Union",
        "",
        "",
        f"class {class_name}:",
        f'    """大漠插件封装类"""',
        "",
        "    def __init__(self, dll_path: Optional[str] = None, reg_dll_path: Optional[str] = None):",
        '        """',
        "        初始化大漠插件",
        "",
        "        支持多线程调用，每个线程创建独立实例即可",
        "        内部自动初始化COM组件",
        "",
        "        Args:",
        "            dll_path: dm.dll 路径，None 则使用已注册版本",
        "            reg_dll_path: DmReg.dll 路径，用于免注册调用",
        '        """',
        "        # 初始化当前线程的COM组件（支持多线程）",
        "        try:",
        "            pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)",
        "        except pythoncom.error:",
        "            pass  # 已经初始化过了",
        "",
        "        if dll_path and reg_dll_path:",
        "            obj = ctypes.windll.LoadLibrary(reg_dll_path)",
        "            obj.SetDllPathW(dll_path)",
        "        self._dm = win32com.client.Dispatch('dm.dmsoft')",
        "",
        "    @property",
        "    def dm(self):",
        '        """获取原始 COM 对象"""',
        "        return self._dm",
        "",
        "    @property",
        "    def version(self) -> str:",
        '        """获取大漠插件版本号"""',
        "        return self._dm.Ver()",
        "",
    ]

    for method_info in methods:
        # 兼容旧格式和新格式
        if len(method_info) == 4:
            method_name, params, return_type, doc = method_info
            returns_detail = None
        else:
            method_name, params, return_type, doc, returns_detail = method_info

        # 构建参数列表
        param_defs = ["self"]
        param_calls = []
        param_docs = []

        for param_info in params:
            if len(param_info) == 2:
                # 旧格式: (参数名, 类型)
                param_name, param_type = param_info
                param_desc = ""
            else:
                # 新格式: (参数名, 类型, 描述)
                param_name, param_type, param_desc = param_info

            param_defs.append(f"{param_name}: {param_type}")
            param_calls.append(param_name)
            if param_desc:
                param_docs.append(f"            {param_name} ({param_type}): {param_desc}")
            else:
                param_docs.append(f"            {param_name}: {param_type} 类型参数")

        param_str = ", ".join(param_defs)
        call_str = ", ".join(param_calls)

        # 构建完整文档字符串
        doc_lines = [f'        """']
        doc_lines.append(f"        {doc}")
        if param_docs:
            doc_lines.append("")
            doc_lines.append("        Args:")
            doc_lines.extend(param_docs)
        doc_lines.append("")
        doc_lines.append("        Returns:")

        # 如果有详细的返回值说明
        if returns_detail:
            return_type_desc = {
                "int": "整形数",
                "str": "字符串",
                "float": "浮点数",
                "bool": "布尔值",
                "Any": "任意类型",
                "List": "列表",
                "Tuple": "元组",
                "Union": "联合类型",
            }
            type_desc = return_type_desc.get(return_type, return_type)
            doc_lines.append(f"            {type_desc}:")
            for key, value in returns_detail.items():
                doc_lines.append(f"                {key}: {value}")
        else:
            return_type_desc = {
                "int": "整形数",
                "str": "字符串",
                "float": "浮点数",
                "bool": "布尔值",
                "Any": "任意类型",
                "List": "列表",
                "Tuple": "元组",
                "Union": "联合类型",
            }
            type_desc = return_type_desc.get(return_type, return_type)
            doc_lines.append(f"            {type_desc}: 返回值")

        doc_lines.append(f'        """')

        # 生成方法（保持原始大小写）
        lines.append(f"    def {method_name}(self, {', '.join(param_defs[1:])}) -> {return_type}:")
        lines.extend(doc_lines)
        lines.append(f"        return self._dm.{method_name}({call_str})")
        lines.append("")

    # 添加 __all__
    lines.extend([
        "",
        "",
        f"__all__ = ['{class_name}']",
        "",
        "",
        f"def create_dm(dll_path: Optional[str] = None, reg_dll_path: Optional[str] = None) -> {class_name}:",
        '    """便捷创建函数"""',
        f"    return {class_name}(dll_path, reg_dll_path)",
    ])

    return "\n".join(lines)


def extract_methods_from_com(dll_path: str, reg_dll_path: str) -> List[Tuple]:
    """
    从 COM 对象动态提取方法名
    用于补充内置接口列表中缺少的方法
    """
    # 免注册加载
    obj = ctypes.windll.LoadLibrary(reg_dll_path)
    obj.SetDllPathW(dll_path)

    import win32com.client
    dm = win32com.client.Dispatch("dm.dmsoft")

    methods = []
    for name in dir(dm):
        if name.startswith("_"):
            continue

        attr = getattr(dm, name)
        if not callable(attr):
            continue

        # 跳过已在内置列表中的方法
        if any(m[0] == name for m in DM_INTERFACE):
            continue

        methods.append((name, [], "Any", f"大漠插件方法: {name}"))

    return methods


def show_menu():
    """显示交互式菜单"""
    print("=" * 60)
    print("        大漠插件 Python 类生成器")
    print("=" * 60)
    print()
    print("生成方式选择：")
    print()
    print("  [1] 内置接口模式")
    print("      使用预定义的接口列表生成（推荐）")
    print("      优点：参数完整，有中文注释，代码提示最准确")
    print("      缺点：可能缺少最新版本的方法")
    print()
    print("  [2] 动态反射模式")
    print("      从 dm.dll 动态提取所有方法")
    print("      优点：包含所有方法，包括最新版本新增的")
    print("      缺点：参数信息不全，没有中文注释")
    print()
    print("  [3] 混合模式")
    print("      内置接口 + 动态提取的额外方法")
    print("      优点：兼顾完整性和准确性")
    print("      缺点：动态提取的方法没有参数提示")
    print()
    print("  [4] 命令行模式")
    print("      使用自定义参数生成")
    print()
    print("  [0] 退出")
    print()
    print("=" * 60)


def interactive_mode():
    """交互式模式"""
    show_menu()

    while True:
        choice = input("请选择生成方式 [0-4]: ").strip()

        if choice == "0":
            print("已退出")
            sys.exit(0)

        elif choice == "1":
            output = input("请输入输出文件名 [默认: dm_soft.py]: ").strip() or "dm_soft.py"
            print(f"\n正在使用内置接口模式生成...")
            code = generate_class(DM_INTERFACE)
            with open(output, "w", encoding="utf-8") as f:
                f.write(code)
            print(f"生成完成: {os.path.abspath(output)}")
            print(f"共 {len(DM_INTERFACE)} 个方法")
            print(f"使用方法: from {os.path.splitext(output)[0]} import DmSoft")
            break

        elif choice == "2":
            dll_path = input("请输入 dm.dll 路径: ").strip()
            reg_dll_path = input("请输入 DmReg.dll 路径: ").strip()
            output = input("请输入输出文件名 [默认: dm_soft.py]: ").strip() or "dm_soft.py"

            if not os.path.exists(dll_path):
                print(f"错误: 找不到文件 {dll_path}")
                continue
            if not os.path.exists(reg_dll_path):
                print(f"错误: 找不到文件 {reg_dll_path}")
                continue

            print(f"\n正在从 COM 对象提取方法...")
            try:
                dynamic_methods = extract_methods_from_com(dll_path, reg_dll_path)
                print(f"提取到 {len(dynamic_methods)} 个方法")
                code = generate_class(dynamic_methods)
                with open(output, "w", encoding="utf-8") as f:
                    f.write(code)
                print(f"生成完成: {os.path.abspath(output)}")
                print(f"使用方法: from {os.path.splitext(output)[0]} import DmSoft")
                break
            except Exception as e:
                print(f"生成失败: {e}")

        elif choice == "3":
            dll_path = input("请输入 dm.dll 路径: ").strip()
            reg_dll_path = input("请输入 DmReg.dll 路径: ").strip()
            output = input("请输入输出文件名 [默认: dm_soft.py]: ").strip() or "dm_soft.py"

            if not os.path.exists(dll_path):
                print(f"错误: 找不到文件 {dll_path}")
                continue
            if not os.path.exists(reg_dll_path):
                print(f"错误: 找不到文件 {reg_dll_path}")
                continue

            print(f"\n正在使用混合模式生成...")
            all_methods = list(DM_INTERFACE)

            try:
                dynamic_methods = extract_methods_from_com(dll_path, reg_dll_path)
                all_methods.extend(dynamic_methods)
                print(f"内置接口: {len(DM_INTERFACE)} 个")
                print(f"动态提取: {len(dynamic_methods)} 个")
                print(f"总计: {len(all_methods)} 个方法")
            except Exception as e:
                print(f"动态提取失败，仅使用内置接口: {e}")

            code = generate_class(all_methods)
            with open(output, "w", encoding="utf-8") as f:
                f.write(code)
            print(f"生成完成: {os.path.abspath(output)}")
            print(f"使用方法: from {os.path.splitext(output)[0]} import DmSoft")
            break

        elif choice == "4":
            print("\n命令行模式，请输入参数（直接回车使用默认值）")
            dll_path = input("dm.dll 路径 [可选]: ").strip() or None
            reg_dll_path = input("DmReg.dll 路径 [可选]: ").strip() or None
            output = input("输出文件名 [默认: dm_soft.py]: ").strip() or "dm_soft.py"

            all_methods = list(DM_INTERFACE)

            if dll_path and reg_dll_path and os.path.exists(dll_path) and os.path.exists(reg_dll_path):
                use_dynamic = input("是否同时提取动态方法 [y/N]: ").strip().lower() == "y"
                if use_dynamic:
                    try:
                        dynamic_methods = extract_methods_from_com(dll_path, reg_dll_path)
                        all_methods.extend(dynamic_methods)
                        print(f"提取到 {len(dynamic_methods)} 个额外方法")
                    except Exception as e:
                        print(f"动态提取失败: {e}")

            code = generate_class(all_methods)
            with open(output, "w", encoding="utf-8") as f:
                f.write(code)
            print(f"生成完成: {os.path.abspath(output)}")
            print(f"共 {len(all_methods)} 个方法")
            print(f"使用方法: from {os.path.splitext(output)[0]} import DmSoft")
            break

        else:
            print("无效选择，请重新输入")


def main():
    # 如果有命令行参数，使用命令行模式
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="大漠插件 Python 类生成器")
        parser.add_argument("--dll", help="dm.dll 路径")
        parser.add_argument("--reg", help="DmReg.dll 路径")
        parser.add_argument("-o", "--output", default="dm_soft.py", help="输出文件路径")
        parser.add_argument("--dynamic", action="store_true", help="同时提取 COM 动态方法")

        args = parser.parse_args()

        # 合并内置方法和动态提取的方法
        all_methods = list(DM_INTERFACE)

        if args.dynamic and args.dll and args.reg:
            print("正在从 COM 对象提取额外方法...")
            try:
                dynamic_methods = extract_methods_from_com(args.dll, args.reg)
                all_methods.extend(dynamic_methods)
                print(f"提取到 {len(dynamic_methods)} 个额外方法")
            except Exception as e:
                print(f"动态提取失败: {e}")

        # 生成代码
        print(f"正在生成类文件，共 {len(all_methods)} 个方法...")
        code = generate_class(all_methods)

        # 写入文件
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(code)

        print(f"生成完成: {os.path.abspath(args.output)}")
        print(f"使用方法: from {os.path.splitext(args.output)[0]} import DmSoft")

    else:
        # 没有参数，进入交互式模式
        interactive_mode()


if __name__ == "__main__":
    main()