from main_logic.utils import FileHandler, PathHandler, MigrationHandler, LogHandler
from main_logic.conf import settings

def run():
    file_handler = FileHandler.FileHandler()
    path_handler = PathHandler.PathHandler()
    md_list = []
    path_handler.get_md_files(settings.TEST_DIR, md_list)
    migration_log_handler = LogHandler.LogHandler(settings.MIGRATION_LOG_NAME)
    for md in md_list:
        content = file_handler.single_md_operation(md, settings.TEST_DIR, md_list)
        migration_handler = MigrationHandler.MigrationHandler(content, md, settings.TEST_DIR,
                                                              settings.TARGET_TEST_DIR,
                                                              migration_log_handler,
                                                              path_handler)
        migration_handler.migrate()
    if md_list:
        migration_handler.migrate_assets()
        count = migration_handler.count
        print(f'运行完成！博客字符总数：{count[0]}；汉字字符数：{count[1]}')
