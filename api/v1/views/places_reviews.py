#!/usr/bin/python3
"""Flask route that returns JSON response"""

from flask import Flask, jsonify, abort, request
from models import storage
from models import storage
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=[
    'GET'], strict_slashes=False)
def get_reviews_by_place(place_id):
    """Handles reviews by places"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Gets a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=[
    'DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=[
    'POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    user_id = data.get('user_id')
    if user_id is None or storage.get(User, user_id) is None:
        abort(400, 'Missing user_id or invalid user_id')

    text = data.get('text')
    if text is None:
        abort(400, 'Missing text')

    new_review = Review(user_id=user_id, place_id=place_id, text=text)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in [
                'id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
