import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from datetime import date, datetime

from auto_mailing import send_email, process_results_and_send_email

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from tabulate import tabulate
import smtplib



# Load mappings from JSON file
with open('disc_mappings.json', 'r') as f:
    mappings = json.load(f)

# Extract all mappings dynamically
all_mappings = [mappings[f"mapping{i}"] for i in range(1, 25)]  # Adjust range based on the number of mappings in your JSON

# Initialize session state to store user details and selections
if 'user_details' not in st.session_state:
    st.session_state.user_details = {
        "name": "",
        "date_of_birth": None,
        "gender": ""
    }

# Initialize session state to store selections
if 'most_likely' not in st.session_state:
    st.session_state.most_likely = [None] * len(all_mappings)

if 'least_likely' not in st.session_state:
    st.session_state.least_likely = [None] * len(all_mappings)

if 'disc_scores_most' not in st.session_state:
    st.session_state.disc_scores_most = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}

if 'disc_scores_least' not in st.session_state:
    st.session_state.disc_scores_least = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}

if 'current_section' not in st.session_state:
    st.session_state.current_section = 0  # Start at the first section

if 'same_option_error' not in st.session_state:
    st.session_state.same_option_error = False  # Initialize error flag

if 'user_selections' not in st.session_state:
    st.session_state.user_selections = []
    
if 'assessment_completed' not in st.session_state:
    st.session_state.assessment_completed = False  # Initialize assessment completion status

# Function to handle the first section for user details
def input_user_details():
        # Create the table layout with checkboxes
    st.write(f"### DISC Personality Assessment")
    st.write("""Choose the option which best reflects your personality. Select one option as the **most likely** and one option as the **least likely**.""")
    st.write("""This form should be completed within **7 minutes**, or as close to that as possible.""")

    
    st.write("### Please fill in your details")
    
    # Collect user details
    st.session_state.user_details['name'] = st.text_input("Name *", st.session_state.user_details['name'])
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
    if next_button_clicked and not st.session_state.user_details['name']:
        st.error("Name is required to proceed.")
    elif next_button_clicked:
        st.session_state.current_section = 1  # Move to the first question of the DISC assessment
        st.rerun()
        
# Define a function to ensure only one checkbox is selected at a time in a column
def on_change_checkbox(current_key, idx, column):
    # Ensure only one checkbox is selected in the current column
    for key in st.session_state.checkbox_keys[idx][column]:
        if key != current_key:
            st.session_state[key] = False

    # Check if the same option is selected for both most and least likely
    other_column = 1 - column
    current_option = current_key.split("_")[2]
    conflicting_key = f"{'most' if other_column == 0 else 'least'}_{idx}_{current_option}"
    
    if st.session_state.get(current_key) and st.session_state.get(conflicting_key):
        st.session_state[current_key] = False  # Reset the current selection
        st.session_state.same_option_error = True  # Set error flag
    else:
        st.session_state.same_option_error = False  # Reset error flag if no conflict

# Initialize the keys for checkboxes
st.session_state.checkbox_keys = [[[], []] for _ in all_mappings]  # Adjust lists based on the number of mappings
# Function to save user's selections for the current section
def save_selections(idx):
    most_likely_key = next((key for key in st.session_state.checkbox_keys[idx][0] if st.session_state.get(key)), None)
    least_likely_key = next((key for key in st.session_state.checkbox_keys[idx][1] if st.session_state.get(key)), None)

    if most_likely_key and least_likely_key:
        most_option = most_likely_key.split("_")[2]
        least_option = least_likely_key.split("_")[2]

        # Save the selection as a dictionary
        st.session_state.user_selections.append({
            "section": idx,
            "most_likely": most_option,
            "least_likely": least_option
        })
        
        
def auto_mail_results(user_name):
    me = 'disc.assessment.results@gmail.com'
    password = 'ngpb dgna afkw guuu'
    you = 'dino.grif@gmail.com'
    server = 'smtp.gmail.com:587'

    # Prepare DISC data for the table
    data = [
        ["Category", "D", "I", "S", "C", "*", "Total"],
        ["Most Likely", st.session_state.disc_scores_most['D'], st.session_state.disc_scores_most['I'], st.session_state.disc_scores_most['S'], st.session_state.disc_scores_most['C'], st.session_state.disc_scores_most['*'], sum(st.session_state.disc_scores_most.values())],
        ["Least Likely", st.session_state.disc_scores_least['D'], st.session_state.disc_scores_least['I'], st.session_state.disc_scores_least['S'], st.session_state.disc_scores_least['C'], st.session_state.disc_scores_least['*'], sum(st.session_state.disc_scores_least.values())],
        ["Difference", st.session_state.disc_scores_most['D'] - st.session_state.disc_scores_least['D'], st.session_state.disc_scores_most['I'] - st.session_state.disc_scores_least['I'], st.session_state.disc_scores_most['S'] - st.session_state.disc_scores_least['S'], st.session_state.disc_scores_most['C'] - st.session_state.disc_scores_least['C'], "-", (st.session_state.disc_scores_most['D'] - st.session_state.disc_scores_least['D']) + (st.session_state.disc_scores_most['I'] - st.session_state.disc_scores_least['I']) + (st.session_state.disc_scores_most['S'] - st.session_state.disc_scores_least['S']) + (st.session_state.disc_scores_most['C'] - st.session_state.disc_scores_least['C'])]
    ]

    # Create plain text and HTML versions of the message
    text = f"""
    This is confirmation of the completion of the DISC Assessment by {user_name}.
    
    Date of Birth: {st.session_state.user_details['date_of_birth']}
    Gender: {st.session_state.user_details['gender']}
    
    DISC Results:

    {tabulate(data, headers="firstrow", tablefmt="grid")}

    """

    html = f"""
    <html><body><p>This is confirmation of the completion of the DISC Assessment by {user_name}.</p>
    <p>Date of Birth: {st.session_state.user_details['date_of_birth']}</p>
    <p>Gender: {st.session_state.user_details['gender']}</p>
    {tabulate(data, headers="firstrow", tablefmt="html")}
    <p>See attached images for the plotted DISC scores:</p>
    <img src="cid:image1"><br>
    <img src="cid:image2"><br>
    <img src="cid:image3"><br>
    </body></html>
    """

    # Construct the email
    message = MIMEMultipart("related")
    message['Subject'] = f"DISC Assessment Results | {user_name}"
    message['From'] = me
    message['To'] = you

    # Attach text and HTML versions of the email
    message_alternative = MIMEMultipart("alternative")
    message.attach(message_alternative)
    message_alternative.attach(MIMEText(text, 'plain'))
    message_alternative.attach(MIMEText(html, 'html'))

    # Save plots as images and attach them
    images = []

    # Plot Most Likely
    plt.figure(figsize=(6, 3))
    plt.plot(categories, most_likely_scores, marker='o', linestyle='-', color='blue')
    plt.title('Most Likely DISC Scores')
    plt.xlabel('DISC Category')
    plt.ylabel('Score')
    plt.grid(True)
    plt.savefig('/tmp/most_likely.png')
    plt.close()
    images.append(('/tmp/most_likely.png', 'image1'))

    # Plot Least Likely
    plt.figure(figsize=(6, 3))
    plt.plot(categories, least_likely_scores, marker='o', linestyle='-', color='green')
    plt.title('Least Likely DISC Scores')
    plt.xlabel('DISC Category')
    plt.ylabel('Score')
    plt.grid(True)
    plt.savefig('/tmp/least_likely.png')
    plt.close()
    images.append(('/tmp/least_likely.png', 'image2'))

    # Plot Difference
    plt.figure(figsize=(6, 3))
    plt.plot(categories, difference_scores, marker='o', linestyle='-', color='red')
    plt.title('Difference in DISC Scores (Most - Least)')
    plt.xlabel('DISC Category')
    plt.ylabel('Score Difference')
    plt.grid(True)
    plt.savefig('/tmp/difference.png')
    plt.close()
    images.append(('/tmp/difference.png', 'image3'))

    # Attach the images to the email
    for file_path, cid in images:
        with open(file_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-ID', f'<{cid}>')
            message.attach(img)

    # Send the email
    smtp_server = smtplib.SMTP(server)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login(me, password)
    smtp_server.sendmail(me, you, message.as_string())
    smtp_server.quit()
    print('Email sent successfully')    
    

# Calculate DISC scores after saving selections
def calculate_disc_scores():
    # Initialize DISC scores
    st.session_state.disc_scores_most = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}
    st.session_state.disc_scores_least = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}

    # Loop through saved selections to calculate DISC scores
    for selection in st.session_state.user_selections:
        idx = selection["section"]
        most_option = selection["most_likely"]
        least_option = selection["least_likely"]

        most_disc_type = all_mappings[idx][most_option]["most"]
        least_disc_type = all_mappings[idx][least_option]["least"]

        st.session_state.disc_scores_most[most_disc_type] += 1  # Increment for Most Likely
        st.session_state.disc_scores_least[least_disc_type] += 1  # Increment for Least Likely

# Show the form or the result depending on the assessment completion status
if st.session_state.current_section == 0:
    input_user_details()  # First, prompt the user to fill in their details
elif not st.session_state.assessment_completed:
    idx = st.session_state.current_section - 1  # Adjust the section index because the first section is user details
    mapping = all_mappings[idx]

# Calculate progress
    progress = f"{idx + 1}/{len(all_mappings)}"

    # Create the table layout with checkboxes
    st.write(f"### DISC Personality Assessment ({progress})")
    st.write("""Choose the option which best reflects your personality. Select one option as the **most likely** and one option as the **least likely**.""")
    st.write("""This form should be completed within **7 minutes**, or as close to that as possible.""")

    col1, col2, col3 = st.columns([1, 1, 3])

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

    # Display the same option error message
    if st.session_state.same_option_error:
        st.error("You cannot select the same option for both 'Most Likely' and 'Least Likely'. Please choose different options.")

    # Validation and Submission
    most_likely_selected = any(st.session_state.get(key) for key in st.session_state.checkbox_keys[idx][0])
    least_likely_selected = any(st.session_state.get(key) for key in st.session_state.checkbox_keys[idx][1])

    if most_likely_selected and least_likely_selected:
        if idx < len(all_mappings) - 1:
            # Handle button click before rerendering the UI
            if st.button("Next"):
                save_selections(idx)
                st.session_state.current_section += 1
                st.rerun()  # Force a rerun to immediately update the section
        else:
            if st.button("Submit"):
                save_selections(idx)
                # Reset DISC scores before calculation
                calculate_disc_scores()
                st.session_state.assessment_completed = True
                st.rerun()  # Force a rerun to display the result
    else: 
        st.error("Please make a selection for both 'Most Likely' and 'Least Likely' options.")
# ...

else:
    # Calculate the sum for each row
    sum_most = sum(st.session_state.disc_scores_most.values())
    sum_least = sum(st.session_state.disc_scores_least.values())

    # Calculate the difference between Most Likely and Least Likely (excluding the * column)
    diff_D = st.session_state.disc_scores_most["D"] - st.session_state.disc_scores_least["D"]
    diff_I = st.session_state.disc_scores_most["I"] - st.session_state.disc_scores_least["I"]
    diff_S = st.session_state.disc_scores_most["S"] - st.session_state.disc_scores_least["S"]
    diff_C = st.session_state.disc_scores_most["C"] - st.session_state.disc_scores_least["C"]
    diff_total = diff_D + diff_I + diff_S + diff_C

    # Prepare data for the table including the sum and difference row
    data = {
        "Category": ["Most Likely", "Least Likely", "Difference"],
        "D": [st.session_state.disc_scores_most["D"], st.session_state.disc_scores_least["D"], diff_D],
        "I": [st.session_state.disc_scores_most["I"], st.session_state.disc_scores_least["I"], diff_I],
        "S": [st.session_state.disc_scores_most["S"], st.session_state.disc_scores_least["S"], diff_S],
        "C": [st.session_state.disc_scores_most["C"], st.session_state.disc_scores_least["C"], diff_C],
        "*": [st.session_state.disc_scores_most["*"], st.session_state.disc_scores_least["*"], "-"],  # Exclude * from Difference calculation
        "Total": [sum_most, sum_least, diff_total]  # Add the sum as the final column
    }

    df = pd.DataFrame(data)

    # Comment out or remove the following lines to prevent displaying the table and plots
    # st.write("### DISC Scores Table")
    # st.write(df.to_html(index=False), unsafe_allow_html=True)
        
    # Plot the line graphs
    categories = ["D", "I", "S", "C"]
    most_likely_scores = [st.session_state.disc_scores_most[cat] for cat in categories]
    least_likely_scores = [st.session_state.disc_scores_least[cat] for cat in categories]
    difference_scores = [diff_D, diff_I, diff_S, diff_C]

    # Comment out or remove the following lines to prevent displaying the plots
    # Plot Most Likely
    # plt.figure(figsize=(10, 4))
    # plt.plot(categories, most_likely_scores, marker='o', linestyle='-', color='blue')
    # plt.title('Most Likely DISC Scores')
    # plt.xlabel('DISC Category')
    # plt.ylabel('Score')
    # plt.grid(True)
    # st.pyplot(plt)

    # Plot Least Likely
    # plt.figure(figsize=(10, 4))
    # plt.plot(categories, least_likely_scores, marker='o', linestyle='-', color='green')
    # plt.title('Least Likely DISC Scores')
    # plt.xlabel('DISC Category')
    # plt.ylabel('Score')
    # plt.grid(True)
    # st.pyplot(plt)

    # Plot Difference
    # plt.figure(figsize=(10, 4))
    # plt.plot(categories, difference_scores, marker='o', linestyle='-', color='red')
    # plt.title('Difference in DISC Scores (Most - Least)')
    # plt.xlabel('DISC Category')
    # plt.ylabel('Score Difference')
    # plt.grid(True)
    # st.pyplot(plt)
    
    # Thank you message
    user_name = st.session_state.user_details['name']
    auto_mail_results(user_name)
    st.write(f"### Thank you, {user_name}, for completing the assessment!")
    st.write("Your results have been sent to Dino.")
