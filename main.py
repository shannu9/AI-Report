from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uuid
import os
from pathlib import Path
from pdf_report import PDFReport
from data_analysis import analyze_data
from ai_agent import process_with_ai_agent


app = FastAPI()

# ✅ Add this CORS configuration
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
    # Save uploaded file
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Read CSV into DataFrame
    try:
        df = pd.read_csv(file_path)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV file")

    # Perform analysis
    if use_ai:
        if not gpt_api_key:
            raise HTTPException(status_code=400, detail="Missing GPT API key for AI analysis")
        analysis_result = process_with_ai_agent(gpt_api_key, df.to_dict(orient="records"), industry)
    else:
        analysis_result = analyze_data(df, industry)

    # Generate PDF report using PDFReport class
    summary = analysis_result.get("summary", "")
    strategy = analysis_result.get("strategy", "")
    insights = analysis_result.get("insights", "")
    plots = analysis_result.get("plots", [])
    table_data = analysis_result.get("table_data", [])

    pdf_tool = PDFReport(output_path=REPORT_DIR)
    report_path = pdf_tool.create_pdf(summary, strategy, insights, plots, table_data)

    return FileResponse(path=report_path, filename="AI_Insights_Report.pdf", media_type='application/pdf')
