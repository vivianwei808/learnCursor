from playwright.sync_api import sync_playwright
import json
from datetime import datetime
import os
import time

def get_changelog():
    url = 'https://www.cursor.com/changelog'
    
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            print(f"正在访问: {url}")
            page.goto(url)
            
            # 等待页面加载
            page.wait_for_load_state('networkidle')
            time.sleep(3)  # 额外等待以确保内容加载
            
            # 打印页面源码以便调试
            print("\n页面源码预览:")
            print(page.content()[:1000])
            
            # 尝试不同的选择器
            changelog_items = []
            
            # 方法1：查找所有包含版本信息的元素
            items = page.query_selector_all('[class*="changelog"], [class*="version"]')
            if items:
                print(f"找到 {len(items)} 个可能的更新日志项")
                changelog_items = items
            
            # 方法2：如果没有找到，尝试查找所有包含日期的元素
            if not changelog_items:
                items = page.query_selector_all('[class*="date"], [class*="time"]')
                if items:
                    print(f"找到 {len(items)} 个包含日期的项")
                    changelog_items = items
            
            # 方法3：如果还是没有找到，尝试查找所有 h3 标签
            if not changelog_items:
                items = page.query_selector_all('h3')
                if items:
                    print(f"找到 {len(items)} 个 h3 标签")
                    changelog_items = items
            
            changelog_data = []
            
            for item in changelog_items:
                try:
                    # 提取版本号
                    version = item.query_selector('h3') or item
                    version = version.text_content().strip() if version else "Unknown Version"
                    
                    # 提取日期
                    date = item.query_selector('time') or item
                    date = date.text_content().strip() if date else "Unknown Date"
                    
                    # 提取内容
                    content = item.query_selector('[class*="content"], p') or item
                    content = content.text_content().strip() if content else item.text_content().strip()
                    
                    changelog_data.append({
                        'version': version,
                        'date': date,
                        'content': content
                    })
                    
                    print(f"\n找到更新日志项:")
                    print(f"版本: {version}")
                    print(f"日期: {date}")
                    print(f"内容: {content[:100]}...")
                    
                except Exception as e:
                    print(f"处理项目时出错: {e}")
                    continue
            
            return changelog_data
            
        except Exception as e:
            print(f"爬取过程中出错: {e}")
            return None
            
        finally:
            browser.close()

def save_to_file(data):
    if not data:
        return
    
    # 创建输出目录
    output_dir = 'changelog_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 生成文件名（使用当前时间戳）
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{output_dir}/cursor_changelog_{timestamp}.json'
    
    # 保存为 JSON 文件
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"更新日志已保存到: {filename}")
    
    # 同时保存为文本文件
    txt_filename = f'{output_dir}/cursor_changelog_{timestamp}.txt'
    with open(txt_filename, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(f"版本: {item['version']}\n")
            f.write(f"日期: {item['date']}\n")
            f.write(f"内容:\n{item['content']}\n")
            f.write("-" * 50 + "\n\n")
    
    print(f"文本格式更新日志已保存到: {txt_filename}")

def main():
    print("开始爬取 Cursor 更新日志...")
    changelog_data = get_changelog()
    
    if changelog_data:
        print(f"\n成功获取 {len(changelog_data)} 条更新记录")
        save_to_file(changelog_data)
    else:
        print("获取更新日志失败")

if __name__ == "__main__":
    main() 