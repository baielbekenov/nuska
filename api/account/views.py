from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from api.account.serializers import UserAccountSerializer, ChangePasswordSerializer, ConfirmUserEmailSerializer, \
    ActivateUserEmailSerializer
import datetime
import random
from django.utils.encoding import force_bytes
from django.utils.translation import gettext as _
from api.account.utils import send_code_email_confirm
from api.authentication.serializers import UserGetSerializer

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


class ConfirmUserEmailView(APIView):
    serializer_class = ConfirmUserEmailSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        code = "".join([str(random.randint(1, 9)) for _ in range(0, 6)])
        user.code = urlsafe_base64_encode(force_bytes(code))
        user.last_sms_date = datetime.datetime.now(datetime.timezone.utc)
        user.save()

        send_code_email_confirm(user.email, code)

        return Response({'message': _('Код отправлен на ваш email.')}, status=status.HTTP_200_OK)


class SendCodeAgainView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = request.user
        code = "".join([str(random.randint(1, 9)) for _ in range(0, 6)])
        user.code = urlsafe_base64_encode(force_bytes(code))
        user.last_sms_date = datetime.datetime.now(datetime.timezone.utc)
        user.save()

        send_code_email_confirm(user.email, code)
        return Response({"message": _("Код отправлен на ваш email.")}, status=status.HTTP_200_OK)


class ActivateEmailUserView(APIView):
    serializer_class = ActivateUserEmailSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        code = serializer.validated_data.get("code")
        encoded = urlsafe_base64_encode(force_bytes(code))

        if not encoded == user.code:
            return Response(
                {"detail": _("Вы ввели неверный код.")}, status=status.HTTP_404_NOT_FOUND
            )

        user.is_confirm = True
        user.save()

        return Response(
            {"detail": _("Email подтвержден!.")},
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Пароль успешно изменен!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMeApiView(APIView):
    """Позволяет пользователю получить информацию о себе"""
    serializer_class = UserGetSerializer

    def get(self, request):
        user = self.request.user

        return Response(
            {
                "user": UserGetSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )