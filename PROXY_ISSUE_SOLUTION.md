# 代理问题解决方案

## 问题描述

如果您看到以下错误：
```
ValueError: check_hostname requires server_hostname
```

这说明您的系统配置了HTTPS代理，导致pip无法正常连接镜像源。

## 解决方案

### 方案1：检查并禁用系统代理（推荐）

#### 步骤1：检查系统代理设置

1. 打开 **设置** → **网络和Internet** → **代理**
2. 查看是否启用了"使用代理服务器"
3. 如果启用了，记下代理地址后**暂时关闭**

#### 步骤2：检查环境变量

打开PowerShell，运行：

```powershell
$env:HTTP_PROXY
$env:HTTPS_PROXY
```

如果有输出，说明设置了代理环境变量。

#### 步骤3：临时清除代理

在PowerShell中执行：

```powershell
$env:HTTP_PROXY=''
$env:HTTPS_PROXY=''
$env:http_proxy=''
$env:https_proxy=''
```

然后重新尝试安装。

### 方案2：配置pip信任镜像源

创建或编辑文件：`C:\Users\你的用户名\pip\pip.ini`

内容：

```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
[install]
trusted-host = pypi.tuna.tsinghua.edu.cn
```

### 方案3：使用pip配置命令

```cmd
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn
```

### 方案4：手动下载whl文件安装

如果以上方法都不行，可以手动下载包：

1. 访问：https://pypi.tuna.tsinghua.edu.cn/simple/django/
2. 下载对应Python版本的whl文件
3. 使用 `pip install 文件名.whl` 安装

## 完整的安装命令（解决代理问题）

### PowerShell版本

```powershell
# 1. 清除代理
$env:HTTP_PROXY=''
$env:HTTPS_PROXY=''
$env:NO_PROXY='*'

# 2. 进入项目目录
cd C:\Users\16094\Desktop\fsdownload\CCD\backend

# 3. 激活虚拟环境（如果已创建）
.\venv\Scripts\Activate.ps1

# 4. 升级pip
python -m pip install --upgrade pip --index-url https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn

# 5. 安装依赖
pip install --no-cache-dir --index-url https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt
```

### CMD版本

```cmd
REM 1. 清除代理
set HTTP_PROXY=
set HTTPS_PROXY=
set NO_PROXY=*

REM 2. 进入项目目录
cd C:\Users\16094\Desktop\fsdownload\CCD\backend

REM 3. 激活虚拟环境
venv\Scripts\activate.bat

REM 4. 升级pip
python -m pip install --upgrade pip --index-url https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn

REM 5. 安装依赖
pip install --no-cache-dir --index-url https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn -r requirements.txt
```

## 测试代理是否清除

```cmd
echo %HTTP_PROXY%
echo %HTTPS_PROXY%
```

应该显示空白或`ECHO is off`。

## 常用镜像源（按推荐顺序）

1. **清华大学**
   ```
   https://pypi.tuna.tsinghua.edu.cn/simple
   ```

2. **阿里云**
   ```
   https://mirrors.aliyun.com/pypi/simple/
   ```

3. **豆瓣**
   ```
   https://pypi.douban.com/simple
   ```

4. **中科大**
   ```
   https://pypi.mirrors.ustc.edu.cn/simple/
   ```

5. **华为云**
   ```
   https://mirrors.huaweicloud.com/repository/pypi/simple
   ```

## 如果您在公司网络环境

如果您在公司网络，可能需要使用公司代理。请咨询IT部门获取正确的代理配置。

配置方法：

```cmd
set HTTP_PROXY=http://proxy.company.com:8080
set HTTPS_PROXY=http://proxy.company.com:8080
pip install --proxy http://proxy.company.com:8080 包名
```

## 验证安装

安装完成后，验证Django是否安装成功：

```cmd
python -c "import django; print(django.get_version())"
```

应该输出：`4.2.7`

## 如果还是无法解决

请尝试以下步骤：

1. **重启电脑**（清除所有环境变量）
2. **使用管理员权限**打开CMD或PowerShell
3. **关闭杀毒软件**（某些杀毒软件会拦截HTTPS连接）
4. **检查防火墙设置**
5. **尝试使用手机热点**（排除网络问题）

## 联系方式

如果以上方法都无法解决，请提供以下信息：

1. 错误的完整截图
2. 运行 `pip -V` 的输出
3. 运行 `python --version` 的输出
4. 是否在公司网络环境
5. 是否使用VPN或代理软件

