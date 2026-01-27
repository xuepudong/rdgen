from django import forms
from PIL import Image

class GenerateForm(forms.Form):
    #Platform
    platform = forms.ChoiceField(choices=[('windows','Windows 64Bit'),('windows-x86','Windows 32Bit'),('linux','Linux'),('android','Android'),('macos','macOS')], initial='windows')
    version = forms.ChoiceField(choices=[('master','nightly'),('1.4.5','1.4.5'),('1.4.4','1.4.4'),('1.4.3','1.4.3'),('1.4.2','1.4.2'),('1.4.1','1.4.1'),('1.4.0','1.4.0'),('1.3.9','1.3.9'),('1.3.8','1.3.8'),('1.3.7','1.3.7'),('1.3.6','1.3.6'),('1.3.5','1.3.5'),('1.3.4','1.3.4'),('1.3.3','1.3.3')], initial='1.4.5')
    help_text="'master' is the development version (nightly build) with the latest features but may be less stable"
    ui_mode = forms.BooleanField(initial=True, required=False)
    delayFix = forms.BooleanField(initial=True, required=False)

    #General
    exename = forms.CharField(label="配置名称", required=True)
    appname = forms.CharField(label="应用名称", required=False)
    direction = forms.ChoiceField(widget=forms.RadioSelect, choices=[
        ('incoming', '仅被控'),
        ('outgoing', '仅主控'),
        ('both', '双向控制')
    ], initial='both')
    installation = forms.ChoiceField(label="安装行为", choices=[
        ('installationY', '否，启用安装'),
        ('installationN', '是，禁用安装')
    ], initial='installationY')
    settings = forms.ChoiceField(label="设置权限", choices=[
        ('settingsY', '否，启用设置'),
        ('settingsN', '是，禁用设置')
    ], initial='settingsY')
    androidappid = forms.CharField(label="安卓客户端标识符（默认'com.carriez.flutter_hbb'）", required=False)

    #Custom Server
    serverIP = forms.CharField(label="服务器地址", required=False)
    apiServer = forms.CharField(label="API 地址", required=False)
    RS_PUB_KEY = forms.CharField(label="密钥（公钥）", required=False)
    urlLink = forms.CharField(label="门户网站", required=False)
    downloadLink = forms.CharField(label="更新下载链接", required=False)
    updateLink = forms.CharField(label="在线更新链接", required=False)
    compname = forms.CharField(label="公司名称",required=False)

    #Visual
    iconfile = forms.FileField(label="应用图标（PNG 格式）", required=False, widget=forms.FileInput(attrs={'accept': 'image/png'}))
    logofile = forms.FileField(label="品牌标识（PNG 格式）", required=False, widget=forms.FileInput(attrs={'accept': 'image/png'}))
    privacy_wallpaper = forms.FileField(label="隐私模式背景图（PNG 格式）", required=False, widget=forms.FileInput(attrs={'accept': 'image/png'}))
    iconbase64 = forms.CharField(required=False)
    logobase64 = forms.CharField(required=False)
    privacybase64 = forms.CharField(required=False)
    theme = forms.ChoiceField(choices=[
        ('light', '浅色主题'),
        ('dark', '深色主题'),
        ('system', '跟随系统')
    ], initial='system')
    themeDorO = forms.ChoiceField(choices=[('default', '默认设置'),('override', '强制覆盖')], initial='default')
    image_quality = forms.ChoiceField(choices=[
        ('best', '最佳'),
        ('balanced', '平衡'),
        ('low', '低'),
        ('custom', '自定义')
    ], initial='balanced', required=False)
    custom_fps = forms.ChoiceField(choices=[
        ('30', '30 FPS'),
        ('60', '60 FPS'),
        ('90', '90 FPS'),
        ('120', '120 FPS')
    ], initial='30', required=False)

    #Security
    passApproveMode = forms.ChoiceField(choices=[('password','通过密码接受会话'),('click','通过点击接受会话'),('password-click','两者均可')],initial='password-click')
    permanentPassword = forms.CharField(label="预设密码", widget=forms.PasswordInput(), required=False)
    unlockPin = forms.CharField(label="配置PIN", widget=forms.PasswordInput(), required=False)
    #runasadmin = forms.ChoiceField(choices=[('false','No'),('true','Yes')], initial='false')
    denyLan = forms.BooleanField(initial=False, required=False)
    enableDirectIP = forms.BooleanField(initial=False, required=False)
    #ipWhitelist = forms.BooleanField(initial=False, required=False)
    autoClose = forms.BooleanField(initial=False, required=False)
    hideSecuritySettings = forms.BooleanField(initial=False, required=False)
    hideNetworkSettings = forms.BooleanField(initial=False, required=False)
    hideServerSettings = forms.BooleanField(initial=False, required=False)
    hideRemotePrinterSettings = forms.BooleanField(initial=False, required=False)
    hide_account = forms.BooleanField(initial=False, required=False)
    remove_preset_password_warning = forms.BooleanField(initial=False, required=False)
    hideProxySettings = forms.BooleanField(initial=False, required=False)
    hideWebsocketSettings = forms.BooleanField(initial=False, required=False)

    #Permissions
    permissionsDorO = forms.ChoiceField(label="权限模式", choices=[('default', '默认设置'),('override', '强制覆盖')], initial='default')
    permissionsType = forms.ChoiceField(label="权限预设", choices=[('custom', '自定义'),('full', '完全访问'),('view','仅共享屏幕')], initial='custom')
    enableKeyboard =  forms.BooleanField(initial=True, required=False)
    enableClipboard = forms.BooleanField(initial=True, required=False)
    enableFileTransfer = forms.BooleanField(initial=True, required=False)
    enableAudio = forms.BooleanField(initial=True, required=False)
    enableTCP = forms.BooleanField(initial=True, required=False)
    enableRemoteRestart = forms.BooleanField(initial=True, required=False)
    enableRecording = forms.BooleanField(initial=True, required=False)
    enableBlockingInput = forms.BooleanField(initial=True, required=False)
    enableRemoteModi = forms.BooleanField(initial=False, required=False)
    hidecm = forms.BooleanField(initial=False, required=False)
    enablePrinter = forms.BooleanField(initial=True, required=False)
    enableCamera = forms.BooleanField(initial=True, required=False)
    enableTerminal = forms.BooleanField(initial=True, required=False)

    #Other
    removeWallpaper = forms.BooleanField(initial=True, required=False)

    defaultManual = forms.CharField(widget=forms.Textarea, required=False)
    overrideManual = forms.CharField(widget=forms.Textarea, required=False)

    #custom added features
    cycleMonitor = forms.BooleanField(initial=False, required=False)
    xOffline = forms.BooleanField(initial=False, required=False)
    removeNewVersionNotif = forms.BooleanField(initial=False, required=False)

    #Controller features (主控端功能)
    hide_chat_voice = forms.BooleanField(initial=False, required=False)
    viewOnly = forms.BooleanField(initial=False, required=False)
    collapse_toolbar = forms.BooleanField(initial=False, required=False)
    privacy_mode = forms.BooleanField(initial=False, required=False)
    hide_username_on_card = forms.BooleanField(initial=False, required=False)

    #Controlled features (被控端功能)
    hideTray = forms.BooleanField(initial=False, required=False)
    hidePassword = forms.BooleanField(initial=False, required=False)
    hideMenuBar = forms.BooleanField(initial=False, required=False)
    hideQuit = forms.BooleanField(initial=False, required=False)
    addcopy = forms.BooleanField(initial=False, required=False)
    applyprivacy = forms.BooleanField(initial=False, required=False)
    passpolicy = forms.BooleanField(initial=False, required=False)
    allowHostnameAsId = forms.BooleanField(initial=False, required=False)
    hideService_Start_Stop = forms.BooleanField(initial=False, required=False)

    #Common features (通用功能)
    disable_check_update = forms.BooleanField(initial=False, required=False)
    no_uninstall = forms.BooleanField(initial=False, required=False)
    disable_install = forms.BooleanField(initial=False, required=False)
    allowD3dRender = forms.BooleanField(initial=False, required=False)
    use_texture_render = forms.BooleanField(initial=False, required=False)
    pre_elevate_service = forms.BooleanField(initial=False, required=False)
    sync_init_clipboard = forms.BooleanField(initial=False, required=False)
    hide_powered_by_me = forms.BooleanField(initial=False, required=False)

    def clean_iconfile(self):
        print("checking icon")
        image = self.cleaned_data['iconfile']
        if image:
            try:
                # Open the image using Pillow
                img = Image.open(image)

                # Check if the image is a PNG (optional, but good practice)
                if img.format != 'PNG':
                    raise forms.ValidationError("只允许 PNG 格式的图片。")

                # Get image dimensions
                width, height = img.size

                # Check for square dimensions
                if width != height:
                    raise forms.ValidationError("应用图标必须是正方形尺寸。")

                return image
            except OSError:  # Handle cases where the uploaded file is not a valid image
                raise forms.ValidationError("无效的图标文件。")
            except Exception as e: # Catch any other image processing errors
                raise forms.ValidationError(f"处理图标时出错：{e}")
