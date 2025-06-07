import json
from datetime import timezone

from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView

from BlogApi.models import Post


class PostViews(APIView):
    def get(self,request, slug=None):
        """
        Get post details
        """

        if not slug:
            return JsonResponse({'error':'No post slug provided'},
                                status=status.HTTP_400_BAD_REQUEST)
        data = {}
        try:
            post = Post.objects.get(slug=slug)

            data = {
                'id': post.pk,
                'slug': post.slug,
                'title': post.title,
                'excerpt': post.excerpt,
                'image': post.image,
                'category': post.category,
                'date': post.published_at,
                'author': {
                    'name': post.author.name,
                    'email': post.author.email,
                    'bio': post.author.bio,
                    'avatar': post.author.avatar.url,
                },

            }

        except Post.DoesNotExist:
            return JsonResponse({'error':'Post not found'},
                                status=status.HTTP_404_NOT_FOUND)

        finally:
            return JsonResponse(data,status=status.HTTP_200_OK)

class PostPagesCount(APIView):
    def get(self, request, post_per_page=6):
        try:
            count = Post.objects.filter(published_at__gte=timezone.now()).count() / post_per_page

            return JsonResponse({'count': count},status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return JsonResponse({'error':'Post not found'},)

class PostPageView(APIView):
    def get(self, request, page_number=1):

        per_page = request.GET.get('per_page', 6)
        filt_json = request.GET.get('filter')

        data = {}
        try:
            posts = Post.objects.order_by('-published_at').all()
            if filt_json:
                filt_json = json.loads(filt_json)

                if 'title' in filt_json:
                    posts = posts.filter(title__icontains=filt_json['title'])
                if 'tags' in filt_json:
                    posts = posts.filter(tags__slug=filt_json['tags'])
                if 'category' in filt_json:
                    posts = posts.filter(category__slug=filt_json['category'])


            page = posts[(per_page * (page_number - 1)):(per_page * page_number)]

            data = {
                'page': page_number,
                'posts': [
                    {
                        'title': post.title,
                        'author': post.author.name,
                        'publish_at': post.published_at.isoformat("%d-%m-%Y"),
                        'comments': post.comment_count,
                        'tags': [ tag.name for tag in post.tags.all()],
                        'category': post.category,
                    }
                    for post in page
                ]
            }
            return JsonResponse(data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return JsonResponse({'error':'Post not found'},status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return JsonResponse(
                {'error': 'Invalid JSON in filter param'},
                status=status.HTTP_400_BAD_REQUEST
            )
