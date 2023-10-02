#!/usr/bin/python3
"""states view"""

from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET', 'POST'], strict_slashes=False)
def all_amenities():
    """function to get all states or post new one"""
    if request.method == 'GET':
        return jsonify([amenity.to_dict()
                       for amenity in storage.all('Amenity').values()])
    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'name' not in request.json:
            abort(400, 'Missing name')
        new_amenity = Amenity(**request.get_json())
        new_amenity.save()
        return make_response(jsonify(new_amenity.to_dict()), 201)

@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def id_amenity(amenity_id):
    """get state by its id"""
    amenity = storage.get('Amenity', amenity_id)

    if not amenity:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        try:
            storage.delete(amenity)
            storage.save()
            return make_response(jsonify({}), 200)
        except Exception:
            abort(404)

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for k, v in request.json.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, k, v)
            amenity.save()
            return make_response(jsonify(amenity.to_dict()), 200)
