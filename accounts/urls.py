from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('alterar_dados/', views.update_user, name='update_user'),
    path('registro/', views.register, name='register'),
]
