import datetime
import jwt
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from Foodify_API import models


def create_access_token(id):
    return jwt.encode(
        {
            'user_id': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow()
        }, 'access_secret', algorithm='HS256'
    )


def create_refresh_token(id):
    return jwt.encode(
        {
            'user_id': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=14),
            'iat': datetime.datetime.utcnow()
        }, 'refresh_secret', algorithm='HS256'
    )


def decode_access_token(token):
    try:
        payload = jwt.decode(token, 'access_secret', algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return Response({'errorMessage': 'Unauthenticated, token has expired'}, status=401)


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, 'refresh_secret', algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return Response({'errorMessage': 'Refresh token has expired, login again'}, status=401)


def is_token_valid(request):
    try:
        header = get_authorization_header(request).split()

        if header and len(header) == 2:
            token = header[1].decode('utf-8')
        else:
            return False

        payload = jwt.decode(token, 'access_secret', algorithms=['HS256'])
        user = models.User.objects.get(id=payload['user_id'])
        if not user:
            return False
        return True
    except jwt.ExpiredSignatureError:
        return False
