import json
from datetime import timezone

from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status, permissions
from rest_framework.views import APIView

from BlogApi.models import Post, Tag, Category


class PostViewsEndpoint(APIView):
    permission_classes = (permissions.AllowAny,)
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
                'category': post.category.title,
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

class PostPagesCountEndpoint(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, post_per_page=6):
        try:
            count = (Post.objects
                     .filter(published_at__gte=timezone.now()).count() / post_per_page)

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
                     order_by('-published_at').all())
            if filt_json:
                filt_json = json.loads(filt_json)

                if 'title' in filt_json:
                    posts = posts.filter(title__icontains=filt_json['title'])
                if 'tags' in filt_json:
                    posts = posts.filter(tags__slug__in=filt_json['tags'])
                if 'category' in filt_json:
                    posts = posts.filter(category__slug=filt_json['category'])


            page = posts[(per_page * (page_number - 1)):(per_page * page_number)]

            data = {
                'page': page_number,
                'posts': [
                    {
                        'title': post.title,
                        'slug': post.slug,
                        'author': post.author.name,
                        'publish_at': post.published_at.strftime("%d-%m-%Y"),
                        'comments': post.comment_count,
                        'featured': post.featured,
                        'image': post.image.url or "",
                        'tags': [ tag.name for tag in post.tags.all()],
                        'category': post.category.title,
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
