import os
from django.conf import settings


# TEST_DIR = r'C:\Users\Sure\PyProject\神器\技术查阅手册'
# TARGET_TEST_DIR = r'C:\Users\Sure\PyProject\神器\技术查阅手册2'

TEST_DIR = os.path.join(settings.BASE_DIR, 'main_logic', 'test')
TARGET_TEST_DIR = os.path.join(settings.BASE_DIR, 'main_logic', 'test2')

CODE_BLOCK_RE = '```.+?\n```\n'    # 匹配时需要设置 DOTALL
INLINE_CODE_BLOCK_RE = '`.+?`'
TITLE_RE = '^\n*#{1,3} .+?\n'
PARAGRAPH_RE = '\n#+ .+?\n'
LINK_RE = '\\[.+?\\]\\(.*?\\.md[\\)#]'

YAML_STR_RE = "---.+?---\n\n"    # 匹配时需要设置 DOTALL

IMG_RE_LIST = [
    {'tag': '!\\[.+?\\]\\(.+?[.]assets.+?\\..+?\\)', 'file_name': '!\\[.+?\\]\\(.+?[.]assets.(.+?\\..+?)\\)'},
    {'tag': '<img src = .+?\\.assets.+?\\..+?>', 'file_name': '<img src = .+?\\.assets.(.+?\\..+?).>'},
]
BRACE_RE_LIST = ['{{.*?}}', '{#.*?#}']
TOC_RE_LIST = [
    '\n[toc]\n',
    '\n[Toc]\n',
    '\n[tOc]\n',
    '\n[toC]\n',
    '\n[TOc]\n',
    '\n[ToC]\n',
    '\n[tOC]\n',
    '\n[TOC]\n',
]

CATEGORY_DICT = {
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

YAML_STR = """---
title: "%s"
date: %s
toc: %s
categories: "%s"
layout: single-column
---

"""

BRACE_LEFT = "{% raw %}"
BRACE_RIGHT = "{% endraw %}"

# 需要忽略的文件或文件夹名
FILE_IGNORE = []

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'log')
MIGRATION_LOG_NAME = 'migration.log'



