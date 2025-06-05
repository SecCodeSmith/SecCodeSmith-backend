from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from api.models import *

class ModelTests(TestCase):

    def test_skill_creation(self):
        icon = IconsClass.objects.create(class_name="fas fa-code")
        skill = Skill.objects.create(name="Python", icon_class=icon)
        self.assertEqual(str(skill), "Python")
        self.assertEqual(skill.icon_class, icon)

    def test_skills_card_creation(self):
        icon = IconsClass.objects.create(class_name="fas fa-cogs")
        skill = Skill.objects.create(name="Django", icon_class=icon)
        card = SkillsCard.objects.create(category_title="Backend", icon_class=icon)
        card.skills.add(skill)

        self.assertEqual(card.category_title, "Backend")
        self.assertIn(skill, card.skills.all())


class APITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.icon = IconsClass.objects.create(class_name="fas fa-tools")
        self.skill = Skill.objects.create(name="JavaScript", icon_class=self.icon)
        self.card = SkillsCard.objects.create(category_title="Frontend", icon_class=self.icon)
        self.card.skills.add(self.skill)

    def test_csrf_token_view(self):
        response = self.client.get("/csrf-token/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("csrfToken", response.json())

    def test_skill_cards_view(self):
        response = self.client.get("/skills/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["categoryTitle"], "Frontend")
        self.assertEqual(data[0]["skills"][0]["name"], "JavaScript")



