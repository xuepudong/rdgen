from django import forms
from PIL import Image

class GenerateForm(forms.Form):
    #Platform
    platform = forms.ChoiceField(choices=[('windows','Windows 64位'),('windows-x86','Windows 32位'),('linux','Linux'),('android','Android'),('macos-x86','macOS x86 (Intel)'),('macos-aarch64','macOS ARM64 (Apple Silicon)')], initial='windows')
    version = forms.ChoiceField(choices=[('master','开发版（每夜构建）'),('1.4.4','1.4.4'),('1.4.3','1.4.3'),('1.4.2','1.4.2'),('1.4.1','1.4.1'),('1.4.0','1.4.0'),('1.3.9','1.3.9'),('1.3.8','1.3.8'),('1.3.7','1.3.7'),('1.3.6','1.3.6'),('1.3.5','1.3.5'),('1.3.4','1.3.4'),('1.3.3','1.3.3')], initial='1.4.4')
    help_text="'master' 是开发版本（每夜构建），具有最新功能但可能不太稳定"
    delayFix = forms.BooleanField(initial=True, required=False)

    #General
    exename = forms.CharField(label="EXE 文件名", required=True)
    appname = forms.CharField(label="自定义应用名称", required=False)
    direction = forms.ChoiceField(widget=forms.RadioSelect, choices=[
        ('incoming', '仅被控端（仅接受连接）'),
        ('outgoing', '仅控制端（仅发起连接）'),
        ('both', '双向（可接受和发起连接）')
    ], initial='both')
    installation = forms.ChoiceField(label="禁用安装", choices=[
        ('installationY', '否，允许安装'),
        ('installationN', '是，禁止安装')
    ], initial='installationY')
    settings = forms.ChoiceField(label="禁用设置", choices=[
        ('settingsY', '否，允许设置'),
        ('settingsN', '是，禁止设置')
    ], initial='settingsY')
    androidappid = forms.CharField(label="自定义 Android 应用 ID（替换 'com.carriez.flutter_hbb'）", required=False)

    #Custom Server
    serverIP = forms.CharField(label="服务器地址", required=False)
    apiServer = forms.CharField(label="API 服务器", required=False)
    key = forms.CharField(label="密钥", required=False)
    urlLink = forms.CharField(label="自定义网站链接", required=False)
    downloadLink = forms.CharField(label="自定义下载链接", required=False)
    compname = forms.CharField(label="公司名称",required=False)

    #Visual
    iconfile = forms.FileField(label="自定义应用图标（PNG 格式）", required=False, widget=forms.FileInput(attrs={'accept': 'image/png'}))
    logofile = forms.FileField(label="自定义品牌标识（PNG 格式）", required=False, widget=forms.FileInput(attrs={'accept': 'image/png'}))
    iconbase64 = forms.CharField(required=False)
    logobase64 = forms.CharField(required=False)
    theme = forms.ChoiceField(choices=[
        ('light', '浅色主题'),
        ('dark', '深色主题'),
        ('system', '跟随系统')
    ], initial='system')
    themeDorO = forms.ChoiceField(choices=[('default', '默认设置'),('override', '强制覆盖')], initial='default')

    #Security
    passApproveMode = forms.ChoiceField(choices=[('password','通过密码接受会话'),('click','通过点击接受会话'),('password-click','两者皆可')],initial='password-click')
    permanentPassword = forms.CharField(widget=forms.PasswordInput(), required=False)
    #runasadmin = forms.ChoiceField(choices=[('false','No'),('true','Yes')], initial='false')
    denyLan = forms.BooleanField(initial=False, required=False)
    enableDirectIP = forms.BooleanField(initial=False, required=False)
    #ipWhitelist = forms.BooleanField(initial=False, required=False)
    autoClose = forms.BooleanField(initial=False, required=False)

    #Permissions
    permissionsDorO = forms.ChoiceField(choices=[('default', '默认设置'),('override', '强制覆盖')], initial='default')
    permissionsType = forms.ChoiceField(choices=[('custom', '自定义'),('full', '完全访问'),('view','仅查看屏幕')], initial='custom')
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
    hidePassword = forms.BooleanField(initial=False, required=False)
    hideMenuBar = forms.BooleanField(initial=True, required=False)
    removeTopNotice = forms.BooleanField(initial=True, required=False)
    hideQuit = forms.BooleanField(initial=False, required=False)
    addcopy = forms.BooleanField(initial=True, required=False)
    applyprivacy = forms.BooleanField(initial=True, required=False)
    hide_chat_voice = forms.BooleanField(initial=False, required=False)
    supercm = forms.BooleanField(initial=False, required=False)
    passpolicy = forms.BooleanField(initial=False, required=False)
    no_uninstall = forms.BooleanField(initial=True, required=False)
    disable_install = forms.BooleanField(initial=True, required=False)
    hideSecuritySettings = forms.BooleanField(initial=False, required=False)
    hideNetworkSettings = forms.BooleanField(initial=False, required=False)
    hideServerSettings = forms.BooleanField(initial=False, required=False)
    hideRemotePrinterSettings = forms.BooleanField(initial=False, required=False)
    hideTray = forms.BooleanField(initial=False, required=False)
    allowD3dRender = forms.BooleanField(initial=True, required=False)
    allowHostnameAsId = forms.BooleanField(initial=False, required=False)
    allowNumericOneTimePassword = forms.BooleanField(initial=True, required=False)
    enableAbr = forms.BooleanField(initial=True, required=False)
    viewOnly = forms.BooleanField(initial=False, required=False)

    def clean_iconfile(self):
        print("checking icon")
        image = self.cleaned_data['iconfile']
        if image:
            try:
                # Open the image using Pillow
                img = Image.open(image)

                # Check if the image is a PNG (optional, but good practice)
                if img.format != 'PNG':
                    raise forms.ValidationError("Only PNG images are allowed.")

                # Get image dimensions
                width, height = img.size

                # Check for square dimensions
                if width != height:
                    raise forms.ValidationError("Custom App Icon dimensions must be square.")
                
                return image
            except OSError:  # Handle cases where the uploaded file is not a valid image
                raise forms.ValidationError("Invalid icon file.")
            except Exception as e: # Catch any other image processing errors
                raise forms.ValidationError(f"Error processing icon: {e}")
