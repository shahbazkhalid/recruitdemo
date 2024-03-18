import os, streamlit as st
import openai
import hmac
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        # if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
        if hmac.compare_digest(st.session_state["password"], os.environ.get("password")):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Main Streamlit app starts here

# Access the API key using os.environ
api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = api_key

from llama_index import VectorStoreIndex, SimpleDirectoryReader

# Define a simple Streamlit app
st.title("Resume Q/A Demo")
query = st.text_input("What would you like to ask? (e.g.: Who has python experience?)", "")

# If the 'Submit' button is clicked
if st.button("Submit"):
    if not query.strip():
        st.error(f"Please provide the search query.")
    else:
        try:
            # This example uses text-davinci-003 by default; feel free to change if desired
            documents = SimpleDirectoryReader("data").load_data()
            index = VectorStoreIndex.from_documents(documents)
            query_engine = index.as_query_engine()
            response = query_engine.query(query)
            st.success(response)
        except Exception as e:
            st.error(f"An error occurred: {e}")