# 🔍 为什么在 CodeBuddy 插件市场搜索不到插件？

## 问题分析

### ❌ 常见误解

很多开发者认为：
- 发布插件后就能在全局搜索到
- 有一个统一的官方插件市场
- 插件会自动被索引和发现

### ✅ 实际情况

根据 [CodeBuddy 官方文档](https://www.codebuddy.ai/docs/zh/cli/plugins)：

1. **没有统一的官方市场**
   - CodeBuddy 采用**分布式市场机制**
   - 每个市场都是独立的 Git 仓库或 HTTP 服务器
   - 用户需要**手动添加**想要使用的市场

2. **插件发现机制**
   - 用户必须先**添加市场源**
   - 系统才会索引该市场中的插件
   - 搜索只在已添加的市场中进行

3. **正确的市场结构**
   - 需要根目录的 `.codebuddy-plugin/marketplace.json`
   - 插件放在 `plugins/` 子目录
   - 每个插件有自己的 `plugin.json`

---

## 💡 解决方案

### 方案一：创建正确的市场结构（推荐）

我已经为你创建了符合规范的市场：

**市场位置**：`/Users/heluchao/WorkBuddy/Claw/bond-marketplace/`

**市场结构**：
```
bond-marketplace/
├── .codebuddy-plugin/
│   └── marketplace.json     # ✅ 市场清单（关键！）
├── plugins/
│   └── bond-monitor/        # 插件目录
│       ├── .codebuddy-plugin/
│       │   └── plugin.json  # ✅ 插件清单
│       ├── commands/
│       ├── skills/
│       ├── scripts/
│       └── README.md
└── README.md
```

### 步骤 1：推送到 GitHub

```bash
# 创建 GitHub 仓库
# 访问：https://github.com/new
# 仓库名：bond-marketplace

# 初始化并推送
cd /Users/heluchao/WorkBuddy/Claw/bond-marketplace
git init
git add .
git commit -m "feat: 创建 CodeBuddy 插件市场"
git remote add origin https://github.com/HeLuchao/bond-marketplace.git
git push -u origin main
```

### 步骤 2：用户添加市场

```bash
# 用户需要执行这个命令来添加你的市场
codebuddy plugin marketplace add https://github.com/HeLuchao/bond-marketplace -n heluchao-market

# 然后就可以搜索和安装了
codebuddy plugin install bond-monitor@heluchao-market
```

---

## 🔄 对比：两种结构

### ❌ 错误结构（之前）

```
bond-monitor-plugin/
├── .codebuddy-plugin/
│   ├── plugin.json          # 这是插件清单
│   └── marketplace.json     # ❌ 不应该在插件根目录
├── commands/
├── skills/
└── scripts/
```

**问题**：
- 混淆了"市场"和"插件"的概念
- `marketplace.json` 应该在**市场根目录**，而不是插件目录
- 这是一个插件，不是一个市场

### ✅ 正确结构（现在）

```
bond-marketplace/                # 市场根目录
├── .codebuddy-plugin/
│   └── marketplace.json         # ✅ 市场清单
└── plugins/
    ├── bond-monitor/            # 插件 1
    │   ├── .codebuddy-plugin/
    │   │   └── plugin.json      # ✅ 插件清单
    │   └── ...
    └── another-plugin/          # 插件 2（未来可以添加更多）
        └── ...
```

**优势**：
- 清晰的市场-插件层级关系
- 可以托管多个插件
- 符合官方规范
- 用户添加一次市场就能看到所有插件

---

## 📚 用户使用流程

### 完整的安装步骤

#### 1. 添加市场

```bash
# 方式一：命令行
codebuddy plugin marketplace add https://github.com/HeLuchao/bond-marketplace -n heluchao-market

# 方式二：交互式
/plugin → 添加市场 → 输入 URL
```

#### 2. 搜索插件

```bash
# 在已添加的市场中搜索
codebuddy plugin list --marketplace heluchao-market

# 或使用交互式界面
/plugin → Browse → 选择市场 → 查看插件
```

#### 3. 安装插件

```bash
# 安装
codebuddy plugin install bond-monitor@heluchao-market
```

---

## 🎯 核心要点

### 为什么搜索不到？

1. **没有全局市场**
   - CodeBuddy 没有统一的市场
   - 每个市场都是独立的

2. **需要手动添加**
   - 用户必须先添加你的市场
   - 系统才会索引你的插件

3. **正确的结构**
   - 市场：`.codebuddy-plugin/marketplace.json`
   - 插件：`plugins/[name]/.codebuddy-plugin/plugin.json`

---

## 🚀 下一步行动

### 1. 推送新的市场仓库

```bash
cd /Users/heluchao/WorkBuddy/Claw/bond-marketplace
git init
git add .
git commit -m "feat: 创建 CodeBuddy 插件市场"
git remote add origin git@github.com:HeLuchao/bond-marketplace.git
git push -u origin main
```

### 2. 更新文档

在你的项目中说明用户如何添加市场：

```markdown
## 安装方式

1. 添加插件市场：
```bash
codebuddy plugin marketplace add https://github.com/HeLuchao/bond-marketplace -n heluchao-market
```

2. 安装插件：
```bash
codebuddy plugin install bond-monitor@heluchao-market
```
```

### 3. 分享市场地址

- GitHub 仓库：`https://github.com/HeLuchao/bond-marketplace`
- 用户添加命令：`codebuddy plugin marketplace add https://github.com/HeLuchao/bond-marketplace`

---

## 📖 参考文档

- [CodeBuddy 插件系统官方文档](https://www.codebuddy.ai/docs/zh/cli/plugins)
- [marketplace.json 格式说明](https://www.codebuddy.ai/docs/zh/cli/plugins#marketplacejson)
- [插件目录结构规范](https://www.codebuddy.ai/docs/zh/cli/plugins#插件目录结构)

---

<div align="center">

**总结：创建正确的市场结构，推送后让用户添加市场即可搜索到！**

</div>
