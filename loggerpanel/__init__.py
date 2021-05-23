import re
import logging
from django.conf import settings

LOGGER = logging.getLogger(__name__)

_DEFAULT_BASE_URL = "/loggers/"

if hasattr(settings, "LOGGING_PANEL_BASE_URL"):
    BASE_URL = settings.LOGGING_PANEL_BASE_URL
    LOGGER.debug("Using settings.LOGGING_PANEL_BASE_URL='%s' as BASE_URL", BASE_URL)
else:
    BASE_URL = _DEFAULT_BASE_URL
    LOGGER.debug("Using default value '%s' as BASE_URL", BASE_URL)

# Used by urls.py
BASE_URL_WITHOUT_LEADING_SLASH = re.sub(f"^/", "", BASE_URL)