from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .tasks import send_mail_task

User = get_user_model()


class EmailView(APIView):
    def post(self, request):
        email_list = request.data.getlist('email')
        subject = request.data['subject']
        message = request.data['message']
        # https://support.google.com/accounts/answer/6010255
        for email in email_list:
            send_mail_task.delay(
                subject,
                message,
                email,
            )
        return Response(status=status.HTTP_200_OK)