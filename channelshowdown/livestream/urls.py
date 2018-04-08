from django.conf.urls import url
from .views import (
    StartLiveStreamView,
    GetTokenPublisherView,
    GetTokenSubscriberView,
    VoteView
)

urlpatterns = [
    url(r'^startlivestream/$', StartLiveStreamView.as_view(), name='session'),
    url(r'^gettokenpublisher/$',
        GetTokenPublisherView.as_view(),
        name='publisher'),
    url(r'^gettokensubscriber/$',
        GetTokenSubscriberView.as_view(),
        name='subscriber'),
    url(r'^vote/$', VoteView.as_view(), name='vote')
]
