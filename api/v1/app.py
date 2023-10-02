#!/usr/bin/python3
"""This module is to create an instance of Flask"""


from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Handles teardown by calling storage.close()"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """
    Handels error code 404
    """
    code_response = {
            "error": "Not fount"
    }
    return jsonify(code_response), 404

if __name__ == "__main__":
    """
    Main App
    """
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
