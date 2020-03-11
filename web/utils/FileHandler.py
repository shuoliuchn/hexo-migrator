import os
import re

import yaml
from django.conf import settings

from . import DBHandler
from .. import models


def img_migration(file_detail_list, blog_gen_dir=settings.BLOG_GEN_DIR, assets_suffix=''):
    for file_dict in file_detail_list:
        img_path = file_dict.get('img_path')
        if img_path:
            file_list = os.listdir(img_path)
            for file in file_list:
                file_path = os.path.join(img_path, file)
                file_rel_path = file_dict.get('img_rel_path')
                target_file_path = os.path.join(blog_gen_dir, file_rel_path.replace(assets_suffix, ''), file)
                target_file_dir = os.path.dirname(target_file_path)
                if os.path.isfile(target_file_path):
                    # 如果目标路径有同名文件，默认跳过
                    continue
                elif not os.path.isdir(target_file_dir):
                    os.makedirs(target_file_dir)
                with open(file_path, 'rb') as fh_read, open(target_file_path, 'wb') as fh_write:
                    fh_write.write(fh_read.read())


class OldFileHandlser:
    def __init__(self):
        self.old_title_dict = {}
        self.content = ''

    def parse_yaml(self):
        """
        获取已存在文件的yaml信息，
        同时，去除旧文件头部的yaml
        :return:
        """
        yaml_str = re.match(settings.YAML_STR_RE, self.content, re.DOTALL)
        if yaml_str:
            clean_yaml_str = yaml_str.group().strip().strip('-').strip()
            self.old_title_dict = yaml.load(clean_yaml_str, Loader=yaml.SafeLoader)
            self.content = self.content.replace(yaml_str.group(), '')

    def old_file_db_dump(self, file_detail_list):
        for file in file_detail_list:
            file_full_path = file['file_full_path']
            if not os.path.isfile(file_full_path):
                raise ValueError('%s 文件不存在' % file_full_path)
            with open(file_full_path, 'r', encoding='utf8') as fh:
                self.content = fh.read()
            self.parse_yaml()
            data_dict = dict(**self.old_title_dict, **file, **{'content': self.content})
            DBHandler.old_blog_db_handler(data_dict)


class OriginalFileHandler:
    def link_replace(self, content, file_dict):
        file_path = file_dict.get('file_full_path')
        file_rel_path = file_dict.get('file_rel_path')
        project_path = file_path.replace(file_rel_path, '').rsplit(os.path.sep, 1)[0]
        link_list = re.findall(settings.LINK_RE, content)
        for link in link_list:
            rel_dir = link.strip(')').strip('#').rsplit('(', 1)[-1]
            file_dir = os.path.dirname(file_path)
            abs_dir = os.path.abspath(os.path.join(file_dir, rel_dir))
            url_link = abs_dir.replace(project_path, '').replace(os.path.sep, '/')[:-3]    # 把第一个replace换成相对路径
            new_link = link.replace(rel_dir, url_link)
            content = content.replace(link, new_link)
        return content

    @staticmethod
    def img_replace(re_dict, content):
        img_tag_list = re.findall(re_dict['tag'], content)
        for img_tag in img_tag_list:
            img_name = re.findall(re_dict['file_name'], img_tag)[0]
            # {% asset_img example.jpg This is an example image %}
            new_str = '{% asset_img ' + img_name + ' ' + img_name.split('.')[0] + ' %}'
            content = content.replace(img_tag, new_str)
        return content

    @staticmethod
    def get_safe_brace_str(s):
        return '{% raw %}' + s + '{% endraw %}'

    def brace_replace(self, content: str) -> str:
        """
        替换特殊大括号，将其使用 {% raw %} 和 {% endraw %} 包裹起来
        有一个 bug，{{}} 中间如果什么都没有，会被替换成 {% raw %}{{{% endraw %{% raw %}}}{% endraw %}}
        哪怕中间有一个空格都可以。暂时没找到解决办法。
        :param content:
        :return:
        """
        content_list = self.split_code_block(content, settings.BRACE_RE_LIST_STRANGE, False)
        l = len(content_list)
        for i in range(l):
            content_part = content_list[i]
            if not i % 2:
                if settings.BRACE_RE_STRANGE_LEFT in content_part:
                    content_part = content_part.replace(
                        settings.BRACE_RE_STRANGE_LEFT, self.get_safe_brace_str(settings.BRACE_RE_STRANGE_LEFT)
                    )
                elif settings.BRACE_RE_STRANGE_RIGHT in content_part:
                    content_part = content_part.replace(
                        settings.BRACE_RE_STRANGE_RIGHT, self.get_safe_brace_str(settings.BRACE_RE_STRANGE_RIGHT)
                    )
                for brace_re in settings.BRACE_RE_LIST_NORMAL:
                    content_part = content_part.replace(brace_re, self.get_safe_brace_str(brace_re))
                content_part = content_part[1: -1]
            else:
                content_part = self.get_safe_brace_str(content_part)
            content_list[i] = content_part
        content = ''.join(content_list)
        return content

    @staticmethod
    def split_code_block(content: str, code_block_re=settings.CODE_BLOCK_RE, dotall=True) -> list:
        """
        以代码段为基准，拆分 content
        偶数索引为普通文本内容，
        奇数索引为代码块内容，不需替换
        :param content: 去除掉标题的全文文本内容
        :param code_block_re: 代码块正则规则
        :param dotall: 是否跨行匹配
        :return: 拆分好的文本列表
        """
        content_list = []
        params = [code_block_re, content] + ([re.DOTALL] if dotall else [])
        block_list = re.findall(*params)
        for block in block_list:
            content_before, content = content.split(block, 1)
            content_list.append(f'\n{content_before}\n')
            content_list.append(block)
        content_list.append(f'\n{content}\n')
        return content_list

    @staticmethod
    def toc_replace(content: str) -> str:
        """
        用于替换普通文本中的形如 \n[TOC]\n 的结构
        :param content: 传入需要替换的文本字符串
        :return: 替换好的内容列表
        """
        for toc_re in settings.TOC_RE_LIST:
            content = content.replace(toc_re, '\n')
        return content

    @staticmethod
    def content_title_handler(file_full_path: str, file_title: str) -> tuple:
        """
        打开文件，获取标题和文本内容，返回值为元组
        :param file_full_path: 文件的绝对路径
        :param file_title: 文件名，不要 .md 后缀
        :return: tuple (content, title)
        """
        with open(file_full_path, 'r', encoding='utf8') as fh:
            content = fh.read().strip()
        title_raw = re.match(settings.TITLE_RE, content)
        if title_raw:
            title = title_raw.group().strip().lstrip('#').lstrip()
            # content 前后都加上 \n 是为了正则匹配方便，否则在使用 \n[TOC]\n 之类的正则时还要考虑匹配开头和结尾的情况
            content = f"\n{content.replace(title_raw.group(), '').strip()}\n"
        else:
            title = file_title
        return content, title

    def single_import_original(self, file_dict: dict) -> None:
        """
        导入单个文件到数据库中
        :param file_dict: 文件信息字典
        :return: 不需要返回
        """
        print(file_dict.get('wrapper_folder'))
        try:
            categories = models.CategoriesModel.objects.get(
                wrapper_folder=file_dict.get('wrapper_folder'))
        except models.CategoriesModel.DoesNotExist:
            categories = None
        file_data_dict = {
            'path': file_dict.get('file_rel_path'),
            'categories': categories,
            'is_top': not file_dict.get('wrapper_folder'),
        }
        content, file_data_dict['title'] = self.content_title_handler(
            file_dict['file_full_path'], file_dict['file_title'])

        # 以下内容替换都只替换普通文本，代码块中的内容不会影响
        content_list = self.split_code_block(content)
        l = len(content_list)
        for i in range(0, l, 2):
            content_part = content_list[i]
            # 替换 toc
            content_part = self.toc_replace(content_part)
            # 判断 is_toc 是否为 True
            if re.search(settings.PARAGRAPH_RE, content):
                file_data_dict['is_toc'] = True
            # 替换有特殊含义的括号
            content_part = self.brace_replace(content_part)
            # 替换图片链接
            for re_dict in settings.IMG_RE_LIST:
                content_part = self.img_replace(re_dict, content_part)
            # 替换站内链接
            content_part = self.link_replace(content_part, file_dict)
            content_list[i] = content_part[1: -1]
        content = ''.join(content_list)
        file_data_dict['content'] = content
        blog_obj = models.BlogModel.objects.filter(path=file_data_dict.get('path'))
        if blog_obj:
            blog_obj.update(**file_data_dict)
        else:
            models.BlogModel.objects.create(**file_data_dict)

    def bulk_import_original(self, file_detail_list: list):
        for file_dict in file_detail_list:
            self.single_import_original(file_dict)


class HexoFileHandler:
    def hexo_generate(self, blog_obj):
        pass

    def bulk_hexo_generate(self, blog_obj_list):
        for blog_obj in blog_obj_list:
            self.hexo_generate(blog_obj)
