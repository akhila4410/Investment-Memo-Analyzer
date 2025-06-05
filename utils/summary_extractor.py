def extract_summary_fields(text, llm):
    prompt = f"""
You are an investment analyst. Extract the following fields from the investment memo
Not only the below fields if any additional information available which is important regarding the investment also extract those as fields.:


- Fund Name
- Target Raise
- Target IRR
- Founders
- Sector
- Exit Strategy
- Key Risks
- Use of Funds
- Geography
- Contact Information
- Prepared By
- Date

Return ONLY a valid JSON object. Do not include explanations or formatting or headings.
Make sure the output has both start and end paranthesis
Memo Content:
{text[:3000]}
"""
    return llm.invoke(prompt)