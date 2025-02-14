from functools import wraps
from sanic import response
from sqlalchemy import select
import jwt
import hashlib
import os

import settings
from models import *


entity_dict = {'user': (User, User.user_id), 'admin': (Admin, Admin.admin_id)}


def generate_password_hash(password):
    salt = os.urandom(16).hex()
    password_hash = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), salt.encode(), 100000
    )
    return salt + password_hash.hex()


def verify_password(stored_password, password):
    salt = stored_password[:32]
    stored_password = stored_password[32:]
    password_hash = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), salt.encode(), 100000
    )
    return stored_password == password_hash.hex()


def decode_token(authorization_header):
    token = authorization_header[7:]
    token = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
    return token['id'], token['role']


def generate_token(id, role):
    token = jwt.encode({'id': id, 'role': role}, key=settings.JWT_SECRET, algorithm='HS256')
    return token


def check_token(func):
    @wraps(func)
    async def decorated_function(request, *args, **kwarg):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return response.json(
                {'message': 'Not authorized'},
                status=403
            )
        id, role = decode_token(authorization_header)
        session = request.ctx.session
        session.begin()
        result = await session.execute(select(entity_dict[role][1], entity_dict[role][0].full_name, entity_dict[role][0].email).where(entity_dict[role][1] == id))
        entity = result.first()
        await session.commit()
        await session.close()
        if not entity:
            return response.json(
                {'message': 'Authorization error'},
                status=401
            )
        return await func(request, entity, *args, **kwarg)

    return decorated_function



