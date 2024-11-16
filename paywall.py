import streamlit as st
from st_paywall import add_auth

def access_paywall():
    st.write(f"### DISC Personality Assessment")

    st.write("""To Proceed with the DISC personality assessment, please complete authentication and proceed to secure payment.""")
    st.write("""The fee for this Assessment will be **$0.00**, payment processed my Stripe.""")

    add_auth(required = True)
    if st.button("Proceed to Payment"):
        return