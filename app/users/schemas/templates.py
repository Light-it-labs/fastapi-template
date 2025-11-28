from app import templates


class NewUserTemplate(templates.BaseEmailTemplate, path="new_user_email.mjml"):
    name: str
