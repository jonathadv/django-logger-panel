from django import forms


class SetLoggerLevelForm(forms.Form):
    """SetLoggerLevelForm"""

    levels = forms.CharField()
    log_names = forms.CharField()
