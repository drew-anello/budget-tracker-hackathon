from fastapi import APIRouter, UploadFile, File, Form
from .utils import parse_csv
from .schema import FinanceData

router = APIRouter()

@router.post("/convert")
async def convert_csv_to_json(file: UploadFile = File(...), income: float = Form(...)):
    csv_data = (await file.read()).decode("utf-8")
    expenses = parse_csv(csv_data)
    return FinanceData(income=income, expenses=expenses)
