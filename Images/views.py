from django.http import JsonResponse
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Image


class ImageProps(APIView):

    permission_classes = (permissions.AllowAny,)
    def get(self, request, name=None):
        if not name:
            return Response({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
        data = {}
        try:
            image = Image.objects.get(name=name)

            data = {
                'image': image.image.url,
                'name': image.name,
                'alt': image.alt
            }

        except Image.DoesNotExist:
            return JsonResponse({'error': 'Image not found'} ,status=status.HTTP_404_NOT_FOUND)
        except Image.MultipleObjectsReturned:
            return JsonResponse({'error': 'Problem with database'} ,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': e} ,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            return Response(data, status=status.HTTP_200_OK)