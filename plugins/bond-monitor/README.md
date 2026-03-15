# 可转债申购监控插件

<div align="center">

[![CodeBuddy Plugin](https://img.shields.io/badge/CodeBuddy-Plugin-blue.svg)](https://www.codebuddy.ai)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/HeLuchao/bond-monitor)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

**自动监控可转债申购机会，推送提醒到微信**

[功能特性](#功能特性) • [快速开始](#快速开始) • [使用指南](#使用指南) • [配置说明](#配置说明)

</div>

---

## 功能特性

✨ **智能查询**：自动获取今日和明日的可转债申购信息

📊 **数据分析**：提取关键指标（转股价值、发行规模、申购日期）

🔔 **微信推送**：通过 Server酱 实时推送到个人微信

⏰ **定时任务**：支持定时自动执行，不错过任何申购机会

🛡️ **错误处理**：完善的异常处理和日志记录

🧪 **测试模式**：支持 dry-run 模式，方便测试

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 Server酱

1. 访问 [Server酱官网](https://sct.ftqq.com/)
2. 使用微信扫码登录
3. 复制你的 SendKey

### 3. 运行查询

#### 命令行方式

```bash
# 基础查询
python scripts/query_bond.py --sendkey YOUR_SENDKEY

# 启用每日状态通知
python scripts/query_bond.py --sendkey YOUR_SENDKEY --daily-status

# 测试模式（不推送）
python scripts/query_bond.py --sendkey YOUR_SENDKEY --dry-run
```

#### 斜杠命令方式（CodeBuddy 中）

```bash
/bond-query --sendkey YOUR_SENDKEY
```

#### 对话方式（CodeBuddy 中）

```
用户：今天有什么新债申购吗？
助手：让我为你查询今日的可转债申购信息...
[自动查询并推送]
```

---

## 使用指南

### 基础使用

#### 1. 查询今日新债

```bash
python scripts/query_bond.py --sendkey SCT321629TV9CvNbMDefg
```

**输出示例：**

```
============================================================
[2026-03-12 09:00:00] 🔔 可转债申购监控启动
============================================================

🔄 正在获取可转债数据...
✅ 成功获取 450 条债券数据
📊 筛选出 2 只今日新债，1 只明日新债
📤 正在推送消息到微信...
✅ 推送成功: 今日有2只新债申购

============================================================
[2026-03-12 09:00:07] 监控任务完成
============================================================
```

#### 2. 测试模式

```bash
python scripts/query_bond.py --sendkey YOUR_SENDKEY --dry-run
```

**输出示例：**

```
🧪 测试模式：仅查询不推送

🔄 正在获取可转债数据...
✅ 成功获取 450 条债券数据

📊 查询结果：
  - 今日可申购：2 只
  - 明日可申购：1 只

今日新债：
  - XX转债（123456）
   - 申购日期：2026-03-12
   - 转股价值：105.32
   - 发行规模：10亿
```

### 高级功能

#### 1. 定时任务

使用 cron 设置定时任务：

```bash
# 编辑 crontab
crontab -e

# 添加以下内容（每天早上 8:00 执行）
0 8 * * * cd /path/to/bond-monitor && python scripts/query_bond.py --sendkey YOUR_SENDKEY --daily-status
```

#### 2. 环境变量配置

```bash
# 设置环境变量
export SERVERCHAN_SENDKEY="YOUR_SENDKEY"

# 使用环境变量
python scripts/query_bond.py --sendkey $SERVERCHAN_SENDKEY
```

#### 3. 日志记录

```bash
# 将输出重定向到日志文件
python scripts/query_bond.py --sendkey YOUR_SENDKEY >> bond_monitor.log 2>&1
```

---

## 配置说明

### 插件参数

#### 必需参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `serverchan_sendkey` | Server酱 SendKey | `SCT321629TV9CvNbMDefg` |

#### 可选参数

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `send_daily_status` | 是否发送每日状态通知 | `false` | `true` |
| `push_time` | 推送时间（24小时制，北京时间） | `08:00` | `08:30` |

### Server酱配置

#### 免费版限制

- 每天推送次数：5 次
- 消息长度：64KB

#### 升级版

- 每天推送次数：无限制
- 消息长度：无限制
- 支持 Telegram、钉钉等多渠道

---

## 推送内容示例

### 有新债时

```
🔔 可转债申购提醒

📅 今日可申购（2只）：
1. XX转债（123456）
   - 申购日期：2026-03-12
   - 转股价值：105.32
   - 发行规模：10亿

2. YY转债（123457）
   - 申购日期：2026-03-12
   - 转股价值：98.56
   - 发行规模：5亿

📅 明日可申购（1只）：
1. ZZ转债（123458）
   - 申购日期：2026-03-13
   - 转股价值：112.45
   - 发行规模：8亿

💡 提示：请提前准备申购资金
```

### 无新债时（启用每日状态）

```
🔔 可转债申购提醒

📭 今日无新债申购
明日也无新债申购

💡 提示：请提前准备申购资金
```

---

## 项目结构

```
bond-monitor-plugin/
├── .codebuddy-plugin/
│   └── plugin.json          # 插件清单
├── commands/
│   └── bond-query.md        # 斜杠命令定义
├── skills/
│   └── bond-monitor/
│       └── SKILL.md         # AI技能定义
├── scripts/
│   └── query_bond.py        # 核心脚本
├── requirements.txt         # Python依赖
└── README.md               # 本文档
```

---

## 开发指南

### 本地测试

```bash
# 1. 克隆仓库
git clone https://github.com/HeLuchao/bond-monitor.git
cd bond-monitor

# 2. 安装依赖
pip install -r requirements.txt

# 3. 测试运行
python scripts/query_bond.py --sendkey YOUR_SENDKEY --dry-run
```

### 添加新功能

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/new-feature`
3. 提交更改：`git commit -am 'Add new feature'`
4. 推送分支：`git push origin feature/new-feature`
5. 提交 Pull Request

---

## 常见问题

### Q1: 推送失败怎么办？

**A:** 检查以下几点：

1. SendKey 是否正确
2. 网络连接是否正常
3. Server酱服务是否正常
4. 是否超出每日推送限制

### Q2: 如何获取更多推送次数？

**A:** 两种方式：

1. 升级 Server酱 Pro 版
2. 使用多个 SendKey（不同微信账号）

### Q3: 周末会有推送吗？

**A:** 不会。周末和节假日没有新债申购，建议：

- 不设置周末的定时任务
- 或者启用 `--daily-status` 接收"无新债"提醒

### Q4: 如何查看历史推送？

**A:** 两种方式：

1. 在 Server酱 后台查看推送历史
2. 查看本地日志文件

---

## 更新日志

### v1.0.0 (2026-03-12)

- ✅ 初始版本发布
- ✅ 基础查询功能
- ✅ 微信推送支持
- ✅ 定时任务支持
- ✅ 错误处理机制
- ✅ 测试模式支持

---

## 相关资源

- [CodeBuddy 官方文档](https://www.codebuddy.ai/docs/zh/cli/plugins)
- [AkShare 官方文档](https://akshare.akfamily.xyz/)
- [Server酱 官网](https://sct.ftqq.com/)
- [GitHub 项目主页](https://github.com/HeLuchao/bond-monitor)

---

## 许可证

本项目采用 [MIT 许可证](LICENSE)

---

## 技术支持

如有问题或建议，请通过以下方式联系：

- 📧 Email: heluchao1994@gmail.com
- 💬 GitHub Issues: [提交问题](https://github.com/HeLuchao/bond-monitor/issues)
- 📖 项目文档: [查看文档](https://github.com/HeLuchao/bond-monitor/wiki)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star！⭐**

Made with ❤️ by HeLuchao

</div>
