# 若依文档爬虫

这是一个用于爬取若依文档的爬虫工具，可以将若依文档网站的内容按照目录结构保存为本地HTML文件。

## 功能特点

- 自动爬取若依文档网站的目录结构
- 保存完整的文档内容
- 生成本地HTML文件，保持原有的目录结构
- 支持离线浏览
- 支持 VIP 内容的手动处理

## 环境要求

- Python 3.7+
- Chrome浏览器

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

3. 当检测到 VIP 内容时：
   - 程序会自动打开默认浏览器
   - 等待油猴脚本执行完成
   - 右键点击页面内容区域，选择"检查"
   - 在开发者工具中找到 ".content-wrapper" 元素
   - 右键点击该元素，选择"Copy" -> "Copy outerHTML"
   - 按回车键继续

4. 爬取的内容将保存在 `yudao_docs` 目录下：
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
├── yudao_bypass.js
└── yudao_docs/
    ├── index.html
    └── menu_structure.json
```

## 开发日志

### 2024-03-21
- 会话的主要目的：清理代码，删除不相关的功能
- 完成的主要任务：删除了所有与浏览器自动化和 VIP 内容自动处理相关的代码
- 关键决策和解决方案：保留核心功能，使用默认浏览器和手动复制内容的方式
- 使用的技术栈：Python、BeautifulSoup、webbrowser、pyperclip
- 修改了哪些文件：yudao_doc_crawler.py