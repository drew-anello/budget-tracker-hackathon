from csv_api.schema import FinanceData
import anthropic
import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Test data
TEST_DATA = {
    "income": 5200,
    "expenses": [
        {"category": "Housing", "subcategory": "Rent", "amount": 1650, "frequency": "monthly", "essential": True},
        {"category": "Housing", "subcategory": "Utilities", "amount": 180, "frequency": "monthly", "essential": True},
        {"category": "Housing", "subcategory": "Internet", "amount": 75, "frequency": "monthly", "essential": True},
        {"category": "Food", "subcategory": "Groceries", "amount": 500, "frequency": "monthly", "essential": True},
        {"category": "Food", "subcategory": "Dining Out", "amount": 320, "frequency": "monthly", "essential": False},
        {"category": "Transportation", "subcategory": "Car Payment", "amount": 325, "frequency": "monthly", "essential": True},
        {"category": "Transportation", "subcategory": "Gas", "amount": 160, "frequency": "monthly", "essential": True},
        {"category": "Transportation", "subcategory": "Insurance", "amount": 140, "frequency": "monthly", "essential": True},
        {"category": "Health", "subcategory": "Insurance", "amount": 220, "frequency": "monthly", "essential": True},
        {"category": "Health", "subcategory": "Gym", "amount": 50, "frequency": "monthly", "essential": False},
        {"category": "Health", "subcategory": "Medications", "amount": 45, "frequency": "monthly", "essential": True},
        {"category": "Entertainment", "subcategory": "Streaming Services", "amount": 35, "frequency": "monthly", "essential": False},
        {"category": "Entertainment", "subcategory": "Hobbies", "amount": 100, "frequency": "monthly", "essential": False},
        {"category": "Personal", "subcategory": "Clothing", "amount": 120, "frequency": "monthly", "essential": True},
        {"category": "Personal", "subcategory": "Haircuts", "amount": 60, "frequency": "monthly", "essential": True},
        {"category": "Debt", "subcategory": "Student Loans", "amount": 350, "frequency": "monthly", "essential": True},
        {"category": "Debt", "subcategory": "Credit Card", "amount": 200, "frequency": "monthly", "essential": True},
        {"category": "Subscriptions", "subcategory": "Software", "amount": 25, "frequency": "monthly", "essential": False},
        {"category": "Miscellaneous", "subcategory": "Gifts", "amount": 50, "frequency": "monthly", "essential": False},
        {"category": "Education", "subcategory": "Online Courses", "amount": 35, "frequency": "monthly", "essential": False}
    ]
}

def send_to_claude(data: FinanceData):
    client = anthropic.Anthropic(api_key=os.getenv("API_KEY"))

    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=20000,
        temperature=1,
        system="""Analyze this budget and provide recommendations in a structured JSON format. 
        The response should include:
        - overview: key financial metrics
        - essential_expenses: breakdown of essential expenses
        - non_essential_expenses: breakdown of non-essential expenses
        - recommendations: array of optimization suggestions
        - summary: brief conclusion
        Format all monetary values with dollar signs and percentages with % symbols.
        IMPORTANT: Return ONLY the JSON object, without any markdown formatting or additional text.""",
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": json.dumps(data.model_dump())}]
            }
        ]
    )
    
    # Extract the text content from the response
    response_text = message.content[0].text
    
    # Remove any markdown formatting if present
    if response_text.startswith("```json"):
        response_text = response_text[7:]  # Remove ```json
    if response_text.endswith("```"):
        response_text = response_text[:-3]  # Remove ```
    
    # Parse the JSON to ensure it's valid
    try:
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON response from Claude: {str(e)}")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Finance API"}

@app.get("/test-data")
async def get_test_data():
    return TEST_DATA

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
   
    return {"message": "File uploaded successfully"}

@app.post("/analyze")
async def analyze_finance(data: FinanceData):
    try:
        analysis = send_to_claude(data)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test-analyze")
async def test_analyze():
    try:
        # Convert test data to FinanceData model
        test_finance_data = FinanceData(**TEST_DATA)
        analysis = send_to_claude(test_finance_data)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
