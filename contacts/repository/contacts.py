from typing import List
from sqlalchemy.orm import Session
from contacts.database.models import Contact
from datetime import date, datetime, timedelta
from contacts.schemas import ContactEmail, ContactModel, ResponseContactModel


async def create_contact(contact: ContactModel, db: Session) -> ContactModel:
    new_contact = Contact(**contact.model_dump(exclude_unset=True))
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact


async def get_contacts(db: Session) -> List[ResponseContactModel]:

    return db.query(Contact).all()


async def get_contact(contact_id: int, db: Session) -> ContactModel:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def update_contact(
    contact_id: int, db: Session, name, lastname, email, phone, born_date, description
) -> ContactModel:
    target_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if name:
        target_contact.name = name
    if lastname:
        target_contact.lastname = lastname
    if email:
        target_contact.email = email
    if phone:
        target_contact.phone = phone
    if born_date:
        target_contact.born_date = born_date
    if description:
        target_contact.description = description

    db.commit()
    return target_contact


async def delete_contact(contact_id, db) -> Contact | None:
    item = db.query(Contact).filter(Contact.id == contact_id).first()
    if item:
        db.delete(item)
        db.commit()
    return


async def search_data(
    db: Session, name: str, lastname: str, email: str
) -> ContactModel | None:

    if name:
        return db.query(Contact).filter(Contact.name == name).first()
    if lastname:
        return db.query(Contact).filter(Contact.lastname == lastname).first()
    if email:
        return db.query(Contact).filter(Contact.email == email).first()


async def birthday_to_week(db: Session) -> List[ContactModel] | None:
    users = db.query(Contact).all()
    week = date.today() + timedelta(days=6)
    happy_users = []
    for user in users:
        bday = datetime(
            date.today().year,
            user.born_date.month,
            user.born_date.day,
        ).date()

        if date.today() <= bday <= week:
            happy_users.append(user)

    return happy_users
