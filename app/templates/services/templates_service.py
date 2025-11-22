import itertools
from typing import ClassVar

import jinja2


import app.templates.types as _types
import app.templates.schemas as _schemas


class TemplatesService:
    DEFAULT_ENVIRONMENT: ClassVar[jinja2.Environment] = jinja2.Environment(
        loader=jinja2.FileSystemLoader("assets/templates/"),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    def __init__(
        self,
        *,
        environment: jinja2.Environment | None = None,
        pipeline: _types.PostProcessingPipeline | None = None,
    ) -> None:
        self._jinja_environment = environment or self.DEFAULT_ENVIRONMENT
        self._pipeline = pipeline

    def render(
        self,
        template: _schemas.BaseTemplate,
        *,
        pipeline: _types.PostProcessingPipeline | None = None,
    ) -> str:
        jinja_template = self.DEFAULT_ENVIRONMENT.get_template(template.path)
        rendered_template = jinja_template.render(**template.get_args())

        for processor in itertools.chain(
            template.pipeline,
            pipeline or [],
            self._pipeline or [],
        ):
            rendered_template = processor(rendered_template)

        return rendered_template
