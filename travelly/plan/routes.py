from flask import render_template, Blueprint, redirect, url_for, request
from flask_login import current_user, login_required
from flask_sqlalchemy import sqlalchemy
from travelly import db
from travelly.models import Location
from travelly.plan.utils import create_map, get_matrix, route_map
from travelly.plan.BranchAndBound import TSP_bnb

plan = Blueprint('plan', __name__)

@plan.route('/planner')
@login_required
def planner():
    locations = Location.query.filter(Location.user_id==current_user.id)\
                .order_by(Location.street)

    map = create_map(locations=locations)

    page = request.args.get('page', 1, type=int)
    planned_locations = Location.query.filter((Location.user_id==current_user.id),\
                        (Location.in_planner==True)).paginate(page=page, per_page=10)
    return render_template('planner/plan.html', map=map, locations=planned_locations)


# @plan.plan_trip('/plan_trip')
# @login_required
# def plan_trip():
#     locations = Location.query.filter(Location.in_planner==True)
#     return


@plan.route('/planner/add/<int:location_id>')
@login_required
def add(location_id):
    location = Location.query.get_or_404(location_id)
    if location.author != current_user:
        abort(403)
    location.in_planner = True
    db.session.commit()
    return redirect(url_for('locations.location'))


@plan.route('/planner/remove/<int:location_id>')
@login_required
def remove(location_id):
    location = Location.query.get_or_404(location_id)
    if location.author != current_user:
        abort(403)
    location.in_planner = False
    db.session.commit()
    return redirect(url_for('locations.location'))


@plan.route('/planner/remove_from_plan/<int:location_id>')
@login_required
def remove_from_plan(location_id):
    location = Location.query.get_or_404(location_id)
    if location.author != current_user:
        abort(403)
    location.in_planner = False
    db.session.commit()
    return redirect(url_for('plan.planner'))

@plan.route('/planner/branch_and_bound')
@login_required
def branch_and_bound():
    locations = Location.query.filter((Location.user_id==current_user.id),
                (Location.in_planner==True))

    matrix = get_matrix(locations)
    print(matrix)

    path, cost = TSP_bnb(matrix)
    print(path)

    # rv = TSP_bnb(matrix)
    # print(rv)

    for location, path_id in zip(locations, path):
        location.path_order = path_id
        # db.session.commit()
    page = request.args.get('page', 1, type=int)
    locations = locations.order_by(Location.path_order)

    map = route_map(locations=locations)

    return render_template('planner/planned_route.html', map=map,\
        locations=locations.paginate(page=page, per_page=10))
