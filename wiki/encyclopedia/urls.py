from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('random_page', views.random_page, name='random_page'),
    path('search', views.search, name='search'),
    path("wiki/<str:entry_title>", views.entry_page, name='entry_page'),
    path('new_entry', views.new_entry, name='new_entry'),
    path('edit_entry/<str:entry_title>', views.edit_entry, name='edit_entry'),
]
