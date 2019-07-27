from django.urls import path

from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:slug>/', views.category, name='category'),
    path('produto/<slug:slug>/', views.product, name='product'),
]
