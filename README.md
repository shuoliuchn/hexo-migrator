# Hexo Migrator 博客迁移工具

个人博客：https://sliu.vip

我的博客就是用这个工具，使用 Typera 写完之后，迁移成为 Hexo 友好型的博客。可以自动生成 Front Matter 头部，自动转换图片和站内链接。

## 项目背景

一直在用 Typeroa 写博客，写完之后想通过 Typery 发送图片。可每次都会







## 使用方法

### 项目下载

```
git clone 
```



### 安装依赖

开发使用 Python 版本：Python 3.6.8

有用到 f-strings，依赖 Python 3.6 以上版本。

如果需要，可以在虚拟环境中配置，就不多说了。

#### Django 安装

依赖 Django 2.2.0：

```bash
pip install django==2.2.0
```



项目启动：

在项目根路径普通启动 Django 项目的命令即可：

```
python manage.py runserver
```

默认启动在

账号注册：

没有写账号注册的功能，使用的是 django 自带的 admin 框架。创建账号通过命令：

```bash
python manage.py createsuperuser
```

有超级用户后，启动 admin 也可以实现用户的增加。

用户登录