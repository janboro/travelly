import os
import folium
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
            [location.lat, location.lng],
            popup=(
                f"{location.street} {location.number},\
                                {location.code}, {location.city}"
            ),
            tooltip=tooltip,
            icon=folium.Icon(color="red"),
        ).add_to(map)

    iterator = 0
    for loc1 in locations:
        iterator += 1
        for loc2 in locations:
            if loc2.path_order == iterator:
                # print(loc1.path_order, loc2.path_order)
                # print((loc1.lat,loc1.lng), (loc2.lat, loc2.lng))
                folium.PolyLine(
                    [(loc1.lat, loc1.lng), (loc2.lat, loc2.lng)], line_opacity=0.5
                ).add_to(map)
            if loc2.path_order == (locations.count() - 1) and loc1.path_order == 0:
                # print(loc2.path_order, loc1.path_order)
                # print((loc1.lat,loc1.lng), (loc2.lat, loc2.lng))
                folium.PolyLine(
                    [(loc1.lat, loc1.lng), (loc2.lat, loc2.lng)], line_opacity=0.5
                ).add_to(map)
    return map._repr_html_()

def get_distance(lat_lng1, lat_lng2):
    return distance.distance(lat_lng1, lat_lng2).km


def get_matrix(locations):
    matrix = []
    for location1 in locations:
        sub_matrix = []
        lat_lng1 = (location1.lat, location1.lng)

        for location2 in locations:
            lat_lng2 = (location2.lat, location2.lng)
            dist = get_distance(lat_lng1, lat_lng2)
            sub_matrix.append(dist)
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