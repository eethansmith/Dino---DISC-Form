# DISC Personality Assessment Tool

## Overview

This Streamlit-based application serves as an interactive form for analyzing individuals' personality types based on the DISC assessment method. Users answer a series of questions, and their responses are scored and categorized into DISC dimensions. The tool is designed to replace traditional hand-drawing methods with a digital solution that includes graphical representations of assessment results.

## Features

- **Interactive Form**: Users input their responses directly through the Streamlit application.
- **Scoring System**: Each answer contributes to the user’s score in one of the DISC categories (Dominance, Influence, Steadiness, Conscientiousness).
- **Graphical Results**: Upon completion, participants receive a graph visualizing their scores in each DISC category, making it easier to analyze personality traits.
- **Email Integration**: Detailed results, including graphical representations, are automatically emailed to the customer, providing a record of each assessment.

## Technology Stack

- **Streamlit**: For creating the interactive web application.
- **Python**: Backend logic for scoring and data handling.
- **Matplotlib**: For generating graphical representations of the DISC scores.
- **SMTP Library**: For sending emails with the results.

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourgithubusername/disc-personality-assessment.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd disc-personality-assessment
   ```
3. **Install required libraries**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Usage

- Start the application and access it through a web browser at `localhost:8501`.
- Follow the on-screen instructions to complete the DISC assessment.
- Upon completion, check your email for the assessment results.

## Contribution

- **Bug Fixes**: Submit an issue on GitHub if you encounter any bugs.
- **Features**: Propose new features or enhancements through GitHub issues.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.

## Contact

For support or queries, please email [ethan.a.smith@hotmail.co.uk](mailto:ethan.a.smith@hotmail.co.uk).
