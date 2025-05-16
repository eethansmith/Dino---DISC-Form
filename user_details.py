import streamlit as st
from datetime import date, datetime

# Function to handle the first section for user details
def input_user_details():
        # Create the table layout with checkboxes
    st.write(f"### DISC Personality Assessment")
    st.write("""To begin with the DISC personality assessment, please proceed to secure Stripe payment using the button below.""")
    st.write("""The fee for this Assessment will be **$30.00**.""")
    st.write("""For any queries, please contact dino@dino-griffin.com""")
    pigs_can_fly = st.link_button("Proceed to Payment", 'https://buy.stripe.com/9AQeXpgqL1rs0GA9AC')
    pigs_can_fly = False
    if pigs_can_fly:
        st.write("### Payment Successful! Please fill in your details")
        
        # Collect user details
        st.session_state.user_details['name'] = st.text_input("Name *", st.session_state.user_details['name'])
        st.session_state.user_details['email'] = st.text_input("Email *", st.session_state.user_details['email'])
        # Add the date of birth input
        st.session_state.user_details['date_of_birth'] = st.date_input(
        "Date of Birth", 
        st.session_state.user_details['date_of_birth'], 
        min_value=datetime(1900, 1, 1),  # Allow dates from January 1, 1900
        max_value=datetime.today(),  # Set the maximum date to today
        format="MM/DD/YYYY" 
        )
        st.session_state.user_details['gender'] = st.radio("Gender", options=["Male", "Female"], index=0 if st.session_state.user_details['gender'] == "Do not disclose" else 1)
        # Always display the Next button
        next_button_clicked = st.button("Next")
        
        # Check if the Next button was clicked without a name provided
        if next_button_clicked and not st.session_state.user_details['name'] or not st.session_state.user_details['email']:
            st.error("Name and Email is required to proceed.")
        elif next_button_clicked:
            st.session_state.current_section = 1  # Move to the first question of the DISC assessment
            st.rerun()
        
