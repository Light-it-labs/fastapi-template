from pydantic import BaseModel, EmailStr

from app.emails.schema.email import Email


class _Recipient(BaseModel):
    Email: EmailStr
    Name: str | None = None


class _Attachment(BaseModel):
    Content: str
    """Base64-encoded string of the file content."""
    Filename: str
    ContentID: str | None = None
    """Optional Content-ID (cid) for inline attachments."""
    ContentType: str | None = None
    """Optional content type. If empty, it's auto-detected."""


class _MailpitEmailSchema(BaseModel):
    From: _Recipient
    To: list[_Recipient] = []

    Subject: str | None = None
    HTML: str | None = None
    Text: str | None = None

    Cc: list[_Recipient] | None = None
    Bcc: list[EmailStr] | None = None
    ReplyTo: list[_Recipient] | None = None

    Headers: dict[str, str] | None = None
    Attachments: list[_Attachment] | None = None
    Tags: list[str] | None = None
    """Optional Mailpit tags for categorization."""

    @classmethod
    def from_email(cls, email: Email) -> "_MailpitEmailSchema":
        if email.headers:
            sanitized_headers = email.headers.copy()
            for mailpit_forbidden_header in (
                "MIME-Version",
                "Content-Type",
            ):
                if mailpit_forbidden_header in sanitized_headers:
                    del sanitized_headers[mailpit_forbidden_header]
        else:
            sanitized_headers = None

        return cls(
            From=_Recipient(
                Email=email.from_email,
                Name=email.from_name,
            ),
            To=[_Recipient(Email=to_email) for to_email in email.to_emails],
            Cc=[_Recipient(Email=to_email) for to_email in email.cc_emails],
            Bcc=[_Recipient(Email=to_email) for to_email in email.bcc_emails],
            Subject=email.subject,
            Headers=sanitized_headers,
            HTML=email.html,
        )
