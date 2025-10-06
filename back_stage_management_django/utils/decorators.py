from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
import traceback

def atomic_view(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                return func(self, request, *args, **kwargs)
        except Exception as e:
            print("事务回滚异常：", traceback.format_exc())
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper
