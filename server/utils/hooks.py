

def auth_required(req, res, resource,code):
    if req.context['auth_user'] is None:
        raise AssertionError()