from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('update_list', views.updateList, name='update_list'),
    path('filmes/todos', views.todosFilmes, name='todos'),
    path('categoria/<str:categoria>', views.listaCategoria, name='lista_categoria'),
    path('filme/<str:nome>', views.movie, name='filme')
]