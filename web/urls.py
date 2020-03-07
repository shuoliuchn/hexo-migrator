from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.Home.as_view(), name='home'),
    path('import/old/', views.BulkImportOld.as_view(), name='bulk_import_old'),
]