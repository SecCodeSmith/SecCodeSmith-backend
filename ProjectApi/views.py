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
                    'github': project.github_url,
                    'demo': project.demo_url,
                    'documentation': project.documents_url,
                    'project_details': project.project_details is not None,
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
                'github': project.github_url,
                'demo': project.demo_url,
                'documentation': project.documents_url,
                'project_details': {
                    'descriptions': project.project_details.full_description,
                    'start_date': project.project_details.start_date,
                    'end_date': project.project_details.end_date,
                    'date_format': '',
                    'role': project.project_details.role,
                    'status': project.project_details.status,
                    'client': project.project_details.client,
                    'key_features': [
                       feature.name for feature in KeyFeatures.objects.filter(project=project).all()
                    ],
                    'gallery': [
                       image.image.url for image in ProjectGallery.objects.filter(project=project).all()
                    ],
                    'full_tech_stack': [
                        {
                            'name': tech.name,
                            'icon': tech.class_name,
                        } for tech in project.project_details.full_technologies.all()
                    ]
                }
            }

            return Response(data, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
