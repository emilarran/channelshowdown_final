from django.conf.urls import url
from .views import (
    StartLiveStreamView,
    GetTokenPublisherView,
    GetTokenSubscriberView,
    VoteView,
    StartArchiveView,
    EndEventView,
    SavedVideoView
)

urlpatterns = [
    url(r'^startlivestream/$', StartLiveStreamView.as_view(), name='session'),
    url(r'^gettokenpublisher/$',
        GetTokenPublisherView.as_view(),
        name='publisher'),
    url(r'^gettokensubscriber/$',
        GetTokenSubscriberView.as_view(),
        name='subscriber'),
    url(r'^vote/$', VoteView.as_view(), name='vote'),
    url(r'^startarchive/$', StartArchiveView.as_view(), name='startarchive'),
    url(r'^endevent/$', EndEventView.as_view(), name='endevent'),
    url(r'^savedvideo/$',
        SavedVideoView.as_view(),
        name='savedvideos'),
]
