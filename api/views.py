from sqlite3 import IntegrityError

from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
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

    @method_decorator(cache_page(60))
    def get(self, request):
        """
        Returns a list of all available skills card.
        """

        try:
            card = SkillsCard.objects.all()
        except SkillsCard.DoesNotExist:
            return JsonResponse({'error': 'No skills found'}, status=status.HTTP_404_NOT_FOUND)


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

    @method_decorator(cache_page(60))
    def get(self, request, lang_arg = None):
        """
        Returns an About section of the website in specified language.
        """

        try:
            try:
                lang = Lang.objects.get(iso_code=lang_arg)
            except Lang.DoesNotExist:
                try:
                    lang = Lang.objects.first()
                except Lang.DoesNotExist:
                    return JsonResponse({'error': 'Database is empty'}
                                        , status=status.HTTP_404_NOT_FOUND)
            if lang is None:
                return JsonResponse({'error': 'Language not found'}, status=status.HTTP_404_NOT_FOUND)

            about = About.objects.get(lang=lang)

            if about is None:
                return JsonResponse({'error': 'Language not found'}, status=status.HTTP_404_NOT_FOUND)

            professional_journey = (ProfessionalJourney.objects.filter(about=about)
                                    .order_by('-end_date', '-start_date')
                                    .all())
            technical_arsenal = TechnicalArsenal.objects.filter(about=about).all()
            core_value = CoreValue.objects.filter(about=about).all()
            testimonials = Testimonials.objects.filter(about=about).all()
        except About.DoesNotExist:
            return JsonResponse({'error': 'About in lang {} not found'.format(lang.name or lang_arg)}
                                , status=status.HTTP_404_NOT_FOUND)

        data = {
            'title': about.about_title,
            'subtitle': about.sub_title,
            'text': about.about_text,
            'language': lang.name or "",
            'image': about.image.url,
            'image_title': about.image_title,
            'professional_journal_title': about.professional_journal_title,
            'professional_journal': [
                {
                    'title': item.title,
                    'description': item.description,
                    'company': item.company,
                    'duration': item.duration
                } for item in professional_journey
            ],
            'technical_arsenal_title': about.technical_arsenal_title,
            'technical_arsenal': [
                {
                    'icon': item.icon.class_name,
                    'title': item.title,
                    'skills': [
                       skill.text for skill in TechnicalArsenalSkill.objects.filter(technical_arsenal=item).all()
                    ]
                } for item in technical_arsenal
            ],
            'core_values_title': about.core_value_title,
            'core_values': [
                {
                    'title': value.title,
                    'icon': value.icon.class_name,
                    'description': value.description,
                } for value in core_value
            ],
            'testimonials_title': about.testimonials_title,
            'testimonials': [
                {
                    'author': testimonial.author,
                    'position': testimonial.position,
                    'text': testimonial.text,
                } for testimonial in testimonials
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

    @method_decorator(cache_page(60))
    def get(self, request):
        try:
            socials = SocialLinks.objects.filter(footer=True).all()

            if not socials or len(socials) == 0:
                return JsonResponse({'error': 'No social links found'}, status=status.HTTP_404_NOT_FOUND)

            data = [
                {
                    'icon': social.icon_class.class_name,
                    'url': social.url
                } for social in socials
            ]

            return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
        except SocialLinks.DoesNotExist:
            return JsonResponse({'error': 'No social links found'}, status=status.HTTP_404_NOT_FOUND)

class ContactPage(APIView):
    permission_classes = (permissions.AllowAny,)

    @method_decorator(cache_page(60))
    def get(self, request, lang_arg = None):
        try:
            try:
                lang = Lang.objects.get(iso_code=lang_arg)
            except Lang.DoesNotExist:
                lang = Lang.objects.first()

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

class ContactFormEndpoint(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        subject = request.data.get('subject')
        project_type = request.data.get('projectType')
        message = request.data.get('message')
        budget = request.data.get('budget')

        if not all([name, email, message]):
            return JsonResponse(
                {'error': 'Name, email, and message are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            Message.objects.create(
                name=name,
                email=email,
                subject=subject,
                project_type=project_type,
                message=message,
                budget=budget,
            ).save()

            contact = Contact.objects.first()
            if contact:
                admin_emails = []
                if contact.email:
                    admin_emails.append(contact.email)
                if contact.business_email:
                    admin_emails.append(contact.business_email)

                if admin_emails:
                    admin_subject = 'New message from your portfolio contact form'
                    admin_message = f"""
                    You have a new message from {name} ({email}).
                    Subject: {subject}
                    Project Type: {project_type}
                    Budget: {budget}
                    Message:
                    {message}
                    """
                    send_mail(
                        subject=admin_subject,
                        message=admin_message,
                        from_email=None,  # Use default from settings
                        recipient_list=admin_emails,
                        fail_silently=False,
                    )

            # Send confirmation email to the user
            user_subject = 'Thank you for your message'
            user_message = f"""
            Hi {name},

            Thank you for contacting me. I have received your message and will get back to you shortly.

            Best regards,
            SecCodeSmith
            """
            send_mail(
                subject=user_subject,
                message=user_message,
                from_email=None, # Use default from settings
                recipient_list=[email],
                fail_silently=False,
            )

            return JsonResponse({'message': 'Message created'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return JsonResponse({'message' : 'Bad request'} ,status=status.HTTP_400_BAD_REQUEST)

