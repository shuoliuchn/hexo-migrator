import os
import re

import yaml
from django.conf import settings

from . import DBHandler


def img_migration(file_detail_list):
    for file_dict in file_detail_list:
        img_path = file_dict.get('img_path')
        if img_path:
            file_list = os.listdir(img_path)
            for file in file_list:
                file_path = os.path.join(img_path, file)
                file_rel_path = file_dict.get('img_rel_path')
                target_file_path = os.path.join(settings.BLOG_GEN_DIR, file_rel_path, file)
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
