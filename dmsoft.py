# -*- coding: UTF-8 -*-
"""
大漠插件 Python 封装类
自动生成，包含所有接口方法
"""

import ctypes
import pythoncom
import win32com.client
from typing import Optional, Tuple, Any, List, Union


class DmSoft:
    """大漠插件封装类"""

    def __init__(self, dll_path: Optional[str] = None, reg_dll_path: Optional[str] = None):
        """
        初始化大漠插件

        支持多线程调用，每个线程创建独立实例即可
        内部自动初始化COM组件

        Args:
            dll_path: dm.dll 路径，None 则使用已注册版本
            reg_dll_path: DmReg.dll 路径，用于免注册调用
        """
        # 初始化当前线程的COM组件（支持多线程）
        try:
            pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
        except pythoncom.error:
            pass  # 已经初始化过了

        if dll_path and reg_dll_path:
            obj = ctypes.windll.LoadLibrary(reg_dll_path)
            obj.SetDllPathW(dll_path)
        self._dm = win32com.client.Dispatch('dm.dmsoft')

    @property
    def dm(self):
        """获取原始 COM 对象"""
        return self._dm

    @property
    def version(self) -> str:
        """获取大漠插件版本号"""
        return self._dm.Ver()

    def Ver(self, ) -> str:
        """
        获取大漠插件版本号

        Returns:
            字符串: 返回值
        """
        return self._dm.Ver()

    def Reg(self, reg_code: str, ver_info: str) -> int:
        """
        注册大漠插件（标准注册，绑定机器码）

        Args:
            reg_code (str): 注册码，从大漠官网购买获得
            ver_info (str): 版本附加信息，一般留空即可

        Returns:
            整形数:
                1: 成功
                2: 余额不足
                -1: 无法连接网络
                -2: 进程没有以管理员方式运行
        """
        return self._dm.Reg(reg_code, ver_info)

    def RegEx(self, reg_code: str, ver_info: str, ip: str) -> int:
        """
        注册大漠插件（高级注册，可指定IP）

        Args:
            reg_code (str): 注册码，从大漠官网购买获得
            ver_info (str): 版本附加信息，一般留空即可
            ip (str): 指定IP地址，用于多机注册

        Returns:
            整形数:
                1: 成功
                2: 余额不足
                -1: 无法连接网络
                -2: 进程没有以管理员方式运行
        """
        return self._dm.RegEx(reg_code, ver_info, ip)

    def RegNoMac(self, reg_code: str, ver_info: str) -> int:
        """
        注册大漠插件（不绑定机器码）

        Args:
            reg_code (str): 注册码，从大漠官网购买获得
            ver_info (str): 版本附加信息，一般留空即可

        Returns:
            整形数:
                1: 成功
                2: 余额不足
                -1: 无法连接网络
                -2: 进程没有以管理员方式运行
        """
        return self._dm.RegNoMac(reg_code, ver_info)

    def RegExNoMac(self, reg_code: str, ver_info: str, ip: str) -> int:
        """
        注册大漠插件（高级不绑定机器码）

        Args:
            reg_code (str): 注册码，从大漠官网购买获得
            ver_info (str): 版本附加信息，一般留空即可
            ip (str): 指定IP地址，用于多机注册

        Returns:
            整形数:
                1: 成功
                2: 余额不足
                -1: 无法连接网络
                -2: 进程没有以管理员方式运行
        """
        return self._dm.RegExNoMac(reg_code, ver_info, ip)

    def SetExePath(self, path: str) -> int:
        """
        设置可执行文件路径

        Args:
            path (str): 可执行文件路径，用于设置插件工作目录

        Returns:
            整形数:
                1: 成功
                0: 失败
        """
        return self._dm.SetExePath(path)

    def GetID(self, ) -> int:
        """
        获取当前对象ID

        Returns:
            整形数: 返回值
        """
        return self._dm.GetID()

    def GetLastError(self, ) -> int:
        """
        获取插件命令的最后错误(必须紧跟上一句函数调用)

        Returns:
            整形数:
                0: 无错误
                -1: 使用了绑定里的收费功能，但是没注册，无法使用
                -2: 使用模式0 2时出现，目标窗口有保护（常见于win7以上系统/安全软件拦截）
                -3: 使用模式0 2时出现，目标窗口有保护或异常错误，尝试换绑定模式
                -4: 使用模式101 103时出现，异常错误
                -5: 使用模式101 103时出现，关闭目标窗口重新打开再绑定，或检查管理员权限
                -6: 被安全软件拦截（360关闭即可，金山必须卸载）
                -7: 使用模式101 103时出现，异常错误或安全软件问题，尝试卸载360
                -8: 使用模式101 103时出现，目标进程有保护或插件版本过老，可尝试DmGuard的np2盾
                -9: 使用模式101 103时出现，异常错误或安全软件问题，尝试卸载360
                -10: 使用模式101 103时出现，目标进程有保护或插件版本过老
                -11: 使用模式101 103时出现，目标进程有保护
                -12: 使用模式101 103时出现，目标进程有保护
                -13: 使用模式101 103时出现，目标进程有保护或上次绑定未解绑，尝试ForceUnBindWindow
                -14: 系统缺少部分DLL（尝试安装d3d）或鼠标键盘使用了dx.api但无设备/图色被占用
                -16: 使用了绑定模式0和101并指定了子窗口，换模式2或103，或使用父窗口/顶级窗口
                -17: 模式101 103时出现，异常错误
                -18: 句柄无效
                -19: 使用模式0 11 101时出现，异常错误
                -20: 使用模式101 103时出现，目标进程未解绑且子绑定达最大，尝试ForceUnBindWindow
                -21: 任何模式时出现，目标进程已存在绑定，尝试ForceUnBindWindow或检查代码
                -22: 使用模式0 2绑定64位窗口时，安全软件拦截插件释放的EXE
                -23: 使用模式0 2绑定64位窗口时，安全软件拦截插件释放的DLL
                -24: 使用模式0 2绑定64位窗口时，安全软件拦截插件运行释放的EXE
                -25: 使用模式0 2绑定64位窗口时，安全软件拦截插件运行释放的EXE
                -26: 使用模式0 2绑定64位窗口时，目标窗口有保护（常见于win7以上系统/安全软件拦截）
                -27: 绑定64位窗口时使用了不支持的模式，只支持模式0 2 11 13 101 103
                -28: 绑定32位窗口时使用了不支持的模式，只支持模式0 2 11 13 101 103
                -37: 使用模式101 103时出现，目标进程有保护
                -38: 使用大于2的绑定模式且使用dx.public.inject.c时，分配内存失败，可尝试memory系列盾
                -39: 使用大于2的绑定模式且使用dx.public.inject.c时，异常错误
                -40: 使用大于2的绑定模式且使用dx.public.inject.c时，写入内存失败，可尝试memory系列盾
                -41: 使用大于2的绑定模式且使用dx.public.inject.c时，异常错误
                -42: 绑定时创建映射内存失败，异常错误，检查是否有同对象同时绑定或句柄泄露
                -43: 绑定时映射内存失败，异常错误，检查进程是否内存泄漏
                -44: 无效的参数，传递了不支持的参数
                -45: 绑定时创建互斥信号失败，异常错误，检查进程是否有句柄泄漏
                -100: 调用读写内存函数后，发现无效的窗口句柄
                -101: 读写内存函数失败
                -200: AsmCall失败
                -202: AsmCall平台兼容问题
        """
        return self._dm.GetLastError()

    def GetMachineCode(self, ) -> str:
        """
        获取机器码

        Returns:
            字符串: 返回值
        """
        return self._dm.GetMachineCode()

    def GetMachineCodeNoMac(self, ) -> str:
        """
        获取机器码（不包含MAC地址）

        Returns:
            字符串: 返回值
        """
        return self._dm.GetMachineCodeNoMac()

    def FindWindow(self, class_name: str, title: str) -> int:
        """
        查找窗口

        Args:
            class_name (str): 窗口类名，可用Spy++查看，为空字符串表示匹配所有
            title (str): 窗口标题，为空字符串表示匹配所有

        Returns:
            整形数:
                0: 未找到
                其他: 窗口句柄
        """
        return self._dm.FindWindow(class_name, title)

    def FindWindowEx(self, parent: int, class_name: str, title: str) -> int:
        """
        查找子窗口

        Args:
            parent (int): 父窗口句柄，0表示桌面窗口
            class_name (str): 窗口类名，可用Spy++查看
            title (str): 窗口标题，为空字符串表示匹配所有

        Returns:
            整形数:
                0: 未找到
                其他: 窗口句柄
        """
        return self._dm.FindWindowEx(parent, class_name, title)

    def FindWindowByProcess(self, process_name: str, class_name: str, title: str) -> int:
        """
        通过进程名查找窗口

        Args:
            process_name (str): 进程名，如：notepad.exe
            class_name (str): 窗口类名，为空字符串表示匹配所有
            title (str): 窗口标题，为空字符串表示匹配所有

        Returns:
            整形数:
                0: 未找到
                其他: 窗口句柄
        """
        return self._dm.FindWindowByProcess(process_name, class_name, title)

    def FindWindowByProcessId(self, process_id: int, class_name: str, title: str) -> int:
        """
        通过进程ID查找窗口

        Args:
            process_id (int): 进程ID（PID）
            class_name (str): 窗口类名，为空字符串表示匹配所有
            title (str): 窗口标题，为空字符串表示匹配所有

        Returns:
            整形数:
                0: 未找到
                其他: 窗口句柄
        """
        return self._dm.FindWindowByProcessId(process_id, class_name, title)

    def GetWindow(self, hwnd: int, flag: int) -> int:
        """
        获取指定窗口

        Args:
            hwnd (int): 窗口句柄
            flag (int): 获取方式：0父窗口,1第一个子窗口,2前一个兄弟窗口,3后一个兄弟窗口

        Returns:
            整形数:
                0: 失败
                其他: 窗口句柄
        """
        return self._dm.GetWindow(hwnd, flag)

    def GetWindowRect(self, hwnd: int) -> str:
        """
        获取窗口矩形坐标

        Args:
            hwnd (int): 窗口句柄

        Returns:
            字符串:
                格式: x1,y1,x2,y2
        """
        return self._dm.GetWindowRect(hwnd)

    def GetWindowTitle(self, hwnd: int) -> str:
        """
        获取窗口标题

        Args:
            hwnd (int): 窗口句柄

        Returns:
            字符串:
                : 失败
                其他: 窗口标题
        """
        return self._dm.GetWindowTitle(hwnd)

    def GetWindowClass(self, hwnd: int) -> str:
        """
        获取窗口类名

        Args:
            hwnd (int): 窗口句柄

        Returns:
            字符串:
                : 失败
                其他: 窗口类名
        """
        return self._dm.GetWindowClass(hwnd)

    def GetForegroundWindow(self, ) -> int:
        """
        获取前台窗口句柄

        Returns:
            整形数:
                0: 失败
                其他: 窗口句柄
        """
        return self._dm.GetForegroundWindow()

    def GetForegroundFocus(self, ) -> int:
        """
        获取焦点窗口句柄

        Returns:
            整形数:
                0: 失败
                其他: 窗口句柄
        """
        return self._dm.GetForegroundFocus()

    def GetMousePointWindow(self, ) -> int:
        """
        获取鼠标指向的窗口句柄

        Returns:
            整形数:
                0: 失败
                其他: 窗口句柄
        """
        return self._dm.GetMousePointWindow()

    def GetPointWindow(self, x: int, y: int) -> int:
        """
        获取指定坐标点的窗口句柄

        Args:
            x (int): 屏幕X坐标
            y (int): 屏幕Y坐标

        Returns:
            整形数:
                0: 失败
                其他: 窗口句柄
        """
        return self._dm.GetPointWindow(x, y)

    def GetSpecialWindow(self, flag: int) -> int:
        """
        获取特殊窗口句柄

        Args:
            flag (int): 0=桌面窗口,1=任务栏窗口,2=开始按钮,3=托盘窗口

        Returns:
            整形数:
                0: 桌面窗口
                1: 任务栏窗口
                2: 开始按钮
                3: 托盘窗口
        """
        return self._dm.GetSpecialWindow(flag)

    def GetWindowProcessId(self, hwnd: int) -> int:
        """
        获取窗口所属进程ID

        Args:
            hwnd (int): 窗口句柄

        Returns:
            整形数:
                0: 失败
                其他: 进程ID
        """
        return self._dm.GetWindowProcessId(hwnd)

    def GetWindowThreadId(self, hwnd: int) -> int:
        """
        获取窗口所属线程ID

        Args:
            hwnd (int): 窗口句柄

        Returns:
            整形数:
                0: 失败
                其他: 线程ID
        """
        return self._dm.GetWindowThreadId(hwnd)

    def MoveWindow(self, hwnd: int, x: int, y: int) -> int:
        """
        移动窗口

        Args:
            hwnd (int): 窗口句柄
            x (int): 新的X坐标
            y (int): 新的Y坐标

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.MoveWindow(hwnd, x, y)

    def SetWindowState(self, hwnd: int, flag: int) -> int:
        """
        设置窗口状态

        Args:
            hwnd (int): 窗口句柄
            flag (int): 0=关闭,1=激活,2=最小化,3=最大化,4=还原,5=置顶,6=取消置顶,7=禁用,8=启用,9=隐藏,10=显示,11=闪烁标题,12=停止闪烁

        Returns:
            整形数:
                0: 关闭
                1: 激活
                2: 最小化
                3: 最大化
                4: 还原
                5: 置顶
                6: 取消置顶
                7: 禁用
                8: 启用
                9: 隐藏
                10: 显示
                11: 闪烁标题
                12: 停止闪烁
        """
        return self._dm.SetWindowState(hwnd, flag)

    def SetWindowSize(self, hwnd: int, width: int, height: int) -> int:
        """
        设置窗口大小

        Args:
            hwnd (int): 窗口句柄
            width (int): 新的宽度
            height (int): 新的高度

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetWindowSize(hwnd, width, height)

    def SetWindowText(self, hwnd: int, title: str) -> int:
        """
        设置窗口标题

        Args:
            hwnd (int): 窗口句柄
            title (str): 新的窗口标题

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetWindowText(hwnd, title)

    def SetWindowTransparent(self, hwnd: int, trans: int) -> int:
        """
        设置窗口透明度

        Args:
            hwnd (int): 窗口句柄
            trans (int): 透明度值，0-255，0=完全透明，255=不透明

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetWindowTransparent(hwnd, trans)

    def EnumWindow(self, parent: int, title: str, class_name: str, filter: int) -> str:
        """
        枚举窗口

        Args:
            parent (int): 父窗口句柄，0表示枚举顶级窗口
            title (str): 窗口标题，为空字符串表示匹配所有
            class_name (str): 窗口类名，为空字符串表示匹配所有
            filter (int): 过滤方式：0=不过滤,1=只枚举可见窗口,2=只枚举有标题的窗口

        Returns:
            字符串:
                : 未找到
                其他: 窗口句柄列表，格式: hwnd1,hwnd2,...
        """
        return self._dm.EnumWindow(parent, title, class_name, filter)

    def EnumWindowByProcess(self, process_name: str, title: str, class_name: str, filter: int) -> str:
        """
        按进程名枚举窗口

        Args:
            process_name (str): 进程名，如：notepad.exe
            title (str): 窗口标题，为空字符串表示匹配所有
            class_name (str): 窗口类名，为空字符串表示匹配所有
            filter (int): 过滤方式：0=不过滤,1=只枚举可见窗口,2=只枚举有标题的窗口

        Returns:
            字符串:
                : 未找到
                其他: 窗口句柄列表，格式: hwnd1,hwnd2,...
        """
        return self._dm.EnumWindowByProcess(process_name, title, class_name, filter)

    def EnumWindowSuper(self, spec1: str, flag1: int, type1: int, spec2: str, flag2: int, type2: int, sort: int) -> str:
        """
        超级枚举窗口

        Args:
            spec1 (str): 第一个条件，格式：类名|标题|进程名|PID
            flag1 (int): 第一个条件匹配方式：0=完全匹配,1=模糊匹配
            type1 (int): 第一个条件类型：0=类名,1=标题,2=进程名,3=PID
            spec2 (str): 第二个条件，格式同上，为空字符串表示不使用
            flag2 (int): 第二个条件匹配方式
            type2 (int): 第二个条件类型
            sort (int): 排序方式：0=不排序,1=按窗口Z序排序

        Returns:
            字符串:
                : 未找到
                其他: 窗口句柄列表
        """
        return self._dm.EnumWindowSuper(spec1, flag1, type1, spec2, flag2, type2, sort)

    def EnumProcess(self, name: str) -> str:
        """
        枚举进程

        Args:
            name (str): 进程名，如：notepad.exe，为空字符串表示枚举所有进程

        Returns:
            字符串:
                : 未找到
                其他: 进程ID列表，格式: pid1,pid2,...
        """
        return self._dm.EnumProcess(name)

    def GetProcessInfo(self, pid: int) -> str:
        """
        获取进程信息

        Args:
            pid (int): 进程ID

        Returns:
            字符串:
                : 失败
                其他: 进程信息字符串
        """
        return self._dm.GetProcessInfo(pid)

    def MoveTo(self, x: int, y: int) -> int:
        """
        移动鼠标到指定坐标

        Args:
            x (int): 屏幕X坐标
            y (int): 屏幕Y坐标

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.MoveTo(x, y)

    def MoveToEx(self, x: int, y: int, w: int, h: int) -> str:
        """
        移动到目的范围内的任意一点（防检测）

        Args:
            x (int): 目标区域左上角X坐标
            y (int): 目标区域左上角Y坐标
            w (int): 目标区域宽度
            h (int): 目标区域高度

        Returns:
            字符串:
                格式: x,y
                示例: 101,102
        """
        return self._dm.MoveToEx(x, y, w, h)

    def MoveR(self, rx: int, ry: int) -> int:
        """
        相对移动鼠标

        Args:
            rx (int): 相对X偏移量，正数向右负数向左
            ry (int): 相对Y偏移量，正数向下负数向上

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.MoveR(rx, ry)

    def LeftClick(self, ) -> int:
        """
        左键单击

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.LeftClick()

    def LeftDoubleClick(self, ) -> int:
        """
        左键双击

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.LeftDoubleClick()

    def LeftDown(self, ) -> int:
        """
        左键按下

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.LeftDown()

    def LeftUp(self, ) -> int:
        """
        左键弹起

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.LeftUp()

    def RightClick(self, ) -> int:
        """
        右键单击

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.RightClick()

    def RightDown(self, ) -> int:
        """
        右键按下

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.RightDown()

    def RightUp(self, ) -> int:
        """
        右键弹起

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.RightUp()

    def MiddleClick(self, ) -> int:
        """
        中键单击

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.MiddleClick()

    def WheelDown(self, ) -> int:
        """
        鼠标滚轮下滚

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.WheelDown()

    def WheelUp(self, ) -> int:
        """
        鼠标滚轮上滚

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.WheelUp()

    def GetCursorPos(self, ) -> str:
        """
        获取当前鼠标坐标

        Returns:
            字符串:
                格式: x,y
        """
        return self._dm.GetCursorPos()

    def GetCursorShape(self, ) -> str:
        """
        获取当前鼠标形状

        Returns:
            字符串:
                : 失败
                其他: 鼠标形状字符串
        """
        return self._dm.GetCursorShape()

    def GetCursorShapeEx(self, type: int) -> str:
        """
        获取当前鼠标形状（扩展）

        Args:
            type (int): 类型：0=当前形状,1=当前形状+位置

        Returns:
            字符串:
                : 失败
                其他: 鼠标形状字符串
        """
        return self._dm.GetCursorShapeEx(type)

    def KeyPress(self, key_code: int) -> int:
        """
        按键（虚拟键码）

        Args:
            key_code (int): 虚拟键码，如：13=回车,32=空格,65=A

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.KeyPress(key_code)

    def KeyDown(self, key_code: int) -> int:
        """
        按下按键

        Args:
            key_code (int): 虚拟键码，如：13=回车,32=空格,65=A

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.KeyDown(key_code)

    def KeyUp(self, key_code: int) -> int:
        """
        弹起按键

        Args:
            key_code (int): 虚拟键码，如：13=回车,32=空格,65=A

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.KeyUp(key_code)

    def WaitKey(self, key_code: int, time_out: int) -> int:
        """
        等待按键

        Args:
            key_code (int): 等待的虚拟键码
            time_out (int): 超时时间，单位毫秒，0表示无限等待

        Returns:
            整形数:
                0: 超时
                1: 成功
        """
        return self._dm.WaitKey(key_code, time_out)

    def SendString(self, hwnd: int, input_str: str) -> int:
        """
        向指定窗口发送字符串

        Args:
            hwnd (int): 目标窗口句柄
            input_str (str): 要发送的字符串

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SendString(hwnd, input_str)

    def SendStringIme(self, input_str: str) -> int:
        """
        发送字符串（IME方式）

        Args:
            input_str (str): 要发送的字符串，支持中文

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SendStringIme(input_str)

    def SendString2(self, hwnd: int, input_str: str) -> int:
        """
        向指定窗口发送字符串（方式2）

        Args:
            hwnd (int): 目标窗口句柄
            input_str (str): 要发送的字符串

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SendString2(hwnd, input_str)

    def FindPic(self, x1: int, y1: int, x2: int, y2: int, pic_name: str, delta_color: str, sim: float, dir: int) -> str:
        """
        查找指定区域内的图片(位图必须是24位色格式,支持透明色,当图像上下左右4个顶点颜色一样时该颜色作为透明色处理)。只返回第一个找到的XY坐标

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            pic_name (str): 图片名，可以是多个图片用|分隔，如：test.bmp|test2.bmp|test3.bmp
            delta_color (str): 颜色色偏，如：203040表示RGB色偏分别是20/30/40(16进制)。如果2位表示灰度找图，如：20
            sim (float): 相似度，取值范围0.1-1.0
            dir (int): 查找方向：0=从左到右从上到下,1=从左到右从下到上,2=从右到左从上到下,3=从右到左从下到上

        Returns:
            字符串:
                -1|-1|-1: 未找到
                其他: x|y|index 格式，如: 100,200,0（index为找到的图片序号，从0开始）
        """
        return self._dm.FindPic(x1, y1, x2, y2, pic_name, delta_color, sim, dir)

    def FindPicE(self, x1: int, y1: int, x2: int, y2: int, pic_name: str, delta_color: str, sim: float, dir: int) -> str:
        """
        找图（易语言格式）

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            pic_name (str): 图片名，多个用|分隔
            delta_color (str): 偏色，如：000000-FFFFFF表示不偏色
            sim (float): 相似度，0.0-1.0之间
            dir (int): 查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上

        Returns:
            字符串:
                -1|-1|-1: 未找到
                其他: 易语言数组格式
        """
        return self._dm.FindPicE(x1, y1, x2, y2, pic_name, delta_color, sim, dir)

    def FindPicEx(self, x1: int, y1: int, x2: int, y2: int, pic_name: str, delta_color: str, sim: float, dir: int) -> str:
        """
        找图（返回所有结果）

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            pic_name (str): 图片名，多个用|分隔
            delta_color (str): 偏色，如：000000-FFFFFF表示不偏色
            sim (float): 相似度，0.0-1.0之间
            dir (int): 查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上

        Returns:
            字符串:
                : 未找到
                其他: 多组坐标，格式: x1,y1,index1|x2,y2,index2|...
        """
        return self._dm.FindPicEx(x1, y1, x2, y2, pic_name, delta_color, sim, dir)

    def FindPicExS(self, x1: int, y1: int, x2: int, y2: int, pic_name: str, delta_color: str, sim: float, dir: int) -> str:
        """
        找图（返回所有结果，字符串格式）

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            pic_name (str): 图片名，多个用|分隔
            delta_color (str): 偏色，如：000000-FFFFFF表示不偏色
            sim (float): 相似度，0.0-1.0之间
            dir (int): 查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上

        Returns:
            字符串:
                : 未找到
                其他: 字符串格式结果
        """
        return self._dm.FindPicExS(x1, y1, x2, y2, pic_name, delta_color, sim, dir)

    def FindPicMem(self, x1: int, y1: int, x2: int, y2: int, pic_info: str, delta_color: str, sim: float, dir: int) -> str:
        """
        从内存中找图

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            pic_info (str): 图片数据，由LoadPic加载到内存后的数据
            delta_color (str): 偏色，如：000000-FFFFFF表示不偏色
            sim (float): 相似度，0.0-1.0之间
            dir (int): 查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上

        Returns:
            字符串:
                -1|-1|-1: 未找到
                其他: x|y|index 格式
        """
        return self._dm.FindPicMem(x1, y1, x2, y2, pic_info, delta_color, sim, dir)

    def FindPicMemE(self, x1: int, y1: int, x2: int, y2: int, pic_info: str, delta_color: str, sim: float, dir: int) -> str:
        """
        从内存中找图（易语言格式）

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            pic_info (str): 图片数据，由LoadPic加载到内存后的数据
            delta_color (str): 偏色，如：000000-FFFFFF表示不偏色
            sim (float): 相似度，0.0-1.0之间
            dir (int): 查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上

        Returns:
            字符串:
                -1|-1|-1: 未找到
                其他: 易语言数组格式
        """
        return self._dm.FindPicMemE(x1, y1, x2, y2, pic_info, delta_color, sim, dir)

    def FindPicMemEx(self, x1: int, y1: int, x2: int, y2: int, pic_info: str, delta_color: str, sim: float, dir: int) -> str:
        """
        从内存中找图（扩展）

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            pic_info (str): 图片数据，由LoadPic加载到内存后的数据
            delta_color (str): 偏色，如：000000-FFFFFF表示不偏色
            sim (float): 相似度，0.0-1.0之间
            dir (int): 查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上

        Returns:
            字符串:
                : 未找到
                其他: 多组坐标
        """
        return self._dm.FindPicMemEx(x1, y1, x2, y2, pic_info, delta_color, sim, dir)

    def SetPicPwd(self, pwd: str) -> int:
        """
        设置图片密码

        Args:
            pwd: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetPicPwd(pwd)

    def FindColor(self, x1: int, y1: int, x2: int, y2: int, color: str, sim: float, dir: int) -> str:
        """
        找色

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            color (str): 颜色值，格式：RRGGBB，如：FFFFFF
            sim (float): 相似度，0.0-1.0之间
            dir (int): 查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上

        Returns:
            字符串:
                -1|-1: 未找到
                其他: x|y 格式，如: 100,200
        """
        return self._dm.FindColor(x1, y1, x2, y2, color, sim, dir)

    def FindColorE(self, x1: int, y1: int, x2: int, y2: int, color: str, sim: float, dir: int) -> str:
        """
        找色（易语言格式）

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            color (str): 颜色值，格式：RRGGBB
            sim (float): 相似度，0.0-1.0之间
            dir (int): 查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上

        Returns:
            字符串:
                -1|-1: 未找到
                其他: 易语言数组格式
        """
        return self._dm.FindColorE(x1, y1, x2, y2, color, sim, dir)

    def FindColorEx(self, x1: int, y1: int, x2: int, y2: int, color: str, sim: float, dir: int) -> str:
        """
        找色（返回所有结果）

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            color (str): 颜色值，格式：RRGGBB
            sim (float): 相似度，0.0-1.0之间
            dir (int): 查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上

        Returns:
            字符串:
                : 未找到
                其他: 多组坐标，格式: x1,y1|x2,y2|...
        """
        return self._dm.FindColorEx(x1, y1, x2, y2, color, sim, dir)

    def FindMultiColor(self, x1: int, y1: int, x2: int, y2: int, first_color: str, offset_color: str, sim: float, dir: int) -> str:
        """
        找多色

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            first_color (str): 主颜色，格式：RRGGBB
            offset_color (str): 偏移颜色，格式：x1-y1-颜色1|x2-y2-颜色2|...
            sim (float): 相似度，0.0-1.0之间
            dir (int): 查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上

        Returns:
            字符串:
                -1|-1: 未找到
                其他: x|y 格式
        """
        return self._dm.FindMultiColor(x1, y1, x2, y2, first_color, offset_color, sim, dir)

    def FindMultiColorE(self, x1: int, y1: int, x2: int, y2: int, first_color: str, offset_color: str, sim: float, dir: int) -> str:
        """
        找多色（易语言格式）

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            first_color (str): 主颜色，格式：RRGGBB
            offset_color (str): 偏移颜色，格式：x1-y1-颜色1|x2-y2-颜色2|...
            sim (float): 相似度，0.0-1.0之间
            dir (int): 查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上

        Returns:
            字符串:
                -1|-1: 未找到
                其他: 易语言数组格式
        """
        return self._dm.FindMultiColorE(x1, y1, x2, y2, first_color, offset_color, sim, dir)

    def FindMultiColorEx(self, x1: int, y1: int, x2: int, y2: int, first_color: str, offset_color: str, sim: float, dir: int) -> str:
        """
        找多色（扩展）

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            first_color (str): 主颜色，格式：RRGGBB
            offset_color (str): 偏移颜色，格式：x1-y1-颜色1|x2-y2-颜色2|...
            sim (float): 相似度，0.0-1.0之间
            dir (int): 查找方向：0=从左到右从上到下,1=从右到左,2=从上到下,3=从下到上

        Returns:
            字符串:
                : 未找到
                其他: 多组坐标
        """
        return self._dm.FindMultiColorEx(x1, y1, x2, y2, first_color, offset_color, sim, dir)

    def GetColor(self, x: int, y: int) -> str:
        """
        获取指定点颜色

        Args:
            x (int): 屏幕X坐标
            y (int): 屏幕Y坐标

        Returns:
            字符串:
                格式: RRGGBB
                示例: FFFFFF
        """
        return self._dm.GetColor(x, y)

    def GetColorBGR(self, x: int, y: int) -> str:
        """
        获取指定点BGR颜色

        Args:
            x (int): 屏幕X坐标
            y (int): 屏幕Y坐标

        Returns:
            字符串:
                格式: BBGGRR
                示例: FFFFFF
        """
        return self._dm.GetColorBGR(x, y)

    def GetAveRGB(self, x1: int, y1: int, x2: int, y2: int) -> str:
        """
        获取区域平均颜色

        Args:
            x1 (int): 区域左上角X坐标
            y1 (int): 区域左上角Y坐标
            x2 (int): 区域右下角X坐标
            y2 (int): 区域右下角Y坐标

        Returns:
            字符串:
                格式: RRGGBB
        """
        return self._dm.GetAveRGB(x1, y1, x2, y2)

    def GetAveHSV(self, x1: int, y1: int, x2: int, y2: int) -> str:
        """
        获取区域平均HSV

        Args:
            x1 (int): 区域左上角X坐标
            y1 (int): 区域左上角Y坐标
            x2 (int): 区域右下角X坐标
            y2 (int): 区域右下角Y坐标

        Returns:
            字符串:
                格式: H.S.V
        """
        return self._dm.GetAveHSV(x1, y1, x2, y2)

    def CmpColor(self, x: int, y: int, color: str, sim: float) -> int:
        """
        比较颜色

        Args:
            x (int): 屏幕X坐标
            y (int): 屏幕Y坐标
            color (str): 要比较的颜色，格式：RRGGBB
            sim (float): 相似度，0.0-1.0之间

        Returns:
            整形数:
                0: 颜色不匹配
                1: 颜色匹配
        """
        return self._dm.CmpColor(x, y, color, sim)

    def RGB2BGR(self, rgb_color: str) -> str:
        """
        RGB颜色转BGR颜色

        Args:
            rgb_color (str): RGB颜色值，格式：RRGGBB

        Returns:
            字符串:
                格式: BBGGRR
        """
        return self._dm.RGB2BGR(rgb_color)

    def BGR2RGB(self, bgr_color: str) -> str:
        """
        BGR颜色转RGB颜色

        Args:
            bgr_color (str): BGR颜色值，格式：BBGGRR

        Returns:
            字符串:
                格式: RRGGBB
        """
        return self._dm.BGR2RGB(bgr_color)

    def Ocr(self, x1: int, y1: int, x2: int, y2: int, color_format: str, sim: float) -> str:
        """
        文字识别

        Args:
            x1 (int): 识别区域左上角X坐标
            y1 (int): 识别区域左上角Y坐标
            x2 (int): 识别区域右下角X坐标
            y2 (int): 识别区域右下角Y坐标
            color_format (str): 颜色格式，如：FFFFFF-000000表示白底黑字
            sim (float): 相似度，0.0-1.0之间

        Returns:
            字符串:
                : 识别失败或未找到文字
                其他: 识别出的文字内容
        """
        return self._dm.Ocr(x1, y1, x2, y2, color_format, sim)

    def OcrEx(self, x1: int, y1: int, x2: int, y2: int, color_format: str, sim: float) -> str:
        """
        文字识别（返回详细坐标）

        Args:
            x1 (int): 识别区域左上角X坐标
            y1 (int): 识别区域左上角Y坐标
            x2 (int): 识别区域右下角X坐标
            y2 (int): 识别区域右下角Y坐标
            color_format (str): 颜色格式，如：FFFFFF-000000表示白底黑字
            sim (float): 相似度，0.0-1.0之间

        Returns:
            字符串:
                : 识别失败
                其他: 格式: 文字1|x1|y1|文字2|x2|y2|...
        """
        return self._dm.OcrEx(x1, y1, x2, y2, color_format, sim)

    def OcrInFile(self, x1: int, y1: int, x2: int, y2: int, color_format: str, sim: float, file_name: str) -> str:
        """
        从文件文字识别

        Args:
            x1 (int): 识别区域左上角X坐标
            y1 (int): 识别区域左上角Y坐标
            x2 (int): 识别区域右下角X坐标
            y2 (int): 识别区域右下角Y坐标
            color_format (str): 颜色格式，如：FFFFFF-000000表示白底黑字
            sim (float): 相似度，0.0-1.0之间
            file_name (str): 图片文件名，从该文件识别文字

        Returns:
            字符串:
                : 识别失败
                其他: 识别出的文字内容
        """
        return self._dm.OcrInFile(x1, y1, x2, y2, color_format, sim, file_name)

    def FindStr(self, x1: int, y1: int, x2: int, y2: int, string: str, color_format: str, sim: float) -> str:
        """
        找字

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            string (str): 要查找的字符串
            color_format (str): 颜色格式，如：FFFFFF-000000表示白底黑字
            sim (float): 相似度，0.0-1.0之间

        Returns:
            字符串:
                -1|-1: 未找到
                其他: x|y 格式，如: 100,200
        """
        return self._dm.FindStr(x1, y1, x2, y2, string, color_format, sim)

    def FindStrE(self, x1: int, y1: int, x2: int, y2: int, string: str, color_format: str, sim: float) -> str:
        """
        找字（易语言格式）

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            string (str): 要查找的字符串
            color_format (str): 颜色格式，如：FFFFFF-000000表示白底黑字
            sim (float): 相似度，0.0-1.0之间

        Returns:
            字符串:
                -1|-1: 未找到
                其他: 易语言数组格式
        """
        return self._dm.FindStrE(x1, y1, x2, y2, string, color_format, sim)

    def FindStrEx(self, x1: int, y1: int, x2: int, y2: int, string: str, color_format: str, sim: float) -> str:
        """
        找字（返回所有结果）

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            string (str): 要查找的字符串
            color_format (str): 颜色格式，如：FFFFFF-000000表示白底黑字
            sim (float): 相似度，0.0-1.0之间

        Returns:
            字符串:
                : 未找到
                其他: 多组坐标，格式: x1,y1|x2,y2|...
        """
        return self._dm.FindStrEx(x1, y1, x2, y2, string, color_format, sim)

    def FindStrExS(self, x1: int, y1: int, x2: int, y2: int, string: str, color_format: str, sim: float) -> str:
        """
        找字（返回所有结果，字符串格式）

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            string (str): 要查找的字符串
            color_format (str): 颜色格式，如：FFFFFF-000000表示白底黑字
            sim (float): 相似度，0.0-1.0之间

        Returns:
            字符串:
                : 未找到
                其他: 字符串格式结果
        """
        return self._dm.FindStrExS(x1, y1, x2, y2, string, color_format, sim)

    def FindStrFast(self, x1: int, y1: int, x2: int, y2: int, string: str, color_format: str, sim: float) -> str:
        """
        快速找字

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            string (str): 要查找的字符串
            color_format (str): 颜色格式，如：FFFFFF-000000表示白底黑字
            sim (float): 相似度，0.0-1.0之间

        Returns:
            字符串:
                -1|-1: 未找到
                其他: x|y 格式
        """
        return self._dm.FindStrFast(x1, y1, x2, y2, string, color_format, sim)

    def FindStrFastE(self, x1: int, y1: int, x2: int, y2: int, string: str, color_format: str, sim: float) -> str:
        """
        快速找字（易语言格式）

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            string (str): 要查找的字符串
            color_format (str): 颜色格式，如：FFFFFF-000000表示白底黑字
            sim (float): 相似度，0.0-1.0之间

        Returns:
            字符串:
                -1|-1: 未找到
                其他: 易语言数组格式
        """
        return self._dm.FindStrFastE(x1, y1, x2, y2, string, color_format, sim)

    def FindStrFastEx(self, x1: int, y1: int, x2: int, y2: int, string: str, color_format: str, sim: float) -> str:
        """
        快速找字（扩展）

        Args:
            x1 (int): 查找区域左上角X坐标
            y1 (int): 查找区域左上角Y坐标
            x2 (int): 查找区域右下角X坐标
            y2 (int): 查找区域右下角Y坐标
            string (str): 要查找的字符串
            color_format (str): 颜色格式，如：FFFFFF-000000表示白底黑字
            sim (float): 相似度，0.0-1.0之间

        Returns:
            字符串:
                : 未找到
                其他: 多组坐标
        """
        return self._dm.FindStrFastEx(x1, y1, x2, y2, string, color_format, sim)

    def SetDict(self, index: int, file_name: str) -> int:
        """
        设置字库文件

        Args:
            index (int): 字库索引，0-9之间
            file_name (str): 字库文件路径，如：C:\test\test.txt

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetDict(index, file_name)

    def UseDict(self, index: int) -> int:
        """
        使用指定字库

        Args:
            index (int): 字库索引，0-9之间

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.UseDict(index)

    def GetNowDict(self, ) -> int:
        """
        获取当前使用的字库索引

        Returns:
            整形数:
                : 未设置字库
                其他: 字库索引
        """
        return self._dm.GetNowDict()

    def SetShowErrorMsg(self, show: int) -> int:
        """
        设置是否显示错误信息

        Args:
            show (int): 0=不显示,1=显示

        Returns:
            整形数:
                0: 不显示
                1: 显示
        """
        return self._dm.SetShowErrorMsg(show)

    def SetShowMsg(self, x: int, y: int, color: str, size: int, msg: str) -> int:
        """
        在屏幕上显示信息

        Args:
            x (int): 显示位置X坐标
            y (int): 显示位置Y坐标
            color (str): 文字颜色，格式：RRGGBB
            size (int): 字体大小
            msg (str): 要显示的信息内容

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetShowMsg(x, y, color, size, msg)

    def BindWindow(self, hwnd: int, display: str, mouse: str, keypad: str, mode: int) -> int:
        """
        绑定指定的窗口,并指定屏幕颜色获取方式,鼠标仿真模式,键盘仿真模式以及模式设定

        Args:
            hwnd (int): 指定的窗口句柄
            display (str): 屏幕颜色获取方式: normal=正常(前台截屏), gdi=gdi后台(Win10截图失败尝试重开目标程序), gdi2=gdi2后台(兼容性强但慢), dx2=dx2后台(部分在屏幕外,Win10截图失败尝试重开), dx3=dx3后台(后台不刷新时尝试,比dx2慢), dx=dx模式(等同BindWindowEx的dx.graphic.2d|dx.graphic.3d)
            mouse (str): 鼠标仿真模式: normal=正常(前台), windows=模拟Windows消息(同按键后台), windows2=模拟Windows消息锁定鼠标位置, windows3=支持多子窗口的后台, dx=dx后台(锁定鼠标输入,绑定后可能需要激活窗口), dx2=dx2后台(不锁定外部鼠标输入,绑定后可能需要激活窗口)
            keypad (str): 键盘仿真模式: normal=正常(前台), windows=模拟Windows消息(同按键后台), dx=dx后台(绑定后可能需要激活窗口)
            mode (int): 绑定模式: 0=推荐模式(通用且后台效果最好), 2=同模式0(模式0崩溃时尝试,主绑定线程必须保持), 101=超级绑定模式(隐藏dm.dll,推荐), 103=同模式101(模式101崩溃时尝试), 11=驱动模式(特殊窗口,不支持32位), 13=驱动模式(特殊窗口,不支持32位)

        Returns:
            整形数:
                0: 失败(可调用GetLastError查看具体错误码)
                1: 成功
        """
        return self._dm.BindWindow(hwnd, display, mouse, keypad, mode)

    def BindWindowEx(self, hwnd: int, display: str, mouse: str, keypad: str, public_desc: str, mode: int) -> int:
        """
        绑定指定的窗口,并指定屏幕颜色获取方式,鼠标仿真模式,键盘仿真模式以及公共属性(高级用户推荐)

        Args:
            hwnd (int): 指定的窗口句柄
            display (str): 屏幕颜色获取方式(支持组合用|连接): normal=正常(前台截屏), gdi=gdi后台(Win10截图失败尝试重开目标程序), gdi2=gdi2后台(兼容性强但慢), dx2=dx2后台(部分在屏幕外,Win10截图失败尝试重开), dx3=dx3后台(后台不刷新时尝试,比dx2慢), dx.graphic.2d=2d窗口dx图色, dx.graphic.2d.2=增强模式(兼容性更好), dx.graphic.3d=3d窗口dx图色, dx.graphic.3d.8=dx8图色(64位进程无效), dx.graphic.opengl=opengl图色(速度可能较慢,截图可能上下反向,可配合dx.public.graphic.revert), dx.graphic.opengl.esv2=opengl_esv2图色, dx.graphic.3d.10plus=dx10/11/12图色
            mouse (str): 鼠标仿真模式(支持组合用|连接): normal=正常(前台), windows=模拟Windows消息(同按键后台), windows3=支持多子窗口的后台, dx.mouse.position.lock.api=封锁API锁定鼠标位置, dx.mouse.position.lock.message=封锁消息锁定鼠标位置, dx.mouse.focus.input.api=封锁API锁定输入焦点, dx.mouse.focus.input.message=封锁消息锁定输入焦点, dx.mouse.clip.lock.api=封锁API锁定刷新区域(绑定前需窗口完全显示), dx.mouse.input.lock.api=封锁API锁定鼠标输入接口, dx.mouse.state.api=封锁API锁定鼠标状态, dx.mouse.state.message=封锁消息锁定鼠标状态, dx.mouse.api=封锁API模拟dx鼠标, dx.mouse.cursor=后台获取鼠标特征码, dx.mouse.raw.input=部分窗口需要, dx.mouse.input.lock.api2=防止前台鼠标移动, dx.mouse.input.lock.api3=防止前台鼠标移动, dx.mouse.raw.input.active=配合raw.input使用(绑定前需激活窗口,非必要不用)
            keypad (str): 键盘仿真模式(支持组合用|连接): normal=正常(前台), windows=模拟Windows消息(同按键后台), dx.keypad.input.lock.api=封锁API锁定键盘输入接口, dx.keypad.state.api=封锁API锁定键盘状态, dx.keypad.api=封锁API模拟dx键盘, dx.keypad.raw.input=部分窗口需要, dx.keypad.raw.input.active=配合raw.input使用(绑定前需激活窗口,非必要不用)
            public_desc (str): 公共属性(支持组合用|连接,可为空): dx.public.active.api=封锁API锁定窗口激活(部分窗口耗资源慎用), dx.public.active.message=封锁消息锁定激活(绑定前需窗口激活), dx.public.disable.window.position=锁定窗口位置(不可与fake.window.min共用), dx.public.disable.window.size=禁止改变大小(不可与fake.window.min共用), dx.public.disable.window.minmax=禁止最大最小化(会置顶,不可与fake.window.min共用), dx.public.fake.window.min=最小化仍可操作(单开建议,多开混乱,可能不刷新或黑屏), dx.public.hide.dll=隐藏dm.dll(可能不稳定), dx.public.active.api2=部分窗口遮挡需要, dx.public.input.ime=配合SendStringIme使用, dx.public.graphic.protect=保护dx图色不被检测(可能导致场景重载时失效), dx.public.disable.window.show=禁止窗口显示(配合fake.window.min), dx.public.anti.api=突破部分后台保护, dx.public.km.protect=保护dx键鼠不被检测(可能导致部分功能失效), dx.public.prevent.block=避免模式1/3/5/7/101/103卡死, dx.public.ori.proc=让不同界面键鼠控制效果一致(测试无问题再用), dx.public.down.cpu=配合DownCpu降低CPU(会让图色降CPU失效), dx.public.focus.message=强制键盘消息到焦点窗口(可能导致后台键盘失灵), dx.public.graphic.speed=牺牲性能提高DX图色速度(刷新慢时有用), dx.public.memory=突破防护使用内存接口(速度取决于刷新率), dx.public.inject.super=突破难以绑定的窗口(除0/2模式), dx.public.hack.speed=配合HackSpeed变速齿轮, dx.public.inject.c=突破难以绑定的窗口(除0/2模式), dx.public.graphic.revert=截图内容上下反向(仅opengl/esv2有效)
            mode (int): 绑定模式: 0=推荐模式(通用且后台效果最好), 2=同模式0(模式0崩溃时尝试,主绑定线程必须保持), 101=超级绑定模式(隐藏dm.dll,推荐), 103=同模式101(模式101崩溃时尝试), 11=驱动模式(特殊窗口,不支持32位), 13=驱动模式(特殊窗口,不支持32位)

        Returns:
            整形数:
                0: 失败(可调用GetLastError查看具体错误码)
                1: 成功
        """
        return self._dm.BindWindowEx(hwnd, display, mouse, keypad, public_desc, mode)

    def UnBindWindow(self, ) -> int:
        """
        解绑窗口

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.UnBindWindow()

    def GetBindWindow(self, ) -> int:
        """
        获取当前绑定的窗口句柄

        Returns:
            整形数:
                0: 未绑定
                其他: 窗口句柄
        """
        return self._dm.GetBindWindow()

    def IsBind(self, ) -> int:
        """
        判断是否已绑定窗口

        Returns:
            整形数:
                0: 未绑定
                1: 已绑定
        """
        return self._dm.IsBind()

    def GetDisplayMode(self, ) -> str:
        """
        获取显示器分辨率

        Returns:
            字符串:
                格式: width,height
                示例: 1920,1080
        """
        return self._dm.GetDisplayMode()

    def SetDisplayInput(self, mode: str) -> int:
        """
        设置显示输入模式

        Args:
            mode (str): 输入模式：dx.mouse.input.lock|dx.mouse.input.api|dx.keypad.input.lock

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetDisplayInput(mode)

    def SetUAC(self, uac: int) -> int:
        """
        设置UAC

        Args:
            uac (int): 0=关闭UAC,1=开启UAC

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetUAC(uac)

    def EnableRealMouse(self, enable: int, mousedelay: int, mousestep: int) -> int:
        """
        启用真实鼠标模拟

        Args:
            enable (int): 0=关闭,1=开启
            mousedelay (int): 鼠标移动延迟，单位毫秒
            mousestep (int): 鼠标移动步长

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.EnableRealMouse(enable, mousedelay, mousestep)

    def EnableRealKeypad(self, enable: int) -> int:
        """
        启用真实键盘模拟

        Args:
            enable (int): 0=关闭,1=开启

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.EnableRealKeypad(enable)

    def EnableKeypadMsg(self, enable: int) -> int:
        """
        启用键盘消息

        Args:
            enable (int): 0=关闭,1=开启

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.EnableKeypadMsg(enable)

    def EnableMouseMsg(self, enable: int) -> int:
        """
        启用鼠标消息

        Args:
            enable: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.EnableMouseMsg(enable)

    def EnableKeypadPatch(self, enable: int) -> int:
        """
        启用键盘补丁

        Args:
            enable: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.EnableKeypadPatch(enable)

    def EnableMouseAccuracy(self, enable: int) -> int:
        """
        启用鼠标高精度模式

        Args:
            enable: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.EnableMouseAccuracy(enable)

    def Capture(self, x1: int, y1: int, x2: int, y2: int, file_name: str) -> int:
        """
        截图保存为BMP

        Args:
            x1: int 类型参数
            y1: int 类型参数
            x2: int 类型参数
            y2: int 类型参数
            file_name: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.Capture(x1, y1, x2, y2, file_name)

    def CapturePng(self, x1: int, y1: int, x2: int, y2: int, file_name: str) -> int:
        """
        截图保存为PNG

        Args:
            x1: int 类型参数
            y1: int 类型参数
            x2: int 类型参数
            y2: int 类型参数
            file_name: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.CapturePng(x1, y1, x2, y2, file_name)

    def CaptureJpg(self, x1: int, y1: int, x2: int, y2: int, file_name: str, quality: int) -> int:
        """
        截图保存为JPG

        Args:
            x1: int 类型参数
            y1: int 类型参数
            x2: int 类型参数
            y2: int 类型参数
            file_name: str 类型参数
            quality: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.CaptureJpg(x1, y1, x2, y2, file_name, quality)

    def CaptureGif(self, x1: int, y1: int, x2: int, y2: int, file_name: str, delay: int, time: int) -> int:
        """
        截图保存为GIF

        Args:
            x1: int 类型参数
            y1: int 类型参数
            x2: int 类型参数
            y2: int 类型参数
            file_name: str 类型参数
            delay: int 类型参数
            time: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.CaptureGif(x1, y1, x2, y2, file_name, delay, time)

    def GetScreenData(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """
        获取屏幕数据到内存

        Args:
            x1: int 类型参数
            y1: int 类型参数
            x2: int 类型参数
            y2: int 类型参数

        Returns:
            整形数:
                0: 失败
                其他: 数据句柄
        """
        return self._dm.GetScreenData(x1, y1, x2, y2)

    def GetScreenDataBmp(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """
        获取屏幕数据（BMP格式）

        Args:
            x1: int 类型参数
            y1: int 类型参数
            x2: int 类型参数
            y2: int 类型参数

        Returns:
            整形数:
                0: 失败
                其他: 数据句柄
        """
        return self._dm.GetScreenDataBmp(x1, y1, x2, y2)

    def FreeScreenData(self, handle: int) -> int:
        """
        释放屏幕数据

        Args:
            handle: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.FreeScreenData(handle)

    def SetScreen(self, width: int, height: int, depth: int) -> int:
        """
        设置屏幕分辨率

        Args:
            width: int 类型参数
            height: int 类型参数
            depth: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetScreen(width, height, depth)

    def ReadInt(self, hwnd: int, addr: str) -> int:
        """
        读取内存整数

        Args:
            hwnd: int 类型参数
            addr: str 类型参数

        Returns:
            整形数:
                其他: 读取到的整数值
        """
        return self._dm.ReadInt(hwnd, addr)

    def ReadFloat(self, hwnd: int, addr: str) -> float:
        """
        读取内存浮点数

        Args:
            hwnd: int 类型参数
            addr: str 类型参数

        Returns:
            浮点数:
                其他: 读取到的浮点数值
        """
        return self._dm.ReadFloat(hwnd, addr)

    def ReadDouble(self, hwnd: int, addr: str) -> float:
        """
        读取内存双精度浮点数

        Args:
            hwnd: int 类型参数
            addr: str 类型参数

        Returns:
            浮点数:
                其他: 读取到的双精度浮点数值
        """
        return self._dm.ReadDouble(hwnd, addr)

    def ReadString(self, hwnd: int, addr: str, type: int, length: int) -> str:
        """
        读取内存字符串

        Args:
            hwnd: int 类型参数
            addr: str 类型参数
            type: int 类型参数
            length: int 类型参数

        Returns:
            字符串:
                : 失败
                其他: 读取到的字符串
        """
        return self._dm.ReadString(hwnd, addr, type, length)

    def WriteInt(self, hwnd: int, addr: str, value: int) -> int:
        """
        写入内存整数

        Args:
            hwnd: int 类型参数
            addr: str 类型参数
            value: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.WriteInt(hwnd, addr, value)

    def WriteFloat(self, hwnd: int, addr: str, value: float) -> int:
        """
        写入内存浮点数

        Args:
            hwnd: int 类型参数
            addr: str 类型参数
            value: float 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.WriteFloat(hwnd, addr, value)

    def WriteDouble(self, hwnd: int, addr: str, value: float) -> int:
        """
        写入内存双精度浮点数

        Args:
            hwnd: int 类型参数
            addr: str 类型参数
            value: float 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.WriteDouble(hwnd, addr, value)

    def WriteString(self, hwnd: int, addr: str, type: int, value: str) -> int:
        """
        写入内存字符串

        Args:
            hwnd: int 类型参数
            addr: str 类型参数
            type: int 类型参数
            value: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.WriteString(hwnd, addr, type, value)

    def AsmCall(self, hwnd: int, asm: str, mode: int) -> int:
        """
        执行汇编代码

        Args:
            hwnd: int 类型参数
            asm: str 类型参数
            mode: int 类型参数

        Returns:
            整形数:
                0: 失败
                其他: 返回值
        """
        return self._dm.AsmCall(hwnd, asm, mode)

    def AsmCallEx(self, hwnd: int, asm: str, mode: int, param: str) -> int:
        """
        执行汇编代码（扩展）

        Args:
            hwnd: int 类型参数
            asm: str 类型参数
            mode: int 类型参数
            param: str 类型参数

        Returns:
            整形数:
                0: 失败
                其他: 返回值
        """
        return self._dm.AsmCallEx(hwnd, asm, mode, param)

    def GetModuleBaseAddr(self, pid: int, module_name: str) -> int:
        """
        获取模块基址

        Args:
            pid: int 类型参数
            module_name: str 类型参数

        Returns:
            整形数:
                0: 失败
                其他: 模块基址
        """
        return self._dm.GetModuleBaseAddr(pid, module_name)

    def GetModuleBaseAddrEx(self, hwnd: int, module_name: str) -> int:
        """
        获取模块基址（扩展）

        Args:
            hwnd: int 类型参数
            module_name: str 类型参数

        Returns:
            整形数:
                0: 失败
                其他: 模块基址
        """
        return self._dm.GetModuleBaseAddrEx(hwnd, module_name)

    def GetRemoteProcAddress(self, hwnd: int, base_addr: int, proc_name: str) -> int:
        """
        获取远程进程函数地址

        Args:
            hwnd: int 类型参数
            base_addr: int 类型参数
            proc_name: str 类型参数

        Returns:
            整形数:
                0: 失败
                其他: 函数地址
        """
        return self._dm.GetRemoteProcAddress(hwnd, base_addr, proc_name)

    def SetMemoryHwndAsProcessId(self, enable: int) -> int:
        """
        设置内存操作句柄为进程ID

        Args:
            enable: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetMemoryHwndAsProcessId(enable)

    def SetMemoryFindResultToFile(self, file_name: str) -> int:
        """
        设置内存查找结果保存到文件

        Args:
            file_name: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetMemoryFindResultToFile(file_name)

    def SetPath(self, path: str) -> int:
        """
        设置全局路径

        Args:
            path: str 类型参数

        Returns:
            整形数: 返回值
        """
        return self._dm.SetPath(path)

    def GetPath(self, ) -> str:
        """
        获取全局路径

        Returns:
            字符串:
                : 未设置
                其他: 当前全局路径
        """
        return self._dm.GetPath()

    def SetExitKey(self, exit_key: int) -> int:
        """
        设置退出键

        Args:
            exit_key: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetExitKey(exit_key)

    def SetClientSize(self, hwnd: int, width: int, height: int) -> int:
        """
        设置客户区大小

        Args:
            hwnd: int 类型参数
            width: int 类型参数
            height: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetClientSize(hwnd, width, height)

    def SetMouseDelay(self, type: str, delay: int) -> int:
        """
        设置鼠标延时

        Args:
            type: str 类型参数
            delay: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetMouseDelay(type, delay)

    def SetKeypadDelay(self, type: str, delay: int) -> int:
        """
        设置键盘延时

        Args:
            type: str 类型参数
            delay: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetKeypadDelay(type, delay)

    def SetWordGap(self, word_gap: int) -> int:
        """
        设置文字间隔

        Args:
            word_gap: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetWordGap(word_gap)

    def SetRowGapNoDict(self, row_gap: int) -> int:
        """
        设置无字库行间隔

        Args:
            row_gap: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetRowGapNoDict(row_gap)

    def SetColGapNoDict(self, col_gap: int) -> int:
        """
        设置无字库列间隔

        Args:
            col_gap: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetColGapNoDict(col_gap)

    def GetClipboard(self, ) -> str:
        """
        获取剪贴板内容

        Returns:
            字符串:
                : 剪贴板为空
                其他: 剪贴板内容
        """
        return self._dm.GetClipboard()

    def SetClipboard(self, data: str) -> int:
        """
        设置剪贴板内容

        Args:
            data: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetClipboard(data)

    def FoobarCreate(self, x: int, y: int, w: int, h: int, name: str, dir: int) -> int:
        """
        创建进度条窗口

        Args:
            x: int 类型参数
            y: int 类型参数
            w: int 类型参数
            h: int 类型参数
            name: str 类型参数
            dir: int 类型参数

        Returns:
            整形数:
                0: 失败
                其他: 进度条窗口句柄
        """
        return self._dm.FoobarCreate(x, y, w, h, name, dir)

    def FoobarClose(self, hwnd: int) -> int:
        """
        关闭进度条窗口

        Args:
            hwnd: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.FoobarClose(hwnd)

    def FoobarClearText(self, hwnd: int) -> int:
        """
        清除进度条文本

        Args:
            hwnd: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.FoobarClearText(hwnd)

    def FoobarPrintText(self, hwnd: int, text: str, color: str) -> int:
        """
        在进度条打印文本

        Args:
            hwnd: int 类型参数
            text: str 类型参数
            color: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.FoobarPrintText(hwnd, text, color)

    def FoobarSetFont(self, hwnd: int, font_name: str, size: int, flag: int) -> int:
        """
        设置进度条字体

        Args:
            hwnd: int 类型参数
            font_name: str 类型参数
            size: int 类型参数
            flag: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.FoobarSetFont(hwnd, font_name, size, flag)

    def FoobarSetSave(self, hwnd: int, file_name: str) -> int:
        """
        设置进度条保存文件

        Args:
            hwnd: int 类型参数
            file_name: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.FoobarSetSave(hwnd, file_name)

    def FoobarDrawLine(self, hwnd: int, x1: int, y1: int, x2: int, y2: int, color: str, style: int, width: int) -> int:
        """
        在进度条绘制线条

        Args:
            hwnd: int 类型参数
            x1: int 类型参数
            y1: int 类型参数
            x2: int 类型参数
            y2: int 类型参数
            color: str 类型参数
            style: int 类型参数
            width: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.FoobarDrawLine(hwnd, x1, y1, x2, y2, color, style, width)

    def FoobarDrawText(self, hwnd: int, x: int, y: int, w: int, h: int, text: str, color: str, align: int) -> int:
        """
        在进度条绘制文本

        Args:
            hwnd: int 类型参数
            x: int 类型参数
            y: int 类型参数
            w: int 类型参数
            h: int 类型参数
            text: str 类型参数
            color: str 类型参数
            align: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.FoobarDrawText(hwnd, x, y, w, h, text, color, align)

    def FoobarDrawPic(self, hwnd: int, x: int, y: int, pic_name: str) -> int:
        """
        在进度条绘制图片

        Args:
            hwnd: int 类型参数
            x: int 类型参数
            y: int 类型参数
            pic_name: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.FoobarDrawPic(hwnd, x, y, pic_name)

    def FoobarFillRect(self, hwnd: int, x1: int, y1: int, x2: int, y2: int, color: str) -> int:
        """
        在进度条填充矩形

        Args:
            hwnd: int 类型参数
            x1: int 类型参数
            y1: int 类型参数
            x2: int 类型参数
            y2: int 类型参数
            color: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.FoobarFillRect(hwnd, x1, y1, x2, y2, color)

    def FoobarTextLineDir(self, hwnd: int, dir: int) -> int:
        """
        设置进度条文本方向

        Args:
            hwnd: int 类型参数
            dir: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.FoobarTextLineDir(hwnd, dir)

    def Delay(self, mis: int) -> int:
        """
        延时（毫秒）

        Args:
            mis: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.Delay(mis)

    def Delays(self, mis_min: int, mis_max: int) -> int:
        """
        随机延时（最小毫秒, 最大毫秒）

        Args:
            mis_min: int 类型参数
            mis_max: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.Delays(mis_min, mis_max)

    def LoadPic(self, pic_name: str) -> int:
        """
        加载图片到内存

        Args:
            pic_name: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.LoadPic(pic_name)

    def FreePic(self, pic_name: str) -> int:
        """
        释放内存中的图片

        Args:
            pic_name: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.FreePic(pic_name)

    def GetNetTime(self, ) -> str:
        """
        获取网络时间

        Returns:
            字符串:
                : 失败
                其他: 网络时间字符串
        """
        return self._dm.GetNetTime()

    def GetNetTimeSafe(self, ) -> str:
        """
        获取网络时间（安全模式）

        Returns:
            字符串:
                : 失败
                其他: 网络时间字符串
        """
        return self._dm.GetNetTimeSafe()

    def CheckUAC(self, ) -> int:
        """
        检查UAC状态

        Returns:
            整形数:
                0: UAC已关闭
                1: UAC已开启
        """
        return self._dm.CheckUAC()

    def SetParam64ToPointer(self, enable: int) -> int:
        """
        设置64位参数转指针

        Args:
            enable: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SetParam64ToPointer(enable)

    def EnumIniKey(self, section: str, file_name: str) -> str:
        """
        枚举INI文件的键

        Args:
            section: str 类型参数
            file_name: str 类型参数

        Returns:
            字符串:
                : 失败
                其他: 键名列表
        """
        return self._dm.EnumIniKey(section, file_name)

    def EnumIniKeyPwd(self, section: str, file_name: str, pwd: str) -> str:
        """
        枚举加密的INI文件键

        Args:
            section: str 类型参数
            file_name: str 类型参数
            pwd: str 类型参数

        Returns:
            字符串:
                : 失败
                其他: 键名列表
        """
        return self._dm.EnumIniKeyPwd(section, file_name, pwd)

    def ReadIni(self, section: str, key: str, file_name: str) -> str:
        """
        读取INI文件

        Args:
            section: str 类型参数
            key: str 类型参数
            file_name: str 类型参数

        Returns:
            字符串:
                : 失败或不存在
                其他: 键值
        """
        return self._dm.ReadIni(section, key, file_name)

    def ReadIniPwd(self, section: str, key: str, file_name: str, pwd: str) -> str:
        """
        读取加密的INI文件

        Args:
            section: str 类型参数
            key: str 类型参数
            file_name: str 类型参数
            pwd: str 类型参数

        Returns:
            字符串:
                : 失败或不存在
                其他: 键值
        """
        return self._dm.ReadIniPwd(section, key, file_name, pwd)

    def WriteIni(self, section: str, key: str, value: str, file_name: str) -> int:
        """
        写入INI文件

        Args:
            section: str 类型参数
            key: str 类型参数
            value: str 类型参数
            file_name: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.WriteIni(section, key, value, file_name)

    def WriteIniPwd(self, section: str, key: str, value: str, file_name: str, pwd: str) -> int:
        """
        写入加密的INI文件

        Args:
            section: str 类型参数
            key: str 类型参数
            value: str 类型参数
            file_name: str 类型参数
            pwd: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.WriteIniPwd(section, key, value, file_name, pwd)

    def DeleteIni(self, section: str, key: str, file_name: str) -> int:
        """
        删除INI文件键值

        Args:
            section: str 类型参数
            key: str 类型参数
            file_name: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.DeleteIni(section, key, file_name)

    def DeleteIniPwd(self, section: str, key: str, file_name: str, pwd: str) -> int:
        """
        删除加密的INI文件键值

        Args:
            section: str 类型参数
            key: str 类型参数
            file_name: str 类型参数
            pwd: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.DeleteIniPwd(section, key, file_name, pwd)

    def DeleteFile(self, file_name: str) -> int:
        """
        删除文件

        Args:
            file_name: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.DeleteFile(file_name)

    def MoveFile(self, src_file: str, dst_file: str) -> int:
        """
        移动文件

        Args:
            src_file: str 类型参数
            dst_file: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.MoveFile(src_file, dst_file)

    def CreateFolder(self, folder_name: str) -> int:
        """
        创建文件夹

        Args:
            folder_name: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.CreateFolder(folder_name)

    def DeleteFolder(self, folder_name: str) -> int:
        """
        删除文件夹

        Args:
            folder_name: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.DeleteFolder(folder_name)

    def GetFileLength(self, file_name: str) -> int:
        """
        获取文件大小

        Args:
            file_name: str 类型参数

        Returns:
            整形数:
                -1: 失败
                其他: 文件大小（字节）
        """
        return self._dm.GetFileLength(file_name)

    def ReadFile(self, file_name: str) -> str:
        """
        读取文件内容

        Args:
            file_name: str 类型参数

        Returns:
            字符串:
                : 失败
                其他: 文件内容
        """
        return self._dm.ReadFile(file_name)

    def WriteFile(self, file_name: str, content: str) -> int:
        """
        写入文件内容

        Args:
            file_name: str 类型参数
            content: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.WriteFile(file_name, content)

    def AppendFile(self, file_name: str, content: str) -> int:
        """
        追加文件内容

        Args:
            file_name: str 类型参数
            content: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.AppendFile(file_name, content)

    def OpenFile(self, file_name: str) -> int:
        """
        打开文件

        Args:
            file_name: str 类型参数

        Returns:
            整形数:
                0: 失败
                其他: 文件句柄
        """
        return self._dm.OpenFile(file_name)

    def CloseFile(self, handle: int) -> int:
        """
        关闭文件

        Args:
            handle: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.CloseFile(handle)

    def ReadFileData(self, handle: int, length: int) -> str:
        """
        读取文件数据

        Args:
            handle: int 类型参数
            length: int 类型参数

        Returns:
            字符串:
                : 失败
                其他: 读取的数据
        """
        return self._dm.ReadFileData(handle, length)

    def WriteFileData(self, handle: int, data: str) -> int:
        """
        写入文件数据

        Args:
            handle: int 类型参数
            data: str 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.WriteFileData(handle, data)

    def SeekFile(self, handle: int, offset: int) -> int:
        """
        移动文件指针

        Args:
            handle: int 类型参数
            offset: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.SeekFile(handle, offset)

    def GetFilePointer(self, handle: int) -> int:
        """
        获取文件指针位置

        Args:
            handle: int 类型参数

        Returns:
            整形数:
                -1: 失败
                其他: 当前指针位置
        """
        return self._dm.GetFilePointer(handle)

    def FlushFile(self, handle: int) -> int:
        """
        刷新文件缓冲区

        Args:
            handle: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.FlushFile(handle)

    def Base64Encode(self, data: str) -> str:
        """
        Base64编码

        Args:
            data: str 类型参数

        Returns:
            字符串:
                : 失败
                其他: Base64编码字符串
        """
        return self._dm.Base64Encode(data)

    def Base64Decode(self, data: str) -> str:
        """
        Base64解码

        Args:
            data: str 类型参数

        Returns:
            字符串:
                : 失败
                其他: 解码后的字符串
        """
        return self._dm.Base64Decode(data)

    def MD5(self, data: str) -> str:
        """
        计算MD5

        Args:
            data: str 类型参数

        Returns:
            字符串:
                : 失败
                其他: MD5哈希值
        """
        return self._dm.MD5(data)

    def GetLocale(self, ) -> int:
        """
        获取系统区域设置

        Returns:
            整形数:
                其他: 区域设置ID
        """
        return self._dm.GetLocale()

    def GetLocaleAlias(self, id: int) -> str:
        """
        获取区域设置别名

        Args:
            id: int 类型参数

        Returns:
            字符串:
                : 失败
                其他: 区域别名
        """
        return self._dm.GetLocaleAlias(id)

    def GetOsType(self, ) -> int:
        """
        获取操作系统类型

        Returns:
            整形数:
                0: 失败
                其他: 操作系统类型码
        """
        return self._dm.GetOsType()

    def GetTime(self, ) -> int:
        """
        获取系统时间

        Returns:
            整形数:
                其他: 时间戳
        """
        return self._dm.GetTime()

    def GetSystemInfo(self, type: int) -> str:
        """
        获取系统信息

        Args:
            type: int 类型参数

        Returns:
            字符串:
                : 失败
                其他: 系统信息字符串
        """
        return self._dm.GetSystemInfo(type)

    def SelectDirectory(self, ) -> str:
        """
        选择文件夹对话框

        Returns:
            字符串:
                : 取消
                其他: 选择的文件夹路径
        """
        return self._dm.SelectDirectory()

    def SelectFile(self, ) -> str:
        """
        选择文件对话框

        Returns:
            字符串:
                : 取消
                其他: 选择的文件路径
        """
        return self._dm.SelectFile()

    def RunApp(self, app_path: str, cmd: str) -> int:
        """
        运行程序

        Args:
            app_path: str 类型参数
            cmd: str 类型参数

        Returns:
            整形数:
                0: 失败
                其他: 进程ID
        """
        return self._dm.RunApp(app_path, cmd)

    def StopApp(self, pid: int) -> int:
        """
        停止程序

        Args:
            pid: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.StopApp(pid)

    def GetProcessState(self, pid: int) -> int:
        """
        获取进程状态

        Args:
            pid: int 类型参数

        Returns:
            整形数:
                0: 不存在
                1: 运行中
                2: 挂起
        """
        return self._dm.GetProcessState(pid)

    def GetCommandLine(self, pid: int) -> str:
        """
        获取进程命令行

        Args:
            pid: int 类型参数

        Returns:
            字符串:
                : 失败
                其他: 命令行字符串
        """
        return self._dm.GetCommandLine(pid)

    def GetParentFolder(self, folder: str) -> str:
        """
        获取父文件夹路径

        Args:
            folder: str 类型参数

        Returns:
            字符串:
                : 失败
                其他: 父文件夹路径
        """
        return self._dm.GetParentFolder(folder)

    def GetFolderPath(self, folder: str) -> str:
        """
        获取文件夹路径

        Args:
            folder: str 类型参数

        Returns:
            字符串:
                : 失败
                其他: 文件夹路径
        """
        return self._dm.GetFolderPath(folder)

    def GetDiskSerial(self, ) -> str:
        """
        获取硬盘序列号

        Returns:
            字符串:
                : 失败
                其他: 硬盘序列号
        """
        return self._dm.GetDiskSerial()

    def GetDiskModel(self, ) -> str:
        """
        获取硬盘型号

        Returns:
            字符串:
                : 失败
                其他: 硬盘型号
        """
        return self._dm.GetDiskModel()

    def GetCpuSerial(self, ) -> str:
        """
        获取CPU序列号

        Returns:
            字符串:
                : 失败
                其他: CPU序列号
        """
        return self._dm.GetCpuSerial()

    def GetCpuModel(self, ) -> str:
        """
        获取CPU型号

        Returns:
            字符串:
                : 失败
                其他: CPU型号
        """
        return self._dm.GetCpuModel()

    def GetMac(self, ) -> str:
        """
        获取MAC地址

        Returns:
            字符串:
                : 失败
                其他: MAC地址
        """
        return self._dm.GetMac()

    def GetNetIPByName(self, name: str) -> str:
        """
        通过网卡名获取IP

        Args:
            name: str 类型参数

        Returns:
            字符串:
                : 失败
                其他: IP地址
        """
        return self._dm.GetNetIPByName(name)

    def GetNetIP(self, ) -> str:
        """
        获取本机IP地址

        Returns:
            字符串:
                : 失败
                其他: IP地址
        """
        return self._dm.GetNetIP()

    def GetNetIPEx(self, ) -> str:
        """
        获取本机IP地址（扩展）

        Returns:
            字符串:
                : 失败
                其他: IP地址
        """
        return self._dm.GetNetIPEx()

    def EnableSpeedDx(self, enable: int) -> int:
        """
        启用SpeedDX模式

        Args:
            enable: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.EnableSpeedDx(enable)

    def EnableFakeActive(self, enable: int) -> int:
        """
        启用假激活模式

        Args:
            enable: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.EnableFakeActive(enable)

    def SendCommand(self, cmd: str) -> str:
        """
        发送命令

        Args:
            cmd: str 类型参数

        Returns:
            字符串:
                : 失败
                其他: 命令返回结果
        """
        return self._dm.SendCommand(cmd)

    def SendCommandEx(self, cmd: str, param: str) -> str:
        """
        发送命令（扩展）

        Args:
            cmd: str 类型参数
            param: str 类型参数

        Returns:
            字符串:
                : 失败
                其他: 命令返回结果
        """
        return self._dm.SendCommandEx(cmd, param)

    def GetResult(self, id: int) -> str:
        """
        获取异步结果

        Args:
            id: int 类型参数

        Returns:
            字符串:
                : 失败或未完成
                其他: 结果字符串
        """
        return self._dm.GetResult(id)

    def FreeResult(self, id: int) -> int:
        """
        释放异步结果

        Args:
            id: int 类型参数

        Returns:
            整形数:
                0: 失败
                1: 成功
        """
        return self._dm.FreeResult(id)



__all__ = ['DmSoft']


def create_dm(dll_path: Optional[str] = None, reg_dll_path: Optional[str] = None) -> DmSoft:
    """便捷创建函数"""
    return DmSoft(dll_path, reg_dll_path)