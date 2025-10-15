from typing import Annotated, Final

from pydantic import BaseModel, EmailStr, Field
import requests

from app.common.exceptions.external_provider_exception import (
    ExternalProviderException,
)
from app.core.config import settings

from .base_email_client import BaseEmailClient


class Recipient(BaseModel):
    """
    Represents an email recipient with an email and an optional name.
    Used for 'From', 'To', 'Cc', and 'ReplyTo' fields.
    """

    Email: Annotated[
        EmailStr, Field(description="Email address of the recipient.")
    ]
    Name: Annotated[
        str | None, Field(description="Optional name of the recipient.")
    ] = None


class Attachment(BaseModel):
    """
    Represents a single file attachment.
    """

    Content: Annotated[
        str, Field(description="Base64-encoded string of the file content.")
    ]
    Filename: Annotated[
        str, Field(description="The filename of the attachment.")
    ]
    ContentID: Annotated[
        str | None,
        Field(description="Optional Content-ID (cid) for inline attachments."),
    ] = None
    ContentType: Annotated[
        str | None,
        Field(
            description="Optional content type. If empty, it's auto-detected."
        ),
    ] = None


class EmailSchema(BaseModel):
    """
    Defines the JSON schema for sending an email via Mailpit.
    """

    From: Annotated[Recipient, Field(description="The sender of the email.")]
    To: Annotated[
        list[Recipient],
        Field(default_factory=list, description='"To" recipients.'),
    ]

    Subject: Annotated[
        str | None, Field(description="The email subject line.")
    ] = None
    HTML: Annotated[
        str | None, Field(description="The HTML body of the message.")
    ] = None
    Text: Annotated[
        str | None, Field(description="The plain text body of the message.")
    ] = None

    Cc: Annotated[
        list[Recipient] | None, Field(description='"Cc" recipients.')
    ] = None
    Bcc: Annotated[
        list[EmailStr] | None,
        Field(description='"Bcc" recipients (email only).'),
    ] = None
    ReplyTo: Annotated[
        list[Recipient] | None,
        Field(description="Optional 'Reply-To' recipients."),
    ] = None

    Headers: Annotated[
        dict[str, str] | None,
        Field(description="Optional headers in key:value format."),
    ] = None
    Attachments: Annotated[
        list[Attachment] | None, Field(description="A list of attachments.")
    ] = None
    Tags: Annotated[
        list[str] | None,
        Field(description="Optional Mailpit tags for categorization."),
    ] = None


class MailpitEmailClient(BaseEmailClient):
    URL: Final[str] = (
        f"http://mailpit:{settings.FORWARD_MAILPIT_DASHBOARD_PORT}/api/v1/send"
    )

    def send_email(
        self,
        to_emails: list[str],
        html_message: str,
    ) -> None:
        email_schema = EmailSchema(
            To=[Recipient(Email=email) for email in to_emails],
            From=Recipient(Email=settings.SENDER_EMAIL),
            HTML=html_message,
        )

        try:
            response = requests.post(
                self.URL,
                json=email_schema.model_dump(exclude_unset=True),
                timeout=2,
            )
        except requests.exceptions.Timeout:
            raise ExternalProviderException("Request timed out.")

        if response.status_code == 200:
            return

        raise ExternalProviderException(response.json()["Error"])
