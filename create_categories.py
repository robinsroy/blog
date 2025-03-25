import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_blog.settings')
django.setup()

from blog.models import Category

categories = [
    {'name': 'Technology', 'description': 'Posts about technology, programming, and software development.'},
    {'name': 'Travel', 'description': 'Travel experiences, tips, and destination guides.'},
    {'name': 'Lifestyle', 'description': 'Posts about daily life, personal development, and well-being.'},
    {'name': 'Food', 'description': 'Recipes, restaurant reviews, and culinary experiences.'},
    {'name': 'Photography', 'description': 'Photography tips, techniques, and showcases.'},
]

for category_data in categories:
    Category.objects.get_or_create(
        name=category_data['name'],
        defaults={'description': category_data['description']}
    ) 