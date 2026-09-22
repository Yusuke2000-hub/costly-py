from pydantic import BaseModel, ConfigDict
from datetime import date, datetime


class ExpenseCreate(BaseModel):
    category: str
    amount: int
    date: date


class ExpenseUpdate(BaseModel):
    category: str | None = None
    amount: int | None = None
    date: date | None = None


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: str
    amount: int
    date: date
    created_at: datetime
