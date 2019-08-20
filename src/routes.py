from src.app import api
from src.resources.example import ExampleResource


api.add_route('/api/example', ExampleResource())
