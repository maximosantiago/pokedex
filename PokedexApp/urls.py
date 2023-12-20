from django.urls import path
from . import views

urlpatterns =[
    path("", views.pokedex, name = "Pokedex"),
    path("buscar/", views.buscar, name = "Buscar")
]