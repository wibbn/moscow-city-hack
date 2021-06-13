from flask import request, jsonify
from flask_restx import Resource, Namespace
from app.utils.get_places import get_topk_places

# Namespace

places_ns = Namespace("Places", path="/places", description="Get top places")

# Resources

@places_ns.route("")
class Place(Resource):
    def get(self):
        resp = get_topk_places(5)
        return {'places': resp}

    # def post(self):
    #     org_type = request.form['type']

        
    #     return {'a': 1}
