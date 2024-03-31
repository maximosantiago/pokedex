from django.shortcuts import render, redirect
from .lista_favoritos import lista_fav
from utils.utils import pokemones
from asgiref.sync import sync_to_async 
import requests
# Create your views here.

def find_id(request,id):
    if len(pokemones)==0:

        for i in request.session["fav"]:
            pokemones.append(i)
    for pok in pokemones: 
        
        if pok["id"] == id:
            return pok
    return {}    

async def agregar_fav(request, id):
    pokemon=await sync_to_async(find_id)(request,id)
    if pokemon:
        lista = await sync_to_async(lista_fav)(request)
        await sync_to_async(lista.agregar)(pokemon = pokemon) 

            
    return redirect(request.META.get("HTTP_REFERER"))
async def eliminar_fav(request, id):

    pokemon=await sync_to_async(find_id)(request, id)
    print(pokemon)
    if pokemon:
        lista = await sync_to_async(lista_fav)(request)
        await sync_to_async(lista.eliminar)(pokemon = pokemon) 
    return redirect(request.META.get("HTTP_REFERER"))

    

def favoritos(request):
    favs = []
    if "fav" in request.session and len(request.session["fav"]) !=0:
        
        for fav in request.session["fav"]:
            #Comprobante para si el fav es True
            favs.append(fav)


    return render(request, "favoritos/favorito.html",{"favs":favs})