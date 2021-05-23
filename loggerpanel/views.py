from logging import Logger, PlaceHolder, CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET

from django import forms
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from loggerpanel import BASE_URL

LEVELS = {
    'CRITICAL': CRITICAL,
    'ERROR': ERROR,
    'WARNING': WARNING,
    'INFO': INFO,
    'DEBUG': DEBUG,
    'NOTSET': NOTSET,
}

ALL_LOG_LEVEL = NOTSET


class ContactForm(forms.Form):
    loglevel = forms.CharField()
    logname = forms.CharField()


class LoggingListView(FormView):
    template_name = "loggerpanel/loggers.html"
    form_class = ContactForm
    success_url = BASE_URL


    def form_invalid(self, form):
        print(f"#############INVALID")
        response = super().form_invalid(form)
        return response

    def form_valid(self, form):
        loglevel = form.cleaned_data["loglevel"]
        logname = form.cleaned_data["logname"]
        loggers = get_all_loggers()

        if logname == "ALL":
            global ALL_LOG_LEVEL
            ALL_LOG_LEVEL = LEVELS.get(loglevel, NOTSET)
            for _, logger in loggers.items():
                logger.setLevel(loglevel)
        else:
            loggers.get(logname).setLevel(loglevel)

        return super(LoggingListView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loggerdict'] = get_all_loggers()
        context['all_log_level'] = ALL_LOG_LEVEL
        context['log_levels'] = LEVELS
        context['base_url'] = BASE_URL


        return context




class LoggingDetailView(TemplateView):
    template_name = "loggerpanel/detail.html"

    def get_context_data(self, logname=None, **kwargs):
        context = super().get_context_data(**kwargs)
        loggers = loggers = get_all_loggers()
        context['logname'] = logname
        context['logger'] = loggers.get(logname)
        context['base_url'] = BASE_URL
        return context


def get_all_loggers():
    loggers = {
        "root": Logger.root,
    }
    for key, logger in Logger.manager.loggerDict.items():
        if not isinstance(logger, PlaceHolder):
            loggers[key] = logger
    return loggers
