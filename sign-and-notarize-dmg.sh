#!/bin/bash

# 配置
TEAM_ID="52MJ3RAU3G"
CERT_NAME="Developer ID Application: Beijing Yiyuan Information Technology Co., Ltd. (52MJ3RAU3G)"
KEYCHAIN_PROFILE="Ruijie_Profile"

# 检查是否提供了 DMG 文件参数
if [ -n "$1" ]; then
    INPUT_FILE="$1"
    echo "📍 使用指定的文件: $INPUT_FILE"
else
    # 自动查找 DMG 文件
    echo "🔍 在当前目录查找 DMG 文件..."
    INPUT_FILE=$(find . -maxdepth 1 -name "*.dmg" -type f | head -1)

    if [ -z "$INPUT_FILE" ]; then
        echo "❌ 错误: 未找到 DMG 文件"
        echo "用法: $0 [DMG文件路径]"
        echo "示例: $0 Ruijie-SOS_MacOS-aarch64.dmg"
        exit 1
    fi

    echo "📍 找到 DMG: $INPUT_FILE"
fi

# 验证文件存在
if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ 错误: 文件不存在: $INPUT_FILE"
    exit 1
fi

# 获取文件扩展名
FILE_EXT="${INPUT_FILE##*.}"

if [ "$FILE_EXT" = "dmg" ]; then
    echo "📦 检测到 DMG 文件，开始挂载..."

    # 挂载 DMG
    MOUNT_OUTPUT=$(hdiutil attach "$INPUT_FILE" | tail -1)
    VOLUME_PATH=$(echo "$MOUNT_OUTPUT" | awk '{print $3}')

    if [ -z "$VOLUME_PATH" ]; then
        echo "❌ 错误: 无法挂载 DMG"
        exit 1
    fi

    echo "✅ DMG 已挂载到: $VOLUME_PATH"

    # 查找 .app 文件
    APP_IN_DMG=$(find "$VOLUME_PATH" -maxdepth 1 -name "*.app" -type d | head -1)

    if [ -z "$APP_IN_DMG" ]; then
        echo "❌ 错误: DMG 中未找到 .app 文件"
        hdiutil detach "$VOLUME_PATH"
        exit 1
    fi

    APP_NAME=$(basename "$APP_IN_DMG" .app)
    echo "📱 找到应用: $APP_NAME"

    # 复制 .app 到当前目录
    echo "📋 复制应用到当前目录..."
    cp -R "$APP_IN_DMG" "./"
    APP_PATH="./${APP_NAME}.app"

    # 卸载 DMG
    echo "💿 卸载 DMG..."
    hdiutil detach "$VOLUME_PATH"

elif [ "$FILE_EXT" = "app" ] || [ -d "$INPUT_FILE" ]; then
    # 直接使用 .app 文件
    APP_PATH="$INPUT_FILE"
    APP_NAME=$(basename "$APP_PATH" .app)
    echo "📱 应用名称: $APP_NAME"
else
    echo "❌ 错误: 不支持的文件类型: $FILE_EXT"
    echo "支持的类型: .dmg, .app"
    exit 1
fi

echo ""
echo "🔐 开始签名和公证流程..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. 移除旧签名
echo ""
echo "📝 步骤 1/9: 移除旧签名..."
codesign --remove-signature "$APP_PATH" 2>/dev/null || true

# 2. 签名框架
echo ""
echo "🔧 步骤 2/9: 签名框架..."
find "$APP_PATH/Contents/Frameworks" -name "*.framework" -exec \
  codesign --deep --force --sign "$CERT_NAME" --options runtime {} \; 2>/dev/null

find "$APP_PATH/Contents/Frameworks" -name "*.dylib" -exec \
  codesign --force --sign "$CERT_NAME" --options runtime {} \; 2>/dev/null

# 3. 签名主应用
echo ""
echo "✍️  步骤 3/9: 签名主应用..."
codesign --deep --force --sign "$CERT_NAME" \
  --options runtime \
  --entitlements entitlements.plist \
  "$APP_PATH"

if [ $? -ne 0 ]; then
    echo "❌ 签名失败！"
    exit 1
fi

# 4. 验证签名
echo ""
echo "✅ 步骤 4/9: 验证签名..."
codesign -vvv --deep --strict "$APP_PATH"

if [ $? -ne 0 ]; then
    echo "❌ 签名验证失败！"
    exit 1
fi

# 5. 创建 ZIP
echo ""
echo "📦 步骤 5/9: 创建 ZIP..."
ZIP_NAME="${APP_NAME}.zip"
ditto -c -k --keepParent "$APP_PATH" "$ZIP_NAME"

# 6. 提交公证
echo ""
echo "📤 步骤 6/9: 提交公证（这可能需要几分钟）..."
xcrun notarytool submit "$ZIP_NAME" \
  --keychain-profile "$KEYCHAIN_PROFILE" \
  --wait

if [ $? -ne 0 ]; then
    echo "❌ 公证失败！"
    echo "💡 提示: 检查公证日志以了解失败原因"
    exit 1
fi

# 7. 装订票据
echo ""
echo "📎 步骤 7/9: 装订票据..."
xcrun stapler staple "$APP_PATH"

if [ $? -ne 0 ]; then
    echo "❌ 装订票据失败！"
    exit 1
fi

# 8. 验证
echo ""
echo "🔍 步骤 8/9: 验证公证..."
xcrun stapler validate "$APP_PATH"

# 9. 创建 DMG
echo ""
echo "💿 步骤 9/9: 创建已签名的 DMG..."
DMG_NAME="${APP_NAME}-signed.dmg"

# 删除旧的 DMG（如果存在）
[ -f "$DMG_NAME" ] && rm "$DMG_NAME"

create-dmg \
  --volname "$APP_NAME" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --app-drop-link 600 185 \
  "$DMG_NAME" \
  "$APP_PATH"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 完成！"
echo ""
echo "📂 生成的文件："
echo "  ├─ 应用: $APP_PATH"
echo "  ├─ ZIP: $ZIP_NAME"
echo "  └─ DMG: $DMG_NAME"
echo ""
echo "🎉 已签名和公证的 DMG 可以分发给用户了！"
