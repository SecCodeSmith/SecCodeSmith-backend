import json
from datetime import timezone

from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status, permissions
from rest_framework.views import APIView

from BlogApi.models import Post, Tag, Category
from BlogApi.untils import filter_posts


class PostViewsEndpoint(APIView):
    permission_classes = (permissions.AllowAny,)

    @method_decorator(cache_page(60))
    def get(self,request, slug=None):
        """
        Get post details
        """

        if not slug:
            return JsonResponse({'error':'No post slug provided'},
                                status=status.HTTP_400_BAD_REQUEST)
        try:
            post = Post.objects.get(slug=slug)

            data = {
                'id': post.pk,
                'slug': post.slug,
                'title': post.title,
                'excerpt': post.excerpt,
                'image': post.image.url or "",
                'category': {
                    'title': post.category.title,
                    'slug': post.category.slug,
                },
                'read_time': post.read_time,
                'publish_at': post.published_at.strftime("%d-%m-%Y"),
                'tags': [
                    {
                        'name': tag.name,
                        'slug': tag.slug
                    } for tag in post.tags.all()
                ],
                'date': post.published_at.strftime('%d-%m-%Y'),
                'content': post.content,
                'author': {
                    'name': post.author.name,
                    'bio': post.author.bio,
                    'avatar': post.author.avatar.url,
                },
            }
            return JsonResponse(data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return JsonResponse({'error':'Post not found'},
                                status=status.HTTP_404_NOT_FOUND)

class RelatedPostsViewsEndpoint(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, category_slug=None):
        """
        Get 3 related post for main.
        """
        if not category_slug:
            return JsonResponse({'error':'No post slug provided'},
                                status=status.HTTP_400_BAD_REQUEST)
        try:

            related_posts = (Post.objects.
                             filter(published_at__lte=timezone.now()).
                             filter(category__slug=category_slug))[:3]

            data = [
                {
                    'id': post_data.pk,
                    'slug': post_data.slug,
                    'title': post_data.title,
                    'publish_at': post_data.published_at.strftime("%d-%m-%Y"),
                    'image': post_data.image.url or "",
                } for post_data in related_posts
            ]
            return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except Post.DoesNotExist:
            return JsonResponse({'error':'Post not found'},
                                status=status.HTTP_404_NOT_FOUND)


class PostPagesCountEndpoint(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, post_per_page=6):

        filt_json = request.GET.get('filter')

        try:


            posts = Post.objects.filter(published_at__gte=timezone.now())

            if filt_json:
                posts = filter_posts(posts, filt_json)

            count = int(posts.count() / post_per_page)

            return JsonResponse({'count': count},status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return JsonResponse({'error':'Post not found'},
                                status=status.HTTP_404_NOT_FOUND)

class PostPageViewEndpoint(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, page_number=1):

        per_page = request.GET.get('per_page', '6')

        per_page = int(per_page)

        filt_json = request.GET.get('filter')

        try:
            posts = (Post.objects.
                    filter(published_at__lte=timezone.now()).
                     order_by('-published_at'))
            if filt_json:
                posts = filter_posts(posts, filt_json)

            posts = posts.all()

            page = posts[(per_page * (page_number - 1)):(per_page * page_number)]

            data = {
                'page': page_number,
                'posts': [
                    {
                        'title': post.title,
                        'slug': post.slug,
                        'author': {
                            'name' : post.author.name,
                            'bio': post.author.bio,
                            'avatar': post.author.avatar.url,
                        },
                        'publish_at': post.published_at.strftime("%d-%m-%Y"),
                        'comments': post.comment_count,
                        'featured': post.featured,
                        'image': post.image.url or "",
                        'tags': [ {
                            'name': tag.name,
                            'slug': tag.slug
                        } for tag in post.tags.all()],
                        'category': {
                            'title': post.category.title,
                            'slug': post.category.slug
                        },
                    }
                    for post in page
                ]
            }
            return JsonResponse(data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return JsonResponse({'error':'Post not found'},
                                status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return JsonResponse(
                {'error': 'Invalid JSON in filter param'},
                status=status.HTTP_400_BAD_REQUEST
            )

class TagListsEndpoint(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        try:
            tag = Tag.objects.all()
            data = [{
                'name': t.name,
                'slug': t.slug
            } for t in tag]
            return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except Tag.DoesNotExist:
            return JsonResponse({'error': 'not found'},
                                status=status.HTTP_404_NOT_FOUND)

class BlogCategoriesEndpoint(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        try:
            category = Category.objects.all()
            data = [{
                'title': category.title,
                'slug': category.slug,
                'BlogCount': Post.objects.filter(published_at__lt=timezone.now(),
                                                 category=category).count(),
            } for category in category]
            return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except Category.DoesNotExist:
            return JsonResponse({'error':'not found'},
                                status=status.HTTP_404_NOT_FOUND)
