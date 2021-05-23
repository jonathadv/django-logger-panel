from django.urls import path

from loggingpanel.views import LoggingDetailView, LoggingListView

urlpatterns = [
    path('logging/', LoggingListView.as_view(), name='logging-list'),
    path('logging/<str:logname>', LoggingDetailView.as_view(), name='logging-detail'),
]
