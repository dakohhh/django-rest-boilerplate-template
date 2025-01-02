from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated


class CustomResponse(Response):
    """
    A custom response class for Django REST Framework that adds a `status_code`
    attribute to the response data.
    """

    def __init__(self, message: str, data=None, status_code: int = status.HTTP_200_OK, **kwargs):
        data = {"message": message, "data": data, "status_code": status_code}
        super().__init__(data, status=status_code, **kwargs)
