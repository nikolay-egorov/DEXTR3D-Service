import falcon
import json

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict



class BaseResource(object):
    HELLO_WORLD = {
        'server': '%s' % 'Falcon REST API Template',
        'database': '%s (%s)' % ("mongoDB", '127.0.0.1' )
    }

    def to_json(self, body_dict):
        return json.dumps(body_dict)

    def on_error(self, res, error=None):
        res.status = error['status']
        meta = OrderedDict()
        meta['code'] = error['code']
        meta['message'] = error['message']

        obj = OrderedDict()
        obj['meta'] = meta
        res.body = self.to_json(obj)

    def on_success(self, res, data=None, id=None):
        res.status = falcon.HTTP_200
        meta = OrderedDict()
        meta['code'] = 200
        meta['message'] = 'OK'
        if id is not None:
            meta['id'] = id.__str__()
        obj = OrderedDict()
        obj['meta'] = meta
        obj['data'] = data
        if id is not None:
            obj['id'] = id.__str__()
        res.body = self.to_json(obj)


    def on_success_pswrd_change(self, res, data = None):
        res.status = falcon.HTTP_200
        meta = OrderedDict()
        meta['code'] = 200
        meta['message'] = 'Password has been successfully changed'


        obj = OrderedDict()
        obj['meta'] = meta
        obj['data'] = data
        res.body = self.to_json(obj)

    def on_get(self, req, res):
        if req.path == '/':
            res.status = falcon.HTTP_200
            res.body = self.to_json(self.HELLO_WORLD)
        else:
            raise falcon.HTTP_400(method='GET', url=req.path)

    def on_post(self, req, res):
        raise falcon.HTTP_200(method='POST', url=req.path)

    def on_put(self, req, res):
        raise falcon.HTTP_300(method='PUT', url=req.path)

    def on_delete(self, req, res):
        raise falcon.HTTP_401(method='DELETE', url=req.path)