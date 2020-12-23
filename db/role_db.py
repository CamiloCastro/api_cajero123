from sqlalchemy import Column, Integer, String
from db.db_connection import Base, engine

class RoleInDB(Base):
    __tablename__ = "roles"
    role_name = Column(String, primary_key = True, unique=True)

Base.metadata.create_all(bind=engine)
