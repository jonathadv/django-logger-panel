import logging

from django import forms
from django.core.exceptions import ValidationError
from django.views.generic import FormView, TemplateView

from . import BASE_URL
from .__version__ import __version__
from .loggerpanel import LEVELS, set_logger_level, get_all_loggers, get_all_log_level

LOGGER = logging.getLogger(__name__)


class SetLoggerLevelForm(forms.Form):
    log_level = forms.CharField()
    log_name = forms.CharField()


class LoggerBaseView(TemplateView):
    _first_crumb = {"url": BASE_URL, "name": "Loggers", "is_last": True}

    def get_context_data(self, **kwargs):
        base_context = {
            "base_url": BASE_URL,
            "project_version": __version__,
            "breadcrumb": self.get_base_breadcrumb()
        }
        context: dict = super().get_context_data(**kwargs)
        context.update(base_context)
        return context

    def set_breadcrumb(self, context: dict, url: str, name: str):
        crumb = {"url": url, "name": name, "is_last": True}
        context["breadcrumb"] = self.get_base_breadcrumb()
        context["breadcrumb"][0]["is_last"] = False
        context["breadcrumb"].append(crumb)

    def get_base_breadcrumb(self):
        return [dict(self._first_crumb)]


class LoggerListView(FormView, LoggerBaseView):
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
        context: dict = super().get_context_data(**kwargs)
        context["loggerdict"] = get_all_loggers()
        context["all_log_level"] = get_all_log_level()
        context["log_levels"] = LEVELS
        return context


class LoggingDetailView(LoggerBaseView):
    template_name = "loggerpanel/detail.html"

    def get_context_data(self, log_name=None, **kwargs):
        context: dict = super().get_context_data(**kwargs)
        self.set_breadcrumb(context, log_name, log_name)
        loggers = get_all_loggers()
        context["log_name"] = log_name
        context["logger"] = loggers.get(log_name)
        return context
