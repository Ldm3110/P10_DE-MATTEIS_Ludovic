from django.db import models

from authentication.models import User
from config import settings
from utilities import *


class Projects(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=4000)
    type = models.CharField(max_length=128, choices=TYPE)

    contribution = models.ManyToManyField(User, through='Contributors')

    def __str__(self):
        return "%s %s" % (self.id, self.title)


class Issues(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=4000)
    tag = models.CharField(max_length=128, choices=TAG)
    priority = models.CharField(max_length=128, choices=PRIORITY)
    status = models.CharField(max_length=128, choices=STATUS)

    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return "#%s %s" % (self.id, self.title)


class Comments(models.Model):
    description = models.TextField(max_length=4000)

    issues_id = models.ForeignKey(Issues, on_delete=models.CASCADE)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class Contributors(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, choices=ROLE)
