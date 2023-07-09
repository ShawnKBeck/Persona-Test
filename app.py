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

input_box = st.empty()
prompt = input_box.text_input("Type your message here")

for message in st.session_state.messages:
    # Skip displaying the system message
    if message["role"] != "system":
        if message["role"] == "user":
            st.markdown(f'<p style="color: black;">{message["content"]}</p>', unsafe_allow_html=True)  # User messages in black
        else:
            st.markdown(f'<p style="color: gray;">{message["content"]}</p>', unsafe_allow_html=True)  # Assistant messages in gray

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<p style="color: black;">{prompt}</p>', unsafe_allow_html=True)  # User input in black
    input_box.text_input("Type your message here", value="")  # Clear the input box

    with st.spinner('Assistant is typing...'):
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
        st.markdown(f'<p style="color: gray;">{full_response}</p>', unsafe_allow_html=True)  # Assistant response in gray
    st.session_state.messages.append({"role": "assistant", "content": full_response})
