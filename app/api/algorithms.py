from flask import jsonify, request
from app.api import api
from app.models import User, Restaurant
import random

# @api.route("recommend/<string:username>/<int:id>", methods=["GET"])
# def recommend(username, id):

@api.route("recommend", methods=["GET"])
def recommend():
    """
    .. include:: docs/algorithms/recommend.md
    """
    username = request.args.get("username")
    id = request.args.get("id")
    user = User.query.filter_by(username=username)
    # history = user.history
    # diet = user.diet
    # ... do some algorit  hm stuff
    restaurants = list(Restaurant.query.all())
    size = len(restaurants)
    r = restaurants[random.randint(0, size - 1)]

    response = {
        "recommendation": {
            "name": r.name,
            "alias": r.alias,
            "latitude": r.latitude,
            "longitude": r.longitude
        },
        "id": id
    }

    return jsonify(response)
