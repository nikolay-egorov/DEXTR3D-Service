import falcon
import re

from cerberus import Validator, DocumentError
from src.utils.auth import *
from src.utils.hooks import auth_required
from src.resources import user
from src.resources.base.base import BaseResource
from src.model.user import User
from src.conf import initMongoDBConn, initConfig
from bson.json_util import dumps
from webargs import fields
from webargs.falconparser import use_args


FIELDS = {
    'login': {
        'type': 'string',
        'required': True,
        'minlength': 4,
        'maxlength': 20
    },
    'email': {
        'type': 'string',
        'regex': '[a-zA-Z0-9._-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}',
        'required': True,
        'maxlength': 320
    },
    'password': {
        'type': 'string',
        'regex': '[0-9a-zA-Z]\w{3,14}',
        'required': True,
        'minlength': 8,
        'maxlength': 64
    },
    'info': {
        'type': 'dict',
        'required': False
    }
}

new_user_validation = {
    'login': fields.Str(required=True),
    'email': fields.Str(required=True)
}

def validate_user_create(req, res, resource, params):
    schema = {
        'login': FIELDS['login'],
        'email': FIELDS['email'],
        'password': FIELDS['password'],
        'info': FIELDS['info']
    }

    v = Validator(schema)
    try:
        if not v.validate(req.context['data']):
            raise EnvironmentError(v.errors)
    except DocumentError:
        raise DocumentError('Invalid Request %s' % req.context)


class Collection(BaseResource):
    """
    Handle for endpoint: /register
    """
    #TODO: implement scripting via user class, not pure json
    def __add_to_mongo(self, json_data):
        mongo_conn = initMongoDBConn(mongodb_collection)

        insert_id = mongo_conn['account'].insert_one({
            'login': json_data['login'],
            'email': json_data['email'].lower(),
            'password': json_data['password'],
            'info': json_data['info']
        }).inserted_id

        return insert_id

    # @falcon.before(validate_user_create)
    # @use_args(new_user_validation)
    # def on_post(self, req, res, args):
    def on_post(self, req, res):
        # session = req.context['session']
        user_req = req.context['data']
        # user_req = args
        if user_req:
            user = User()

            mongo_conn = initMongoDBConn(mongodb_collection)

            account = mongo_conn['account'].find_one({
                'login': user_req['login'].lower()
            })

            if account is not None:
                status_code = (falcon.HTTP_200, 404,)
                msg ='Your login is in base, no need to register'
                res.body = dumps({
                    'status': status_code[1],
                    'msg': msg,
                })
                return

            user.login = user_req['data']['login']
            user.email = user_req['data']['email']
            user.password = hash_password(user_req['data']['password']).decode('utf-8')
            user.info = user_req['data']['info'] if 'info' in user_req else None
            sid = uuid()
            user.sid = sid
            user.token = encrypt_token(sid).decode('utf-8')
            # session.add(user)
            id = self.__add_to_mongo(user_req['data'])
            self.on_success(res, None, id)

            'A way to serve static resources via Falcon'
            # res.content_type = 'text/html'
            # with open('index.html', 'r') as f:
            #     res.body = f.read()
        else:
            raise AssertionError(req.context['data'])

    # @falcon.before(auth_required)
    # def on_get(self, req, res):
    #     session = req.context['session']
    #     user_dbs = session.query(User).all()
    #     if user_dbs:
    #         obj = [user.to_dict() for user in user_dbs]
    #         self.on_success(res, obj, None)
    #     else:
    #         raise EnvironmentError()

    @falcon.before(auth_required)
    def on_put(self, req, res):
        pass


config = initConfig()
mongodb_collection = config.get('accounts-storage', 'collection', fallback='accounts-storage')


class Manage_Account(BaseResource):

    def __change_password(self, json_data, account_id):
        hashed_password = hash_password(json_data['password']).decode('utf-8')

        mongo_conn = initMongoDBConn(component=mongodb_collection)
        mongo_conn['account'].update_one({
            '_id': account_id
        }, {
            '$set': {
                'password': hashed_password
            }
        })


    LOGIN = 'login'
    RESETPW = 'resetpsw'


    def on_get(self, req, res):
        cmd = re.split('\\W+', req.path)[-1:][0]
        if cmd == self.LOGIN:
            self.process_login(req, res)
        elif cmd == self.RESETPW:
            self.process_resetpsw(req, res)

    def process_login(self, req, res):
        data = req.context['data']
        email = data['data']['email']
        password = data['data']['password']
        # session = req.context['session']
        try:
            # user_db = User.find_by_email(session, email)
            mongo_conn = initMongoDBConn(component=mongodb_collection)
            user_db = mongo_conn['account'].find_one({
                'email': email
            })

            if verify_password(password, user_db['password'].encode('utf-8')):
                self.on_success(res, user_db.to_dict(), id=None)
            else:
                # raise PasswordNotMatch()
                raise AssertionError("Password do not match")
        except ValueError as e :
            raise print('User email: %s' % email)


    # @falcon.before(auth_required)
    def process_resetpsw(self, req, res):
        # session = req.context['session']
        insert_id = None
        status_code = (falcon.HTTP_200, 200,)
        json_data = req.context['data']


        if status_code[1] == 200:
            status, msg,  account_id = False if req.context['status'][1] != 200 else True, req.context[
                'msg'], req.context['account']['_id']

            if 'password' not in json_data:
                status_code = (falcon.HTTP_200, 404,)
                msg.append('Your new password is missing')
                status = False

            if status:
                self.__change_password(json_data, account_id)

        res.body = dumps({
            'status': status_code[1],
            'msg': msg,
            'insert_id': insert_id
        })

        self.on_success_pswrd_change(res, res.body)

