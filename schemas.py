from pydantic import BaseModel, ConfigDict
from datetime import date as DateType, datetime


class ExpenseCreate(BaseModel):
    category: str
    amount: int
    date: DateType


class ExpenseUpdate(BaseModel):
    category: str | None = None
    amount: int | None = None
    date: DateType | None = None


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: str
    amount: int
    date: DateType
    created_at: datetime
