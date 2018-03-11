from django.conf.urls import url
from .views import RegistrationView, LoginView, LogoutView

urlpatterns = [
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
]