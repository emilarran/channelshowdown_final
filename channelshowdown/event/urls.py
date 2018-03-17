from django.conf.urls import url
from .views import (
    CreateEventView,
    UpcomingEventsView,
    OngoingEventsView,
    FinishedEventsView
)

urlpatterns = [
    url(r'^createevent/$', CreateEventView.as_view(), name='createevent'),
    url(r'^upcomingevents/$',
        UpcomingEventsView.as_view(),
        name='upcomingevents'),
    url(r'^ongoingevents/$',
        OngoingEventsView.as_view(),
        name='ongoingevents'),
    url(r'^finishedevents/$',
        FinishedEventsView.as_view(),
        name='finishedevents'),
]
