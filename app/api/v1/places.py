from flask import request, jsonify
from flask_restx import Resource, Namespace, reqparse
from app.utils.get_places import get_topk_places

# Namespace

places_ns = Namespace("Places", path="/places", description="Get top places")

# Resources

places_parser = reqparse.RequestParser()
places_parser.add_argument("type", type=str, location="json", store_missing=False,
                         help="Type of business")
places_parser.add_argument("address", type=str, location="json", store_missing=False,
                         help="Address of area")
places_parser.add_argument("topk", type=int, location="json", store_missing=False,
                         help="Number of results")

@places_ns.route("")
class Place(Resource):
    @places_ns.expect(places_parser)
    def post(self):
        args = places_parser.parse_args()
        org_type = args['type']
        place = args['address']
        k = args['topk']
        resp = get_topk_places(k, org_type, place)
        
        return {'places': resp}