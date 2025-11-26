from app import templates


class NewUserTemplate(templates.BaseEmailTemplate, path="base.mjml"):
    name: str
