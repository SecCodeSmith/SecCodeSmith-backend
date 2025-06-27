import json
from datetime import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework import status
from api.models import *
from api.views import CSRFTokenView, AboutPage, SkillCards, SocialLinksFooter

class SkillCardsViewTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = SkillCards.as_view()
        self.url = "/api/skills-cards"

        self.icon1 = IconsClass.objects.create(
            name="GitHub", class_name="fab fa-github", description="GitHub icon"
        )
        self.icon2 = IconsClass.objects.create(
            name="LinkedIn", class_name="fab fa-linkedin", description="LinkedIn icon"
        )

        self.skill_a = Skill.objects.create(name="Python", icon_class=self.icon1)
        self.skill_b = Skill.objects.create(name="Django", icon_class=self.icon2)

    def test_get_when_no_cards_returns_404(self):
        """
        If there are no SkillsCard records in the DB, GET should return 404
        with JSON {'error': 'No card found'}.
        """
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        payload = json.loads(response.text)
        self.assertEqual(payload, {"error": "No card found"})

    def test_get_returns_all_cards_structure(self):
        """
        When at least one SkillsCard exists, GET should return 200 OK with a JSON list.
        Each element must contain:
          - 'categoryTitle': SkillsCard.category_title
          - 'categoryIcon': SkillsCard.icon_class.class_name
          - 'skills': a list of dicts, each having {'name': <Skill.name>, 'icon': <Skill.icon_class.class_name>}
        """
        # Create a SkillsCard and associate both skills
        card = SkillsCard.objects.create(
            category_title="Dev Tools", icon_class=self.icon1
        )
        card.skills.add(self.skill_a, self.skill_b)

        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = json.loads(response.text)
        self.assertIsInstance(payload, list)
        self.assertEqual(len(payload), 1)

        card_data = payload[0]
        # Verify structure of the single card
        self.assertEqual(card_data["categoryTitle"], "Dev Tools")
        self.assertEqual(card_data["categoryIcon"], self.icon1.class_name)

        skills_list = card_data["skills"]
        self.assertIsInstance(skills_list, list)
        self.assertEqual(len(skills_list), 2)

        returned_pairs = {(s["name"], s["icon"]) for s in skills_list}
        expected_pairs = {
            (self.skill_a.name, self.skill_a.icon_class.class_name),
            (self.skill_b.name, self.skill_b.icon_class.class_name),
        }
        self.assertEqual(returned_pairs, expected_pairs)


class AboutPageViewTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AboutPage.as_view()
        self.url = "/api/about"
        self.lang_en = Lang.objects.create(name="English", iso_code="en")

        self.contact = Contact.objects.create(
            email="user@example.com",
            business_email="biz@example.com",
            phone="+48123123123",
            map_iframe="https://maps.example.com/embed",
            language=self.lang_en,
        )

        self.sample_file = SimpleUploadedFile(
            name='test.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )

        self.icon = IconsClass.objects.create(
            name="SampleIcon", class_name="fas fa-sample", description="Sample icon"
        )

        self.about = About.objects.create(
            about_title="About Me Section",
            about_text="I am a full‐stack developer.",
            lang=self.lang_en,
            image=self.sample_file,
        )

        self.testimonial = Testimonials.objects.create(
            author="Jane Smith", email="jane@example.com", position="CTO", text="Excellent!", about=self.about
        )

        self.tech_arsenal = TechnicalArsenal.objects.create(
            icon=self.icon, title="Python Stack", about=self.about
        )

        self.prof_journey = ProfessionalJourney.objects.create(
            title="Backend Developer",
            company="Acme Corp",
            start_date=datetime.strptime("01-2018", "%m-%Y"),
            end_date=datetime.strptime("01-2021", "%m-%Y"),
            description="Built REST APIs",
            about=self.about,
        )

        self.tech_skill = TechnicalArsenalSkill.objects.create(
            text="Django",
            technical_arsenal=self.tech_arsenal
        )
        self.core_value = CoreValue.objects.create(
            about=self.about,
            title="Integrity",
            icon=self.icon,
            description="Always do right"
        )
        try:
            self.about.testimonials.add(self.testimonial)
        except Exception:
            pass

    def tearDown(self):
        self.about.image.delete(save=False)
        super(APITestCase, self).tearDown()

    def test_get_when_no_about_returns_404(self):
        """
        If there is no About matching the requested language, the view should return 404
        and the JSON {'error': 'About in lang <lang_name> not found'}.
        """

        About.objects.all().delete()

        request = self.factory.get(self.url)

        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        payload = json.loads(response.text)
        self.assertIn("error", payload)
        self.assertEqual(
            payload["error"],
            f"About in lang {self.lang_en.name} not found"
        )

    def test_get_returns_about_structure(self):
        """
        When an About matching the requested language exists, GET should return 200 OK
        with a JSON payload containing the keys:
          - 'title'
          - 'text'
          - 'language'
          - 'professional_journal' (list of dicts with keys 'title', 'description', 'duration')
          - 'technical_arsenal' (list of dicts with keys 'icon', 'title', 'skills')
          - 'core_values' (list of dicts with keys 'title', 'icon', 'descriptions')
          - 'testimonials' (list of dicts with keys 'author', 'position', 'text')
        """

        request = self.factory.get(self.url)

        response = self.view(request, self.lang_en.iso_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = json.loads(response.text)
        expected_top_keys = {
            "title",
            "subtitle",
            "image",
            "image_title",
            "text",
            "language",
            "professional_journal",
            "professional_journal_title",
            "technical_arsenal",
            "technical_arsenal_title",
            "core_values_title",
            "core_values",
            "testimonials_title",
            "testimonials",
            "about_social_links",
        }
        self.assertEqual(set(payload.keys()), expected_top_keys)

        self.assertEqual(payload["title"], self.about.about_title)
        self.assertEqual(payload["text"], self.about.about_text)
        self.assertEqual(payload["language"], self.lang_en.name)

        prof_list = payload["professional_journal"]
        self.assertIsInstance(prof_list, list)
        self.assertEqual(len(prof_list), 1)
        prof_item = prof_list[0]
        self.assertEqual(prof_item["title"], self.prof_journey.title)
        self.assertEqual(prof_item["description"], self.prof_journey.description)
        self.assertEqual(prof_item["duration"], self.prof_journey.duration)

        ta_list = payload["technical_arsenal"]
        self.assertIsInstance(ta_list, list)
        self.assertEqual(len(ta_list), 1)
        ta_item = ta_list[0]
        self.assertEqual(ta_item["icon"], self.tech_arsenal.icon.class_name)
        self.assertEqual(ta_item["title"], self.tech_arsenal.title)
        skills_texts = ta_item["skills"]
        self.assertIsInstance(skills_texts, list)
        self.assertIn(self.tech_skill.text, skills_texts)

        cv_list = payload["core_values"]
        self.assertIsInstance(cv_list, list)
        self.assertEqual(len(cv_list), 1)
        cv_item = cv_list[0]
        self.assertEqual(cv_item["title"], self.core_value.title)
        self.assertEqual(cv_item["icon"], self.core_value.icon.class_name)
        self.assertEqual(cv_item["description"], self.core_value.description)

        tst_list = payload["testimonials"]
        self.assertIsInstance(tst_list, list)
        if tst_list:
            self.assertEqual(len(tst_list), 1)
            tst_item = tst_list[0]
            self.assertEqual(tst_item.get("author", tst_item.get("autor")), self.testimonial.author)
            self.assertEqual(tst_item["position"], self.testimonial.position)
            self.assertEqual(tst_item["text"], self.testimonial.text)


class FooterLinksViewTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = SocialLinksFooter.as_view()
        self.url = '/api/footer-links/'
        self.icon_LinkedIn = IconsClass.objects.create(
            class_name="LinkedIn",
            name="LinkedIn",
        )

        self.icon_github = IconsClass.objects.create(
            class_name="Github",
            name="Github",
        )

        self.link_1 = SocialLinks.objects.create(
            name="LinkedIn",
            url="https://www.linkedin.com/in/linkedin/",
            icon_class=self.icon_LinkedIn,
            footer=True,
            contact_pages=False,
            about_pages=False,
        )

        self.link_2 = SocialLinks.objects.create(
            name="Github",
            url="https://www.github.com",
            footer=False,
            contact_pages=False,
            about_pages=False,
        )

    def test_footer_links(self):
        request = self.factory.get(self.url)

        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = json.loads(response.text)

        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["icon"], self.link_1.icon_class.class_name)
        self.assertEqual(payload[0]["url"], self.link_1.url)


class APITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.icon = IconsClass.objects.create(class_name="fas fa-tools")
        self.skill = Skill.objects.create(name="JavaScript", icon_class=self.icon)
        self.card = SkillsCard.objects.create(category_title="Frontend", icon_class=self.icon)
        self.card.skills.add(self.skill)

    def test_csrf_token_view(self):
        response = self.client.get("/api/csrf")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("csrfToken", response.json())

    def test_skill_cards_view(self):
        response = self.client.get("/api/skills-cards")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["categoryTitle"], "Frontend")
        self.assertEqual(data[0]["skills"][0]["name"], "JavaScript")

class TestMessagesViewTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = reverse("contact")

    def test_messages_view(self):
        data = {
            'name': 'Jon Wick',
            'email': 'jon@example.pl',
            'subject': 'Hello World!',
            'projectType': 'Hotel continental',
            'message': 'One coin',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
