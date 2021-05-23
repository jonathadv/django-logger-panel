from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.template import loader
from logging import Logger, PlaceHolder, CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET

LEVELS = {
    'CRITICAL': CRITICAL,
    'ERROR': ERROR,
    'WARNING': WARNING,
    'INFO': INFO,
    'DEBUG': DEBUG,
    'NOTSET': NOTSET,
}

from django.views.generic.edit import FormView
from django import forms


class ContactForm(forms.Form):
    loglevel = forms.CharField()
    logname = forms.CharField()


class LoggingListView(FormView):
    template_name = "loggingpanel/logging.html"
    form_class = ContactForm
    success_url = '/logging/'

    def form_invalid(self, form):
        print(f"#############INVALID")
        response = super().form_invalid(form)
        return response

    def form_valid(self, form):
        loglevel = form.cleaned_data["loglevel"]
        logname = form.cleaned_data["logname"]
        if logname == "ALL":
            for _, logger in Logger.manager.loggerDict.items():
                print(f"########### logger: {logger}")
                if not isinstance(logger, PlaceHolder):
                    logger.setLevel(loglevel)
        else:
            Logger.manager.loggerDict.get(logname).setLevel(loglevel)
        return super(LoggingListView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loggerdict'] = {k: v for k, v in Logger.manager.loggerDict.items() if not isinstance(v, PlaceHolder)}
        context['log_levels'] = LEVELS
        return context


class LoggingDetailView(TemplateView):
    template_name = "loggingpanel/detail.html"

    def get_context_data(self, logname=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logname'] = logname
        context['logger'] = Logger.manager.loggerDict.get(logname)
        return context

