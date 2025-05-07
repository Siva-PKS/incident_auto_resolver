import openai
import pandas as pd
import os
import smtplib
from email.message import EmailMessage
import streamlit as st

# Access the OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["openai_api_key"]

# Verify if the API key is correctly set (for debugging)
st.write(f"API Key: {openai.api_key}")

# Example OpenAI API call
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt="Say something nice!",
    max_tokens=50
)

st.write(response.choices[0].text.strip())

# Function to find an exact match in a CSV of past tickets
def find_exact_match(description, csv_path='data/tickets.csv'):
    df = pd.read_csv(csv_path)
    match = df[df['description'].str.lower() == description.lower()]
    return match.iloc[0] if not match.empty else None, df

# Function to generate an LLM response using OpenAI
def generate_llm_response(query, df):
    context = "\n".join(
        [f"Issue: {row['description']}\nResolution: {row['resolution']}" for _, row in df.iterrows()]
    )
    prompt = f"""You are an IT helpdesk assistant. Based on the following past tickets, suggest a resolution:

{context}

Now, resolve this issue:
Issue: {query}
Resolution:"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"❌ LLM error: {e}"

# Function to send an email via Gmail SMTP
def send_email(subject, body, to_email):
    from_email = st.secrets.get("email_user")
    app_password = st.secrets.get("email_password")  # Gmail App Password

    if not from_email or not app_password:
        print("Email credentials not configured. Skipping email.")
        return

    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(from_email, app_password)
            smtp.send_message(msg)

        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
