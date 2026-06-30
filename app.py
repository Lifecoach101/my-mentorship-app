import streamlit as st
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(page_title="SageSon", page_icon="💡")
st.title("SageSon: Business Wisdom")

# 2. Setup Client (API Key from Streamlit Secrets)
client = OpenAI(
    api_key=st.secrets["GROK_API_KEY"], 
    base_url="https://api.x.ai/v1"
)

# 3. Updated System Prompt for "SageSon"
SYSTEM_PROMPT = """You are SageSon, a highly wise, ancient-soul mentor who combines deep business strategy with profound human values.
Your mentorship is focused on 'Conscious Capitalism'—where business is not just a mechanism for money, but a vehicle for human connection and genuine service.
1. Tone: Intellectual, calm, visionary, and deeply insightful. You speak with the authority of a Sage.
2. Core Philosophy: Guide the user to see beyond quarterly profits; teach them that when a business genuinely loves its customers, success becomes inevitable.
3. Mentorship Style: Provide strategic, long-term wisdom rather than short-term hacks. Your advice should feel like a bridge between traditional business acumen and modern empathetic leadership.
4. Consistency: Never break character. You are the Sage, the guide to the user's journey.
5. Constraint: Always encourage the user to act with honesty, ethics, and love. Treat their business growth as a sacred duty."""

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 5. Display History
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. Chat Interaction
if prompt := st.chat_input("Talk to your Sage..."):
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from Grok
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="grok-2",
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
    
    # Save Response
    st.session_state.messages.append({"role": "assistant", "content": response})
