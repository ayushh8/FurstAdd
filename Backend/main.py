from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from models import AnalyzeResponse
from ai_logic import get_diagnosis
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": "Validation error. Please check your input."}
    )

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_pet(
    pet_name: str = Form(...),
    breed: str = Form(...),
    weight: float = Form(...),
    symptoms: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None)
):
    try:
        image_bytes = await image.read() if image else None
        ai_response = await get_diagnosis(
            pet_name=pet_name,
            breed=breed,
            weight=weight,
            symptoms=symptoms,
            image_bytes=image_bytes
        )
        if "Advice:" in ai_response:
            parts = ai_response.split("Advice:", 1)
            diagnosis = parts[0].strip()
            advice = parts[1].strip()
        else:
            diagnosis = ai_response.strip()
            advice = "See above."
        return AnalyzeResponse(diagnosis=diagnosis, advice=advice)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 