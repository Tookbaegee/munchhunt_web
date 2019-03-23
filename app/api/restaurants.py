from flask import jsonify, render_template
from app.api import api
from app.models import Restaurant
from app.api.auth import token_auth

# Function to retrieve all restaurants and give enough information to put on the map

@api.route("/restaurants/get/all_restaurants/", methods=["GET"])
@token_auth.login_required
def get_all_restaurants():
    restaurants = Restaurant.query.all()
    if len(restaurants) > 0:
        stuff = {
            "status" : "success",
            "restaurants": [
                {
                    "name":r.name,
                    "alias":r.alias,
                    "latitude":r.latitude,
                    "longitude":r.longitude
                }
            for r in restaurants]
        }
        return jsonify(stuff)
    else:
        return jsonify({"status" : "error", "message" : "there are no restaurants available"})

# Function to get all information of specified restaurant
@api.route("/restaurants/get/restaurant_info_all/<string:alias>/", methods=["GET"])
@token_auth.login_required
def get_restaurant_info_all(alias):
    rest = Restaurant.query.filter_by(alias=alias).first()
    hours = rest.hours.first()
    menu = rest.menu.first()
    if rest:
        stuff = {
            "status":"success",
            "name": rest.name,
            "alias": rest.alias,
            "latitude": rest.latitude,
            "longitude": rest.longitude,
            "phone": rest.phone,
            "price": rest.price,
            "direction": rest.direction,
            "time": rest.time,
            "hours": {
                "sunday" : hours.sunday,
                "monday" : hours.monday,
                "tuesday" : hours.tuesday,
                "wednesday": hours.wednesday,
                "thursday": hours.thursday,
                "friday": hours.friday,
                "saturday": hours.saturday
            } if hours else None,
            "menu": [{
                "name" : item.name,
                "description" : item.description,
                "itemType" : item.itemType,
                "price" : item.price,
            } for item in menu.menuItems] if menu else None 
        }
        return jsonify(stuff)
    else:
        return jsonify({"status": "error", "message":"Specified restaurant could not be found."})

# Function to get minimum amount of restaurant information (used for putting info on map)
@api.route("/restaurants/get/restaurant_info/<string:alias>/", methods=["GET"])
@token_auth.login_required
def get_restaurant_info(alias):
    rest = Restaurant.query.filter_by(alias=alias).first()
    if rest:
        stuff = {
            "status":"success",
            "name": rest.name,
            "alias": rest.alias,
            "latitude": rest.latitude,
            "longitude": rest.longitude,
            "phone": rest.phone,
            "price": rest.price,
            "direction": rest.direction,
            "time": rest.time
        }
        return jsonify(stuff)
    else:
        return jsonify({"status": "error", "message":"Specified restaurant could not be found."})

# retrieves ONLY hours of specified restaurant (and name)
@api.route("/restaurants/get/restaurant_hours/<string:alias>/", methods=["GET"])
@token_auth.login_required
def get_restaurant_hours(alias):
    rest = Restaurant.query.filter_by(alias=alias).first()
    hours = rest.hours.first()
    if rest:
        stuff = {
            "status":"success",
            "name": rest.name,
            "hours": {
                "sunday" : hours.sunday,
                "monday" : hours.monday,
                "tuesday" : hours.tuesday,
                "wednesday": hours.wednesday,
                "thursday": hours.thursday,
                "friday": hours.friday,
                "saturday": hours.saturday
            } if hours else None
        }
        return jsonify(stuff)
    else:
        return jsonify({"status": "error", "message":"Specified restaurant could not be found."})

# retrieves ONLY menu items of specified restaurant (and name)
@api.route("/restaurants/get/restaurant_menu/<string:alias>/", methods=["GET"])
@token_auth.login_required
def get_restaurant_menu(alias):
    rest = Restaurant.query.filter_by(alias=alias).first()
    menu = rest.menu.first()
    if rest:
        stuff = {
            "status":"success",
            "name": rest.name,
            "menu": [{
                "name" : item.name,
                "description" : item.description,
                "itemType" : item.itemType,
                "price" : item.price,
            } for item in menu.menuItems] if menu else None 
        }
        return jsonify(stuff)
    else:
        return jsonify({"status": "error", "message":"Specified restaurant could not be found."})