# CodeBuddy 插件市场

<div align="center">

[![CodeBuddy](https://img.shields.io/badge/CodeBuddy-Plugin%20Marketplace-blue.svg)](https://www.codebuddy.ai)
[![Plugins](https://img.shields.io/badge/Plugins-1-green.svg)](https://github.com/HeLuchao/bond-marketplace)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

**个人开发的实用工具插件集合**

</div>

---

## 📦 插件列表

### 1. bond-monitor - 可转债申购监控

**功能特性**：
- ✅ 自动查询今日/明日可转债申购信息
- ✅ 通过 Server酱 推送到个人微信
- ✅ 支持定时任务自动化
- ✅ 斜杠命令 + AI 技能双触发

**安装方式**：
```bash
# 添加此市场
codebuddy plugin marketplace add https://github.com/HeLuchao/bond-marketplace -n heluchao-market

# 安装插件
codebuddy plugin install bond-monitor@heluchao-market
```

**详细文档**：[插件 README](plugins/bond-monitor/README.md)

---

## 🚀 如何使用此市场

### 方式一：命令行添加（推荐）

```bash
# 添加市场
codebuddy plugin marketplace add https://github.com/HeLuchao/bond-marketplace -n heluchao-market

# 浏览插件
codebuddy plugin list --marketplace heluchao-market

# 安装插件
codebuddy plugin install bond-monitor@heluchao-market
```

### 方式二：项目配置

在项目根目录创建 `.codebuddy/settings.json`：

```json
{
  "pluginMarketplaces": [
    "https://github.com/HeLuchao/bond-marketplace"
  ],
  "plugins": [
    "bond-monitor"
  ]
}
```

### 方式三：交互式界面

在 CodeBuddy 中输入 `/plugin`，然后：
1. 点击"添加市场"
2. 输入：`https://github.com/HeLuchao/bond-marketplace`
3. 搜索 `bond-monitor` 并安装

---

## 📚 市场结构

```
bond-marketplace/
├── .codebuddy-plugin/
│   └── marketplace.json     # 市场清单（索引文件）
├── plugins/
│   └── bond-monitor/        # 插件目录
│       ├── .codebuddy-plugin/
│       │   └── plugin.json  # 插件清单
│       ├── commands/        # 斜杠命令
│       ├── skills/          # AI 技能
│       ├── scripts/         # 可执行脚本
│       └── README.md        # 插件文档
└── README.md               # 本文档
```

---

## ✅ 为什么搜索不到？

### 常见原因分析

1. **官方市场 vs 第三方市场**
   - CodeBuddy **没有统一的官方市场**
   - 需要用户**手动添加第三方市场**
   - 你的插件市场需要被添加后才能被搜索到

2. **正确的市场结构**
   - ✅ 根目录有 `.codebuddy-plugin/marketplace.json`
   - ✅ 插件在 `plugins/` 子目录中
   - ✅ 每个插件有自己的 `plugin.json`

3. **用户安装流程**
   ```bash
   # 第一步：添加你的市场
   codebuddy plugin marketplace add https://github.com/HeLuchao/bond-marketplace

   # 第二步：搜索或安装插件
   /plugin  # 在交互式界面中搜索
   ```

---

## 🔧 解决方案

### 已创建正确的市场结构

我已经为你创建了一个符合规范的插件市场：

**GitHub 仓库**：https://github.com/HeLuchao/bond-marketplace（需要创建）

**市场地址**：`https://github.com/HeLuchao/bond-marketplace`

**用户使用方式**：
```bash
# 添加市场后即可搜索到插件
codebuddy plugin marketplace add https://github.com/HeLuchao/bond-marketplace -n heluchao-market
```

---

## 📞 联系方式

- **开发者**：HeLuchao
- **Email**：heluchao@example.com
- **GitHub**：https://github.com/HeLuchao

---

<div align="center">

**如果这个市场对你有帮助，请给一个 Star！⭐**

Made with ❤️ by HeLuchao

</div>
