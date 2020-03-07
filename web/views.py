from django.shortcuts import render, HttpResponse, redirect
from django import views
from django.contrib.auth.backends import ModelBackend
from django.conf import settings

from . import myforms
from web.utils import PathHandler, FileHandler

# Create your views here.


class Login(views.View, ModelBackend):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        user = self.authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        print(user)
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
        return render(request, 'home.html')


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
            FileHandler.img_migration(file_detail_list)
            return redirect('web:bulk_import_old')
            # return redirect('web:home')
        else:
            return render(request, 'import_old.html', {'form_obj': form_obj})


