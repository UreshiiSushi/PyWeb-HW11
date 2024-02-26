from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.orm import Session

from contacts.database.db import get_db
from contacts.schemas import ContactModel, ResponseContactModel, ContactEmail
from contacts.repository import contacts as repository_contacts

router = APIRouter()


# Create a new contact
@router.post(
    "/", response_model=ResponseContactModel, status_code=status.HTTP_201_CREATED
)
async def create_new_contact(contact: ContactModel, db: Session = Depends(get_db)):

    return await repository_contacts.create_contact(contact, db)


@router.get("/", response_model=list[ResponseContactModel])
async def get_all_contacts(db: Session = Depends(get_db)):

    return await repository_contacts.get_contacts(db)


# Get one contact with the specific ID
@router.get("/{contact_id}", response_model=ResponseContactModel)
async def read_contact(
    contact_id: int = Path(description="The ID of the contsct to get", gt=0),
    db: Session = Depends(get_db),
):
    contact = await repository_contacts.get_contact(contact_id, db)

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


# Update exist contact
@router.patch("/{contact_id}", response_model=ResponseContactModel)
async def update_contact(
    contact_id: int = Path(description="The ID of the contsct to get", gt=0),
    db: Session = Depends(get_db),
    name: str = None,
    lastname: str = None,
    email: str = None,
    phone: str = None,
    born_date: str = None,
    description: str = None,
):
    target_contact = await repository_contacts.update_contact(
        contact_id, db, name, lastname, email, phone, born_date, description
    )
    if target_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return target_contact


# Delete contact
@router.delete("/{contact_id}", response_model=ResponseContactModel)
async def delete_contact(
    contact_id: int = Path(description="The ID of the contsct to get", gt=0),
    db: Session = Depends(get_db),
):
    contact = await repository_contacts.delete_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    return {"message": "Contact Deleted Succesfully"}


# Search for an email, name or lastname
@router.get("/search/", response_model=ResponseContactModel)
async def search_contact(
    db: Session = Depends(get_db),
    name: str = Query(None),
    lastname: str = Query(None),
    email: str = Query(None),
):
    search_result = await repository_contacts.search_data(db, name, lastname, email)
    if search_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )

    return search_result


# Get birthdays for next 7 days
@router.get("/birthdays/")
async def get_birthday_week(db: Session = Depends(get_db)):
    happy_users = await repository_contacts.birthday_to_week(db)
    if happy_users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contacts not found"
        )

    return happy_users
