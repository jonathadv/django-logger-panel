"""
URLConf for test suite.
"""
from django.urls import path, include


urlpatterns = [
    path("", include("django_logger_panel.urls")),
]
