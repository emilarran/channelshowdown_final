from django.conf.urls import url
from .views import RegistrationView

urlpatterns = [
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),
]