from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from accounts.models import UserProfileInfo
from posts.models import Posts, Comments
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView, ListView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from groups.models import Group
# Create your views here.


def list_and_create(request, pk):
    if request.session.has_key('user_id'):
        u_id = request.session['user_id']

    profile = get_object_or_404(UserProfileInfo, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.profile = profile
            post.save()
            return redirect('posts:list_and_create', pk=profile.pk)
    else:
        form = PostForm()

    objects = Posts.objects.all().order_by('-posted_on')

    if objects:

        return render(request, 'posts/newsfeed.html', context={'posts': objects, 'form': form, 'user_id': u_id})
    else:

        return render(request, 'posts/newsfeed.html', context={'form': form, 'user_id': u_id})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'accounts/profile.html'
    model = Posts

    def get_success_url(self):
        if self.request.session.has_key('user_id'):
            u_id = self.request.session['user_id']
            return reverse('accounts:profile', kwargs={'pk': u_id})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'accounts/profile.html'
    form_class = PostForm
    model = Posts
    template_name = 'posts/post_update.html'

    def get_context_data(self, **kwargs):
        if self.request.session.has_key('user_id'):
            u_id = self.request.session['user_id']
            context = super(PostUpdateView, self).get_context_data(**kwargs)
            context['user_id'] = u_id
            return context

    def get_success_url(self):
        if self.request.session.has_key('user_id'):
            u_id = self.request.session['user_id']
            return reverse('accounts:profile', kwargs={'pk': u_id})


class PostDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'posts/newsfeed.html'
    model = Posts
    template_name = 'posts/post_detail.html'

    def get_context_data(self, **kwargs):
        if self.request.session.has_key('user_id'):
            u_id = self.request.session['user_id']
            context = super(PostDetailView, self).get_context_data(**kwargs)
            context['user_id'] = u_id

        myuser = get_object_or_404(UserProfileInfo, pk=u_id)
        context['myuser'] = myuser

        post = get_object_or_404(Posts, pk=self.kwargs.get('pk'))

        try:
            myuser_req = get_object_or_404(myuser.requests, group=post.group)
        except:
            myuser_req = None

        context['user_req'] = myuser_req

        f = CommentForm()
        context['form'] = f
        return context


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Posts, pk=pk)
    if request.session.has_key('user_id'):
        u_id = request.session['user_id']

    if request.method == "POST":
        form = CommentForm(request.POST)
        author_name = get_object_or_404(UserProfileInfo, pk=u_id)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = author_name
            comment.comment_date = timezone.now()
            comment.save()
            return redirect('posts:post_detail', pk=post.pk)


class CommentCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/user_login'
    redirect_field_name = 'posts/newsfeed.html'
    form_class = CommentForm
    model = Comments
    success_url = 'posts/post_detail.html'


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'posts/newsfeed.html'
    model = Comments
    success_url = reverse_lazy('NEWSFEED')



