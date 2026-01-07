# RustDesk 客户端生成器 - 附加功能说明

## 概述

本 RustDesk 客户端自定义生成器已集成 **24 个附加功能选项**，允许你完全定制客户端的界面和行为。

---

## ✅ 已集成的附加功能列表

### 🖥️ 界面显示功能

| 功能 | 字段名 | 默认值 | 说明 |
|------|--------|--------|------|
| 会话顶部添加显示器切换按钮 | `cycleMonitor` | ❌ | 在远程会话工具栏添加快速切换多显示器的按钮 |
| 在地址簿添加离线标记 | `xOffline` | ❌ | 使用 "X" 标记代替橙色圆圈表示设备离线 |
| 移除密码显示框 | `hidePassword` | ❌ | 隐藏主界面的密码显示区域 |
| 移除设置菜单 | `hideMenuBar` | ✅ | 完全隐藏设置菜单，防止用户修改配置 |
| 移除预设密码警告 | `removeTopNotice` | ✅ | 隐藏预设密码的警告提示 |
| 移除退出按钮 | `hideQuit` | ❌ | 隐藏程序退出按钮 |
| 添加复制按钮 | `addcopy` | ✅ | 在界面添加快速复制 ID 的按钮 |
| 隐藏系统托盘图标 | `hideTray` | ❌ | 不在系统托盘显示图标 |

### 🔒 安全与权限功能

| 功能 | 字段名 | 默认值 | 说明 |
|------|--------|--------|------|
| 禁止退出隐私模式 | `applyprivacy` | ✅ | 强制保持隐私模式，用户无法关闭 |
| 无条件隐藏连接管理器 | `supercm` | ❌ | 完全隐藏连接管理窗口（更彻底的隐藏） |
| 更改密码策略 | `passpolicy` | ❌ | 修改密码生成和验证策略 |
| 隐藏安全设置 | `hideSecuritySettings` | ❌ | 隐藏安全设置选项卡 |
| 隐藏网络设置 | `hideNetworkSettings` | ❌ | 隐藏网络配置选项 |
| 隐藏服务器设置 | `hideServerSettings` | ❌ | 隐藏服务器配置选项 |

### 🛠️ 功能控制

| 功能 | 字段名 | 默认值 | 说明 |
|------|--------|--------|------|
| 移除会话工具栏聊天功能 | `hide_chat_voice` | ❌ | 隐藏远程会话中的聊天和语音功能 |
| 隐藏远程打印设置 | `hideRemotePrinterSettings` | ❌ | 隐藏远程打印配置选项 |
| 仅查看模式 | `viewOnly` | ❌ | 强制仅查看模式，禁止所有控制操作 |

### 📦 安装与部署

| 功能 | 字段名 | 默认值 | 说明 |
|------|--------|--------|------|
| 移除卸载功能 | `no_uninstall` | ✅ | 移除卸载选项，防止用户卸载程序 |
| 制作便携版 | `disable_install` | ✅ | 编译为便携版，无需安装即可使用 |

### 🎨 渲染与性能

| 功能 | 字段名 | 默认值 | 说明 |
|------|--------|--------|------|
| 允许使用 Direct3D 渲染 | `allowD3dRender` | ✅ | 启用 Direct3D 硬件加速渲染 |
| 启用自适应比特率 | `enableAbr` | ✅ | 根据网络状况自动调整视频质量 |

### 🆔 身份识别

| 功能 | 字段名 | 默认值 | 说明 |
|------|--------|--------|------|
| 允许使用主机名作为 ID | `allowHostnameAsId` | ❌ | 允许使用计算机主机名代替数字 ID |
| 允许使用纯数字一次性密码 | `allowNumericOneTimePassword` | ✅ | 允许纯数字格式的一次性密码 |

### 🔔 通知管理

| 功能 | 字段名 | 默认值 | 说明 |
|------|--------|--------|------|
| 移除官方新版本通知 | `removeNewVersionNotif` | ❌ | 禁用官方新版本更新提示 |

---

## 🚀 使用方法

### 1. 启动 Web 界面

```bash
# 使用 Docker Compose
docker-compose up -d

# 或直接运行 Django
python manage.py runserver
```

### 2. 访问生成器

浏览器访问：`http://localhost:8000`

### 3. 配置附加功能

在 **"Additional Features"** 部分，勾选你需要的功能：

```
✅ 推荐的默认配置（已勾选）：
  - Remove settings menu (移除设置菜单)
  - Remove preset password warning (移除预设密码警告)
  - Add copy button (添加复制按钮)
  - Prevent exiting privacy mode (禁止退出隐私模式)
  - Remove uninstall function (移除卸载功能)
  - Make portable version (制作便携版)
  - Allow Direct3D rendering (允许 Direct3D 渲染)
  - Allow pure numeric one-time password (允许纯数字一次性密码)
  - Enable adaptive bitrate (启用自适应比特率)
```

### 4. 提交构建

点击 **"Generate Custom Client"** 按钮，等待云端编译完成（通常 5-15 分钟）。

---

## 📊 技术实现细节

### 数据流程

```
用户表单 (generator.html)
    ↓
Django 后端处理 (views.py)
    ↓
extras JSON 构建
    ↓
GitHub Actions 触发 (generator-*.yml)
    ↓
应用补丁和配置
    ↓
编译二进制文件
    ↓
回传到 rdgen 服务器
    ↓
用户下载
```

### 文件修改记录

#### 1. `rdgenerator/forms.py` (第 81-105 行)
- 添加了 24 个 `BooleanField` 字段
- 每个字段都设置了合理的默认值

#### 2. `rdgenerator/views.py`
- **第 30-50 行**: 添加字段提取逻辑
- **第 226-246 行**: 构建 `extras` JSON 字典

#### 3. `rdgenerator/templates/generator.html` (第 366-392 行)
- 添加 "Additional Features" 部分
- 使用 Django 模板语法渲染表单字段

---

## ⚙️ 配置传递机制

所有附加功能通过 **`extras` JSON** 传递给 GitHub Actions：

```json
{
  "hidePassword": "true",
  "hideMenuBar": "true",
  "removeTopNotice": "true",
  "addcopy": "true",
  "applyprivacy": "true",
  "no_uninstall": "true",
  "disable_install": "true",
  "allowD3dRender": "true",
  "allowNumericOneTimePassword": "true",
  "enableAbr": "true",
  ...
}
```

GitHub Actions 工作流在 `inputs.extras` 中接收这些值，并应用相应的补丁。

---

## 🔍 验证集成

### 快速检查

```bash
# 检查 forms.py 中的字段数量
grep -c "BooleanField" rdgenerator/forms.py
# 应该输出: 43 (包括其他布尔字段)

# 检查 views.py 中的 extras 条目
grep "extras\['" rdgenerator/views.py | wc -l
# 应该输出: 33 (包括 genurl、urlLink 等其他条目)

# 检查 generator.html 中的新字段
grep "form\\.hide" rdgenerator/templates/generator.html | wc -l
# 应该输出: 11 (所有以 hide 开头的字段)
```

---

## 🎯 典型使用场景

### 场景 1: 企业部署（高度锁定）

```
✅ 推荐启用：
  - Remove settings menu
  - Remove preset password warning
  - Prevent exiting privacy mode
  - Unconditionally hide connection manager
  - Remove uninstall function
  - Hide security settings
  - Hide network settings
  - Hide server settings
```

**目的**: 防止员工修改配置，确保统一管理。

---

### 场景 2: 客户支持工具

```
✅ 推荐启用：
  - Add copy button
  - Add monitor switch button
  - Allow Direct3D rendering
  - Enable adaptive bitrate
  - View-only mode (可选)
```

**目的**: 提供流畅的远程支持体验，同时控制权限。

---

### 场景 3: 便携版部署

```
✅ 推荐启用：
  - Make portable version
  - Remove uninstall function
  - Hide system tray icon (可选)
```

**目的**: 创建无需安装的绿色版本。

---

## 🛡️ 安全建议

1. **隐藏敏感设置**: 企业部署时建议启用所有 "Hide" 开头的选项
2. **强制隐私模式**: 启用 `applyprivacy` 防止被控端用户关闭隐私模式
3. **移除卸载功能**: 启用 `no_uninstall` 确保软件不被轻易删除
4. **锁定配置**: 启用 `hideMenuBar` 防止用户修改服务器地址等关键配置

---

## 📝 注意事项

1. **默认值已优化**: 带有 ✅ 标记的功能默认启用，已经过实际使用测试
2. **兼容性**: 所有功能与 RustDesk 1.3.3 - 1.4.4 版本兼容
3. **GitHub Actions 依赖**: 这些功能通过 GitHub Actions 在云端应用，需要确保工作流正常运行
4. **补丁文件**: 某些功能需要对应的补丁文件（位于 `.github/patches/` 目录）

---

## 🔧 故障排除

### 问题 1: 附加功能不生效

**检查项**:
- 确认 `extras` JSON 正确传递到 GitHub Actions
- 查看 GitHub Actions 工作流日志
- 验证补丁文件是否存在

### 问题 2: 编译失败

**检查项**:
- 查看 GitHub Actions 错误日志
- 确认 GitHub Token 权限正确
- 检查 RustDesk 版本兼容性

---

## 📞 支持

如有问题，请查看：
- GitHub Issues: `https://github.com/YOUR_REPO/issues`
- RustDesk 官方文档: `https://rustdesk.com/docs/`

---

**最后更新**: 2026-01-07
**版本**: v2.0 (集成 24 个附加功能)
