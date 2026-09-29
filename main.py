from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date as DateType
from routers import expenses, incomes
from database import get_db
import crud.expenses as expense_crud
import crud.incomes as income_crud
from schemas import ExpenseCreate, IncomeCreate, IncomeUpdate

app = FastAPI(title="COSTLY", description="家計原価率管理アプリ")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    today = DateType.today()
    current_month = today.strftime("%Y-%m")

    all_expenses = expense_crud.get_all(db)
    monthly_expenses = [e for e in all_expenses if e.date.strftime("%Y-%m") == current_month]

    total_expense = sum(e.amount for e in monthly_expenses)

    category_totals: dict[str, int] = {}
    for e in monthly_expenses:
        category_totals[e.category] = category_totals.get(e.category, 0) + e.amount

    income = income_crud.get_by_month(db, current_month)

    defense_rate = None
    if income and income.amount > 0:
        defense_rate = round(total_expense / income.amount * 100, 1)

    return templates.TemplateResponse(request, "dashboard.html", context={
        "current_month": current_month,
        "total_expense": total_expense,
        "income": income,
        "defense_rate": defense_rate,
        "category_totals": category_totals,
    })


@app.get("/expenses/new", response_class=HTMLResponse)
def expense_form(request: Request):
    return templates.TemplateResponse(request, "expense_new.html", context={
        "today": DateType.today().isoformat(),
    })


@app.post("/expenses/new")
def create_expense_form(
    category: str = Form(...),
    amount: int = Form(...),
    date: str = Form(...),
    db: Session = Depends(get_db),
):
    data = ExpenseCreate(category=category, amount=amount, date=DateType.fromisoformat(date))
    expense_crud.create(db, data)
    return RedirectResponse(url="/", status_code=303)


@app.get("/incomes/new", response_class=HTMLResponse)
def income_form(request: Request):
    return templates.TemplateResponse(request, "income_new.html", context={
        "current_month": DateType.today().strftime("%Y-%m"),
    })


@app.post("/incomes/new")
def create_income_form(
    amount: int = Form(...),
    month: str = Form(...),
    db: Session = Depends(get_db),
):
    existing = income_crud.get_by_month(db, month)
    if existing:
        income_crud.update(db, existing, IncomeUpdate(amount=amount))
    else:
        income_crud.create(db, IncomeCreate(amount=amount, month=month))
    return RedirectResponse(url="/", status_code=303)


# HTMLルートの後にJSONルーターを追加（/expenses/{id}との順序衝突を防ぐため）
app.include_router(expenses.router)
app.include_router(incomes.router)
