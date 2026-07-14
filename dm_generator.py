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
    ("Reg", [("reg_code", "str"), ("ver_info", "str")], "int", "注册大漠插件（标准注册，绑定机器码）",
     {1: "成功", 2: "余额不足", -1: "无法连接网络", -2: "进程没有以管理员方式运行"}),
    ("RegEx", [("reg_code", "str"), ("ver_info", "str"), ("ip", "str")], "int", "注册大漠插件（高级注册，可指定IP）",
     {1: "成功", 2: "余额不足", -1: "无法连接网络", -2: "进程没有以管理员方式运行"}),
    ("RegNoMac", [("reg_code", "str"), ("ver_info", "str")], "int", "注册大漠插件（不绑定机器码）",
     {1: "成功", 2: "余额不足", -1: "无法连接网络", -2: "进程没有以管理员方式运行"}),
    ("RegExNoMac", [("reg_code", "str"), ("ver_info", "str"), ("ip", "str")], "int", "注册大漠插件（高级不绑定机器码）",
     {1: "成功", 2: "余额不足", -1: "无法连接网络", -2: "进程没有以管理员方式运行"}),
    ("SetExePath", [("path", "str")], "int", "设置可执行文件路径", {1: "成功", 0: "失败"}),
    ("GetID", [], "int", "获取当前对象ID", None),
    ("GetLastError", [], "int", "获取最后错误码",
     {0: "无错误", -1: "错误", -2: "进程没有以管理员方式运行"}),
    ("GetMachineCode", [], "str", "获取机器码", None),
    ("GetMachineCodeNoMac", [], "str", "获取机器码（不包含MAC地址）", None),

    # ==================== 窗口操作 ====================
    ("FindWindow", [("class_name", "str"), ("title", "str")], "int", "查找窗口",
     {0: "未找到", "其他": "窗口句柄"}),
    ("FindWindowEx", [("parent", "int"), ("class_name", "str"), ("title", "str")], "int", "查找子窗口",
     {0: "未找到", "其他": "窗口句柄"}),
    ("FindWindowByProcess", [("process_name", "str"), ("class_name", "str"), ("title", "str")], "int", "通过进程名查找窗口",
     {0: "未找到", "其他": "窗口句柄"}),
    ("FindWindowByProcessId", [("process_id", "int"), ("class_name", "str"), ("title", "str")], "int", "通过进程ID查找窗口",
     {0: "未找到", "其他": "窗口句柄"}),
    ("GetWindow", [("hwnd", "int"), ("flag", "int")], "int", "获取指定窗口",
     {0: "失败", "其他": "窗口句柄"}),
    ("GetWindowRect", [("hwnd", "int")], "str", "获取窗口矩形坐标",
     {"格式": "x1,y1,x2,y2"}),
    ("GetWindowTitle", [("hwnd", "int")], "str", "获取窗口标题",
     {"": "失败", "其他": "窗口标题"}),
    ("GetWindowClass", [("hwnd", "int")], "str", "获取窗口类名",
     {"": "失败", "其他": "窗口类名"}),
    ("GetForegroundWindow", [], "int", "获取前台窗口句柄",
     {0: "失败", "其他": "窗口句柄"}),
    ("GetForegroundFocus", [], "int", "获取焦点窗口句柄",
     {0: "失败", "其他": "窗口句柄"}),
    ("GetMousePointWindow", [], "int", "获取鼠标指向的窗口句柄",
     {0: "失败", "其他": "窗口句柄"}),
    ("GetPointWindow", [("x", "int"), ("y", "int")], "int", "获取指定坐标点的窗口句柄",
     {0: "失败", "其他": "窗口句柄"}),
    ("GetSpecialWindow", [("flag", "int")], "int", "获取特殊窗口句柄",
     {0: "桌面窗口", 1: "任务栏窗口", 2: "开始按钮", 3: "托盘窗口"}),
    ("GetWindowProcessId", [("hwnd", "int")], "int", "获取窗口所属进程ID",
     {0: "失败", "其他": "进程ID"}),
    ("GetWindowThreadId", [("hwnd", "int")], "int", "获取窗口所属线程ID",
     {0: "失败", "其他": "线程ID"}),
    ("MoveWindow", [("hwnd", "int"), ("x", "int"), ("y", "int")], "int", "移动窗口",
     {0: "失败", 1: "成功"}),
    ("SetWindowState", [("hwnd", "int"), ("flag", "int")], "int", "设置窗口状态",
     {0: "关闭", 1: "激活", 2: "最小化", 3: "最大化", 4: "还原", 5: "置顶", 6: "取消置顶", 7: "禁用", 8: "启用", 9: "隐藏", 10: "显示", 11: "闪烁标题", 12: "停止闪烁"}),
    ("SetWindowSize", [("hwnd", "int"), ("width", "int"), ("height", "int")], "int", "设置窗口大小",
     {0: "失败", 1: "成功"}),
    ("SetWindowText", [("hwnd", "int"), ("title", "str")], "int", "设置窗口标题",
     {0: "失败", 1: "成功"}),
    ("SetWindowTransparent", [("hwnd", "int"), ("trans", "int")], "int", "设置窗口透明度",
     {0: "失败", 1: "成功"}),
    ("EnumWindow", [("parent", "int"), ("title", "str"), ("class_name", "str"), ("filter", "int")], "str", "枚举窗口",
     {"": "未找到", "其他": "窗口句柄列表，格式: hwnd1,hwnd2,..."}),
    ("EnumWindowByProcess", [("process_name", "str"), ("title", "str"), ("class_name", "str"), ("filter", "int")], "str", "按进程名枚举窗口",
     {"": "未找到", "其他": "窗口句柄列表，格式: hwnd1,hwnd2,..."}),
    ("EnumWindowSuper", [("spec1", "str"), ("flag1", "int"), ("type1", "int"), ("spec2", "str"), ("flag2", "int"), ("type2", "int"), ("sort", "int")], "str", "超级枚举窗口",
     {"": "未找到", "其他": "窗口句柄列表"}),
    ("EnumProcess", [("name", "str")], "str", "枚举进程",
     {"": "未找到", "其他": "进程ID列表，格式: pid1,pid2,..."}),
    ("GetProcessInfo", [("pid", "int")], "str", "获取进程信息",
     {"": "失败", "其他": "进程信息字符串"}),

    # ==================== 鼠标操作 ====================
    ("MoveTo", [("x", "int"), ("y", "int")], "int", "移动鼠标到指定坐标",
     {0: "失败", 1: "成功"}),
    ("MoveToEx", [("x", "int"), ("y", "int"), ("w", "int"), ("h", "int")], "str", "移动到目的范围内的任意一点（防检测）",
     {"格式": "x,y", "示例": "101,102"}),
    ("MoveR", [("rx", "int"), ("ry", "int")], "int", "相对移动鼠标",
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
    ("GetCursorShapeEx", [("type", "int")], "str", "获取当前鼠标形状（扩展）",
     {"": "失败", "其他": "鼠标形状字符串"}),

    # ==================== 键盘操作 ====================
    ("KeyPress", [("key_code", "int")], "int", "按键（虚拟键码）",
     {0: "失败", 1: "成功"}),
    ("KeyDown", [("key_code", "int")], "int", "按下按键",
     {0: "失败", 1: "成功"}),
    ("KeyUp", [("key_code", "int")], "int", "弹起按键",
     {0: "失败", 1: "成功"}),
    ("WaitKey", [("key_code", "int"), ("time_out", "int")], "int", "等待按键",
     {0: "超时", 1: "成功"}),
    ("SendString", [("hwnd", "int"), ("input_str", "str")], "int", "向指定窗口发送字符串",
     {0: "失败", 1: "成功"}),
    ("SendStringIme", [("input_str", "str")], "int", "发送字符串（IME方式）",
     {0: "失败", 1: "成功"}),
    ("SendString2", [("hwnd", "int"), ("input_str", "str")], "int", "向指定窗口发送字符串（方式2）",
     {0: "失败", 1: "成功"}),

    # ==================== 找图 ====================
    ("FindPic", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                 ("pic_name", "str"), ("delta_color", "str"), ("sim", "float"), ("dir", "int")], "str", "找图",
     {"-1|-1|-1": "未找到", "其他": "x|y|index 格式，如: 100,200,0"}),
    ("FindPicE", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                  ("pic_name", "str"), ("delta_color", "str"), ("sim", "float"), ("dir", "int")], "str", "找图（易语言格式）",
     {"-1|-1|-1": "未找到", "其他": "易语言数组格式"}),
    ("FindPicEx", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                   ("pic_name", "str"), ("delta_color", "str"), ("sim", "float"), ("dir", "int")], "str", "找图（返回所有结果）",
     {"": "未找到", "其他": "多组坐标，格式: x1,y1,index1|x2,y2,index2|..."}),
    ("FindPicExS", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                    ("pic_name", "str"), ("delta_color", "str"), ("sim", "float"), ("dir", "int")], "str", "找图（返回所有结果，字符串格式）",
     {"": "未找到", "其他": "字符串格式结果"}),
    ("FindPicMem", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                    ("pic_info", "str"), ("delta_color", "str"), ("sim", "float"), ("dir", "int")], "str", "从内存中找图",
     {"-1|-1|-1": "未找到", "其他": "x|y|index 格式"}),
    ("FindPicMemE", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                     ("pic_info", "str"), ("delta_color", "str"), ("sim", "float"), ("dir", "int")], "str", "从内存中找图（易语言格式）",
     {"-1|-1|-1": "未找到", "其他": "易语言数组格式"}),
    ("FindPicMemEx", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                      ("pic_info", "str"), ("delta_color", "str"), ("sim", "float"), ("dir", "int")], "str", "从内存中找图（扩展）",
     {"": "未找到", "其他": "多组坐标"}),
    ("SetPicPwd", [("pwd", "str")], "int", "设置图片密码",
     {0: "失败", 1: "成功"}),

    # ==================== 找色 ====================
    ("FindColor", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                   ("color", "str"), ("sim", "float"), ("dir", "int")], "str", "找色",
     {"-1|-1": "未找到", "其他": "x|y 格式，如: 100,200"}),
    ("FindColorE", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                    ("color", "str"), ("sim", "float"), ("dir", "int")], "str", "找色（易语言格式）",
     {"-1|-1": "未找到", "其他": "易语言数组格式"}),
    ("FindColorEx", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                     ("color", "str"), ("sim", "float"), ("dir", "int")], "str", "找色（返回所有结果）",
     {"": "未找到", "其他": "多组坐标，格式: x1,y1|x2,y2|..."}),
    ("FindMultiColor", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                        ("first_color", "str"), ("offset_color", "str"), ("sim", "float"), ("dir", "int")], "str", "找多色",
     {"-1|-1": "未找到", "其他": "x|y 格式"}),
    ("FindMultiColorE", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                         ("first_color", "str"), ("offset_color", "str"), ("sim", "float"), ("dir", "int")], "str", "找多色（易语言格式）",
     {"-1|-1": "未找到", "其他": "易语言数组格式"}),
    ("FindMultiColorEx", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                          ("first_color", "str"), ("offset_color", "str"), ("sim", "float"), ("dir", "int")], "str", "找多色（扩展）",
     {"": "未找到", "其他": "多组坐标"}),
    ("GetColor", [("x", "int"), ("y", "int")], "str", "获取指定点颜色",
     {"格式": "RRGGBB", "示例": "FFFFFF"}),
    ("GetColorBGR", [("x", "int"), ("y", "int")], "str", "获取指定点BGR颜色",
     {"格式": "BBGGRR", "示例": "FFFFFF"}),
    ("GetAveRGB", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int")], "str", "获取区域平均颜色",
     {"格式": "RRGGBB"}),
    ("GetAveHSV", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int")], "str", "获取区域平均HSV",
     {"格式": "H.S.V"}),
    ("CmpColor", [("x", "int"), ("y", "int"), ("color", "str"), ("sim", "float")], "int", "比较颜色",
     {0: "颜色不匹配", 1: "颜色匹配"}),
    ("RGB2BGR", [("rgb_color", "str")], "str", "RGB颜色转BGR颜色",
     {"格式": "BBGGRR"}),
    ("BGR2RGB", [("bgr_color", "str")], "str", "BGR颜色转RGB颜色",
     {"格式": "RRGGBB"}),

    # ==================== 文字识别 ====================
    ("Ocr", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
             ("color_format", "str"), ("sim", "float")], "str", "文字识别",
     {"": "识别失败或未找到文字", "其他": "识别出的文字内容"}),
    ("OcrEx", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
               ("color_format", "str"), ("sim", "float")], "str", "文字识别（返回详细坐标）",
     {"": "识别失败", "其他": "格式: 文字1|x1|y1|文字2|x2|y2|..."}),
    ("OcrInFile", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                   ("color_format", "str"), ("sim", "float"), ("file_name", "str")], "str", "从文件文字识别",
     {"": "识别失败", "其他": "识别出的文字内容"}),
    ("FindStr", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                 ("string", "str"), ("color_format", "str"), ("sim", "float")], "str", "找字",
     {"-1|-1": "未找到", "其他": "x|y 格式，如: 100,200"}),
    ("FindStrE", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                  ("string", "str"), ("color_format", "str"), ("sim", "float")], "str", "找字（易语言格式）",
     {"-1|-1": "未找到", "其他": "易语言数组格式"}),
    ("FindStrEx", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                   ("string", "str"), ("color_format", "str"), ("sim", "float")], "str", "找字（返回所有结果）",
     {"": "未找到", "其他": "多组坐标，格式: x1,y1|x2,y2|..."}),
    ("FindStrExS", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                    ("string", "str"), ("color_format", "str"), ("sim", "float")], "str", "找字（返回所有结果，字符串格式）",
     {"": "未找到", "其他": "字符串格式结果"}),
    ("FindStrFast", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                     ("string", "str"), ("color_format", "str"), ("sim", "float")], "str", "快速找字",
     {"-1|-1": "未找到", "其他": "x|y 格式"}),
    ("FindStrFastE", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                      ("string", "str"), ("color_format", "str"), ("sim", "float")], "str", "快速找字（易语言格式）",
     {"-1|-1": "未找到", "其他": "易语言数组格式"}),
    ("FindStrFastEx", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                       ("string", "str"), ("color_format", "str"), ("sim", "float")], "str", "快速找字（扩展）",
     {"": "未找到", "其他": "多组坐标"}),
    ("SetDict", [("index", "int"), ("file_name", "str")], "int", "设置字库文件",
     {0: "失败", 1: "成功"}),
    ("UseDict", [("index", "int")], "int", "使用指定字库",
     {0: "失败", 1: "成功"}),
    ("GetNowDict", [], "int", "获取当前使用的字库索引",
     {"": "未设置字库", "其他": "字库索引"}),
    ("SetShowErrorMsg", [("show", "int")], "int", "设置是否显示错误信息",
     {0: "不显示", 1: "显示"}),
    ("SetShowMsg", [("x", "int"), ("y", "int"), ("color", "str"), ("size", "int"), ("msg", "str")], "int", "在屏幕上显示信息",
     {0: "失败", 1: "成功"}),

    # ==================== 窗口绑定 ====================
    ("BindWindow", [("hwnd", "int"), ("display", "str"), ("mouse", "str"), ("keypad", "str"), ("mode", "int")], "int", "绑定窗口",
     {0: "失败", 1: "成功"}),
    ("BindWindowEx", [("hwnd", "int"), ("display", "str"), ("mouse", "str"), ("keypad", "str"),
                      ("public_desc", "str"), ("mode", "int")], "int", "高级绑定窗口",
     {0: "失败", 1: "成功"}),
    ("UnBindWindow", [], "int", "解绑窗口",
     {0: "失败", 1: "成功"}),
    ("GetBindWindow", [], "int", "获取当前绑定的窗口句柄",
     {0: "未绑定", "其他": "窗口句柄"}),
    ("IsBind", [], "int", "判断是否已绑定窗口",
     {0: "未绑定", 1: "已绑定"}),
    ("GetDisplayMode", [], "str", "获取显示器分辨率",
     {"格式": "width,height", "示例": "1920,1080"}),
    ("SetDisplayInput", [("mode", "str")], "int", "设置显示输入模式",
     {0: "失败", 1: "成功"}),
    ("SetUAC", [("uac", "int")], "int", "设置UAC",
     {0: "失败", 1: "成功"}),
    ("EnableRealMouse", [("enable", "int"), ("mousedelay", "int"), ("mousestep", "int")], "int", "启用真实鼠标模拟",
     {0: "失败", 1: "成功"}),
    ("EnableRealKeypad", [("enable", "int")], "int", "启用真实键盘模拟",
     {0: "失败", 1: "成功"}),
    ("EnableKeypadMsg", [("enable", "int")], "int", "启用键盘消息",
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
        "        Args:",
        "            dll_path: dm.dll 路径，None 则使用已注册版本",
        "            reg_dll_path: DmReg.dll 路径，用于免注册调用",
        '        """',
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

        for param_name, param_type in params:
            param_defs.append(f"{param_name}: {param_type}")
            param_calls.append(param_name)
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