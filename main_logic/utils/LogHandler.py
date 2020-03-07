import logging
import os

from main_logic.conf import  settings


class LogHandler:
    def __init__(self, log_file_name: str):
        log_path = os.path.join(settings.LOG_DIR, log_file_name)
        self.logger = logging.getLogger()    # 创建一个空架子
        fh = logging.FileHandler(log_path, mode='a', encoding='utf-8')    # 创建一个文件句柄，用来记录日志（文件流）
        ch = logging.StreamHandler()    # 创建一个屏幕流，打印记录的内容
        f_str = logging.Formatter('%(asctime)s %(name)s %(filename)s %(lineno)s %(message)s')    # 定义一个记录日志的格式
        self.logger.level = 10    # 设置日志记录的级别
        fh.setFormatter(f_str)    # 给文件句柄设置记录内容的格式
        ch.setFormatter(f_str)    # 给中控台设置记录内容的格式
        self.logger.addHandler(fh)    # 将文件句柄添加到logger对象中
        self.logger.addHandler(ch)    # 将中控台添加到logger对象中

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
