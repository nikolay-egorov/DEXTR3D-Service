import bcrypt
import shortuuid
from cryptography.fernet import Fernet, InvalidToken



app_secret_key = Fernet("xs4G5ZD9SwNME6nWRWrK_aq6Yb9H8VJpdwCzkTErFPw=")

UUID_ALPHABET = ''.join(map(chr, range(38, 58)))

def get_common_key():
    return app_secret_key


def uuid():
    return shortuuid.ShortUUID(alphabet=UUID_ALPHABET).random(10)


def encrypt_token(data):
    encryptor = get_common_key()
    return encryptor.encrypt(data.encode('utf-8'))


def decrypt_token(token):
    try:
        decryptor = get_common_key()
        return decryptor.decrypt(token.encode('utf-8'))
    except InvalidToken:
        return None


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def verify_password(password, hashed):
    return bcrypt.hashpw(password.encode('utf-8'), hashed) == hashed