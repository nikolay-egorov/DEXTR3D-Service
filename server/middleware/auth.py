from server.utils.auth import decrypt_token



class AuthHandler(object):
    def process_request(self, req, res):
        # if req.auth is not None:
        #     token = decrypt_token(req.auth)
        #     if token is None:
        #         raise EnvironmentError()
        #     else:
        #         req.context['auth_user'] = token.decode('utf-8')
        # else:
            req.context['auth_user'] = None
