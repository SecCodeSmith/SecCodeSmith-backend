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
                    'description': project.description,
                    'image': project.image.url,
                    'category': [cat.category_name for cat in project.category.all()],
                    'featured': project.feathered,
                    'technologies': [
                        {
                            'name': tech.name, 'icon': tech.class_name
                        } for tech in project.main_technologies.all()
                    ],
                    'fullTechStack': [
                        {
                            'name': tech.name, 'icon': tech.class_name
                        } for tech in project.full_technologies.all()
                    ],
                    'github': project.github_url,
                    'demo': project.demo_url,
                    'documentation': project.documents_url,
                } for project in projects
            ]

            return Response(data, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ProjectDetail(APIView):
    def get(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)

            data = {
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
                'fullTechStack': [
                    {
                        'name': tech.name, 'icon': tech.class_name
                    } for tech in project.full_technologies.all()
                ],
                'github': project.github_url,
                'demo': project.demo_url,
                'documentation': project.documents_url,
                'project_details': {
                }
            }

        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
