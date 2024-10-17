# Create your views here.
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .CustomAuthBackend import AuthBackend
from django.conf import settings
from datetime import datetime, timedelta
from core.utility import Syserror
from AuthApp.models import User, Token
from AuthApp.customAuth import JWTEncrytpToken
from rest_framework.decorators import api_view
from .serializers import UserSignUpSerializer


@api_view(['POST'])
def user_signup(request):
    serializer = UserSignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

class Login(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request):
        try:
            data = request.data
            email = data.get("email", None)
            password = data.get("password", None)
            if not email:
                response = {"success": False, "message": "Required email."}
                return Response(response, status=400)
            if not password:
                response = {"success": False, "message": "Required password."}
                return Response(response, status=400)

            user_exist = User.objects.filter(email=email)
            if not user_exist.exists():
                response = {"success": False, "message": "email not found."}
                return Response(response, status=400)

            if not user_exist.first().is_active:
                response = {
                    "success": False,
                    "message": "Your Account is Inactive. Please contact admin.",
                }
                return Response(response, status=400)

            user = AuthBackend.authenticate(
                request, email=email, password=password
            )
            if not user:
                response = {
                    "success": False,
                    "message": "Invalid Password",
                }
                return Response(response, status=400)
            expired_at = datetime.now() + timedelta(seconds=settings.JWT_EXPIRE)
            jwt_payload = {
                "user_id": user.id,
                "iat": int(datetime.now().timestamp()),
                "exp": int(expired_at.timestamp())
            }
            
            user.save()
            token = JWTEncrytpToken(jwt_payload)
            Token.objects.create(
                token=token,
                user=user,
                expired_at=expired_at
            )
           
            userData = UserProfileSerializer(user).data
            resp_data = {
                "success": True,
                "message": "Login Successfully",
                "token": token,
                "data": userData,
            }
            return Response(resp_data, status=200)
        except Exception as e:
            Syserror(e)
            response = {
                "success": False,
                "message": str(e),
            }
            return Response(response, status=400)


class Logout(APIView):
    # permission_classes = (AllowAny, IsAuthenticated)
    # authentication_classes = []

    def get(self, request):
        try:
            data = {
                "success": True,
                "message": "Logout successfully",
            }
            
            
            return Response(data, status=200)

        except Exception as e:
            Syserror(e)
            response = {
                "success": "false",
                "message": str(e),
            }
            return Response(response, status=400)



