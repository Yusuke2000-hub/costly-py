from sqlalchemy.orm import Session
from models import Income
from schemas import IncomeCreate, IncomeUpdate


def get_all(db: Session) -> list[Income]:
    return db.query(Income).all()


def get_by_id(db: Session, income_id: int) -> Income | None:
    return db.query(Income).filter(Income.id == income_id).first()


def get_by_month(db: Session, month: str) -> Income | None:
    return db.query(Income).filter(Income.month == month).first()


def create(db: Session, data: IncomeCreate) -> Income:
    income = Income(**data.model_dump())
    db.add(income)
    db.commit()
    db.refresh(income)
    return income


def update(db: Session, income: Income, data: IncomeUpdate) -> Income:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(income, field, value)
    db.commit()
    db.refresh(income)
    return income


def delete(db: Session, income: Income) -> None:
    db.delete(income)
    db.commit()
