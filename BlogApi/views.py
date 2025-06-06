from django.http import JsonResponse
from django.shortcuts import render
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