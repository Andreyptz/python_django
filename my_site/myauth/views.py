from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.contrib import messages

from my_site import settings

class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")

def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response

def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r}")

def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")

def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f'Session value: {value!r}')

# class MyLoginView(LoginView):
#     def get_success_url(self):
#         return resolve_url(settings.LOGIN_REDIRECT_URL)
#
#     def form_invalid(self, form):
#         messages.error(self.request, 'Invalid username or password')
#         return self.render_to_response(self.get_context_data(form=form))

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

# def logout_view(request: HttpRequest):
#     logout(request)
#     return redirect(reverse("myauth:login"))