import json
import logging

from django.http import JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django_logger_panel import BASE_URL
from django_logger_panel.core import LEVELS, set_logger_level, get_all_loggers
from django_logger_panel.serializers import (
    logger_response_serializer,
    logger_serializer,
)
from django_logger_panel.views.base import LoggerBaseView

LOGGER = logging.getLogger(__name__)

LOGGERS_KEY = "loggers"
LOGGER_NAME_KEY = "logger_name"
LOGGER_LEVEL_KEY = "logger_level"
LOGGER_LEVELS_KEY = "logger_levels"
LOGGER_INSTANCE_KEY = "logger"
ERROR_KEY = "error"


class LoggerListView(LoggerBaseView):
    """
    View to List the loggers
    """

    template_name = "loggerpanel/loggers.html"
    success_url = BASE_URL

    def post(self, request, *_args, **kwargs):
        """Calls the `set_logger_level()` function with the arguments received in the `form`"""
        logger_name = request.POST.get(LOGGER_NAME_KEY)
        logger_level = request.POST.get(LOGGER_LEVEL_KEY)
        try:
            set_logger_level(logger_name, logger_level)
            return HttpResponseRedirect(self.success_url)
        except Exception as err:
            LOGGER.error(err)
            context = self.get_context_data(**kwargs)
            context[ERROR_KEY] = str(err)
            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """Adds `loggers` and `logger_levels` to the context"""
        context: dict = super().get_context_data(**kwargs)
        context[LOGGERS_KEY] = get_all_loggers()
        context[LOGGER_LEVELS_KEY] = LEVELS
        return context

    def render_to_json_response(self, context: dict):
        """Renders `logger_levels` and `loggers` as JSON"""
        data = logger_response_serializer(context["logger_levels"], context["loggers"])
        return JsonResponse(data)


@method_decorator(csrf_exempt, name="dispatch")
class LoggingDetailView(LoggerBaseView):
    """View to display the details of a specific logger instance"""

    template_name = "loggerpanel/detail.html"

    def post(self, request, *_args, **kwargs):
        """Handles the details for a logger instance"""
        try:
            logger_name = kwargs.get(LOGGER_NAME_KEY)
            logger_level = json.loads(request.body)[LOGGER_LEVEL_KEY]

            set_logger_level(logger_name, logger_level)
            data = logger_serializer(get_all_loggers()[logger_name])
            return JsonResponse(data)
        except KeyError as err:
            LOGGER.error(err)
            return JsonResponse({ERROR_KEY: f"missing argument {err}"}, status=400)
        except Exception as err:
            LOGGER.error(err)
            return JsonResponse({ERROR_KEY: str(err)}, status=400)

    def get_context_data(self, **kwargs):
        """Adds `logger_name` and a `Logger` instance to the context"""

        logger_name = kwargs.get(LOGGER_NAME_KEY)
        context: dict = super().get_context_data(**kwargs)
        loggers = get_all_loggers()
        context[LOGGER_NAME_KEY] = logger_name
        context[LOGGER_INSTANCE_KEY] = loggers.get(logger_name)
        return context

    def render_to_json_response(self, context: dict):
        """Renders a `Logger` instance as JSON"""

        data = logger_serializer(context[LOGGER_INSTANCE_KEY])
        return JsonResponse(data)
