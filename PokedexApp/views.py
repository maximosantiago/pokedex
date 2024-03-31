from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from utils.utils import pokemones
import requests
# Create your views here.

def buscar(request):
    pokemones.clear() #Lo limpio para que en la busqueda no me salgan los pokemones buscados anteriormente 
    if request.method == "GET":
        nombre = request.GET.get("nombre")
        resultados = {}
        #api_url_name = "https://pokeapi.co/api/v2/pokemon/"
        api_url_name = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"
        response = requests.get(api_url_name)

        if len(nombre)<3:
            messages.error(request,"Pon un minimo de 2 letras")
            return redirect("Pokedex")

        if response.status_code == 200:
            datos = response.json()
            #Se filtra el pokemon por el nombre
            results = [pokemon for pokemon in datos["results"] if isinstance(pokemon, dict) and pokemon.get("name") and nombre.lower() in pokemon["name"].lower()] #Se va agregar pokemon a results si se encuentra lo buscado en la api
            #Agregue el pokemon y pokemon.get para que me devuelva true si existe el nombre o el pokemon
            """results = []
            for pokemon in datos["results"]:
                print(pokemon["name"])
                if isinstance(pokemon, dict) and pokemon.get("name"):
                    if nombre.lower() in pokemon["name"].lower():
                        results.append(pokemon)     """

            # Detalles adicionales
            if len(results) == 0:
                messages.warning(request, "No se ha encontrado ningun pokemon")
                return redirect("Pokedex")
            for pokemon in results:
                api_url_pokemon = pokemon["url"]
                response_pokemon = requests.get(api_url_pokemon)

                if response_pokemon.status_code == 200:
                    
                    datos_pokemon = response_pokemon.json()
            
                    tipos_pokemon = [tipo["type"]["name"] for tipo in datos_pokemon.get("types",[])]

                    peso = datos_pokemon["weight"]/10.0
                    altura = datos_pokemon["height"]/10.0
                    active = False
                    
                    if "fav" in request.session: #Determina si fav existe en session
                        for i in request.session["fav"]:
                            if i["name"] == pokemon["name"]:
                                active = True
                                break
                           
                    resultados={
                        "id":  datos_pokemon["id"],
                        "name": pokemon["name"],
                        "tipos": tipos_pokemon,
                        "weight": peso,
                        "height": altura,
                        "sprite_front": datos_pokemon["sprites"]["front_default"],
                        "sprite_back": datos_pokemon["sprites"]["back_default"],
                        "sprite_front_shiny": datos_pokemon["sprites"]["front_shiny"],
                        "sprite_back_shiny": datos_pokemon["sprites"]["back_shiny"],
                        "fav":active
                    }
                    pokemones.append(resultados)
            # Crea un objeto Paginator
            paginator = Paginator(pokemones, 6)

            # Obtiene el número de página desde la solicitud GET
            pagina = request.GET.get('pagina', 1)
            try:
                # Obtén la lista de pokemones para la página dada
                pokemones_pagina = paginator.page(pagina)
            except PageNotAnInteger:
                # Si la página no es un número entero, entrega la primera página
                pokemones_pagina = paginator.page(1)
            except EmptyPage:
                # Si la página está fuera de rango (por ejemplo, 9999), entrega la última página
                pokemones_pagina = paginator.page(paginator.num_pages)   

            #results_type  = [tipo for tipo in datos_type["types"] if tipo == ]
            

            return render(request, "pokedex.html", {"results":pokemones_pagina, "busqueda":nombre})
                

def pokedex(request):
    """if not request.user.is_authenticated:
        request.session["fav"].clear()
        print(request.session["fav"])"""
    return render(request, "pokedex.html")
