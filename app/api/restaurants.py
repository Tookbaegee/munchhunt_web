from flask import jsonify, render_template
from app.api import api
from app.models import Restaurant

# Method to get all information of specified restaurant
@api.route("/restaurants/get/restaurant_info_all/<string:alias>", methods=["GET"])
def get_restaurant_info_all(alias):
    rest = Restaurant.query.filter_by(alias=alias).first_or_404()
    if rest:
        stuff = {
            "name": rest.name,
            "alias": rest.alias,
            "latitude": rest.latitude,
            "longitude": rest.longitude,
            "phone": rest.phone,
            "price": rest.price,
            "direction": rest.direction,
            "time": rest.time,
            "hours": [{
                "sunday" : h.sunday,
                "monday" : h.monday,
                "tuedsay" : h.tuesday,
                "wednesday": h.wednesday,
                "thursday": h.thursday,
                "friday": h.friday,
                "saturday": h.saturday
            } for h in rest.hours] if rest.menus else None,
            "menus": [[{
                "name" : item.name,
                "description" : item.description,
                "itemType" : item.itemType,
                "price" : item.price,
            } for item in m.menuItems] for m in rest.menus] if rest.menus else None 
        }
        return jsonify(stuff)

# Method to get minimum amount of restaurant information (used for putting info on map)
@api.route("/restaurants/get/restaurant_info/<string:alias>", methods=["GET"])
def get_restaurant_info(alias):
    rest = Restaurant.query.filter_by(alias=alias).first_or_404()
    if rest:
        stuff = {
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

# retrieves ONLY hours of specified restaurant (and name)
@api.route("/restaurants/get/restaurant_hours/<string:alias>", methods=["GET"])
def get_restaurant_hours(alias):
    rest = Restaurant.query.filter_by(alias=alias).first_or_404()
    if rest:
        stuff = {
            "name": rest.name,
            "hours": [{
                "sunday" : h.sunday,
                "monday" : h.monday,
                "tuedsay" : h.tuesday,
                "wednesday": h.wednesday,
                "thursday": h.thursday,
                "friday": h.friday,
                "saturday": h.saturday
            } for h in rest.hours] if rest.menus else None
        }
        return jsonify(stuff)

# retrieves ONLY Hours of specified restaurant (and name)
@api.route("/restaurants/get/restaurant_menu/<string:alias>", methods=["GET"])
def get_restaurant_menu(alias):
    rest = Restaurant.query.filter_by(alias=alias).first_or_404()
    if rest:
        stuff = {
            "name": rest.name,
            "menus": [[{
                "name" : item.name,
                "description" : item.description,
                "itemType" : item.itemType,
                "price" : item.price,
            } for item in m.menuItems] for m in rest.menus] if rest.menus else None 
        }
        return jsonify(stuff)