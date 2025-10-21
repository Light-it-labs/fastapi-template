from pydantic import BaseModel, EmailStr

from app.emails.schema.email import Email


class _Recipient(BaseModel):
    """
    Represents an email recipient with an email and an optional name.
    Used for 'From', 'To', 'Cc', and 'ReplyTo' fields.
    """

    Email: EmailStr
    """Email address of the recipient."""
    Name: str | None = None
    """Optional name of the recipient."""


class _Attachment(BaseModel):
    """
    Represents a single file attachment.
    """

    Content: str
    """Base64-encoded string of the file content."""
    Filename: str
    """The filename of the attachment."""
    ContentID: str | None = None
    """Optional Content-ID (cid) for inline attachments."""
    ContentType: str | None = None
    """Optional content type. If empty, it's auto-detected."""


class _MailpitEmailSchema(BaseModel):
    """
    Defines the JSON schema for sending an email via Mailpit.
    """

    From: _Recipient
    """The sender of the email."""
    To: list[_Recipient] = []
    """'To' recipients."""

    Subject: str | None = None
    """The email subject line."""
    HTML: str | None = None
    """The HTML body of the message."""
    Text: str | None = None
    """The plain text body of the message."""

    Cc: list[_Recipient] | None = None
    """'Cc' recipients."""
    Bcc: list[EmailStr] | None = None
    """'Bcc' recipients (email only)."""
    ReplyTo: list[_Recipient] | None = None
    """Optional 'Reply-To' recipients."""

    Headers: dict[str, str] | None = None
    """Optional headers in key:value format."""
    Attachments: list[_Attachment] | None = None
    """A list of attachments."""
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
