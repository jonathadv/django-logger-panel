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

### INSTALLED_APPS
Add `loggerpanel` to installed apps

```python
INSTALLED_APPS = [
    ...
    'django_logger_panel',    
]
```

### LOGGING

Make sure the `root` has a `handler` set at the `LOGGING` dictionary in `settings.py`, as described in the [Django Documentation.](https://docs.djangoproject.com/en/3.2/topics/logging/#examples)
This is the `root` `logger` configuration and will allow all `loggers` with no `handler` to inherit it from the `root`. 

**Example:**

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)-8s %(name)-12s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },
}
```

### LOGGER_PANEL_BASE_URL
Optionally, change the default base url `/loggers/` by setting the property `LOGGER_PANEL_BASE_URL`.
This variable is not required.

```python
LOGGER_PANEL_BASE_URL = "/another-path/"
```

## urls.py

Add the `django_logger_panel.urls` to the `urlpatterns`.

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