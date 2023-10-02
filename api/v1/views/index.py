#!/usr/bin/python3
"""Returns a JSON representation os status"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('status', methods=['GET'])
def get_status():
    """status endpoint"""
    return jsonify({"status": "OK"})
