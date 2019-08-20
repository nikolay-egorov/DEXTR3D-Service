from mongoengine import *
import datetime


class User(Document):
    user_id = IntField(unique=True)
    login = StringField(unique=True)
    email = EmailField(unique=True)
    password = StringField(default=True)
    info = StringField( )
    # timestamp = DateTimeField(default=datetime.datetime.now())

    def __repr__(self):
        return "<User(name='%s', email='%s', token='%s', info='%s')>" % \
               (self.login, self.email, self.timestamp, self.info)

    @classmethod
    def get_id(cls):
        return User.user_id

    @classmethod
    def find_by_email(cls, session, email):
        return session.query(User).filter(User.email == email).one()

    # @classmethod
    # def change_pswrd