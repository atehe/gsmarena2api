from sqlalchemy.orm import Session

from .models import BaseModel


def paginate_model(session: Session, model: BaseModel, page: int, limit: int, **filter) -> list[BaseModel]:
    offset = (page - 1) * limit
    result = session.query(model).filter_by(**filter).order_by(model.id).offset(offset).limit(limit).all()

    return result
