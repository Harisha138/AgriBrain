# frontend.py
import streamlit as st
from backend import agribrain
import os

st.set_page_config(
    page_title="AgriBrain - Farmer's AI Assistant",
    page_icon="🌾",
    layout="centered"
)

# Custom CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Roboto', sans-serif;
    }
    
    .chat-message {
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .user-message {
        background: #ffffff;
        color: #2c3e50;
    }
    
    .bot-message {
        background: #2ecc71;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<h1 style='text-align: center; color: #2ecc71;'>🌾 AgriBrain - Farmer's AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask your farming question..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user", avatar="user"):
        st.markdown(prompt)
    
    # Get AI response
    with st.spinner("Analyzing your query..."):
        try:
            response = agribrain.get_response(prompt)
            formatted_response = f"""
            <div class="chat-message bot-message">
                <h4>AgriBrain's Advice 🌱</h4>
                {response}
            </div>
            """
        except Exception as e:
            formatted_response = f"""
            <div class="chat-message bot-message" style="background-color: #e74c3c;">
                Error: {str(e)}
            </div>
            """
    
    # Display AI response
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(formatted_response, unsafe_allow_html=True)
    
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": formatted_response})