from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        if email is None:
            return None
        email_clean = str(email).strip().lower()
        return self.model.query.filter_by(email=email_clean).first()