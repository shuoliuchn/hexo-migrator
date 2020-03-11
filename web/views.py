from django.shortcuts import render, HttpResponse, redirect
from django import views
from django.contrib.auth.backends import ModelBackend
from django.conf import settings

from . import myforms, models
from web.utils import PathHandler, FileHandler, DBHandler

# Create your views here.


class Login(views.View, ModelBackend):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        user = self.authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            request.session['username'] = str(user)
            return redirect('web:home')
        else:
            return redirect('web:login')


def logout(request):
    request.session.flush()
    return redirect('web:login')


class Home(views.View):
    def get(self, request):
        count = FileHandler.word_count()
        blog_list = models.BlogModel.objects.filter(is_valid=True)
        blog_del_list = models.BlogModel.objects.filter(is_valid=False)
        return render(request, 'home.html', {'blog_list': blog_list, 'blog_del_list': blog_del_list, 'count': count})


class BlogAddEditView(views.View):
    def get(self, request, pk=None):
        blog_obj = models.BlogModel.objects.filter(pk=pk).first()
        form_obj = myforms.BlogModelForm(instance=blog_obj)
        return render(request, 'blog_add_edit.html', {'form_obj': form_obj})

    def post(self, request, pk=None):
        blog_obj = models.BlogModel.objects.filter(pk=pk).first()
        form_obj = myforms.BlogModelForm(request.POST, instance=blog_obj)
        if form_obj.is_valid:
            form_obj.save()
            return redirect('web:home')
        else:
            return render(request, 'blog_add_edit.html', {'form_obj': form_obj})


def blog_del_view(request, pk=None):
    blog_obj = models.BlogModel.objects.filter(pk=pk)
    if blog_obj:
        blog_obj.update(is_valid=False)
    return redirect('web:home')


def blog_permanent_del_view(request, pk=None):
    blog_obj = models.BlogModel.objects.filter(pk=pk)
    if blog_obj:
        blog_obj.delete()
    return redirect('web:home')


def blog_restore_view(request, pk=None):
    blog_obj = models.BlogModel.objects.filter(pk=pk)
    if blog_obj:
        blog_obj.update(is_valid=True)
    return redirect('web:home')


class BulkImportOld(views.View):
    def get(self, request):
        data = {
            'old_blog_path': request.POST.get('old_blog_path') or settings.DEFAULT_OLD_DIR,
            'target_blog_path': request.POST.get('target_blog_path') or settings.BLOG_GEN_DIR
        }
        form_obj = myforms.ImportOldForm(data=data)
        return render(request, 'import_old.html', {'form_obj': form_obj})

    def post(self, request):
        form_obj = myforms.ImportOldForm(request.POST)
        if form_obj.is_valid():
            old_blog_path = request.POST.get('old_blog_path') or settings.DEFAULT_OLD_DIR
            target_blog_path = request.POST.get('target_blog_path') or settings.BLOG_GEN_DIR
            # 获取所有的 md 文件及从路径中提取到的信息
            file_list = []
            path_handler = PathHandler.PathHandler()
            path_handler.get_md_files(old_blog_path, file_list)
            file_detail_list = path_handler.get_file_detail(file_list, old_blog_path)
            # 对文件进行处理，分析 front-matter 中的信息，存储各种信息到数据库
            old_blog_handler = FileHandler.OldFileHandlser()
            old_blog_handler.old_file_db_dump(file_detail_list)
            # 转移图片
            FileHandler.img_migration(file_detail_list, target_blog_path)
            # return redirect('web:bulk_import_old')
            return redirect('web:home')
        else:
            return render(request, 'import_old.html', {'form_obj': form_obj})


class BulkImportOriginal(views.View):
    def get(self, request):
        data = {
            'old_blog_path': request.POST.get('old_blog_path') or settings.BLOG_BASE_DIR,
            'target_blog_path': request.POST.get('target_blog_path') or settings.BLOG_GEN_DIR
        }
        form_obj = myforms.ImportOldForm(data=data)
        return render(request, 'import_origin.html', {'form_obj': form_obj})

    def post(self, request):
        form_obj = myforms.ImportOldForm(request.POST)
        if form_obj.is_valid():
            blog_base_dir = request.POST.get('old_blog_path') or settings.DEFAULT_OLD_DIR
            blog_gen_dir = request.POST.get('target_blog_path') or settings.BLOG_GEN_DIR
            # 获取所有的 md 文件及从路径中提取到的信息
            file_list = []
            path_handler = PathHandler.PathHandler()
            path_handler.get_md_files(blog_base_dir, file_list)    # 找到 md 文件
            file_detail_list = path_handler.get_file_detail(file_list, blog_base_dir, '.assets')
            # 文件批量处理
            file_handler = FileHandler.OriginalFileHandler()
            file_handler.bulk_import_original(file_detail_list)
            # 转移图片
            FileHandler.img_migration(file_detail_list, blog_gen_dir, '.assets')
            # return redirect('web:bulk_import_original')
            return redirect('web:home')
        else:
            return render(request, 'import_old.html', {'form_obj': form_obj})


# def hexo_generate(request, pk):
#     try:
#         blog_obj = models.BlogModel.objects.get(pk=pk)
#     except models.BlogModel.DoesNotExist:
#         pass
#     return redirect('web:home')


def bulk_hexo_generate(request):
    """
    批量创建 Hexo 博客文件，或许未来可以增加指定文件生成，但真心觉得没这个必要，先不做了
    :param request:
    :return:
    """
    if request.method == 'GET':
        data = {
            'target_blog_path': request.POST.get('target_blog_path') or settings.BLOG_GEN_DIR
        }
        form_obj = myforms.ImportOldForm(data=data)
        return render(request, 'hexo_generate.html', {'form_obj': form_obj})
    blog_obj = models.BlogModel.objects.filter(is_valid=True)
    print(request.POST.get('target_blog_path'))
    return redirect('web:home')


def categories_bulk_create(request):
    DBHandler.categories_generator(settings.CATEGORY_DICT)
    return redirect('web:home')


class CategoriesView(views.View):
    def get(self, request):
        categories_list = models.CategoriesModel.objects.filter(is_valid=True)
        tags_list = models.TagsModel.objects.filter(is_valid=True)
        categories_del_list = models.CategoriesModel.objects.filter(is_valid=False)
        tags_del_list = models.TagsModel.objects.filter(is_valid=False)
        return render(request, 'categories_list.html', {
            'categories_list': categories_list,
            'categories_del_list': categories_del_list,
            'tags_list': tags_list,
            'tags_del_list': tags_del_list,
        })


class CategoriesAddEditView(views.View):
    def get(self, request, pk=None):
        categories_obj = models.CategoriesModel.objects.filter(pk=pk).first()
        form_obj = myforms.CategoriesModelForm(instance=categories_obj)
        return render(request, 'categories_add_edit.html', {'form_obj': form_obj})

    def post(self, request, pk=None):
        categories_obj = models.CategoriesModel.objects.filter(pk=pk).first()
        form_obj = myforms.CategoriesModelForm(request.POST, instance=categories_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('web:categories_list')
        else:
            return render(request, 'categories_add_edit.html', {'form_obj': form_obj})


def categories_del_view(request, pk):
    categories_obj = models.CategoriesModel.objects.filter(pk=pk)
    if categories_obj:
        categories_obj.update(is_valid=False)
    return redirect('web:categories_list')


def categories_permanent_del_view(request, pk):
    categories_obj = models.CategoriesModel.objects.filter(pk=pk)
    if categories_obj:
        categories_obj.delete()
    return redirect('web:categories_list')


def categories_restore_view(request, pk):
    categories_obj = models.CategoriesModel.objects.filter(pk=pk)
    if categories_obj:
        categories_obj.update(is_valid=True)
    return redirect('web:categories_list')


class TagsAddEditView(views.View):
    def get(self, request, pk=None):
        tags_obj = models.TagsModel.objects.filter(pk=pk).first()
        form_obj = myforms.TagsModelForm(instance=tags_obj)
        return render(request, 'categories_add_edit.html', {'form_obj': form_obj})

    def post(self, request, pk=None):
        tags_obj = models.TagsModel.objects.filter(pk=pk).first()
        form_obj = myforms.TagsModelForm(request.POST, instance=tags_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('web:categories_list')
        else:
            return render(request, 'tags_add_edit.html', {'form_obj': form_obj})


def tags_del_view(request, pk):
    tags_obj = models.TagsModel.objects.filter(pk=pk)
    if tags_obj:
        tags_obj.update(is_valid=False)
    return redirect('web:categories_list')


def tags_permanent_del_view(request, pk):
    tags_obj = models.TagsModel.objects.filter(pk=pk)
    if tags_obj:
        tags_obj.delete()
    return redirect('web:categories_list')


def tags_restore_view(request, pk):
    tags_obj = models.TagsModel.objects.filter(pk=pk)
    if tags_obj:
        tags_obj.update(is_valid=True)
    return redirect('web:categories_list')
