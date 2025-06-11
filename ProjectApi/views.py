from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ProjectApi.models import *


class Projects(APIView):
    def get(self, request):

        try:
            projects = Project.objects.all()

            data = [
                {
                    'id': project.pk,
                    'title': project.title,
                    'description': [x for x in project.description.split('\n')],
                    'image': project.image.url,
                    'category': [cat.category_name for cat in project.category.all()],
                    'featured': project.feathered,
                    'technologies': [
                        {
                            'name': tech.name, 'icon': tech.class_name
                        } for tech in project.main_technologies.all()
                    ],

                } for project in projects
            ]

        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

