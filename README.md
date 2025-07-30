# Python_desktop-tools-unit

## 📖 写在最前面
> 该项目基于 Python 3.10.8 开发，使用 PyQt5 作为 UI 框架。
> 该项目仍处于开发阶段，其中部分内容源码设计暂未完成，功能在主程序中不可用

---

## ⭐️ 介绍
> 该程序基于日常工作学习需求开发，是一个桌面程序合计，集成了一些个人常用的工具及学习测试项目

---

## 📌 主要功能
- ✅ 功能 1：App主页（内容暂未添加）
- ✅ 功能 2：工作备忘录（支持保存，自动跳转到最近记录）
- ✅ 功能 3：基于API调用的AI助手（支持基本的短期记忆，对话内容复制）
- ✅ 功能 4：基于pillow的二维码生成器（支持自定义内容，生成并保存图片，复制二维码图片）

---

## 🆕 最近更新
| 日期 | 版本 | 变更摘要 |
|------|------|----------|
| 2025-07-30 | v0.1.0 | 整理代码并上传 github |

---

## 🛠️ 技术栈
- Python PyQt5 PyQt-Fluent-Widgets
- Openai API
- QR code pillow

---

## 🚀 快速开始
1. 克隆仓库  
   ```bash
   git clone https://github.com/yijiu2333/Python_desktop-tools-unit.git
   cd Python_desktop-tools-unit
   ```

2. 安装依赖
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3.  本地启动
   ```bash
   python main_window.py
   ```
---

## 🖼️ 程序总览
   ![home page](./github/home.png)
   ![AI assistant](./github/Eileen.png)
   ![QR generator](./github/qr.png)
   ![notebook](./github/notes.png)

---

## 🚫 版权说明
   - 整体项目：以 GPL-3.0 许可证发布（详见 LICENSE）
   - 第三方组件：
        - 界面框架 PyQt-Fluent-Widgets 采用 GPL-3.0，其源码已按许可证要求随附于 third_party/ 目录。
        - 其余引用的开源代码均已保留原始版权信息及许可证文件。
   - 使用限制：本项目仅供学习/作品集展示，内部包含的非商用资源（如示例图标、图片、字体。UI组件等）请自行替换后方可用于商业场景。

---

## 📄 许可证
   - 本项目整体以 **GPL-3.0** 发布  
   - 使用的 UI 库 [PyQt-Fluent-Widgets](https://github.com/zhiyiYo/PyQt-Fluent-Widgets) 亦为 GPLv3[^12^]
