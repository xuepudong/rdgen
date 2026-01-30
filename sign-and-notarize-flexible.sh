#!/bin/bash

# 配置
TEAM_ID="52MJ3RAU3G"
CERT_NAME="Developer ID Application: Beijing Yiyuan Information Technology Co., Ltd. (52MJ3RAU3G)"
KEYCHAIN_PROFILE="Ruijie_Profile"

# 检查是否提供了应用路径参数
if [ -n "$1" ]; then
    APP_PATH="$1"
    echo "📍 使用指定的应用路径: $APP_PATH"
else
    # 自动查找 .app 文件
    echo "🔍 在当前目录查找 .app 文件..."
    APP_PATH=$(find . -maxdepth 1 -name "*.app" -type d | head -1)

    if [ -z "$APP_PATH" ]; then
        echo "❌ 错误: 未找到 .app 文件"
        echo "用法: $0 [应用路径.app]"
        echo "示例: $0 \"小锐云桥(被控端).app\""
        exit 1
    fi

    echo "📍 找到应用: $APP_PATH"
fi

# 验证应用存在
if [ ! -d "$APP_PATH" ]; then
    echo "❌ 错误: 应用不存在: $APP_PATH"
    exit 1
fi

# 获取应用名称（不含 .app 后缀）
APP_NAME=$(basename "$APP_PATH" .app)
echo "📱 应用名称: $APP_NAME"

echo "🔐 开始签名和公证流程..."

# 1. 移除旧签名
echo "📝 移除旧签名..."
codesign --remove-signature "$APP_PATH"

# 2. 签名框架
echo "🔧 签名框架..."
find "$APP_PATH/Contents/Frameworks" -name "*.framework" -exec \
  codesign --deep --force --sign "$CERT_NAME" --options runtime {} \;

find "$APP_PATH/Contents/Frameworks" -name "*.dylib" -exec \
  codesign --force --sign "$CERT_NAME" --options runtime {} \;

# 3. 签名主应用
echo "✍️  签名主应用..."
codesign --deep --force --sign "$CERT_NAME" \
  --options runtime \
  --entitlements entitlements.plist \
  "$APP_PATH"

# 4. 验证签名
echo "✅ 验证签名..."
codesign -vvv --deep --strict "$APP_PATH"

# 5. 创建 ZIP
echo "📦 创建 ZIP..."
ZIP_NAME="${APP_NAME}.zip"
ditto -c -k --keepParent "$APP_PATH" "$ZIP_NAME"

# 6. 提交公证
echo "📤 提交公证..."
xcrun notarytool submit "$ZIP_NAME" \
  --keychain-profile "$KEYCHAIN_PROFILE" \
  --wait

# 7. 装订票据
echo "📎 装订票据..."
xcrun stapler staple "$APP_PATH"

# 8. 验证
echo "🔍 验证公证..."
xcrun stapler validate "$APP_PATH"

# 9. 创建 DMG
echo "💿 创建 DMG..."
DMG_NAME="${APP_NAME}-notarized.dmg"
create-dmg \
  --volname "$APP_NAME" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --app-drop-link 600 185 \
  "$DMG_NAME" \
  "$APP_PATH"

echo "✅ 完成！"
echo "📦 已创建：$DMG_NAME"
echo ""
echo "文件位置："
echo "  - 应用: $APP_PATH"
echo "  - ZIP: $ZIP_NAME"
echo "  - DMG: $DMG_NAME"
