from server.app import api
from server.resources.example import ExampleResource


api.add_route('/api/example', ExampleResource())
