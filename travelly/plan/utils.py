import os
import folium
import numpy as np
from geopy import distance
from flask import current_app
from travelly.models import Location


def create_map(locations):
    map = folium.Map(
        location=[51.1079, 17.0385], zoom_start=12, width="100%", height="100%"
    )
    tooltip = "Click for more"

    for location in locations:
        if location.in_planner == True:
            color = "red"
        else:
            color = "blue"
        folium.Marker(
            [location.lat, location.lng],
            popup=(
                f"{location.street} {location.number},\
                                {location.code}, {location.city}"
            ),
            tooltip=tooltip,
            icon=folium.Icon(color=color),
        ).add_to(map)
    return map._repr_html_()


def route_map(locations):
    map = folium.Map(
        location=[51.1079, 17.0385], zoom_start=12, width="100%", height="100%"
    )
    tooltip = "Click for more"

    for location in locations:
        folium.Marker(
            [location[4], location[5]],
            popup=(
                f"{location[0]} {location[1]},\
                                {location[2]}, {location[3]}"
            ),
            tooltip=tooltip,
            icon=folium.Icon(color="red"),
        ).add_to(map)

    iterator = 0
    for i in range(len(locations) - 1):
        temp = iterator
        iterator += 1
        loc1 = (locations[temp][4], locations[temp][5])
        loc2 = (locations[iterator][4], locations[iterator][5])
        folium.PolyLine([loc1, loc2], line_opacity=0.5).add_to(map)
    return map._repr_html_()


def get_distance(lat_lng1, lat_lng2):
    return distance.distance(lat_lng1, lat_lng2).km


# get_euclidian_distance
# def get_distance(coord1, coord2):
#     x = coord1[0]*100 - coord2[0]*100
#     y = coord1[1]*100 - coord2[1]*100
#     return (x ** 2 + y ** 2) * 100


def get_matrix(locations):
    matrix = []
    for location1 in locations:
        sub_matrix = []
        lat_lng1 = (location1[4], location1[5])

        for location2 in locations:
            lat_lng2 = (location2[4], location2[5])
            dist = get_distance(lat_lng1, lat_lng2)
            sub_matrix.append(int(dist * 100))
        matrix.append(sub_matrix)
    return matrix


def get_final_cost(matrix, path):
    index = path[0]
    cost = 0
    for i in path[1:]:
        previous_index = index
        index = i
        cost += matrix[previous_index][index]
    return cost
