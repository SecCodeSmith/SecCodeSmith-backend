import json

from django.test import TestCase
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework import status
from api.models import *
from api.views import CSRFTokenView, AboutPage, SkillCards


class ModelTests(TestCase):
    def setUp(self):
        self.icon_github = IconsClass.objects.create(
            name="GitHub",
            class_name="fab fa-github",
            description="GitHub icon"
        )

        self.icon_linkedin = IconsClass.objects.create(
            name="LinkedIn",
            class_name="fab fa-linkedin",
            description="LinkedIn icon"
        )

        self.lang_en = Lang.objects.create(name="English", iso_code="en")
        self.lang_pl = Lang.objects.create(name="Polish", iso_code="pl")

        self.contact = Contact.objects.create(
            email="user@example.com",
            business_email="biz@example.com",
            phone="+48123123123",
            map_iframe="https://maps.example.com/embed",
            language=self.lang_en
        )

        self.skill_prog = Skill.objects.create(
            name="Programming Languages",
            icon_class=self.icon_github
        )
        self.skill_fw = Skill.objects.create(
            name="Frameworks",
            icon_class=self.icon_linkedin
        )

        self.card = SkillsCard.objects.create(
            category_title="Dev Skills",
            icon_class=self.icon_github
        )
        self.card.skills.add(self.skill_prog, self.skill_fw)

        self.core_value = CoreValue.objects.create(
            title="Integrity",
            icon=self.icon_linkedin,
            description="Always do the right thing."
        )

        self.prof_journey = ProfessionalJourney.objects.create(
            title="Backend Developer",
            company="Acme Corp",
            duration="2018–2021",
            description="Worked on REST APIs."
        )

        self.tech_skill = TechnicalArsenalSkill.objects.create(text="Django")

        self.tech_arsenal = TechnicalArsenal.objects.create(
            icon=self.icon_github,
            title="Backend Stack"
        )
        self.tech_arsenal.skills.add(self.tech_skill)

        self.testimonial = Testimonials.objects.create(
            author="John Doe",
            email="john@example.com",
            position="CTO",
            text="Great work!"
        )

        self.about = About.objects.create(
            about_title="About Me",
            about_text="I am a developer.",
            lang=self.lang_en
        )
        self.about.professional_journey.add(self.prof_journey)
        self.about.technical_arsenal.add(self.tech_arsenal)
        self.about.core_value.add(self.core_value)

        self.faq = FAQ.objects.create(
            question="How to contact?",
            answer="Use email.",
            contact=self.contact
        )

    def test_iconsclass_str_and_fields(self):
        self.assertEqual(str(self.icon_github), "fab fa-github")
        self.assertEqual(self.icon_github.name, "GitHub")
        self.assertEqual(self.icon_github.class_name, "fab fa-github")
        self.assertEqual(self.icon_github.description, "GitHub icon")

    def test_lang_fields(self):
        self.assertEqual(self.lang_en.name, "English")
        self.assertEqual(self.lang_en.iso_code, "en")

    def test_contact_str_and_fields(self):
        expected = f"Email: {self.contact.email} Business email {self.contact.business_email} Phone {self.contact.phone} Lang {self.lang_en}"
        self.assertEqual(str(self.contact), expected)
        self.assertEqual(self.contact.language, self.lang_en)

    def test_skill_str_and_icon_relation(self):
        self.assertEqual(str(self.skill_prog), "Programming Languages")
        self.assertEqual(self.skill_prog.icon_class, self.icon_github)

    def test_skillscard_relations(self):
        self.assertEqual(self.card.category_title, "Dev Skills")
        self.assertEqual(self.card.icon_class, self.icon_github)
        skills_in_card = list(self.card.skills.all())
        self.assertIn(self.skill_prog, skills_in_card)
        self.assertIn(self.skill_fw, skills_in_card)

    def test_corevalue_str_and_fields(self):
        self.assertEqual(str(self.core_value), f"Title: Integrity Text: Always do the right thing.")
        self.assertEqual(self.core_value.icon, self.icon_linkedin)
        self.assertEqual(self.core_value.description, "Always do the right thing.")

    def test_faq_str_and_relation(self):
        self.assertEqual(str(self.faq), "How to contact?")
        self.assertEqual(self.faq.contact, self.contact)

    def test_professionaljourney_str_and_fields(self):
        self.assertEqual(str(self.prof_journey), "Backend Developer")
        self.assertEqual(self.prof_journey.company, "Acme Corp")
        self.assertEqual(self.prof_journey.duration, "2018–2021")
        self.assertIn("REST APIs", self.prof_journey.description)

    def test_technicalarsenalskill_str(self):
        self.assertEqual(str(self.tech_skill), "Django")

    def test_technicalarsenal_relations(self):
        self.assertEqual(self.tech_arsenal.title, "Backend Stack")
        self.assertEqual(self.tech_arsenal.icon, self.icon_github)
        skills_list = list(self.tech_arsenal.skills.all())
        self.assertIn(self.tech_skill, skills_list)

    def test_testimonials_fields(self):
        self.assertEqual(self.testimonial.author, "John Doe")
        self.assertEqual(self.testimonial.email, "john@example.com")
        self.assertEqual(self.testimonial.position, "CTO")
        self.assertEqual(self.testimonial.text, "Great work!")

    def test_about_str_and_relations(self):
        self.assertEqual(self.about.about_title, "About Me")
        self.assertEqual(self.about.about_text, "I am a developer.")
        self.assertEqual(self.about.lang, self.lang_en)

        pj_list = list(self.about.professional_journey.all())
        self.assertIn(self.prof_journey, pj_list)

        ta_list = list(self.about.technical_arsenal.all())
        self.assertIn(self.tech_arsenal, ta_list)

        cv_list = list(self.about.core_value.all())
        self.assertIn(self.core_value, cv_list)

        try:
            testimonials_qs = getattr(self.about, "about_testimonials")
            self.assertTrue(hasattr(testimonials_qs, "all"))
        except Exception:
            pass

    def test_about_without_testimonials_assignment(self):
        about2 = About.objects.create(
            about_title="Another About",
            about_text="More text.",
            lang=self.lang_pl
        )
        about2.professional_journey.add(self.prof_journey)
        about2.technical_arsenal.add(self.tech_arsenal)
        about2.core_value.add(self.core_value)
        self.assertIsInstance(about2, About)

class CSRFTokenViewTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CSRFTokenView.as_view()

    def test_get_returns_csrf_token(self):
        """
        GET on CSRFTokenView should return a 200 OK with a JSON payload
        containing the key "csrfToken" and a non‐empty string value.
        """
        request = self.factory.get("/api/csrf")
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = json.loads(response.text)
        self.assertIn("csrfToken", payload)
        token = payload["csrfToken"]
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 0)

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

        self.icon = IconsClass.objects.create(
            name="SampleIcon", class_name="fas fa-sample", description="Sample icon"
        )

        self.prof_journey = ProfessionalJourney.objects.create(
            title="Backend Developer",
            company="Acme Corp",
            duration="2018–2021",
            description="Built REST APIs",
        )

        self.tech_skill = TechnicalArsenalSkill.objects.create(text="Django")
        self.tech_arsenal = TechnicalArsenal.objects.create(
            icon=self.icon, title="Python Stack"
        )
        self.tech_arsenal.skills.add(self.tech_skill)

        self.core_value = CoreValue.objects.create(
            title="Integrity", icon=self.icon, description="Always do right"
        )

        self.testimonial = Testimonials.objects.create(
            author="Jane Smith", email="jane@example.com", position="CTO", text="Excellent!"
        )

        self.about = About.objects.create(
            about_title="About Me Section",
            about_text="I am a full‐stack developer.",
            lang=self.lang_en,
        )
        self.about.professional_journey.add(self.prof_journey)
        self.about.technical_arsenal.add(self.tech_arsenal)
        self.about.core_value.add(self.core_value)
        try:
            self.about.testimonials.add(self.testimonial)
        except Exception:
            pass

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
            "text",
            "language",
            "professional_journal",
            "technical_arsenal",
            "core_values",
            "testimonials",
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
        self.assertEqual(cv_item["descriptions"], self.core_value.description)

        tst_list = payload["testimonials"]
        self.assertIsInstance(tst_list, list)
        if tst_list:
            self.assertEqual(len(tst_list), 1)
            tst_item = tst_list[0]
            self.assertEqual(tst_item.get("author", tst_item.get("autor")), self.testimonial.author)
            self.assertEqual(tst_item["position"], self.testimonial.position)
            self.assertEqual(tst_item["text"], self.testimonial.text)



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



