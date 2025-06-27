from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from BlogApi.models import Category
from ProjectApi.models import *


class ProjectsEndpoint(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        cat = request.GET.get('cat')
        try:
            projects = Project.objects.order_by('-pk')

            if cat:
                projects = projects.filter(category__short=cat)
            projects = projects.all()

            data = [
                {
                    'id': project.pk,
                    'title': project.title,
                    'description': project.description,
                    'image': project.image.url,
                    'category': [{
                        'name': cat.category_name,
                        'short': cat.short,
                        'icon': cat.icon.class_name,
                    }for cat in project.category.all()],
                    'featured': project.feathered,
                    'technologies': [
                        {
                            'name': tech.name, 'icon': tech.icon.class_name
                        } for tech in project.main_technologies.all()
                    ],
                    'github': project.github_url,
                    'demo': project.demo_url,
                    'documentation': project.documents_url,
                    'project_details': ProjectDetail.objects.get(project=project) is not None
                } for project in projects
            ]

            return Response(data, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ProjectDetailEndpoint(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, project_id):
        try:
            project = Project.objects.get(pk=project_id)
            project_details = ProjectDetail.objects.get(project=project)

            data = {
                'id': project.pk,
                'title': project.title,
                'description': [x for x in project.description.split('\n')],
                'image': project.image.url,
                'category': [cat.category_name for cat in project.category.all()],
                'featured': project.feathered,
                'technologies': [
                    {
                        'name': tech.name, 'icon': tech.icon.class_name
                    } for tech in project.main_technologies.all()
                ],
                'github': project.github_url,
                'demo': project.demo_url,
                'documentation': project.documents_url,
                'project_details': {
                    'descriptions': project_details.full_description.split('\n'),
                    'start_date': project_details.start_date.strftime('%d/%m/%Y'),
                    'end_date': project_details.end_date.strftime('%d/%m/%Y') if project_details.end_date is not None else None,
                    'date_format': '%d/%m/%Y',
                    'role': project_details.role,
                    'client': project_details.client,
                    'key_features': [
                       feature.name for feature in KeyFeatures.objects.filter(project=project).all()
                    ],
                    'gallery': [
                       image.image.url for image in ProjectGallery.objects.filter(project=project).all()
                    ],
                    'full_tech_stack': [
                        {
                            'name': tech.name,
                            'icon': tech.icon.class_name,
                        } for tech in project_details.full_technologies.all()
                    ]
                }
            }

            return Response(data, status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ProjectCategoryEndpoint(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        try:
            cat = ProjectCategory.objects.all()
            data = [
                {
                    'name': category.category_name,
                    'short': category.short,
                    'icon': category.icon.class_name if category.icon else "",
                    'countOfProject': Project.objects.filter(category=category).count(),
                } for category in cat
            ]

            return Response(data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

