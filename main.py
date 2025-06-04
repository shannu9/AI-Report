from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uuid
import os
import traceback
from pathlib import Path
from pdf_report import PDFReport
from data_analysis import analyze_data
from ai_agent import process_with_ai_agent

app = FastAPI()

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

        # Read file into DataFrame
        df = pd.read_csv(file_path)

        # Always run non-AI analysis first
        basic_result = analyze_data(df, industry)

        # Then optionally run AI enhancement
        if use_ai:
            if not gpt_api_key:
                raise HTTPException(status_code=400, detail="Missing GPT API key for AI analysis")

            # Pass base result and user data to AI agent
            analysis_result = process_with_ai_agent(
                api_key=gpt_api_key,
                records=df.to_dict(orient="records"),
                industry=industry,
                base_result=basic_result
            )
        else:
            analysis_result = {
                "summary": basic_result.get("summary", ""),
                "strategy": basic_result.get("strategy", ""),
                "insights": basic_result.get("insights", ""),
                "plots": basic_result.get("plots", []),
                "table_data": basic_result.get("table_data", [])
            }

        # Generate PDF
        pdf_tool = PDFReport(output_path=REPORT_DIR)
        report_path = pdf_tool.create_pdf(
            analysis_result["summary"],
            analysis_result["strategy"],
            analysis_result["insights"],
            analysis_result["plots"],
            analysis_result["table_data"]
        )

        return FileResponse(path=report_path, filename="AI_Insights_Report.pdf", media_type='application/pdf')

    except Exception as e:
        print("Error:", str(e))
        print("❌ INTERNAL ERROR:")
        traceback.print_exc() 
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
