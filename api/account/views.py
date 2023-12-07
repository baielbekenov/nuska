from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from api.account.serializers import UserAccountSerializer, ChangePasswordSerializer

User = get_user_model()


class UserAccountUpdateView(APIView):
    serializer_class = UserAccountSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        user = request.user
        if user is None:
            return Response({'error': 'Пользователь не найден!'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(user, context={'request': request})
        return Response(serializer.data)

    def put(self, request, format=None):
        user = request.user
        if user is None:
            return Response({"error": "Пользователь не найден!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        user = request.user
        if user is None:
            return Response({"error": "Пользователь не найден!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Пароль успешно изменен!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)