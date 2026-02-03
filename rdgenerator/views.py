import io
from pathlib import Path
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.files.base import ContentFile
import os
import re
import requests
import base64
import json
import uuid
import pyzipper
from django.conf import settings as _settings
from django.db.models import Q
from .forms import GenerateForm
from .models import GithubRun
from PIL import Image
from urllib.parse import quote

def generator_view(request):
    if request.method == 'POST':
        form = GenerateForm(request.POST, request.FILES)
        if form.is_valid():
            platform = form.cleaned_data['platform']
            version = form.cleaned_data['version']
            ui_mode = form.cleaned_data['ui_mode']
            delayFix = form.cleaned_data['delayFix']
            cycleMonitor = form.cleaned_data['cycleMonitor']
            xOffline = form.cleaned_data['xOffline']
            hidecm = form.cleaned_data['hidecm']
            removeNewVersionNotif = form.cleaned_data['removeNewVersionNotif']
            server = form.cleaned_data['serverIP']
            # 使用 RS_PUB_KEY 作为密钥字段
            key = form.cleaned_data['RS_PUB_KEY']
            apiServer = form.cleaned_data['apiServer']
            urlLink = form.cleaned_data['urlLink']
            downloadLink = form.cleaned_data['downloadLink']
            updateLink = form.cleaned_data['updateLink']
            if not server:
                server = 'rs-ny.rustdesk.com' #default rustdesk server
            if not key:
                key = 'OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=' #default rustdesk key
            if not apiServer:
                apiServer = server+":21114"
            if not urlLink:
                urlLink = "https://rustdesk.com"
            if not downloadLink:
                downloadLink = "https://rustdesk.com/download"
            direction = form.cleaned_data['direction']
            installation = form.cleaned_data['installation']
            settings = form.cleaned_data['settings']
            filename = form.cleaned_data['exename']
            # 根据direction自动设置应用名称
            if direction == 'incoming':
                appname = "小锐云桥(被控端)"
            elif direction == 'outgoing':
                appname = "小锐云桥(工程师端)"
            else:  # both
                appname = "小锐云桥(工程师端)"
            compname = form.cleaned_data['compname']
            if not compname:
                compname = "Beijing Yiyuan Information Technology Co., Ltd."
            androidappid = form.cleaned_data['androidappid']
            if not androidappid:
                androidappid = "com.carriez.flutter_hbb"
            compname = compname.replace("&","\\&")
            permPass = form.cleaned_data['permanentPassword']
            unlockPin = form.cleaned_data['unlockPin']
            theme = form.cleaned_data['theme']
            themeDorO = form.cleaned_data['themeDorO']
            image_quality = form.cleaned_data['image_quality']
            custom_fps = form.cleaned_data['custom_fps']
            #runasadmin = form.cleaned_data['runasadmin']
            passApproveMode = form.cleaned_data['passApproveMode']
            denyLan = form.cleaned_data['denyLan']
            enableDirectIP = form.cleaned_data['enableDirectIP']
            #ipWhitelist = form.cleaned_data['ipWhitelist']
            autoClose = form.cleaned_data['autoClose']

            # Security Settings隐藏选项
            hideSecuritySettings = form.cleaned_data['hideSecuritySettings']
            hideNetworkSettings = form.cleaned_data['hideNetworkSettings']
            hideServerSettings = form.cleaned_data['hideServerSettings']
            hideRemotePrinterSettings = form.cleaned_data['hideRemotePrinterSettings']
            hide_account = form.cleaned_data['hide_account']
            remove_preset_password_warning = form.cleaned_data['remove_preset_password_warning']
            hideProxySettings = form.cleaned_data['hideProxySettings']
            hideWebsocketSettings = form.cleaned_data['hideWebsocketSettings']

            permissionsDorO = form.cleaned_data['permissionsDorO']
            permissionsType = form.cleaned_data['permissionsType']
            enableKeyboard = form.cleaned_data['enableKeyboard']
            enableClipboard = form.cleaned_data['enableClipboard']
            enableFileTransfer = form.cleaned_data['enableFileTransfer']
            enableAudio = form.cleaned_data['enableAudio']
            enableTCP = form.cleaned_data['enableTCP']
            enableRemoteRestart = form.cleaned_data['enableRemoteRestart']
            enableRecording = form.cleaned_data['enableRecording']
            enableBlockingInput = form.cleaned_data['enableBlockingInput']
            enableRemoteModi = form.cleaned_data['enableRemoteModi']
            removeWallpaper = form.cleaned_data['removeWallpaper']
            defaultManual = form.cleaned_data['defaultManual']
            overrideManual = form.cleaned_data['overrideManual']
            enablePrinter = form.cleaned_data['enablePrinter']
            enableCamera = form.cleaned_data['enableCamera']
            enableTerminal = form.cleaned_data['enableTerminal']

            # 主控端功能
            hide_chat_voice = form.cleaned_data['hide_chat_voice']
            viewOnly = form.cleaned_data['viewOnly']
            collapse_toolbar = form.cleaned_data['collapse_toolbar']
            privacy_mode = form.cleaned_data['privacy_mode']
            hide_username_on_card = form.cleaned_data['hide_username_on_card']

            # 被控端功能
            hideTray = form.cleaned_data['hideTray']
            hidePassword = form.cleaned_data['hidePassword']
            hideMenuBar = form.cleaned_data['hideMenuBar']
            hideQuit = form.cleaned_data['hideQuit']
            addcopy = form.cleaned_data['addcopy']
            applyprivacy = form.cleaned_data['applyprivacy']
            passpolicy = form.cleaned_data['passpolicy']
            allowHostnameAsId = form.cleaned_data['allowHostnameAsId']
            hideService_Start_Stop = form.cleaned_data['hideService_Start_Stop']

            # 通用功能
            disable_check_update = form.cleaned_data['disable_check_update']
            no_uninstall = form.cleaned_data['no_uninstall']
            disable_install = form.cleaned_data['disable_install']
            allowD3dRender = form.cleaned_data['allowD3dRender']
            use_texture_render = form.cleaned_data['use_texture_render']
            pre_elevate_service = form.cleaned_data['pre_elevate_service']
            sync_init_clipboard = form.cleaned_data['sync_init_clipboard']
            hide_powered_by_me = form.cleaned_data['hide_powered_by_me']

            if all(char.isascii() for char in filename):
                filename = re.sub(r'[^\w\s-]', '_', filename).strip()
                filename = filename.replace(" ","_")
            else:
                filename = "rustdesk"
            # 注释掉appname的ASCII检查，因为我们现在使用预定义的中文名称
            # if not all(char.isascii() for char in appname):
            #     appname = "rustdesk"
            myuuid = str(uuid.uuid4())
            protocol = _settings.PROTOCOL
            host = request.get_host()
            full_url = f"{protocol}://{host}"
            try:
                iconfile = form.cleaned_data.get('iconfile')
                if not iconfile:
                    iconfile = form.cleaned_data.get('iconbase64')
                iconlink_url, iconlink_uuid, iconlink_file = save_png(iconfile,myuuid,full_url,"icon.png")
            except:
                print("failed to get icon, using default")
                iconlink_url = "false"
                iconlink_uuid = "false"
                iconlink_file = "false"
            try:
                logofile = form.cleaned_data.get('logofile')
                if not logofile:
                    logofile = form.cleaned_data.get('logobase64')
                logolink_url, logolink_uuid, logolink_file = save_png(logofile,myuuid,full_url,"logo.png")
            except:
                print("failed to get logo")
                logolink_url = "false"
                logolink_uuid = "false"
                logolink_file = "false"
            try:
                # 使用 privacy_wallpaper 作为隐私图片
                privacy_wallpaper = form.cleaned_data.get('privacy_wallpaper')
                if not privacy_wallpaper:
                    privacy_wallpaper = form.cleaned_data.get('privacybase64')

                if privacy_wallpaper:
                    # 保存为两个用途：privacy.png (旧组件) 和 privacy_wallpaper.png (新功能)
                    privacylink_url, privacylink_uuid, privacylink_file = save_png(privacy_wallpaper,myuuid,full_url,"privacy.png")
                    privacy_wallpaper_url, privacy_wallpaper_uuid, privacy_wallpaper_file = save_png(privacy_wallpaper,myuuid,full_url,"privacy_wallpaper.png")
                else:
                    privacylink_url = "false"
                    privacylink_uuid = "false"
                    privacylink_file = "false"
                    privacy_wallpaper_url = "false"
                    privacy_wallpaper_uuid = "false"
                    privacy_wallpaper_file = "false"
            except:
                print("failed to get privacy wallpaper")
                privacylink_url = "false"
                privacylink_uuid = "false"
                privacylink_file = "false"
                privacy_wallpaper_url = "false"
                privacy_wallpaper_uuid = "false"
                privacy_wallpaper_file = "false"

            ###create the custom.txt json here and send in as inputs below
            decodedCustom = {}
            if direction != "Both":
                decodedCustom['conn-type'] = direction
                # 当选择"仅被控"时，自动隐藏账户选项卡
                if direction == "incoming":
                    if 'override-settings' not in decodedCustom:
                        decodedCustom['override-settings'] = {}
                    decodedCustom['override-settings']['hide-account'] = 'Y'
            if installation == "installationN":
                decodedCustom['disable-installation'] = 'Y'
            if settings == "settingsN":
                decodedCustom['disable-settings'] = 'Y'
            if appname.upper() != "RUSTDESK" and appname != "":
                decodedCustom['app-name'] = appname
            decodedCustom['override-settings'] = {}
            decodedCustom['default-settings'] = {}
            if permPass != "":
                decodedCustom['password'] = permPass
            if unlockPin != "":
                decodedCustom['unlock-pin'] = unlockPin
            if theme != "system":
                if themeDorO == "default":
                    if platform == "windows-x86":
                        decodedCustom['default-settings']['allow-darktheme'] = 'Y' if theme == "dark" else 'N'
                    else:
                        decodedCustom['default-settings']['theme'] = theme
                elif themeDorO == "override":
                    if platform == "windows-x86":
                        decodedCustom['override-settings']['allow-darktheme'] = 'Y' if theme == "dark" else 'N'
                    else:
                        decodedCustom['override-settings']['theme'] = theme

            # 图像质量和帧率设置
            if image_quality:
                decodedCustom['override-settings']['image_quality'] = image_quality
            if custom_fps and custom_fps != '30':
                decodedCustom['override-settings']['custom-fps'] = custom_fps

            decodedCustom['enable-lan-discovery'] = 'N' if denyLan else 'Y'
            #decodedCustom['direct-server'] = 'Y' if enableDirectIP else 'N'
            decodedCustom['allow-auto-disconnect'] = 'Y' if autoClose else 'N'
            if permissionsDorO == "default":
                decodedCustom['default-settings']['access-mode'] = permissionsType
                decodedCustom['default-settings']['enable-keyboard'] = 'Y' if enableKeyboard else 'N'
                decodedCustom['default-settings']['enable-clipboard'] = 'Y' if enableClipboard else 'N'
                decodedCustom['default-settings']['enable-file-transfer'] = 'Y' if enableFileTransfer else 'N'
                decodedCustom['default-settings']['enable-audio'] = 'Y' if enableAudio else 'N'
                decodedCustom['default-settings']['enable-tunnel'] = 'Y' if enableTCP else 'N'
                decodedCustom['default-settings']['enable-remote-restart'] = 'Y' if enableRemoteRestart else 'N'
                decodedCustom['default-settings']['enable-record-session'] = 'Y' if enableRecording else 'N'
                decodedCustom['default-settings']['enable-block-input'] = 'Y' if enableBlockingInput else 'N'
                decodedCustom['default-settings']['allow-remote-config-modification'] = 'Y' if enableRemoteModi else 'N'
                decodedCustom['default-settings']['direct-server'] = 'Y' if enableDirectIP else 'N'
                decodedCustom['default-settings']['verification-method'] = 'use-permanent-password' if hidecm else 'use-both-passwords'
                decodedCustom['default-settings']['approve-mode'] = passApproveMode
                decodedCustom['default-settings']['allow-hide-cm'] = 'Y' if hidecm else 'N'
                decodedCustom['default-settings']['allow-remove-wallpaper'] = 'Y' if removeWallpaper else 'N'
                decodedCustom['default-settings']['enable-remote-printer'] = 'Y' if enablePrinter else 'N'
                decodedCustom['default-settings']['enable-camera'] = 'Y' if enableCamera else 'N'
                decodedCustom['default-settings']['enable-terminal'] = 'Y' if enableTerminal else 'N'
            else:
                decodedCustom['override-settings']['access-mode'] = permissionsType
                decodedCustom['override-settings']['enable-keyboard'] = 'Y' if enableKeyboard else 'N'
                decodedCustom['override-settings']['enable-clipboard'] = 'Y' if enableClipboard else 'N'
                decodedCustom['override-settings']['enable-file-transfer'] = 'Y' if enableFileTransfer else 'N'
                decodedCustom['override-settings']['enable-audio'] = 'Y' if enableAudio else 'N'
                decodedCustom['override-settings']['enable-tunnel'] = 'Y' if enableTCP else 'N'
                decodedCustom['override-settings']['enable-remote-restart'] = 'Y' if enableRemoteRestart else 'N'
                decodedCustom['override-settings']['enable-record-session'] = 'Y' if enableRecording else 'N'
                decodedCustom['override-settings']['enable-block-input'] = 'Y' if enableBlockingInput else 'N'
                decodedCustom['override-settings']['allow-remote-config-modification'] = 'Y' if enableRemoteModi else 'N'
                decodedCustom['override-settings']['direct-server'] = 'Y' if enableDirectIP else 'N'
                decodedCustom['override-settings']['verification-method'] = 'use-permanent-password' if hidecm else 'use-both-passwords'
                decodedCustom['override-settings']['approve-mode'] = passApproveMode
                decodedCustom['override-settings']['allow-hide-cm'] = 'Y' if hidecm else 'N'
                decodedCustom['override-settings']['allow-remove-wallpaper'] = 'Y' if removeWallpaper else 'N'
                decodedCustom['override-settings']['enable-remote-printer'] = 'Y' if enablePrinter else 'N'
                decodedCustom['override-settings']['enable-camera'] = 'Y' if enableCamera else 'N'
                decodedCustom['override-settings']['enable-terminal'] = 'Y' if enableTerminal else 'N'

            # 安全设置隐藏选项（BUILDIN_SETTINGS）
            if hideSecuritySettings:
                decodedCustom['override-settings']['hide-security-settings'] = 'Y'
            if hideNetworkSettings:
                decodedCustom['override-settings']['hide-network-settings'] = 'Y'
            if hideServerSettings:
                decodedCustom['override-settings']['hide-server-settings'] = 'Y'
            if hideRemotePrinterSettings:
                decodedCustom['override-settings']['hide-remote-printer-settings'] = 'Y'
            if hide_account:
                decodedCustom['override-settings']['hide-account'] = 'Y'
            if remove_preset_password_warning:
                decodedCustom['override-settings']['remove-preset-password-warning'] = 'Y'
            if hideProxySettings:
                decodedCustom['override-settings']['hide-proxy-settings'] = 'Y'
            if hideWebsocketSettings:
                decodedCustom['override-settings']['hide-websocket-settings'] = 'Y'

            # 主控端功能
            if hide_chat_voice:
                decodedCustom['override-settings']['hide-chat-voice'] = 'Y'
            if viewOnly:
                decodedCustom['override-settings']['view-only'] = 'Y'
            if collapse_toolbar:
                decodedCustom['default-settings']['collapse-toolbar'] = 'Y'
            if privacy_mode:
                decodedCustom['default-settings']['privacy-mode'] = 'Y'
            if hide_username_on_card:
                decodedCustom['override-settings']['hide-username-on-card'] = 'Y'

            # 被控端功能
            if hideTray:
                decodedCustom['override-settings']['hide-tray'] = 'Y'
            if hidePassword:
                decodedCustom['override-settings']['hide-password'] = 'Y'
            if hideMenuBar:
                decodedCustom['override-settings']['hide-menu-bar'] = 'Y'
            if hideQuit:
                decodedCustom['override-settings']['hide-quit'] = 'Y'
            if addcopy:
                decodedCustom['override-settings']['add-copy'] = 'Y'
            if applyprivacy:
                decodedCustom['override-settings']['apply-privacy'] = 'Y'
            if passpolicy:
                decodedCustom['override-settings']['allow-simple-password'] = 'Y'
            if allowHostnameAsId:
                decodedCustom['override-settings']['allow-hostname-as-id'] = 'Y'
            if hideService_Start_Stop:
                decodedCustom['override-settings']['hide-service-start-stop'] = 'Y'

            # 通用功能
            if disable_check_update:
                decodedCustom['override-settings']['disable-check-update'] = 'Y'
            if no_uninstall:
                decodedCustom['override-settings']['no-uninstall'] = 'Y'
            if disable_install:
                decodedCustom['override-settings']['disable-install'] = 'Y'
            if allowD3dRender:
                decodedCustom['default-settings']['allow-d3d-render'] = 'Y'
            if use_texture_render:
                decodedCustom['default-settings']['use-texture-render'] = 'Y'
            if pre_elevate_service:
                decodedCustom['override-settings']['pre-elevate-service'] = 'Y'
            if sync_init_clipboard:
                decodedCustom['default-settings']['sync-init-clipboard'] = 'Y'
            if hide_powered_by_me:
                decodedCustom['override-settings']['hide-powered-by-me'] = 'Y'

            for line in defaultManual.splitlines():
                k, value = line.split('=')
                decodedCustom['default-settings'][k.strip()] = value.strip()

            for line in overrideManual.splitlines():
                k, value = line.split('=')
                decodedCustom['override-settings'][k.strip()] = value.strip()
            
            decodedCustomJson = json.dumps(decodedCustom)

            string_bytes = decodedCustomJson.encode("ascii")
            base64_bytes = base64.b64encode(string_bytes)
            encodedCustom = base64_bytes.decode("ascii")

            # #github limits inputs to 10, so lump extras into one with json
            # extras = {}
            # extras['genurl'] = _settings.GENURL
            # #extras['runasadmin'] = runasadmin
            # extras['urlLink'] = urlLink
            # extras['downloadLink'] = downloadLink
            # extras['delayFix'] = 'true' if delayFix else 'false'
            # extras['rdgen'] = 'true'
            # extras['cycleMonitor'] = 'true' if cycleMonitor else 'false'
            # extras['xOffline'] = 'true' if xOffline else 'false'
            # extras['removeNewVersionNotif'] = 'true' if removeNewVersionNotif else 'false'
            # extras['compname'] = compname
            # extras['androidappid'] = androidappid
            # extra_input = json.dumps(extras)

            ####from here run the github action, we need user, repo, access token.
            if platform == 'windows':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-windows.yml/dispatches'
            if platform == 'windows-x86':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-windows-x86.yml/dispatches'
            elif platform == 'linux':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-linux.yml/dispatches'
            elif platform == 'android':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-android.yml/dispatches'
            elif platform == 'macos':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-macos.yml/dispatches'
            else:
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-windows.yml/dispatches'

            #url = 'https://api.github.com/repos/'+_settings.GHUSER+'/rustdesk/actions/workflows/test.yml/dispatches'
            inputs_raw = {
                "server":server,
                "key":key,
                "apiServer":apiServer,
                "custom":encodedCustom,
                "uuid":myuuid,
                "iconlink_url":iconlink_url,
                "iconlink_uuid":iconlink_uuid,
                "iconlink_file":iconlink_file,
                "logolink_url":logolink_url,
                "logolink_uuid":logolink_uuid,
                "logolink_file":logolink_file,
                "privacylink_url":privacylink_url,
                "privacylink_uuid":privacylink_uuid,
                "privacylink_file":privacylink_file,
                "privacy_wallpaper_url":privacy_wallpaper_url,
                "privacy_wallpaper_uuid":privacy_wallpaper_uuid,
                "privacy_wallpaper_file":privacy_wallpaper_file,
                "appname":appname,
                "genurl":_settings.GENURL,
                "urlLink":urlLink,
                "downloadLink":downloadLink,
                "updateLink":updateLink if updateLink else "",
                "delayFix": 'true' if delayFix else 'false',
                "rdgen":'true',
                "cycleMonitor": 'true' if cycleMonitor else 'false',
                "xOffline": 'true' if xOffline else 'false',
                "removeNewVersionNotif": 'true' if removeNewVersionNotif else 'false',
                "compname": compname,
                "androidappid":androidappid,
                "filename":filename,
                "ui_mode": 'true' if ui_mode else 'false',
                "hide_powered_by_me": 'true' if hide_powered_by_me else 'false',
                "direction": direction
            }

            temp_json_path = f"data_{uuid.uuid4()}.json"
            zip_filename = f"secrets_{uuid.uuid4()}.zip"
            zip_path = "temp_zips/%s" % (zip_filename)
            Path("temp_zips").mkdir(parents=True, exist_ok=True)

            with open(temp_json_path, "w") as f:
                json.dump(inputs_raw, f)

            with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
                zf.setpassword(_settings.ZIP_PASSWORD.encode())
                zf.write(temp_json_path, arcname="secrets.json")

            # 4. Cleanup the plain JSON file immediately
            if os.path.exists(temp_json_path):
                os.remove(temp_json_path)

            zipJson = {}
            zipJson['url'] = full_url
            zipJson['file'] = zip_filename

            zip_url = json.dumps(zipJson)

            data = {
                "ref":_settings.GHBRANCH,
                "inputs":{
                    "version":version,
                    "zip_url":zip_url
                }
            } 
            #print(data)
            headers = {
                'Accept':  'application/vnd.github+json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer '+_settings.GHBEARER,
                'X-GitHub-Api-Version': '2022-11-28'
            }
            create_github_run(myuuid)
            response = requests.post(url, json=data, headers=headers)
            print(response)
            if response.status_code == 204 or response.status_code == 200:
                return render(request, 'waiting.html', {'filename':filename, 'uuid':myuuid, 'status':"Starting generator...please wait", 'platform':platform})
            else:
                return JsonResponse({"error": "Something went wrong"})
    else:
        form = GenerateForm()
    #return render(request, 'maintenance.html')
    return render(request, 'generator.html', {'form': form})


def check_for_file(request):
    filename = request.GET['filename']
    uuid = request.GET['uuid']
    platform = request.GET['platform']
    gh_run = GithubRun.objects.filter(Q(uuid=uuid)).first()
    status = gh_run.status

    #if file_exists:
    if status == "Success":
        return render(request, 'generated.html', {'filename': filename, 'uuid':uuid, 'platform':platform})
    else:
        return render(request, 'waiting.html', {'filename':filename, 'uuid':uuid, 'status':status, 'platform':platform})

def download(request):
    filename = request.GET['filename']
    uuid = request.GET['uuid']
    #filename = filename+".exe"
    file_path = os.path.join('exe',uuid,filename)
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, headers={
            'Content-Type': 'application/vnd.microsoft.portable-executable',
            'Content-Disposition': f'attachment; filename="{filename}"'
        })

    return response

def get_png(request):
    filename = request.GET['filename']
    uuid = request.GET['uuid']
    #filename = filename+".exe"
    file_path = os.path.join('png',uuid,filename)
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, headers={
            'Content-Type': 'application/vnd.microsoft.portable-executable',
            'Content-Disposition': f'attachment; filename="{filename}"'
        })

    return response

def create_github_run(myuuid):
    new_github_run = GithubRun(
        uuid=myuuid,
        status="Starting generator...please wait"
    )
    new_github_run.save()

def update_github_run(request):
    data = json.loads(request.body)
    myuuid = data.get('uuid')
    mystatus = data.get('status')
    GithubRun.objects.filter(Q(uuid=myuuid)).update(status=mystatus)
    return HttpResponse('')

def resize_and_encode_icon(imagefile):
    maxWidth = 200
    try:
        with io.BytesIO() as image_buffer:
            for chunk in imagefile.chunks():
                image_buffer.write(chunk)
            image_buffer.seek(0)

            img = Image.open(image_buffer)
            imgcopy = img.copy()
    except (IOError, OSError):
        raise ValueError("Uploaded file is not a valid image format.")

    # Check if resizing is necessary
    if img.size[0] <= maxWidth:
        with io.BytesIO() as image_buffer:
            imgcopy.save(image_buffer, format=imagefile.content_type.split('/')[1])
            image_buffer.seek(0)
            return_image = ContentFile(image_buffer.read(), name=imagefile.name)
        return base64.b64encode(return_image.read())

    # Calculate resized height based on aspect ratio
    wpercent = (maxWidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))

    # Resize the image while maintaining aspect ratio using LANCZOS resampling
    imgcopy = imgcopy.resize((maxWidth, hsize), Image.Resampling.LANCZOS)

    with io.BytesIO() as resized_image_buffer:
        imgcopy.save(resized_image_buffer, format=imagefile.content_type.split('/')[1])
        resized_image_buffer.seek(0)

        resized_imagefile = ContentFile(resized_image_buffer.read(), name=imagefile.name)

    # Return the Base64 encoded representation of the resized image
    resized64 = base64.b64encode(resized_imagefile.read())
    #print(resized64)
    return resized64
 
#the following is used when accessed from an external source, like the rustdesk api server
def startgh(request):
    #print(request)
    data_ = json.loads(request.body)
    ####from here run the github action, we need user, repo, access token.
    url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-'+data_.get('platform')+'.yml/dispatches'  
    data = {
        "ref": _settings.GHBRANCH,
        "inputs":{
            "server":data_.get('server'),
            "key":data_.get('key'),
            "apiServer":data_.get('apiServer'),
            "custom":data_.get('custom'),
            "uuid":data_.get('uuid'),
            "iconlink":data_.get('iconlink'),
            "logolink":data_.get('logolink'),
            "appname":data_.get('appname'),
            "extras":data_.get('extras'),
            "filename":data_.get('filename')
        }
    } 
    headers = {
        'Accept':  'application/vnd.github+json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+_settings.GHBEARER,
        'X-GitHub-Api-Version': '2022-11-28'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response)
    return HttpResponse(status=204)

def save_png(file, uuid, domain, name):
    file_save_path = "png/%s/%s" % (uuid, name)
    Path("png/%s" % uuid).mkdir(parents=True, exist_ok=True)

    if isinstance(file, str):  # Check if it's a base64 string
        try:
            header, encoded = file.split(';base64,')
            decoded_img = base64.b64decode(encoded)
            file = ContentFile(decoded_img, name=name) # Create a file-like object
        except ValueError:
            print("Invalid base64 data")
            return None  # Or handle the error as you see fit
        except Exception as e:  # Catch general exceptions during decoding
            print(f"Error decoding base64: {e}")
            return None
        
    with open(file_save_path, "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)
    # imageJson = {}
    # imageJson['url'] = domain
    # imageJson['uuid'] = uuid
    # imageJson['file'] = name
    #return "%s/%s" % (domain, file_save_path)
    return domain, uuid, name

def save_custom_client(request):
    file = request.FILES['file']
    myuuid = request.POST.get('uuid')
    file_save_path = "exe/%s/%s" % (myuuid, file.name)
    Path("exe/%s" % myuuid).mkdir(parents=True, exist_ok=True)
    with open(file_save_path, "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)

    return HttpResponse("File saved successfully!")

def cleanup_secrets(request):
    # Pass the UUID as a query param or in JSON body
    data = json.loads(request.body)
    my_uuid = data.get('uuid')
    
    if not my_uuid:
        return HttpResponse("Missing UUID", status=400)

    # 1. Find the files in your temp directory matching the UUID
    temp_dir = os.path.join('temp_zips')
    
    # We look for any file starting with 'secrets_' and containing the uuid
    for filename in os.listdir(temp_dir):
        if my_uuid in filename and filename.endswith('.zip'):
            file_path = os.path.join(temp_dir, filename)
            try:
                os.remove(file_path)
                print(f"Successfully deleted {file_path}")
            except OSError as e:
                print(f"Error deleting file: {e}")

    return HttpResponse("Cleanup successful", status=200)

def get_zip(request):
    filename = request.GET['filename']
    #filename = filename+".exe"
    file_path = os.path.join('temp_zips',filename)
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, headers={
            'Content-Type': 'application/vnd.microsoft.portable-executable',
            'Content-Disposition': f'attachment; filename="{filename}"'
        })

    return response
