from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("search/", views.search, name="search"),
    path("random/", views.random_page, name="random_page"),
    path("wiki/<str:title>/edit/", views.edit, name="edit"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path('wiki/CSS/', views.view_css, name='view_css'),
    path('wiki/Django_(web_framework)/', views.view_django, name='view_django'),
    path('wiki/Git/', views.view_git, name='view_git'),
    path('wiki/HTML/', views.view_html, name='view_html'),
    path('wiki/Python_(programming_language)/', views.view_python, name='view_python'),
]


