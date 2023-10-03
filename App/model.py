"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos

def new_data_structs(choice):
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    data_structs = {"goalscorers": None,
                    "results": None,
                    "shootouts": None
                    }
    if choice == 1:

        data_structs["goalscorers"] = lt.newList("ARRAY_LIST")
        data_structs["results"] = lt.newList("ARRAY_LIST")
        data_structs["shootouts"] = lt.newList("ARRAY_LIST")

    elif choice == 2:

        data_structs["goalscorers"] = lt.newList("SINGLE_LINKED")
        data_structs["results"] = lt.newList("SINGLE_LINKED")
        data_structs["shootouts"] = lt.newList("SINGLE_LINKED")

    return data_structs



# Funciones para agregar informacion al modelo

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    
    lt.addLast(data_structs,data)


# Funciones para creacion de datos

def new_data_results(data):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos

    data["away_score"] = int(data["away_score"])
    data["home_score"] = int(data["home_score"])
    
    return data

def new_data_goalscorers(data):

    if data["minute"] != "":

        data["minute"] = float(data["minute"])

    return data




# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    for data in data_structs:
        if data.get("id") == id:
            return data
    
    return None


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    return len(data_structs)
    


def req_1(data_structs,equipo,condicion,n_numero):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    
    lista_results = data_structs["results"]

    lista_entrega = lt.newList("ARRAY_LIST")

    for result in lt.iterator(lista_results):
            if condicion == "Local":
                if result["home_team"] == equipo:
                    lt.addLast(lista_entrega,result)
            elif condicion == "Visitante":
                if result["away_team"] == equipo:
                    lt.addLast(lista_entrega,result)

            elif condicion == "Indiferente":
                if result["home_team"] == equipo or result["away_team"] == equipo:
                    lt.addLast(lista_entrega,result)

    if lt.size(lista_entrega) > n_numero:

        respuesta = lt.subList(lista_entrega,1,n_numero)
    
    else:
        
        respuesta = lista_entrega

    return respuesta,lt.size(lista_entrega)
        
     
def cmp_dates_req2(data_1,data_2):
    if data_1["date"] < data_2["date"]:
        return True
    else:
        return False



def req_2(data_structs,nombre_jugador,n_numero):
    """
    Función que soluciona el requerimiento 2
    """
    lista_scorers = data_structs["goalscorers"]

    lista_entrega = lt.newList("ARRAY_LIST")

    for scorer in lt.iterator(lista_scorers):
        if scorer["scorer"] == nombre_jugador:
            lt.addLast(lista_entrega,scorer)

    lista_entrega = merg.sort(lista_entrega,cmp_dates_req2)

    if lt.size(lista_entrega) > n_numero:

        respuesta = lt.subList(lista_entrega,1,n_numero)

    else:

        respuesta = lista_entrega

    return respuesta, lt.size(lista_entrega)




def req_3(data_structs,high_date,low_date,nombre_equipo):
    """
    Función que soluciona el requerimiento 3
    """
    
    lista_results = data_structs["results"]

    lista_scorers = data_structs["goalscorers"]

    lista_equipos = lt.newList("ARRAY_LIST")

    contador_local = 0   

    contador_visitante = 0


    for elemento in lt.iterator(lista_results): 
            
            if elemento["date"] >= low_date and elemento["date"] <= high_date:

                if elemento["home_team"] == nombre_equipo or elemento["away_team"] == nombre_equipo:

                    elemento["penalty"] = "Unknown"
                    elemento["own_goal"] = "Unknown"

                    if elemento["home_team"] == nombre_equipo:
                        contador_local += 1

                    else:
                        contador_visitante += 1
                   

                    lt.addLast(lista_equipos,elemento)


    for elemento_agregado in lt.iterator(lista_equipos):
        for elemento_scorer in lt.iterator(lista_scorers):
            if elemento_agregado["date"] == elemento_scorer["date"]:
                if elemento_agregado["home_team"] == elemento_scorer["home_team"]:
                    if elemento_agregado["penalty"] != True:
                        elemento_agregado["penalty"] = elemento_scorer["penalty"]
                    if elemento_agregado["own_goal"] != True:
                        elemento_agregado["own_goal"] = elemento_scorer["own_goal"]

    lista_equipos = merg.sort(lista_equipos,cmp_dates_req2)

    size = lt.size(lista_equipos)

    return lista_equipos,contador_local,contador_visitante,size


def req_4(data_structs,nombre_torneo,high_date,low_date):
    
    results = data_structs["results"]

    shootouts = data_structs["shootouts"]

    lista_entrega = lt.newList("ARRAY_LIST")

    total_shootout = 0

    cities = lt.newList("ARRAY_LIST")

    countries = lt.newList("ARRAY_LIST")

    
    for result in lt.iterator(results):
        if result["date"] >= low_date and result["date"] <= high_date:
            if result["tournament"] == nombre_torneo:
                
                result["winner"] = "Unknown"

                if lt.isPresent(cities,result["city"]) == 0:
                    lt.addLast(cities,result["city"])
                if lt.isPresent(countries,result["country"]) == 0:
                    lt.addLast(countries,result["country"])

                lt.addLast(lista_entrega,result)
    

    for result_2 in lt.iterator(lista_entrega):
        for shootout in lt.iterator(shootouts):
            if result_2["date"] == shootout["date"]:
                if result_2["home_team"] == shootout["home_team"] and result_2["away_team"] == shootout["away_team"]:
                    result_2["winner"] = shootout["winner"]
                    total_shootout += 1

    matches = lt.size(lista_entrega)

    total_cities = lt.size(cities)

    total_countries = lt.size(countries)

    return lista_entrega,matches,total_cities,total_countries,total_shootout


def req_5(data_structs,nombre_jugador,high_date,low_date):
    """
    Función que soluciona el requerimiento 5
    """
    lista_scorers = data_structs["goalscorers"]

    lista_results = data_structs["results"]

    lista_entrega = lt.newList("ARRAY_LIST")

    contador_torneos = lt.newList("ARRAY_LIST")

    goles = 0

    penalties = 0

    autogoles = 0

    for scorer in lt.iterator(lista_scorers):
        if scorer["date"] >= low_date and scorer["date"] <= high_date:
            if scorer["scorer"] == nombre_jugador:

                goles += 1

                scorer["tournament"] = "Unknown"
                scorer["home_score"] = 0
                scorer["away_score"] = 0

                if scorer["penalty"] == True:
                    penalties += 1

                if scorer["own_goal"] == True:
                    autogoles += 1

                lt.addLast(lista_entrega,scorer)


    
    for scorer_2 in lt.iterator(lista_entrega):
        for result in lt.iterator(lista_results):
            if scorer_2["date"] == result["date"]:
                
                if scorer_2["home_team"] == result["home_team"]:
                   
                    scorer_2["tournament"] = result["tournament"]

                    scorer_2["home_score"] = result["home_score"]

                    scorer_2["away_score"] = result["away_score"]

                    if lt.isPresent(contador_torneos,result["tournament"]) == 0:
                        lt.addLast(contador_torneos,result["tournament"])

    return lista_entrega,lt.size(contador_torneos),penalties,autogoles,goles



def comparacion_puntos(home_score,away_score):

    if home_score > away_score:
        points = 3
    elif home_score < away_score:
        points = 0
    else:
        points = 1

    return points



def comparacion_puntos_wins(puntos):

    victorias = 0
    perdidas = 0
    empates = 0

    if puntos == 3:
        victorias +=1 
    elif puntos == 1:
        empates +=1
    else:
        perdidas += 1
    
    return victorias,perdidas,empates


def cmp_mejor_equipo(equipo_1,equipo_2):

        if equipo_1["goals"] > equipo_2["goals"]:
            return True
        else:
            return False



def req_6(data_structs,nombre_torneo,high_date,low_date,n_numero):
    

    results = data_structs["results"] 

    scorers = data_structs["goalscorers"]
 
    lista_control_equipos = lt.newList("ARRAY_LIST") 

    lista_equipos = lt.newList("ARRAY_LIST")

    matches = 0

    cities = lt.newList("ARRAY_LIST")

    countries = lt.newList("ARRAY_LIST")

    for result in lt.iterator(results): 
        if result["tournament"] == nombre_torneo: 
            if result["date"] >= low_date and result["date"] <= high_date: 

                if lt.isPresent(countries,result["country"]) == 0:
                    lt.addLast(countries,result["country"])

                if lt.isPresent(cities,result["city"]) == 0:
                    lt.addLast(cities,result["city"])

                if lt.isPresent(lista_control_equipos,result["home_team"]) == 0: 

                    result["team"] = result["home_team"]

                    puntos = comparacion_puntos(result["home_score"],result["away_score"])

                    result["total_points"] = puntos

                    result["penalty_points"] = 0

                    result["matches"] = 1

                    result["own_goal_points"] = 0

                    wins,losses,draws = comparacion_puntos_wins(puntos)

                    result["wins"] = wins

                    result["draws"] = draws

                    result["losses"] = losses

                    result["goals_for"] = result["home_score"]

                    result["goals_against"] = result["away_score"]

                    result["goal_diferrence"] = result["goals_for"] - result["goals_against"]

                    result["top_scorer"] = []

                    print("x")

                    lt.addLast(lista_control_equipos,result["home_team"])

                    lt.addLast(lista_equipos,result)

                else:

                    for equipo_agregado in lt.iterator(lista_equipos):

                        if equipo_agregado["team"] == result["home_team"]:

                             puntos = comparacion_puntos(result["home_score"],result["away_score"])

                             equipo_agregado["total_points"] += puntos

                             equipo_agregado["matches"] += 1

                             wins,losses,draws = comparacion_puntos_wins(puntos)

                             equipo_agregado["wins"] += wins

                             equipo_agregado["draws"] += draws

                             equipo_agregado["losses"] += losses

                             equipo_agregado["goals_for"] += result["home_score"]

                             equipo_agregado["goals_against"] += result["away_score"]

                             equipo_agregado["goal_diferrence"] = equipo_agregado["goals_for"] - equipo_agregado["goals_against"]



                if lt.isPresent(lista_control_equipos,result["away_team"]) == 0: 

                    result["team"] = result["away_team"]

                    puntos = comparacion_puntos(result["away_score"],result["home_score"])

                    result["total_points"] = puntos

                    result["penalty_points"] = 0

                    result["matches"] = 1

                    result["own_goal_points"] = 0

                    wins,losses,draws = comparacion_puntos_wins(puntos)

                    result["wins"] = wins

                    result["draws"] = draws

                    result["losses"] = losses

                    result["goals_for"] = result["away_score"]

                    result["goals_against"] = result["home_score"]

                    result["goal_diferrence"] = result["goals_for"] - result["goals_against"]

                    result["top_scorer"] = []

                    lt.addLast(lista_control_equipos,result["away_team"])

                    lt.addLast(lista_equipos,result)

                else:

                    for equipo_agregado in lt.iterator(lista_equipos):

                        if equipo_agregado["team"] == result["away_team"]:

                             puntos = comparacion_puntos(result["away_score"],result["home_score"])

                             equipo_agregado["total_points"] += puntos

                             equipo_agregado["matches"] += 1

                             wins,losses,draws = comparacion_puntos_wins(puntos)

                             equipo_agregado["wins"] += wins

                             equipo_agregado["draws"] += draws

                             equipo_agregado["losses"] += losses

                             equipo_agregado["goals_for"] += result["away_score"]

                             equipo_agregado["goals_against"] += result["home_score"]

                             equipo_agregado["goal_diferrence"] = equipo_agregado["goals_for"] - equipo_agregado["goals_against"]


    for equipo in lt.iterator(lista_equipos):

        lista_control_jugadores = lt.newList("ARRAY_LIST")

        for scorer in lt.iterator(scorers):

            if scorer["team"] == equipo["team"]:

                if scorer["date"] >= low_date and scorer["date"] <= high_date:
                    
                    if scorer["penalty"] != False:

                        equipo["penalty_points"] += 1

                    if scorer["own_goal"] != False:

                        equipo["own_goal_points"] += 1

                    if lt.isPresent(lista_control_jugadores,scorer["scorer"]) == 0:
                        
                        scorer["goals"] = 1

                        scorer["matches"] = 1

                        scorer["total_time"] = scorer["minute"]

                        scorer["avg_time"] =  scorer["total_time"] / scorer["matches"]

                        equipo["top_scorer"].append(scorer)


                    else:

                        for scorer_anadido in equipo["top_scorer"]:
                            if scorer_anadido["scorer"] == scorer["scorer"]:

                                scorer_anadido["goals"] += 1

                                scorer_anadido["matches"] += 1

                                scorer_anadido["total_time"] += scorer["minute"]

                                scorer_anadido["avg_time"] = scorer_anadido["total_time"] / scorer_anadido["matches"]


        top_scorer = equipo["top_scorer"][0]
        max_goals = top_scorer["goals"]

        for scorer_max in equipo["top_scorer"]:
            if scorer_max["goals"] > max_goals:
                max_goals = scorer_max["goals"]
                top_scorer = scorer_max


        equipo["top_scorer"] = top_scorer

    cities_counter = lt.size(cities)

    countries_counter = lt.size(countries)

    teams_counter = lt.size(lista_equipos)

    if teams_counter > n_numero:

        lista_retorno = lt.subList(lista_equipos,1,n_numero)

    else:

        lista_retorno = lista_equipos

    
    lista_retorno_final = merg.sort(lista_retorno,cmp_mejor_equipo)

    
    return lista_retorno_final,cities_counter,countries_counter,teams_counter,matches


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento


def sort_criteria_results(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """


    if data_1["date"] > data_2["date"]:
        return True
    elif data_1["date"] < data_2["date"]:
        return False
    else:
        if data_1["home_score"] > data_2["away_score"]:
            return True
        else:
            return False
  
def sort_criteria_shootouts(data_1, data_2):

    if data_1["date"] > data_2["date"]:
        return True
    elif data_1["date"] < data_2["date"]:
        return False
    else:
        if data_1["home_team"] > data_2["away_team"]:
            return True
        elif data_1["home_team"] < data_2["away_team"]:
            return False
        else:
            return False
        
  
    

def sort_criteria_goalscorers(data_1, data_2):
    
    if data_1["date"] > data_2["date"]:
        return True
    elif data_1["date"] < data_2["date"]:
        return False
    else:
        if data_1["minute"] > data_1["minute"]:
            return True
        elif data_1["minute"] < data_1["minute"]:
            return False
        else:
            if data_1["scorer"] > data_1["scorer"]:
                return True
            else:
                return False
        


def sort(data_structs,order):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    if order == 1:
        data_structs["results"] = merg.sort(data_structs["results"],sort_criteria_results)
        data_structs["shootouts"] = merg.sort(data_structs["shootouts"],sort_criteria_shootouts)
        data_structs["goalscorers"] = merg.sort(data_structs["goalscorers"],sort_criteria_goalscorers)
    elif order == 2:
        data_structs["results"] = quk.sort(data_structs["results"],sort_criteria_results)
        data_structs["shootouts"] = quk.sort(data_structs["shootouts"],sort_criteria_shootouts)
        data_structs["goalscorers"] = quk.sort(data_structs["goalscorers"],sort_criteria_goalscorers)
    elif order == 3:
        data_structs["results"] = ins.sort(data_structs["results"],sort_criteria_results)
        data_structs["shootouts"] = ins.sort(data_structs["shootouts"],sort_criteria_shootouts)
        data_structs["goalscorers"] = ins.sort(data_structs["goalscorers"],sort_criteria_goalscorers)
    elif order == 4:
        data_structs["results"] = se.sort(data_structs["results"],sort_criteria_results)
        data_structs["shootouts"] = se.sort(data_structs["shootouts"],sort_criteria_shootouts)
        data_structs["goalscorers"] = se.sort(data_structs["goalscorers"],sort_criteria_goalscorers)

    return data_structs