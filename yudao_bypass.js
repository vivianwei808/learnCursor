// ==UserScript==
// @name         Yudao-Doc-Bypass
// @namespace    none
// @version      1.0
// @license      MIT
// @description  帮助访问 Yudao 文档的 VIP 内容
// @author       AI Assistant
// @match        https://www.iocoder.cn/*
// @match        https://doc.iocoder.cn/*
// @match        https://cloud.iocoder.cn/*
// @grant        unsafeWindow
// @run-at       document-end
// ==/UserScript==

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