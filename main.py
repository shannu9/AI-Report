from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uuid
from pathlib import Path
from pdf_report import PDFReport
from data_analysis import analyze_data
from ai_agent import AIAgent  # ✅ import the class

app = FastAPI()

# ✅ CORS settings for Firebase
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://shanmukh-resume.web.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
REPORT_DIR = Path("reports")
UPLOAD_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

@app.post("/generate-report/")
async def generate_report(
    file: UploadFile = File(...),
    industry: str = Form(...),
    use_ai: bool = Form(...),
    gpt_api_key: str = Form(default=None)
):
    try:
        # Save uploaded file
        file_id = str(uuid.uuid4())
        file_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        df = pd.read_csv(file_path)

        if use_ai:
            if not gpt_api_key:
                raise HTTPException(status_code=400, detail="Missing GPT API key for AI analysis")
            agent = AIAgent(gpt_api_key)
            summary = "Auto-generated summary from data."
            patterns = "Patterns from data distribution."
            suggestions = "Initial business suggestions."
            insights = agent.query_insights(industry, summary, patterns, suggestions)
            strategy = "Suggested strategies from AI"
            plots = []         # ✅ define empty list   
            table_data = []    # ✅ define empty list
        else:
            result = analyze_data(df, industry)
            summary = result.get("summary", "")
            strategy = result.get("strategy", "")
            insights = result.get("insights", "")
            plots = result.get("plots", [])
            table_data = result.get("table_data", [])
        # use empty plots/table_data if AI (not generated from AI for now)
        pdf_tool = PDFReport(output_path=REPORT_DIR)
        pdf_path = pdf_tool.create_pdf(summary, strategy, insights, plots if not use_ai else [], table_data if not use_ai else [])

        return FileResponse(path=pdf_path, filename="AI_Insights_Report.pdf", media_type='application/pdf')

    except Exception as e:
        print("Error in generate_report:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
