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

## REST API

### List loggers

**Curl Example:**

```bash
curl http://localhost:8000/loggers/ -H 'Accept:application/json'
```

**Response:**

```json
{
  "log_levels": {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
    "NOTSET": 0
  },
  "loggers": [
    {
      "name": "_all_loggers_",
      "level": {
        "code": 0,
        "name": "NOTSET"
      },
      "effectiveLevel": {
        "code": 0,
        "name": "NOTSET"
      },
      "parent": null
    },
    {
      "name": "root",
      "level": {
        "code": 30,
        "name": "WARNING"
      },
      "effectiveLevel": {
        "code": 30,
        "name": "WARNING"
      },
      "parent": null
    },
    {
      "name": "django",
      "level": {
        "code": 20,
        "name": "INFO"
      },
      "effectiveLevel": {
        "code": 20,
        "name": "INFO"
      },
      "parent": "root"
    },
    {
      "name": "django.db.backends",
      "level": {
        "code": 0,
        "name": "NOTSET"
      },
      "effectiveLevel": {
        "code": 20,
        "name": "INFO"
      },
      "parent": "django"
    },
    {
      "name": "django.request",
      "level": {
        "code": 0,
        "name": "NOTSET"
      },
      "effectiveLevel": {
        "code": 20,
        "name": "INFO"
      },
      "parent": "django"
    },
    {
      "name": "django.server",
      "level": {
        "code": 20,
        "name": "INFO"
      },
      "effectiveLevel": {
        "code": 20,
        "name": "INFO"
      },
      "parent": "django"
    },
    {
      "name": "django.security.csrf",
      "level": {
        "code": 0,
        "name": "NOTSET"
      },
      "effectiveLevel": {
        "code": 20,
        "name": "INFO"
      },
      "parent": "django"
    },
    {
      "name": "django.db.backends.schema",
      "level": {
        "code": 0,
        "name": "NOTSET"
      },
      "effectiveLevel": {
        "code": 20,
        "name": "INFO"
      },
      "parent": "django.db.backends"
    }    
  ]
}


```

### Return a single logger

**Curl Example:**

```bash
curl http://localhost:8000/loggers/django.db.backends -H 'Accept:application/json'
```

**Response:**

```json
{
  "name": "django.db.backends",
  "level": {
    "code": 0,
    "name": "NOTSET"
  },
  "effectiveLevel": {
    "code": 20,
    "name": "INFO"
  },
  "parent": "django"
}
```

### Change logger level

**Curl Example:**

```bash
curl -X POST http://localhost:8000/loggers/django.db.backends -d '{"logger_level": "DEBUG"}'
```

**Response:**

```json
{
  "name": "django.db.backends",
  "level": {
    "code": 10,
    "name": "DEBUG"
  },
  "effectiveLevel": {
    "code": 10,
    "name": "DEBUG"
  },
  "parent": "django"
}
```