from django.shortcuts import render

# Create your views here.

# standard messages for the user
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse
from django.views import generic
from groups.models import Group, GroupMember
from groups import models
from django.shortcuts import get_object_or_404


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    # not slugs nor members -> that' should be automatic
    fields = ('name', 'description')
    model = Group


class SingleGroup(generic.DetailView):
    model = Group


class ListGroups(generic.ListView):
    model = Group

# Redirect View for doing stuff when Join Group is clicked and then redirect
class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    # used automatically after user joined the group
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        # try to create a group member (add user to group)
        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            #request is empty
            messages.warning(self.request, 'Warning already a member!')
        else:
            messages.success(self.request, 'You are now a member!')
        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    # used automatically after user joined the group

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):

        try:
            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request, 'Sorry, You are not in this group!')
        else:
            membership.delete()
            messages.success(self.request, 'You have left the group!')
        return super().get(request, *args, **kwargs)
