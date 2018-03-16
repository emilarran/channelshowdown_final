from django.conf.urls import url
from .views import (
    RegistrationView,
    LoginView,
    LogoutView,
    EditUserView,
    UserProfileView,
)


urlpatterns = [
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^edituser/$', EditUserView.as_view(), name='edituser'),
    url(r'^userprofile/$', UserProfileView.as_view(), name='userprofile'),
]
