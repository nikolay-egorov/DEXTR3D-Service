import falcon
import falcon_jsonify
import mongoengine as mongo

import server.settings as settings
from server.resources.example import ExampleResource
from server.middleware.auth import AuthHandler
from server.resources.base import base
from server.resources import user
from server.middleware.json_translator import JSONTranslator


class App(falcon.API):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.add_route('/api', ExampleResource())
        self.add_route('/', base.BaseResource())
        self.add_route('/register', user.Collection())
        self.add_route('/manage/login', user.Manage_Account())
        self.add_route('/manage/resetpsw', user.Manage_Account())


middleware = [AuthHandler(), JSONTranslator()]
api = App(middleware=middleware)
#  falcon_jsonify.Middleware(help_messages=settings.DEBUG)


if __name__ == "__main__":
    from waitress import serve

    serve(api, host="127.0.0.1", port=8000)