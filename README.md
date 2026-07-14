# DmPyGen - 大漠插件 Python 封装生成器

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)](https://www.microsoft.com/windows)

一键生成大漠插件(dm.dll)的 Python 封装类，包含 **200+ 个接口方法**，完整的类型注解和中文注释，让你写游戏自动化脚本时有完美的代码提示！

---

## ✨ 特性

- 🚀 **200+ 个接口方法** - 覆盖大漠插件 7.x 版本所有常用功能
- 💡 **完整代码提示** - 每个方法都有参数类型、中文描述、返回值说明
- 🎯 **多种生成模式** - 内置接口 / 动态提取 / 混合模式
- 🔧 **交互式菜单** - 无需记命令，直接运行按提示操作
- 📝 **免注册调用** - 支持 DmReg.dll 免注册方式
- 🛡️ **防检测支持** - 包含 MoveToEx、Delays 等防检测方法
- 🧵 **多线程支持** - 自动初始化 COM 组件，每个线程可独立创建实例

---

## 📦 安装

### 环境要求

- Windows 7/10/11
- Python 3.7+
- pywin32

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/x7dbg/DmPyGen.git
cd DmPyGen

# 安装依赖
pip install -r requirements.txt
```

---

## 🚀 快速开始

### 方式1：交互式菜单（推荐）

直接运行脚本，按提示选择生成方式：

```bash
python dm_generator.py
```

输出示例：

```
============================================================
        大漠插件 Python 类生成器
============================================================

生成方式选择：

  [1] 内置接口模式
      使用预定义的接口列表生成（推荐）
      优点：参数完整，有中文注释，代码提示最准确
      缺点：可能缺少最新版本的方法

  [2] 动态反射模式
      从 dm.dll 动态提取所有方法
      优点：包含所有方法，包括最新版本新增的
      缺点：参数信息不全，没有中文注释

  [3] 混合模式
      内置接口 + 动态提取的额外方法
      优点：兼顾完整性和准确性
      缺点：动态提取的方法没有参数提示

  [4] 命令行模式
      使用自定义参数生成

  [0] 退出

============================================================
请选择生成方式 [0-4]: 
```

### 方式2：命令行直接生成

```bash
# 仅使用内置接口（参数完整，有中文注释）
python dm_generator.py -o dm_soft.py

# 混合模式（内置 + 动态提取）
python dm_generator.py --dll ./dm.dll --reg ./DmReg.dll --dynamic -o dm_soft.py
```

---

## 📖 使用示例

### 基础用法

```python
from dm_soft import DmSoft

# 方式1：已注册调用（需先用 regsvr32 注册 dm.dll）
dm = DmSoft()

# 方式2：免注册调用（指定 dm.dll 和 DmReg.dll 路径）
dm = DmSoft(
    dll_path=r"C:\path\to\dm.dll",
    reg_dll_path=r"C:\path\to\DmReg.dll"
)

# 方式3：免注册调用（只指定 dm.dll，自动找同目录的 DmReg.dll）
dm = DmSoft(dll_path=r"C:\path\to\dm.dll")

# 注册插件
ret = dm.Reg("你的注册码", "")
if ret == 1:
    print("注册成功")
elif ret == 2:
    print("余额不足")
else:
    print(f"注册失败，错误码: {ret}")
```

### 窗口操作

```python
# 查找窗口（类名和标题支持模糊匹配，空字符串表示匹配所有）
hwnd = dm.FindWindow("", "游戏窗口标题")

# 绑定窗口（后台模式）
# display: normal/gdi/gdi2/dx2/opengl
# mouse: normal/windows/windows3
# keypad: normal/windows
dm.BindWindow(hwnd, "dx2", "windows", "windows", 0)

# 获取窗口大小
rect = dm.GetWindowRect(hwnd)  # 返回 "x1,y1,x2,y2"
```

### 找图找色

```python
# 找图
# pic_name: 图片文件名，多个用 | 分隔
# delta_color: 偏色，如 "000000-FFFFFF" 表示不偏色
# sim: 相似度，0.0-1.0，如 0.9 表示 90% 相似
# dir: 查找方向，0=从左到右从上到下, 1=从右到左, 2=从上到下, 3=从下到上
result = dm.FindPic(0, 0, 1920, 1080, "test.bmp", "000000", 0.9, 0)
if result != "-1|-1|-1":
    x, y, index = result.split("|")
    print(f"找到图片，坐标: ({x}, {y})")

# 找色
result = dm.FindColor(0, 0, 1920, 1080, "ff0000", 1.0, 0)
if result != "-1|-1":
    x, y = result.split("|")
    print(f"找到颜色，坐标: ({x}, {y})")
```

### 文字识别

```python
# 设置字库
dm.SetDict(0, "字库.txt")
dm.UseDict(0)

# 文字识别
# color_format: 颜色格式，如 "ffffff-000000" 表示白底黑字
text = dm.Ocr(0, 0, 100, 50, "ffffff-000000", 1.0)
print(f"识别结果: {text}")

# 找字
result = dm.FindStr(0, 0, 1920, 1080, "目标文字", "ffffff-000000", 0.9)
```

### 鼠标键盘

```python
# 移动鼠标
dm.MoveTo(100, 200)

# 防检测随机移动（在 100,100 为起点，50x50 范围内随机）
point = dm.MoveToEx(100, 100, 50, 50)
print(f"实际移动到: {point}")

# 点击
dm.LeftClick()

# 按键（虚拟键码）
dm.KeyPress(13)  # Enter键
dm.KeyPress(32)  # 空格键

# 发送字符串
dm.SendString(hwnd, "Hello World")
```

### 多线程调用

```python
import threading
from dm_soft import DmSoft

def worker(thread_id):
    # 每个线程创建独立实例，自动初始化 COM
    dm = DmSoft()
    
    # 查找并绑定窗口
    hwnd = dm.FindWindow("", f"窗口标题_{thread_id}")
    if hwnd:
        dm.BindWindow(hwnd, "normal", "normal", "normal", 0)
        dm.MoveTo(100, 100)
        dm.LeftClick()

# 创建多个线程
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

### 防检测技巧

```python
import random

# 随机延时（1000-3000毫秒）
dm.Delays(1000, 3000)

# 随机移动后点击
x, y = 500, 300
w, h = 20, 20
dm.MoveToEx(x, y, w, h)
dm.Delays(200, 500)
dm.LeftClick()

# 随机多次点击
for _ in range(random.randint(2, 4)):
    dm.LeftClick()
    dm.Delays(50, 150)
```

---

## 📋 接口分类

### 版本与注册（9个）

| 方法 | 说明 |
|------|------|
| `Ver()` | 获取版本号 |
| `Reg(reg_code, ver_info)` | 标准注册（绑定机器码） |
| `RegEx(reg_code, ver_info, ip)` | 高级注册（可指定IP） |
| `RegNoMac(reg_code, ver_info)` | 不绑定机器码注册 |
| `GetMachineCode()` | 获取机器码 |

### 窗口操作（19个）

| 方法 | 说明 |
|------|------|
| `FindWindow(class_name, title)` | 查找窗口 |
| `FindWindowEx(parent, class_name, title)` | 查找子窗口 |
| `GetWindowRect(hwnd)` | 获取窗口矩形 |
| `MoveWindow(hwnd, x, y)` | 移动窗口 |
| `SetWindowState(hwnd, flag)` | 设置窗口状态（0=关闭,1=激活,2=最小化...） |
| `EnumWindow(parent, title, class_name, filter)` | 枚举窗口 |

### 鼠标操作（12个）

| 方法 | 说明 |
|------|------|
| `MoveTo(x, y)` | 移动鼠标 |
| `MoveToEx(x, y, w, h)` | 随机移动（防检测） |
| `LeftClick()` | 左键单击 |
| `RightClick()` | 右键单击 |
| `GetCursorPos()` | 获取鼠标位置 |

### 键盘操作（6个）

| 方法 | 说明 |
|------|------|
| `KeyPress(key_code)` | 按键（虚拟键码） |
| `SendString(hwnd, input_str)` | 发送字符串 |
| `WaitKey(key_code, time_out)` | 等待按键 |

### 找图（10个）

| 方法 | 说明 |
|------|------|
| `FindPic(x1, y1, x2, y2, pic_name, delta_color, sim, dir)` | 找图 |
| `FindPicEx(x1, y1, x2, y2, pic_name, delta_color, sim, dir)` | 找图（返回所有结果） |
| `FindPicMem(x1, y1, x2, y2, pic_info, delta_color, sim, dir)` | 从内存找图 |

### 找色（8个）

| 方法 | 说明 |
|------|------|
| `FindColor(x1, y1, x2, y2, color, sim, dir)` | 找色 |
| `FindMultiColor(x1, y1, x2, y2, first_color, offset_color, sim, dir)` | 找多色 |
| `GetColor(x, y)` | 获取指定点颜色 |
| `CmpColor(x, y, color, sim)` | 比较颜色 |

### 文字识别（12个）

| 方法 | 说明 |
|------|------|
| `Ocr(x1, y1, x2, y2, color_format, sim)` | 文字识别 |
| `FindStr(x1, y1, x2, y2, string, color_format, sim)` | 找字 |
| `SetDict(index, file_name)` | 设置字库 |
| `UseDict(index)` | 使用字库 |

### 窗口绑定（12个）

| 方法 | 说明 |
|------|------|
| `BindWindow(hwnd, display, mouse, keypad, mode)` | 绑定窗口 |
| `BindWindowEx(hwnd, display, mouse, keypad, public_desc, mode)` | 高级绑定 |
| `UnBindWindow()` | 解绑窗口 |
| `EnableRealMouse(enable, mousedelay, mousestep)` | 启用真实鼠标模拟 |

### 截图（7个）

| 方法 | 说明 |
|------|------|
| `Capture(x1, y1, x2, y2, file_name)` | 截图保存为 BMP |
| `CapturePng(x1, y1, x2, y2, file_name)` | 截图保存为 PNG |
| `CaptureJpg(x1, y1, x2, y2, file_name, quality)` | 截图保存为 JPG |

### 内存操作（11个）

| 方法 | 说明 |
|------|------|
| `ReadInt(hwnd, addr)` | 读取内存整数 |
| `WriteInt(hwnd, addr, value)` | 写入内存整数 |
| `AsmCall(hwnd, asm, mode)` | 执行汇编代码 |

### 文件操作（15个）

| 方法 | 说明 |
|------|------|
| `ReadFile(file_name)` | 读取文件 |
| `WriteFile(file_name, content)` | 写入文件 |
| `DeleteFile(file_name)` | 删除文件 |

### 系统信息（10个）

| 方法 | 说明 |
|------|------|
| `GetOsType()` | 获取系统类型 |
| `GetMac()` | 获取MAC地址 |
| `GetNetIp()` | 获取本机IP |

### 其他（20个）

| 方法 | 说明 |
|------|------|
| `Delay(mis)` | 固定延时 |
| `Delays(mis_min, mis_max)` | 随机延时 |
| `GetClipboard()` | 获取剪贴板 |
| `SetClipboard(data)` | 设置剪贴板 |
| `Md5(data)` | 计算MD5 |

---

## 🛠️ 生成模式详解

### 模式1：内置接口模式 ⭐ 推荐

使用预定义的接口列表生成，**参数完整，有中文注释**。

```bash
python dm_generator.py
# 选择 [1]
```

**优点**：
- 所有方法都有完整的参数定义
- 每个参数都有中文描述（如：`x1 (int): 查找区域左上角X坐标`）
- 每个返回值都有详细说明（如：`{1: "成功", 0: "失败"}`）
- 代码提示最准确，IDE 可以自动补全和类型检查

**缺点**：
- 可能缺少最新版本大漠插件新增的方法

### 模式2：动态反射模式

从 COM 对象动态提取所有方法名。

```bash
python dm_generator.py --dll ./dm.dll --reg ./DmReg.dll
# 选择 [2]
```

**优点**：
- 包含所有方法，包括最新版本新增的
- 不需要维护接口列表

**缺点**：
- 参数信息不全（所有参数都是 `*args`）
- 没有中文注释
- 代码提示不够准确

### 模式3：混合模式

内置接口 + 动态提取的额外方法，兼顾完整性和准确性。

```bash
python dm_generator.py --dll ./dm.dll --reg ./DmReg.dll --dynamic
# 选择 [3]
```

**优点**：
- 内置方法有完整参数和注释
- 动态方法补充最新接口

**缺点**：
- 动态提取的方法没有参数提示

---

## 📁 项目结构

```
DmPyGen/
├── LICENSE                 # MIT 许可证
├── README.md              # 项目说明
├── dm_generator.py        # 代码生成器（核心）
├── dmsoft.py              # 生成的封装类示例
├── requirements.txt       # 依赖文件
└── examples/              # 示例代码
    ├── 01_basic_usage.py       # 基础使用
    ├── 02_find_and_click.py    # 找图点击
    ├── 03_window_bind.py       # 窗口绑定
    ├── 04_ocr_and_color.py     # 文字识别与找色
    ├── 05_multithread.py       # 多线程使用
    ├── 06_anti_detection.py    # 防检测技巧
    └── README.md               # 示例说明
```

---

## 📚 示例代码

项目提供了完整的示例代码，位于 `examples/` 目录：

| 示例 | 内容 | 难度 |
|------|------|------|
| `01_basic_usage.py` | 初始化、版本获取、鼠标移动 | ⭐ |
| `02_find_and_click.py` | 找图、解析结果、防检测点击 | ⭐⭐ |
| `03_window_bind.py` | 查找窗口、后台绑定、后台操作 | ⭐⭐ |
| `04_ocr_and_color.py` | OCR、颜色查找、颜色比较 | ⭐⭐ |
| `05_multithread.py` | 多线程找图、线程池 | ⭐⭐⭐ |
| `06_anti_detection.py` | 随机延时、人类轨迹、模拟点击 | ⭐⭐⭐ |

快速运行示例：

```bash
# 基础示例
python examples/01_basic_usage.py

# 找图点击示例（需修改图片路径）
python examples/02_find_and_click.py
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交 Issue

- 描述清楚问题和复现步骤
- 提供环境信息（Python版本、系统版本）
- 如果有错误信息，请贴出完整报错

### 提交 PR

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

---

## 📄 许可证

本项目基于 [MIT](LICENSE) 许可证开源。

---

## 🙏 致谢

- [大漠插件](http://www.dmplugin.net/) - 提供强大的 Windows 自动化功能
- [pywin32](https://github.com/mhammond/pywin32) - Python Windows 扩展

---

## 📮 联系方式

- GitHub: [@x7dbg](https://github.com/x7dbg)
- 项目地址: [https://github.com/x7dbg/DmPyGen](https://github.com/x7dbg/DmPyGen)

---

> ⚠️ **免责声明**：本项目仅供学习和研究使用，请勿用于非法用途。使用大漠插件进行游戏自动化可能违反游戏服务条款，请自行承担风险。