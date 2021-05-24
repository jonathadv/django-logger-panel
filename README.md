# django-logger-panel
 
An easy way to change the log level in runtime


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
    'loggerpanel',    
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
    path("", include("loggerpanel.urls")),
    ...

]
```

## Screenshots

### Logger Panel

![logger panel](https://raw.githubusercontent.com/jonathadv/django-logger-panel/main/docs/img/loggers.png)


### Logger Details

![logger details](https://raw.githubusercontent.com/jonathadv/django-logger-panel/main/docs/img/logger-detail.png)