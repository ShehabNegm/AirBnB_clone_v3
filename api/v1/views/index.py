#!/usr/bin/python3
"""Returns a JSON representation os status"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def get_status():
    """status endpoint"""
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def get_count():
    count_dict = {"amenities": 'Amenity',
                  "cities": 'City',
                  "places": 'Place',
                  "reviews": 'Review',
                  "states": 'State',
                  "users": 'User'}

    for k in count_dict.keys():
        count_dict[k] = storage.count(count_dict.get(k))
    return jsonify(count_dict)
