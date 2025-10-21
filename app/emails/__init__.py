from .exceptions import EmailClientException, GlobalEmailClientNotSetException
from .schema.email import Email

from .interfaces.base_email_client import BaseEmailClient

from ._global_state import set_client, get_client

from .clients import MailpitEmailClient, ExampleEmailClient
from .services.emails_service import EmailService
