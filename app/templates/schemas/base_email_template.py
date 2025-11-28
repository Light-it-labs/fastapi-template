from abc import ABC

from app.templates import utils

from .base_template import BaseTemplate


class BaseEmailTemplate(
    BaseTemplate,
    ABC,
    pipeline=(utils.render_mjml,),
):
    pass
