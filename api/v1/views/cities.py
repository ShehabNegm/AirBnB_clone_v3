#!/usr/bin/python3
"""Flask route that returns JSON response"""


from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=[
    'GET', 'POST'], strict_slashes=False)
def handle_cities_by_state(state_id):
    """carries out requests on all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)

    if request.method == 'POST':
        response = request.get_json()
        if response is None:
            abort(400, 'Not a JSON')

        name = response.get('name')
        if name is None:
            abort(400, 'Missing name')

        new_city = City(name=name, state_id=state_id)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=[
    'GET', 'PUT', 'DELETE'], strict_slashes=False)
def handle_city(city_id):
    """performs all methods on a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        city = city.to_dict()
        return jsonify(city)

    if request.method == 'PUT':
        response = request.get_json()
        if response is None:
            abort(400, 'Not a JSON')

        existing_keys = ['id', 'state_is', 'created_at', 'updated_at']
        for key, value in response.items():
            if key not in existing_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200

    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
