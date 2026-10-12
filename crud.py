from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserUpdate

def create_user(db: Session, user_data: UserCreate):
    user = User(**user_data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session, city=None, is_active=None):
    query = db.query(User)
    if city:
        query = query.filter(User.city.ilike(f"%{city.strip()}%"))
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.order_by(User.id).all()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == str(email).lower()).first()

def update_user(db: Session, user: User, user_data: UserUpdate):
    changes = user_data.model_dump(exclude_unset=True)
    if "email" in changes and changes["email"] is not None:
        changes["email"] = str(changes["email"]).lower()
    for key, value in changes.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()
