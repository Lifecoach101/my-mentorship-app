import streamlit as st
from openai import OpenAI # Grok API is compatible with OpenAI library

# 1. Page Configuration
st.set_page_config(page_title="Father's Wisdom", page_icon="👨‍💼")
st.title("Business Wisdom from Father")

# 2. Setup Client (API Key from Streamlit Secrets)
client = OpenAI(
    api_key=st.secrets["GROK_API_KEY"], 
    base_url="https://api.x.ai/v1" # Grok's API endpoint
)

# 3. System Prompt (The Persona)
SYSTEM_PROMPT = """You are a highly experienced, successful, and deeply caring father figure acting as a business mentor to your son. 
Your mentorship style is emotional, wise, and grounded in integrity. 
You believe that a company that loves and respects its customers will naturally achieve long-term success. 
Maintain this persona at all times. Never refer to yourself as an AI. 
Provide practical, actionable steps for your son."""

# 4. Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# 5. Display History on Page Load
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. Chat Interaction
if prompt := st.chat_input("Talk to your father..."):
    # Add User Message to History
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from Grok
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="grok-beta", # Or latest model version
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
    
    # Add Assistant Response to History
    st.session_state.messages.append({"role": "assistant", "content": response})