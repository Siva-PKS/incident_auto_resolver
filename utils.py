import openai
import pandas as pd
import os
import smtplib
from email.message import EmailMessage
import streamlit as st

openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("openai_api_key"))

# Function to find exact match from past tickets (CSV)
def find_exact_match(description, csv_path='data/tickets.csv'):
    df = pd.read_csv(csv_path)
    match = df[df['description'].str.lower() == description.lower()]
    return match.iloc[0] if not match.empty else None, df

# Function to send email via Gmail SMTP
def send_email(subject, body, to_email):
    from_email = st.secrets.get("email_user")
    app_password = st.secrets.get("email_password")  # Use Gmail App Password

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

        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to generate resolution using OpenAI LLM based on past tickets
def generate_llm_resolution(query, df):
    context = "\n".join(
        [f"Issue: {row['description']}\nResolution: {row['resolution']}" for _, row in df.iterrows()]
    )
    prompt = f"""You are an IT helpdesk assistant. Based on the following past tickets, suggest a resolution:

{context}

Now, resolve this issue:
Issue: {query}
Resolution:"""

    response = openai.ChatCompletion.create(
        model="gpt-4",  # You can adjust the model if needed
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message['content'].strip()

