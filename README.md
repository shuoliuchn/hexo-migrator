# Hexo Migrator 博客迁移工具

个人博客：https://sliu.vip

[开发文档](docs\开发文档.md) 

我的博客就是用这个工具，使用 Typera 写完之后，迁移成为 Hexo 友好型的博客。可以自动生成 Front Matter 头部，自动转换图片和站内链接。

## 项目背景

一直在用 Typeroa 写博客，写完之后想通过 Typery 发送图片。可每次都会







## 配置部署

### 项目下载

```bash
git clone https://gitee.com/shuoliuchn/hexo-migrator.git
```

### 安装依赖

开发使用 Python 版本：Python 3.6.8

有用到 f-strings，依赖 Python 3.6 以上版本。

如果需要，可以在虚拟环境中配置，就不多说了。

进入到**项目根目录**，运行命令安装依赖：

```bash
pip3 install -r requirements.txt
```

### 创建数据库

进入到 MySQL 数据库中，运行命令创建数据库：

```mysql
create database hexo default charset=utf8
```

### 数据库迁移

在此之前，需要修改项目设置中的 settings.py 文件数据库相关配置。找到下面的代码，修改成恰当的设置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',    # 使用 MySQL 数据库
        'NAME': 'hexo',    # 数据库名
        'HOST': '127.0.0.1',    # 数据库 IP
        'PORT': 3306,    # 数据库端口
        'USER': 'root',   # 登录数据库使用的用户名
        'PASSWORD': '123'    # 登录数据库使用的密码
    }
}
```

在项目根目录运行命令，迁移数据库：

```python
python3 manage.py makemigrations
python3 manage.py migrate
```

### 账号注册

没有写账号注册的功能，使用的是 django 自带的 admin 框架。创建账号通过命令：

```bash
python manage.py createsuperuser
```

有超级用户后，使用 admin 也可以实现用户的增加。

### 项目启动

在项目根路径普通启动 Django 项目的命令即可：

```python
python manage.py runserver    # 也可以指定 IP 端口，默认为 127.0.0.1:8000
```

## 基本使用

### 用户登录

浏览器访问 http://127.0.0.1:8000/login/ 进入登陆页面，使用刚刚注册好的账号即可登录。

### 分类和标签

在 settings.py 中，找到 CATEGORY_DICT 配置，键为最外层文件夹的内容，值为设置的对应的分类名。比如我写好的：

```python
# 外层文件夹和分类对应字典，批量导入分类时会用到
CATEGORY_DICT = {
    '': '首页',
    'bug-bible': 'Bug 宝典',
    'database': '数据库',
    'linux': 'Linux',
    'notes': '学习实践笔记',
    'python-advanced': 'Python 进阶',
    'python-basic': 'Python 基础',
    'raspberry-pi': '树莓派',
    'testing': '测试',
    'translation': '官方文档翻译',
    'web': 'Web',
    'django': 'Django',
    'project': '综合项目',
    'git': 'Git',
    'hexo': 'Hexo',
}
```

在 `settings.py` 中配置好以后，点击 `博客操作` 下的 `批量导入分类`，即可将设置中的分类信息导入到数据库中：

![1584075954118](README.assets/1584075954118.png)

点击 `查看分类和标签`，即可对分类和标签进行管理：

![1584076237107](README.assets/1584076237107.png)

### 博客管理

#### 已有博客批量导入

将已经生成了的 Hexo 博客导入到数据库中。若是第一次使用 Hexo，未生成过 Hexo 博客，没有将其导入数据库的需求，可忽略此功能。

需要注意的是，导入的博客信息将会覆盖数据库中已有的信息。

点击 `博客操作` 下的 `从现有博客导入`：

![1584076535746](README.assets/1584076535746.png)

输入原博客位置和目标博客位置，点击 `批量导入` 即可：

![1584076681455](README.assets/1584076681455.png)

原博客路径默认为 settings.py 中的 DEFAULT_OLD_DIR，目标路径默认为 settings.py 中的 BLOG_GEN_DIR。可以把这两个文件夹修改成你需要的，从而减少操作量：

```python
BLOG_GEN_DIR = r'/tmp/hexo/source/_posts'    # 生成的博客路径
DEFAULT_OLD_DIR = r'/data/blog'    # 要导入的旧的已经生成好的博客路径
```

#### 博客原文导入

使用 Typera 新写好的博客文件，有些地方并不符合 Hexo 格式要求。使用原文导入，会将这些不符合要求的语句转换为更规范的格式。这样，使用 Hexo 生成静态文件的时候才不会报错。

点击 `博客操作` 下的 `导入新写好的博客原文件`：

![1584077232664](README.assets/1584077232664.png)

在 `原博客路径` 中输入博客原文件的最外层目录，在 `目标路径` 中输入要导出到的路径，点击 `批量导入` 即可：

![1584077369778](README.assets/1584077369778.png)

`原博客路径` 默认为 `settings.py` 中的 BLOG_BASE_DIR，`目标路径` 默认为 `settings.py` 中的 BLOG_GEN_DIR。可以通过修改这两个配置，减少后续操作步骤：

```python
BLOG_BASE_DIR = r'/data/PyProject/神器/技术查阅手册'    # 博客原文根路径
BLOG_GEN_DIR = r'/tmp/hexo/source/_posts'    # 生成的博客路径
```

#### 批量生成 Hexo 博客文件

将数据库中的内容导出为 Hexo 友好型的 md 博客文件，即：Front Matter 中写明了博客的各种信息，内容中的静态文件和链接都是按照规则书写，特殊含义的花括号被转义，等等。

点击 `批量生成 Hexo 博客文件`：

![1584081717758](README.assets/1584081717758.png)

点击 `批量生成`，即可将数据库中的博客内容导出成为 Hexo 友好型的 md 博客文件：

![1584082575897](README.assets/1584082575897.png)

同样地，默认的目标路径是 `settings.py` 中的 BLOG_GEN_DIR，可以通过配置 `setting.py` 中对应的内容，简化日后的操作：

```python
BLOG_GEN_DIR = r'/tmp/hexo/source/_posts'    # 生成的博客路径
```

#### 一键操作

一键操作就是按照 `settings.py` 中的路径，一键实现 `博客原文导入` 和 `批量生成 Hexo 博客文件` 两个功能。在首页点击 `一键操作` 即可实现：



特别强调，一定要把 settings.py 中的相关配置修改为你自己博客的配置。





![1584078958791](README.assets/1584078958791.png)