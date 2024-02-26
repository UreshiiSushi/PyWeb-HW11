from sqlalchemy import Column, Integer, String, Boolean, Date, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy_utils import EmailType

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    lastname = Column(String(50))
    email = Column(EmailType)
    phone = Column(String(50))
    born_date = Column("Born_date", DateTime, comment="Contact's birthday")
    description = Column(String(250))
