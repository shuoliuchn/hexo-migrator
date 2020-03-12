import datetime

from django.db.models import Q

from web import models


def old_blog_db_handler(data_dict: dict):
    """
    将字典数据生成为数据库内容
    :param data_dict: 字典的键要和 BlogModel 中的字段相匹配
    :return:
    """
    path = data_dict.get('file_rel_path')
    blog_obj = models.BlogModel.objects.filter(path=path).first() or models.BlogModel()
    blog_obj.title = data_dict.get('title') or data_dict.get('file_title')
    blog_obj.path = path
    blog_obj.categories = models.CategoriesModel.objects.filter(
        Q(category_name=data_dict.get('categories')) | Q(wrapper_folder=data_dict.get('wrapper_folder'))
    ).first()
    # blog_obj.tags = data_dict.get('tags')
    blog_obj.is_mathjax = bool(data_dict.get('mathjax'))
    blog_obj.allow_comments = bool(data_dict.get('comments'))
    blog_obj.is_top = bool(data_dict.get('top'))
    blog_obj.layout = data_dict.get('layout')
    blog_obj.is_toc = bool(data_dict.get('toc'))
    blog_obj.date = data_dict.get('date') or datetime.datetime.now()
    blog_obj.update = data_dict.get('update') or datetime.datetime.now()
    blog_obj.description = data_dict.get('description')
    blog_obj.content = data_dict.get('content')

    blog_obj.save()


def categories_generator(categories_dict: dict):
    """
    使用字典，批量导入分类信息
    :param categories_dict: {外层文件夹名: 分类名}
    :return:
    """
    for wrapper_folder, category_name in categories_dict.items():
        categories_obj = models.CategoriesModel.objects.filter(
            wrapper_folder=wrapper_folder).first() or models.CategoriesModel()
        categories_obj.wrapper_folder = wrapper_folder
        categories_obj.category_name = category_name
        categories_obj.save()
