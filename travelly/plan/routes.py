from flask import render_template, Blueprint, redirect, url_for, request, flash
from flask_login import current_user, login_required
from flask_sqlalchemy import sqlalchemy
from travelly.travelly import db
from travelly.models import Location
from travelly.plan.utils import create_map, get_matrix, route_map
from travelly.locations.utils import add_location_to_planner, remove_location_from_planner

# from travelly.plan.BranchAndBound import TSP_bnb
from ortools.constraint_solver import routing_enums_pb2
from travelly.plan.algorithms.ORTools_solver import ORsolve
from travelly.plan.algorithms.my_NN import solve_my_NN
from travelly.plan.algorithms.my_nearest_insertion import solve_nearest_insertion
from travelly.plan.algorithms.my_furthest_insertion import solve_furthest_insertion
from travelly.plan.algorithms.lib_2opt import solve_2opt

plan = Blueprint("plan", __name__)


@plan.route("/planner")
@login_required
def planner():
    locations = Location.query.filter(Location.user_id == current_user.id).order_by(
        Location.id
    )

    map = create_map(locations=locations.order_by(Location.id))

    page = request.args.get("page", 1, type=int)
    planned_locations = Location.query.filter(
        (Location.user_id == current_user.id), (Location.in_planner == True)
    ).paginate(page=page, per_page=10)
    return render_template("planner/plan.html", map=map, locations=planned_locations)


@plan.route("/planner/add/<int:location_id>")
@login_required
def add(location_id):
    add_location_to_planner(location_id, current_user)
    return redirect(url_for("locations.location"))


@plan.route("/planner/remove/<int:location_id>")
@login_required
def remove(location_id):
    remove_location_from_planner(location_id, current_user)
    return redirect(url_for("locations.location"))


@plan.route("/planner/get_route", methods=["POST"])
@login_required
def get_route():
    if request.method == "POST":
        algorithm = request.form.get("algorithm")

        if algorithm == None:
            flash("Please choose an algorithm before proceeding", "danger")
            return redirect(url_for("plan.planner"))

        locations = Location.query.filter(
            (Location.user_id == current_user.id), (Location.in_planner == True)
        ).order_by(Location.id)

        locations_list = []
        for location in locations:
            loc = (
                location.street,
                location.number,
                location.code,
                location.city,
                location.lat,
                location.lng,
            )
            locations_list.append(loc)

        matrix = get_matrix(locations_list)

        if algorithm == "christofides":
            solver_method = routing_enums_pb2.FirstSolutionStrategy.CHRISTOFIDES
            path, cost = ORsolve(matrix, solver_method)

        elif algorithm == "path_cheapest_arc":
            solver_method = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
            path, cost = ORsolve(matrix, solver_method)

        elif algorithm == "nearest_neighbour":
            path, cost = solve_my_NN(matrix)

        elif algorithm == "nearest_insertion":
            path, cost = solve_nearest_insertion(matrix)

        elif algorithm == "furthest_insertion":
            path, cost = solve_furthest_insertion(matrix)

        elif algorithm == "two_opt":
            path, cost = solve_2opt(matrix)
        else:
            abort(404)

        ordered_locations = []
        for path_id in path:
            ordered_locations.append(locations_list[path_id])

        order = []
        for item in ordered_locations:
            order.append(item[0])
        print(order)
        page = request.args.get("page", 1, type=int)
        # locations = locations.order_by(sqlalchemy.func.field(Location.street, *order))

        # loc

        map = route_map(locations=ordered_locations)

        return render_template(
            "planner/planned_route.html",
            map=map,
            locations= ordered_locations
            # locations=locations.paginate(page=page, per_page=10),
        )
