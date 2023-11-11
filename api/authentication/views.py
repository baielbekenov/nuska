from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from apps.authentication.models import Soglashenie
from api.authentication.serializers import UserSerializer, SoglashenieSerializer
User = get_user_model()


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'status': 403,
                'errors': serializer.errors,
                'message': 'Something went wrong'
            })

        if User.objects.filter(username=serializer.validated_data['username']).exists():
            return Response({
                'error': 'This user already exists!'
            }, status=409)

        user = serializer.save()
        token_obj, _ = Token.objects.get_or_create(user=user)

        return Response({
            'status': 200,
            'payload': serializer.data,
            'token': str(token_obj),
            'is_superuser': user.is_superuser,
            'message': 'Your data is saved'
        })
        
        
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
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated, IsAdminUser]
    
    