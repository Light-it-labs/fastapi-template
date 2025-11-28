import mjml


def render_mjml(input: str) -> str:
    return mjml.mjml2html(input, disable_comments=True)
