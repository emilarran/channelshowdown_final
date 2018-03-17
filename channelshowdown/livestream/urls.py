from django.conf.urls import url
from .views import StartLiveStreamView
from .views import GetTokenPublisherView, GetTokenSubscriberView

urlpatterns = [
    url(r'^startlivestream/$', StartLiveStreamView.as_view(), name='session'),
    url(r'^gettokenpublisher/$',
        GetTokenPublisherView.as_view(),
        name='publisher'),
    url(r'^gettokensubscriber/$',
        GetTokenSubscriberView.as_view(),
        name='subscriber'),

]