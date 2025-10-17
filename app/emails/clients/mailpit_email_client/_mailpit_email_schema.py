from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class _Recipient(BaseModel):
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


class _Attachment(BaseModel):
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


class _EmailSchema(BaseModel):
    """
    Defines the JSON schema for sending an email via Mailpit.
    """

    From: Annotated[_Recipient, Field(description="The sender of the email.")]
    To: Annotated[
        list[_Recipient],
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
        list[_Recipient] | None, Field(description='"Cc" recipients.')
    ] = None
    Bcc: Annotated[
        list[EmailStr] | None,
        Field(description='"Bcc" recipients (email only).'),
    ] = None
    ReplyTo: Annotated[
        list[_Recipient] | None,
        Field(description="Optional 'Reply-To' recipients."),
    ] = None

    Headers: Annotated[
        dict[str, str] | None,
        Field(description="Optional headers in key:value format."),
    ] = None
    Attachments: Annotated[
        list[_Attachment] | None, Field(description="A list of attachments.")
    ] = None
    Tags: Annotated[
        list[str] | None,
        Field(description="Optional Mailpit tags for categorization."),
    ] = None
