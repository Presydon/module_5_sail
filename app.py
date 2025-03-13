# ====================== Library Imports ====================== #
import os
import streamlit as st
from groq import Client
from dotenv import load_dotenv

# ====================== Load Environment Variables ====================== #
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

# ====================== Initialize Groq Client ====================== #
def initialize_client(api_key: str):
    if not api_key:
        st.error("API key is missing. Please set the GROQ_API_KEY in the environment variables.")
        return None
    return Client(api_key=api_key)

# ====================== Generate Chat Response ====================== #
def get_chat_response(client, user_input):
    if not client:
        return "Error: Client not initialized."
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
            model='llama-3.3-70b-versatile',
            temperature=0.8,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# ====================== Streamlit UI ====================== #
def main():
    st.set_page_config(page_title="Groq Chatbot", layout="centered")
    st.title("🤖 Groq AI Chatbot")
    
    # Initialize client
    client = initialize_client(API_KEY)
    
    # User input
    user_input = st.text_area("Enter your message:", height=100)
    
    if st.button("Send Message"):
        if user_input.strip():
            with st.spinner("Generating response..."):
                response = get_chat_response(client, user_input)
            st.subheader("Response:")
            st.write(response)
        else:
            st.warning("Please enter a message before submitting.")

if __name__ == "__main__":
    main()