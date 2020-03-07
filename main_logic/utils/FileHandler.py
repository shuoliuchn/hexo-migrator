import os
import re
import time
import random

from main_logic.conf import settings


class FileHandler:
    def split_code_block(self, content: str) -> list:
        """
        偶数索引为普通文本内容，
        奇数索引为代码块内容，不需替换
        :param content:
        :return:
        """
        content_list = []
        block_list = re.findall(settings.CODE_BLOCK_RE, content, re.DOTALL)
        for block in block_list:
            content_before, content = content.split(block, 1)
            content_list.append(content_before)
            content_list.append(block)
        content_list.append(content)
        return content_list

    def img_replace(self, re_dict, content):
        content_list = self.split_code_block(content)
        l = len(content_list)
        img_tag_list = re.findall(re_dict['tag'], content)
        for img_tag in img_tag_list:
            img_name = re.findall(re_dict['file_name'], img_tag)[0]
            # {% asset_img example.jpg This is an example image %}
            new_str = '{% asset_img ' + img_name + ' ' + img_name.split('.')[0] + ' %}'
            for i in range(0, l, 2):
                content_list[i] = content_list[i].replace(img_tag, new_str)
        return ''.join(content_list)

    def re_replace(self, re_str: str, content: str, new_str='', dotall=False):
        params = [re_str, content] + ([re.DOTALL] if dotall else [])
        re_list = re.findall(*params)
        for s in re_list:
            content = content.replace(s, new_str)
        return content

    def remove_code_block(self, content: str):
        content = self.re_replace(settings.CODE_BLOCK_RE, content, dotall=True)
        # 这个判断最好是代码块替换完之后再判断，因为代码块有可能被识别为行内代码
        content = self.re_replace(settings.INLINE_CODE_BLOCK_RE, content)
        return content

    def get_category(self, file_path, project_path):
        if os.path.dirname(file_path) == project_path:
            return os.path.basename(file_path)
        else:
            return self.get_category(os.path.dirname(file_path), project_path)

    def title_replace(self, content, file_path, project_path):
        title_raw = re.match(settings.TITLE_RE, content)
        if title_raw:
            title = title_raw.group().strip().lstrip('#').lstrip()
            content = content.replace(title_raw.group(), '')
        else:
            title = self.file_name
        if re.search(settings.PARAGRAPH_RE, content):
            toc = 'true'
        else:
            toc = 'false'
        if os.path.dirname(file_path) == project_path:
            categories = '首页\ntop: true'
        else:
            categories = settings.CATEGORY_DICT.get(self.get_category(file_path, project_path), '')
        # now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()+random.randint(1, 1000)))
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        head = settings.YAML_STR % (title.replace('`', '').replace('"', '').replace("'", ''), now_time, toc, categories)
        content = head + content
            
        return content

    def link_replace(self, content, file_path, project_path):
        link_list = re.findall(settings.LINK_RE, content)
        content_list = self.split_code_block(content)
        l = len(content_list)
        for link in link_list:
            rel_dir = link.strip(')').strip('#').rsplit('(', 1)[-1]
            file_dir = os.path.dirname(file_path)
            abs_dir = os.path.abspath(os.path.join(file_dir, rel_dir))
            # project_rel_dir = os.path.relpath(abs_dir, project_path)
            # new_link = link
            url_link = abs_dir.replace(project_path, '').replace('\\', '/')[:-3]
            new_link = link.replace(rel_dir, url_link)
            # for md_file in md_file_list:
            #     if md_file.endswith(project_rel_dir):
            #         url_link = md_file.replace(project_path, '').replace('\\', '/')[:-3]
            #         new_link = link.replace(rel_dir, url_link)
            #         break
            for i in range(0, l, 2):
                content_list[i] = content_list[i].replace(link, new_link)
        return ''.join(content_list)

    def toc_replace(self, content):
        content_list = self.split_code_block(content)
        l = len(content_list)
        for toc_re in settings.TOC_RE_LIST:
            for i in range(0, l, 2):
                content_list[i] = content_list[i].replace(toc_re, '\n')
        return ''.join(content_list)

    def brace_replace(self, content):
        for brace_re in settings.BRACE_RE_LIST:
            brace_list = set(re.findall(brace_re, content))
            for brace in brace_list:
                new_brace = settings.BRACE_LEFT + brace + settings.BRACE_RIGHT
                content = content.replace(brace, new_brace)
        return content

    def single_md_operation(self, file_path, project_path, md_file_list):
        f = open(file_path, 'r', encoding='utf8')
        self.file_name = os.path.basename(file_path).split('.')[0]
        content = f.read()
        # 替换目录
        content = self.toc_replace(content)
        # print('替换目录完成')
        # 替换标题
        # content = self.title_replace(content, file_path, project_path)
        # print('替换标题完成')
        # 括号替换
        # content = self.brace_replace(content)
        # print('替换括号完成')
        # 图片替换
        for re_dict in settings.IMG_RE_LIST:
            content = self.img_replace(re_dict, content)
        # print('替换图片完成')
        # 链接替换
        content = self.link_replace(content, file_path, project_path)
        # print('替换链接完成')
        f.close()
        return content


