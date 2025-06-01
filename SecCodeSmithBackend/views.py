import json

from django.contrib.auth import login as log, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from SecCodeSmithBackend.data.skills_lists import SkillList
from SecCodeSmithBackend.data.projects import Project

class CSRFTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        Returns the CSRF token for the current session.
        """
        csrf_token = get_token(request)
        return JsonResponse({'csrfToken': csrf_token}, status=status.HTTP_200_OK)

class GetSkillListsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        Returns all skill lists.
        """
        skill_lists = SkillList.objects.all()
        data = [
            {
                'id': skill_list.id,
                'name': skill_list.list_name,
                'className': skill_list.class_name,
                'skills': [skill.name for skill in skill_list.list_of_skills.all()]
            }
            for skill_list in skill_lists
        ]
        return JsonResponse(data, safe=False, status=status.HTTP_200_OK)