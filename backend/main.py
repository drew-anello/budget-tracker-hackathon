from csv_api.schema import FinanceData
import anthropic
import json

def send_to_claude(data: FinanceData):
    client = anthropic.Anthropic(api_key="your_key_here")

    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=20000,
        temperature=1,
        system="Evaluate this budget that is in json format and tell me what way's I can optimize improve my finical stance",
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": json.dumps(data.dict())}]
            }
        ]
    )
    return message.content
