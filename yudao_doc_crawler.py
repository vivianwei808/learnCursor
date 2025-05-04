import os
import time
import json
import random
from playwright.sync_api import sync_playwright, TimeoutError
from bs4 import BeautifulSoup
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
import re
import traceback
import webbrowser
import pyperclip
import asyncio

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class YudaoDocCrawler:
    def __init__(self):
        self.base_url = 'https://doc.iocoder.cn'
        self.output_dir = 'yudao_docs'
        self.menu_structure = []
        self.crawled_pages = set()
        self.error_pages = set()
        
        # 创建输出目录
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        # 加载已爬取的页面记录
        self.load_crawled_pages()

    def load_crawled_pages(self):
        """加载已爬取的页面记录"""
        try:
            if os.path.exists(os.path.join(self.output_dir, 'crawled_pages.json')):
                with open(os.path.join(self.output_dir, 'crawled_pages.json'), 'r', encoding='utf-8') as f:
                    self.crawled_pages = set(json.load(f))
                logging.info(f"已加载 {len(self.crawled_pages)} 个已爬取页面记录")
        except Exception as e:
            logging.warning(f"加载已爬取页面记录失败: {str(e)}")

    def save_crawled_pages(self):
        """保存已爬取的页面记录"""
        try:
            with open(os.path.join(self.output_dir, 'crawled_pages.json'), 'w', encoding='utf-8') as f:
                json.dump(list(self.crawled_pages), f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.warning(f"保存已爬取页面记录失败: {str(e)}")

    def random_sleep(self):
        """随机等待一段时间，避免频繁请求"""
        time.sleep(random.uniform(1, 2))

    def setup_browser(self, context):
        """设置浏览器"""
        context.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        })

    def inject_bypass_script(self, page):
        """注入绕过VIP限制的脚本"""
        bypass_script = """
        (function() {
            'use strict';

            // 禁用弹窗
            window.jqueryAlert = function(opts) {
                var dialog;
                dialog.show = function() {}
                return dialog;
            }

            // 存储原始文档内容
            let originalDoc = null;
            let prevPath = document.location.pathname;

            // VIP 限制路径列表
            const blockPathList = [
                "/bpm/", "/user-center/", "/social-user/", "/oauth2/", "/saas-tenant/", 
                "/sms/", "/mail/", "/notify/", "/mybatis-pro/", "/dynamic-datasource/", 
                "/report/", "/Spring-Boot", "/Spring-Cloud", "/api-doc/", "/module-new/", 
                "/new-feature/", "/dev-hot-swap/", "/file/", "/message-queue/", "/job/", 
                "/idempotent/", "/distributed-lock/", "/rate-limiter/", "/http-sign/", 
                "/project-rename/", "/delete-code/", "/resource-permission/", "/data-permission/", 
                "/deployment-linux/", "/deployment-docker/", "/deployment-baota", "/registry-center/", 
                "/config-center/", "/rpc/", "/gateway/", "/distributed-transaction/", 
                "/server-protection/", "/cloud-debug/", "/mp/", "/mall/", "/pay/", "/crm/", 
                "/member/", "/erp/", "/ai/", "/websocket/", "/vo/", "/system-log/"
            ];

            // 检查当前URL是否被限制
            const isBlocked = () => {
                return blockPathList.some((path) => document.location.pathname.includes(path));
            }

            // 获取文档内容包装器
            const getWrapper = () => {
                return document.querySelector('.content-wrapper');
            }

            // 替换内容
            const replaceContent = (content) => {
                const wrapper = getWrapper();
                if (content && wrapper) {
                    wrapper.innerHTML = content;
                }
            }

            // 监听内容变化
            const contentObserver = new MutationObserver(() => {
                const wrapper = getWrapper();
                if (wrapper && wrapper.innerHTML.includes('仅 VIP 可见')) {
                    replaceContent(originalDoc);
                }
            });

            // 监听URL变化
            const urlObserver = new MutationObserver(() => {
                if (prevPath !== document.location.pathname) {
                    window.location.reload();
                }
            });

            // 初始化
            const init = () => {
                const wrapper = getWrapper();
                if (wrapper && isBlocked()) {
                    originalDoc = wrapper.innerHTML.includes('仅 VIP 可见') ? null : wrapper.innerHTML;
                    
                    if (originalDoc) {
                        // 保存原始内容到全局变量
                        window.$$content = originalDoc;
                        window.$$replace = function() {
                            replaceContent(window.$$content);
                        }

                        // 开始监听
                        contentObserver.observe(wrapper, { 
                            childList: true, 
                            characterData: true, 
                            subtree: true 
                        });
                        urlObserver.observe(document.body, { childList: true });

                        // 立即替换内容
                        replaceContent(originalDoc);
                    }
                }
            }

            // 页面加载完成后初始化
            window.addEventListener('load', init);
            
            // 立即执行一次初始化
            init();
        })();
        """
        # 在页面加载完成后注入脚本
        page.evaluate(bypass_script)

    def is_vip_content(self, content_html):
        """检查是否为VIP内容"""
        return "仅 VIP 可见" in content_html

    def load_menu_structure(self):
        """加载菜单结构"""
        try:
            with open(os.path.join(self.output_dir, 'menu_structure.json'), 'r', encoding='utf-8') as f:
                self.menu_structure = json.load(f)
            logging.info(f"成功加载菜单结构，共 {len(self.menu_structure)} 个分类")
        except Exception as e:
            logging.error(f"加载菜单结构时发生错误: {str(e)}\n{traceback.format_exc()}")
            raise

    def sanitize_filename(self, filename):
        """清理文件名"""
        filename = re.sub(r'[\\/*?:"<>|]', '', filename)
        filename = filename.replace(' ', '_')
        return filename

    def get_vip_content(self, url):
        """获取VIP内容"""
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,  # 使用有头模式
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-features=IsolateOrigins,site-per-process',
                    '--disable-site-isolation-trials',
                    '--disable-web-security',
                    '--disable-features=BlockInsecurePrivateNetworkRequests'
                ]
            )
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                java_script_enabled=True,
                has_touch=True,
                locale='zh-CN',
                timezone_id='Asia/Shanghai'
            )
            
            # 设置浏览器
            context.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            })
            
            page = context.new_page()
            
            # 访问页面
            page.goto(url, wait_until='networkidle')
            
            # 等待内容加载
            page.wait_for_selector('.content-wrapper', timeout=60000)
            
            # 等待油猴脚本执行完成
            page.wait_for_timeout(5000)  # 等待5秒
            
            # 检查是否需要手动处理
            vip_content = page.query_selector('.content-wrapper')
            content_html = None
            if vip_content:
                content_html = vip_content.inner_html()
                if "仅 VIP 可见" in content_html:
                    logging.info("等待用户手动复制页面内容...")
                    print("\n请按照以下步骤操作：")
                    print("1. 在浏览器中等待油猴脚本执行完成")
                    print("2. 右键点击页面内容区域，选择'检查'")
                    print("3. 在开发者工具中找到 '.content-wrapper' 元素")
                    print("4. 右键点击该元素，选择'Copy' -> 'Copy outerHTML'")
                    print("5. 将复制的内容粘贴到此处，然后按回车键继续...")
                    
                    # 等待用户输入
                    content_html = input().strip()
                    
                    if not content_html:
                        logging.warning("未获取到用户输入的内容")
                        browser.close()
                        return None
            
            # 关闭浏览器
            browser.close()
            
            return content_html

    def crawl_page(self, page, url, title):
        """爬取单个页面"""
        try:
            # 检查是否已经爬取过
            if url in self.crawled_pages:
                logging.info(f"页面已爬取，跳过: {title} ({url})")
                return None
            
            if url in self.error_pages:
                logging.warning(f"页面之前爬取失败，跳过: {title} ({url})")
                return None

            logging.info(f"开始爬取页面: {title} ({url})")
            
            # 设置超时时间
            page.set_default_timeout(120000)  # 120秒
            
            # 访问页面
            try:
                response = page.goto(url, wait_until='networkidle')
                if not response:
                    raise Exception("页面响应为空")
            except Exception as e:
                logging.warning(f"页面加载异常，尝试重新加载: {url}")
                page.reload(wait_until='networkidle')
            
            self.random_sleep()
            
            # 等待内容加载
            try:
                page.wait_for_selector('.content-wrapper', timeout=60000)  # 60秒
            except Exception as e:
                logging.warning(f"等待内容加载超时: {url}")
            
            # 获取内容包装器
            content_wrapper = page.query_selector('.content-wrapper')
            if not content_wrapper:
                raise Exception("未找到内容包装器")
            
            # 获取内容
            content_html = content_wrapper.inner_html()
            if not content_html or not content_html.strip():
                raise Exception("页面内容为空")
            
            # 检查是否为VIP内容
            if self.is_vip_content(content_html):
                logging.info(f"检测到VIP内容，使用默认浏览器打开: {title} ({url})")
                print("\n请按照以下步骤操作：")
                print("1. 等待浏览器打开页面")
                print("2. 等待油猴脚本执行完成")
                print("3. 右键点击页面内容区域，选择'检查'")
                print("4. 在开发者工具中找到 '.content-wrapper' 元素")
                print("5. 右键点击该元素，选择'Copy' -> 'Copy outerHTML'")
                print("6. 按回车键继续...")
                
                # 使用默认浏览器打开页面
                webbrowser.open(url)
                
                # 等待用户操作完成
                input()
                
                # 获取剪贴板内容
                try:
                    content_html = pyperclip.paste()
                    if not content_html:
                        logging.warning("剪贴板内容为空")
                        self.error_pages.add(url)
                        return None
                except Exception as e:
                    logging.error(f"获取剪贴板内容失败: {str(e)}")
                    self.error_pages.add(url)
                    return None
            
            # 处理内容中的链接
            soup = BeautifulSoup(content_html, 'html.parser')
            
            # 处理所有链接
            for a in soup.find_all('a'):
                href = a.get('href', '')
                if href and not href.startswith(('http', '#')):
                    a['href'] = f"{self.base_url}{href}"
            
            # 处理所有图片
            for img in soup.find_all('img'):
                src = img.get('src', '')
                if src and not src.startswith(('http', 'data:')):
                    img['src'] = f"{self.base_url}{src}"
            
            # 保存页面内容
            filename = self.sanitize_filename(title)
            with open(os.path.join(self.output_dir, f"{filename}.html"), 'w', encoding='utf-8') as f:
                f.write(str(soup))
            
            self.crawled_pages.add(url)
            self.save_crawled_pages()  # 保存已爬取页面记录
            logging.info(f"成功爬取页面: {title} ({url})")
            return str(soup)
            
        except TimeoutError as e:
            error_msg = f"页面加载超时: {url}\n{traceback.format_exc()}"
            logging.error(error_msg)
            self.error_pages.add(url)
            raise
        except Exception as e:
            error_msg = f"爬取页面 {url} 时发生错误: {str(e)}\n{traceback.format_exc()}"
            logging.error(error_msg)
            self.error_pages.add(url)
            raise

    def generate_menu_html(self):
        """生成菜单HTML"""
        html = '<div class="menu">'
        for category in self.menu_structure:
            html += f'<div class="category"><h3>{category["title"]}</h3>'
            html += '<ul>'
            for item in category['items']:
                filename = self.sanitize_filename(item['title'])
                html += f'<li><a href="{filename}.html">{item["title"]}</a></li>'
            html += '</ul></div>'
        html += '</div>'
        return html

    def generate_html(self, menu_html, content_html):
        """生成完整的HTML文档"""
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Yudao 文档</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    display: flex;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif;
                }}
                .menu {{
                    width: 300px;
                    height: 100vh;
                    overflow-y: auto;
                    padding: 20px;
                    background-color: #f3f4f5;
                    position: fixed;
                }}
                .content {{
                    margin-left: 320px;
                    padding: 20px;
                    flex-grow: 1;
                }}
                .category {{
                    margin-bottom: 20px;
                }}
                .category h3 {{
                    margin: 0 0 10px 0;
                    color: #2c3e50;
                }}
                ul {{
                    list-style: none;
                    padding: 0;
                    margin: 0;
                }}
                li {{
                    margin: 5px 0;
                }}
                a {{
                    color: #476582;
                    text-decoration: none;
                }}
                a:hover {{
                    color: #3eaf7c;
                }}
                .theme-default-content {{
                    max-width: 960px;
                    margin: 0 auto;
                    padding: 2rem 2.5rem;
                }}
                .theme-default-content img {{
                    max-width: 100%;
                }}
                .theme-default-content pre {{
                    background-color: #f8f8f8;
                    padding: 1em;
                    border-radius: 4px;
                    overflow-x: auto;
                }}
                .theme-default-content code {{
                    background-color: #f8f8f8;
                    padding: 0.2em 0.4em;
                    border-radius: 3px;
                }}
            </style>
        </head>
        <body>
            {menu_html}
            <div class="content">
                <div class="theme-default-content">
                    {content_html}
                </div>
            </div>
        </body>
        </html>
        '''

    def run(self):
        try:
            # 加载菜单结构
            self.load_menu_structure()
            
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-features=IsolateOrigins,site-per-process',
                        '--disable-site-isolation-trials',
                        '--disable-web-security',
                        '--disable-features=BlockInsecurePrivateNetworkRequests'
                    ]
                )
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    java_script_enabled=True,
                    has_touch=True,
                    locale='zh-CN',
                    timezone_id='Asia/Shanghai'
                )
                
                # 设置浏览器
                self.setup_browser(context)
                page = context.new_page()
                
                # 爬取所有页面
                total_pages = sum(len(category['items']) for category in self.menu_structure)
                current_page = 0
                
                for category in self.menu_structure:
                    for item in category['items']:
                        current_page += 1
                        logging.info(f"进度: {current_page}/{total_pages} - {item['title']}")
                        
                        try:
                            content_html = self.crawl_page(page, item['url'], item['title'])
                            if content_html:
                                # 生成页面HTML
                                page_html = self.generate_html(self.generate_menu_html(), content_html)
                                
                                # 保存页面HTML
                                filename = self.sanitize_filename(item['title'])
                                with open(os.path.join(self.output_dir, f"{filename}.html"), 'w', encoding='utf-8') as f:
                                    f.write(page_html)
                        except Exception as e:
                            logging.error(f"处理页面 {item['title']} 时发生错误: {str(e)}")
                            continue
                
                # 生成首页
                if self.menu_structure and self.menu_structure[0]['items']:
                    first_page_url = self.menu_structure[0]['items'][0]['url']
                    first_page_title = self.menu_structure[0]['items'][0]['title']
                    try:
                        content_html = self.crawl_page(page, first_page_url, first_page_title)
                        if content_html:
                            index_html = self.generate_html(self.generate_menu_html(), content_html)
                            with open(os.path.join(self.output_dir, 'index.html'), 'w', encoding='utf-8') as f:
                                f.write(index_html)
                    except Exception as e:
                        logging.error(f"生成首页时发生错误: {str(e)}")
                
                browser.close()
                
                # 输出统计信息
                success_count = len(self.crawled_pages)
                error_count = len(self.error_pages)
                logging.info(f"爬取完成！成功: {success_count}, 失败: {error_count}")
                
                if error_count > 0:
                    logging.warning("失败的页面:")
                    for url in self.error_pages:
                        logging.warning(f"- {url}")
                
        except Exception as e:
            logging.error(f"运行过程中发生错误: {str(e)}\n{traceback.format_exc()}")
            raise

if __name__ == '__main__':
    crawler = YudaoDocCrawler()
    crawler.run() 