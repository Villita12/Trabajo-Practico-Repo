# capa de servicio/lógica de negocio

from ..transport import transport
from ..dao import repositories
from ..generic import mapper
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def getAllImages(input=None):
    # obtiene un listado de imágenes desde transport.py y lo guarda en un json_collection.
    # ¡OJO! el parámetro 'input' indica si se debe buscar por un valor introducido en el buscador.
    json_collection = []
    images = []
    if input:
        json_collection = transport.getAllImages(input)
    else:
        json_collection = transport.getAllImages(None)
    
    for json in json_collection:
        nasa_card = mapper.fromRequestIntoNASACard(json)
        images.append(nasa_card)
    
    return images


def getImagesBySearchInputLike(input):
    return getAllImages(input)


# añadir favoritos (usado desde el template 'home.html')  
def save_Favourite(request):
    fav = mapper.fromTemplateIntoNASACard(request)# transformamos un request del template en una NASACard.
    fav.user =request.user # le seteamos el usuario correspondiente.
    return repositories.saveFavourite(fav) # lo guardamos en la base.

# usados en el template 'favourites.html'
def getAllFavouritesByUser(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = repositories.getAllFavouritesByUser(user) # buscamos desde el repositorio TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            nasa_card = mapper.fromRequestIntoNASACard(favourite)# transformamos cada favorito en una NASACard, y lo almacenamos en nasa_card.
            mapped_favourites.append(nasa_card)

        return mapped_favourites


def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.





####MODIFICACIONES*********