# 🎫 Incident Ticket Auto-Resolver (LLM + Outlook + Streamlit)

This app auto-resolves IT tickets by checking for exact matches and sending replies via Outlook. If no match is found, it uses OpenAI GPT to suggest a resolution.

## 🔧 Requirements
- Windows with Outlook configured
- Python 3.8+
- OpenAI API key

## 📦 Setup

```bash
git clone https://github.com/your-org/incident_auto_resolver.git
cd incident_auto_resolver
pip install -r requirements.txt
```

Create a `.env` file with your OpenAI key:

```
OPENAI_API_KEY=your-api-key
```

## 🚀 Run the App

```bash
streamlit run app.py
```

## 📧 Email Sending

- Exact match → auto email via Outlook
- No match → LLM suggests → user manually clicks to send
