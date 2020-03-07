import os

from conf import settings


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
                    path_list.append(file_path)
                elif file.endswith('.assets'):
                    continue
                else:
                    self.get_md_files(file_path, path_list)
        else:
            path_list.append(project_path)

    def get_assets_dirs(self, project_path, path_list: list):
        if os.path.isdir(project_path):
            # ['bug-bible', 'database', 'index.md', ..., 'testing', 'translation', 'web']
            file_list = os.listdir(project_path)
            for file in file_list:
                if file in settings.FILE_IGNORE:
                    continue
                # C:\Users\Sure\PyProject\神器\技术查阅手册\bug-bible
                file_path = os.path.join(project_path, file)
                if os.path.isfile(file_path):
                    continue
                elif file.endswith('.assets'):
                    path_list.append(file_path)
                else:
                    self.get_assets_dirs(file_path, path_list)
        else:
            path_list.append(project_path)
