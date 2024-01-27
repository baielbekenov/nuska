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
from api.authentication.utils import send_email_code_for_reset
from apps.authentication.models import Soglashenie
from rest_framework_simplejwt.tokens import RefreshToken
from api.authentication.serializers import CustomTokenObtainSerializer, UserGetSerializer, \
    UserRegisterSerializer, PasswordResetSerializer, CodeResetPasswordSerializer, ResetPasswordConfirmSerializer, \
    UserListSerializer
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
            "message": "Колдонуучуну каттоо ийгиликтүү өттү"
        }
        return Response(data, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = (AllowAny, )
    throttle_classes = [ScopedRateThrottle]
    serializer_class = PasswordResetSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                
                code = "".join([str(random.randint(1, 9)) for _ in range(0, 6)])
                user.code = urlsafe_base64_encode(force_bytes(code))
                user.last_sms_date = datetime.datetime.now(datetime.timezone.utc)
                print("code: ", code)
                user.save()
                if user.is_active:
                    send_email_code_for_reset(email, code)
                else:
                    raise ValueError('User is not confirmed!')
                    
                return Response(UserGetSerializer(user).data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'message': 'Бул электрондук почта үчүн каттоо эсеби бар болсо, сырсөздү баштапкы абалга келтирүү шилтемеси жөнөтүлөт.'},
                                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CodeResetPasswordView(APIView):
    serializer_class = CodeResetPasswordSerializer
    permission_classes = (AllowAny, )
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
            
        code = serializer.validated_data['code']
        email = serializer.validated_data['email']
        encoded = urlsafe_base64_encode(force_bytes(code))
        
        user = User.objects.filter(email=email, code=encoded)
        
        if not user.exists():
            return Response(
                {"detail": 'Сиз туура эмес код киргиздиңиз.'}, status=status.HTTP_404_NOT_FOUND
            )
        user = user.first()
        user.is_active = True
        user.save()
        
        token = MyTokenObtainPairSerializer()
        tokens = token.get_token(user=user)
        data = {
            "tokens": tokens,
            "message": "Код иштетилди"
        }

        return Response(
            data,
            status=status.HTTP_200_OK,
        )
        

class ResetPasswordConfirmView(APIView):
    serializer_class = ResetPasswordConfirmSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']

            # Использование токена для идентификации пользователя
            user = request.user
            if not user:
                return Response({"detail": "Туура эмес токен"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({"detail": "Сырсөз ийгиликтүү өзгөртүлдү"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )
    
    
                
    
    