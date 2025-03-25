import os
import django
from django.core.files import File
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_blog.settings')
django.setup()

from blog.models import Post, Comment, Category
from django.contrib.auth.models import User

def create_default_posts():
    # Get or create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("Created admin user")

    # Get or create categories
    tech_category, _ = Category.objects.get_or_create(
        name='Technology',
        defaults={'description': 'Posts about technology and innovation'}
    )
    travel_category, _ = Category.objects.get_or_create(
        name='Travel',
        defaults={'description': 'Travel experiences and tips'}
    )
    lifestyle_category, _ = Category.objects.get_or_create(
        name='Lifestyle',
        defaults={'description': 'Lifestyle and personal development'}
    )

    # Sample posts
    posts = [
        {
            'title': 'Getting Started with Django',
            'content': '''Django is a high-level Python web framework that enables rapid development of secure and maintainable websites. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.

Key features of Django:
- Fast and secure
- Scalable
- Versatile
- Maintainable

In this post, we'll explore the basics of Django and how to get started with your first project.''',
            'category': tech_category,
            'status': 'published',
            'author': admin_user
        },
        {
            'title': 'Exploring the Hidden Gems of Paris',
            'content': '''Paris, the City of Light, is known for its iconic landmarks like the Eiffel Tower and Notre-Dame. However, beyond these famous attractions lie countless hidden gems waiting to be discovered.

In this post, we'll explore:
- Secret gardens
- Local markets
- Hidden cafes
- Lesser-known museums

Join us on a journey through the lesser-explored corners of Paris.''',
            'category': travel_category,
            'status': 'published',
            'author': admin_user
        },
        {
            'title': 'The Art of Minimalist Living',
            'content': '''Minimalism is more than just owning fewer possessions. It's a lifestyle choice that can lead to greater happiness and fulfillment.

Key principles of minimalist living:
- Declutter regularly
- Focus on experiences over things
- Practice gratitude
- Simplify daily routines

Learn how to embrace minimalism and transform your life.''',
            'category': lifestyle_category,
            'status': 'published',
            'author': admin_user
        }
    ]

    # Create posts
    for post_data in posts:
        post, created = Post.objects.get_or_create(
            title=post_data['title'],
            defaults={
                'content': post_data['content'],
                'category': post_data['category'],
                'status': post_data['status'],
                'author': post_data['author']
            }
        )
        if created:
            print(f"Created post: {post.title}")

            # Add some comments
            comments = [
                {
                    'content': 'Great article! Very informative and well-written.',
                    'author': admin_user
                },
                {
                    'content': 'I learned a lot from this post. Thanks for sharing!',
                    'author': admin_user
                },
                {
                    'content': 'This is exactly what I was looking for. Keep up the good work!',
                    'author': admin_user
                }
            ]

            for comment_data in comments:
                Comment.objects.create(
                    post=post,
                    content=comment_data['content'],
                    author=comment_data['author']
                )

if __name__ == '__main__':
    create_default_posts()
    print("Default posts and comments created successfully!") 