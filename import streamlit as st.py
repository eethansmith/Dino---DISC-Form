import streamlit as st

# Define the options for the table rows
options = ["Option 1", "Option 2", "Option 3", "Option 4"]

# Initialize session state to store selections
if 'most_likely' not in st.session_state:
    st.session_state.most_likely = None

if 'least_likely' not in st.session_state:
    st.session_state.least_likely = None

# Create the table layout with checkbox columns
st.write("### Choose the most likely and least likely options:")

col1, col2, col3 = st.columns([1, 1, 4])

with col1:
    st.write("Most Likely")

with col2:
    st.write("Least Likely")

with col3:
    st.write("Options")

for option in options:
    with col1:
        # Handle Most Likely selection
        if st.checkbox("", key=f"most_{option}", value=(st.session_state.most_likely == option), label_visibility="collapsed"):
            st.session_state.most_likely = option
        elif st.session_state.most_likely == option:
            st.session_state.most_likely = None

    with col2:
        # Handle Least Likely selection
        if st.checkbox("", key=f"least_{option}", value=(st.session_state.least_likely == option), label_visibility="collapsed"):
            st.session_state.least_likely = option
        elif st.session_state.least_likely == option:
            st.session_state.least_likely = None
    
    with col3:
        st.write(option)

# Validation and Submission
if st.session_state.most_likely and st.session_state.least_likely:
    if st.session_state.most_likely == st.session_state.least_likely:
        st.error("The most likely and least likely options cannot be the same. Please choose different options.")
    else:
        if st.button("Submit"):
            st.success(f"You selected '{st.session_state.most_likely}' as Most Likely and '{st.session_state.least_likely}' as Least Likely.")
else:
    st.error("Please make a selection for both most likely and least likely options.")
