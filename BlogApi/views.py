import json
from datetime import timezone

from django.http import JsonResponse
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
    def get(self, request):
        try:
            count = Post.objects.filter(published_at__gte=timezone.now()).count()

            return JsonResponse({'count': count},status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return JsonResponse({'error':'Post not found'},)

class PostPageView(APIView):
    def get(self, request, page_nuber=None, post_per_pages=6, filter = None):
        data = {}
        try:
            posts = Post.objects.order_by('-published_at').all()
            if filter:
                filter = json.loads(filter)

                if 'title' in filter:
                    posts = posts.filter(title__icontains=filter['title'])
                if 'tags' in filter:
                    posts = posts.filter(tags__slug=filter['tags'])
                if 'category' in filter:
                    posts = posts.filter(category__slug=filter['category'])


            page = posts[(post_per_pages * (page_nuber - 1)):(post_per_pages * page_nuber)]

            data = {
                'page': page_nuber,
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

        except Post.DoesNotExist:
            return JsonResponse({'error':'Post not found'},status=status.HTTP_404_NOT_FOUND)

        finally:
            return JsonResponse(data,status=status.HTTP_200_OK)