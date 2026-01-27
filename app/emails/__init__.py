from .exceptions import EmailClientException, GlobalEmailClientNotSetException
from .schema.email import Email

from .clients.base import BaseEmailClient

from ._global_state import set_client, get_client

from .clients import MailpitEmailClient, ExampleEmailClient, CeleryTaskEmailClient
from .services.emails_service import EmailService
