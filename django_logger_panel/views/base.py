from typing import List, Dict

from django.views.generic import TemplateView
from django_logger_panel import BASE_URL
from django_logger_panel.__version__ import __version__

BASE_URL_KEY = "base_url"
PROJECT_VERSION_KEY = "project_version"
BREADCRUMBS_KEY = "breadcrumbs"


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
            BASE_URL_KEY: BASE_URL,
            PROJECT_VERSION_KEY: __version__,
            BREADCRUMBS_KEY: self.get_breadcrumbs(),
        }
        context: dict = super().get_context_data(**kwargs)
        context.update(base_context)
        return context

    def render_to_response(self, context, **response_kwargs):
        """Check the accept header and calls the proper render function"""
        if self.request.META.get("HTTP_ACCEPT") == "application/json":
            return self.render_to_json_response(context)
        return super().render_to_response(context, **response_kwargs)

    def render_to_json_response(self, context: dict):
        """Each class should implement its own way
        to render the JSON response.
        """
        raise NotImplementedError()
