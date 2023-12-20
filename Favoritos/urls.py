from django.urls import path
from . import views

app_name = "favoritos"
urlpatterns = [
    path("añadir/<int:id>", views.agregar_fav, name = "Agregar"),
    path("eliminar/<int:id>", views.eliminar_fav, name = "Eliminar"),
    path("", views.favoritos, name = "Favoritos")
]