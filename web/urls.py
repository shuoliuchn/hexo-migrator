from django.urls import path, re_path
from . import views

app_name = 'web'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.Home.as_view(), name='home'),
    path('blog/add/', views.BlogAddEditView.as_view(), name='blog_add'),
    re_path('blog/edit/(?P<pk>\d+)/', views.BlogAddEditView.as_view(), name='blog_edit'),
    re_path('categories/list/', views.CategoriesView.as_view(), name='categories_list'),
    re_path('categories/add/', views.CategoriesAddEditView.as_view(), name='categories_add'),
    re_path('categories/edit/(?P<pk>\d+)/', views.CategoriesAddEditView.as_view(), name='categories_edit'),
    re_path('tags/add/', views.TagsAddEditView.as_view(), name='tags_add'),
    re_path('tags/edit/(?P<pk>\d+)/', views.TagsAddEditView.as_view(), name='tags_edit'),
    path('import/old/', views.BulkImportOld.as_view(), name='bulk_import_old'),
    path('categories/bulk/create', views.categories_bulk_create, name='categories_bulk_create'),
]