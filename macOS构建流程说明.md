# macOS 构建和签名流程说明

## 📋 概述

本项目的 macOS 应用构建流程分为两个阶段：

1. **GitHub Actions 自动构建**：构建未签名的应用
2. **本地签名和公证**：在本地完成签名和公证

## 🔄 完整流程

### 阶段 1：GitHub Actions 构建（自动）

GitHub Actions 会自动：
- ✅ 构建 macOS 应用
- ✅ 创建应用图标
- ✅ 重命名应用
- ✅ 创建 DMG 文件
- ❌ **不进行签名**
- ❌ **不进行公证**

**输出：** 未签名的 DMG 文件

### 阶段 2：本地签名和公证（手动）

下载 DMG 后，在本地：
1. 提取应用
2. 签名应用
3. 公证应用
4. 装订公证票据
5. 重新打包 DMG

**输出：** 已签名和公证的 DMG 文件，可以分发给用户

## 📖 详细步骤

### 1. 触发 GitHub Actions 构建

1. 访问：https://github.com/xuepudong/rdgen/actions/workflows/generator-macos.yml
2. 点击 "Run workflow"
3. 填写参数：
   - version: 例如 `1.4.5`
   - zip_url: 配置 JSON 的 URL
4. 等待构建完成

### 2. 下载构建产物

从 GitHub Actions 下载生成的 DMG 文件。

### 3. 本地签名和公证

**详细步骤请参考：** [`本地签名和公证流程.md`](./本地签名和公证流程.md)

**快速命令：**

```bash
# 1. 挂载 DMG 并提取应用
hdiutil attach Ruijie-SOS_MacOS-aarch64.dmg
cp -R "/Volumes/小锐云桥(被控端)/小锐云桥(被控端).app" ./

# 2. 移除旧签名（如果有）
codesign --remove-signature "小锐云桥(被控端).app"

# 3. 重新签名
codesign --deep --force --sign "Developer ID Application: Beijing Yiyuan Information Technology Co., Ltd. (52MJ3RAU3G)" \
  --options runtime \
  --entitlements entitlements.plist \
  "小锐云桥(被控端).app"

# 4. 公证
ditto -c -k --keepParent "小锐云桥(被控端).app" "小锐云桥(被控端).zip"
xcrun notarytool submit "小锐云桥(被控端).zip" \
  --keychain-profile "Ruijie_Profile" \
  --wait

# 5. 装订票据
xcrun stapler staple "小锐云桥(被控端).app"

# 6. 创建最终 DMG
create-dmg \
  --volname "小锐云桥(被控端)" \
  --app-drop-link 600 185 \
  "Ruijie-SOS_MacOS-aarch64-signed.dmg" \
  "小锐云桥(被控端).app"
```

## 🔑 所需文件

- **`entitlements.plist`** - 应用权限配置文件（已包含在仓库中）
- **Developer ID Application 证书** - 在你的 macOS Keychain 中
- **Apple ID 和 App-Specific Password** - 用于公证

## ⚠️ 重要说明

### 为什么不在 GitHub Actions 中签名？

1. **安全性**：证书和密钥不需要上传到 GitHub
2. **灵活性**：可以随时调整签名参数
3. **调试方便**：本地可以立即看到结果
4. **避免权限问题**：避免 `get-task-allow` 等调试权限问题

### GitHub Actions 构建的应用能用吗？

- ✅ 可以在你自己的 Mac 上运行（右键打开）
- ❌ 不能直接分发给其他用户（会提示"不安全"）
- ✅ 签名和公证后可以正常分发

## 📚 相关文档

- [本地签名和公证流程.md](./本地签名和公证流程.md) - 详细的签名和公证指南
- [entitlements.plist](./entitlements.plist) - 应用权限配置

## 🎯 最终用户体验

完成签名和公证后，用户：
1. ✅ 下载 DMG
2. ✅ 双击打开
3. ✅ 拖到应用程序
4. ✅ 双击应用
5. ✅ **直接运行，无任何警告！**

## 🆘 需要帮助？

如果遇到问题，请查看：
- [本地签名和公证流程.md](./本地签名和公证流程.md) 中的"常见问题"部分
- Apple 官方文档：https://developer.apple.com/documentation/security/notarizing_macos_software_before_distribution
