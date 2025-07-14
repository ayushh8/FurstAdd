# FurstAid: Your Personal Pet Symptom Analyzer

FurstAid is a fullstack AI-powered web app that helps pet owners get instant, AI-generated advice and diagnosis for their pets' symptoms. It supports both text and image input, and features a chat-style interface for follow-up questions.

---

## 🚀 Features
- **Pet Symptom Form:** Enter pet name, breed, weight, symptoms, and optionally upload an image.
- **AI Diagnosis:** Uses Microsoft Phi-4 Multimodal Instruct (via OpenRouter) for text+image analysis.
- **Chat Interface:** Ask follow-up questions in a chat-style UI after the initial diagnosis.
- **Day/Night Theme:** Toggle between light and dark mode.
- **Modern UI:** Built with Next.js (React) and Tailwind CSS.

---

## 🛠️ Tech Stack
- **Frontend:** Next.js (TypeScript, App Router), Tailwind CSS
- **Backend:** FastAPI (Python)
- **AI Integration:** OpenRouter API (Microsoft Phi-4 Multimodal Instruct)

---

## 📦 File Structure
```
FurstAid/
├── backend/
│   ├── main.py           # FastAPI app, routes, CORS, error handling
│   ├── ai_logic.py       # OpenRouter API integration
│   ├── models.py         # Pydantic models
│   ├── requirements.txt  # Python dependencies
│   └── ...
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   └── page.tsx          # Main chat UI
│   │   ├── components/
│   │   │   └── PetForm.tsx       # Pet info form
│   │   └── ...
│   ├── package.json
│   └── ...
├── .gitignore
└── README.md
```

---

## ⚡ Setup Instructions

### 1. Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install python-multipart
# Add your OpenRouter API key to a .env file:
echo "OPENROUTER_API_KEY=sk-..." > .env
uvicorn main:app --reload
```
- Visit http://127.0.0.1:8000/docs to test the API.

### 2. Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```
- Visit http://localhost:3000 to use the app.

---

## 🧩 How It Works
- The frontend collects pet info and (optionally) an image, then sends it to the backend.
- The backend calls the OpenRouter API with the Microsoft Phi-4 Multimodal Instruct model.
- The AI's diagnosis/advice is returned and shown in a chat interface, where you can ask follow-up questions.

---

## 🐾 Challenges Faced & Solutions

### 1. **CORS Issues**
- **Problem:** The frontend (localhost:3000) could not access the backend (127.0.0.1:8000) due to CORS policy errors.
- **Solution:** Added FastAPI CORS middleware to allow both `http://localhost:3000` and `http://127.0.0.1:3000` as allowed origins. Always restart the backend after changing CORS settings.

### 2. **Model Not Accepting Images**
- **Problem:** Some models (like Mixtral) on OpenRouter are text-only, even if the playground UI seems to accept images.
- **Solution:** Switched to a true multimodal model (`microsoft/phi-4-multimodal-instruct`) that supports both text and image input via the API.

### 3. **UnicodeDecodeError with Image Uploads**
- **Problem:** FastAPI tried to serialize image bytes in error responses, causing UnicodeDecodeError.
- **Solution:** Added a custom error handler for validation errors to avoid serializing image bytes.

### 4. **Type Mismatch for Weight Field**
- **Problem:** The weight field was sent as a string, causing backend validation errors.
- **Solution:** Ensured the frontend always sends weight as a float string.

---

## 🙏 Credits
- [OpenRouter](https://openrouter.ai/) for free API access to advanced AI models.
- [Microsoft Phi-4 Multimodal Instruct](https://openrouter.ai/models/microsoft/phi-4-multimodal-instruct)
- [FastAPI](https://fastapi.tiangolo.com/), [Next.js](https://nextjs.org/), [Tailwind CSS](https://tailwindcss.com/)

---

