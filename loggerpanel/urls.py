from django.urls import path

from loggerpanel.views import LoggingDetailView, LoggerListView
from loggerpanel import BASE_URL_WITHOUT_LEADING_SLASH

BASE_URL = BASE_URL_WITHOUT_LEADING_SLASH

urlpatterns = [
    path(f"{BASE_URL}", LoggerListView.as_view(), name="loggerpanel-list"),
    path(
        f"{BASE_URL}<str:log_name>",
        LoggingDetailView.as_view(),
        name="loggerpanel-detail",
    ),
]
