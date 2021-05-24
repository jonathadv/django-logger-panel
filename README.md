[![pypi version](https://img.shields.io/pypi/v/django-logger-panel.svg)](https://pypi.python.org/pypi/django-logger-panel) 
[![license](https://img.shields.io/pypi/l/django-logger-panel.svg)](https://pypi.python.org/pypi/django-logger-panel) 
[![python versions](https://img.shields.io/pypi/pyversions/django-logger-panel.svg)](https://pypi.python.org/pypi/django-logger-panel) 
[![contributors](https://img.shields.io/github/contributors/jonathadv/django-logger-panel.svg)](https://github.com/jonathadv/django-logger-panel/graphs/contributors) 


# django-logger-panel
 
An easy way to change the log level in runtime


## Installation

`pip install django-logger-panel`

## Features
- List all active loggers .
- Change any logger level in run time.
- Change all logger levels at once.
- Display logger information.


## Settings.py


Add `loggerpanel` to installed apps

```python
INSTALLED_APPS = [
    ...
    'django_logger_panel',    
]
```

Optionally, change the default base url `/loggers/` by setting the property `LOGGER_PANEL_BASE_URL`.


```
LOGGER_PANEL_BASE_URL = "/another-path/"
```

## urls.py

```python
urlpatterns = [
    ...
    path("", include("django_logger_panel.urls")),
    ...

]
```

## Screenshots

### Logger Panel

![logger panel](https://raw.githubusercontent.com/jonathadv/django-logger-panel/main/docs/img/loggers.png)


### Logger Details

![logger details](https://raw.githubusercontent.com/jonathadv/django-logger-panel/main/docs/img/logger-detail.png)