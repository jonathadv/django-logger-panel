import json
import logging

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from django_logger_panel import BASE_URL
from django_logger_panel.core import LEVELS, set_logger_level, get_all_loggers
from django_logger_panel.serializers import (
    logger_response_serializer,
    logger_serializer,
)
from django_logger_panel.views.base import LoggerBaseView
from django_logger_panel.views.forms import SetLoggerLevelForm

LOGGER = logging.getLogger(__name__)


class LoggerListView(FormView, LoggerBaseView):
    """
    View to List the loggers
    """

    template_name = "loggerpanel/loggers.html"
    form_class = SetLoggerLevelForm
    success_url = BASE_URL

    def form_invalid(self, form):
        """Logs if the form is invalid"""
        LOGGER.error("Form is invalid! Form content: %s", form)
        response = super().form_invalid(form)
        return response

    def form_valid(self, form):
        """Calls the `set_logger_level()` function with the arguments received in the `form`"""
        logger_name = form.cleaned_data["log_name"]
        logger_level = form.cleaned_data["log_level"]
        try:
            set_logger_level(logger_name, logger_level)
        except Exception as err:
            raise ValidationError(err) from err

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Adds `loggers` and `log_levels` to the context"""
        context: dict = super().get_context_data(**kwargs)
        context["loggers"] = get_all_loggers()
        context["log_levels"] = LEVELS
        return context

    def render_to_json_response(self, context: dict):
        """Renders `log_levels` and `loggers` as JSON"""
        data = logger_response_serializer(context["log_levels"], context["loggers"])
        return JsonResponse(data)


@method_decorator(csrf_exempt, name="dispatch")
class LoggingDetailView(LoggerBaseView):
    """View to display the details of a specific logger instance"""

    template_name = "loggerpanel/detail.html"

    def post(self, request, *_args, **kwargs):
        logger_name = kwargs.get("log_name")
        logger_level = json.loads(request.body)["level"]
        try:
            set_logger_level(logger_name, logger_level)
            data = logger_serializer(get_all_loggers()[logger_name])
            return JsonResponse(data)
        except Exception as err:
            return JsonResponse({"error": str(err)}, status=400)

    def get_context_data(self, **kwargs):
        """Adds `log_name` and `logger` instance to the context"""

        log_name = kwargs.get("log_name")
        context: dict = super().get_context_data(**kwargs)
        loggers = get_all_loggers()
        context["log_name"] = log_name
        context["logger"] = loggers.get(log_name)
        return context

    def render_to_json_response(self, context: dict):
        """Renders a `logger` as JSON"""

        data = logger_serializer(context["logger"])
        return JsonResponse(data)
