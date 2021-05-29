import logging
from typing import List, Dict
from django import forms
from django.core.exceptions import ValidationError
from django.views.generic import FormView, TemplateView

from . import BASE_URL
from .__version__ import __version__
from .loggerpanel import LEVELS, set_logger_level, get_all_loggers, get_all_log_level

LOGGER = logging.getLogger(__name__)


class SetLoggerLevelForm(forms.Form):
    """SetLoggerLevelForm"""

    log_level = forms.CharField()
    log_name = forms.CharField()


class LoggerBaseView(TemplateView):
    """The base class for Views in Logger Panel"""

    def get_breadcrumbs(self) -> List[Dict[str, str]]:
        """Creates a list of dicts to work as breadcrumbs"""
        breadcrumbs = []
        crumbs = [v for v in self.request.path.split("/") if v]
        while crumbs:
            breadcrumbs.insert(
                0,
                {"url": f"/{'/'.join(crumbs)}", "name": crumbs.pop(), "is_last": False},
            )
        breadcrumbs[-1]["is_last"] = True
        return breadcrumbs

    def get_context_data(self, **kwargs):
        """
        Adds `base_url`, `project_version` and `breadcrumbs` to the common context.
        """
        base_context = {
            "base_url": BASE_URL,
            "project_version": __version__,
            "breadcrumbs": self.get_breadcrumbs(),
        }
        context: dict = super().get_context_data(**kwargs)
        context.update(base_context)
        return context


class LoggerListView(FormView, LoggerBaseView):
    """
    View to List the loggers
    """

    template_name = "loggerpanel/loggers.html"
    form_class = SetLoggerLevelForm
    success_url = BASE_URL

    def form_invalid(self, form):
        """Logs if the form is invalid"""
        LOGGER.debug("Form is invalid! Form content: %s", form)
        response = super().form_invalid(form)
        return response

    def form_valid(self, form):
        """Calls the `set_logger_level()` function with the arguments received in the `form`"""
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

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Adds `loggers`, `all_log_level` and `log_levels` to the context"""
        context: dict = super().get_context_data(**kwargs)
        context["loggers"] = get_all_loggers()
        context["all_log_level"] = get_all_log_level()
        context["log_levels"] = LEVELS
        return context


class LoggingDetailView(LoggerBaseView):
    """View to display the details of a specific logger instance"""

    template_name = "loggerpanel/detail.html"

    def get_context_data(self, **kwargs):
        """Adds `log_name` and `logger` instance to the context"""
        log_name = kwargs.get("log_name")
        context: dict = super().get_context_data(**kwargs)
        loggers = get_all_loggers()
        context["log_name"] = log_name
        context["logger"] = loggers.get(log_name)
        return context
