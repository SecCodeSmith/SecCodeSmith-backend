from django.http import JsonResponse
from django.middleware.csrf import get_token
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

    def get(self, request, lang_arg = None):
        """
        Returns an About section of the website in specified language.
        """

        try:
            lang = Lang.objects.get(iso_code=lang_arg)
        except Lang.DoesNotExist:
            lang = Lang.objects.first()

        try:
            about = About.objects.get(lang=lang)
        except About.DoesNotExist:
            return JsonResponse({'error': 'About in lang {} not found'.format(lang.name or lang_arg)}
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
                    'author': testimonial.author,
                    'position': testimonial.position,
                    'text': testimonial.text,
                } for testimonial in about.testimonials.all()
            ],
            'about_social_links': [
                {
                    'icon': link.icon_class.class_name,
                    'title': link.name,
                    'url': link.url
                } for link in SocialLinks.objects
                .filter(about_pages=True).all()
            ]
        }

        return JsonResponse(data, safe=False,status=status.HTTP_200_OK)

class SocialLinksFooter(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        socials = SocialLinks.objects.filter(footer=True).all()

        if not socials or len(socials) == 0:
            return JsonResponse({'error': 'No social links found'}, status=status.HTTP_404_NOT_FOUND)

        data = [
            {
                'icon': social.icon_class.class_name,
                'url': social.url
            } for social in socials
        ]

        return JsonResponse(data, safe=False,status=status.HTTP_200_OK)

class ContactPage(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, lang_arg = None):
        try:
            lang = Lang.objects.get(iso_code=lang_arg)
        except Lang.DoesNotExist:
            lang = Lang.objects.first()

        try:
            contact = Contact.objects.get(language=lang)
            socials = SocialLinks.objects.filter(contact_pages=True).all()
            faq = FAQ.objects.filter(contact=contact).all()

            data = {
                'email': contact.email,
                'business_email': contact.business_email,
                'map_iframe_url': contact.map_iframe,
                'phone': contact.phone,
                'social_links': [
                    {
                        'platform': link.name,
                        'url': link.url,
                        'icon': link.icon_class.class_name,
                    } for link in socials
                ],
                'FAQ': [
                    {
                        'question': element.question,
                        'answer': element.answer
                    } for element in faq
                ]
            }

            return JsonResponse(data, safe=False,status=status.HTTP_200_OK)
        except Contact.DoesNotExist:
            return JsonResponse({'error': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)
