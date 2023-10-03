#!/usr/bin/python3
"""states view"""

from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/amenities/', methods=['GET', 'POST'], strict_slashes=False)
def all_users():
    """function to get all users or post new one"""
    if request.method == 'GET':
        return jsonify([user.to_dict()
                       for user in storage.all('User').values()])
    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'name' not in request.json:
            abort(400, 'Missing name')
        new_user = Amenity(**request.get_json())
        new_user.save()
        return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def id_user(user_id):
    """get state by its id"""
    user = storage.get('User', user_id)

    if not user:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        try:
            storage.delete(user)
            storage.save()
            return make_response(jsonify({}), 200)
        except Exception:
            abort(404)

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for k, v in request.json.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(user, k, v)
            user.save()
            return make_response(jsonify(user.to_dict()), 200)
