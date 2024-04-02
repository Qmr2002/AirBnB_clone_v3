#!/usr/bin/python3
''' New view for Place objects '''

from flask import Flask, abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    ''' Retrieve all Place objects of a City '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<string:place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    ''' Retrieve a Place object by id '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/cities/<string:city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    ''' Create a new Place object '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, {'error': 'Not a JSON'})
    if 'user_id' not in data:
        abort(400, {'error': 'Missing user_id'})
    if 'name' not in data:
        abort(400, {'error': 'Missing name'})
    user_id = data.get('user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data['city_id'] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<string:place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    ''' Update a Place object '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, {'error': 'Not a JSON'})
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<string:place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    ''' Delete a Place object '''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200
