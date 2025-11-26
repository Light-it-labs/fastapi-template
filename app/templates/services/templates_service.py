import itertools
from typing import ClassVar

import jinja2

from app.templates import exceptions, schemas, types


class TemplatesService:
    ENVIRONMENT: ClassVar[jinja2.Environment] = jinja2.Environment(
        loader=jinja2.FileSystemLoader("assets/templates/"),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    def __init__(
        self,
        *,
        environment: jinja2.Environment | None = None,
        pipeline: types.ProcessingPipeline | None = None,
    ) -> None:
        self._environment = environment or self.ENVIRONMENT
        self._pipeline = pipeline

    def render(
        self,
        template: schemas.BaseTemplate,
        *,
        pipeline: types.ProcessingPipeline | None = None,
    ) -> str:
        path, args = template.get_path(), template.get_args()

        try:
            jinja_template = self._environment.get_template(path)
        except jinja2.exceptions.TemplateNotFound:
            raise exceptions.InvalidTemplatePathException(template)

        rendered_template = jinja_template.render(**args)

        for processor in itertools.chain(
            template.get_pipeline(),
            pipeline or [],
            self._pipeline or [],
        ):
            rendered_template = processor(rendered_template)

        return rendered_template
