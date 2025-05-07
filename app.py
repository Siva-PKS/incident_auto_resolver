import streamlit as st
from utils import find_exact_match, send_email, generate_llm_response

st.title("🎫 Incident Auto-Resolver with LLM Fallback")

# User inputs
desc_input = st.text_area("Enter new incident description")
user_email = st.text_input("User Email")

# Button to trigger resolution
if st.button("Resolve Ticket"):
    if not desc_input or not user_email:
        st.warning("Please enter both the description and user email.")
    else:
        # Check for exact match
        match, df = find_exact_match(desc_input)
        
        if match is not None:
            st.success("✅ Exact match found!")
            st.write("**Resolution:**", match['resolution'])

            # Send the resolution via email
            send_email(
                subject=f"Issue Resolved: {match['description']}",
                body=f"Here is the resolution:\n\n{match['resolution']}",
                to_email=user_email
            )
            st.info("📧 Auto-reply email sent to your email address.")
        else:
            st.warning("No exact match found. Generating suggestion via LLM...")
            suggestion = generate_llm_response(desc_input, df)
            st.subheader("🤖 Suggested Resolution")
            st.write(suggestion)

            # Button to send the generated LLM resolution via email
            if st.button("Send Suggested Reply via Email"):
                send_email(
                    subject="Suggested Resolution to Your Reported Issue",
                    body=f"Issue: {desc_input}\n\nSuggested Resolution:\n{suggestion}",
                    to_email=user_email
                )
                st.success("📤 Suggested resolution emailed to you.")
