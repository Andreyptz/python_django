from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView
from .models import Profile

# class AboutMeView(TemplateView):
#     template_name = "myauth/about-me.html"
class AboutMeView(UpdateView):
    model = Profile
    fields = ['avatar']
    template_name = 'myauth/about-me.html'
    success_url = reverse_lazy('myauth:about-me')

    def get_object(self, queryset=None):
        if hasattr(self.request.user, 'profile'):
            return self.request.user.profile
        return self.request.user

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class ProfileListView(ListView):
    model = Profile
    template_name = 'myauth/profile_list.html'
    context_object_name = "profiles"

    def get_object(self, queryset=None):
        super().get_object(queryset=queryset)
        return self.request.user.profile

# class ProfileDetailView(DetailView):
#     template_name = 'myauth/profile_details.html'
#     context_object_name = "user"
#     queryset = User.objects.all()
class ProfileDetailView(UserPassesTestMixin, DetailView, UpdateView):
    def test_func(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.user.profile.user.username == self.request.user.username or self.request.user.is_staff:
            return self.request.user.username

    model = Profile
    fields = ['avatar']
    template_name = 'myauth/profile_details.html'
    success_url = reverse_lazy('myauth:profile_list')

class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")

@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response

def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")

@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")

@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f'Session value: {value!r}')

class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})


# """ Avatar """
# class UpdateAvatarView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         avatar = request.FILES.get('avatar')
#         if avatar:
#             request.user.profile.avatar = avatar
#             request.user.profile.save()
#         return redirect('myauth:about-me')
#
#     def get(self, request, *args, **kwargs):
#         return redirect('myauth:about-me')

# @login_required
# def update_avatar(request):
#     if request.method == 'POST':
#         avatar = request.FILES.get('avatar')
#         if avatar:
#             request.user.profile.avatar = avatar
#             request.user.profile.save()
#             messages.success(request, 'Your avatar has been updated!')
#         else:
#             messages.error(request, 'Please select an avatar image to upload.')
#
#         return redirect('myauth:about-me')
#     else:
#         return redirect('myauth:about-me')

# def login_view(request: HttpRequest) -> HttpResponse:
#     if request.method == "GET":
#         if request.user.is_authenticated:
#             return redirect('/admin/')
#         return render(request, 'myauth/login.html')
#
#     username = request.POST['username']
#     password = request.POST['password']
#
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return redirect("/admin/")
#     return render(request, 'myauth/login.html', {"error": "Invalid login credentials"})
#
# def logout_view(request: HttpRequest):
#     logout(request)
#     return redirect(reverse("myauth:login"))