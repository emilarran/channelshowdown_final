from django.conf.urls import url
from .views import CreateEventView

urlpatterns = [
    url(r'^createevent/$', CreateEventView.as_view(), name='createevent'),
]