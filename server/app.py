#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os
from flask_cors import CORS


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

CORS(app)

# api = Api(app)

# HOME ROUTE
@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

# GET ALL RESTAURANTS
@app.route('/restaurants', methods=['GET'])
def get_restaurants():

        restaurants=Restaurant.query.all()  
        return make_response(jsonify(
            [{
                "id": r.id,
                "name": r.name,
                "address":r.address}
                for r in restaurants]), 200)


# GET RESTAURANTS BY ID AND DELETE 
@app.route('/restaurants/<int:id>', methods=['GET','DELETE'])
def get_restaurant_by_id(id):

    restaurant= db.session.get(Restaurant, id)
    
    if not restaurant:
        return make_response(jsonify({"error":"Restaurant not found"}), 404)

    if request.method=='GET':
        return make_response(jsonify(restaurant.to_dict()), 200)

    elif request.method=='DELETE':
        db.session.delete(restaurant)
        db.session.commit()
        return make_response("", 204)

# GET ALL PIZZAS
@app.route('/pizzas', methods=['GET'])
def get_pizza():
    
    pizzas=Pizza.query.all()
    return make_response(jsonify([
        {
            "id": p.id,
            "name":p.name,
            "ingredients": p.ingredients
        }
        for p in pizzas]), 200)

# ADD RESTAURANTPIZZA
@app.route('/restaurant_pizzas', methods=['POST'])
def add_restaurant_pizza():
    data = request.get_json()

    try:
        new_pizza_restaurant = RestaurantPizza(
            price=data["price"],
            restaurant_id=data["restaurant_id"],
            pizza_id=data["pizza_id"]
        )
        db.session.add(new_pizza_restaurant)
        db.session.commit()

        response = {
            "id": new_pizza_restaurant.id,
            "price": new_pizza_restaurant.price,
            "pizza_id": new_pizza_restaurant.pizza_id,
            "restaurant_id": new_pizza_restaurant.restaurant_id,
            "pizza": new_pizza_restaurant.pizza.to_dict(),
            "restaurant": new_pizza_restaurant.restaurant.to_dict()
        }

        return make_response(jsonify(response), 201)

    except Exception:
        return make_response(jsonify({"errors":["validation errors"]}), 400)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
