import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Data points and labels
labels = ['D', 'I', 'S', 'C']
values = [7, 6, 3, 1]
positions = np.arange(len(labels))  # x positions for the labels

# Create a Streamlit app
st.title("DISC Profile Graph")
st.write("This graph displays values for the DISC profile.")

# Plot the line graph
fig, ax = plt.subplots()
ax.plot(positions, values, marker='o', linestyle='-')  # Connect points with a line

# Set y-axis to range from 0 to 80, and add grid lines at every 10 units
ax.set_ylim(0, 80)  # Set y limits from 0 to 80
ax.set_yticks(np.arange(0, 81, 10))  # Set y ticks to show every 10 units
ax.grid(which='major', axis='y', linestyle='--', linewidth=0.5, color='gray')  # Add horizontal grid lines

# Update x-axis settings
ax.set_xticks([])  # Remove x-axis ticks
ax.spines['bottom'].set_visible(False)  # Hide the bottom spine
ax.spines['left'].set_visible(False)  # Optionally, hide the left spine if preferred

# Create a secondary x-axis at the top
ax2 = ax.twiny()  # Create a second x-axis
ax2.set_xlim(ax.get_xlim())  # Ensure the limits are the same
ax2.set_xticks(positions)
ax2.set_xticklabels(labels)
ax2.spines['top'].set_visible(False)  # Optionally hide the top spine if preferred

st.pyplot(fig)


#Most

#D: 0=9 , 1=14 , 2=20 , 3=28 , 4=32 , 5=35 , 6=39 , 7=43 , 8=45, 9=50, 10=55, 11=57, 12=59, 13=64, 14=66, 15=73, 16=75, 17,18,19,20=76, 21=77, 22=78, 23=79 24=80
#I: 0=4 , 1=16 , 2=28 , 3=35 , 4=45 , 5=55 , 6=57 , 7=66 , 8=68, 9=70, 10=73, 11 = 75, 12,13,14,15,16,17,18=76 , 19,20= 77 , 21=78 , 22=78 , 23=79 , 24 = 80  
#S: 0=12 , 1=18, 2=22 , 3=32 , 4=37 , 5=43 , 6=45 , 7=53 , 8=55 , 9=59, 10=64, 11=66, 12=68, 13=70, 14=73 , 15=73 , 16=74 , 17=74 , 18=75, 19=76, 20=77 , 21=78 , 22=79 , 23=80 , 24 = 80
#C: 0=9 , 1=16 , 2=22 , 3=32 , 4=43 , 5=50 , 6=55 , 7=66 , 8=68, 9=70, 10=71, 11 = 73, 12=74,13=75,14=75,15=76,16=76,17=77,18=77 , 19=78,20= 78 , 21=79 , 22=79 , 23=80 , 24 = 80

#thin dotted line = 10
#thick dotted line = 20
#thin dotted line = 30
#thick solid line = 40
#thin dotted line = 50
#thick dotted line = 60
#thin dotted line = 70
#top of graph = 80