from django.conf.urls import url
from . import views
from .views import StartLiveStreamView

urlpatterns = [
    url(r'^startlivestream/$', StartLiveStreamView.as_view(), name=''),
]