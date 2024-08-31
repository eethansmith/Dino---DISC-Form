import streamlit as st
import pandas as pd

# Define the options for the table rows and their corresponding DISC types
most_mapping1 = {
    "Easy-going, Agreeable": "S",
    "Trusting, Believing in others": "I",
    "Adventurous, Risk taker": "*",
    "Tolerant, Respectful": "C"
}

least_mapping1 = {
    "Easy-going, Agreeable": "S",
    "Trusting, Believing in others": "I",
    "Adventurous, Risk taker": "D",
    "Tolerant, Respectful": "C"
}

most_mapping2 = {
    "Soft spoken, Reserved": "C",
    "Optimistic, Visionary": "D",
    "Center of attention, Sociable": "*",
    "Peacemaker, Bring harmony": "S"
}

least_mapping2 = {
    "Soft spoken, Reserved": "*",
    "Optimistic, Visionary": "D",
    "Center of attention, Sociable": "I",
    "Peacemaker, Bring harmony": "S"
}

# Combine all mappings for easy iteration later
all_most_mappings = [most_mapping1, most_mapping2]
all_least_mappings = [least_mapping1, least_mapping2]

# Initialize session state to store selections
if 'most_likely' not in st.session_state:
    st.session_state.most_likely = [None, None]

if 'least_likely' not in st.session_state:
    st.session_state.least_likely = [None, None]

if 'disc_scores' not in st.session_state:
    st.session_state.disc_scores = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}

# Create the table layout with checkbox columns
st.write("### DISC Personality Assessment")
st.write("""Choose the option which best reflects your personality. Select one option as the most likely and one option as the least likely.""")
st.write("""This form should be completed within **7 minutes**, or as close to that as possible.""")

for idx, (most_mapping, least_mapping) in enumerate(zip(all_most_mappings, all_least_mappings)):
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        st.write(f"Most Likely (Set {idx + 1})")

    with col2:
        st.write(f"Least Likely (Set {idx + 1})")

    with col3:
        st.write("Options")

    options = most_mapping.keys()
    for option in options:
        with col1:
            # Handle Most Likely selection
            if st.checkbox("", key=f"most_{option}_{idx}", value=(st.session_state.most_likely[idx] == option), label_visibility="collapsed"):
                st.session_state.most_likely[idx] = option
            elif st.session_state.most_likely[idx] == option:
                st.session_state.most_likely[idx] = None

        with col2:
            # Handle Least Likely selection
            if st.checkbox("", key=f"least_{option}_{idx}", value=(st.session_state.least_likely[idx] == option), label_visibility="collapsed"):
                st.session_state.least_likely[idx] = option
            elif st.session_state.least_likely[idx] == option:
                st.session_state.least_likely[idx] = None
        
        with col3:
            st.write(option)

# Validation and Submission
if all(st.session_state.most_likely) and all(st.session_state.least_likely):
    if any(most == least for most, least in zip(st.session_state.most_likely, st.session_state.least_likely)):
        st.error("The most likely and least likely options cannot be the same for any set. Please choose different options.")
    else:
        if st.button("Submit"):
            # Reset DISC scores before calculation
            st.session_state.disc_scores = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}

            # Calculate DISC scores based on the mappings
            for idx, (most_option, least_option) in enumerate(zip(st.session_state.most_likely, st.session_state.least_likely)):
                most_disc_type = all_most_mappings[idx][most_option]
                least_disc_type = all_least_mappings[idx][least_option]

                st.session_state.disc_scores[most_disc_type] += 1  # Increment for Most Likely
                st.session_state.disc_scores[least_disc_type] += 1  # Increment for Least Likely

            # Prepare data for the table
            data = {
                "Category": ["Most Likely", "Least Likely"],
                "D": [st.session_state.disc_scores["D"], st.session_state.disc_scores["D"]],
                "I": [st.session_state.disc_scores["I"], st.session_state.disc_scores["I"]],
                "S": [st.session_state.disc_scores["S"], st.session_state.disc_scores["S"]],
                "C": [st.session_state.disc_scores["C"], st.session_state.disc_scores["C"]],
                "*": [st.session_state.disc_scores["*"], st.session_state.disc_scores["*"]]
            }

            # Convert to DataFrame and display as a table
            df = pd.DataFrame(data)
            st.write("### DISC Scores Table")
            st.table(df)
else:
    st.error("Please make a selection for both most likely and least likely options in each set.")
