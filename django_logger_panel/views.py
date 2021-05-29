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
    def get_breadcrumbs(self):
        breadcrumbs = []
        crumbs = [v for v in self.request.path.split("/") if v]
        while crumbs:
            breadcrumbs.insert(0, {"url": f"/{'/'.join(crumbs)}", "name": crumbs.pop(), "is_last": False})
        breadcrumbs[-1]["is_last"] = True
        return breadcrumbs

    def get_context_data(self, **kwargs):
        base_context = {
            "base_url": BASE_URL,
            "project_version": __version__,
            "breadcrumbs": self.get_breadcrumbs()
        }
        context: dict = super().get_context_data(**kwargs)
        context.update(base_context)
        return context


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
        context["loggers"] = get_all_loggers()
        context["all_log_level"] = get_all_log_level()
        context["log_levels"] = LEVELS
        return context


class LoggingDetailView(LoggerBaseView):
    template_name = "loggerpanel/detail.html"

    def get_context_data(self, log_name=None, **kwargs):
        context: dict = super().get_context_data(**kwargs)
        loggers = get_all_loggers()
        context["log_name"] = log_name
        context["logger"] = loggers.get(log_name)
        return context
