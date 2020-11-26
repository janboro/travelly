import os
import secrets
import requests
import urllib
import json
import csv
from flask import flash, current_app
from travelly.travelly import db
from travelly.models import Location


def remove_accents(input_text):
    strange = "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ"
    ascii_replacements = "acelnoszzACELNOSZZ"

    translator = str.maketrans(strange, ascii_replacements)
    return input_text.translate(translator)


def get_lat_lng(street, number, code, city):
    """
    input: address
    output: [lat, lng]
    """
    base_url = "https://nominatim.openstreetmap.org/search?"

    street = number + " " + street

    parameters = {"street": street, "city": city, "postalcode": code}
    r = requests.get(
        f"{base_url}{urllib.parse.urlencode(parameters)}{'&format=geojson'}"
    )
    data = json.loads(r.content)

    try:
        lat_lng = data.get("features")[0].get("geometry").get("coordinates")
        return lat_lng
    except Exception as e:
        # flash(f'Error: {e}')
        return False


def validate_location(street, number, code, city, user_id):
    location = Location.query.filter_by(
        street=street, number=number, code=code, city=city, user_id=user_id
    ).first()
    if location:
        msg = "This location already exists!"
        return msg
    try:
        # [1] -> latitude [0] -> longitude
        lat_lng = get_lat_lng(street, number, code, city)
        lat = lat_lng[1]
        lng = lat_lng[0]
        # if lat and lng don't exist, skips to except
        return (lat, lng)
    except:
        msg = f"The location {street} {number}, {code}, {city} \
                    doesn't seem to exist"
        return msg
    return True


def save_csv(csv_file):
    # generating a random hex as a new file name
    random_hex = secrets.token_hex(8)
    # extracting the file extension from uploaded file
    _, f_ext = os.path.splitext(csv_file.filename)
    # creating a new csv filename to be stored in our database
    csv_fn = random_hex + f_ext
    csv_path = os.path.join(current_app.root_path, "static/csv", csv_fn)
    # csv = open(csv_form)
    csv_file.save(csv_path)

    return csv_fn


def import_csv(csv_file, user_id):
    csv_path = os.path.join(current_app.root_path, "static/csv", csv_file)

    with open(csv_path, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            street = remove_accents(row["Street"]).capitalize()
            number = remove_accents(row["Number"]).upper()
            code = row["Code"]
            city = remove_accents(row["City"]).capitalize()

            try:
                print(row)
                value = validate_location(
                    street=street, number=number, code=code, city=city, user_id=user_id
                )
                if type(value) == str:
                    flash(value, "danger")
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
                        user_id=user_id,
                    )
                    db.session.add(location)
                    db.session.commit()
            except Exception as e:
                flash(f"Error: {e}")
    return
