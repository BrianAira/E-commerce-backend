from typing import List, Optional
from sqlmodel import Session, select

from app.domain.models.user import User, UserCreate, AdminUpdate
from app.application.ports.user_port import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user


    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def update(self, user_id: int, user_data: AdminUpdate) -> Optional[User]:
        db_user = self.session.get(User, user_id)
        if not db_user:
            return None

        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(db_user, key, value)

        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def delete(self, user_id: int) -> bool:
        db_user = self.session.get(User, user_id)
        if not db_user:
            return False
        self.session.delete(db_user)
        self.session.commit()
        return True

    def list_all(self) -> List[User]:
        return list(self.session.exec(select(User)))
