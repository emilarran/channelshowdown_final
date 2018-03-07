from django.conf.urls import url
from . import views
from .views import StartLiveStreamView
from .views import GetTokenPublisher, GetTokenSubscriber

urlpatterns = [
    url(r'^startlivestream/$', StartLiveStreamView.as_view(), name='session'),
    url(r'^gettokenpublisher/$',
        GetTokenPublisher.as_view(),
        name='publisher'),
    url(r'^gettokensubscriber/$',
        GetTokenSubscriber.as_view(),
        name='subscriber'),

]