from django.db import models
# remove any caracters tht aren't aphanumeric (ex: lowercases and replaces spaces with underscores)
from django.utils.text import slugify
# link embetting, mark down text (like reedit)
import misaka
from django.urls import reverse

from django.contrib.auth import get_user_model

# calls things from the user session
User = get_user_model()

# registering for
from django import template
register = template.Library()


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    # Save method; treats the data and save

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    # membership is the name of the foreignkey
    group = models.ForeignKey(Group, related_name='memberships', on_delete=models.PROTECT)
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')
