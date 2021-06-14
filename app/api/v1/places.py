from numpy import require
from app.utils.get_heatmap import get_heatmap
from flask_restx import Resource, Namespace, reqparse
from flask_cors import cross_origin

from app.utils.get_places import get_topk_places
from app.utils.get_heatmap import get_heatmap

# Namespace

places_ns = Namespace("Places", path="/", description="Get top places")

# Resources

places_parser = reqparse.RequestParser()
places_parser.add_argument("type", type=str, location="json", store_missing=False,
                         help="Type of business")
places_parser.add_argument("address", type=str, location="json", store_missing=False,
                         help="Address of area")
places_parser.add_argument("from_price", type=float, location="json", required=False,
                         help="Address of area")
places_parser.add_argument("to_price", type=float, location="json", required=False,
                         help="Address of area")
places_parser.add_argument("from_area", type=float, location="json", required=False,
                         help="Address of area")
places_parser.add_argument("to_area", type=float, location="json", required=False,
                         help="Address of area")
places_parser.add_argument("topk", type=int, location="json", store_missing=False,
                         help="Number of results")

heatmap_parser = reqparse.RequestParser()
heatmap_parser.add_argument("lat", type=float, location="json", store_missing=False,
                         help="lat of center")
heatmap_parser.add_argument("lng", type=float, location="json", store_missing=False,
                         help="lng of center")
heatmap_parser.add_argument("radius", type=float, location="json", store_missing=False,
                         help="Radius")

@places_ns.route("/places")
class Place(Resource):
    @places_ns.expect(places_parser)
    @cross_origin()
    def post(self):
        args = places_parser.parse_args()
        org_type = args['type']
        place = args['address']
        k = args['topk']

        price = None
        area = None

        if 'from_price' in args.keys() and 'to_price' in args.keys():
            price = args['from_price'], args['to_price']
        if 'from_area' in args.keys() and 'to_area' in args.keys():
            area = args['from_area'], args['to_area']

        resp = get_topk_places(k, org_type, place, price, area)

        return {'places': resp}

@places_ns.route("/heatmap")
class Heatmap(Resource):
    @places_ns.expect(heatmap_parser)
    @cross_origin()
    def post(self):
        args = heatmap_parser.parse_args()
        
        coords = {}

        coords['lat'] = args['lat']
        coords['lng'] = args['lng']

        heat, comps = get_heatmap(coords, args['radius'])

        return {'heatmap': heat, 'comps': comps}