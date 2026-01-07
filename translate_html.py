#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量汉化 generator.html 文件
"""

import re

# 汉化映射表
translations = {
    # 标题和章节
    "Save/Load Configuration": "保存/加载配置",
    "Save Configuration": "保存配置",
    "Load Configuration": "加载配置",
    "Select Platform": "选择平台",
    "General": "通用设置",
    "Custom Server": "自定义服务器",
    "Security": "安全设置",
    "Visual": "视觉定制",
    "Permissions": "权限控制",
    "Additional Features": "附加功能",
    "Other": "其他设置",

    # 平台相关
    "Windows 64 Bit": "Windows 64位",
    "Windows 32 Bit": "Windows 32位",

    # 通用设置
    "Name for EXE file": "EXE 文件名（仅英文字符）",
    "Custom App Name": "自定义应用程序名称",
    "Client type:": "客户端类型：",
    "Incoming Only": "仅被控端（仅接受连接）",
    "Outgoing Only": "仅控制端（仅发起连接）",
    "Bidirectional": "双向（可接受和发起连接）",
    "Disable Installation": "禁用安装",
    "No, enable installation": "否，允许安装",
    "Yes, DISABLE installation": "是，禁止安装",
    "Disable Settings": "禁用设置权限",
    "No, enable settings": "否，允许设置",
    "Yes, DISABLE settings": "是，禁止设置",
    "Custom Android App ID": "自定义 Android 应用 ID",
    "replaces 'com.carriez.flutter_hbb'": "替换默认包名 'com.carriez.flutter_hbb'",
    "Disable installation = User cannot install": "禁止安装 = 用户无法安装",
    "Fix delay when using custom API server": "修复使用自定义 API 时的连接延迟",

    # 服务器配置
    "Server address \\(Host\\):": "服务器地址 (Host)：",
    "Key:": "密钥 (Key)：",
    "API Server:": "API 服务器：",
    "Custom URL for links": "自定义网站链接",
    "Custom URL for downloading new versions": "自定义下载链接",
    "Company name": "版权公司名",

    # 安全设置
    "Approval mode:": "验证方式：",
    "Accept sessions via password": "通过密码接受会话",
    "Accept sessions via click": "通过点击接受会话",
    "Accepts sessions via both": "两者皆可",
    "Permanent password:": "永久密码：",
    "Deny LAN discovery": "禁止局域网内设备发现",
    "Enable direct IP connection": "启用直连 IP 连接",
    "Auto-disconnect when no operation": "无操作时自动关闭会话",
    "Hide settings to show/hide the remote connection manager from the remote side": "隐藏远程端的连接管理器",
    "Permanent Password Required": "需要设置永久密码",
    "A permanent password is required when the connection manager is hidden": "隐藏连接管理器时必须设置永久密码",

    # 视觉定制
    "Custom App Icon \\(in \\.png format\\)": "自定义应用图标（PNG 格式）",
    "Custom App Logo \\(in \\.png format\\)": "自定义品牌标识（PNG 格式）",
    "Theme:": "主题：",
    "Light": "浅色主题",
    "Dark": "深色主题",
    "Follow System": "跟随系统",
    "Default": "默认设置",
    "Override": "强制覆盖",

    # 权限控制
    "Permission type:": "权限预设：",
    "Custom": "自定义",
    "Full Access": "完全访问",
    "Screen share": "仅查看屏幕",
    "Enable keyboard/mouse": "启用键盘鼠标控制",
    "Enable clipboard": "启用剪贴板同步",
    "Enable file transfer": "启用文件传输",
    "Enable audio": "启用音频捕获",
    "Enable TCP tunneling": "启用 TCP 隧道",
    "Enable remote restart": "启用远程重启",
    "Enable recording session": "启用会话录制",
    "Enable blocking user input": "启用阻止输入",
    "Enable remote configuration modification": "启用远程修改配置",
    "Enable remote printer": "启用远程打印",
    "Enable remote camera": "启用摄像头访问",
    "Enable remote terminal": "启用终端访问",

    # 附加功能
    "Add monitor switch button to session toolbar": "会话顶部添加显示器切换按钮",
    "Add offline marker in address book": "在地址簿添加离线标记",
    "Remove official new version notification": "移除官方新版本通知",
    "Remove password display box": "移除密码显示框",
    "Remove settings menu": "移除设置菜单",
    "Remove preset password warning": "移除预设密码警告",
    "Remove exit button": "移除退出按钮",
    "Add copy button": "添加复制按钮",
    "Prevent exiting privacy mode": "禁止退出隐私模式",
    "Remove session toolbar chat function": "移除会话工具栏聊天功能",
    "Unconditionally hide connection manager": "无条件隐藏连接管理器",
    "Change password policy": "更改密码策略",
    "Remove uninstall function": "移除卸载功能",
    "Make portable version": "制作便携版",
    "Hide security settings": "隐藏安全设置",
    "Hide network settings": "隐藏网络设置",
    "Hide server settings": "隐藏服务器设置",
    "Hide remote printer settings": "隐藏远程打印设置",
    "Hide system tray icon": "隐藏系统托盘图标",
    "Allow Direct3D rendering": "允许使用 Direct3D 渲染",
    "Allow hostname as ID": "允许使用主机名作为 ID",
    "Allow pure numeric one-time password": "允许使用纯数字一次性密码",
    "Enable adaptive bitrate": "启用自适应比特率",
    "View-only mode": "仅查看模式",

    # 其他设置
    "Remove wallpaper during incoming sessions": "远程会话期间移除桌面壁纸",
    "Click here for a list of Default/Override settings": "点击此处查看可配置的高级选项列表",
    "Default settings": "默认设置（用户可修改）",
    "Override settings": "覆盖设置（用户不可修改）",

    # 按钮
    "Generate Custom Client": "牛逼，开始制造",
    "Source Code on Github": "源代码（Github）",
    "Donate": "赞助作者",
}

def translate_html(input_file, output_file):
    """汉化 HTML 文件"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 执行替换
    for en, zh in translations.items():
        # 使用正则表达式进行替换，保持 HTML 结构
        pattern = re.compile(re.escape(en), re.IGNORECASE)
        content = pattern.sub(zh, content)

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ 汉化完成！")
    print(f"📁 输入文件: {input_file}")
    print(f"📁 输出文件: {output_file}")
    print(f"🔢 替换了 {len(translations)} 个词条")

if __name__ == '__main__':
    input_file = 'rdgenerator/templates/generator.html'
    output_file = 'rdgenerator/templates/generator.html'
    translate_html(input_file, output_file)
