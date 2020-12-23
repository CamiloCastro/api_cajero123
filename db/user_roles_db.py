from sqlalchemy import Column, Integer, String, ForeignKey
from db.db_connection import Base, engine

class UserRoleInDB(Base):
    __tablename__ = "user_roles"
    username = Column(String, ForeignKey("users.username"), primary_key=True)
    role_name = Column(String, ForeignKey("roles.role_name"), primary_key = True)

Base.metadata.create_all(bind=engine)