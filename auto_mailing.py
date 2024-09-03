import os
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import streamlit as st

load_dotenv()

def send_email(subject, message, to_email):
    from_email = 'dino.disc.results@mail.com'
    from_password = '!DinoDiscPassword!'

    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the message to the MIME message
    msg.attach(MIMEText(message, 'plain'))

    # Use the SMTP server for mail.com
    server = smtplib.SMTP('smtp.mail.com', 587)  # mail.com SMTP server
    server.starttls()  # Start TLS encryption
    server.login(from_email, from_password)  # Log in to the server

    # Send the email
    server.send_message(msg)
    server.quit()

# Call this function after the user completes the form
def process_results_and_send_email():
    # Prepare the results
    user_name = st.session_state.user_details['name']
    results_message = f"""
    DISC Assessment Results for {user_name}\n\n
    Most Likely Scores:\n
    D: {st.session_state.disc_scores_most['D']}\n
    I: {st.session_state.disc_scores_most['I']}\n
    S: {st.session_state.disc_scores_most['S']}\n
    C: {st.session_state.disc_scores_most['C']}\n\n
    Least Likely Scores:\n
    D: {st.session_state.disc_scores_least['D']}\n
    I: {st.session_state.disc_scores_least['I']}\n
    S: {st.session_state.disc_scores_least['S']}\n
    C: {st.session_state.disc_scores_least['C']}\n
    """

    # Send the email with the results
    send_email(
        subject=f"DISC Assessment Results for {user_name}",
        message=results_message,
        to_email="ethan.a.smith@hotmail.co.uk"
    )
    st.write("Results have been sent to your email.")
