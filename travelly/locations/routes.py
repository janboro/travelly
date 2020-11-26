from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from travelly.travelly import db
from travelly.locations.forms import AddLocationForm, UpdateLocationForm, CSVForm
from travelly.models import Location
from travelly.locations.utils import (
    get_lat_lng,
    validate_location,
    remove_accents,
    import_csv,
    save_csv,
)

locations = Blueprint("locations", __name__)


@locations.route("/location", methods=["GET", "POST"])
@login_required
def location():
    page = request.args.get("page", 1, type=int)
    locations = (
        Location.query.filter(Location.user_id == current_user.id)
        .order_by(Location.street)
        .paginate(page=page, per_page=10)
    )

    add_location_form = AddLocationForm()
    if add_location_form.validate_on_submit():
        street = remove_accents(add_location_form.street.data).capitalize()
        number = remove_accents(add_location_form.number.data).upper()
        code = add_location_form.code.data
        city = remove_accents(add_location_form.city.data).capitalize()

        value = validate_location(
            street=street, number=number, code=code, city=city, user_id=current_user.id
        )
        if type(value) == str:
            flash(value, "danger")
            return redirect(url_for("locations.new_location"))
        else:
            lat = value[0]
            lng = value[1]

        location = Location(
            street=street,
            number=number,
            code=code,
            city=city,
            lat=lat,
            lng=lng,
            user_id=current_user.id,
        )
        db.session.add(location)
        db.session.commit()
        flash("Your location has been added!", "success")
        return redirect(url_for("locations.location"))

    CSV_form = CSVForm()
    if CSV_form.validate_on_submit():
        csv_file = save_csv(CSV_form.csv.data)
        import_csv(csv_file, user_id=current_user.id)

        return redirect(url_for("locations.location"))
    return render_template(
        "location/location.html",
        locations=locations,
        add_location_form=add_location_form,
        CSV_form=CSV_form,
    )


@locations.route("/location/new", methods=["GET", "POST"])
@login_required
def new_location():
    form = AddLocationForm()
    if form.validate_on_submit():
        street = remove_accents(form.street.data).capitalize()
        number = remove_accents(form.number.data).upper()
        code = form.code.data
        city = remove_accents(form.city.data).capitalize()

        value = validate_location(
            street=street, number=number, code=code, city=city, user_id=current_user.id
        )
        if type(value) == str:
            flash(value, "danger")
            return redirect(url_for("locations.new_location"))
        else:
            lat = value[0]
            lng = value[1]

        location = Location(
            street=street,
            number=number,
            code=code,
            city=city,
            lat=lat,
            lng=lng,
            user_id=current_user.id,
        )
        db.session.add(location)
        db.session.commit()
        flash("Your location has been added!", "success")
        return redirect(url_for("locations.location"))
    return redirect(url_for("locations.location"))


@locations.route("/location/detail/<int:location_id>")
@login_required
def detail(location_id):
    location = Location.query.get_or_404(location_id)
    if location.author != current_user:
        abort(403)
    return render_template("location/detail.html", location=location)


@locations.route("/location/<int:location_id>/delete", methods=["POST"])
@login_required
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    if location.author != current_user:
        abort(403)
    try:
        db.session.delete(location)
        db.session.commit()
        flash("This location has been deleted!", "success")
        return redirect(url_for("locations.location"))
    except:
        flash("There was an error deleting that location")


@locations.route("/location/delete_multiple", methods=["GET", "POST"])
def delete_multiple():
    if request.method == "POST":
        to_delete = request.form.getlist("location_checkbox")
        for location_id in to_delete:
            delete_location(location_id)
    return redirect(url_for("locations.location"))


@locations.route("/location/<int:location_id>/update", methods=["GET", "POST"])
@login_required
def update_location(location_id):
    location = Location.query.get_or_404(location_id)
    if location.author != current_user:
        abort(403)
    form = UpdateLocationForm()
    if form.validate_on_submit():
        street = remove_accents(form.street.data).capitalize()
        number = remove_accents(form.number.data).upper()
        code = form.code.data
        city = remove_accents(form.city.data).capitalize()

        value = validate_location(
            street=street, number=number, code=code, city=city, user_id=current_user.id
        )
        if type(value) == str:
            flash(value, "danger")
            return redirect(
                url_for("locations.update_location", location_id=location_id)
            )
        else:
            lat = value[0]
            lng = value[1]

        location.street = street
        location.number = number
        location.code = code
        location.city = city
        location.lat = lat
        location.lng = lng
        db.session.commit()
        flash("Your location has been updated!", "success")
        return redirect(url_for("locations.location"))
    else:
        form.street.data = location.street
        form.number.data = location.number
        form.code.data = location.code
        form.city.data = location.city
    return render_template("location/update_location.html", form=form)
