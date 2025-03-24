import streamlit as st
import requests

# API Configuration
API_KEY = ""
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Function to Determine Relevant Departments (Max 4-5)
def get_departments(brand_name):
    headers = {"Content-Type": "application/json"}
    prompt = f"""
    Identify up to 4-5 key customer-facing departments for sentiment analysis of the brand "{brand_name}".
    Select only the most relevant ones. Examples: Product Quality, Customer Service, Pricing, Delivery & Logistics, User Experience.
    """
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        departments = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Product Quality, Customer Service, Pricing, User Experience").split(", ")
        return departments[:5]  # Limit to 4-5 departments
    except requests.exceptions.RequestException as e:
        return ["Product Quality", "Customer Service", "Pricing", "User Experience"]

# Function to Fetch Customer Feedback
def fetch_feedback(brand_name):
    headers = {"Content-Type": "application/json"}
    prompt = f"""
    Generate customer feedback for the brand "{brand_name}" from thousands of analyzed reviews.
    Cover areas such as product quality, customer service, pricing, and user experience.
    """
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        feedback = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No feedback generated.")
        return feedback.split("\n")
    except requests.exceptions.RequestException as e:
        return [f"API Error: {e}"]

# Function to Analyze Sentiment
def analyze_sentiment(brand_name, feedback_list, departments):
    headers = {"Content-Type": "application/json"}
    
    department_analysis = "\n\n".join([
        f"""
        **{dept}**:
        - **Sentiment Score:** (% Positive, Neutral, Negative)
        - **Key Positive Factors:** (List 3-5 major positive aspects customers appreciate)
        - **Key Negative Factors:** (List 3-5 common complaints)
        - **Actionable Recommendations:** (Suggestions to improve based on feedback)
        """ for dept in departments
    ])

    prompt = f"""
    Perform a **detailed sentiment analysis** on customer feedback for "{brand_name}" from thousands of analyzed reviews.

    **Overall Sentiment Score**: Percentage of Positive, Neutral, and Negative feedback.

    **Department-Wise Sentiment Analysis**:
    {department_analysis}

    **Competitor Benchmarking**:
    - Identify 3 competitors of "{brand_name}" and compare sentiment scores.
    - Highlight strengths and weaknesses of "{brand_name}" vs competitors.

    **AI Summary of Findings**:
    - Overall brand performance assessment.
    - Key insights and opportunities for improvement.
    - Strategic recommendations.
    """
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        analysis = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No analysis generated.")
        return analysis
    except requests.exceptions.RequestException as e:
        return f"API Error: {e}"

# Streamlit UI
st.title("📊 Customer Sentiment Analyzer")
st.markdown("Analyze customer sentiment for any brand using AI-powered insights.")

brand_name = st.text_input("🔍 Enter Brand Name")

if st.button("Analyze Sentiment"):
    if brand_name:
        with st.spinner("Analyzing... Please wait."):
            departments = get_departments(brand_name)
            feedback = fetch_feedback(brand_name)
            sentiment_result = analyze_sentiment(brand_name, feedback, departments)

            st.subheader("📌 Analysis Result")
            st.markdown(sentiment_result)
    else:
        st.warning("⚠️ Please enter a brand name.")
