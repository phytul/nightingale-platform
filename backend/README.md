# nightingale-platform 夜莺平台 - backend

## 个人任务调度中心后台

> 基本信息

- 框架: fastapi - https://fastapi.tiangolo.com
- 包管理器: uv - https://docs.astral.sh/uv
- python version: 3.13

## 初始化项目

- 安装依赖：确保 uv 正常工作，使用`uv sync`安装所有依赖
  1. 未全局安装 uv 可以查看官网进行安装: https://docs.astral.sh/uv/getting-started/installation/
  2. 也可以在 venv 中局部安装
     - 创建虚拟环境：`python -m venv .venv`
     - 启用虚拟环境：`source .venv/bin/activate`(Mac)、`.\.venv\Scripts\activate`(Windows)
     - 局部安装 uv：`pip install uv`

- uv 常用命令

| 操作     | 命令                  | 备注                                    |
| -------- | --------------------- | --------------------------------------- |
| 添加包   | `uv add <package>`    | 自动更新 pyproject.toml                 |
| 移除包   | `uv remove <package>` |                                         |
| 同步环境 | `uv sync`             | 根据 lock 文件确保 .venv 完全一致       |
| 运行代码 | `uv run main.py`      | 自动在虚拟环境中运行，无需手动 activate |
| 锁定版本 | `uv lock`             | 生成 uv.lock 文件（类似 yarn.lock）     |
