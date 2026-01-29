#!/bin/bash

echo "=== RuijieDesk-SOS 客户端诊断 ==="
echo ""

# 1. 检查客户端文件
echo "1. 检查可用的客户端文件："
ls -lh exe/*/Ruijie-SOS_Winx64.exe 2>/dev/null | awk '{print $6, $7, $8, $9}'

echo ""
echo "最新客户端（推荐测试）："
echo "  exe/393df99c-9896-4970-a8ac-1eca88cf785a/Ruijie-SOS_Winx64.exe"
echo "  生成时间: 2026-01-27 22:27"
echo "  配置: ✓ 已修复"

echo ""
echo "2. 配置目录状态："
if [ -d "RuijieDesk-SOS" ]; then
    echo "  ✗ 配置目录存在: RuijieDesk-SOS/"
    echo "  建议: 删除后重新测试"
    echo "  命令: rm -rf RuijieDesk-SOS/"
else
    echo "  ✓ 配置目录已删除"
fi

echo ""
echo "=== 测试步骤 ==="
echo "1. 删除旧配置："
echo "   rm -rf RuijieDesk-SOS/"
echo ""
echo "2. 运行最新客户端："
echo "   exe/393df99c-9896-4970-a8ac-1eca88cf785a/Ruijie-SOS_Winx64.exe"
echo ""
echo "3. 检查配置文件："
echo "   cat RuijieDesk-SOS/config/RuijieDesk-SOS2.toml"
echo ""
echo "应该看到："
echo "  - app-name = 'RuijieDesk-SOS'"
echo "  - conn_type = 'incoming'"
echo "  - disable_settings = true"
echo "  - hide-menu-bar = 'Y'"

