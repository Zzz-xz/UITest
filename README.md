<!--
 * @Author: Zzz 483393079@qq.com
 * @Date: 2025-11-06 18:59:15
 * @LastEditors: Zzz 483393079@qq.com
 * @LastEditTime: 2026-03-23 16:18:07
 * @FilePath: \UITest\README.md
 * @Description: 
-->

# SSH 客户端应用 (UITest)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![PySide6](https://img.shields.io/badge/PySide6-6.6%2B-orange?logo=qt)
![Paramiko](https://img.shields.io/badge/Paramiko-4.0%2B-green?logo=ssh)

一个基于 Python 和 PySide6 的图形化 SSH 客户端应用，提供直观的用户界面来管理远程服务器连接和执行命令。

## 🌟 功能特性

- **图形化界面**: 基于 Qt/QML 构建的现代化用户界面
- **SSH 连接管理**: 支持主机名、端口、用户名和密码认证
- **实时命令执行**: 可以在远程服务器上执行任意命令
- **预设命令**: 内置常用命令快捷操作（如查看当前路径、列出目录文件）
- **跨平台支持**: 支持 Windows、macOS 和 Linux 系统
- **打包部署**: 支持使用 PyInstaller 打包为独立可执行文件

## 🎥 演示视频

<video src="https://github.com/user-attachments/assets/31ec0f2f-c250-48d3-b977-50306961d825" width="50%" height="50%" controls autoplay></video>

## 🚀 快速开始

### 环境要求

- Python 3.9 或更高版本
- pip 包管理器

### 安装依赖

```bash
pip install -r requirements.txt
```

或者直接安装所需依赖：

```bash
pip install pyside6>=6.6.0 paramiko>=4.0.0
```

### 运行应用

```bash
python main.py
```

## 📁 项目结构

```
UITest/
├── main.py          # 应用程序入口点
├── ssh_logic.py     # SSH 连接和命令执行核心逻辑
├── cmds.py          # 预设命令函数集合
├── pyproject.toml   # 项目配置和依赖管理
├── README.md        # 项目说明文档
└── qml/             # QML 界面文件目录（需单独提供）
```

## 🔧 核心模块说明

### SSHLogic 类 (`ssh_logic.py`)
- 处理 SSH 连接的建立、断开和状态管理
- 提供错误处理和用户反馈机制
- 支持各种 SSH 异常情况的优雅处理

### 预设命令 (`cmds.py`)
- `get_remote_current_path()`: 获取远程服务器当前工作目录
- `get_remote_dir_files()`: 列出远程服务器当前目录的文件详情

### 主程序 (`main.py`)
- 初始化 Qt 应用程序
- 加载 QML 界面文件
- 注册 SSH 逻辑对象到 QML 上下文

## 📦 打包部署

项目配置了 PyInstaller 支持，可以打包为独立的可执行文件：

```bash
# 安装开发依赖
pip install pyinstaller>=6.16.0

# 打包应用（需要先准备qml目录）
pyinstaller --name ssh_client --noconsole --hidden-import paramiko --hidden-import PySide6.QtCore --hidden-import PySide6.QtWidgets main.py
```
## 💻 使用示例

1. 启动应用：`python main.py`
2. 在界面中输入远程服务器的：
   - 主机名（IP地址或域名）
   - 端口号（默认22）
   - 用户名
   - 密码
3. 点击连接按钮建立SSH会话
4. 连接成功后可以执行任意命令或使用预设命令