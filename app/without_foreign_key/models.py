from django.db import models
from django.utils.translation import gettext_lazy as _


class Users(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=1)

    class UsersType(models.TextChoices):
        ADMIN = 'ADM', _('Admin')
        BLOGGER = 'BLG', _('Blogger')
        READER = 'RD', _('Reader')

    user_type = models.CharField(
        max_length=3,
        db_index=True,
        choices=UsersType.choices,
        default=UsersType.READER,
    )


class BlogTypes(models.Model):
    type = models.CharField(max_length=128, db_index=True)
    active = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)


class Blogs(models.Model):
    title = models.CharField(max_length=64, db_index=True)
    short_description = models.CharField(max_length=256)
    description = models.TextField()
    created_by = models.IntegerField(null=True, db_index=True)
    type = models.IntegerField(null=True, db_index=True)
    show = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    comment = models.TextField()
    comment_to = models.IntegerField(null=True, db_index=True)
    created_by = models.IntegerField(null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
