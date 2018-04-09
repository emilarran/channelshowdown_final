from django.conf.urls import url
from .views import (
    StartLiveStreamView,
    GetTokenPublisherView,
    GetTokenSubscriberView,
    VoteView,
    StartArchiveView,
    StopArchiveView,
    EndEventView,
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
    url(r'^stoparchive/$', StopArchiveView.as_view(), name='stoparchive'),
    url(r'^endevent/$', EndEventView.as_view(), name='endevent'),
]
