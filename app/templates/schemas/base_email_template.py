from abc import ABC

import app.templates.utils as _utils

from .base_template import BaseTemplate


class BaseEmailTemplate(BaseTemplate, ABC):
    pipeline = (_utils.render_mjml,)
