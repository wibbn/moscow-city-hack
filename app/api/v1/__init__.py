import os
from flask import Blueprint, render_template, url_for
from flask_restx import Api

blueprint = Blueprint("api", __name__)
api = Api(blueprint, version="1.0", title="Best Place Api",
          description="Recommendation of business locations application with REST-API")

# from . import main 
from .places import places_ns

api.add_namespace(places_ns)