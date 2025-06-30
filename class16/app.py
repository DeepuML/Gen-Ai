import streamlit as st
import requests
import re
import json
import os
import pandas as pd
from dotenv import load_dotenv
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# === Load secrets from .env ===
load_dotenv()
EURI_API_URL =  os.getenv("EURI_API_URL")
EURI_API_KEY = os.getenv("EURI_API_KEY")
MODEL = os.getenv("MODEL", "gemini-2.0-flash-001")

# === Sentiment Categories ===
SENTIMENT_TYPES = [
    "Very Positive", "Positive", "Neutral", "Negative", "Very Negative", "Sarcastic", "Political",
    "Joy", "Sadness", "Anger", "Fear", "Surprise", "Disgust", "Humorous", "Critical", "Mixed",
    "Promotional", "Complaint", "Supportive", "Suggestion"
]

# === Prompt Template ===
def build_sentiment_prompt(text):
    return f"""
You are a professional sentiment analysis system. Analyze the following text and classify its sentiment as one of the following:
{", ".join(SENTIMENT_TYPES)}

Also, explain the reasoning briefly.

Text:
\"\"\"{text}\"\"\"

Respond strictly in the following JSON format:
{{
  "sentiment": "...",
  "reason": "..."
}}
"""

# === API Call ===
def get_sentiment_analysis(text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {EURI_API_KEY}"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a professional sentiment analysis bot."},
            {"role": "user", "content": build_sentiment_prompt(text)}
        ],
        "max_tokens": 500,
        "temperature": 0.3
    }

    response = requests.post(EURI_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            raw_result = response.json()["choices"][0]["message"]["content"]
            cleaned = re.sub(r"```json|```", "", raw_result).strip()
            return json.loads(cleaned)
        except Exception:
            return {"error": "⚠️ Failed to parse result", "raw_output": raw_result}
    else:
        return {"error": f"❌ Failed: {response.status_code}", "details": response.text}

# === Word Cloud ===
def show_wordcloud(text):
    wordcloud = WordCloud(width=600, height=300, background_color='white').generate(text)
    plt.figure(figsize=(10, 4))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# === Streamlit UI ===
st.set_page_config(page_title="📊 Sentiment Analysis Dashboard", layout="centered")
st.title("📊 Advanced Real-Time Sentiment Tracker")
st.markdown("Analyze your text or CSV file for **deep sentiment insights** using EURI AI.")

# === Single Text Input ===
st.subheader("📝 Analyze Single Text")
text_input = st.text_area("Enter your text here:")

if st.button("🔍 Analyze Sentiment"):
    if text_input.strip():
        with st.spinner("Analyzing..."):
            result = get_sentiment_analysis(text_input)
        if "error" in result:
            st.error(result["error"])
            if "raw_output" in result:
                st.code(result["raw_output"], language="json")
            elif "details" in result:
                st.code(result["details"])
        else:
            st.success("✅ Analysis Complete")
            st.json(result)
            show_wordcloud(text_input)
    else:
        st.warning("⚠️ Please enter some text.")

# === Batch Analysis ===
st.subheader("📁 Upload CSV for Batch Sentiment Analysis")
uploaded_file = st.file_uploader("Upload CSV file with a 'text' column", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'text' not in df.columns:
        st.error("❌ CSV must have a 'text' column.")
    else:
        st.info(f"Found {len(df)} texts. Starting batch analysis...")
        results = []
        for i, row in df.iterrows():
            with st.spinner(f"Analyzing row {i + 1}/{len(df)}"):
                res = get_sentiment_analysis(row['text'])
                results.append({
                    "text": row['text'],
                    "sentiment": res.get("sentiment", "error"),
                    "reason": res.get("reason", res.get("error", "unknown"))
                })

        result_df = pd.DataFrame(results)
        st.dataframe(result_df)

        # Visualization
        st.subheader("📊 Sentiment Distribution")
        chart_data = result_df["sentiment"].value_counts().reset_index()
        chart_data.columns = ["Sentiment", "Count"]
        st.bar_chart(chart_data.set_index("Sentiment"))

        # Word Cloud from batch
        all_text = " ".join(result_df["text"])
        st.subheader("☁️ Word Cloud from All Texts")
        show_wordcloud(all_text)

        # Downloadable results
        st.download_button("📥 Download Results as CSV", result_df.to_csv(index=False), "sentiment_results.csv", "text/csv")
