from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify

class Author(models.Model):
    """
    Represents an author of a post.
    If you use Django’s built-in User, you can instead
    point to settings.AUTH_USER_MODEL via ForeignKey.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        upload_to='authors/avatars/',
        null=True,
        blank=True,
        help_text="Optional profile picture for the author"
    )

    @admin.display
    def image_tag(self):
        return format_html('<img src="{}" alt="author img" height="100" />',
                           self.image.url)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    A simple Category model. If you prefer to keep category
    as a CharField, you can skip this and use a choices tuple instead.
    """
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Automatically generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """
    Tags for posts. Many-to-many relationship from Post to Tag.
    """
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=40, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatically generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    """
    The main Post model, corresponding to:
      id: string;
      slug: string;
      title: string;
      excerpt: string;
      image: string;
      category: string;
      date: string;
      author: string;
      commentCount: number;
      readTime: string;
      featured?: boolean;
      tags: string[];
      content: string;
    """
    slug = models.SlugField(
        max_length=150,
        unique=True,
        help_text="A URL-friendly identifier derived from title."
    )
    title = models.CharField(max_length=200)
    excerpt = models.TextField(
        help_text="Short summary of the post (e.g. first 1–2 sentences)."
    )
    image = models.ImageField(
        upload_to='posts/images/',
        null=True, blank=True,)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="posts",
        help_text="Select a category for this post."
    )
    published_at = models.DateTimeField(
        db_index=True,
        help_text="When the post was (or will be) published.",
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    featured = models.BooleanField(
        default=False,
        help_text="Mark as featured post (e.g. for homepage slider)."
    )
    read_time = models.CharField(
        max_length=20,
        blank=True,
        help_text="Estimated read time, e.g. '5 min read'."
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="posts",
        blank=True
    )
    content = models.TextField(help_text="Full HTML or Markdown content of the post.")

    class Meta:
        ordering = ["-published_at"]
        indexes = [
            models.Index(fields=["published_at"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.title

    @admin.display
    def image_tag(self):
        return format_html('<img src="{}" height="100" />',
                           self.image.url)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    @property
    def comment_count(self):
        # Instead of storing commentCount redundantly, compute it on the fly.
        return self.comments.count()

    def save(self, *args, **kwargs):
        # Auto-generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    """
    Represents a comment on a Post. Adjust fields as needed
    (e.g. if you want to link comments to registered users).
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    name = models.CharField(max_length=80, help_text="Display name of the commenter")
    email = models.EmailField(help_text="Email of the commenter")
    content = models.TextField(help_text="Comment text")
    created_at = models.DateTimeField(auto_now_add=True)

    is_public = models.BooleanField(
        default=True,
        help_text="Uncheck to hide comment without deleting."
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"
