#!/bin/bash

# 配置
APP_NAME="小锐云桥(被控端)"
TEAM_ID="52MJ3RAU3G"
CERT_NAME="Developer ID Application: Beijing Yiyuan Information Technology Co., Ltd. (52MJ3RAU3G)"
KEYCHAIN_PROFILE="Ruijie_Profile"

echo "🔐 开始签名和公证流程..."

# 1. 移除旧签名
echo "📝 移除旧签名..."
codesign --remove-signature "${APP_NAME}.app"

# 2. 签名框架
echo "🔧 签名框架..."
find "${APP_NAME}.app/Contents/Frameworks" -name "*.framework" -exec \
  codesign --deep --force --sign "${CERT_NAME}" --options runtime {} \;

find "${APP_NAME}.app/Contents/Frameworks" -name "*.dylib" -exec \
  codesign --force --sign "${CERT_NAME}" --options runtime {} \;

# 3. 签名主应用
echo "✍️  签名主应用..."
codesign --deep --force --sign "${CERT_NAME}" \
  --options runtime \
  --entitlements entitlements.plist \
  "${APP_NAME}.app"

# 4. 验证签名
echo "✅ 验证签名..."
codesign -vvv --deep --strict "${APP_NAME}.app"

# 5. 创建 ZIP
echo "📦 创建 ZIP..."
ditto -c -k --keepParent "${APP_NAME}.app" "${APP_NAME}.zip"

# 6. 提交公证
echo "📤 提交公证..."
xcrun notarytool submit "${APP_NAME}.zip" \
  --keychain-profile "${KEYCHAIN_PROFILE}" \
  --wait

# 7. 装订票据
echo "📎 装订票据..."
xcrun stapler staple "${APP_NAME}.app"

# 8. 验证
echo "🔍 验证公证..."
xcrun stapler validate "${APP_NAME}.app"

# 9. 创建 DMG
echo "💿 创建 DMG..."
create-dmg \
  --volname "${APP_NAME}" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --app-drop-link 600 185 \
  "Ruijie-SOS_MacOS-notarized.dmg" \
  "${APP_NAME}.app"

echo "✅ 完成！"
echo "📦 已创建：Ruijie-SOS_MacOS-notarized.dmg"