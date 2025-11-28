from app import templates


class NewUserTemplate(templates.BaseEmailTemplate, path="new_user_email.j2"):
    name: str
