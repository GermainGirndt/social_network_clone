from django.contrib import admin
from groups import models
# Register your models here.

# For showing the groups and the instances on the admin page


class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember


admin.site.register(models.Group)
