from django.conf.urls import url
from . import views
from .views import StartLiveStreamView, GetTokenModerator

urlpatterns = [
    url(r'^startlivestream/$', StartLiveStreamView.as_view(), name=''),
    url(r'^gettokenmoderator/$', GetTokenModerator.as_view(), name=''),
]