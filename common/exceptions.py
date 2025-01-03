"""
You should probably add a custom exception handler to your project based on
who consumes your APIs. To learn how to create a custom exception handler,
you can check out the Django Rest Framework documentation at:
https://www.django-rest-framework.org/api-guide/exceptions/#custom-exception-handling
"""


from rest_framework import status
from rest_framework.views import exception_handler
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException, ValidationError


# Extract error messages into a structured list of dictionaries
def extract_messages(detail):
    errors = []
    if isinstance(detail, list):  # Handle lists of errors
        for item in detail:
            errors.extend(extract_messages(item))
    elif isinstance(detail, dict):  # Handle nested dictionaries
        for field, messages in detail.items():
            if isinstance(messages, list):
                for message in messages:
                    errors.append({field: message})
            else:
                errors.append({field: str(messages)})
    else:
        errors.append({"non_field_error": str(detail)})
    return errors


def get_summary_message(detail):
    if isinstance(detail, list):
        return get_summary_message(detail[0])
    elif isinstance(detail, dict):
        if "messages" in detail:
            return get_summary_message(detail.get('messages'))
        elif "detail" in detail:
            return get_summary_message(detail.get('detail'))
        
        return detail.get('message', str(detail))
    return str(detail)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        errors = []
        if isinstance(exc, ValidationError):
            # Extract detailed error messages for ValidationError
            errors = extract_messages(exc.detail)
            summary_message = "Validation Error"
        elif isinstance(exc, APIException):
            errors = extract_messages(exc.detail)
            summary_message = get_summary_message(exc.detail)

        # Customize the response structure
        response.data = {
            "message": summary_message,  # Summary of the error
            "errors": errors,            # Detailed field-level errors
            "status_code": response.status_code,
            "data": None
        }

    return response


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Bad Request')
    default_code = 'bad_request'
