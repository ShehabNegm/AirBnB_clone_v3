#!/usr/bin/python3
"""places view"""

from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/places/', methods=['GET', 'POST'], strict_slashes=False)
def all_places():
    """function to get all places or post new one"""
    if request.method == 'GET':
        return jsonify([place.to_dict()
                       for place in storage.all('Place').values()])
    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'name' not in request.json:
            abort(400, 'Missing name')
        new_place = Place(**request.get_json())
        new_place.save()
        return make_response(jsonify(new_place.to_dict()), 201)

@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def id_place(place_id):
    """get place by its id"""
    place = storage.get('Place', place_id)

    if not place:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        try:
            storage.delete(place)
            storage.save()
            return make_response(jsonify({}), 200)
        except Exception:
            abort(404)

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for k, v in request.json.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(place, k, v)
            place.save()
            return make_response(jsonify(place.to_dict()), 200)
