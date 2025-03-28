from app.users.models import Patient
from app.users.repositories.users_repository import UsersRepository
from app.users.schemas.patient_schema import PatientCreate, PatientUpdate


class PatientsRepository(
    UsersRepository[Patient, PatientCreate, PatientUpdate]
):
    pass


patients_repository = PatientsRepository(Patient)
