from .db import db
from .models.user import User


def validate_model(cls, id):
    try:
        id = int(id)
    except ValueError:
        raise ValueError(f"{cls.__name__} id ({id}) is invalid.")

    query = db.select(cls).where(cls.id == id)
    model = db.session.scalar(query)

    if not model:
        raise LookupError(f"{cls.__name__} with id ({id}) not found.")

    return model


def get_user_by_email(email):
    try:
        user = db.session.scalar(
            db.select(User).where(User.email == email)
        )
    except Exception:
        raise RuntimeError("Something went wrong")

    if not user:
        raise LookupError("Could not find account.")

    return user


def validate_by_email(cls, email):
    user = db.select(cls).where(cls.email == email)

    if user:
        return user

    raise LookupError("Could not find account.")


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
        db.session.add(new_model)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return new_model


def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(
                    getattr(cls, attribute).ilike(f"%{value}%"))

    models = db.session.scalars(query.order_by(cls.id))
    models_response = [model.to_dict() for model in models]
    return models_response


def update_model(obj, data):
    for attr, value in data.items():
        if hasattr(obj, attr):
            setattr(obj, attr, value)

    db.session.commit()
