from django.urls import path, re_path
from . import views

app_name = 'web'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.Home.as_view(), name='home'),
    path('blog/add/', views.BlogAddEditView.as_view(), name='blog_add'),
    re_path('blog/edit/(?P<pk>\d+)/', views.BlogAddEditView.as_view(), name='blog_edit'),
    re_path('blog/del/(?P<pk>\d+)/', views.blog_del_view, name='blog_del'),
    re_path('blog/permanent/del/(?P<pk>\d+)/', views.blog_permanent_del_view, name='blog_permanent_del'),
    re_path('blog/restore/(?P<pk>\d+)/', views.blog_restore_view, name='blog_restore'),
    path('categories/list/', views.CategoriesView.as_view(), name='categories_list'),
    path('categories/add/', views.CategoriesAddEditView.as_view(), name='categories_add'),
    re_path('categories/edit/(?P<pk>\d+)/', views.CategoriesAddEditView.as_view(), name='categories_edit'),
    re_path('categories/del/(?P<pk>\d+)/', views.categories_del_view, name='categories_del'),
    re_path('categories/permanent/del/(?P<pk>\d+)/', views.categories_permanent_del_view, name='categories_permanent_del'),
    re_path('categories/restore/(?P<pk>\d+)/', views.categories_restore_view, name='categories_restore'),
    path('tags/add/', views.TagsAddEditView.as_view(), name='tags_add'),
    re_path('tags/edit/(?P<pk>\d+)/', views.TagsAddEditView.as_view(), name='tags_edit'),
    re_path('tags/del/(?P<pk>\d+)/', views.tags_del_view, name='tags_del'),
    re_path('tags/permanent/del/(?P<pk>\d+)/', views.tags_permanent_del_view, name='tags_permanent_del'),
    re_path('tags/restore/(?P<pk>\d+)/', views.tags_restore_view, name='tags_restore'),
    path('import/old/', views.BulkImportOld.as_view(), name='bulk_import_old'),
    path('import/original/', views.BulkImportOriginal.as_view(), name='bulk_import_original'),
    path('categories/bulk/create', views.categories_bulk_create, name='categories_bulk_create'),
]