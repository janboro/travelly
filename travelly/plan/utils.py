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
            # if iterator == print

    # for i in range(len(locations.all())):
    #     print(i)
    #     if i == range(len(locations.all())):
    #         location1 = Location.query.filter(Location.path_order.in_([i]))
    #         location2 = Location.query.filter(Location.path_order.in_([0]))
    #         folium.PolyLine(locations[(location1.lat, location1.lng),
    #                                 (location2.lat, location2.lng)],
    #                                 line_opacity = 0.5).add_to(map)
    #     else:
    #         location1 = Location.query.filter(Location.path_order.in_([i]))
    #         print(location1.id)
    #         location2 = Location.query.filter(Location.path_order.in_([i+1]))
    #         folium.PolyLine(locations[(location1.lat, location1.lng),
    #                                 (location2.lat, location2.lng)],
    #                                 line_opacity = 0.5).add_to(map)
    return map._repr_html_()


# def plot_route(path, map):
#     for i in range(len(path)):
#         if i == (len(path) - 1):
#             location1 = Location.query.get_or_404(path[i])
#             location2 = Location.query.get_or_404(path[0])
#             folium.PolyLine(locations[(location1.lat, location1.lng),
#                                     (location2.lat, location2.lng)],
#                                     line_opacity = 0.5).add_to(map)

#         else:
#             location1 = Location.query.get_or_404(path[i])
#             location2 = Location.query.get_or_404(path[i+1])
#             folium.PolyLine(locations[(location1.lat, location1.lng),
#                             (location2.lat, location2.lng)],
#                             line_opacity = 0.5).add_to(map)
#         location = Location.query.get_or_404(path_id)
#     return map._repr_html_()


# for path_id, i in zip(path, len(path)):
#     if i == len(path):
#         location1 = Location.query.get_or_404(path_id)
#         location2 = Location.query.get_or_404(1)
#         folium.PolyLine(locations[(location1.lat, location1.lng),
#                         (location2.lat, location2.lng)],
#                         line_opacity = 0.5).add_to(map)

#     else:
#         location1 = Location.query.get_or_404(path_id)
#         location2 = Location.query.get_or_404(path[i+1])
#         folium.PolyLine(locations[(location1.lat, location1.lng),
#                         (location2.lat, location2.lng)],
#                         line_opacity = 0.5).add_to(map)
#     location = Location.query.get_or_404(path_id)


#     if i == locations.total - 1:
#         folium.PolyLine(locations[(Location.location[i].lat, location[i].lng),
#                         (location[0].lat, location[0].lng)],
#                         line_opacity = 0.5).add_to(map)


# for i in range(locations.total):
#     if i == locations.total - 1:
#         folium.PolyLine(locations[(location[i].lat, location[i].lng),
#                         (location[0].lat, location[0].lng)],
#                         line_opacity = 0.5).add_to(map)
#     else:
#         folium.PolyLine(locations[(location[i].lat, location[i].lng),
#                         (location[i+1].lat, location[i+1].lng)],
#                         line_opacity = 0.5).add_to(map)


def get_distance(lat_lng1, lat_lng2):
    """
    This function returns the geographical distance beetween two points.
    Input: Latiture & Longitude of point 1 and point 2
    If used to calculate the matrix of distances, the matrix will be symetrical
    """
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
