# tests/test_models.py

from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta

from BlogApi.models import Author, Category, Tag, Post, Comment


class AuthorModelTests(TestCase):
    def test_author_str(self):
        author = Author.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            bio="Just a test author."
        )
        self.assertEqual(str(author), "Jane Doe")

    def test_author_fields(self):
        author = Author.objects.create(
            name="John Smith",
            email="john@example.com",
            bio=""
        )
        self.assertEqual(author.name, "John Smith")
        self.assertEqual(author.email, "john@example.com")
        self.assertEqual(author.bio, "")


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


class PostModelTests(TestCase):
    def setUp(self):
        # Create a single author and category to reuse
        self.author = Author.objects.create(
            name="Alice",
            email="alice@example.com"
        )
        self.category = Category.objects.create(title="Tech News")

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
            content="This is the full content of the post."
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
            content="Content here."
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
            content="Some content."
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
            content="Content."
        )
        # Initially no comments
        self.assertEqual(post.comment_count, 0)

        # Add comments
        Comment.objects.create(
            post=post,
            name="Anna",
            email="anna@example.com",
            content="First comment."
        )
        Comment.objects.create(
            post=post,
            name="Bob",
            email="bob@example.com",
            content="Second comment."
        )
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
            content="Old content."
        )
        post_now = Post.objects.create(
            title="Now Post",
            excerpt="Now excerpt.",
            image="",
            category=self.category,
            published_at=now,
            author=self.author,
            read_time="1 min read",
            content="Now content."
        )
        post_future = Post.objects.create(
            title="Future Post",
            excerpt="Future excerpt.",
            image="",
            category=self.category,
            published_at=later,
            author=self.author,
            read_time="1 min read",
            content="Future content."
        )

        qs = Post.objects.all()
        # Because Meta.ordering = ["-published_at"], the newest (future) first, then now, then earlier
        self.assertEqual(list(qs), [post_future, post_now, post_old])


class CommentModelTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="Commenter Author",
            email="commenter@example.com"
        )
        self.category = Category.objects.create(title="Comments Category")
        self.post = Post.objects.create(
            title="Post for Comments",
            excerpt="Excerpt.",
            image="",
            category=self.category,
            published_at=timezone.now(),
            author=self.author,
            read_time="1 min read",
            content="Content."
        )

    def test_comment_str(self):
        comment = Comment.objects.create(
            post=self.post,
            name="Tester",
            email="tester@example.com",
            content="This is a test comment."
        )
        expected = f"Comment by Tester on {self.post.title}"
        self.assertEqual(str(comment), expected)

    def test_comment_fields_and_defaults(self):
        comment = Comment.objects.create(
            post=self.post,
            name="Emily",
            email="emily@example.com",
            content="Hello world!"
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

