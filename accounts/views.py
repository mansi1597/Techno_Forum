from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm, UpdateProfileForm
from django.views.generic import DetailView,UpdateView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import UserProfileInfo, User
from django.shortcuts import get_object_or_404
from posts.forms import CommentForm
# Create your views here.


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home:index'))


def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

        if registered:
            return HttpResponseRedirect('/accounts/user_login')

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'accounts/registration.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                request.session['user_id'] = user.profile.pk
                return HttpResponseRedirect(reverse('posts:list_and_create', kwargs={'pk': user.profile.pk}))
            else:
                return HttpResponse("Account not active")
        else:
            print("Tried login and failed")
            print("username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied!")

    else:
        return render(request, 'accounts/login.html', {})


class ProfileDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/user_login'
    redirect_field_name = 'home:index'
    model = UserProfileInfo
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        if self.request.session.has_key('user_id'):
            u_id = self.request.session['user_id']
            context = super(ProfileDetailView, self).get_context_data(**kwargs)
            context['user_id'] = u_id

        f = CommentForm()
        context['form'] = f
        return context


def profile_update(request, pk):
    if request.session.has_key('user_id'):
        u_id = request.session['user_id']

    profile = get_object_or_404(UserProfileInfo, pk=pk)
    user = get_object_or_404(User, pk=profile.user.pk)

    if request.method == "POST":
        form1 = UpdateProfileForm(request.POST, instance=user)
        form2 = UserProfileInfoForm(request.POST, instance=profile)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            profile_info = form2.save(commit=False)

            if 'profile_pic' in request.FILES:
                profile_info.profile_pic = request.FILES['profile_pic']

            profile_info.save()
            return HttpResponseRedirect(reverse('accounts:profile', kwargs={'pk': pk}))

    else:

        profile = get_object_or_404(UserProfileInfo, pk=pk)
        user = get_object_or_404(User, pk=profile.user.pk)
        form1 = UpdateProfileForm(instance=user)
        form2 = UserProfileInfoForm(instance=profile)
        return render(request, 'accounts/profile_update.html',
                      context={'user_id': u_id, 'form1': form1, 'form2': form2})
