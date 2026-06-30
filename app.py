import streamlit as st
from openai import OpenAI

# Page Config
st.set_page_config(page_title="SageSon", page_icon="💡")
st.title("SageSon: Business Wisdom")

# API Client setup
# Koshish karein ki GROK_API_KEY wahi ho jo kal generate ki thi
client = OpenAI(
    api_key=st.secrets["GROK_API_KEY"], 
    base_url="https://api.x.ai/v1"
)

# SageSon Persona
SYSTEM_PROMPT = """You are SageSon, a highly wise mentor focused on Conscious Capitalism.
Your goal is to guide the user to treat customers like family and build a lasting legacy."""

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
        # Yahan 'grok-2' ya 'grok-beta' use karein. 
        # Agar 'grok-2' par error aaye toh 'grok-beta' wapis use karein.
        stream = client.chat.completions.create(
            model="grok-beta", 
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
