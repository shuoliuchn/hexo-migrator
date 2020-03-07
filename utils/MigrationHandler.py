import os
import re
import time
from datetime import datetime

import yaml

from conf import settings
from utils import Singleton


class MigrationHandler(Singleton.Singleton):
    def __init__(self, content, file_path, project_path, target_path, log_handler, path_handler):
        self.content = content    # 修改好的文章内容
        self.file_path = file_path    # 原文存放位置
        self.file_name = os.path.basename(file_path)
        self.migration_log_handler = log_handler
        self.project_path = project_path
        self.target_path = target_path.rstrip('\\').rstrip('/')
        self.path_handler = path_handler
        self.old_title_dict = {}
        self.count = self.count if hasattr(self, 'count') else [0, 0]
        
    def yaml_front_matter_generator(self):
        yaml_str = '---\n'
        for k, v in self.title_dict.items():
            yaml_str = yaml_str + k + ': ' + v + '\n'
        yaml_str += '---\n\n'
        self.yaml_front_matter = yaml_str.replace('`', '').replace('\"', '').replace("\'", '')

    def file_write(self):
        """
        文本文件，也就是博客文件的写入
        1. 询问用户是否需要添加描述内容
            若需要，让用户输入，不需要则跳过
        2. 拼接开头的yaml front-matter
        3. 将yaml和content拼接
        4. 写入文件
        :return:
        """
        msg = f'请输入博客{self.file_name}的描述信息：'
        if self.old_title_dict.get('date'):
            self.title_dict['date'] = datetime.strftime(self.old_title_dict['date'], "%Y-%m-%d %H:%M:%S")
        else:
            self.title_dict['date'] = self.title_dict['updated']
        if self.old_title_dict.get('mathjax'):
            self.title_dict['mathjax'] = 'true'
        if self.old_title_dict.get('description'):
            print(self.old_title_dict['description'])
            change_choice = input('已发现之前的描述信息，是否需要修改[y/N]？').strip().upper()
            if change_choice not in ['Y', 'YES']:
                self.title_dict['description'] = self.old_title_dict['description']
            else:
                new_desc = input(msg).strip()
                if new_desc:
                    self.title_dict['description'] = new_desc
        else:
            change_choice = input('未发现从前文件中的描述信息，是否需要输入[Y/n]？').strip().upper()
            if change_choice in ['Y', 'YES', '']:
                desc = input(msg).strip()
                if desc:
                    self.title_dict['description'] = desc
        self.yaml_front_matter_generator()
        with open(self.target_file_path, 'w', encoding='utf8') as f:
            f.write(self.yaml_front_matter)
            f.write(self.content.strip())
            f.write('\n')
            f.flush()
            self.migration_log_handler.info(f'向文件 {self.file_rel_path} 中写入成功')

    def file_write_b(self):
        """
        静态文件，主要是图片的写入
        :return:
        """
        with open(self.target_file_path, 'wb') as f:
            f.write(self.content)
            f.flush()
            self.migration_log_handler.info(f'图片 {self.file_rel_path.replace(".assets", "")} 写入成功')

    def get_old_content(self):
        with open(self.target_file_path, 'r', encoding='utf8') as f:
            self.old_content = f.read()

    def remove_yaml(self, content: str):
        """
        获取已存在文件的yaml信息，
        同时，去除旧文件头部的yaml
        :param content:
        :return:
        """
        yaml_str = re.match(settings.YAML_STR_RE, content, re.DOTALL)
        if yaml_str:
            clean_yaml_str = yaml_str.group().strip().strip('-').strip()
            self.old_title_dict = yaml.load(clean_yaml_str, Loader=yaml.SafeLoader)
            return content.replace(yaml_str.group(), '')
        else:
            return content

    def get_category(self, file_path, project_path):
        if os.path.dirname(file_path) == project_path:
            return os.path.basename(file_path)
        else:
            return self.get_category(os.path.dirname(file_path), project_path)

    def get_title_dict(self):
        title_dict = {'layout': 'single-column'}
        title_raw = re.match(settings.TITLE_RE, self.content)
        if title_raw:
            title_dict['title'] = title_raw.group().strip().lstrip('#').lstrip()
            self.content = self.content.replace(title_raw.group(), '')
        else:
            title_dict['title'] = self.file_name.replace('.md', '')
        if re.search(settings.PARAGRAPH_RE, self.content):
            title_dict['toc'] = 'true'
        else:
            title_dict['toc'] = 'false'
        if os.path.dirname(self.file_path) == self.project_path:
            title_dict['categories'] = '首页'
            title_dict['top'] = 'true'
        else:
            category = self.get_category(self.file_path, self.project_path)
            title_dict['categories'] = settings.CATEGORY_DICT.get(category, '')
        # now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()+random.randint(1, 1000)))
        # title_dict['date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        title_dict['updated'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # head = settings.YAML_STR % (title.replace('`', '').replace('"', '').replace("'", ''), now_time, toc, categories)
        # content = head + content
        self.title_dict = title_dict
    
    def compare_content(self):
        old_content = self.remove_yaml(self.old_content)
        return self.content.strip() == old_content.strip()

    def migrate_assets(self):
        asset_list = []
        self.path_handler.get_assets_dirs(self.project_path, asset_list)
        for asset in asset_list:
            file_list = os.listdir(asset)
            for file in file_list:
                self.file_path = os.path.join(asset, file)
                self.file_rel_path = os.path.relpath(self.file_path, self.project_path)
                with open(self.file_path, 'rb') as f:
                    self.content = f.read()
                self.target_file_path = os.path.join(self.target_path, self.file_rel_path.replace('.assets', ''))
                target_file_dir = os.path.dirname(self.target_file_path)
                if os.path.isfile(self.target_file_path):
                    continue
                elif os.path.isdir(target_file_dir):
                    self.file_write_b()
                else:
                    os.makedirs(target_file_dir)
                    self.file_write_b()

    def word_count(self):
        self.count[0] += len(self.content)
        hanz_total = 0
        for char in self.content:
            # 中文字符其实还有很多，但几乎都用不到，这个范围已经足够了
            if '\u4e00' <= char <= '\u9fef':
                hanz_total += 1
        self.count[1] += hanz_total

    def migrate(self):
        self.file_rel_path = os.path.relpath(self.file_path, self.project_path)
        self.target_file_path = os.path.join(self.target_path, self.file_rel_path)
        target_file_dir = os.path.dirname(self.target_file_path)
        self.get_title_dict()
        self.content = self.content.replace('```vue\n', '```html\n').replace('```shell\n', '```bash\n')
        self.word_count()
        if os.path.isfile(self.target_file_path):
            self.get_old_content()
            if not self.compare_content():
                self.migration_log_handler.info(f'文件 {self.file_rel_path} 有更新内容')
                self.file_write()
        elif os.path.isdir(target_file_dir):
            self.file_write()
        else:
            os.makedirs(target_file_dir)
            self.file_write()



if __name__ == '__main__':
    print(22222222222222222222222)
    from utils import PathHandler, FileHandler
    test_dir = settings.TEST_DIR
    f = FileHandler.FileHandler()
    p = PathHandler.PathHandler()
    p_list = []
    p.get_md_files(test_dir, p_list)
    # print(p_list)
    for p in p_list:
        content = f.single_md_operation(p, test_dir, p_list)
        m = MigrationHandler(content, p, settings.TEST_DIR, settings.TARGET_TEST_DIR)
        m.migrate()
        break
