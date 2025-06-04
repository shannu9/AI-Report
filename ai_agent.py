import openai
import os

class AIAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = self.api_key

    def query_insights(self, industry: str, summary: str, patterns: str, suggestions: str) -> str:
        try:
            prompt = f"""
            You are a business intelligence AI assistant. A user from the {industry} industry uploaded data.
            Based on the following:

            Summary:
            {summary}

            Patterns:
            {patterns}

            Suggestions:
            {suggestions}

            Generate a highly insightful, realistic, and strategic summary including potential business actions, comparisons to industry benchmarks, and suggestions for optimization. Include advanced trends, real-world case examples, and visual storytelling ideas.
            """

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a highly analytical business analyst and strategist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1200
            )

            return response['choices'][0]['message']['content'].strip()

        except Exception as e:
            return f"[AI Agent Error] {str(e)}"


# ✅ Add this function so main.py can import it
def process_with_ai_agent(api_key, records, industry):
    summary = f"The uploaded dataset contains {len(records)} records related to the {industry} industry."
    patterns = "Patterns identified using basic statistical insights and correlations."
    suggestions = "Standard strategic suggestions based on the given data."

    ai = AIAgent(api_key)
    insights = ai.query_insights(industry, summary, patterns, suggestions)

    return {
        "summary": summary,
        "strategy": suggestions,
        "insights": insights,
        "plots": [],
        "table_data": records[:10]
    }
