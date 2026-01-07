@echo off
chcp 65001 >nul
cd /d C:\Users\Administrator\Documents\rdgen\rdgenerator\templates

echo 正在汉化 generator.html...

REM 使用 PowerShell 进行批量替换
powershell -Command "$content = Get-Content 'generator.html' -Raw -Encoding UTF8; $content = $content -replace 'Fix connection delay when using third-party API', '修复使用第三方 API 时的连接延迟'; $content = $content -replace 'To use the hide connection window feature, please set a permanent password\.', '使用隐藏连接窗口功能时，请设置永久密码。'; $content = $content -replace 'Set Permanent Password:', '设置永久密码：'; $content = $content -replace 'The password is used as default, but can be changed by the client', '密码用作默认密码，但客户端可以更改'; $content = $content -replace '<h2><i class=\"fas fa-paint-brush\"></i> Visual</h2>', '<h2><i class=\"fas fa-paint-brush\"></i> 视觉定制</h2>'; $content = $content -replace '<h2><i class=\"fas fa-lock\"></i> Permissions</h2>', '<h2><i class=\"fas fa-lock\"></i> 权限控制</h2>'; $content = $content -replace '<h2><i class=\"fas fa-cog\"></i> Other</h2>', '<h2><i class=\"fas fa-cog\"></i> 其他设置</h2>'; $content = $content -replace 'Permission type:', '权限预设：'; $content = $content -replace 'Custom', '自定义'; $content = $content -replace 'Full Access', '完全访问'; $content = $content -replace 'Screen share', '仅查看屏幕'; $content = $content -replace 'Remove wallpaper during incoming sessions', '远程会话期间移除桌面壁纸'; $content = $content -replace 'Click here for a list of Default/Override settings', '点击此处查看可配置的高级选项列表'; $content = $content -replace 'Default settings', '默认设置（用户可修改）'; $content = $content -replace 'Override settings', '覆盖设置（用户不可修改）'; $content = $content -replace 'Generate Custom Client', '牛逼，开始制造'; $content = $content -replace 'Source Code on Github', '源代码（Github）'; $content = $content -replace 'Donate', '赞助作者'; Set-Content 'generator.html' $content -Encoding UTF8"

echo 汉化完成！
pause
