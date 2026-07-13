# DmPyGen - 大漠插件 Python 封装生成器

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)](https://www.microsoft.com/windows)

一键生成大漠插件(dm.dll)的 Python 封装类，包含 **200+ 个接口方法**，完整的类型注解和中文注释，让你写游戏自动化脚本时有完美的代码提示！

---

## ✨ 特性

- 🚀 **200+ 个接口方法** - 覆盖大漠插件 7.x 版本所有常用功能
- 💡 **完整代码提示** - 每个方法都有参数类型和中文注释
- 🎯 **多种生成模式** - 内置接口 / 动态提取 / 混合模式
- 🔧 **交互式菜单** - 无需记命令，直接运行按提示操作
- 📝 **免注册调用** - 支持 DmReg.dll 免注册方式
- 🛡️ **防检测支持** - 包含 MoveToEx、Delays 等防检测方法

---

## 📦 安装

### 环境要求

- Windows 7/10/11
- Python 3.7+
- pywin32

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/yourname/DmPyGen.git
cd DmPyGen

# 安装依赖
pip install pywin32
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

# 初始化（免注册调用）
dm = DmSoft(
    dll_path=r"C:\path\to\dm.dll",
    reg_dll_path=r"C:\path\to\DmReg.dll"
)

# 注册插件
ret = dm.reg("你的注册码", "")
if ret == 1:
    print("注册成功")
elif ret == 2:
    print("余额不足")
else:
    print(f"注册失败，错误码: {ret}")
```

### 窗口操作

```python
# 查找窗口
hwnd = dm.find_window("", "游戏窗口标题")

# 绑定窗口（后台模式）
dm.bind_window(hwnd, "dx2", "windows", "windows", 0)

# 获取窗口大小
rect = dm.get_window_rect(hwnd)  # 返回 "x1,y1,x2,y2"
```

### 找图找色

```python
# 找图
result = dm.find_pic(0, 0, 1920, 1080, "test.bmp", "000000", 0.9, 0)
if result != "-1|-1|-1":
    x, y, index = result.split("|")
    print(f"找到图片，坐标: ({x}, {y})")

# 找色
result = dm.find_color(0, 0, 1920, 1080, "ff0000", 1.0, 0)
if result != "-1|-1":
    x, y = result.split("|")
    print(f"找到颜色，坐标: ({x}, {y})")
```

### 文字识别

```python
# 设置字库
dm.set_dict(0, "字库.txt")
dm.use_dict(0)

# 文字识别
text = dm.ocr(0, 0, 100, 50, "ffffff-000000", 1.0)
print(f"识别结果: {text}")

# 找字
result = dm.find_str(0, 0, 1920, 1080, "目标文字", "ffffff-000000", 0.9)
```

### 鼠标键盘

```python
# 移动鼠标
dm.move_to(100, 200)

# 防检测随机移动（在 100,100 为起点，50x50 范围内随机）
point = dm.move_to_ex(100, 100, 50, 50)
print(f"实际移动到: {point}")

# 点击
dm.left_click()

# 按键
dm.key_press(13)  # Enter键

# 发送字符串
dm.send_string(hwnd, "Hello World")
```

### 防检测技巧

```python
import random

# 随机延时（1000-3000毫秒）
dm.delays(1000, 3000)

# 随机移动后点击
x, y = 500, 300
w, h = 20, 20
dm.move_to_ex(x, y, w, h)
dm.delays(200, 500)
dm.left_click()

# 随机多次点击
for _ in range(random.randint(2, 4)):
    dm.left_click()
    dm.delays(50, 150)
```

---

## 📋 接口分类

### 版本与注册（9个）

| 方法 | 说明 |
|------|------|
| `ver()` | 获取版本号 |
| `reg(reg_code, ver_info)` | 标准注册 |
| `reg_ex(reg_code, ver_info, ip)` | 高级注册 |
| `reg_no_mac(reg_code, ver_info)` | 不绑定机器码注册 |
| `get_machine_code()` | 获取机器码 |

### 窗口操作（19个）

| 方法 | 说明 |
|------|------|
| `find_window(class_name, title)` | 查找窗口 |
| `find_window_ex(parent, class_name, title)` | 查找子窗口 |
| `get_window_rect(hwnd)` | 获取窗口矩形 |
| `move_window(hwnd, x, y)` | 移动窗口 |
| `set_window_state(hwnd, flag)` | 设置窗口状态 |
| `enum_window(parent, title, class_name, filter)` | 枚举窗口 |

### 鼠标操作（12个）

| 方法 | 说明 |
|------|------|
| `move_to(x, y)` | 移动鼠标 |
| `move_to_ex(x, y, w, h)` | 随机移动（防检测） |
| `left_click()` | 左键单击 |
| `right_click()` | 右键单击 |
| `get_cursor_pos()` | 获取鼠标位置 |

### 键盘操作（6个）

| 方法 | 说明 |
|------|------|
| `key_press(key_code)` | 按键 |
| `send_string(hwnd, input_str)` | 发送字符串 |
| `wait_key(key_code, time_out)` | 等待按键 |

### 找图（10个）

| 方法 | 说明 |
|------|------|
| `find_pic(x1, y1, x2, y2, pic_name, delta_color, sim, dir)` | 找图 |
| `find_pic_ex(x1, y1, x2, y2, pic_name, delta_color, sim, dir)` | 找图（返回所有结果） |
| `find_pic_mem(x1, y1, x2, y2, pic_info, delta_color, sim, dir)` | 从内存找图 |

### 找色（8个）

| 方法 | 说明 |
|------|------|
| `find_color(x1, y1, x2, y2, color, sim, dir)` | 找色 |
| `find_multi_color(x1, y1, x2, y2, first_color, offset_color, sim, dir)` | 找多色 |
| `get_color(x, y)` | 获取指定点颜色 |
| `cmp_color(x, y, color, sim)` | 比较颜色 |

### 文字识别（12个）

| 方法 | 说明 |
|------|------|
| `ocr(x1, y1, x2, y2, color_format, sim)` | 文字识别 |
| `find_str(x1, y1, x2, y2, string, color_format, sim)` | 找字 |
| `set_dict(index, file_name)` | 设置字库 |
| `use_dict(index)` | 使用字库 |

### 窗口绑定（12个）

| 方法 | 说明 |
|------|------|
| `bind_window(hwnd, display, mouse, keypad, mode)` | 绑定窗口 |
| `bind_window_ex(hwnd, display, mouse, keypad, public_desc, mode)` | 高级绑定 |
| `unbind_window()` | 解绑窗口 |
| `enable_real_mouse(enable, mousedelay, mousestep)` | 启用真实鼠标 |

### 截图（7个）

| 方法 | 说明 |
|------|------|
| `capture(x1, y1, x2, y2, file_name)` | 截图 |
| `capture_png(x1, y1, x2, y2, file_name)` | 截图PNG |
| `capture_jpg(x1, y1, x2, y2, file_name, quality)` | 截图JPG |

### 内存操作（11个）

| 方法 | 说明 |
|------|------|
| `read_int(hwnd, addr)` | 读取内存整数 |
| `write_int(hwnd, addr, value)` | 写入内存整数 |
| `asm_call(hwnd, asm, mode)` | 执行汇编代码 |

### 文件操作（15个）

| 方法 | 说明 |
|------|------|
| `read_file(file_name)` | 读取文件 |
| `write_file(file_name, content)` | 写入文件 |
| `delete_file(file_name)` | 删除文件 |

### 系统信息（10个）

| 方法 | 说明 |
|------|------|
| `get_os_type()` | 获取系统类型 |
| `get_mac()` | 获取MAC地址 |
| `get_net_ip()` | 获取本机IP |

### 其他（20个）

| 方法 | 说明 |
|------|------|
| `delay(mis)` | 固定延时 |
| `delays(mis_min, mis_max)` | 随机延时 |
| `get_clipboard()` | 获取剪贴板 |
| `set_clipboard(data)` | 设置剪贴板 |
| `md5(data)` | 计算MD5 |

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
- 每个方法都有中文注释说明
- IDE 代码提示最准确

**缺点**：
- 可能缺少最新版本新增的方法

### 模式2：动态反射模式

从 dm.dll 动态提取所有方法。

```bash
python dm_generator.py --dll ./dm.dll --reg ./DmReg.dll
# 选择 [2]
```

**优点**：
- 包含所有方法，包括最新版本新增的
- 不会遗漏任何接口

**缺点**：
- 参数信息不全（都是 `*args`）
- 没有中文注释
- 代码提示不完整

### 模式3：混合模式

内置接口 + 动态提取的额外方法。

```bash
python dm_generator.py --dll ./dm.dll --reg ./DmReg.dll
# 选择 [3]
```

**优点**：
- 常用方法有完整参数提示
- 同时包含最新方法

**缺点**：
- 动态提取的方法没有参数提示

---

## 📁 项目结构

```
DmPyGen/
├── dm_generator.py      # 主生成器脚本
├── dm_soft.py           # 生成的封装类（示例）
├── README.md            # 本文件
├── LICENSE              # MIT 许可证
└── .gitignore
```

---

## ⚠️ 注意事项

1. **平台限制**：本工具仅支持 **Windows** 平台
2. **依赖要求**：需要安装 **pywin32**
3. **免注册调用**：使用免注册方式时需要 **DmReg.dll**
4. **管理员权限**：部分功能可能需要以管理员身份运行
5. **商业软件**：大漠插件为商业软件，请遵守其使用协议

---

## 🤝 贡献指南

欢迎提交 Issue 和 PR！

### 如何贡献

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

### 贡献内容

- 发现方法参数错误？
- 大漠升级了新接口？
- 想添加更多示例代码？
- 文档有改进建议？

统统欢迎！

---

## 📝 更新日志

### v1.0.0 (2024-XX-XX)

- ✨ 初始版本发布
- 🚀 支持 200+ 个大漠插件接口
- 💡 完整的类型注解和中文注释
- 🎯 多种生成模式（内置/动态/混合）
- 🔧 交互式菜单操作

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源许可证。

---

## 🙏 致谢

- [大漠插件](https://www.52hsxx.com/) - 提供强大的游戏自动化接口
- [pywin32](https://github.com/mhammond/pywin32) - Python Windows 扩展

---

**免责声明**：本工具仅供学习交流使用，请勿用于非法用途。使用本工具产生的任何后果由使用者自行承担。