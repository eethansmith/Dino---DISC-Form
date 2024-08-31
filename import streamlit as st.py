import streamlit as st
import pandas as pd
import json

# Load mappings from JSON file
with open('disc_mappings.json', 'r') as f:
    mappings = json.load(f)

# Extract mappings
mapping1 = mappings["mapping1"]
mapping2 = mappings["mapping2"]

all_mappings = [mapping1, mapping2]

# Initialize session state to store selections
if 'most_likely' not in st.session_state:
    st.session_state.most_likely = [None, None]

if 'least_likely' not in st.session_state:
    st.session_state.least_likely = [None, None]

if 'disc_scores_most' not in st.session_state:
    st.session_state.disc_scores_most = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}

if 'disc_scores_least' not in st.session_state:
    st.session_state.disc_scores_least = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}

# Define a function to ensure only one checkbox is selected at a time in a column
def on_change_checkbox(current_key, idx, column):
    for key in st.session_state.checkbox_keys[idx][column]:
        if key != current_key:
            st.session_state[key] = False

# Initialize the keys for checkboxes
st.session_state.checkbox_keys = [[[], []], [[], []]]  # Separate lists for each table's most and least likely

# Create the table layout with checkboxes
st.write("### DISC Personality Assessment")
st.write("""Choose the option which best reflects your personality. Select one option as the **most likely** and one option as the **least likely**.""")
st.write("""This form should be completed within **7 minutes**, or as close to that as possible.""")

for idx, mapping in enumerate(all_mappings):
    col1, col2, col3 = st.columns([1, 1, 5])

    with col1:
        st.write("**Most Likely**")
        for option in mapping.keys():
            key = f"most_{idx}_{option}"
            st.checkbox("", key=key, on_change=on_change_checkbox, args=(key, idx, 0))
            st.session_state.checkbox_keys[idx][0].append(key)

    with col2:
        st.write("**Least Likely**")
        for option in mapping.keys():
            key = f"least_{idx}_{option}"
            st.checkbox("", key=key, on_change=on_change_checkbox, args=(key, idx, 1))
            st.session_state.checkbox_keys[idx][1].append(key)

    with col3:
        st.write("**Options**")
        for option in mapping.keys():
            st.write(option)

# Validation and Submission
most_likely_selections = [key for idx in range(len(all_mappings)) for key in st.session_state.checkbox_keys[idx][0] if st.session_state.get(key)]
least_likely_selections = [key for idx in range(len(all_mappings)) for key in st.session_state.checkbox_keys[idx][1] if st.session_state.get(key)]

if len(most_likely_selections) == len(all_mappings) and len(least_likely_selections) == len(all_mappings):
    if any(most.split("_")[2] == least.split("_")[2] for most, least in zip(most_likely_selections, least_likely_selections)):
        st.error("The most likely and least likely options cannot be the same for any set. Please choose different options.")
    else:
        if st.button("Submit"):
            # Reset DISC scores before calculation
            st.session_state.disc_scores_most = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}
            st.session_state.disc_scores_least = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}

            # Calculate DISC scores based on the mappings
            for most_key, least_key in zip(most_likely_selections, least_likely_selections):
                idx = int(most_key.split("_")[1])
                most_option = most_key.split("_")[2]
                least_option = least_key.split("_")[2]

                most_disc_type = all_mappings[idx][most_option]["most"]
                least_disc_type = all_mappings[idx][least_option]["least"]

                st.session_state.disc_scores_most[most_disc_type] += 1  # Increment for Most Likely
                st.session_state.disc_scores_least[least_disc_type] += 1  # Increment for Least Likely

            # Prepare data for the table
            data = {
                "Category": ["Most Likely", "Least Likely"],
                "D": [st.session_state.disc_scores_most["D"], st.session_state.disc_scores_least["D"]],
                "I": [st.session_state.disc_scores_most["I"], st.session_state.disc_scores_least["I"]],
                "S": [st.session_state.disc_scores_most["S"], st.session_state.disc_scores_least["S"]],
                "C": [st.session_state.disc_scores_most["C"], st.session_state.disc_scores_least["C"]],
                "*": [st.session_state.disc_scores_most["*"], st.session_state.disc_scores_least["*"]]
            }

            df = pd.DataFrame(data)

            # Use the 'columns' argument to exclude the index explicitly
            st.write("### DISC Scores Table")
            st.write(df.to_html(index=False), unsafe_allow_html=True)

else:
    st.error("Please make a selection for both most likely and least likely options in each set.")
