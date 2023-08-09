from django.contrib.auth.views import LoginView
from django.urls import path

from . import views
from .views import (
    get_cookie_view,
    set_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
    AboutMeView,
    RegisterView,
    FooBarView,
    # UpdateAvatarView,
    ProfileListView,
    ProfileDetailView,
)

app_name = "myauth"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("register/", RegisterView.as_view(), name="register"),
    # path("update_avatar/", UpdateAvatarView.as_view(), name="update_avatar"),
    path("profile_list/", ProfileListView.as_view(), name="profile_list"),
    path("profile_list/<int:pk>/", ProfileDetailView.as_view(), name="profile_details"),

    path("cookie/get/", get_cookie_view, name="cookie-get"),
    path("cookie/set/", set_cookie_view, name="cookie-set"),

    path("session/get/", get_session_view, name="session-get"),
    path("session/set/", set_session_view, name="session-set"),

    path("foo-bar/", FooBarView.as_view(), name="foo-bar"),
]