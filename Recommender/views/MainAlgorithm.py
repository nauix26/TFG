# -*- coding: UTF-8 -*-

from django.shortcuts import render
from Recommender.models import Users, Forms, Songs
from Recommender.constants import Constants
from pyechonest import config, artist, song
import time
import re


def MainAlgorithm(request):
    config.ECHO_NEST_API_KEY = Constants.ECHONEST_API_KEY #Poso la API key
    playlist = []

    #===========================LOAD USER & FORM INFORMATION=============================
    #
    user = load_user_information(request)
    #
    #==============================FAVOURITE SONGS=======================================
    #
    direct_songs(user,playlist)
    #
    #==================================ARTISTS===========================================
    #
    artist_songs(user,playlist)
    #
    #============================PREFERENCE FILTER 1=====================================
    #
    # Fins ara era agafar artistes similars i fer la TOP SONG.
    #
    # Aquí és on s'hauria de millorar. Podem fer cerques per tempo, ballable,
    # estil, instruments, llengua, temàtica, ... (incorporar dades a la BDD).
    #
    #============================PREFERENCE FILTER 2=====================================
    #
    # Aquí selecciona dues cançons: una de la zona geogràfica i època. Cançons entre
    # els 0 i 30 anys de vida (anys de rellevància). Mirem a quin país vivia durant
    # aquestes edats. Que torni una cançó del gènere folk, i una del genere preferit
    # de l'usuari o sense especificar gènere (tornarà una cançó popular de l'època).
    #
    #====================================================================================


    #Render Results:
    template_name = 'Recommender/results.html'
    context = {'playlist' : playlist}
    return render(request,template_name, context)


#================================================================================================#
#                                       MÈTODES PER UTILITZAR:                                   #
#================================================================================================#
def load_user_information(request):
    user = {}
    #ID:
    user['id'] = request.session['user_id']
    #Nom:
    user['name'] = Users.objects.get(id = user['id']).first_name
    #Any de naixement:
    user['birth_year'] = Users.objects.get(id = user['id']).birth_date.year
    #LLoc de naixement:
    user['birth_place'] = Users.objects.get(id = user['id']).birth_place
    #LLocs on ha viscut:
    user['lived_places'] = []
    aux_lived_places = Forms.objects.get(id = user['id']).places_lived.split('//')
    for place in aux_lived_places:
        aux_city = re.search('^[A-Za-z]*', place)
        city = aux_city.group(0)
        years = re.findall('[0-9]{4}', place)
        pair_place_period = {"City" : city, "Start" : years[0], "End" : years[1]}
        user['lived_places'].append(pair_place_period)
    #Gèneres preferits:
    user['genres'] = Forms.objects.get(id = user['id']).preferred_genres.split('//')
    #Li agrada ballar?:
    user['dancing'] = Forms.objects.get(id = user['id']).like_dancing
    #Toca algun instrument?:
    if Forms.objects.get(id = user['id']).play_instrument:
        user['instrument'] = Forms.objects.get(id = user['id']).instrument
    else:
        user['instrument'] = None
    #Cançons preferides:
    user['songs'] = []
    aux_songs = Forms.objects.get(id = user['id']).preferred_songs.split('//')
    for aux_song in aux_songs:
        artist_regex = re.search('\([A-Za-z0-9\s\.\-,_]*\)$', aux_song)
        try :
            aux_artist = artist_regex.group(0)[1:-1]
        except :
            aux_artist = None
        title = re.sub('\([A-Za-z0-9\s\.\-,_]*\)$', '', aux_song)
        pair_song_artist = {"Title" : title, "Artist" : aux_artist}
        user['songs'].append(pair_song_artist)
    #Artistes preferits:
    user['artists'] = Forms.objects.get(id = user['id']).preferred_artists.split('//')
    #Retorno la variable usuari:
    return user



def direct_songs(user,playlist):
    if len(user['songs']) < Constants.PLAYLIST_LENGTH:
        list1 = user['songs']
    else:
        list1 = preference_filter(user['songs'],user)
    add_to_playlist(list1,playlist)



def artist_songs(user,playlist):
    #TODO: Agafar temazos dels artistes preferits i similars a aquests.
    # Revisar si amb les cançons directes hem superat el % direct musical data.
    # 1) Fem una llista amb els artistes preferits.
    # 2) Afegim els artistes de les cançons preferides.
    # 3) Anem afegint les TOP SONGS de cada un d'aquests artistes fins a arribar al
    #    límit marcat per percentage_of_direct_musical_data
    x = 'Hello World'



def preference_filter(song_list,user):
    #TODO: El filtre de preferència
    # Ordenem amb algun sistema de puntuació (mateix instrument, mateix tempo, mateix gènere, ...
    # i agafem les primeres.
    x = 'Hello World'



def add_to_playlist(song_list,playlist):
    for song in song_list:
        try:
            aux_song = Songs.objects.get(title = song['Title'])
            #TODO: Agafem totes les dades de la Base de Dades que volem tenir com a resultat.
            playlist.append('Base de Dades')
        except:
            #TODO: Agafem totes les dades d'Echonest / MusicBrainz que volem tenir com a resultat.
            playlist.append('Echonest / MusicBrainz')