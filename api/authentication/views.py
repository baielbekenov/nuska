from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import datetime
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str as force_text
from django.utils.encoding import force_bytes
from rest_framework.throttling import ScopedRateThrottle
from apps.authentication.models import Soglashenie
from api.authentication.serializers import CustomTokenObtainSerializer, UserGetSerializer, UserRegisterSerializer, SoglashenieSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
User = get_user_model()


class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        refresh = super().get_token(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return data


class RegistrationAPIView(APIView):
    """Регистрация пользователя"""

    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        phone = serializer.validated_data.get("phone")
        raw_password = serializer.validated_data.get("password1")
        email = serializer.validated_data.get("email")

        code = "".join([str(random.randint(1, 9)) for _ in range(0, 6)])
        
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Бул электрондук почтасы бар колдонуучу мурунтан эле бар."}, 
                status=status.HTTP_409_CONFLICT
        )

        user = User.objects.filter(email=email)
        

        if user.exists():
            user = user.first()
            user.code = urlsafe_base64_encode(force_bytes(code))
            user.last_sms_date = datetime.datetime.now(datetime.timezone.utc)
        else:
            user = User(
                phone=phone,
                first_name=serializer.validated_data.get("first_name"),
                last_name=serializer.validated_data.get("last_name"),
                email=serializer.validated_data.get("email"),
                code=urlsafe_base64_encode(force_bytes(code)),
                last_sms_date=datetime.datetime.now(datetime.timezone.utc),
            )

        user.set_password(raw_password)
        user.save()
        # send_sms_code(email, code)
        das = MyTokenObtainPairSerializer()
        tokens = das.get_token(user=user)
        data = {
            "user": UserGetSerializer(user).data,
            "tokens": tokens,
            "message": "Регистрация пользователя прошла успешно."
        }
        return Response(data, status=status.HTTP_200_OK)

        
        
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key, 'is_superuser': user.is_superuser},
                        status=status.HTTP_200_OK)
        
        
class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    

class SoglashenieListView(generics.ListAPIView):
    queryset = Soglashenie.objects.all()
    serializer_class = SoglashenieSerializer
    
    
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    permission_classes = [AllowAny]
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated, IsAdminUser]
    
    