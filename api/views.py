from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework import permissions, status
from rest_framework.views import APIView

from .models import SkillsCard, IconsClass, Skill


class CSRFTokenView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        """
        Returns the CSRF token for the current session.
        """
        csrf_token = get_token(request)
        return JsonResponse({'csrfToken': csrf_token}, status=status.HTTP_200_OK)

class SkillCards(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        """
        Returns a list of all available skills card.
        """

        card = SkillsCard.objects.all()

        data = [
            {
                'categoryTitle': card.category_title,
                'categoryIcon': IconsClass.objects.get(pk=card.icon_class).class_name,
                'skills': [{
                    'name': skill.name,
                    'icon': skill.icon_class,
                } for skill in Skill.objects.filter(SkillsCard=card)]
            }
            for card in card
        ]

        return JsonResponse(data, safe=False,status=status.HTTP_200_OK)
