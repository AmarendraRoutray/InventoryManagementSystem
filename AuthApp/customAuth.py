from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from django.contrib.auth import get_user_model
import jwt
from core.utility import Syserror
from django.conf import settings
from functools import wraps
from rest_framework.response import Response

# custom_auth.py


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
       
        if authtoken := request.headers.get('Authorization', None):
            token = authtoken.split(' ')[1]
        else:
            raise NotAuthenticated("Missing Authorization Header.")
        User = get_user_model()
        if not token:
            raise NotAuthenticated("Authentication credentials were not provided.")

        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            user_id = decoded_token["user_id"]
            user = User.objects.get(id=user_id)

        except jwt.ExpiredSignatureError:
            raise NotAuthenticated("Authentication credentials were expried.")

        except jwt.InvalidTokenError:
            raise NotAuthenticated(
                "Incorrect Authentication credentials were provided."
            )
        except User.DoesNotExist:
            raise AuthenticationFailed("No such user exists")
        except Exception as e:
            Syserror(e)
            raise AuthenticationFailed(str(e))
        return (user, None)


def JWTEncrytpToken(payload):
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

