<div align="center">
<h1>✨ncatbot - EssenceManager 插件✨</h1>

一个功能完善的 NcatBot 群组精华消息管理插件，支持精华消息列表查看、添加精华消息等功能。


[![License](https://img.shields.io/badge/License-MIT_License-green.svg)](https://github.com/Sparrived/ncatbot-plugin-essence-manager/blob/master/LICENSE)
[![ncatbot version](https://img.shields.io/badge/ncatbot->=4.3.0-blue.svg)](https://github.com/liyihao1110/ncatbot)
[![Version](https://img.shields.io/badge/version-1.0.2-orange.svg)](https://github.com/Sparrived/ncatbot-plugin-essence-manager/releases)


</div>


---

## 🌟 功能亮点

- ✅ **精华列表** - 查看群内所有精华消息，支持分页显示和一次性显示全部
- ✅ **添加精华** - 支持通过消息ID或回复消息的方式添加精华消息
- ✅ **订阅机制** - 通过白名单限制插件作用范围，避免对未关注群组产生影响
- ✅ **权限检测** - 自动检测Bot权限，避免无权限操作导致的错误

## ⚙️ 配置项

配置文件位于 `data/EssenceManager/EssenceManager.yaml`

| 配置键 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `list_count` | `int` | `5` | 每次列出多少条精华消息（分页显示时使用） |
| `subscribed_groups` | `List[str]` | `['123456789']` | 插件生效的群号白名单。只有在此列表中的群组才会处理事件和命令。 |

**配置示例:**
```yaml
list_count: 5
subscribed_groups:
- '123456789'
- '987654321'
```

> **提示:** 配置文件可通过 NcatBot 的统一配置机制进行覆盖。建议使用 `/essence subscribe` 命令动态添加群组，避免手动修改配置后需要重启机器人。

## 🚀 快速开始

### 依赖要求

- Python >= 3.8
- NcatBot >= 4.3.0
- 无额外第三方依赖

### 使用 Git

```bash
git clone https://github.com/Sparrived/ncatbot-plugin-essence-manager.git
cd ncatbot-plugin-essence-manager
cp -r plugins/essence_manager /path/to/your/ncatbot/plugins/
```

> 请将 `/path/to/your/ncatbot/plugins/` 替换为机器人实际的插件目录。

### 自主下载

1. 将本插件目录置于 `plugins/essence_manager`。
2. 根据实际需要调整 `subscribed_groups` 等配置项（建议在群内使用指令调整，手动调整config需要重启机器人）。
3. 重启 NcatBot，插件将自动加载。

### 插件指令

> **注意事项:**
> - 所有指令仅限 NcatBot 管理员用户使用（`admin_group_filter` 限制）
> - 添加精华消息需要机器人有群管理员权限
> - 支持回复消息来快速添加精华（在 `add` 命令中）

| 指令 | 参数 | 说明 | 示例 |
| --- | --- | --- | --- |
| `/essence list [page] [-a\|--all]` | `page`：页码（可选，默认1）<br>`-a/--all`：显示所有消息 | 列出群内所有精华消息，支持分页或一次性显示全部 | `/essence list`<br>`/essence list 2`<br>`/essence list -a` |
| `/essence add [mid]` | `mid`：消息ID（可选） | 添加群精华消息。可提供消息ID，或回复想要添加的消息 | `/essence add 1234567890`<br>回复消息后发送 `/essence add` |
| `/essence subscribe` | 无 | 订阅群组精华消息管理功能 | `/essence subscribe` |
| `/essence unsubscribe` | 无 | 取消订阅群组精华消息管理功能 | `/essence unsubscribe` |
| `/essence help [command]` | `command`：可选，指定命令名 | 显示所有可用指令或指定命令的详细说明 | `/essence help`<br>`/essence help list` |



## 🧠 运作逻辑

### 订阅机制
- 插件在执行事件处理前，会先检查群组是否在 `subscribed_groups` 配置列表中
- 对于未订阅的群组，插件会跳过处理，同时在日志中输出调试信息
- 使用 `/essence subscribe` 可快速将当前群添加到白名单，无需重启机器人

### 精华消息列表
1. 调用平台接口获取群内所有精华消息
2. 按照配置的 `list_count` 进行分页显示
3. 每条精华显示：消息ID、发送者昵称和ID、设置时间、消息内容
4. 支持使用 `-a` 或 `--all` 参数一次性显示所有精华消息

### 添加精华消息
1. 支持两种方式添加精华：
   - 直接提供消息ID：`/essence add 消息ID`
   - 回复要添加的消息后发送：`/essence add`
2. 添加前会检测Bot是否具有管理员权限
3. 权限不足时会给出友好提示

### 权限检测机制
- **添加精华功能**: 要求Bot具有管理员或群主权限
- 执行前会自动检测权限，权限不足时会给出友好提示

## 🪵 日志与排错

插件使用 NcatBot 的统一日志系统，所有操作都会记录详细日志。

### 查看日志
```bash
# 日志文件位置
logs/bot.log.YYYY_MM_DD

# 筛选 EssenceManager 相关日志
grep "EssenceManager" logs/bot.log.2025_11_07
```

### 常见问题

**Q: 为什么指令没有响应？**
- 检查当前群是否已订阅（使用 `/essence subscribe`）
- 确认发送指令的用户是否在 NcatBot 的管理员列表中
- 查看日志确认是否有错误信息

**Q: 添加精华失败？**
- 确保机器人账号具有群管理员或群主权限
- 确认消息ID是否正确
- 如果使用回复方式，确保回复的是群内消息

**Q: 精华列表为空？**
- 确认群内是否已设置精华消息
- 检查 API 是否返回错误信息

**Q: 如何快速添加精华消息？**
- 直接回复想要添加的消息，然后发送 `/essence add` 即可


## 🤝 贡献

欢迎通过 Issue 或 Pull Request 分享改进建议、提交补丁！

### 贡献指南
1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范
- 遵循 PEP 8 Python 代码风格
- 添加必要的注释和文档字符串
- 确保代码通过基本功能验证


## 🙏 致谢

感谢以下项目和贡献者：

- [NcatBot](https://github.com/liyihao1110/ncatbot) - 提供稳定易用的 OneBot11 Python SDK
- 社区测试者与维护者 - 提交 Issue、Pull Request 以及改进建议

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

<div align="center">

如果本插件帮助到了你，欢迎为项目点亮 ⭐ Star！

[报告问题](https://github.com/Sparrived/ncatbot-plugin-essence-manager/issues) · [功能建议](https://github.com/Sparrived/ncatbot-plugin-essence-manager/issues) · [查看发布](https://github.com/Sparrived/ncatbot-plugin-essence-manager/releases)

</div>
