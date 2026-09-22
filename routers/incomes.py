from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import IncomeCreate, IncomeUpdate, IncomeResponse
import crud.incomes as income_crud

router = APIRouter(prefix="/incomes", tags=["incomes"])


@router.get("/", response_model=list[IncomeResponse])
def list_incomes(db: Session = Depends(get_db)):
    return income_crud.get_all(db)


@router.get("/{income_id}", response_model=IncomeResponse)
def get_income(income_id: int, db: Session = Depends(get_db)):
    income = income_crud.get_by_id(db, income_id)
    if income is None:
        raise HTTPException(status_code=404, detail="Income not found")
    return income


@router.post("/", response_model=IncomeResponse, status_code=201)
def create_income(data: IncomeCreate, db: Session = Depends(get_db)):
    if income_crud.get_by_month(db, data.month) is not None:
        raise HTTPException(status_code=409, detail=f"Income for month '{data.month}' already exists")
    return income_crud.create(db, data)


@router.put("/{income_id}", response_model=IncomeResponse)
def update_income(income_id: int, data: IncomeUpdate, db: Session = Depends(get_db)):
    income = income_crud.get_by_id(db, income_id)
    if income is None:
        raise HTTPException(status_code=404, detail="Income not found")
    return income_crud.update(db, income, data)


@router.delete("/{income_id}", status_code=204)
def delete_income(income_id: int, db: Session = Depends(get_db)):
    income = income_crud.get_by_id(db, income_id)
    if income is None:
        raise HTTPException(status_code=404, detail="Income not found")
    income_crud.delete(db, income)
