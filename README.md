# Quant Base 量化交易基础框架

[English](#english) | [中文](#chinese)

<a name="english"></a>
## English

### Introduction
Quant Base is a fundamental framework for quantitative trading, providing basic functionalities for stock data fetching, processing, and management. It supports various data frequencies and offers both programmatic and command-line interfaces.

### Features
- Stock data fetching from multiple sources (Sina, Tencent)
- Support for multiple data frequencies (1d, 1m, 5m, 15m, 30m, 60m)
- Fuzzy stock name search
- Data caching and management
- Command-line interface for interactive usage

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/quant_base.git
cd quant_base
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage
#### Command Line Interface
Run the CLI application:
```bash
python -m src.interfaces.cli
```

Follow the interactive prompts to:
1. Search for stocks by company name
2. Select a stock from search results
3. Choose data frequency
4. View and save stock data

#### Programmatic Usage
```python
from src.controllers.data_controller import DataController

# Initialize controller
controller = DataController()
controller.initialize()

# Search for stocks
matches = controller.search_stock("company_name")

# Get stock data
success, data = controller.get_stock_data(
    code="sz300718",
    frequency="1d",
    count=5
)
```

### Testing
Run all tests:
```bash
python -m unittest discover tests
```

Run specific test modules:
```bash
python -m unittest tests/unit/test_stock_fetcher.py
python -m unittest tests/unit/test_stock_manager.py
python -m unittest tests/unit/test_data_controller.py
```

<a name="chinese"></a>
## 中文

### 简介
Quant Base 是一个量化交易基础框架，提供股票数据获取、处理和管理的基本功能。支持多种数据频率，并提供程序接口和命令行界面。

### 功能特点
- 从多个数据源获取股票数据（新浪、腾讯）
- 支持多种数据频率（日线、1分钟、5分钟、15分钟、30分钟、60分钟）
- 股票名称模糊搜索
- 数据缓存和管理
- 交互式命令行界面

### 安装方法
1. 克隆代码仓库：
```bash
git clone https://github.com/yourusername/quant_base.git
cd quant_base
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

### 使用方法
#### 命令行界面
运行命令行应用：
```bash
python -m src.interfaces.cli
```

按照交互提示进行操作：
1. 输入公司名称关键词搜索股票
2. 从搜索结果中选择股票
3. 选择数据频率
4. 查看并保存股票数据

#### 程序接口调用
```python
from src.controllers.data_controller import DataController

# 初始化控制器
controller = DataController()
controller.initialize()

# 搜索股票
matches = controller.search_stock("公司名称")

# 获取股票数据
success, data = controller.get_stock_data(
    code="sz300718",
    frequency="1d",
    count=5
)
```

### 测试
运行所有测试：
```bash
python -m unittest discover tests
```

运行特定测试模块：
```bash
python -m unittest tests/unit/test_stock_fetcher.py
python -m unittest tests/unit/test_stock_manager.py
python -m unittest tests/unit/test_data_controller.py
```

### 项目结构
```
quant_base/
├── src/                    # 源代码
│   ├── controllers/       # 控制器模块
│   ├── core/             # 核心功能模块
│   ├── features/         # 功能模块
│   ├── interfaces/       # 接口模块
│   ├── lib/             # 第三方库
│   └── utils/           # 工具函数
├── tests/                 # 测试代码
│   └── unit/            # 单元测试
├── data/                  # 数据目录
│   └── cache/           # 缓存数据
├── requirements.txt       # 项目依赖
└── README.md             # 项目说明
```
