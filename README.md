# 若依文档爬虫

这是一个用于爬取若依文档的爬虫工具，可以将若依文档网站的内容按照目录结构保存为本地HTML文件。

## 功能特点

- 自动爬取若依文档网站的目录结构
- 保存完整的文档内容
- 生成本地HTML文件，保持原有的目录结构
- 支持离线浏览

## 环境要求

- Python 3.7+
- Chrome浏览器
- ChromeDriver

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 确保已安装所有依赖
2. 运行爬虫脚本：

```bash
python yudao_doc_crawler.py
```

3. 爬取的内容将保存在 `yudao_docs` 目录下：
   - `index.html`: 完整的文档页面
   - `menu_structure.json`: 目录结构数据

## 注意事项

- 请确保网络连接正常
- 爬取过程中请勿关闭浏览器
- 建议使用代理访问以避免IP被封

## 项目结构

```
.
├── README.md
├── requirements.txt
├── yudao_doc_crawler.py
└── yudao_docs/
    ├── index.html
    └── menu_structure.json
```

## 会话总结

### 会话主要目的
- 创建一个爬虫工具来爬取若依文档网站的内容

### 完成的主要任务
- 创建了基本的项目结构
- 实现了文档爬虫的核心功能
- 添加了项目说明文档

### 关键决策和解决方案
- 使用 Selenium 进行网页爬取，以处理动态加载的内容
- 采用 BeautifulSoup 解析HTML结构
- 实现了目录结构的递归解析
- 生成本地HTML文件保持原有结构

### 使用的技术栈
- Python
- Selenium
- BeautifulSoup4
- Chrome WebDriver

### 修改的文件
- requirements.txt: 添加了必要的依赖包
- yudao_doc_crawler.py: 创建了爬虫主程序
- README.md: 添加了项目说明文档

## 2025-05-03 会话总结

### 主要目的
优化爬虫代码，解决VIP内容处理和超时问题

### 完成的主要任务
1. 优化了VIP内容处理逻辑
2. 增加了页面加载和内容等待的超时时间
3. 改进了错误处理和日志记录

### 关键决策和解决方案
1. 将破解脚本包装在立即执行函数中，避免全局变量污染
2. 在页面加载前注入破解脚本
3. 使用`networkidle`等待页面完全加载

### 使用的技术栈
- Python
- Playwright
- JavaScript

### 修改的文件
- `yudao_doc_crawler.py` 