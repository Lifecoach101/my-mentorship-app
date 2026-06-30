import streamlit as st
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(page_title="SageSon", page_icon="💡")
st.title("SageSon: Business Wisdom")

# 2. Setup Groq Client
# Note: Hum GROQ_API_KEY use kar rahe hain
client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"], 
    base_url="https://api.groq.com/openai/v1" 
)

# 3. SageSon Persona
SYSTEM_PROMPT = """You are SageSon, a highly wise, ancient-soul mentor who combines deep business strategy with profound human values.
Your mentorship is focused on 'Conscious Capitalism'—where business is not just a mechanism for money, but a vehicle for human connection and genuine service."""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Talk to your Sage..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Groq lara Llama 3 model sab ton stable hai
        stream = client.chat.completions.create(
            model="llama3-8b-8192", 
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
