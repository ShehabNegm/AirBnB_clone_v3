#!/usr/bin/python3
"""states view"""

from flask import jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET', 'POST'], strict_slashes=False)
def all_states():
    """function to get all states or post new one"""
    if request.method == 'GET':
        return jsonify([state.to_dict()
            for state in storage.all('State').values()])
    if request.method == 'POST':
        if not request.json:
            abort(400, 'Not a JSON')
        if 'name' not in request.json:
            abort(400, 'Missing name')
        state = State(**request.get_json())
        state.save()
        return make_response(jsonify(new_State.to_dict()), 201)

@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
        strict_slashes=False)
def id_state(state_id):
    """get state by its id"""
    state = storage.get('State', state_id)

    if not state:
        abort(404)

    if request.method == 'GET':
        return jsonify(state.to_dict())

    if request.method == 'DELETE':
        try:
            storage.delete(state)
            storage.save()
            return make_response(jsonify({}), 200)
        except Exception:
            abort(404)

    if request.method == 'PUT':
        if not request.json:
            abort(400, 'Not a JSON')
        for k, v in request.json.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(state, k, v)
            state.save()
            return make_response(jsonify(state.to_dict()), 200)
