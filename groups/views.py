from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import CreateView,ListView,DetailView
from django.urls import reverse
from groups.models import Group,GroupMember, Message, Request
from django.shortcuts import get_object_or_404
from accounts.models import UserProfileInfo
from django.contrib.auth.decorators import login_required
from .forms import MessageCreateForm
from posts.models import Posts


class GroupList(LoginRequiredMixin, ListView):
    login_url = '/accounts/user_login'
    redirect_field_name = 'home:index'
    model = Group
    template_name = "groups/mygroups.html"

    def get_context_data(self, **kwargs):
        if self.request.session.has_key('user_id'):
            u_id = self.request.session['user_id']
            context = super(GroupList, self).get_context_data(**kwargs)
            context['user_id'] = u_id

            profile = get_object_or_404(UserProfileInfo,pk=u_id)
            groups = profile.groups
            context['groups'] = groups
            return context


class GroupDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/user_login'
    redirect_field_name = 'home:index'
    model = Group
    template_name = "groups/group_detail.html"

    def get_context_data(self, **kwargs):
        if self.request.session.has_key('user_id'):
            u_id = self.request.session['user_id']
            context = super(GroupDetailView, self).get_context_data(**kwargs)
            context['user_id'] = u_id

        f = MessageCreateForm()
        context['form'] = f
        return context


def add_message_to_group(request, pk):

    group = get_object_or_404(Group, pk=pk)
    if request.session.has_key('user_id'):
        u_id = request.session['user_id']
        profile = get_object_or_404(UserProfileInfo, pk=u_id)

    if request.method == "POST":
        f = MessageCreateForm(request.POST)

        if f.is_valid():
            msg = f.save(commit=False)
            msg.group = group
            msg.user = profile
            msg.save()
            return redirect('groups:group_detail', pk=pk)


def send_request_to_group(request, pk):

    if request.session.has_key('user_id'):
        u_id = request.session['user_id']
        profile = get_object_or_404(UserProfileInfo, pk=u_id)

    post = get_object_or_404(Posts, pk=pk)
    group = get_object_or_404(Group, pk=post.group.pk)

    Request.objects.create(group=group, sent_by=profile)
    return redirect('posts:post_detail', pk=pk)


@login_required
def request_accept(request, pk):
    req = get_object_or_404(Request, pk=pk)
    req.accept()
    return redirect('groups:request_list')


@login_required()
def request_reject(request, pk):
    req = get_object_or_404(Request, pk=pk)
    req.delete()
    return redirect('groups:request_list')


class RequestListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/user_login'
    redirect_field_name = 'home:index'
    model = Request
    template_name = 'groups/myrequests.html'

    def get_context_data(self, **kwargs):
        if self.request.session.has_key('user_id'):
            u_id = self.request.session['user_id']
            context = super(RequestListView, self).get_context_data(**kwargs)
            context['user_id'] = u_id

            profile = get_object_or_404(UserProfileInfo, pk=u_id)
            groups = profile.groups
            context['groups'] = groups
            return context