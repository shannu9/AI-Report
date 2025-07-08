# AI Report Tool Backend

# 🧠 AI Business Insights Generator

AI-powered tool that analyzes uploaded business datasets and generates detailed, strategy-rich PDF reports tailored to your industry — combining machine learning, statistical analysis, and GPT-4 intelligence.

## 🚀 Overview

**AI Business Insights Generator** helps business owners, analysts, and strategists make informed decisions without needing deep data expertise. Upload your CSV (≤100 records), select your industry, and receive a customized report containing insights, charts, strategy suggestions, and executive summaries.

✨ Optionally, unlock **AI-enhanced insights** using your OpenAI GPT-4 API key.

---

## 🧩 Tech Stack

- **Frontend:** React + Firebase Hosting
- **Backend:** FastAPI (deployed on Render)
- **Data Processing:** Python, Pandas, Scikit-learn
- **AI Engine:** OpenAI GPT-4 API (optional)
- **Report Generator:** FPDF (PDF creation)
- **Database:** Firebase Firestore

---

## 📊 How It Works

1. **Select your industry**
2. **Upload your CSV file** (max 100 records)
3. **(Optional)** Paste your OpenAI GPT-4 API key to enable AI-powered strategy
4. **Wait as the backend:**
   - Performs EDA & ML analysis
   - If key is present: invokes GPT-4 to generate deep insights, storytelling, executive summaries, and ROI-driven strategy
5. **Download your customized PDF report**, packed with:
   - Key metrics & graphs
   - Clustering or trend insights
   - Recommended business actions
   - Executive-friendly summary

---

## 🧠 What the AI Agent Does

When an OpenAI key is provided, the backend AI Agent:

- Understands uploaded business data contextually
- Performs comparative market reasoning
- Suggests actionable business strategies
- Highlights opportunities and risks using storytelling
- Adds executive summaries for non-technical readers

---

## 🔐 OpenAI API Key (Optional)

To unlock the AI strategy layer:

1. Go to [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. Create and copy your GPT-4 API key
3. Paste it into the input form on the app interface
4. We never store or transmit your key beyond your session

Don’t have a key? No problem — the tool still uses ML/statistical logic to generate valuable insights.

---

## 📁 Example Use Cases

- Sales trend prediction for small businesses
- ROI-focused strategy recommendations for retailers
- Clustering-based segmentation insights for consultants
- Executive summaries for stakeholder presentations

---

## 🛠️ Local Development (Optional)

> You only need this if you're contributing or running locally.

### Frontend (React + Firebase)

```bash
cd frontend
npm install
npm start

