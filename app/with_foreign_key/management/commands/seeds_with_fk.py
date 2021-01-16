from time import time
from django.core.management.base import BaseCommand, CommandError
from with_foreign_key.models import Users, Blogs, BlogTypes, Comments
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Generate seed'

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.fake = Faker()

    def handle(self, *args, **options):
        self.generate_users()
        self.generate_blog_types()
        self.generate_blogs()
        self.generate_comments()

    def generate_users(self):
        for _ in range(100):
            user = Users()
            user.email = str(time()) + self.fake.safe_email()
            user.first_name = self.fake.first_name()
            user.last_name = self.fake.last_name()
            user.active = bool(random.randrange(0, 20) <= 18)
            user.user_type = random.choice(['ADM', 'BLG', 'RD'])
            user.save()

        self.stdout.write(self.style.SUCCESS('Users Created'))

    def generate_blog_types(self):
        for _ in range(10):
            blog_type = BlogTypes()
            blog_type.type = self.fake.sentence(nb_words=2)
            blog_type.save()

        self.stdout.write(self.style.SUCCESS('Blog Types Created'))

    def generate_blogs(self):
        blog_types = list(BlogTypes.objects.all())
        users = list(Users.objects.all())

        for _ in range(1000):
            blog = Blogs()
            blog.title = self.fake.sentence(nb_words=5)
            blog.short_description = self.fake.sentence(nb_words=20)
            blog.description = self.fake.text(max_nb_chars=1000)
            blog.type = random.choice(blog_types)
            blog.show = bool(random.randrange(0, 20) <= 18)
            blog.created_by = random.choice(users)
            blog.save()

        self.stdout.write(self.style.SUCCESS('Blogs Created'))

    def generate_comments(self):
        blogs = list(Blogs.objects.all())
        users = list(Users.objects.all())

        for blog in blogs:
            for _ in range(random.randrange(10, 100)):
                comment = Comments()
                comment.comment = self.fake.sentence(nb_words=10)
                comment.comment_to = blog
                comment.created_by = random.choice(users)
                comment.save()

        self.stdout.write(self.style.SUCCESS('Comments Created'))
