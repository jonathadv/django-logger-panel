from django.urls import path

from django_logger_panel.views import LoggingDetailView, LoggerListView
from django_logger_panel import BASE_URL_WITHOUT_LEADING_SLASH

BASE_URL = BASE_URL_WITHOUT_LEADING_SLASH

urlpatterns = [
    path(f"{BASE_URL}", LoggerListView.as_view(), name="loggerpanel-list"),
    path(
        f"{BASE_URL}<str:log_name>",
        LoggingDetailView.as_view(),
        name="loggerpanel-detail",
    ),
]
