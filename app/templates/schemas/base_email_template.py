from abc import ABC

import app.templates.utils as _utils

from .base_template import BaseTemplate


class BaseEmailTemplate(BaseTemplate, ABC):
    pipeline = (
        _utils.mjml_renderer,
        _utils.css_inliner,
        _utils.css_attr_unpacker,
        _utils.minifier,
    )
