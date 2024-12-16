from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()]
)

# Configure the Generative AI model with the API key
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("API Key for Google Generative AI is not set. Please check your environment variables.")
    logging.error("API Key for Google Generative AI is not set.")
    raise ValueError("API Key for Google Generative AI is not set. Please check your environment variables.")

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    logging.info("Successfully configured Generative AI model.")
except Exception as e:
    logging.error(f"Error configuring Generative AI: {e}")
    st.error("Failed to configure the Generative AI model. Please try again later.")
    raise

# Function to handle query and generate output
def generate_response(query):
    try:
        with st.spinner('Generating response...'):
            response = model.generate_content(query)
            return response.text
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        st.error(f"An error occurred: {str(e)}")
        return "Sorry, I couldn't process your request. Please try again later."

# Streamlit page configuration
st.set_page_config(
    page_title="Mayank Smart Bot (TEXT)",
    page_icon="🤖",
    layout="centered"
)

# Add a header and description to the app
st.title("Mayank Smart Bot (TEXT)")
st.markdown("""
Welcome to the **Mayank Smart Bot**! Ask anything, and the bot will generate a response using Google's Generative AI.

**Instructions:**
- Enter your query in the text box below.
- Click on the **Submit** button to get a response.

---
""")

# Input text box for the user's query
query_input = st.text_input(
    "Input your query here", 
    placeholder="e.g., Explain quantum mechanics in simple terms",
    help="Enter a query you want the bot to answer."
)

# Submit button to process the query
if st.button("Submit"):
    if query_input.strip():
        try:
            logging.info(f"Received query: {query_input}")
            st.info("Processing your request...")  # Add informational message for user feedback
            response = generate_response(query_input)
            st.subheader("Response")
            st.write(response)
        except Exception as e:
            st.error("An unexpected error occurred. Please try again later.")
            logging.error(f"Unexpected error: {e}")
    else:
        st.warning("Please enter a query to get a response.")

# Footer section
st.markdown("""
---
Developed by Mayank Kumar | Powered by **Google Generative AI**

**Disclaimer:** This bot uses AI to generate responses. Please verify critical information from trusted sources.

---
**Security Note:** Your queries are processed via a third-party service. Avoid submitting sensitive or confidential information.
""")
