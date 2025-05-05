import openai
import pandas as pd
import win32com.client as win32
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def find_exact_match(description, csv_path='data/tickets.csv'):
    df = pd.read_csv(csv_path)
    match = df[df['description'].str.lower() == description.lower()]
    return match.iloc[0] if not match.empty else None, df

def send_outlook_email(to_email, issue_description, resolution):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = to_email
    mail.Subject = 'IT Ticket Resolution'
    mail.Body = f"""Hello,

Issue: {issue_description}
Resolution: {resolution}

Let us know if the issue persists.

Best,
IT Support"""
    mail.Send()

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
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message['content'].strip()
