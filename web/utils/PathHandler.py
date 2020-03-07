import os

from django.conf import settings


class PathHandler:
    def get_md_files(self, project_path, path_list: list):
        if os.path.isdir(project_path):
            # ['bug-bible', 'database', 'index.md', ..., 'testing', 'translation', 'web']
            file_list = os.listdir(project_path)
            for file in file_list:
                if file in settings.FILE_IGNORE:
                    continue
                # C:\Users\Sure\PyProject\神器\技术查阅手册\bug-bible
                file_path = os.path.join(project_path, file)
                if os.path.isfile(file_path):
                    if file.endswith('.md'):
                        path_list.append(file_path)
                else:
                    self.get_md_files(file_path, path_list)
        else:
            path_list.append(project_path)

    def get_file_detail(self, file_list, base_dir):
        """
        用来处理文件列表，需确保传入的列表中的元素皆为文件
        :param file_list:
        :param base_dir:
        :return:
        """
        file_detail_list = []
        for file in file_list:
            if not os.path.isfile(file):
                raise ValueError('%s 文件不存在！' % file)
            # C:\Users\Sure\PyProject\神器\hexo_migrator\main_logic\test\linux\test.md
            rel_path = os.path.relpath(file, base_dir)    # linux\test.md
            file_name = os.path.basename(file)    # test.md
            file_title = os.path.splitext(file_name)[0]    # test
            wrapper_folder = rel_path.split(os.path.sep, 1)[0]    # linux
            # C:\Users\Sure\PyProject\神器\hexo_migrator\main_logic\test\linux\test
            img_path = os.path.splitext(file)[0] if os.path.isdir(os.path.splitext(file)[0]) else None
            img_rel_path = os.path.relpath(img_path, base_dir) if img_path else None
            file_detail_list.append({
                'file_full_path': file,
                'file_rel_path': rel_path,
                'file_name': file_name,
                'file_title': file_title,
                'wrapper_folder': wrapper_folder,
                'img_path': img_path,
                'img_rel_path': img_rel_path,
            })
        return file_detail_list
