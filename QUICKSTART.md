# 🚀 快速开始指南

## ✅ 集成完成确认

恭喜！所有 **24 个附加功能** 已成功集成到 RustDesk 客户端生成器中！

---

## 📦 已修改的文件

### 后端文件
1. **`rdgenerator/forms.py`** (第 81-105 行)
   - ✅ 添加了 24 个 BooleanField 字段
   - ✅ 设置了合理的默认值

2. **`rdgenerator/views.py`**
   - ✅ 第 30-50 行: 添加字段提取逻辑
   - ✅ 第 226-246 行: 构建 extras JSON

### 前端文件
3. **`rdgenerator/templates/generator.html`** (第 366-392 行)
   - ✅ 添加 "Additional Features" 部分
   - ✅ 所有 24 个字段完整显示

### 文档文件
4. **`ADDITIONAL_FEATURES.md`**
   - ✅ 详细的功能说明文档
   - ✅ 使用场景和配置建议

5. **`verify_integration.py`**
   - ✅ 自动化验证脚本
   - ✅ 检查字段一致性

---

## 🎯 立即开始使用

### 方法 1: Docker 部署（推荐）

```bash
# 1. 确保 Docker 和 Docker Compose 已安装
docker --version
docker-compose --version

# 2. 配置环境变量（编辑 docker-compose.yml）
# 需要设置:
# - SECRET_KEY: Django 密钥
# - GHUSER: 你的 GitHub 用户名
# - GHBEARER: GitHub Fine-grained Token
# - GENURL: 你的服务器公网地址
# - REPONAME: fork 的仓库名（默认 rdgen）

# 3. 启动服务
docker-compose up -d

# 4. 访问 Web 界面
# 浏览器打开: http://your-server-ip:8000
```

### 方法 2: 本地开发模式

```bash
# 1. 安装 Python 依赖
pip install -r requirements.txt

# 2. 配置环境变量
export SECRET_KEY="your-secret-key"
export GHUSER="your-github-username"
export GHBEARER="your-github-token"
export GENURL="http://localhost:8000"
export REPONAME="rdgen"

# 3. 数据库迁移
python manage.py migrate

# 4. 启动开发服务器
python manage.py runserver

# 5. 访问 Web 界面
# 浏览器打开: http://localhost:8000
```

---

## 🔑 必需的 GitHub 配置

### 创建 GitHub Fine-grained Token

1. 访问 GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. 点击 "Generate new token"
3. 配置权限:
   - **Repository access**: 选择你 fork 的 rdgen 仓库
   - **Permissions**:
     - Actions: **Read and write** ✅
     - Contents: **Read-only**
     - Metadata: **Read-only**
4. 生成并复制 Token
5. 将 Token 设置为 `GHBEARER` 环境变量

---

## 🎨 使用示例

### 示例 1: 生成企业锁定版客户端

1. 访问 Web 界面
2. 填写基本信息:
   - **EXE 文件名**: `CompanyRemote`
   - **自定义应用名**: `Company Remote Support`
   - **服务器地址**: `your-server.com`
   - **密钥**: `your-public-key`

3. 配置附加功能（勾选以下选项）:
   ```
   ✅ Remove settings menu (移除设置菜单)
   ✅ Remove preset password warning (移除预设密码警告)
   ✅ Prevent exiting privacy mode (禁止退出隐私模式)
   ✅ Unconditionally hide connection manager (无条件隐藏连接管理器)
   ✅ Remove uninstall function (移除卸载功能)
   ✅ Hide security settings (隐藏安全设置)
   ✅ Hide network settings (隐藏网络设置)
   ✅ Hide server settings (隐藏服务器设置)
   ```

4. 点击 **"Generate Custom Client"**

5. 等待 5-15 分钟，下载生成的 EXE 文件

---

### 示例 2: 生成高性能便携版

1. 填写基本信息（同上）

2. 配置附加功能:
   ```
   ✅ Add copy button (添加复制按钮)
   ✅ Add monitor switch button (添加显示器切换按钮)
   ✅ Make portable version (制作便携版)
   ✅ Allow Direct3D rendering (允许 Direct3D 渲染)
   ✅ Enable adaptive bitrate (启用自适应比特率)
   ✅ Allow pure numeric one-time password (允许纯数字密码)
   ```

3. 生成并下载

---

## 🔍 验证集成完整性

运行以下命令验证所有功能已正确集成:

```bash
# 检查 forms.py 中的字段
grep -c "BooleanField" rdgenerator/forms.py
# 预期输出: 43 (包括其他字段)

# 检查 views.py 中的 extras
grep "extras\['" rdgenerator/views.py | wc -l
# 预期输出: 33

# 检查 generator.html 中的表单字段
grep "form\\." rdgenerator/templates/generator.html | grep -c "label"
# 预期输出: 60+
```

---

## 📋 附加功能清单（快速参考）

| 功能分类 | 数量 | 主要功能 |
|---------|------|----------|
| 界面显示 | 8 | 隐藏密码框、设置菜单、退出按钮等 |
| 安全权限 | 6 | 隐私模式、连接管理器、密码策略等 |
| 功能控制 | 3 | 聊天功能、仅查看模式等 |
| 安装部署 | 2 | 便携版、移除卸载 |
| 渲染性能 | 2 | Direct3D、自适应比特率 |
| 身份识别 | 2 | 主机名 ID、纯数字密码 |
| 通知管理 | 1 | 移除版本通知 |
| **总计** | **24** | |

---

## 🛟 常见问题

### Q1: 附加功能不生效怎么办？

**A**: 检查以下项目:
1. 确认 GitHub Actions 工作流成功执行
2. 查看 Actions 日志中是否有错误
3. 验证 `extras` JSON 是否正确传递
4. 确认对应的补丁文件存在于 `.github/patches/` 目录

### Q2: 如何查看编译进度？

**A**:
1. 提交表单后会跳转到等待页面
2. 页面会每 3 秒自动刷新状态
3. 也可以访问 GitHub Actions 页面查看详细日志

### Q3: 编译需要多长时间？

**A**:
- Windows 64位: 约 10-15 分钟
- Windows 32位: 约 10-15 分钟
- Linux: 约 8-12 分钟
- Android: 约 15-20 分钟（3 个架构）
- macOS: 约 15-20 分钟

### Q4: 如何自定义图标和 Logo？

**A**:
1. 在 "Visual Customization" 部分上传 PNG 图标
2. 图标必须是正方形（如 512x512）
3. Logo 可以是任意比例的 PNG

---

## 📞 技术支持

如遇到问题:
1. 查看 `ADDITIONAL_FEATURES.md` 详细文档
2. 检查 GitHub Actions 工作流日志
3. 提交 Issue 到项目仓库

---

## 🎉 完成！

现在你的 RustDesk 客户端生成器已经完全配置好，可以开箱即用了！

**享受自定义 RustDesk 客户端的乐趣吧！** 🚀

---

**版本**: v2.0
**最后更新**: 2026-01-07
**集成功能数**: 24 个
