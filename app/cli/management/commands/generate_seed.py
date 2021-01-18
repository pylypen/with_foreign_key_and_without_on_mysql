from time import time
from django.core.management.base import BaseCommand, CommandError
from with_foreign_key.models import \
    Users as UsersFK, \
    Blogs as BlogsFK, \
    BlogTypes as BlogTypesFK, \
    Comments as CommentsFK
from without_foreign_key.models import Users, Blogs, BlogTypes, Comments
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Generate seed'

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.fake = Faker()
        self.n_users = 100
        self.n_blog_types = 30
        self.n_blogs = 500
        self.number_iter = 1
        self.with_fk = True

    def add_arguments(self, parser):
        parser.add_argument(
            '--numbers',
            default=1
        )

    def handle(self, *args, **options):
        if options['numbers']:
            self.number_iter = int(options['numbers'])

        self.stdout.write(self.style.SUCCESS('Generate SEEDS WITH FK'))
        self.generate_seeds(UsersFK, BlogTypesFK, BlogsFK, CommentsFK)
        self.stdout.write(self.style.SUCCESS('================='))

        self.with_fk = False
        self.stdout.write(self.style.SUCCESS('Generate SEEDS WITHOUT FK'))
        self.generate_seeds(Users, BlogTypes, Blogs, Comments)
        self.stdout.write(self.style.SUCCESS('================='))

    def generate_seeds(self, users, blog_types, blogs, comments):
        self.stdout.write(self.style.SUCCESS('================='))
        self.generate_users(users)
        self.stdout.write(self.style.SUCCESS('================='))
        self.generate_blog_types(blog_types)
        self.stdout.write(self.style.SUCCESS('================='))
        self.generate_blogs(blogs, blog_types, users)
        self.stdout.write(self.style.SUCCESS('================='))
        self.generate_comments(comments, blogs, users)

        self.stdout.write(self.style.SUCCESS(' '))
        self.stdout.write(self.style.SUCCESS('================='))
        self.stdout.write(self.style.SUCCESS('All Seeds Created'))
        self.stdout.write(self.style.SUCCESS('================='))

    def generate_users(self, model):
        for i in range(self.n_users * self.number_iter):
            user = model()
            user.email = str(time()) + self.fake.safe_email()
            user.first_name = self.fake.first_name()
            user.last_name = self.fake.last_name()
            user.active = bool(random.randrange(0, 20) <= 18)
            user.user_type = random.choice(['ADM', 'BLG', 'RD'])
            user.save()

            self.print_progress(self.n_users, i, 'Users')

        self.stdout.write(self.style.SUCCESS('Users Created'))

    def generate_blog_types(self, model):
        for i in range(self.n_blog_types * self.number_iter):
            blog_type = model()
            blog_type.type = self.fake.sentence(nb_words=2)
            blog_type.save()

            self.print_progress(self.n_blog_types, i, 'BlogTypes')

        self.stdout.write(self.style.SUCCESS('Blog Types Created'))

    def generate_blogs(self, model, blog_types_model, users_model):
        blog_types = list(blog_types_model.objects.all())
        users = list(users_model.objects.all())

        for i in range(self.n_blogs * self.number_iter):
            blog = model()
            blog.title = self.fake.text(max_nb_chars=50)
            blog.short_description = self.fake.text(max_nb_chars=150)
            blog.description = self.fake.text(max_nb_chars=1000)
            blog.type = random.choice(blog_types) if self.with_fk else random.choice(blog_types).id
            blog.show = bool(random.randrange(0, 20) <= 18)
            blog.created_by = random.choice(users) if self.with_fk else random.choice(users).id
            blog.save()

            self.print_progress(self.n_blogs, i, 'Blogs')

        self.stdout.write(self.style.SUCCESS('Blogs Created'))

    def generate_comments(self, model, blogs_model, users_model):
        blogs = list(blogs_model.objects.all())
        users = list(users_model.objects.all())

        for blog in blogs:
            for _ in range(random.randrange(10, 50)):
                comment = model()
                comment.comment = self.fake.sentence(nb_words=10)
                comment.comment_to = blog if self.with_fk else blog.id
                comment.created_by = random.choice(users) if self.with_fk else random.choice(users).id
                comment.save()

            self.print_progress(self.n_blogs, blog.id, 'Blog Comments')

        self.stdout.write(self.style.SUCCESS('Comments Created'))

    def print_progress(self, numbers, iteration, model):
        if iteration / ((numbers * self.number_iter) / 10) in range(0, 11):
            txt = 'WITH FK' if self.with_fk else 'WITHOUT FK'
            print('%s iteration of %s %s model %s' % (iteration, numbers * self.number_iter, model, txt))
