from csv_api.schema import FinanceData
import anthropic
import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

load_dotenv()

def send_to_claude(data: FinanceData):
    client = anthropic.Anthropic(api_key=os.getenv("API_KEY"))

    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=20000,
        temperature=1,
        system="Evaluate this budget that is in json format and tell me what ways I can optimize and improve my financial stance",
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": json.dumps(data.model_dump())}]
            }
        ]
    )
    return message.content

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Finance API"}

@app.post("/analyze")
async def analyze_finance(data: FinanceData):
    try:
        analysis = send_to_claude(data)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
