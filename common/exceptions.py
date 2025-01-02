"""
You should probably add a custom exception handler to your project based on
who consumes your APIs. To learn how to create a custom exception handler,
you can check out the Django Rest Framework documentation at:
https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling

"""

from rest_framework import status
from .response import CustomResponse as Response
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from django.utils.translation import gettext_lazy as _


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if isinstance(exc, APIException):
        response = Response(exc.detail, status_code=exc.status_code)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Bad Request')
    default_code = 'bad_request'
