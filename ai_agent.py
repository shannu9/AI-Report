import openai
import os

class AIAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = self.api_key

    def query_insights(self, industry: str, summary: str, patterns: str, suggestions: str) -> str:
        try:
            prompt = f""" You are an expert business analyst and educator. A user from the {industry} industry uploaded a small dataset and received the following automated analysis:

                        -------------------------------
                        🔍 Summary of the data:
                        {summary}

                        📊 Identified patterns:
                        {patterns}

                        💡 Initial strategy suggestions:
                        {suggestions}
                        -------------------------------

                        Now, your job is to explain this to someone who is NOT good with numbers or technical terms.

                        Write a friendly, insightful, and motivating explanation in plain English that:

                        1. Helps the user understand what’s really happening in their business.
                        2. Explains why the patterns matter using real-world examples.
                        3. Suggests at least 3 actionable strategies.
                        4. Uses analogies or examples from their industry to make it relatable.
                        5. Avoids technical jargon or statistical terms — make it easy for a business owner or manager to understand.

                        Wrap up by giving advice on what to focus on next.

                        Output should sound like a consultant talking to a client — friendly, smart, and strategic.
                        """

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a strategic business consultant and educator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.75,
                max_tokens=1400
            )

            return response.choices[0].message.content.strip()

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
