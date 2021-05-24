import logging
from django import forms
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from . import BASE_URL
from .loggerpanel import LEVELS, set_logger_level, get_all_loggers, get_all_log_level

LOGGER = logging.getLogger(__name__)


class SetLoggerLevelForm(forms.Form):
    log_level = forms.CharField()
    log_name = forms.CharField()


class LoggerListView(FormView):
    template_name = "loggerpanel/loggers.html"
    form_class = SetLoggerLevelForm
    success_url = BASE_URL

    def form_invalid(self, form):
        LOGGER.debug("Form is invalid! Form content: %s", form)
        response = super().form_invalid(form)
        return response

    def form_valid(self, form):
        logger_name = form.cleaned_data["log_name"]
        logger_level = form.cleaned_data["log_level"]
        try:
            LOGGER.debug(
                "Setting logger_level='%s' to logger_name='%s'",
                logger_level,
                logger_name,
            )
            set_logger_level(logger_name, logger_level)
        except Exception as err:
            LOGGER.error(
                "Error while setting logger_level='%s' to logger_name='%s'",
                logger_level,
                logger_name,
                stack_info=True,
            )
            raise ValidationError(err) from err

        return super(LoggerListView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["loggerdict"] = get_all_loggers()
        context["all_log_level"] = get_all_log_level()
        context["log_levels"] = LEVELS
        context["base_url"] = BASE_URL
        return context


class LoggingDetailView(TemplateView):
    template_name = "loggerpanel/detail.html"

    def get_context_data(self, log_name=None, **kwargs):
        context = super().get_context_data(**kwargs)
        loggers = get_all_loggers()
        context["log_name"] = log_name
        context["logger"] = loggers.get(log_name)
        context["base_url"] = BASE_URL
        return context
