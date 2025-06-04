import openai
from data_analysis import analyze_data

class AIAgent:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)

    def query_insights(self, industry: str, summary: str, patterns: str, suggestions: str) -> str:
        try:
            prompt = f"""You are an expert business analyst and educator. A user from the {industry} industry uploaded a small dataset and received the following automated analysis:

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


# ✅ Use this in main.py
def process_with_ai_agent(api_key, records, industry, base_result=None):
    import pandas as pd

    # Step 1: Convert to DataFrame
    df = pd.DataFrame(records)

    # Step 2: If base_result (from non-AI version) exists, reuse it
    if base_result:
        summary_section = base_result.get("summary", f"The uploaded dataset contains {len(records)} records related to the {industry} industry.")
        patterns = base_result.get("patterns", "No significant patterns found.")
        suggestions = base_result.get("strategy", "No specific strategy found.")
        plots = base_result.get("plots", [])
        table_data = base_result.get("table_data", records[:10])
    else:
        # Otherwise, run local analysis
        full_analysis_text = analyze_data(df, industry)
        summary_section = f"The uploaded dataset contains {len(records)} records related to the {industry} industry."

        if "Linear Regression Analysis:" in full_analysis_text:
            pattern_start = full_analysis_text.index("Linear Regression Analysis:")
            pattern_end = full_analysis_text.index("Strategic Suggestions:") if "Strategic Suggestions:" in full_analysis_text else len(full_analysis_text)
            patterns = full_analysis_text[pattern_start:pattern_end].strip()
        else:
            patterns = "No significant regression patterns found."

        suggestions_start = full_analysis_text.find("Strategic Suggestions:")
        suggestions = full_analysis_text[suggestions_start:].strip() if suggestions_start != -1 else "No specific suggestions identified."

        plots = []
        table_data = records[:10]

    # Step 3: Query GPT Agent
    ai = AIAgent(api_key)
    insights = ai.query_insights(industry, summary_section, patterns, suggestions)

    # Step 4: Return enhanced result
    return {
        "summary": summary_section,
        "strategy": suggestions,
        "patterns": patterns,
        "insights": insights,
        "plots": plots,
        "table_data": table_data
    }
