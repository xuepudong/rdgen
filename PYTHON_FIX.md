# 🔧 Python 环境修复指南

## 问题诊断

你的 Python 3.14.2 安装似乎不完整，缺少 `pip` 模块。这通常发生在：
- Python 安装时未勾选 "Install pip"
- Python 3.14 版本过新，可能存在兼容性问题

---

## 🚀 快速解决方案（推荐）

### 方案 1: 重新安装 Python（推荐使用 Python 3.11 或 3.12）

1. **下载 Python 3.12**
   - 访问: https://www.python.org/downloads/
   - 下载 Python 3.12.x (稳定版)

2. **安装时务必勾选**:
   ```
   ✅ Add Python to PATH
   ✅ Install pip
   ✅ Install for all users (可选)
   ```

3. **验证安装**:
   ```powershell
   python --version
   pip --version
   ```

4. **安装依赖**:
   ```powershell
   cd C:\Users\Administrator\Documents\rdgen
   pip install -r requirements.txt
   ```

5. **启动服务**:
   ```powershell
   python manage.py runserver 0.0.0.0:9444
   ```

---

### 方案 2: 修复当前 Python 3.14 安装

1. **手动安装 pip**:
   ```powershell
   # 下载 get-pip.py
   curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

   # 运行安装
   py get-pip.py
   ```

2. **验证 pip**:
   ```powershell
   py -m pip --version
   ```

3. **安装依赖**:
   ```powershell
   cd C:\Users\Administrator\Documents\rdgen
   py -m pip install django requests pillow gunicorn
   ```

4. **启动服务**:
   ```powershell
   py manage.py runserver 0.0.0.0:9444
   ```

---

### 方案 3: 使用 Docker（最简单，无需处理 Python 环境）

1. **确保 Docker Desktop 已安装并运行**:
   ```powershell
   docker --version
   docker-compose --version
   ```

2. **配置环境变量**:
   编辑 `docker-compose.yml`，设置以下环境变量：
   ```yaml
   environment:
     - SECRET_KEY=your-random-secret-key-here
     - GHUSER=your-github-username
     - GHBEARER=ghp_your_github_token
     - GENURL=http://your-server-ip:9444
     - PROTOCOL=http
     - REPONAME=rdgen
   ```

3. **启动服务**:
   ```powershell
   cd C:\Users\Administrator\Documents\rdgen
   docker-compose up -d
   ```

4. **查看日志**:
   ```powershell
   docker-compose logs -f
   ```

5. **访问服务**:
   - 浏览器打开: http://localhost:9444

---

## 📋 手动安装依赖（如果上述方案都失败）

如果以上方案都不行，手动逐个安装：

```powershell
py -m pip install django==4.2.7
py -m pip install requests
py -m pip install pillow
py -m pip install gunicorn
```

---

## 🔍 验证安装成功

运行以下命令检查所有依赖是否安装成功：

```powershell
py -c "import django; print(f'Django {django.get_version()} installed')"
py -c "import requests; print(f'Requests {requests.__version__} installed')"
py -c "import PIL; print(f'Pillow {PIL.__version__} installed')"
```

预期输出：
```
Django 4.2.x installed
Requests 2.x.x installed
Pillow 10.x.x installed
```

---

## 🚀 启动服务

安装完成后，启动开发服务器：

```powershell
# 切换到项目目录
cd C:\Users\Administrator\Documents\rdgen

# 运行数据库迁移（首次运行）
py manage.py migrate

# 启动服务器
py manage.py runserver 0.0.0.0:9444
```

**访问**: http://localhost:9444

---

## 🎯 推荐方案总结

| 方案 | 难度 | 时间 | 推荐度 |
|------|------|------|--------|
| **Docker** | ⭐ 简单 | 5 分钟 | ⭐⭐⭐⭐⭐ |
| **重装 Python 3.12** | ⭐⭐ 中等 | 10 分钟 | ⭐⭐⭐⭐ |
| **修复当前安装** | ⭐⭐⭐ 困难 | 15 分钟 | ⭐⭐ |

**最推荐**: 使用 **Docker** 方式，完全避免 Python 环境问题！

---

## 💡 为什么推荐 Docker？

✅ **无需处理 Python 版本问题**
✅ **一键启动，开箱即用**
✅ **环境隔离，不影响系统**
✅ **生产环境推荐方案**
✅ **可以轻松迁移到其他服务器**

---

## 📞 如果还有问题

1. 检查 Python 是否正确添加到 PATH
2. 尝试以管理员权限运行 PowerShell
3. 考虑使用虚拟环境 (venv)
4. 或直接使用 Docker 部署

---

**下一步**: 选择一个方案，完成安装后，系统就可以正常运行了！
