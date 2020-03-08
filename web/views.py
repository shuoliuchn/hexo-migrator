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
        blog_list = models.BlogModel.objects.filter(is_valid=True)
        return render(request, 'home.html', {'blog_list': blog_list})


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
            file_list = []
            path_handler = PathHandler.PathHandler()
            path_handler.get_md_files(old_blog_path, file_list)
            file_detail_list = path_handler.get_file_detail(file_list, old_blog_path)
            old_blog_handler = FileHandler.OldFileHandlser()
            old_blog_handler.old_file_db_dump(file_detail_list)
            FileHandler.img_migration(file_detail_list, target_blog_path)
            return redirect('web:bulk_import_old')
            # return redirect('web:home')
        else:
            return render(request, 'import_old.html', {'form_obj': form_obj})


def categories_bulk_create(request):
    DBHandler.categories_generator(settings.CATEGORY_DICT)
    return redirect('web:home')


class CategoriesView(views.View):
    def get(self, request):
        categories_list = models.CategoriesModel.objects.filter(is_valid=True)
        tags_list = models.TagsModel.objects.filter(is_valid=True)
        return render(request, 'categories_list.html', {'categories_list': categories_list, 'tags_list': tags_list})


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



