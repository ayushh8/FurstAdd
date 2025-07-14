import os
import httpx
import base64
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "microsoft/phi-4-multimodal-instruct"

async def get_diagnosis(pet_name: str, breed: str, weight: float, symptoms: Optional[str] = None, image_bytes: Optional[bytes] = None) -> str:
    prompt = f"""
    Pet Name: {pet_name}\nBreed: {breed}\nWeight: {weight}kg\nSymptoms: {symptoms or 'None provided'}\n
    Please provide a veterinary diagnosis and advice for this pet based on the information above. If symptoms are missing, give general advice for the breed and weight.
    """
    messages = [
        {"role": "user", "content": prompt}
    ]
    files = None
    if image_bytes:
        # Encode image as base64 and send as OpenRouter expects
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]
        })
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": messages if image_bytes else [{"role": "user", "content": prompt}]
    }
    print("Sending to OpenRouter:", data)
    async with httpx.AsyncClient() as client:
        response = await client.post(OPENROUTER_API_URL, headers=headers, json=data)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            print("OpenRouter API error:", exc.response.text)
            raise
        result = response.json()
        return result["choices"][0]["message"]["content"] 