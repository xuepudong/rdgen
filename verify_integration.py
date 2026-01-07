#!/usr/bin/env python3
"""
验证附加功能集成的完整性
检查 forms.py、views.py 和 generator.html 之间的字段一致性
"""

import re
import sys

# 定义所有附加功能字段
ADDITIONAL_FEATURES = [
    'cycleMonitor',
    'xOffline',
    'removeNewVersionNotif',
    'hidePassword',
    'hideMenuBar',
    'removeTopNotice',
    'hideQuit',
    'addcopy',
    'applyprivacy',
    'hide_chat_voice',
    'supercm',
    'passpolicy',
    'no_uninstall',
    'disable_install',
    'hideSecuritySettings',
    'hideNetworkSettings',
    'hideServerSettings',
    'hideRemotePrinterSettings',
    'hideTray',
    'allowD3dRender',
    'allowHostnameAsId',
    'allowNumericOneTimePassword',
    'enableAbr',
    'viewOnly',
]

def check_forms_py():
    """检查 forms.py 中是否定义了所有字段"""
    print("🔍 检查 forms.py...")
    with open('rdgenerator/forms.py', 'r', encoding='utf-8') as f:
        content = f.read()

    missing = []
    for field in ADDITIONAL_FEATURES:
        pattern = f"{field} = forms\\.BooleanField"
        if not re.search(pattern, content):
            missing.append(field)

    if missing:
        print(f"   ❌ 缺失字段: {', '.join(missing)}")
        return False
    else:
        print(f"   ✅ 所有 {len(ADDITIONAL_FEATURES)} 个字段已定义")
        return True

def check_views_py():
    """检查 views.py 中是否提取和处理了所有字段"""
    print("\n🔍 检查 views.py...")
    with open('rdgenerator/views.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查字段提取
    missing_extract = []
    for field in ADDITIONAL_FEATURES:
        pattern = f"{field} = form\\.cleaned_data\\['{field}'\\]"
        if not re.search(pattern, content):
            missing_extract.append(field)

    # 检查 extras 字典
    missing_extras = []
    for field in ADDITIONAL_FEATURES:
        pattern = f"extras\\['{field}'\\]"
        if not re.search(pattern, content):
            missing_extras.append(field)

    success = True
    if missing_extract:
        print(f"   ❌ 未提取字段: {', '.join(missing_extract)}")
        success = False
    else:
        print(f"   ✅ 所有字段已提取")

    if missing_extras:
        print(f"   ❌ 未添加到 extras: {', '.join(missing_extras)}")
        success = False
    else:
        print(f"   ✅ 所有字段已添加到 extras")

    return success

def check_generator_html():
    """检查 generator.html 中是否包含了所有字段"""
    print("\n🔍 检查 generator.html...")
    with open('rdgenerator/templates/generator.html', 'r', encoding='utf-8') as f:
        content = f.read()

    missing = []
    for field in ADDITIONAL_FEATURES:
        pattern = f"form\\.{field}"
        if not re.search(pattern, content):
            missing.append(field)

    if missing:
        print(f"   ❌ 缺失表单字段: {', '.join(missing)}")
        return False
    else:
        print(f"   ✅ 所有 {len(ADDITIONAL_FEATURES)} 个字段已添加到模板")
        return True

def main():
    """主验证函数"""
    print("="*60)
    print("附加功能集成验证")
    print("="*60)

    results = {
        'forms.py': check_forms_py(),
        'views.py': check_views_py(),
        'generator.html': check_generator_html(),
    }

    print("\n" + "="*60)
    print("验证结果总结")
    print("="*60)

    all_passed = all(results.values())

    for component, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{component:20s} {status}")

    print("="*60)

    if all_passed:
        print("\n🎉 所有检查通过！附加功能已完整集成。")
        print(f"📊 共集成 {len(ADDITIONAL_FEATURES)} 个附加功能")
        return 0
    else:
        print("\n⚠️  发现问题，请检查上述错误信息。")
        return 1

if __name__ == '__main__':
    sys.exit(main())
