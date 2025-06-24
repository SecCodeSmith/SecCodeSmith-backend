import json

from django.db.models import QuerySet

def filter_posts(posts : QuerySet, filt_json):
    filt_json = json.loads(filt_json)

    if 'title' in filt_json and filt_json['title'] != '':
        posts = posts.filter(title__icontains=filt_json['title'])
    if 'tags' in filt_json:
        for slug in filt_json['tags']:
            posts = posts.filter(tags__slug=slug)
    if 'category' in filt_json and filt_json['category'] != '':
        posts = posts.filter(category__slug=filt_json['category'])

    return posts