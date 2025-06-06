from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.templatetags.i18n import language
from rest_framework import permissions, status
from rest_framework.views import APIView

from .models import *


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

        if not card:
            return JsonResponse({'error': 'No card found'}, status=status.HTTP_404_NOT_FOUND)

        data = [
            {
                'categoryTitle': card.category_title,
                'categoryIcon': card.icon_class.class_name,
                'skills': [{
                    'name': skill.name,
                    'icon': skill.icon_class.class_name,
                } for skill in card.skills.all()]
            }
            for card in card
        ]

        return JsonResponse(data, safe=False,status=status.HTTP_200_OK)

class AboutPage(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, lang = None):
        """
        Returns an About section of the website in specified language.
        """
        lang = Lang.objects.get(iso_code=lang) or Lang.objects.first()

        about = About.objects.get(lang=lang)

        if not about:
            return JsonResponse({'error': 'About in lang {} not found'.format(lang.name)}
                                , status=status.HTTP_404_NOT_FOUND)

        data = {
            'title': about.about_title,
            'text': about.about_text,
            'language': lang.name or "",
            'professional_journal': [
                {
                    'title': item.title,
                    'description': item.description,
                    'duration': item.duration
                } for item in about.professional_journey.all()
            ],
            'technical_arsenal': [
                {
                    'icon': item.icon.class_name,
                    'title': item.title,
                    'skills': [
                       skill.text for skill in item.skills.all()
                    ]
                } for item in about.technical_arsenal.all()
            ],
            'core_values': [
                {
                    'title': value.title,
                    'icon': value.icon.class_name,
                    'descriptions': value.description,
                } for value in about.core_value.all()
            ],
            'testimonials': [
                {
                    'autor': testimonial.autor,
                    'position': testimonial.position,
                    'text': testimonial.text,
                } for testimonial in about.testimonials.all()
            ]
        }

        return JsonResponse(data, safe=False,status=status.HTTP_200_OK)
