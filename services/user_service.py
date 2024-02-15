from models import user_model, chat_model
from schemas import user_schema
from database.engine import SessionDep


def get_users_list(db: SessionDep, is_active: bool = True):
    return db.query(user_model.User).filter_by(is_active=is_active).all()


def get_users_by_id(db: SessionDep, user_id: int, is_active: bool = True):
    return db.query(user_model.User).filter_by(id=user_id, is_active=is_active).first()


def get_users_by_email(db: SessionDep, user_email: str, is_active: bool = True):
    return (
        db.query(user_model.User)
        .filter_by(email=user_email, is_active=is_active)
        .first()
    )


def create_new_users(db: SessionDep, payload: user_schema.UserCreate):
    new_user = user_model.User(**payload.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def update_users(db: SessionDep, user_id: int, payload: user_schema.UserUpdate):
    db.query(user_model.User).filter_by(id=user_id, is_active=True).update(
        payload.model_dump(exclude_unset=True)
    )
    db.commit()


def delete_users(db: SessionDep, user_id: int):
    db.query(user_model.User).filter_by(id=user_id, is_active=True).update(
        {"is_active": False}
    )

    db.commit()


def save_users_chat(db: SessionDep, user_id: int, message: str, response: str):
    new_chat = chat_model.Chat(user_id=user_id, message=message, response=response)

    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    return new_chat
