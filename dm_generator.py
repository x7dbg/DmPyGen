# -*- coding: UTF-8 -*-
"""
大漠插件 Python 类生成器

支持多种生成模式：
1. 内置接口模式：使用预定义的大漠接口列表（最完整，有参数提示）
2. 动态反射模式：从 COM 对象提取方法（方法名准确，但参数信息不全）
3. 混合模式：内置接口 + 动态提取的额外方法

使用方法：
    直接运行: python 09.py
    命令行:   python 09.py --dll dm.dll --reg DmReg.dll --dynamic -o dm_soft.py
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
    ("Ver", [], "str", "获取大漠插件版本号"),
    ("Reg", [("reg_code", "str"), ("ver_info", "str")], "int", "注册大漠插件（标准注册，绑定机器码）"),
    ("RegEx", [("reg_code", "str"), ("ver_info", "str"), ("ip", "str")], "int", "注册大漠插件（高级注册，可指定IP）"),
    ("RegNoMac", [("reg_code", "str"), ("ver_info", "str")], "int", "注册大漠插件（不绑定机器码）"),
    ("RegExNoMac", [("reg_code", "str"), ("ver_info", "str"), ("ip", "str")], "int", "注册大漠插件（高级不绑定机器码）"),
    ("SetExePath", [("path", "str")], "int", "设置可执行文件路径"),
    ("GetID", [], "int", "获取当前对象ID"),
    ("GetLastError", [], "int", "获取最后错误码"),
    ("GetMachineCode", [], "str", "获取机器码"),
    ("GetMachineCodeNoMac", [], "str", "获取机器码（不包含MAC地址）"),

    # ==================== 窗口操作 ====================
    ("FindWindow", [("class_name", "str"), ("title", "str")], "int", "查找窗口"),
    ("FindWindowEx", [("parent", "int"), ("class_name", "str"), ("title", "str")], "int", "查找子窗口"),
    ("FindWindowByProcess", [("process_name", "str"), ("class_name", "str"), ("title", "str")], "int", "通过进程名查找窗口"),
    ("FindWindowByProcessId", [("process_id", "int"), ("class_name", "str"), ("title", "str")], "int", "通过进程ID查找窗口"),
    ("GetWindow", [("hwnd", "int"), ("flag", "int")], "int", "获取指定窗口"),
    ("GetWindowRect", [("hwnd", "int")], "str", "获取窗口矩形坐标"),
    ("GetWindowTitle", [("hwnd", "int")], "str", "获取窗口标题"),
    ("GetWindowClass", [("hwnd", "int")], "str", "获取窗口类名"),
    ("GetForegroundWindow", [], "int", "获取前台窗口句柄"),
    ("GetForegroundFocus", [], "int", "获取焦点窗口句柄"),
    ("GetMousePointWindow", [], "int", "获取鼠标指向的窗口句柄"),
    ("GetPointWindow", [("x", "int"), ("y", "int")], "int", "获取指定坐标点的窗口句柄"),
    ("GetSpecialWindow", [("flag", "int")], "int", "获取特殊窗口句柄"),
    ("GetWindowProcessId", [("hwnd", "int")], "int", "获取窗口所属进程ID"),
    ("GetWindowThreadId", [("hwnd", "int")], "int", "获取窗口所属线程ID"),
    ("MoveWindow", [("hwnd", "int"), ("x", "int"), ("y", "int")], "int", "移动窗口"),
    ("SetWindowState", [("hwnd", "int"), ("flag", "int")], "int", "设置窗口状态（0关闭 1激活 2最小化 3最大化）"),
    ("SetWindowSize", [("hwnd", "int"), ("width", "int"), ("height", "int")], "int", "设置窗口大小"),
    ("SetWindowText", [("hwnd", "int"), ("title", "str")], "int", "设置窗口标题"),
    ("SetWindowTransparent", [("hwnd", "int"), ("trans", "int")], "int", "设置窗口透明度"),
    ("EnumWindow", [("parent", "int"), ("title", "str"), ("class_name", "str"), ("filter", "int")], "str", "枚举窗口"),
    ("EnumWindowByProcess", [("process_name", "str"), ("title", "str"), ("class_name", "str"), ("filter", "int")], "str", "按进程名枚举窗口"),
    ("EnumWindowSuper", [("spec1", "str"), ("flag1", "int"), ("type1", "int"), ("spec2", "str"), ("flag2", "int"), ("type2", "int"), ("sort", "int")], "str", "超级枚举窗口"),
    ("EnumProcess", [("name", "str")], "str", "枚举进程"),
    ("GetProcessInfo", [("pid", "int")], "str", "获取进程信息"),

    # ==================== 鼠标操作 ====================
    ("MoveTo", [("x", "int"), ("y", "int")], "int", "移动鼠标到指定坐标"),
    ("MoveToEx", [("x", "int"), ("y", "int"), ("w", "int"), ("h", "int")], "str", "移动到目的范围内的任意一点（防检测）"),
    ("MoveR", [("rx", "int"), ("ry", "int")], "int", "相对移动鼠标"),
    ("LeftClick", [], "int", "左键单击"),
    ("LeftDoubleClick", [], "int", "左键双击"),
    ("LeftDown", [], "int", "左键按下"),
    ("LeftUp", [], "int", "左键弹起"),
    ("RightClick", [], "int", "右键单击"),
    ("RightDown", [], "int", "右键按下"),
    ("RightUp", [], "int", "右键弹起"),
    ("MiddleClick", [], "int", "中键单击"),
    ("WheelDown", [], "int", "鼠标滚轮下滚"),
    ("WheelUp", [], "int", "鼠标滚轮上滚"),
    ("GetCursorPos", [], "str", "获取当前鼠标坐标"),
    ("GetCursorShape", [], "str", "获取当前鼠标形状"),
    ("GetCursorShapeEx", [("type", "int")], "str", "获取当前鼠标形状（扩展）"),

    # ==================== 键盘操作 ====================
    ("KeyPress", [("key_code", "int")], "int", "按键（虚拟键码）"),
    ("KeyDown", [("key_code", "int")], "int", "按下按键"),
    ("KeyUp", [("key_code", "int")], "int", "弹起按键"),
    ("WaitKey", [("key_code", "int"), ("time_out", "int")], "int", "等待按键"),
    ("SendString", [("hwnd", "int"), ("input_str", "str")], "int", "向指定窗口发送字符串"),
    ("SendStringIme", [("input_str", "str")], "int", "发送字符串（IME方式）"),
    ("SendString2", [("hwnd", "int"), ("input_str", "str")], "int", "向指定窗口发送字符串（方式2）"),

    # ==================== 找图 ====================
    ("FindPic", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                 ("pic_name", "str"), ("delta_color", "str"), ("sim", "float"), ("dir", "int")], "str", "找图（返回字符串格式 x|y|index）"),
    ("FindPicE", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                  ("pic_name", "str"), ("delta_color", "str"), ("sim", "float"), ("dir", "int")], "str", "找图（返回易语言格式）"),
    ("FindPicEx", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                   ("pic_name", "str"), ("delta_color", "str"), ("sim", "float"), ("dir", "int")], "str", "找图（返回所有结果）"),
    ("FindPicExS", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                    ("pic_name", "str"), ("delta_color", "str"), ("sim", "float"), ("dir", "int")], "str", "找图（返回所有结果，字符串格式）"),
    ("FindPicMem", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                    ("pic_info", "str"), ("delta_color", "str"), ("sim", "float"), ("dir", "int")], "str", "从内存中找图"),
    ("FindPicMemE", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                     ("pic_info", "str"), ("delta_color", "str"), ("sim", "float"), ("dir", "int")], "str", "从内存中找图（易语言格式）"),
    ("FindPicMemEx", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                      ("pic_info", "str"), ("delta_color", "str"), ("sim", "float"), ("dir", "int")], "str", "从内存中找图（扩展）"),
    ("SetPicPwd", [("pwd", "str")], "int", "设置图片密码"),

    # ==================== 找色 ====================
    ("FindColor", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                   ("color", "str"), ("sim", "float"), ("dir", "int")], "str", "找色（返回 x|y）"),
    ("FindColorE", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                    ("color", "str"), ("sim", "float"), ("dir", "int")], "str", "找色（易语言格式）"),
    ("FindColorEx", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                     ("color", "str"), ("sim", "float"), ("dir", "int")], "str", "找色（返回所有结果）"),
    ("FindMultiColor", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                        ("first_color", "str"), ("offset_color", "str"), ("sim", "float"), ("dir", "int")], "str", "找多色"),
    ("FindMultiColorE", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                         ("first_color", "str"), ("offset_color", "str"), ("sim", "float"), ("dir", "int")], "str", "找多色（易语言格式）"),
    ("FindMultiColorEx", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                          ("first_color", "str"), ("offset_color", "str"), ("sim", "float"), ("dir", "int")], "str", "找多色（扩展）"),
    ("GetColor", [("x", "int"), ("y", "int")], "str", "获取指定点颜色"),
    ("GetColorBGR", [("x", "int"), ("y", "int")], "str", "获取指定点BGR颜色"),
    ("GetAveRGB", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int")], "str", "获取区域平均颜色"),
    ("GetAveHSV", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int")], "str", "获取区域平均HSV"),
    ("CmpColor", [("x", "int"), ("y", "int"), ("color", "str"), ("sim", "float")], "int", "比较颜色"),
    ("RGB2BGR", [("rgb_color", "str")], "str", "RGB颜色转BGR颜色"),
    ("BGR2RGB", [("bgr_color", "str")], "str", "BGR颜色转RGB颜色"),

    # ==================== 文字识别 ====================
    ("Ocr", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
             ("color_format", "str"), ("sim", "float")], "str", "文字识别"),
    ("OcrEx", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
               ("color_format", "str"), ("sim", "float")], "str", "文字识别（返回详细坐标）"),
    ("OcrInFile", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                   ("color_format", "str"), ("sim", "float"), ("file_name", "str")], "str", "从文件文字识别"),
    ("FindStr", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                 ("string", "str"), ("color_format", "str"), ("sim", "float")], "str", "找字（返回 x|y）"),
    ("FindStrE", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                  ("string", "str"), ("color_format", "str"), ("sim", "float")], "str", "找字（易语言格式）"),
    ("FindStrEx", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                   ("string", "str"), ("color_format", "str"), ("sim", "float")], "str", "找字（返回所有结果）"),
    ("FindStrExS", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                    ("string", "str"), ("color_format", "str"), ("sim", "float")], "str", "找字（返回所有结果，字符串格式）"),
    ("FindStrFast", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                     ("string", "str"), ("color_format", "str"), ("sim", "float")], "str", "快速找字"),
    ("FindStrFastE", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                      ("string", "str"), ("color_format", "str"), ("sim", "float")], "str", "快速找字（易语言格式）"),
    ("FindStrFastEx", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"),
                       ("string", "str"), ("color_format", "str"), ("sim", "float")], "str", "快速找字（扩展）"),
    ("SetDict", [("index", "int"), ("file_name", "str")], "int", "设置字库文件"),
    ("UseDict", [("index", "int")], "int", "使用指定字库"),
    ("GetNowDict", [], "int", "获取当前使用的字库索引"),
    ("SetShowErrorMsg", [("show", "int")], "int", "设置是否显示错误信息（0不显示 1显示）"),
    ("SetShowMsg", [("x", "int"), ("y", "int"), ("color", "str"), ("size", "int"), ("msg", "str")], "int", "在屏幕上显示信息"),

    # ==================== 窗口绑定 ====================
    ("BindWindow", [("hwnd", "int"), ("display", "str"), ("mouse", "str"), ("keypad", "str"), ("mode", "int")], "int", "绑定窗口"),
    ("BindWindowEx", [("hwnd", "int"), ("display", "str"), ("mouse", "str"), ("keypad", "str"),
                      ("public_desc", "str"), ("mode", "int")], "int", "高级绑定窗口"),
    ("UnBindWindow", [], "int", "解绑窗口"),
    ("GetBindWindow", [], "int", "获取当前绑定的窗口句柄"),
    ("IsBind", [], "int", "判断是否已绑定窗口"),
    ("GetDisplayMode", [], "str", "获取显示器分辨率"),
    ("SetDisplayInput", [("mode", "str")], "int", "设置显示输入模式"),
    ("SetUAC", [("uac", "int")], "int", "设置UAC"),
    ("EnableRealMouse", [("enable", "int"), ("mousedelay", "int"), ("mousestep", "int")], "int", "启用真实鼠标模拟"),
    ("EnableRealKeypad", [("enable", "int")], "int", "启用真实键盘模拟"),
    ("EnableKeypadMsg", [("enable", "int")], "int", "启用键盘消息"),
    ("EnableMouseMsg", [("enable", "int")], "int", "启用鼠标消息"),
    ("EnableKeypadPatch", [("enable", "int")], "int", "启用键盘补丁"),
    ("EnableMouseAccuracy", [("enable", "int")], "int", "启用鼠标高精度模式"),

    # ==================== 截图 ====================
    ("Capture", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"), ("file_name", "str")], "int", "截图保存为BMP"),
    ("CapturePng", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"), ("file_name", "str")], "int", "截图保存为PNG"),
    ("CaptureJpg", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"), ("file_name", "str"), ("quality", "int")], "int", "截图保存为JPG"),
    ("CaptureGif", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"), ("file_name", "str"), ("delay", "int"), ("time", "int")], "int", "截图保存为GIF"),
    ("GetScreenData", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int")], "int", "获取屏幕数据到内存"),
    ("GetScreenDataBmp", [("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int")], "int", "获取屏幕数据（BMP格式）"),
    ("FreeScreenData", [("handle", "int")], "int", "释放屏幕数据"),
    ("SetScreen", [("width", "int"), ("height", "int"), ("depth", "int")], "int", "设置屏幕分辨率"),

    # ==================== 内存操作 ====================
    ("ReadInt", [("hwnd", "int"), ("addr", "str")], "int", "读取内存整数"),
    ("ReadFloat", [("hwnd", "int"), ("addr", "str")], "float", "读取内存浮点数"),
    ("ReadDouble", [("hwnd", "int"), ("addr", "str")], "float", "读取内存双精度浮点数"),
    ("ReadString", [("hwnd", "int"), ("addr", "str"), ("type", "int"), ("length", "int")], "str", "读取内存字符串"),
    ("WriteInt", [("hwnd", "int"), ("addr", "str"), ("value", "int")], "int", "写入内存整数"),
    ("WriteFloat", [("hwnd", "int"), ("addr", "str"), ("value", "float")], "int", "写入内存浮点数"),
    ("WriteDouble", [("hwnd", "int"), ("addr", "str"), ("value", "float")], "int", "写入内存双精度浮点数"),
    ("WriteString", [("hwnd", "int"), ("addr", "str"), ("type", "int"), ("value", "str")], "int", "写入内存字符串"),
    ("AsmCall", [("hwnd", "int"), ("asm", "str"), ("mode", "int")], "int", "执行汇编代码"),
    ("AsmCallEx", [("hwnd", "int"), ("asm", "str"), ("mode", "int"), ("param", "str")], "int", "执行汇编代码（扩展）"),
    ("GetModuleBaseAddr", [("pid", "int"), ("module_name", "str")], "int", "获取模块基址"),
    ("GetModuleBaseAddrEx", [("hwnd", "int"), ("module_name", "str")], "int", "获取模块基址（扩展）"),
    ("GetRemoteProcAddress", [("hwnd", "int"), ("base_addr", "int"), ("proc_name", "str")], "int", "获取远程进程函数地址"),
    ("SetMemoryHwndAsProcessId", [("enable", "int")], "int", "设置内存操作句柄为进程ID"),
    ("SetMemoryFindResultToFile", [("file_name", "str")], "int", "设置内存查找结果保存到文件"),

    # ==================== 设置与路径 ====================
    ("SetPath", [("path", "str")], "int", "设置全局路径"),
    ("GetPath", [], "str", "获取全局路径"),
    ("SetExitKey", [("exit_key", "int")], "int", "设置退出键"),
    ("SetClientSize", [("hwnd", "int"), ("width", "int"), ("height", "int")], "int", "设置客户区大小"),
    ("SetMouseDelay", [("type", "str"), ("delay", "int")], "int", "设置鼠标延时"),
    ("SetKeypadDelay", [("type", "str"), ("delay", "int")], "int", "设置键盘延时"),
    ("SetWordGap", [("word_gap", "int")], "int", "设置文字间隔"),
    ("SetRowGapNoDict", [("row_gap", "int")], "int", "设置无字库行间隔"),
    ("SetColGapNoDict", [("col_gap", "int")], "int", "设置无字库列间隔"),

    # ==================== 剪贴板 ====================
    ("GetClipboard", [], "str", "获取剪贴板内容"),
    ("SetClipboard", [("data", "str")], "int", "设置剪贴板内容"),

    # ==================== 进度条(Foobar) ====================
    ("FoobarCreate", [("x", "int"), ("y", "int"), ("w", "int"), ("h", "int"), ("name", "str"), ("dir", "int")], "int", "创建进度条窗口"),
    ("FoobarClose", [("hwnd", "int")], "int", "关闭进度条窗口"),
    ("FoobarClearText", [("hwnd", "int")], "int", "清除进度条文本"),
    ("FoobarPrintText", [("hwnd", "int"), ("text", "str"), ("color", "str")], "int", "在进度条打印文本"),
    ("FoobarSetFont", [("hwnd", "int"), ("font_name", "str"), ("size", "int"), ("flag", "int")], "int", "设置进度条字体"),
    ("FoobarSetSave", [("hwnd", "int"), ("file_name", "str")], "int", "设置进度条保存文件"),
    ("FoobarDrawLine", [("hwnd", "int"), ("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"), ("color", "str"), ("style", "int"), ("width", "int")], "int", "在进度条绘制线条"),
    ("FoobarDrawText", [("hwnd", "int"), ("x", "int"), ("y", "int"), ("w", "int"), ("h", "int"), ("text", "str"), ("color", "str"), ("align", "int")], "int", "在进度条绘制文本"),
    ("FoobarDrawPic", [("hwnd", "int"), ("x", "int"), ("y", "int"), ("pic_name", "str")], "int", "在进度条绘制图片"),
    ("FoobarFillRect", [("hwnd", "int"), ("x1", "int"), ("y1", "int"), ("x2", "int"), ("y2", "int"), ("color", "str")], "int", "在进度条填充矩形"),
    ("FoobarTextLineDir", [("hwnd", "int"), ("dir", "int")], "int", "设置进度条文本方向"),

    # ==================== 其他常用方法 ====================
    ("Delay", [("mis", "int")], "int", "延时（毫秒）"),
    ("Delays", [("mis_min", "int"), ("mis_max", "int")], "int", "随机延时（最小毫秒, 最大毫秒）"),
    ("LoadPic", [("pic_name", "str")], "int", "加载图片到内存"),
    ("FreePic", [("pic_name", "str")], "int", "释放内存中的图片"),
    ("GetNetTime", [], "str", "获取网络时间"),
    ("GetNetTimeSafe", [], "str", "获取网络时间（安全模式）"),
    ("CheckUAC", [], "int", "检查UAC状态"),
    ("SetParam64ToPointer", [("enable", "int")], "int", "设置64位参数转指针"),
    ("EnumIniKey", [("section", "str"), ("file_name", "str")], "str", "枚举INI文件的键"),
    ("EnumIniKeyPwd", [("section", "str"), ("file_name", "str"), ("pwd", "str")], "str", "枚举加密的INI文件键"),
    ("ReadIni", [("section", "str"), ("key", "str"), ("file_name", "str")], "str", "读取INI文件"),
    ("ReadIniPwd", [("section", "str"), ("key", "str"), ("file_name", "str"), ("pwd", "str")], "str", "读取加密的INI文件"),
    ("WriteIni", [("section", "str"), ("key", "str"), ("value", "str"), ("file_name", "str")], "int", "写入INI文件"),
    ("WriteIniPwd", [("section", "str"), ("key", "str"), ("value", "str"), ("file_name", "str"), ("pwd", "str")], "int", "写入加密的INI文件"),
    ("DeleteIni", [("section", "str"), ("key", "str"), ("file_name", "str")], "int", "删除INI文件键值"),
    ("DeleteIniPwd", [("section", "str"), ("key", "str"), ("file_name", "str"), ("pwd", "str")], "int", "删除加密的INI文件键值"),
    ("DeleteFile", [("file_name", "str")], "int", "删除文件"),
    ("MoveFile", [("src_file", "str"), ("dst_file", "str")], "int", "移动文件"),
    ("CreateFolder", [("folder_name", "str")], "int", "创建文件夹"),
    ("DeleteFolder", [("folder_name", "str")], "int", "删除文件夹"),
    ("GetFileLength", [("file_name", "str")], "int", "获取文件大小"),
    ("ReadFile", [("file_name", "str")], "str", "读取文件内容"),
    ("WriteFile", [("file_name", "str"), ("content", "str")], "int", "写入文件内容"),
    ("AppendFile", [("file_name", "str"), ("content", "str")], "int", "追加文件内容"),
    ("OpenFile", [("file_name", "str")], "int", "打开文件"),
    ("CloseFile", [("handle", "int")], "int", "关闭文件"),
    ("ReadFileData", [("handle", "int"), ("length", "int")], "str", "读取文件数据"),
    ("WriteFileData", [("handle", "int"), ("data", "str")], "int", "写入文件数据"),
    ("SeekFile", [("handle", "int"), ("offset", "int")], "int", "移动文件指针"),
    ("GetFilePointer", [("handle", "int")], "int", "获取文件指针位置"),
    ("FlushFile", [("handle", "int")], "int", "刷新文件缓冲区"),
    ("Base64Encode", [("data", "str")], "str", "Base64编码"),
    ("Base64Decode", [("data", "str")], "str", "Base64解码"),
    ("MD5", [("data", "str")], "str", "计算MD5"),
    ("GetLocale", [], "int", "获取系统区域设置"),
    ("GetLocaleAlias", [("id", "int")], "str", "获取区域设置别名"),
    ("GetOsType", [], "int", "获取操作系统类型"),
    ("GetTime", [], "int", "获取系统时间"),
    ("GetSystemInfo", [("type", "int")], "str", "获取系统信息"),
    ("SelectDirectory", [], "str", "选择文件夹对话框"),
    ("SelectFile", [], "str", "选择文件对话框"),
    ("RunApp", [("app_path", "str"), ("cmd", "str")], "int", "运行程序"),
    ("StopApp", [("pid", "int")], "int", "停止程序"),
    ("GetProcessState", [("pid", "int")], "int", "获取进程状态"),
    ("GetCommandLine", [("pid", "int")], "str", "获取进程命令行"),
    ("GetParentFolder", [("folder", "str")], "str", "获取父文件夹路径"),
    ("GetFolderPath", [("folder", "str")], "str", "获取文件夹路径"),
    ("GetDiskSerial", [], "str", "获取硬盘序列号"),
    ("GetDiskModel", [], "str", "获取硬盘型号"),
    ("GetCpuSerial", [], "str", "获取CPU序列号"),
    ("GetCpuModel", [], "str", "获取CPU型号"),
    ("GetMac", [], "str", "获取MAC地址"),
    ("GetNetIPByName", [("name", "str")], "str", "通过网卡名获取IP"),
    ("GetNetIP", [], "str", "获取本机IP地址"),
    ("GetNetIPEx", [], "str", "获取本机IP地址（扩展）"),
    ("EnableSpeedDx", [("enable", "int")], "int", "启用SpeedDX模式"),
    ("EnableFakeActive", [("enable", "int")], "int", "启用假激活模式"),
    ("SendCommand", [("cmd", "str")], "str", "发送命令"),
    ("SendCommandEx", [("cmd", "str"), ("param", "str")], "str", "发送命令（扩展）"),
    ("GetResult", [("id", "int")], "str", "获取异步结果"),
    ("FreeResult", [("id", "int")], "int", "释放异步结果"),
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

    for method_name, params, return_type, doc in methods:
        # 构建参数列表
        param_defs = ["self"]
        param_calls = []

        for param_name, param_type in params:
            param_defs.append(f"{param_name}: {param_type}")
            param_calls.append(param_name)

        param_str = ", ".join(param_defs)
        call_str = ", ".join(param_calls)

        # 生成方法
        lines.append(f"    def {method_name.lower()}(self, {', '.join(param_defs[1:])}) -> {return_type}:")
        lines.append(f'        """{doc}"""')
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