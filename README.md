# People Analytics AI

This is an end-to-end People Analytics pipeline that predicts employee flight risk using demographic data and LLM-powered sentiment analysis on employee survey feedback.

## Setup Instructions
1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment: 
   - Mac/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
3. Install requirements: `pip install -r requirements.txt`
4. Add your Gemini API key in the `.env` file.

## Running the App
1. **Start the backend:** `uvicorn backend.main:app --reload`
2. **Start the frontend (in a new terminal):** `streamlit run frontend/app.py`
