# Snipe-IT 部署指南 (中文版)

本指南将引导你使用项目内置的一键部署脚本，在 Windows 环境下快速、轻松地部署 Snipe-IT。

## 1. 先决条件

在开始之前，请确保你的系统已安装以下软件：

- **Git:** 用于克隆项目代码仓库。你可以从 [git-scm.com](https://git-scm.com/) 下载。
- **Docker Desktop:** 用于构建和管理应用容器。请从 [docker.com](https://www.docker.com/products/docker-desktop/) 下载并安装。

**重要提示:**
- 安装完成后，请确保 Docker Desktop **正在运行**，并已切换到 **Linux 容器模式** (这是默认设置)。
- 建议为 Docker 分配足够的系统资源 (例如，4GB 以上的内存) 以获得更好的性能。

## 2. 一键部署步骤

### 第 1 步：克隆你的仓库

首先，使用 Git 克隆你自己的 Snipe-IT fork 仓库到本地。打开命令行工具 (CMD 或 PowerShell)，并执行以下命令：

```bash
git clone https://github.com/unkaku-1/snipe-it.git
```
(请将上面的 URL 替换为你自己的仓库地址)

然后，进入项目目录：
```bash
cd snipe-it
```

### 第 2 步：运行一键部署脚本

在 `snipe-it` 目录下，直接运行我们为你准备的批处理脚本：

```bash
deploy_snipeit.bat
```

这个脚本会自动完成以下所有工作：
1.  **环境检查:** 确认 Git 和 Docker 是否可用。
2.  **创建 `.env` 文件:** 自动生成一个适用于本地 Docker 环境的配置文件。
3.  **构建并启动服务:** 使用 `docker-compose` 和我们定制的 `Dockerfile.custom` 来构建应用镜像 (这个过程会比较长，请耐心等待)，并启动应用、Web 服务器和数据库。
4.  **清理缓存:** 自动执行 `php artisan config:clear`，确保所有配置正确加载。

### 第 3 步：访问并完成安装

当脚本执行完毕并显示 "部署成功!" 后，打开你的浏览器并访问：

[http://localhost:8000](http://localhost:8000)

你应该会看到 Snipe-IT 的 **"Pre-Flight Check"** (飞行前检查) 页面。这是最后的安装步骤。

1.  点击页面上的 **"Next: Create Database Tables"** (下一步：创建数据库表) 按钮。
2.  等待数据库表创建完成。
3.  接下来，你会看到 **"Create User"** (创建用户) 页面。在这里填写你的管理员账户信息。
4.  完成！现在你可以使用刚刚创建的账户登录到全新的、经过美化的 Snipe-IT 系统了。

## 3. 日常使用

- **启动服务:** `docker-compose up -d`
- **停止服务:** `docker-compose down`

部署完成！享受你的现代化 IT 资产管理系统吧。
