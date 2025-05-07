import streamlit as st
from utils import find_exact_match, send_email, generate_llm_response

st.title("🎫 Incident Auto-Resolver with LLM Fallback")

desc_input = st.text_area("Enter new incident description")
user_email = st.text_input("User Email")

if st.button("Resolve Ticket"):
    if not desc_input or not user_email:
        st.warning("Please enter both the description and user email.")
    else:
        match, df = find_exact_match(desc_input)
        if match is not None:
            st.success("✅ Exact match found!")
            st.write("**Resolution:**", match['resolution'])

            send_email(
                    subject=f"Issue Resolved: {match['description']}",
                     body=f"Here is the resolution:\n\n{match['resolution']}",
                    to_email=match['email']
)
            st.info("📧 Auto-reply email sent via Outlook.")
        else:
            st.warning("No exact match found. Generating suggestion via LLM...")
            suggestion = generate_llm_resolution(desc_input, df)
            st.subheader("🤖 Suggested Resolution")
            st.write(suggestion)

            if st.button("Send Suggested Reply via Outlook"):
                send_outlook_email(
                    to_email=user_email,
                    issue_description=desc_input,
                    resolution=suggestion
                )
                st.success("📤 Suggested resolution emailed via Outlook.")
