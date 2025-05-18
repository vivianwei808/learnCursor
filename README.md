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

### 越野跑记录微信小程序数据库设计

以下是完整的数据库设计 SQL 文件：

```sql
-- 1. 用户表
CREATE TABLE `itra_user` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `openid` varchar(50) NOT NULL COMMENT '微信OpenID',
  `nickname` varchar(50) DEFAULT NULL COMMENT '用户昵称',
  `avatar_url` varchar(255) DEFAULT NULL COMMENT '头像URL',
  `height` decimal(5,2) DEFAULT NULL COMMENT '身高(cm)',
  `age` int(11) DEFAULT NULL COMMENT '年龄',
  `itra_score` decimal(5,2) DEFAULT NULL COMMENT 'ITRA积分',
  `gender` varchar(10) DEFAULT NULL COMMENT '性别',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `openid` (`openid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户信息表';

-- 2. 越野跑跑前记录表
CREATE TABLE `itra_trail_run_pre` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `name` varchar(100) NOT NULL COMMENT '记录名称',
  `run_date` date NOT NULL COMMENT '跑步日期',
  `weather` varchar(50) DEFAULT NULL COMMENT '天气',
  `pre_run_status` varchar(255) DEFAULT NULL COMMENT '跑前状态',
  `run_type` enum('比赛','个人跑山') NOT NULL COMMENT '跑步类型',
  `total_distance` decimal(10,2) DEFAULT NULL COMMENT '总距离(km)',
  `total_elevation` decimal(10,2) DEFAULT NULL COMMENT '总爬升(m)',
  `track_file_url` varchar(255) DEFAULT NULL COMMENT '轨迹文件URL',
  `cp_points` text DEFAULT NULL COMMENT 'CP点信息(JSON)',
  `route_features` text DEFAULT NULL COMMENT '路线特点',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='越野跑跑前记录表';

-- 3. 越野跑跑后记录表
CREATE TABLE `itra_trail_run_post` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '记录ID',
  `pre_run_id` bigint(20) NOT NULL COMMENT '跑前记录ID',
  `post_run_photos` text DEFAULT NULL COMMENT '完赛照片URLs(JSON)',
  `finish_time` time DEFAULT NULL COMMENT '完赛时间',
  `participants_count` int(11) DEFAULT NULL COMMENT '比赛人数',
  `ranking` int(11) DEFAULT NULL COMMENT '排名',
  `special_notes` text DEFAULT NULL COMMENT '特别惊喜',
  `post_run_status` varchar(255) DEFAULT NULL COMMENT '跑后状态',
  `improvement_measures` text DEFAULT NULL COMMENT '改进措施',
  `achievements` text DEFAULT NULL COMMENT '成就',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `pre_run_id` (`pre_run_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='越野跑跑后记录表';

-- 4. 路线段表
CREATE TABLE `itra_route_segment` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '段ID',
  `pre_run_id` bigint(20) NOT NULL COMMENT '跑前记录ID',
  `segment_name` varchar(100) DEFAULT NULL COMMENT '段名称',
  `distance` decimal(10,2) NOT NULL COMMENT '距离(km)',
  `elevation` decimal(10,2) DEFAULT NULL COMMENT '爬升(m)',
  `surface_type` varchar(50) DEFAULT NULL COMMENT '路面类型',
  `technical_analysis` text DEFAULT NULL COMMENT '技术分析',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `pre_run_id` (`pre_run_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='路线段表';

-- 5. 装备表
CREATE TABLE `itra_equipment` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '装备ID',
  `name` varchar(100) NOT NULL COMMENT '装备名称',
  `function` varchar(255) DEFAULT NULL COMMENT '功能',
  `brand` varchar(100) DEFAULT NULL COMMENT '品牌',
  `is_mandatory` tinyint(1) DEFAULT '0' COMMENT '是否强制装备',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='装备表';

-- 6. 用户装备关联表
CREATE TABLE `itra_user_equipment` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '关联ID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `equipment_id` bigint(20) NOT NULL COMMENT '装备ID',
  `race_id` bigint(20) NOT NULL COMMENT '比赛ID',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `equipment_id` (`equipment_id`),
  KEY `race_id` (`race_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户装备关联表';

-- 7. UTMB比赛信息表
CREATE TABLE `itra_utmb_race` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '比赛ID',
  `name` varchar(100) NOT NULL COMMENT '比赛名称',
  `location` varchar(255) NOT NULL COMMENT '比赛地点',
  `race_date` date NOT NULL COMMENT '比赛日期',
  `day_of_week` varchar(10) DEFAULT NULL COMMENT '周几',
  `registration_link` varchar(255) DEFAULT NULL COMMENT '报名链接',
  `stone_count` int(11) DEFAULT NULL COMMENT '可积累跑石数量',
  `expected_weather` varchar(50) DEFAULT NULL COMMENT '预计天气',
  `progress` varchar(50) DEFAULT NULL COMMENT '进度',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='UTMB比赛信息表';

-- 8. 统计报表表
CREATE TABLE `itra_statistics_report` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '报表ID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `report_type` varchar(50) NOT NULL COMMENT '报表类型',
  `report_data` text NOT NULL COMMENT '报表数据(JSON)',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='统计报表表';

-- 9. 奖章表
CREATE TABLE `itra_medal` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '奖章ID',
  `name` varchar(100) NOT NULL COMMENT '奖章名称',
  `description` varchar(255) DEFAULT NULL COMMENT '奖章描述',
  `image_url` varchar(255) DEFAULT NULL COMMENT '奖章图片URL',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='奖章表';

-- 10. 用户奖章关联表
CREATE TABLE `itra_user_medal` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '关联ID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `medal_id` bigint(20) NOT NULL COMMENT '奖章ID',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `medal_id` (`medal_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户奖章关联表';

-- 11. 朋友圈排行榜表
CREATE TABLE `itra_friend_ranking` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '排行ID',
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `itra_score` decimal(5,2) DEFAULT NULL COMMENT 'ITRA积分',
  `race_count` int(11) DEFAULT '0' COMMENT '参与比赛次数',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='朋友圈排行榜表';
```

---

### 会话总结

- **主要目的**：为越野跑记录微信小程序设计数据库结构，并按要求调整表名和拆分记录表。
- **完成的主要任务**：设计了11个数据库表，覆盖用户信息、越野跑记录（跑前和跑后）、路线分析、装备、UTMB比赛信息、统计报表、奖章和排行榜等功能。
- **关键决策和解决方案**：采用关系型数据库设计，去掉所有外键，并在 `itra_user_equipment` 表中增加 `race_id` 字段，同时将 `improvements` 字段改为 `improvement_measures`，并将 `success_points` 字段改为 `achievements`。
- **使用的技术栈**：MySQL
- **修改了哪些文件**：无代码文件修改，仅生成数据库设计文档。

请查看更新后的 `README.md` 文件以获取完整的数据库设计。

