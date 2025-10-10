import json
from datetime import datetime, timedelta
from unittest.mock import patch

import fakeredis
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from BlogApi.models import Author, Category, Comment, Post, Tag
from BlogApi.untils import filter_posts
from Images.models import Image


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    },
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
)
class AuthorModelTests(TestCase):
    def test_author_str(self):
        author = Author.objects.create(name="Jane Doe", email="jane@example.com", bio="Just a test author.")
        self.assertEqual(str(author), "Jane Doe")

        author.avatar.delete(save=False)

    def test_author_fields(self):
        author = Author.objects.create(name="John Smith", email="john@example.com", bio="")
        self.assertEqual(author.name, "John Smith", msg="Author name should be correct")
        self.assertEqual(author.email, "john@example.com", msg="Author email should be correct")
        self.assertEqual(author.bio, "", msg="Author bio should be correct")

        author.avatar.delete(save=False)


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    },
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
)
class CategoryModelTests(TestCase):
    def test_category_str_and_slug_auto_generation(self):
        title = "Test Category"
        category = Category.objects.create(title=title)
        # __str__ should return the title
        self.assertEqual(str(category), title)

        # Slug should be auto-generated from title
        expected_slug = slugify(title)
        self.assertEqual(category.slug, expected_slug)

    def test_category_slug_uniqueness(self):
        title = "Another Category"
        c1 = Category.objects.create(title=title)
        # Creating a second category with same title should raise IntegrityError on slug
        with self.assertRaises(Exception):
            Category.objects.create(title=title)


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    },
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
)
class TagModelTests(TestCase):
    def test_tag_str_and_slug_auto_generation(self):
        name = "Django Test"
        tag = Tag.objects.create(name=name)
        # __str__ should return the name
        self.assertEqual(str(tag), name)

        # Slug should be auto-generated from name
        expected_slug = slugify(name)
        self.assertEqual(tag.slug, expected_slug)

    def test_tag_slug_uniqueness(self):
        name = "UniqueTag"
        Tag.objects.create(name=name)
        with self.assertRaises(Exception):
            Tag.objects.create(name=name)


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    },
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
)
class PostModelTests(TestCase):
    def setUp(self):
        # Create a single author and category to reuse
        self.author = Author.objects.create(name="Alice", email="alice@example.com")
        self.category = Category.objects.create(title="Tech News")

    def tearDown(self):
        self.author.avatar.delete(save=False)

    def test_post_str_and_slug_auto_generation(self):
        title = "My First Post"
        post = Post.objects.create(
            title=title,
            excerpt="An excerpt of my first post.",
            image="https://example.com/image.png",
            category=self.category,
            published_at=timezone.now(),
            author=self.author,
            read_time="3 min read",
            content="This is the full content of the post.",
        )
        # __str__ should return the title
        self.assertEqual(str(post), title)

        # Slug should be auto-generated from title
        expected_slug = slugify(title)
        self.assertEqual(post.slug, expected_slug)

    def test_default_featured_and_read_time_field(self):
        post = Post.objects.create(
            title="Second Post",
            excerpt="Excerpt here.",
            image="",
            category=self.category,
            published_at=timezone.now(),
            author=self.author,
            read_time="",
            content="Content here.",
        )
        # featured defaults to False
        self.assertFalse(post.featured)

        # read_time can be blank
        self.assertEqual(post.read_time, "")

    def test_tags_relationship(self):
        post = Post.objects.create(
            title="Tagged Post",
            excerpt="Excerpt here.",
            image="",
            category=self.category,
            published_at=timezone.now(),
            author=self.author,
            read_time="2 min read",
            content="Some content.",
        )
        # Create two tags
        tag1 = Tag.objects.create(name="django")
        tag2 = Tag.objects.create(name="testing")
        post.tags.add(tag1, tag2)

        self.assertEqual(post.tags.count(), 2)
        self.assertIn(tag1, post.tags.all())
        self.assertIn(tag2, post.tags.all())

    def test_comment_count_property(self):
        post = Post.objects.create(
            title="Commented Post",
            excerpt="An excerpt.",
            image="",
            category=self.category,
            published_at=timezone.now(),
            author=self.author,
            read_time="1 min read",
            content="Content.",
        )
        # Initially no comments
        self.assertEqual(post.comment_count, 0)

        # Add comments
        Comment.objects.create(post=post, name="Anna", email="anna@example.com", content="First comment.")
        Comment.objects.create(post=post, name="Bob", email="bob@example.com", content="Second comment.")
        self.assertEqual(post.comment_count, 2)

    def test_post_ordering_by_published_at(self):
        now = timezone.now()
        earlier = now - timedelta(days=1)
        later = now + timedelta(days=1)

        post_old = Post.objects.create(
            title="Old Post",
            excerpt="Old excerpt.",
            image="",
            category=self.category,
            published_at=earlier,
            author=self.author,
            read_time="1 min read",
            content="Old content.",
        )
        post_now = Post.objects.create(
            title="Now Post",
            excerpt="Now excerpt.",
            image="",
            category=self.category,
            published_at=now,
            author=self.author,
            read_time="1 min read",
            content="Now content.",
        )
        post_future = Post.objects.create(
            title="Future Post",
            excerpt="Future excerpt.",
            image="",
            category=self.category,
            published_at=later,
            author=self.author,
            read_time="1 min read",
            content="Future content.",
        )

        qs = Post.objects.all()
        # Because Meta.ordering = ["-published_at"], the newest (future) first, then now, then earlier
        self.assertEqual(list(qs), [post_future, post_now, post_old])


class CommentModelTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Commenter Author", email="commenter@example.com")
        self.category = Category.objects.create(title="Comments Category")
        self.post = Post.objects.create(
            title="Post for Comments",
            excerpt="Excerpt.",
            image="",
            category=self.category,
            published_at=timezone.now(),
            author=self.author,
            read_time="1 min read",
            content="Content.",
        )

    def tearDown(self):
        self.author.avatar.delete(save=False)

    def test_comment_str(self):
        comment = Comment.objects.create(
            post=self.post,
            name="Tester",
            email="tester@example.com",
            content="This is a test comment.",
        )
        expected = f"Comment by Tester on {self.post.title}"
        self.assertEqual(str(comment), expected)

    def test_comment_fields_and_defaults(self):
        comment = Comment.objects.create(
            post=self.post,
            name="Emily",
            email="emily@example.com",
            content="Hello world!",
        )
        # created_at should be auto-populated; just check it's close to now
        now = timezone.now()
        self.assertTrue((now - comment.created_at).total_seconds() < 10)

        # is_public defaults to True
        self.assertTrue(comment.is_public)

        # Fields match
        self.assertEqual(comment.name, "Emily")
        self.assertEqual(comment.email, "emily@example.com")
        self.assertEqual(comment.content, "Hello world!")
        self.assertEqual(comment.post, self.post)


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }
)
class BlogApiPageTests(APITestCase):
    def setUp(self):
        self.sample_file = SimpleUploadedFile(name="test.jpg", content=b"file_content", content_type="image/jpeg")

        self.image = Image.objects.create(name="existing", alt="An existing image", image=self.sample_file)
        self.author = Author.objects.create(
            name="Commenter Author",
            email="commenter@example.com",
            bio="This is a test comment.",
            avatar=self.sample_file,
        )
        self.second_author = Author.objects.create(
            name="Second Author",
            email="second@example.com",
            bio="This is a second test comment.",
            avatar=self.sample_file,
        )
        # Dates for posts
        self.sample_date = timezone.now() - timedelta(days=1)
        self.future_date = timezone.now() + timedelta(days=1)
        # Category
        self.category = Category.objects.create(title="Comments Category")
        self.tag = Tag.objects.create(slug="test", name="testr")
        # Generate 12 Posts
        self.posts = []
        for i in range(12):
            post = Post.objects.create(
                title=f"Test Post {i}",
                excerpt="Excerpt.",
                image=self.sample_file,
                category=self.category,
                published_at=self.sample_date if i < 6 else self.future_date,
                author=self.author if i % 2 == 0 else self.second_author,
                content="Content for post {}.".format(i),
                read_time="1 min read",
                featured=(i % 3 == 0),
                slug=f"test-slug-{i}",
            )
            self.posts.append(post)
            if i % 2 == 0:
                post.tags.add(self.tag)

        self.posts_count = lambda count_post_on_page: reverse(
            "BlogApi:post_page_count", kwargs={"post_per_page": count_post_on_page}
        )

        self.post_page = lambda page: reverse("BlogApi:post-page", kwargs={"page_number": page})

        self.post_view_page = lambda slug=None: reverse("BlogApi:post", kwargs={"slug": slug}) if slug else reverse("BlogApi:post_without_slug")

        self.related_posts_view = lambda slug=None: (
            reverse("BlogApi:related_post", kwargs={"category_slug": slug})
            if slug
            else reverse("BlogApi:related-posts_without_slug")
        )

        self.tags = reverse("BlogApi:blog-tags")
        self.categoryEndpoint = reverse("BlogApi:blog-categories")

    def tearDown(self):
        self.image.image.delete(save=False)
        self.image.delete()

        self.author.avatar.delete(save=False)
        self.second_author.avatar.delete(save=False)
        for post in self.posts:
            post.image.delete(save=False)

        super().tearDown()

    def test_post_view_no_slug(self):
        url = self.post_view_page()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_related_posts_no_slug(self):
        url = self.related_posts_view()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_related_posts_with_no_image(self):
        # Create a post without an image in the same category
        no_image_post = Post.objects.create(
            title="No Image Post",
            slug="no-image-post",
            category=self.category,
            published_at=timezone.now(),
            author=self.author,
            content="Content.",
        )
        self.posts.append(no_image_post)  # Add for cleanup
        url = self.related_posts_view(self.category.slug)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = json.loads(response.content)
        # Find the post without an image
        no_image_post_data = next((p for p in payload if p["slug"] == "no-image-post"), None)
        self.assertIsNotNone(no_image_post_data)
        self.assertEqual(no_image_post_data["image"], "")

    def test_posts_count_with_filter(self):
        url = self.posts_count(2)
        filter_json = json.dumps({"title": "Test Post 1"})
        response = self.client.get(url, {"filter": filter_json})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = json.loads(response.text)
        self.assertEqual(payload["count"], 1)

    def test_post_page_view_with_filter(self):
        url = self.post_page(1)
        filter_json = json.dumps({"tags": [self.tag.slug]})
        response = self.client.get(url, {"per_page": "3", "filter": filter_json})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = json.loads(response.content)
        self.assertEqual(len(payload["posts"]), 3)

    def test_post_page_view_with_invalid_filter(self):
        url = self.post_page(1)
        response = self.client.get(url, {"filter": "invalid-json"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_posts_count_with_invalid_filter(self):
        url = self.posts_count(2)
        response = self.client.get(url, {"filter": "invalid-json"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_posts_count(self):
        url = self.posts_count(2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = json.loads(response.text)
        self.assertIn("count", payload)
        self.assertEqual(payload["count"], 3)

    def test_posts_page(self):
        url = self.post_page(1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = json.loads(response.text)
        self.assertIn("page", payload)
        self.assertIn("posts", payload)
        self.assertEqual(payload["page"], 1)
        self.assertEqual(len(payload["posts"]), 6)
        url = self.post_page(2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = json.loads(response.text)
        self.assertIn("page", payload)
        self.assertIn("posts", payload)
        self.assertEqual(payload["page"], 2)
        self.assertEqual(len(payload["posts"]), 0)

    def test_posts_pages(self):
        for page in self.posts:
            url = self.post_view_page(page.slug)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            payload = json.loads(response.content)
            self.assertIn("id", payload)
            self.assertEqual(payload["id"], page.id)
            self.assertIn("slug", payload)
            self.assertEqual(payload["slug"], page.slug)
            self.assertEqual(len(payload), 12)

    def test_tags(self):
        response = self.client.get(self.tags)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = json.loads(response.content)
        self.assertEqual(len(payload), 1)

    def test_categories(self):
        response = self.client.get(self.categoryEndpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = json.loads(response.content)
        self.assertEqual(len(payload), 1)
        self.assertIn("slug", payload[0])
        self.assertEqual(payload[0]["slug"], self.category.slug)
        self.assertIn("title", payload[0])
        self.assertEqual(payload[0]["title"], self.category.title)
        self.assertIn("BlogCount", payload[0])
        self.assertEqual(payload[0]["BlogCount"], 6)


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }
)
class BlogApiPageEmptyDatabaseTests(APITestCase):
    def setUp(self):
        self.posts_count = lambda count_post_on_page: reverse(
            "BlogApi:post_page_count", kwargs={"post_per_page": count_post_on_page}
        )

        self.post_page = lambda page: reverse("BlogApi:post-page", kwargs={"page_number": page})

        self.post_view_page = lambda slug: reverse("BlogApi:post", kwargs={"slug": slug})

        self.tags = reverse("BlogApi:blog-tags")
        self.categoryEndpoint = reverse("BlogApi:blog-categories")

    def test_no_posts_count(self):
        url = self.posts_count(2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = json.loads(response.text)
        self.assertIn("count", payload)
        self.assertEqual(payload["count"], 0)

    def test_no_posts_page(self):
        url = self.post_page(1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = json.loads(response.content)
        self.assertIn("page", payload)
        self.assertIn("posts", payload)
        self.assertEqual(payload["page"], 1)
        self.assertEqual(len(payload["posts"]), 0)

    def test_no_posts_pages(self):
        url = self.post_view_page("test")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_tags_empty(self):
        response = self.client.get(self.tags)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payload = json.loads(response.content)
        self.assertEqual(len(payload), 0)


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    },
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    },
)
class FilterPostsTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author", email="author@test.com")
        self.category1 = Category.objects.create(title="Tech")
        self.category2 = Category.objects.create(title="Science")
        self.tag1 = Tag.objects.create(name="Django")
        self.tag2 = Tag.objects.create(name="Python")

        self.post1 = Post.objects.create(
            title="Post about Django",
            author=self.author,
            category=self.category1,
            published_at=timezone.now(),
        )
        self.post1.tags.add(self.tag1)

        self.post2 = Post.objects.create(
            title="Post about Python",
            author=self.author,
            category=self.category1,
            published_at=timezone.now(),
        )
        self.post2.tags.add(self.tag2)

        self.post3 = Post.objects.create(
            title="Another Tech Post",
            author=self.author,
            category=self.category1,
            published_at=timezone.now(),
        )
        self.post3.tags.add(self.tag1, self.tag2)

        self.post4 = Post.objects.create(
            title="Science and Python",
            author=self.author,
            category=self.category2,
            published_at=timezone.now(),
        )
        self.post4.tags.add(self.tag2)

    def tearDown(self):
        self.author.avatar.delete(save=False)
        self.post1.image.delete(save=False)
        self.post2.image.delete(save=False)
        self.post3.image.delete(save=False)
        self.post4.image.delete(save=False)

    def test_filter_by_title(self):
        posts = Post.objects.all()
        filter_json = json.dumps({"title": "Django"})
        filtered = filter_posts(posts, filter_json)
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first(), self.post1)

    def test_filter_by_category(self):
        posts = Post.objects.all()
        filter_json = json.dumps({"category": self.category2.slug})
        filtered = filter_posts(posts, filter_json)
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first(), self.post4)

    def test_filter_by_single_tag(self):
        posts = Post.objects.all()
        filter_json = json.dumps({"tags": [self.tag1.slug]})
        filtered = filter_posts(posts, filter_json)
        self.assertEqual(filtered.count(), 2)
        self.assertIn(self.post1, filtered)
        self.assertIn(self.post3, filtered)

    def test_filter_by_multiple_tags(self):
        posts = Post.objects.all()
        filter_json = json.dumps({"tags": [self.tag1.slug, self.tag2.slug]})
        filtered = filter_posts(posts, filter_json)
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first(), self.post3)

    def test_filter_by_title_and_category(self):
        posts = Post.objects.all()
        filter_json = json.dumps({"title": "Post", "category": self.category1.slug})
        filtered = filter_posts(posts, filter_json)
        self.assertEqual(filtered.count(), 3)
        self.assertIn(self.post1, filtered)
        self.assertIn(self.post2, filtered)
        self.assertIn(self.post3, filtered)

    def test_filter_by_all(self):
        posts = Post.objects.all()
        filter_json = json.dumps({"title": "Django", "category": self.category1.slug, "tags": [self.tag1.slug]})
        filtered = filter_posts(posts, filter_json)
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first(), self.post1)

    def test_no_filter(self):
        posts = Post.objects.all()
        filter_json = json.dumps({})
        filtered = filter_posts(posts, filter_json)
        self.assertEqual(filtered.count(), 4)

    def test_empty_filter_values(self):
        posts = Post.objects.all()
        filter_json = json.dumps({"title": "", "category": "", "tags": []})
        filtered = filter_posts(posts, filter_json)
        self.assertEqual(filtered.count(), 4)
