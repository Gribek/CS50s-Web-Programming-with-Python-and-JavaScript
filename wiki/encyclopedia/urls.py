from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('random_page', views.random_page, name='random_page'),
    path('search', views.search, name='search'),
    path("wiki/<str:entry_title>", views.entry_page, name='entry_page'),
]
