from django.urls import path,re_path
from . import views


urlpatterns = [

    path('upload-image/', views.upload_image, name='upload_image'),
    path('list-images/', views.list_images, name="list_images"),
    path('del-image/', views.del_image, name='del_image'),
    path('images/', views.falls_images, name="falls_images"),


]
app_name = 'image'