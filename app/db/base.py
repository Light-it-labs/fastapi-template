# Import all the models, so that Base has them before being
# imported by Alembic
from app.common.models.base_class import Base  # noqa
from app.users.models.user import User  # noqa
