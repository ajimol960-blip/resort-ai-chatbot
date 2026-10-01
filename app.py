import os
import threading
from email.message import EmailMessage
import smtplib
from libs.menu_loader import load_menu
from libs.llm_utils import send_message_to_llm,start_session
import streamlit as st



# ---------------------------------------------------------
# 1. Email Sending Function with Detailed Booking Summary
# ---------------------------------------------------------
def send_booking_email(summary_text):
    msg = EmailMessage()
    msg['Subject'] = '🔔 New Confirmed Booking Summary - Munnar Gate Residency'
    msg['From'] = 'alnahdhashj4@gmail.com'
    msg['To'] = 'alnahdhashj4@gmail.com'  # Management email

    # Email body formatted with full details
    email_body = f"""
Dear Management,

A new booking summary has been generated via the AI Assistant:

--------------------------------------------------
{summary_text}
--------------------------------------------------

Please check and follow up with the guest accordingly.
"""
    msg.set_content(email_body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


# ---------------------------------------------------------
# 2. UI Setup
# ---------------------------------------------------------
menu_text = load_menu()
st.markdown(
    "<h1 style='font-size:32px; white-space:nowrap;'>🌃 Munnar Gate Residency 🌃 AI Assistant</h1>",
    unsafe_allow_html=True
)
# st.title(" 🌃 Munnar Gate Residency 🌃  AI Assistant")
st.markdown("Gateway of Munnar | Poopara, Munnar | Room Booking & Safari")

# ---------------------------------------------------------
# 3. Session State Initialization
# ---------------------------------------------------------
if "messages" not in st.session_state:
    start_session()
    welcome_message = (
        "Welcome to Munnar Gate Residency! 🌿\n\n"
        "Here are our room options and services:\n" + menu_text + "\n\n"
        "How can I help you with your booking today?"
    )
    st.session_state.messages = [{"role": "ai", "content": welcome_message}]

# ---------------------------------------------------------
# 4. Chat Input & Logic
# ---------------------------------------------------------
user_input = st.chat_input("Enter Your Message...")

if user_input:
    # Append user input
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get response from LLM
    llm_resp = send_message_to_llm(user_input)

    # Append AI response
    st.session_state.messages.append({"role": "ai", "content": llm_resp})

    # Check if the LLM response or user input contains a booking summary structure
    if "Booking Summary:" in llm_resp or "Booking Summary" in user_input:
        # send_booking_email(llm_resp)
        threading.Thread(target=send_booking_email, args=(llm_resp,)).start()

# ---------------------------------------------------------
# 5. Display Chat Messages
# ---------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
