# 可转债申购查询

查询今日和明日的可转债申购信息，并推送到微信。

## 使用方法

```bash
/bond-query [--sendkey YOUR_SENDKEY] [--daily-status]
```

## 参数说明

- `--sendkey`（可选）：Server酱 SendKey，如果未提供则使用已配置的值
- `--daily-status`（可选）：是否发送每日状态通知（即使没有新债）

## 功能说明

此命令会：

1. 从 AkShare 获取最新的可转债申购数据
2. 筛选出今日和明日的可申购新债
3. 如果有新债或启用了 `--daily-status`，则推送到微信
4. 显示详细的查询结果和推送状态

## 示例

### 查询今日新债并推送

```bash
/bond-query --sendkey SCT321629TV9CvNbMDefg
```

### 启用每日状态通知

```bash
/bond-query --sendkey SCT321629TV9CvNbMDefg --daily-status
```

### 使用已配置的 SendKey

```bash
/bond-query
```

## 推送内容示例

```
🔔 可转债申购提醒

📅 今日可申购（2只）：
1. XX转债 (123456)
   - 申购日期：2026-03-12
   - 转股价值：105.32
   - 发行规模：10亿

2. YY转债 (123457)
   - 申购日期：2026-03-12
   - 转股价值：98.56
   - 发行规模：5亿

📅 明日可申购（1只）：
1. ZZ转债 (123458)
   - 申购日期：2026-03-13
   - 转股价值：112.45
   - 发行规模：8亿

💡 提示：请提前准备申购资金
```

## 配置要求

使用前需要配置 Server酱 SendKey，可以通过以下方式：

1. 在命令中直接传入 `--sendkey`
2. 在项目配置文件中设置环境变量
3. 在对话中配置参数

## 注意事项

- 需要网络连接访问 AkShare 数据源
- Server酱每天有推送次数限制（免费版 5 次/天）
- 建议在交易日早上 9:00 前执行查询
- 周末和节假日没有新债申购

## 相关资源

- [AkShare 官方文档](https://akshare.akfamily.xyz/)
- [Server酱 官网](https://sct.ftqq.com/)
- [可转债投资指南](https://github.com/HeLuchao/bond-monitor)
