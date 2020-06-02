# POSTS VIEWS.PY
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
# Create your views here.

from django.http import Http404
from django.views import generic

# pip install braces!
from braces.views import SelectRelatedMixin

from posts import models, form

from django.contrib import messages

from django.contrib.auth import get_user_model
User = get_user_model()


class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    # from the mixin:
    select_related = ('user', 'group')


class UserPosts(generic.list.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
                # Try to fatch the user's posts
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
            print(self.post_user)
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(f"Context antes: {context}")
        context['post_user'] = self.post_user
        print(f"Context depois: {context}")
        return context


class PostDetail(SelectRelatedMixin, generic.detail.DetailView):
    model = models.Post
    select_related = ('user', 'group')

    def get_queryset(self):
        # object relational model: queryset
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.edit.CreateView):
    model = models.Post
    fields = ('message', 'group')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):

    model = models.Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)
