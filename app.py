import openai
import streamlit as st

st.title("ChatGPT-like clone")

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Define the behavior of your assistant
system_prompt = """
You are Shawn Beck and you will embody the presence of Shawn Beck...
"""  # Include the full system prompt here

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    # Include the system message as the first message
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

for message in st.session_state.messages:
    # Skip displaying the system message
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
